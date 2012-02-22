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
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

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
    },
    'require_code':True
}

DASHBOARD_TEMPLATES = [
    {
        'name':'twitter_personal_words',
        'template':{
                "username": "USERNAME",
                "name": "USERNAME Twitter Wordart",
                "created": time.time(),
                "deleted": False,
                "short_url": { },
                "last_saved": time.time(),
                "widgets": {
                    "something": [

                    ]
                },
                "last_saved_pretty": "32 seconds ago",
                "collections": [
                        {
                        "search_results": [

                        ],
                        "search_filters": {
                            "time": "[*%20TO%20*]"
                        },
                        "data_points": [
                                {
                                "image_large": "\/static\/images\/thedashboard\/data_points\/twitter_large.png",
                                "configured_display_name": "Twitter: from:metalayerhq",
                                "image_medium": "\/static\/images\/thedashboard\/data_points\/twitter_medium.png",
                                "configured": False,
                                "image_small": "\/static\/images\/thedashboard\/data_points\/twitter_small.png",
                                "id": "c2243ff90f0a40009d0785278d4a7169",
                                "elements": [
                                        {
                                        "display_name": "What to search for",
                                        "type": "text",
                                        "name": "keywords",
                                        "value": "",
                                        "help": "Enter your Twitter username here"
                                    }
                                ],
                                "display_name_short": "Twitter",
                                "full_display_name": "Twitter Search",
                                "type": "twittersearch",
                                "sub_type": "twittersearch",
                                "instructions": "Use this data point to search the public tweet stream."
                            }
                        ],
                        "actions": [
                                {
                                "elements": [

                                ],
                                "name": "datalayertagging",
                                "configured": True,
                                "image_small": "\/static\/images\/thedashboard\/actions\/tagging_small.png",
                                "display_name_long": "Tagging",
                                "display_name_short": "Tagging",
                                "content_properties": {
                                    "added": [
                                            {
                                            "display_name": "Tags",
                                            "type": "string",
                                            "name": "tags"
                                        }
                                    ]
                                },
                                "id": "d5995f1afca04efea3c753d8be4d15a4",
                                "instructions": "This actions does not need configuring."
                            }
                        ],
                        "options": [

                        ],
                        "outputs": [

                        ],
                        "visualizations": [
                                {
                                "elements": [
                                        {
                                        "display_name": "Color Scheme",
                                        "help": "",
                                        "value": "Orange",
                                        "values": [
                                            "Blue",
                                            "Green",
                                            "Grey",
                                            "Orange",
                                            "Purple",
                                            "RedBlue - Green",
                                            "Blue - Purple",
                                            "Green - Blue",
                                            "Orange - Red",
                                            "Purple - Red",
                                            "Yellow - Brown"
                                        ],
                                        "type": "select",
                                        "name": "colorscheme"
                                    },
                                        {
                                        "display_name": "Background",
                                        "help": "",
                                        "value": "Light",
                                        "values": [
                                            "Light",
                                            "Dark"
                                        ],
                                        "type": "select",
                                        "name": "background"
                                    },
                                        {
                                        "display_name": "Style",
                                        "help": "",
                                        "value": "Standard",
                                        "values": [
                                            "Standard",
                                            "Word Mashup"
                                        ],
                                        "type": "select",
                                        "name": "style"
                                    },
                                        {
                                        "display_name": "Word Limit",
                                        "help": "",
                                        "value": "100",
                                        "values": [
                                            "100",
                                            "50",
                                            "20",
                                            "10",
                                            "5"
                                        ],
                                        "type": "select",
                                        "name": "wordlimit"
                                    }
                                ],
                                "name": "d3cloud",
                                "configured": True,
                                "image_small": "\/static\/images\/thedashboard\/area_chart.png",
                                "data_dimensions": [
                                        {
                                        "display_name": "Words",
                                        "name": "category1",
                                        "value": {
                                            "name": "Tags",
                                            "value": "action_datalayertagging_tags_s"
                                        },
                                        "values": [
                                                {
                                                "name": "Tags",
                                                "value": "action_datalayertagging_tags_s"
                                            }
                                        ],
                                        "type": "string",
                                        "help": ""
                                    }
                                ],
                                "display_name_long": "Words",
                                "display_name_short": "Words",
                                "unconfigurable_message": "There is no category data available to be plotted. Try adding something like tagging",
                                "type": "javascript",
                                "id": "980feda2bbf34e34a01fa8d2e9ea8b34"
                            }
                        ],
                        "id": "4f43d3b57a9c1b3f3d000000"
                    },
                        {
                        "search_results": [

                        ],
                        "search_filters": [

                        ],
                        "data_points": [

                        ],
                        "actions": [

                        ],
                        "options": [

                        ],
                        "outputs": [

                        ],
                        "visualizations": [

                        ],
                        "id": "4f43d3b57a9c1b3f3d000001"
                    }
                ],
                "community": {
                    "challenges": 0,
                    "remixes": 0,
                    "comments": 0,
                    "views": 0
                },
                "accessed": 1,
                "active": True,
                "created_pretty": "",
                "config": [

                ],
        }
    }
]

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
