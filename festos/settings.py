# -*- coding: utf-8 -*-

# Django settings for demoproject project.
from os.path import abspath, dirname, join, pardir

ugettext = lambda s: s

# the root project should be the folder before so there
# can be shared statics living in festos site folder
# there are two pardir because the first remove the settings.py
# and the second one got to the actual parent
PROJECT_ROOT = abspath(join(abspath(__file__), pardir, pardir))
PROJECT_NAME = u"Festos"

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ANONYMOUS_USER_ID = -1

ADMINS = (
    ('festos', 'festos@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        # Or path to database file if using sqlite3.
        'NAME': join(PROJECT_ROOT, 'festos.sqlite3'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Toronto'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-ca'

LANGUAGES = (
    ('en', ugettext('English')),
    ('es', ugettext('Español')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(dirname(abspath(__file__)), 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '91j9vq3vvc%5z3@)(&amp;o@!*tv9pc(@_12^4v@r&amp;l1y5dtivdaos'

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
    'django_pdb.middleware.PdbMiddleware',
    'userena.middleware.UserenaLocaleMiddleware',
    'documents.middleware.DocumentGuardianMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'festos.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'festos.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(dirname(abspath(__file__)), 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # "django.core.context_processors.auth",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.csrf",
    "festos.context_processors.project_name",
    "festos.context_processors.current_date",
    # "base.context_processors.google_api_key",
    # "base.context_processors.google_analytics_code",
    "festos.context_processors.debug",
    "festos.context_processors.accounts",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'pipeline',         # necessary for compression and docviewer templates
    'djcelery',         # necessary for python manage.py celery worker
    'celery_haystack',  # necessary for automatic rebuild_index
    'haystack',         # necessary for manual rebuild_index
    'django_pdb',
    'bootstrapform',
    'userenabootstrap',
    'userena',
    'guardian',
    'easy_thumbnails',
    'docviewer',
    'documents',
    'accounts',
    'django_zotero',
    'django_ses',
    'taggit',
    'festos',
)

# Userena - Guardian configuration
AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.Profile'
USERENA_SIGNIN_REDIRECT_URL = '/documents/'
#LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
SIGNUP_URL = '/accounts/signup/'
GUARDIAN_RENDER_403 = True
USERENA_DISABLE_SIGNUP = False
USERENA_ACTIVATION_REQUIRED = False
USERENA_SIGNIN_AFTER_SIGNUP = True

USER_URL = '/accounts/'

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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Pipeline configuration
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE = False
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'

# Celery configuration
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERYD_TASK_TIME_LIMIT = 86400  # 24 hours
CELERYD_TASK_SOFT_TIME_LIMIT = 86400
#CELERYD_LOG_FILE = "celeryd.log" --deprecated
#CELERYD_LOG_LEVEL = "DEBUG" --deprecated


#Haystack configuration
import os
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
        # 'EXCLUDED_INDEXES': [
        # 'docviewer.search_indexes.PageIndex',
        # ]
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'

# Docviewer Configuration
DOCVIEWER_DOCUMENT_ROOT = join(MEDIA_ROOT, 'docs/')
DOCVIEWER_DOCUMENT_URL = '/media/docs/'
DOCVIEWER_IMAGE_FORMAT = 'png'

from docviewer.pipeline import *
