"""
Django settings for antropoloops project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.abspath( os.path.dirname(__file__) )

# Assets (CSS, JavaScript, Images)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'antropoloops', 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'assets/static')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ENV_PATH, '..', 'assets/media')

DEFAULT_FILE_STORAGE = 'antropoloops.storage_backends.MediaStorage'
IMAGEKIT_DEFAULT_FILE_STORAGE = 'antropoloops.storage_backends.MediaStorage'
S3_MEDIA_FOLDER = 'media'

# Registration

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'goodbye'

# Application definition

PROJECT_ADMIN_APPS = [
    'apps.custom_django_admin',
    'apps.registration',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CONTRIB_APPS = [
    'django_countries',
    'adminsortable',
    'ckeditor',
    'ckeditor_uploader',
    'imagekit',
    'colorful',
    'storages',
    'rest_framework',
]

PROJECT_APPS = [
    'apps.feather',
    'apps.limited_textarea_widget',
    'apps.image_preview_widget',
    'apps.autoslug_widget',
    'apps.models',
    'apps.dashboard',
]

INSTALLED_APPS = PROJECT_ADMIN_APPS + DJANGO_APPS + CONTRIB_APPS + PROJECT_APPS

# Middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'antropoloops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ 'templates', 'antropoloops/templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'antropoloops.templatetags.antropoloops',
                'apps.feather.templatetags.feather_tags'
            ],
        },
    },
]

WSGI_APPLICATION = 'antropoloops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# CKEDITOR
# CKEDITOR_UPLOAD_PATH = "/inline-images/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'width'  : '100%',
        'extraPlugins': 'videodetector,',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList'],
            ['Link', 'Unlink', 'Image', 'VideoDetector'],
            ['RemoveFormat', 'Source'],
        ],
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL  = "/static/admin/js/vendor/jquery/jquery.min.js"


#
# Import private settings
#

from .private_settings import *
