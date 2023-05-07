"""
Django settings for alcalasuena project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zbkckcq9&-n%clm(g45*2nyetxndk7tlysc1&a&b1onf#jwz*r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
ALLOWED_HOSTS = ['localhost', '10.0.0.52', 'ec2-52-211-39-126.eu-west-1.compute.amazonaws.com', 'alcalasuena.es', 'www.alcalasuena.es']


# Application definition

INSTALLED_APPS = [
    'core',
    'bands',
    'contest',
    'archive',
    'tastypie',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'alcalasuena.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates') ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'contest.context_processors.contest_status',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]



WSGI_APPLICATION = 'alcalasuena.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False
SITE_ID = 1

INTERNAL_IPS = ('127.0.0.1',)
TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 250

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = ROOT_DIR + '/static'
MEDIA_ROOT = ROOT_DIR + '/media'
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/contest/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'width':'100%',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Format', 'FontSize','TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList', '-',  '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', 'Link', 'Unlink'],
        ]
    },
}

EMAIL_ACTIVE = False
CONTEST_ACTIVE = True
CONTEST_CLOSED = True
APP_VISIBLE = False
SCHEDULE_ACTIVE = False
PUBLIC_VOTE = False
ARCHIVE_YEARS = []
DELETE_ENABLED = False

# Old Google Universal Analytics ID (starts with "UA-")
GOOGLE_ANALYTICS_UA = ''
# New Google Analytics Tag ID (starts with "G-")
GOOGLE_ANALYTICS_TAG = ''

from alcalasuena.settings_secret import *
