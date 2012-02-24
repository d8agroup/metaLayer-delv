# Django settings for dashboard project.
import time

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mrmatthewgriffiths@gmail.com'
EMAIL_HOST_PASSWORD = 'hellitifyoulike01'
EMAIL_PORT = 587

ADMINS = (
    ('Matthew Griffiths', 'mg@metalayer.com'),
)

MANAGERS = ADMINS

#Django Compressor Settings
COMPRESS_OFFLINE = False
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
COMPRESS_CSS_HASHING_METHOD = 'hash' # not using mtime since it differs between servers.
COMPRESS_CACHE_BACKEND = 'django.core.cache.backends.locmem.LocMemCache'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

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
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'f8dg7df6ggf5h4hj4k3jhqks'

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
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

ROOT_URLCONF = 'dashboard.urls'

AUTH_PROFILE_MODULE = "userprofiles.UserProfile"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_mongodb_engine',
    'djangotoolbox',
    'compressor',

    'dashboard.actions',
    'dashboard.aggregator',
    'dashboard.chargifyapi',
    'dashboard.customtags',
    'dashboard.dashboards',
    'dashboard.datapoints',
    'dashboard.imaging',
    'dashboard.outputs',
    'dashboard.search',
    'dashboard.thecommunity',
    'dashboard.userprofiles',
    'dashboard.thedashboard',
    'dashboard.visualizations',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

DB_LOGGING = {}

SUBSCRIPTIONS_SETTINGS = {
    'allow_subscription_migrations':True,
    'subscriptions':{
        'subscription_type_1':{
            'id':'subscription_type_1',
            'chargify_config':None,
            'display_data':{
                'display_name':'Free Plan',
                'image':'/static/images/thedashboard/no_image_medium.gif',
                'messages':[
                    'No monthly fee!',
                    'Unlimited insights',
                    'Five minute data refresh rate'
                ],
            },
            'templates':{
                'upgrade':None, #its not possible to upgrade to this subscription type
                'downgrade':'subscription_type_1_downgrade_to.html'
            },
            'config':{
                'number_of_saved_dashboards':1,
                'number_of_always_on_dashboards':0,
                'allow_private_insights':False
            }
        },
        'subscription_type_2':{
            'id':'subscription_type_2',
            'chargify_config':{
                'product_handle':'basic-plan',
                'product_id':85271
            },
            'display_data':{
                'display_name':'Basic Plan',
                'image':'/static/images/thedashboard/no_image_medium.gif',
                'messages':[
                    'Only $19 per month!',
                    'Private Insights!',
                    'Five minute data refresh rate'
                ],
            },
            'templates':{
                'upgrade':'subscription_type_2_upgrade_to.html',
                'downgrade':None
            },
            'config':{
                'number_of_saved_dashboards':2,
                'number_of_always_on_dashboards':2,
                'allow_private_insights':True
            }
        }
    }
}

DATA_POINTS_CONFIG = {
    'enabled_data_points':[
        'feed',
        'googleplusactivitysearch',
        'twittersearch',
        'googlenewssearch',
        ]
}

ACTIONS_CONFIG = {
    'enabled_actions':[
        'localsentimentanalysis',
        'yahooplacemaker',
        'languagedetection',
        'datalayertagging'
    ]
}

OUTPUTS_CONFIG = {
    'enabled_outputs':[
        'atomoutput',
        'jsonoutput'
    ]
}

VISUALIZATIONS_CONFIG = {
    'enabled_visualizations':[
        'googlegeochart',
        'googlebarchart',
        'googlepiechart',
        'googleareachart',
        'd3cloud'
    ],
    'visualization_display_hierarchy':[
        'googlegeochart',
        'd3cloud',
        'googlelinechart',
        'googlebarchart',
        'googlepiechart',
        'googleareachart'
    ]
}

INSIGHT_CATEGORIES = [
    'Business',
    'Politics',
    'Science',
    'Current Events',
    'News and Journalism',
    'Investigative',
    'Number and Math',
    'Education',
    'Finance',
    'Travel',
    'Humor',
    'Technology'
]

REGISTRATION_CODES = {
    'codes':{
        'TED':['12345', '23456'],
        'PRIVATE_BETA':['ZM26R']
    },
    'require_code':True
}

SOCIAL_SHARING_SERVICES = [
    'st_sharethis_large',
    'st_twitter_large',
    'st_plusone_large',
    #'st_facebook_large',
    'st_linkedin_large',
    'st_fblike_hcount',
]

from settings_insight_templates import *

import socket
if socket.gethostname() in ['mattgriffiths']:
    from settings_mattgriffiths import *
elif socket.gethostbyname(socket.gethostname()) in ['50.57.164.87']:
    from settings_staging import *
elif socket.gethostbyname(socket.gethostname()) in ['50.57.227.192']:
    from settings_development import *
elif socket.gethostname() == 'Todd-McNeals-MacBook-Pro.local':
    from settings_tmcneal import *
else:
    #TODO this needs to be changed to support multiple envs
    from settings_production import *
