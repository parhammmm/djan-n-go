from common import *

DEBUG = False 
TEMPLATE_DEBUG = DEBUG

IS_PRODUCTION = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

#list of ip addresses where the code should be deployed to
HOST_IPS = []

#username that has access to the hosts
HOST_USERNAME = ''

#path to the pem file for the HOST_USERNAME to gain access to the servers
PEM_KEY_PATH = ''

# [ Amazon S3 ] 
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
# DEFAULT_FILE_STORAGE = 'common.s3.MediaS3BotoStorage'

# The path to the S3 storage class - used for handling static files
# STATIC_FILE_STORAGE = 'common.s3.StaticS3BotoStorage'
