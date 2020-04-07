import os
from .settings import BASE_DIR

#
# Site state settings
#

DEBUG = True

#
# Secret key, move it from settings or generate it using
# https://pypi.org/project/django-generate-secret-key/
#

SECRET_KEY = ''

#
# Allowed hosts
# keep localhost for local server
#

ALLOWED_HOSTS = [ 'localhost', ]

#
# Database
# SQLite3 is default, change it for whatever one you are using
#

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#
# Mail settings
#

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST = 'localhost'
    DEFAULT_FROM_EMAIL = ''
else:
    EMAIL_HOST = 'localhost'
    DEFAULT_FROM_EMAIL = ''
    EMAIL_PORT = '25'
    EMAIL_USE_TLS = True

#
#  S3 Configuration
#  S3 conf if using S3 buckets
#

S3_USER = ''
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''
AWS_S3_CUSTOM_DOMAIN = ''
