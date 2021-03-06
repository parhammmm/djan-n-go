import os, boto, multiprocessing, gzip
from fabric.api import cd, sudo, run, env
from boto.s3.key import Key
from settings.common import AWS_KEY_FILENAME, PROJECT_DIR, STATIC_ROOT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

CONFIG = {
	'SITE_NAME': '{{project_name}}',
	'INSTALL_DIR': PROJECT_DIR, 
	'REPO': '',
	'GUNICORN_PORT': 8000,
	'PRODUCTION_HOSTS': [''],
}

AWS_STORAGE_BUCKET_NAME = ''

def production():
	env.user = 'ubuntu' 
	env.hosts = CONFIG['PRODUCTION_HOSTS']
	env.key_filename = [	
		AWS_KEY_FILENAME
	]
	env.forward_agent = True

def deploy():
	with cd(CONFIG['INSTALL_DIR']):
		run('git checkout master') 
		run('git pull origin master') 
		#virtualenv('pip install -r requirements.txt')
		virtualenv('python manage.py migrate')
		virtualenv('python manage.py collectstatic')
		virtualenv('fab deploy_static')
		restart_app()

def pull():
	with cd(CONFIG['INSTALL_DIR']):
		run('git pull origin master') 

def deploy_admin_static():
	_deploy_folder(os.path.join(STATIC_ROOT, 'admin'))

def deploy_static():
	print 'locating files'
	dirs = [
		os.path.join(STATIC_ROOT, 'js'),
		os.path.join(STATIC_ROOT, 'css'),
		os.path.join(STATIC_ROOT, 'img'),
		os.path.join(STATIC_ROOT, 'vendor'),
	]
	for dir in dirs:
		_deploy_folder(dir)

def add_rank_cron():
	_add_cron('rank')

def _add_cron(command):
	entry = '*/5 * * * * %s/virtualenv/bin/python %s/manage.py %s --settings=%s' % (CONFIG['INSTALL_DIR'], CONFIG['INSTALL_DIR'], command, 'settings.production')
	append = 'crontab -l | { cat; echo "%s"; } | crontab -' % entry
	sudo(append)

def initial_setup():
	sudo('apt-get update')
	sudo('apt-get upgrade')
	sudo('apt-get install --assume-yes python python-dev g++ make curl git gcc vim')
	sudo('apt-get install --assume-yes mysql-client python-mysqldb libmysqlclient-dev')

	run('git clone %(REPO)s ~/%(SITE_NAME)s' % CONFIG)
	sudo('mv ~/%(SITE_NAME)s/ /srv/' % CONFIG )

	with cd('%(INSTALL_DIR)s/bin' % CONFIG):
		sudo('./install.sh')

	setup_nginx()

def restart_app():
	sudo('supervisorctl stop all')
	sudo('supervisorctl start all')

def stop_gunicorn():
	sudo("pkill -9 -f gunicorn")

def start_gunicorn():
	with cd(CONFIG['INSTALL_DIR']):
		virtualenv('python manage.py run_gunicorn --bind 127.0.0.1:%(GUNICORN_PORT)s --workers 2 -D' % CONFIG)

def restart_gunicorn():
	stop_gunicorn()
	start_gunicorn()

def restart_nginx():
	sudo('/etc/init.d/nginx restart')

def setup_nginx():
	sudo('apt-get install --assume-yes nginx')

	sudo('cp %(INSTALL_DIR)s/etc/nginx_staging.conf /etc/nginx/sites-available/%(SITE_NAME)s_staging.conf' % CONFIG)
	sudo('cp %(INSTALL_DIR)s/etc/nginx_production.conf /etc/nginx/sites-available/%(SITE_NAME)s_production.conf' % CONFIG)

	sudo('ln -s /etc/nginx/sites-available/%(SITE_NAME)s_staging.conf /etc/nginx/sites-enabled/%(SITE_NAME)s_staging.conf' % CONFIG)
	sudo('ln -s /etc/nginx/sites-available/%(SITE_NAME)s_production.conf /etc/nginx/sites-enabled/%(SITE_NAME)s_production.conf' % CONFIG)
	restart_nginx()

def virtualenv(command):
	with cd(CONFIG['INSTALL_DIR']):
		sudo('source %s/virtualenv/bin/activate && %s' % (CONFIG['INSTALL_DIR'], command))

def _deploy_folder(path, parallel_upload = 20):
	print 'locating files'
	paths = []
	for path, dir, files in os.walk(path): 
		for file in files: 
			paths.append((file, path))

	_upload_files(paths, parallel_upload)

def _upload_files(paths, parallel_upload):
	buckets = []
	print 'opening connections'

	sysname, nodename, release, version, machine = os.uname()

	for i in range(parallel_upload):
		connection = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) 
		bucket = connection.get_bucket(AWS_STORAGE_BUCKET_NAME) 
		buckets.append(bucket)

	def chunks(l, n):
		for i in xrange(0, len(l), n):
				yield l[i:i+n]
	chunked_paths = chunks(paths, parallel_upload)
	print 'uploading'
	for chunk in chunked_paths:
		ps = []
		i = 0
		for path in chunk:
			bucket = buckets[i % parallel_upload]
			p = multiprocessing.Process(target=_s3_put, args=(bucket,)+path)
			p.start()
			ps.append(p)
			i += 1

		for p in ps:
			p.join()

def _s3_put(bucket, file, path):
	k = Key(bucket) 
	relpath = os.path.relpath(os.path.join(path, file)) 
	localpath = relpath
	filepath, ext = os.path.splitext(localpath)
	headers = {}
	if ext in ['.js', '.css']:
		headers['Content-Encoding'] = 'gzip'
		localpath = _gzip(file, path)

	k.key = relpath
	k.set_contents_from_filename(localpath, headers=headers)
	try:
		k.set_acl('public-read')
		print 'sent...', relpath
	except:
		print 'failed...', relpath

def _gzip(file, path):
	temp_dir = "temp"
	gzip_path = '%s/%s' % (temp_dir, file)
	fullpath = os.path.join(path, file)

	f_in = open(fullpath, 'rb').read()
	if not os.path.exists(temp_dir):
		os.makedirs(temp_dir)
	f_out = gzip.open(gzip_path, 'wb')
	f_out.write(f_in)
	f_out.close()
	return gzip_path 
