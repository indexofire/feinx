# -*- coding: utf-8 -*-
# Django settings for feindex project.
from django.utils.translation import ugettext_lazy as _
from os.path import join
from project.settings import create_secret_key, PROJECT_PATH, PROJECT_NAME, \
    PROJECT_DIRS

#import sys
#sys.path.append('/home/mark/Repos/feinx/feinx/apps/')
#sys.path.append('/home/mark/Repos/feinx/feinx/contrib/')

# Debug
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Admin
ADMINS = (
    ('Administrator', 'admin@example.com'),
)
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-cn'
LANGUAGES     = (
    ('zh-cn', _('Simplified Chinese')),
    ('en-us', _('English')),
)
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = join(PROJECT_DIRS, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(PROJECT_DIRS, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    join(PROJECT_DIRS, 'assets'),
)

# Set default theme, and change it in your own settings
THEME = 'default'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
# Make sure you have the privilieges to write in the data directory
SECRET_KEY = create_secret_key(join(PROJECT_PATH, '../data', '.secret_key'))

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'feincms.context_processors.add_page_if_missing',
)

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

TEMPLATE_DIRS = (
    join(PROJECT_DIRS, 'templates/%s' % THEME),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'feincms',
    'feincms.module.page',
    'feincms.module.medialibrary',
    'mptt',
    'feinx',
    'feinx.apps.forum',
    'feinx.apps.bootloader',
    'feinx.contrib.account',
    #'pagination',
)

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

# Auth definition
#AUTH_PROFILE_MODULE = 'contrib.profile.Profile'

# Use new feincms reverse
FEINCMS_REVERSE_MONKEY_PATCH = False

# Feincms richtext editor
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': '%slibs/tiny_mce/tiny_mce.js' % STATIC_URL,
}

# Profile backend to enable profile as default user model
#AUTHENTICATION_BACKENDS = (
#    'feinx.contrib.profile.auth_backends.ProfileModelBackend',
#)

# Custom user model. Default model is feinx's profile model.
#CUSTOM_USER_MODEL = 'feinx.contrib.profile.Profile'


TIME_ZONE_CHOICES = (
    ('-12.0', '(GMT -12:00) Eniwetok, Kwajalein'),
    ('-11.0', '(GMT -11:00) Midway Island, Samoa'),
    ('-10.0', '(GMT -10:00) Hawaii'),
    ('-9.0', '(GMT -9:00) Alaska'),
    ('-8.0', '(GMT -8:00) Pacific Time (US &amp; Canada)'),
    ('-7.0', '(GMT -7:00) Mountain Time (US &amp; Canada)'),
    ('-6.0', '(GMT -6:00) Central Time (US &amp; Canada), Mexico City'),
    ('-5.0', '(GMT -5:00) Eastern Time (US &amp; Canada), Bogota, Lima'),
    ('-4.0', '(GMT -4:00) Atlantic Time (Canada), Caracas, La Paz'),
    ('-3.5', '(GMT -3:30) Newfoundland'),
    ('-3.0', '(GMT -3:00) Brazil, Buenos Aires, Georgetown'),
    ('-2.0', '(GMT -2:00) Mid-Atlantic'),
    ('-1.0', '(GMT -1:00 hour) Azores, Cape Verde Islands'),
    ('0.0', '(GMT) Western Europe Time, London, Lisbon, Casablanca'),
    ('1.0', '(GMT +1:00 hour) Brussels, Copenhagen, Madrid, Paris'),
    ('2.0', '(GMT +2:00) Kaliningrad, South Africa'),
    ('3.0', '(GMT +3:00) Baghdad, Riyadh, Moscow, St. Petersburg'),
    ('3.5', '(GMT +3:30) Tehran'),
    ('4.0', '(GMT +4:00) Abu Dhabi, Muscat, Baku, Tbilisi'),
    ('4.5', '(GMT +4:30) Kabul'),
    ('5.0', '(GMT +5:00) Ekaterinburg, Islamabad, Karachi, Tashkent'),
    ('5.5', '(GMT +5:30) Bombay, Calcutta, Madras, New Delhi'),
    ('5.75', '(GMT +5:45) Kathmandu'),
    ('6.0', '(GMT +6:00) Almaty, Dhaka, Colombo'),
    ('7.0', '(GMT +7:00) Bangkok, Hanoi, Jakarta'),
    ('8.0', '(GMT +8:00) Beijing, Perth, Singapore, Hong Kong'),
    ('9.0', '(GMT +9:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk'),
    ('9.5', '(GMT +9:30) Adelaide, Darwin'),
    ('10.0', '(GMT +10:00) Eastern Australia, Guam, Vladivostok'),
    ('11.0', '(GMT +11:00) Magadan, Solomon Islands, New Caledonia'),
    ('12.0', '(GMT +12:00) Auckland, Wellington, Fiji, Kamchatka')
)

