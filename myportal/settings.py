"""
Django settings for myportal project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from .local_settings import *
from pathlib import Path
from myportal import search_fields

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# This is a general Django setting if views need to redirect to login
# https://docs.djangoproject.com/en/3.2/ref/settings/#login-url
LOGIN_URL = '/login/globus'

# This dictates which scopes will be requested on each user login
SOCIAL_AUTH_GLOBUS_SCOPE = [
    'urn:globus:auth:scope:search.api.globus.org:search',
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'globus_portal_framework',
    'social_django',
    'gsearch',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'globus_portal_framework.middleware.ExpiredTokenMiddleware',
    'globus_portal_framework.middleware.GlobusAuthExceptionMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

# Authentication backends setup OAuth2 handling and where user data should be
# stored
AUTHENTICATION_BACKENDS = [
    'globus_portal_framework.auth.GlobusOpenIdConnect',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'myportal.urls'

BASE_TEMPLATES = 'dataset-search/globus-portal-framework/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'myportal' / 'templates',
                 BASE_DIR / 'gsearch' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'globus_portal_framework.context_processors.globals',
                'gsearch.context_processors.settings_variables',
            ],
        },
    },
]

WSGI_APPLICATION = 'myportal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    BASE_DIR / 'myportal' / 'static',
]

STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SEARCH_INDEXES = {
    'dataset-search': {
        'name': 'NSF NCAR RDA Dataset search index',
        'uuid': 'fc7218fe-742c-4112-ab05-fc40472ced92',
        'facets': [
          {
              'name': 'Temporal range start',
              'field_name': 'temporal_range_start',
              'type': 'date_histogram',
              'date_interval': 'year',
        },
          {
              'name': 'Temporal range end',
              'field_name': 'temporal_range_end',
              'type': 'date_histogram',
              'date_interval': 'year',
        },
          {
            'name': 'Variables',
            'field_name': 'variables'
          },
          {
            'name': 'GCMD Keywords',
            'field_name': 'gcmd_keywords'
          },
          {
            'name': 'Platform',
            'field_name': 'platform'
          },
          {
            'name': 'Instrument',
            'field_name': 'instrument'
          },
        ],
        'fields': [
          ("title", search_fields.title),
          ("globus_app_link", search_fields.globus_app_link),
          ("dataset_url", search_fields.dataset_url),
          ("https_url", search_fields.https_url),
          ("search_highlights", search_fields.search_highlights),
        ],
    }
}

