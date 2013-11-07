""" Django settings

Configuration settings for DuJour project.

"""

import os

from datetime import datetime

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Dujour Team', 'info@dujour.im'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.mysql',
    # Or path to database file if using sqlite3.
        'NAME': 'dujour',
    # Not used with sqlite3.
        'USER': 'dujour',
    # Not used with sqlite3.
        'PASSWORD': 'TXICKnwrrIPSU9zZ',
    # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '127.0.0.1',
    # Set to empty string for default. Not used with sqlite3.
        'PORT': '3306',
    }
}


############### Customized Settings ################################

AUTH_PROFILE_MODULE = "users.UserProfile"

# the Amazon S3 configuration
S3_ACCESS_KEY_ID = 'AKIAIETJIBFTE4QAHN6A'
S3_SECRET_ACCESS_KEY = '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'
S3_BUCKET = 'media-farm-dujour'
MEDIA_FARM_SERVER_URI = 'https://d956iao6yp65z.cloudfront.net'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': [
            '127.0.0.1:11211',
        ]
    }
}

RESIZED_VERSION = {
    '1': '300x200',
    '2': '480x320',
    '3': '720x480',
    '4': '1080x720',
    '5': '1620x1080',
    '6': '2520x1680',
}

CURRENT_FOLDER = os.getcwd()


## CRON JOB CONSTANTS
CRON_HOUR = 6  # 6AM
TIME = datetime.utcnow()
DAILY_CRON_TIME = datetime(
    TIME.year, TIME.month, TIME.day, CRON_HOUR, 0, 0, 0, TIME.tzinfo)

Maximum_Portable_Devices_Per_User = 10

DOMAIN_NAME = 'www.dujour.im'
RANDOM_TOKEN = 'alpha'
PAGE_BASE_URL = 'https://' + DOMAIN_NAME + '/' + RANDOM_TOKEN + '/#!/page/'
DEV_PAGE_BASE_URL = 'www.derek.dev.dujour.im/#!/page/'
BASE_URL = 'https://' + DOMAIN_NAME + '/' + RANDOM_TOKEN + '/#!/'
DEV_BASE_URL = 'www.derek.dev.dujour.im/#!/'

LOGIN_REDIRECT_URL = '/accounts/my_account/'
AUTH_PROFILE_MODULE = "accounts.models"
AUTH_PROFILE_MODULE = "users.UserProfile"

if CURRENT_FOLDER.find("derek") != -1:
    pass
elif CURRENT_FOLDER.find("dbtsai") != -1:
    pass
else:
    CURRENT_FOLDER = '/home/www-data/sites/api.dujour.im/back-end/'

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
DEFAULT_FROM_EMAIL = 'Dujour <noreply@dujour.im>'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = '@gmail.com'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 587
# LOGIN_REDIRECT_URL = '/'
# End by dbtsai

TEMPLATE_DIRS = (
    os.path.realpath(__file__) + '/django_templates',
)
ACCOUNT_ACTIVATION_DAYS = 7
############ End of Customized Settings ############################

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'gl#mt7q!2lqtvt2*8bxiqfajc97(l-3cu=4i2v9dgbi0h7^q3d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'website.wsgi.application'

TEMPLATE_DIRS = (
    CURRENT_FOLDER + '/django_templates',
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'website.media',
    'registration',
    'website.users',
    'website.brands',
    'website.actions',
    'taggit',
    'tastypie',
    # 'south', # database migration tool
    # 'mptt',
)

#if DEBUG:
#    INSTALLED_APPS = INSTALLED_APPS + ('devserver',)

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
