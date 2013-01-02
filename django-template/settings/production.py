from common import *

DEBUG = False 
TEMPLATE_DEBUG = DEBUG

IS_PRODUCTION = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                	 # Not used with sqlite3.
        'HOST': '',                      		 # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      		 # Set to empty string for default. Not used with sqlite3.
    }
}

# [ Amazon S3 ] - Uncomment if your using S3 in production
# S3 bucket URL. Make sure to use a trailing slash.
# S3_URL = ''

# Amazon Web Services access key, as a string
# AWS_ACCESS_KEY_ID = ''

# Amazon Web Services secret access key, as a string
# AWS_SECRET_ACCESS_KEY = ''

# Amazon Web Services storage bucket name, as a string
# AWS_STORAGE_BUCKET_NAME = ''

# AWS_QUERYSTRING_AUTH = False 

# The bucket directory which holds static files. Make sure to use a
# trailing slash.
# S3_STATIC_PATH = 'static/'

# The bucket directory which holds media files. Make sure to use a
# trailing slash.
# S3_MEDIA_PATH = 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = S3_URL+S3_MEDIA_PATH

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
# STATIC_URL = S3_URL+S3_STATIC_PATH

# The path to the S3 storage class - used for handling media files
# DEFAULT_FILE_STORAGE = 'apps.utils.s3.MediaS3BotoStorage'

# The path to the S3 storage class - used for handling static files
# STATIC_FILE_STORAGE = 'apps.utils.s3.StaticS3BotoStorage'
