# Django settings for {{ project_name }} project
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

IS_PRODUCTION = False
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

ADMINS = (('Admin Name', 'admin@example.com'),)

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-GB'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

FIXTURE_DIRS = (
	# The directories where additional fixtures are stores
	os.path.join(PROJECT_DIR, 'settings', 'fixtures'),
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static', 'dist')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	# Put strings here, like "/home/html/static" or "C:/www/django/static".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_DIR, 'static', 'src'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	# 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '{{secret_key}}'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
	# 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'pipeline.middleware.MinifyHTMLMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.static",
	"django.core.context_processors.tz",
	"django.contrib.messages.context_processors.messages",
	"apps.common.context_processors.debug_mode",
	"apps.common.context_processors.is_production",
	"django.core.context_processors.request",
)

ROOT_URLCONF = 'apps.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'settings.wsgi.application'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.contenttypes',
	'django.contrib.humanize',
	# Uncomment the next line to enable the admin:
	'django.contrib.admin',
	'pipeline',
	'gunicorn',
	'storages',
	# Uncomment the next line to enable admin documentation:
	# 'django.contrib.admindocs',
	'south',
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/'

AWS_KEY_FILENAME = os.path.join(PROJECT_DIR, 'etc/keys/keyname.pem')

# Amazon Web Services access key, as a string
AWS_ACCESS_KEY_ID = ''

# Amazon Web Services secret access key, as a string
AWS_SECRET_ACCESS_KEY = ''

AWS_CLIENT_SECRET_KEY = '' 

AWS_STORAGE_BUCKET_NAME = '' 

# [MAILGUN]
#EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
#MAILGUN_ACCESS_KEY = ''
#MAILGUN_SERVER_NAME = ''

PIPELINE_CSS = {
	'landing': {
		'source_filenames': (
			'css/libs/normalize.css',
			'vendor/jquery.dropdown/css/*.css',
			'css/modules/landing.css',
		),
		'output_filename': 'css/{{ project_name }}.landing.min.css',
	},
	'lavashaki': {
		'source_filenames': (
			'vendor/bootstrap/css/bootstrap.css',
			'vendor/bootstrap/css/bootstrap-theme.css',
			'vendor/jquery.dropdown/css/*.css',
			'css/styles.css',
		),
		'output_filename': 'css/{{ project_name }}.min.css',
	},
}

PIPELINE_JS = {
	'modernizer': {
		'source_filenames': (
			'js/libs/modernizer.js',	
		),
		'output_filename': 'js/modernizer.min.css',
	},
	'landing': {
		'source_filenames': (
			'js/libs/jquery.js',
			'vendor/jquery.dropdown/js/*.js',
			'js/plugins/jquery/jquery.backstretch.js',
			'js/scripts/landing.js',	
		),
		'output_filename': 'js/{{ project_name }}.landing.min.css',
	},
	'main': {
		'source_filenames': (
			'js/libs/handlebars.js',
			'js/templates/*.handlebars',
			'js/libs/jquery.js',
			'js/libs/lodash.underscore.js',
			'js/libs/backbone.js',
			'js/plugins/jquery/*.js',
			'js/plugins/backbone/*.js',
			'vendor/bootstrap/js/*.js',
			'vendor/jquery.dropdown/js/*.js',
			'js/main.js',
			'js/modules/*.js',
			'js/app.js',
		),
		'output_filename': 'js/{{ project_name }}.min.js',
	},
}

PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'

PIPELINE_TEMPLATE_EXT = '.handlebars'
PIPELINE_TEMPLATE_FUNC = 'Handlebars.compile'
PIPELINE_TEMPLATE_NAMESPACE = 'Handlebars.templates'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
		},
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}
