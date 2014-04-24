from common import *
import os

DOMAIN = 'localhost:8080'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'development.db')
    }
}

ALLOWED_HOSTS = [
    '*'
]

DEBUG = True
