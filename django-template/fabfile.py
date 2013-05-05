import os, glob, boto, multiprocessing
from fabric.api import cd, sudo, run, env
from boto.s3.key import Key
from settings import common

CONFIG = {
	'SITE_NAME': '{{ project_name }}',
	'INSTALL_DIR': common.PROJECT_DIR, 
	'REPO': common.MAIN_REPO, 
	'GUNICORN_PORT': 8000,
}

def staging():
	from settings import staging
	_set_host_config(staging)

def production():
	from settings import production
	_set_host_config(production)

def _set_host_config(config):
	env.user = config.HOST_USERNAME 
	env.hosts = config.HOST_IPS 
	env.key_filename = [
		config.PEM_KEY_PATH
	]
	env.forward_agent = True
	env['static_root'] = config.STATIC_ROOT
	env['aws_key'] = config.AWS_ACCESS_KEY_ID
	env['aws_secret'] = config.AWS_SECRET_ACCESS_KEY
	env['aws_s3bucket'] = config.AWS_STORAGE_BUCKET_NAME

def deploy():
	with cd(CONFIG['INSTALL_DIR']):
		run('git pull origin master') 
		virtualenv('pip install -r requirements.txt')
		virtualenv('python manage.py migrate')
		virtualenv('python manage.py collectstatic')
		virtualenv('fab deploy_static')

def deploy_admin_static():
	_deploy_folder(os.path.join(env.static_root, 'admin'))

def deploy_static():
	print 'locating files'
	paths = []
	dirs = [
		os.path.join(env.static_root, 'js'),
		os.path.join(env.static_root, 'css'),
		os.path.join(env.static_root, 'img'),
	]
	for dir in dirs:
		for file in glob.glob(os.path.join(dir, '*')):
			if os.path.isfile(file):
				paths.append((file, dir))

	_upload_files(paths, 10)

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

def stop_gunicorn():
	sudo("ps auxww | grep gunicorn | awk '{print $2}' | xargs kill -9")

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
	for i in range(parallel_upload):
		connection = boto.connect_s3(env.aws_key, env.aws_secret) 
		bucket = connection.get_bucket(env.aws_s3bucket) 
		buckets.append(bucket)

	def chunks(l, n):
		for i in xrange(0, len(l), n):
				yield l[i:i + n]
	chunked_paths = chunks(paths, parallel_upload)
	print 'uploading'
	for chunk in chunked_paths:
		ps = []
		i = 0
		for path in chunk:
			bucket = buckets[i % parallel_upload]
			p = multiprocessing.Process(target=_s3_put, args=(bucket,) + path)
			p.start()
			ps.append(p)
			i += 1

		for p in ps:
			p.join()

def _s3_put(bucket, file, path):
	k = Key(bucket) 
	relpath = os.path.relpath(os.path.join(path, file)) 

	k.key = relpath
	k.set_contents_from_filename(relpath)
	try:
		k.set_acl('public-read')
		print 'sent...', relpath
	except:
		print 'failed...', relpath
