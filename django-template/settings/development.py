from common import *
from os import path

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('{{ project_directory }}','development.db')
    }
}

DEBUG = True