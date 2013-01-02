from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from stat import *

import os
from os.path import isfile
import time
from settings.common import INSTALLED_APPS
# from settings.production import S3_STATIC_PATH, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

############
#### Usage
############
#
# - To install a new instance run, first update the below config then run:
#		
#	1)	fab add_host_user
#	2)	fab production install
#
#
# - Setting up SSH Key forwarding:
#
# 	1) Load SSH agent:
#		ssh-agent bash
#
# 	2) Add SSH Key:
# 		ssh-add
#
#	3) Check it's been added
# 		ssh-add -l
#
# 	4) Allow Agent Forwarding is allowed, open .git/config
#		and add:
#
#			host xxx.xxx.xxx.xxx
#			  ForwardAgent yes
#
#	5) Make sure Agent Forwarding is allowed on the server, look at the template configuration in /etc/sshd_config
#
# - Git workflow:
#
#	http://nvie.com/posts/a-successful-git-branching-model/
#

############
#### Deployment Configuration
############

CONFIG = {
	'ADMIN_USERNAME': '',
	'PRODUCTION_HOSTS': [],
	'STAGING_HOSTS': [],

	'SITE_NAME': '',
	'PROJECT_BASEDIR': '',
	'PROJECT_REPO': '',
	'DATABASE_USERNAME': '',
	'DATABASE_PASSWORD': '',
	'DATABASE_TABLENAME': '',
	'GUNICORN_PORT': 0,

	#### S3 Config
	# 'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
	# 'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
	# 'AWS_STORAGE_BUCKET_NAME': AWS_STORAGE_BUCKET_NAME,
	# 'STATIC_PATH': S3_STATIC_PATH,
}

############
#### Mappings for local folders to static server
############

# mappings = {
# 	'group_name': {
# 		'options': {
# 			'flatten': boolean [default=False]
# 		},
# 		'files': {
# 			'path/to/destination/' : [
# 				'path/to/source/1',
# 				'path/to/source/2',
#				...
# 			]
# 		},
# 	},
#	...
# }

mappings = {
	'admin': {
		'files': {
			'%(STATIC_PATH)sadmin' % CONFIG: [
				'%(STATIC_PATH)sadmin' % CONFIG
			]
		},
	},
	# 'grappelli': {
	# 	'files': {
	# 		'%(STATIC_PATH)sgrappelli' % CONFIG: [
	# 			'%(STATIC_PATH)sgrappelli' % CONFIG
	# 		]
	# 	},
	# },
	'scripts': {
		'options': {
			'flatten': True
		},
		'files': {
			'%(STATIC_PATH)sr' % CONFIG : [
				'%(STATIC_PATH)sdist/release' % CONFIG
			]
		},
	},
	'images': {
		'options': {
			'flatten': True
		},
		'files': {
			'%(STATIC_PATH)simg' % CONFIG : [
				'%(STATIC_PATH)sdist/img' % CONFIG
			]
		}
	},
	'fonts': {
		'options': {
			'flatten': True
		},
		'files': {
			'%(STATIC_PATH)sfonts' % CONFIG : [
				'%(STATIC_PATH)sdist/fonts' % CONFIG
			]
		}
	},
	'in_html': {
		'options': {
			'flatten': True,
		},
		'files': {
			'%(STATIC_PATH)sassets/img/in_html' % CONFIG : [
				'%(STATIC_PATH)sdist/assets/img/in_html' % CONFIG
			]
		}
	},
}

# scp parham@176.58.114.220:/etc/ssh/sshd_config sshd_config

############
#### Host Configurations
############

def vagrant():
	env.user = 'vagrant'
	env.hosts = ['127.0.0.1:2200']
	env.key_filename = '/home/parham/.vagrant.d/insecure_private_key'

def production():
	env.user = CONFIG['ADMIN_USERNAME']
	env.hosts = CONFIG['PRODUCTION_HOSTS']
	env.forward_agent = True

############
#### Fabric Tasks
############

def deploy():
	deploy_scripts()
	pull()
	migrate()
	restart_gunicorn()

def migrate():
	virtualenv('python manage.py migrate')

def pull():
	with cd(_get_project_dir()):
		run('git pull origin master') 

def deploy_scripts():
	deploy_static('scripts')

def deploy_in_html():
	deploy_static('in_html')

def deploy_static(groups=[]):
	"""
	Build and deploy the static files to S3, if an empty list is given for groups, files from all groups will be
	deleted and replaced with their local counterparts
	"""

	if isinstance(groups, basestring):
		groups = [groups]

	if not groups:
		groups = mappings.keys()
		if not confirm("Also update admin static files? (Not recommended as very slow!)"):
			groups.remove('admin')
			groups.remove('grappelli')

	conn = S3Connection(CONFIG['AWS_ACCESS_KEY_ID'], CONFIG['AWS_SECRET_ACCESS_KEY'])
	bucket = conn.get_bucket(CONFIG['AWS_STORAGE_BUCKET_NAME'])
	bucket = conn.get_bucket(CONFIG['AWS_STORAGE_BUCKET_NAME'])

DEFAULTS = {
		'flatten': False,
	}

	_build_static()

	for group in groups:
		try:
			options = mappings[group]
		except KeyError:
			print "[ERROR] No group with the name '%s' found in mappings." % group
			continue

		try:
			options = mappings[group]['options']
		except KeyError:
			options = DEFAULTS

		# Set options without values to their defaults
		for option in DEFAULTS:
			try:
				selection = options[option]
			except KeyError:
				options[option] = DEFAULTS[option]

		dest, sources = mappings[group]['files'].items()[0]

		# Delete everything in the given destination
		for key in bucket.list(prefix=dest):
			key.delete()
		print "[DELETED] %s" % dest

		# Upload everything from the specified sources	
		for source in sources:
			_s3_upload_folder_recursive(bucket, source, dest, options['flatten'])

def uname():
	run('uname -a')

def reboot():
	sudo('shutdown -r now')

def add_host_user():
	env.user = 'root'
	env.password = fabric.operations.prompt("Host's root password?")
	sudo('add user %(ADMIN_USERNAME)s' % CONFIG)
	sudo('usermod -a -G sudo %(ADMIN_USERNAME)s' % CONFIG)

def install():
	uname()

	sudo('apt-get update')

	# Dependencies for building frontend files 
	sudo('apt-get install npm')
	sudo('npm install -g grunt')
	sudo('npm install -g bbb')

	sudo('apt-get install --assume-yes python-dev libpq-dev curl git gcc vim')
	sudo('curl http://python-distribute.org/distribute_setup.py | python')
	sudo('curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python')
	sudo('pip install virtualenv')
	_setup_instance()
	_setup_postgresql()
	_setup_nginx()
	_post_install()

def run_gunicorn():
	with cd(_get_project_dir()):
		virtualenv('python manage.py run_gunicorn --bind 127.0.0.1:%(GUNICORN_PORT)s --workers 2 -D settings/production.py' % CONFIG)

def _get_gunicorn_master_pid():
	processes = sudo('ps aux | less | grep gunicorn | sed -s "s/root\s*//" | sed -s "s/ .*//g"')
	return processes.split('\r\n')[0]

def stop_gunicorn():
	pid = _get_gunicorn_master_pid()
	sudo('kill %s' % pid)

def restart_gunicorn():
	pid = _get_gunicorn_master_pid()
	sudo('kill -HUP %s' % pid)

def restart_postgresql():
	sudo('/etc/init.d/postgresql restart')

def restart_nginx():
	sudo('/etc/init.d/nginx restart')

def reset_database():
	if confirm("WARNING: This will delete the entire database together with its data! Are you sure?"):
		drop_postgresql_db()
		create_postgresql_db()
		virtualenv('python manage.py syncdb --all')

		# Load base fixtures as they aren't automatically registered in South
		virtualenv('python manage.py loaddata settings/fixtures/initial_data.json')
		virtualenv('python manage.py migrate --fake')

def create_postgresql_user():
	sudo('psql -d postgres -U postgres -c "CREATE USER %(DATABASE_USERNAME)s WITH password \'%(DATABASE_PASSWORD)s\'"' % CONFIG, user='postgres')

def create_postgresql_db():
	sudo('psql -d postgres -U postgres -c "CREATE DATABASE %(DATABASE_TABLENAME)s WITH OWNER %(DATABASE_USERNAME)s"' % CONFIG, user='postgres')

def drop_postgresql_db():
	sudo('psql -d postgres -U postgres -c "DROP DATABASE %(DATABASE_TABLENAME)s";' % CONFIG, user='postgres')

def django_syncdb():
	virtualenv('python manage.py syncdb')

def django_collectstatic():
	virtualenv('python manage.py collectstatic')

def django_createsuperuser():
	virtualenv('python manage.py createsuperuser')

def migration_init():
	local('python manage.py syncdb')
	for app in INSTALLED_APPS:
		if not app.find('apps.'):
			_app = app.split('apps.')[1]
			if _app in ['api', 'search', 'landing', 'utils']:
				continue
			local('python manage.py convert_to_south %s' % _app)
			# local('python manage.py schemamigration %s --initial' % _app)

############
#### Private functions used in Fabric Tasks
############

def _post_install():
	# Image decoders - install
	sudo('apt-get install --assume-yes libjpeg8 libpng12-0 libfreetype6 zlib1g libjpeg-dev')

	# Image decoders - make the syminks, solves 64bit compatibility issues
	sudo('ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/')
	sudo('ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/')
	sudo('ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg-dev')
	sudo('ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib')

	# Reinstall PIL
	virtualenv('pip install -I PIL')

	# Sync database with django app
	django_syncdb()

	# Add the first django superuser
	django_createsuperuser()

def _setup_instance():
	sudo('git clone %s %s' % (CONFIG['PROJECT_REPO'], _get_project_dir()) ) 

	with cd(_get_project_dir()):
		sudo('virtualenv virtualenv')

	with cd(_get_project_dir()):
		virtualenv('pip install -r requirements.txt')

def _setup_postgresql():
	sudo('apt-get install --assume-yes postgresql-9.1')
	sudo('cp %setc/pg_hba.conf /etc/postgresql/9.1/main/pg_hba.conf' % _get_project_dir())
	restart_postgresql()
	create_postgresql_user()
	create_postgresql_table()

def _setup_nginx():
	sudo('apt-get install --assume-yes nginx')

	sudo('cp %setc/nginx.conf /etc/nginx/sites-available/%s.conf' % (_get_project_dir(), CONFIG['SITE_NAME']))

	sudo('ln -s /etc/nginx/sites-available/%(SITE_NAME)s.conf /etc/nginx/sites-enabled/%(SITE_NAME)s.conf' % CONFIG)
	restart_nginx()

def _get_project_dir():
	return '%(PROJECT_BASEDIR)s%(SITE_NAME)s/' % CONFIG

def _s3_upload_folder(bucket, source, destination):

	for f in os.listdir(source):
		if not isfile(os.path.join(source, f)):
			continue

		if f.endswith('.swp') or f.startswith('.'):
			continue

		filename_source = '%s/%s' % (source, f)
		filename_destination = '%s/%s' % (destination, f)

		_s3_upload_file (bucket, filename_source, filename_destination)

def _s3_upload_folder_recursive (bucket, source, destination, flatten=True):

	for root, dirs, files in os.walk(source):

		for f in files:
			if f.endswith('.swp') or f.startswith('.') :
				continue

			filename_source = '%s/%s' % (root, f)
			filename_destination = '%s/%s' % (destination, f)

			if not flatten:
				filename_destination = filename_source

			_s3_upload_file (bucket, filename_source, filename_destination)

def _s3_upload_file (bucket, source, destination):
	modify_time = os.stat(source)[ST_MTIME]

	key = bucket.get_key(destination)

	if key is None:
		key = Key(bucket)
		key.key = destination

	if key.last_modified is None or time.ctime(modify_time) > time.strptime(key.last_modified, '%a, %d %b %Y %H:%M:%S %Z'):
		fid = file(source, 'r')
		key.set_contents_from_file(fid)
		key.set_acl('public-read')
		print '[UPLOADED] %s' % source

def _build_static():
	local('python manage.py collectstatic --noinput') 

	# Build the new static files
	with lcd(CONFIG['STATIC_PATH']):
		local('bbb release')

def virtualenv(command):
	with cd(_get_project_dir()):
		sudo('source %svirtualenv/bin/activate && %s' % (_get_project_dir(), command))
