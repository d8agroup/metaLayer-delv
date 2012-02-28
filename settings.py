# Django settings for dashboard project.
import time

SITE_DOWN = False

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

DYNAMIC_IMAGES_WEB_ROOT = '/static/CACHE/images/'

#Django Compressor Settings
COMPRESS_OFFLINE = False
#COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
COMPRESS_CSS_HASHING_METHOD = 'hash' # not using mtime since it differs between servers.
COMPRESS_CACHE_BACKEND = 'django.core.cache.backends.locmem.LocMemCache'

CACHE_TIMEOUT = 300

LOW_LEVEL_CACHE_LIMITS = {
    'imaging_views_last_modified':300,
    'dashboards_models_dashboard_top':300,
    'dashboards_models_dashboard_trending':300,
    'dashboards_models_dashboard_recent':300,
}

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
    'raven.contrib.django',
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
"""
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
"""


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
            },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
            },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
            },
        },
    }

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

REGISTRATION_POLICIES = {
    'DefaultRegistrationPolicy':{
        'name':'Default Registration Policy',
        'active':False,
        'module':'userprofiles.registrationpolicies.defaultregistrationpolicy',
    },
    'ClosedRegistrationPolicy':{
        'name':'Closed Registration Policy',
        'active':True,
        'module':'userprofiles.registrationpolicies.closedregistrationpolicy',
    },
    'TEDRegistrationPolicy':{
        'name':'TED Registration Policy',
        'active':True,
        'module':'userprofiles.registrationpolicies.tedregistrationpolicy',
        'codes':['TEDTEST', '9ARIS', 'VLDRL', 'Z2P35', 'W19H7', 'OXM0Z', 'HVWRG', 'GY5A8', 'YRJ31', 'ETPXM', 'DQUM5', 'EUXR0',
                 'VZPOW', 'K92TW', '1R5B4', 'J0GXT', 'KSJC5', 'XJPZY', '0P54A', 'J357U', 'ZWZ4T', '7XH7A', 'IVLHO',
                 'IZKYP', '9MF6R', 'ABKQ7', 'ZPD8U', 'XGD7Y', 'OMLT3', '8B531', '96CM2', 'AU9H1', 'SK22W', 'UL21N',
                 '9ONOV', 'UMY2P', '9TKMC', '4GCIX', '5DYH9', '0QRSU', '37DH9', 'KB7RH', 'MVXQ2', 'H9N8R', '9WKDF',
                 '3YTHP', 'FBIN6', 'OW9GC', '942P5', '4NYRU', 'B43SS', 'JJ2HI', 'WHFE6', 'N4EOS', 'FPM23', 'KN9PU',
                 '9LCXL', 'EQCX5', '9FW1P', '9IXRQ', 'ER93W', 'BL8PB', 'IX4VT', 'C4HYI', 'RKX3U', 'F5A7Z', '99VTQ',
                 '8F1C7', 'MAW5A', 'E6HH4', 'JDVNI', '867AU', 'CABTR', 'H52EE', 'ZEYTR', 'TLA21', 'TFFM6', 'ATQCX',
                 '5XSX3', 'OL1W0', 'M0O4Y', 'UYHOJ', 'LT89V', 'COPUE', '58IU0', 'IZZKF', 'CORKV', '21M6W', '6BP4K',
                 'GVYG8', 'TTZUA', 'U53VR', 'QDG6E', 'T54CG', 'Y1NEG', 'LD4KD', 'RFQVZ', '2A8FS', 'M675A', 'ULBS5',
                 'IMHC8', 'QVNLP', 'LZ9HK', 'QWDJL', 'WHUYY', 'MD1V8', 'ATWML', '6M2NO', 'OZPQ2', 'RQAAD', '4OPPQ',
                 'C33DC', 'LTO0Q', 'FMDEI', '80CJO', 'T6LY8', 'Q3CBL', 'DCWIW', 'YECHH', 'ZH53E', '2W9BG', 'WGRH9',
                 'B6710', 'MF9LR', 'NP1IL', '8175E', '4BDG4', '7VDEV', 'F2M4I', 'WGLNB', 'SGIPN', 'IA5EJ', 'BQVMQ',
                 '7PR9D', 'I0W1H', 'OUOHM', 'H1U7M', 'XJKOT', 'CUJX7', 'BLA84', 'WJC00', 'SFLJP', 'R2U4F', 'BOQRM',
                 'ETKLL', 'S2OUD', 'H0TM1', '98AZV', 'LD1TU', '525JS', 'SH4NK', 'YHFGA', 'CE9JE', '39MJE', 'NCFK8',
                 'F0QU4', 'WER6R', 'M2LY9', '1GKPZ', 'CD4R1', '7GEKV', 'QJZ3I', 'CO8ZC', 'VRA44', 'DGI6F', 'X2WQW',
                 '5DTBP', 'CTWD2', '15BFT', 'C9TF9', '8BV02', 'SX1E9', '3SUDS', '83PF7', '5D32K', 'DUM48', 'GI304',
                 'G28M9', 'M27QL', 'WTFG5', 'QYO00', 'GSLZ6', 'AXK2T', '3IG8U', '5A0UP', 'JVYXG', 'UX2G1', '0U0R2',
                 'RKM3D', '9RFG0', 'RT5Q2', 'YDGH2', 'HR52X', 'II30A', 'OA3GF', 'HM5VM', 'U85XN', 'R5TEE', 'VN41G',
                 '51RZF', 'TJSBI', 'IOXGH', 'GLM4A', 'EPYA0', '6PXT0', '2F5I8', 'V3WVK', '4FKZR', 'IU0L3', 'D7AV8',
                 '62XX6', '6YKB9', 'V1A1Q', 'OPSSJ', 'I26QQ', 'WANG5', 'Q6MUD', 'FUP4H', 'Q5V92', '8DT8H', 'L0FHU',
                 '8FCIH', '3PHWU', 'M1EQ3', 'JHMOG', 'JQHM6', 'RFKLS', 'H7CS6', 'I3ZAH', 'XKK12', 'R7D83', 'DMJNM',
                 'UQMYT', 'SYLTY', 'ED55A', '5HQ2Y', 'QR1R5', 'D9LS9', '9Z2I6', 'HBBOW', 'FB8YJ', '1JCJO', '0CE02',
                 '7DU9D', 'YVG6Q', 'WD37B', 'HXSKA', 'ECMA8', 'DFJE2', 'Y60Z9', 'D02AO', 'K38VM', 'KMENT', 'NCB8V',
                 'HI4IO', 'QKBXL', 'W5Q8Y', 'WYSKA', 'M3CFI', 'DCXFY', '8LHT8', 'L8LJC', '3LZYF', 'GEUV8', 'INOFM',
                 '358OJ', '91NQT', '06LE4', '6G3WV', 'IZG3H', 'FSN6J', 'FDWRQ', 'N1AYH', 'MUILQ', '4Y6E7', 'TWOSK',
                 'PW61Y', '759MN', 'LJF4D', 'Z48YT', 'B8WIY', '1N710', '7WAF1', 'OKGI2', 'TQ1NJ', 'K2OX5', 'XVQIC',
                 'QGR5Z', '6XE8U', 'TKK5I', '2131Z', 'QACJO', 'K7JSE', '64X2X', 'NETYG', 'PTFPB', '3CNAU', 'WROKG',
                 '0CY85', '21QL7', 'EJG8Q', 'GS446', '5FHM7', '3FA2J', '5XXE5', '1MBE9', 'OOPM1', 'K7KJ9', 'ITM12',
                 '9CAR2', 'LCGRG', 'ADH7G', '4NC71', 'O9WTL', 'XR6A3', 'HX1OM', 'BJXAO', 'Z880W', 'Q92DA', 'QXS4R',
                 'SRGY8', 'FQJI6', 'O839O', '9FV2F', 'U2QC7', 'W2QIV', 'Y7A05', 'LACNI', 'MMWI0', 'C4M92', 'S75N7',
                 'PRIWC', 'QQ4BO', 'OX93P', 'A0NTY', 'SHTIM', 'G2OHA', '11L8O', 'PH7GK', 'PF7HA', 'VKVJC', 'A3FIF',
                 'L3LNP', '3Y59P', '894J7', 'BIC1W', 'UC2ZQ', 'QUWJZ', 'ZUOPF', 'VR85Y', '0AX9K', '6RD5N', 'ENF9M',
                 'VOHP5', 'JHWBP', 'RWPTM', 'Y89KS', 'ZWCFB', 'DTYO9', 'X5X7Y', 'AGBA6', '62BOS', 'O2BFB', 'PV2Z3',
                 'WU4IO', '185F6', 'LEUZG', '4WYFV', 'XZ8PG', '7L7B0', 'JVNC1', 'GFE3G', '9Q1XQ', '0YAX2', 'ZLMC3',
                 'XW9SQ', 'IOAVN', '78V40', '0TP1O', 'LRL9C', '78OG4', '1CHY2', 'O32RB', 'ICEZH', 'SGEQE', 'Z06W4',
                 '55XYX', '1N349', 'AIYBF', 'RAAY6', 'G8OOF', 'X550L', 'VLFUQ', '9N7D1', 'MJ0CJ', 'KF4R4', '0V1NQ',
                 '2DC8K', '9PBIZ', '3ZL5F', 'B5YBO', 'HZEEF', 'O77BT', '9RXDB', 'BTMTM', 'W4D30', 'JEZNU', '4PW0J',
                 'IQ3HP', '3G3HE', 'SS7SV', '978B2', 'G9XG4', 'RIB39', '6ZR95', 'NSTZL', 'OOLLR', 'ZTFVI', 'JGGC3',
                 'KX1EV', '029T0', 'XR1DH', 'IJU19', '1T47Z', 'NM3W1', 'GFHNY', 'TB95M', 'PYTMK', 'ESRRX', 'U0J5G',
                 'B510S', 'OAN64', 'YPCOM', 'A9Y4R', '2ZKH6', 'ZZ0TN', '6RHGQ', '3GSR1', 'NWJ73', 'J9MUD', 'JS02O',
                 'BXTO0', 'DWW5O', 'WCKO3', 'G7MWV', '9FC39', '2M4JO', '5E2D0', 'GXF56', 'UV2L3', 'RXNF1', '3PYVV',
                 'ZSPJX', 'SF425', 'UDXJ0', 'OEVJN', 'O4JE1', 'WRCVJ', '70K3B', 'ISNC0', 'N5W0E', 'U1Q8S', 'YAS5O',
                 '0AXL8', 'M4GNO', '6L1IL', 'LCP85', '4UVBM', '5VFO8', 'DLLFP', 'B6AVC', 'D7WOK', 'KKGID', 'K209J',
                 'M2XGR', '634D6', '48EZA', 'NEWRI', 'KCTNQ', 'HVDCT', '6D2G7', 'IYOAV', 'NMEX9', '32QFB', 'B785U',
                 '9D6OI', '1XZLT', 'B9HR4', 'VUWAV', '4VRBM', 'GTL3Z', 'ISUHE', 'NM6RC', 'OBJ62', 'CHNKD', '2QP9X', 'EBDXS', 'M3P5G', 'OZFCA', 'HUNYK', 'J4DUZ', '8MR57', 'WGZNR', 'DYPMQ', 'TLEUW', 'OOPHZ', 'YJI92', 'LLVOL', 'HLFV1', 'SIVTN', 'CF8Q3', 'Q7WO3', 'TKLO7', 'BO1A3', 'W4IWJ', 'XL7CK', '3HPMG', '6A3Z7', 'F20CM', '0RJGN', 'DYCA7', 'AP7T9', 'F3IE0', '27BZY', 'OX4CN', '1LNNF', 'H1791', '7C8MO', 'TOLCE', 'XFSGC', 'P272Z', 'P8DAO', '72KZA', 'WIGM2', 'PS297', 'G25JN', 'DHYWT', 'X7AS7', 'NE16E', 'YGJBR', '99RVM', 'DDRVC', 'KGHLQ', '9V4FB', '63CZX', 'QDVFL', 'BMAAU', 'RVLUJ', '73JD2', '8AQY0', 'TPFW5', 'QYPTT', 'NTGC6', 'UQ6CV', '305UQ', 'A285I', '3PSQL', '8VZ79', 'DIBOX', 'TIB6O', '39GNC', 'HYD21', 'ZJO0Y', 'E8J2Q', 'YEO35', 'I3K1M', 'VEVS8', 'ZDQDV', 'QO0CX', '1N5XB', 'RCVJ0', 'GFTM9', 'TG0IR', 'IL4XP', '0JDZU', 'KYESX', 'H9KRS', '4G86C', 'A2B5M', 'QW387', 'LA6MT', 'VLSAZ', '9OEZ5', 'R3RHP', '152A1', 'T6P77', 'S3845', 'MT3RJ', 'DPHOF', 'AA6YL', '0OI8M', 'WR1XN', '8G29S', 'E8OGM', '4AA7A', '0JASQ', 'FOZPL', 'JAD5P', 'KI1WI', '4M86Z', 'EGYLW', '0RCIG', 'I273F', 'PT8GF', '0O2E5', 'NLB3L', 'HVVFH', 'GLX18', '9DOWE', '0YMRM', 'H08S4', '8OM9Q', 'M01G2', 'A0SKO', 'H6AQV', 'BWMMW', 'PWD5S', '3T158', '7YAA9', 'VGKB5', 'YFPKK', '806L2', 'NC3S5', 'QYQOX', 'KFA0K', 'EV2PE', 'C77Y3', 'UKOHC', '3YXVV', '1G8N8', 'MUILU', 'ZS0BK', 'BFCY8', '97GAI', 'L125T', 'PMJNB', 'F0734', 'ZJTK6', 'TYH4N', '7GIQI', 'X7RAZ', 'X7YU9', 'S7CAM', 'VNGRG', '576OB', 'MU90D', '6R5GU', 'L0SHY', 'NV3XF', 'S6SXE', 'TGOFF', 'PD9RR', 'N1FPV', '8ESGM', 'GQ9FQ', '45X92', 'WMZRB', 'FBH3D', 'EFWRE', 'GGP7V', 'UE9G5', 'I1NR7', 'B625G', 'TCXC3', 'Q59VC', '1Z3X9', '12QPA', '3FG9C', 'XXFYX', '1X6R7', 'O8LKX', 'B4WVS', 'F6M4W', 'XJU6X', 'T15AS', '503YU', '4S6X5', 'TWUHE', 'O0BKE', 'YN9NP', '1QL12', 'IINPS', 'UO85Y', 'MM2LZ', '4OG9M', 'V8ZVC', 'KXYZK', '81OBO', 'T8MZ3', 'EZC66', '8CJF5', 'KQMBE', '80EJX', 'W3OU0', '776PY', 'T3FQR', 'V5S5W', 'TBMWS', 'E4URR', 'XAOAJ', 'V4ZXY', 'MD0PQ', 'J11X6', '83WF4', 'U0XNT', 'GG3IJ', '43ICN', 'LEDNI', 'ETGJX', 'IQBAD', '1GZDA', 'YGSES', '3HQJC', 'L1WFB', 'LJKV3', 'VKXAS', 'GLW08', 'I0UL2', 'E3I0Z', '6ROTT', '3DTQ6', 'SEK1Q', 'MXRB2', 'K0T29', 'IGB2Y', 'U4ZOR', '1ZKAY', '0JU39', '3I6QB', 'H9QOH', 'S3GBS', '4OQQV', 'OHU2F', 'Z35DH', '06ZKV', '9AVMK', 'U4RVQ', 'KKFSX', 'TTU59', 'G3RIP', '47BLQ', 'M0WYY', 'JJUNO', 'HWP6H', 'YVVKW', 'YBEOR', 'H1EO0', 'AWR4J', '4GBYZ', 'SQJ5W', '8Y0NP', 'PFZPL', 'KATCU', '161AL', 'IYYT1', 'KUWAS', 'VVKI1', '644A8', 'DS0A3', '198AP', 'PRY96', 'ESAFZ', '4CB37', 'FRVLT', 'XWF49', 'KJ5SP', 'WQM66', 'HSYTZ', 'B7JKT', 'IKBXS', 'PFF8N', '17B82', 'OI7RN', '3AMO7', 'DW6YU', 'SXY4Z', 'OPLZQ', 'ZN0WK', 'OKHHV', 'W8R74', 'QGA5S', 'CUFW8', 'SAJZY', 'RRDJZ', 'U8GLE', '6LHMG', '7LAYQ', 'Q91G6', 'HFSQ8', 'KV6O5', '1DTRD', 'B90FB', '9XTFJ', 'X334I', '1E9Y8', 'AGZXH', 'RNZNY', 'S5QNJ', 'R9OY9', '5UBUP', 'E8TB2', '6XROP', '29AZQ', '9RPYG', 'MUSI5', 'TT5LJ', '9XT0Z', 'MCYDO', 'SXQKG', 'M92FH', 'S9OUK', 'EGMBU', 'CRMZL', '81IYA', 'C5QGA', 'IARAN', 'PS40R', 'NKNA2', 'VYM7H', '74HE0', 'FYUDK', 'K48J5', 'YOGLJ', 'GDQF3', 'SX2F0', 'LU3CO', 'GPBE1', 'Q4RFN', 'WPFXH', 'IABCN', 'UEPNC', 'NNZ2K', '0A7MJ', '4VK6O', 'HPD1A', 'Z2PCL', 'WSLLX', 'W12D9', 'DN7IU', '97ECY', '31Z5U', 'JK5R0', 'XUEWR', '7P7L9', '9GXDH', 'HKGFV', 'T7UD5', 'HAQP3', 'OOSPG', 'UJ7AC', 'R2XWI', 'B5U7F', '1W52Y', 'L1VVZ', 'LDTBA', 'KHLW6', 'M13L5', '2K59Q', 'AJ2GD', '5DKAL', '6UFZ6', '945J6', 'U3931', '2OO51', 'OZ4PW', '20SBV', 'OLZNG', 'R96FM', 'KBK19', 'P13NS', '83CH0', 'MD8T3', 'N2CFT', 'HDOKA', 'SUIUL', '41OH2', 'M8UJS', '2XZBN', '45NTB', 'G2N0M', '0E7Z5', 'FJZLL', 'HERHU', '873OR', 'UMR72', 'F25W2', '2LOZ1', 'IAHN0', '4WYF3', 'DMI73', 'T086H', '29NSM', '34T7X', 'V1F9D', 'GVDRF', 'IFFBG', 'L3R5S', 'HPG97', 'E3UG6', 'QQFR9', '76OVO', 'G59D4', '53KWT', 'R3O7O', 'H8OBD', 'MQ4SN', 'Y4M2Y', '8OIJE', 'TTXO8', '732EF', 'JHASC', '4NJXT', 'ZM8BI', 'III5J', '605CG', 'MBSFK', 'S4D6U', '22IH9', 'GQ7T2', '2DIUJ', 'I8DB5', 'Y050C', 'QY1IU', 'LCY7B', '6C6ND', 'LNQXL', '0W2AN', 'JCZO1', 'HA38U', '3JDIM', 'HKRK5', 'KWSTK', 'D78MG', 'P5Z2L', 'KNI61', 'N1895', 'IUXHU', '2SJ70', 'IRPCP', 'WO7N8', 'LU8OH', 'SWYQS', 'SF9CF', 'FNJ9R', 'INFYB', 'B8DA1', 'RXQV3', '5NZ7C', '40RJW', 'T3AIX', '4B4T4', '4CX9G', 'YKHJX', 'NI3VC', '3PAPH', 'IP6Z4', 'Z5PJI', '6Z2ZX', 'AE1XX', 'RZ3F7', '89DOI', 'D5EHB', 'JJ29S', '137WR', 'ZWCY5', 'G5M4B', '4BMIZ', '9QG4T', 'U2EF7', 'KGLRH', '274T4', '9P19Z', 'S8C4R', 'KPJCD', 'P60EE', 'OZH67', 'TXQHK', 'EQ6YF', '7E8NS', 'LRDJM', '5YHGA', 'VE0J2', 'WGDPZ', 'I0223', '8SKOW', '21S37', '74YAG', 'E0BYZ', 'BO18S', 'F0KC6', '4F41C', 'WGV73', 'SG86B', '4XE08', 'ET4TV', 'SSH84', '4PV5Y', 'UXBHY', 'AURRA', '92JJX', 'WGRH4', 'V9ZK2', 'MATO9', '8GIL2', 'BKV7D', '4GJ7Q', '3YY4P', 'GA65Z', 'RYXFS', '5C32W', 'TD19Y', '8Y4M9', 'Y6LMS', '33LX2', '9E56Q', 'DVYY3', '2PWFO', '79KEO', 'G4HPO', '4JB26', 'GMA4O', '51OR3', 'D34EE', 'XZ42Q', 'XP8Y5', 'UQ8AH', 'XZB9X', '04STS', '8TIRN', 'TBOMZ', '6Z6JX', 'WRS0B', 'TAO7E', 'IZZYL', 'B61T4', '3F6ZC', 'JC99Y', 'WP219', '8Y0NF', 'P8PS7', 'NSO3G', 'RL3I7', 'SEKVG', 'B8GV6', 'G5UDL', 'MWJ6A', '4YM81', 'M6E9F', 'C3ZS2', 'TE46O', 'YGHT9', '6PIXN', 'OPIS2', '7D3SB', 'MMM7Q', '7QJWE', '1JUBM', 'LS2SZ', '4C7T3', '9XXEJ', 'TG3AG', '8DOV4', 'DL7N1', '957YN', 'ZEBAO', '8ZT8I', 'FLLLK', '3G7O4', '4A0X3', 'A6VA2', 'GT57J', '33323', 'VW8SJ', 'T1SJ5', 'T5PF4', 'YIKMQ', 'JN6PK', 'GPNUY', 'SO19A', '6Z80P', 'FPOZD', 'XB17V', 'LNPPS', 'B5W1O', 'AH1I9', 'KQ93L', 'X8H8Q', 'F3N04', 'H3M6Q', 'WGXTK', 'PC4CY', '6S7D3', 'KA9WV', 'E63ZD', '5F4N6', 'X4GJM', 'E4XF0', 'QD4BA', 'PQUTO', '009RA', '18485', '49HNY', '01WA4', '4HC2M', 'Q9CUI', 'L8H9N', 'ILIRB', 'M91GW', 'W8MP3', 'LMF8M', '3N682', 'Y29UO', '5RZ21', '7TBLC', 'LQ4YZ', '5W29T', 'SLYF1', '5SIPO', 'KX903', '2O6NM', 'ARXBO', 'HMWZ5', 'TRJK6', 'TGPEL', '6L7YK', '43756', '3BD0I', '4DVTZ', 'CNV01', 'M08A4', 'YDULW', 'PJWEN', 'IJ8M2', 'Y8EIV', 'JYKU2', '2IHJR', 'GLKFT', 'XRJXE', 'LRVRK', '9WDKV', '5WX49', 'WKR7W', '6X7B4', 'VJHDT', 'EFLP3', 'Z6DPF', 'UR1GX', 'R2KTE', '2253O', 'ZEHC8', 'T9UPG', 'MZPLE', '9R0XI', 'QVKLI', 'N3L6A', 'FEGKS', 'I1BUN', 'QP3EI', '6R0DS', 'XSJWU', 'URV6B', '80NDP', 'HQK4A', 'SOX0O', '3B8CQ', 'BVOU5', '3LIUZ', 'EWVIX', '78MP9', 'NF24V', 'CVYGF', '9LALY', '0E0PD', 'SKBQZ', '3CSCQ', '5H96T', 'Q5NBS', 'BMCGE', 'XGZGZ', 'DALEM', '76DKD', '9MAZ9', 'MTXIM', 'GYGJS', '0IBUN', 'KA0KW', 'HSI1R', 'VZLK3', 'XD7GT', 'HJCLD', 'YS1SW', 'F5F31', 'EG9CU', 'O8W28', 'MPVIK', 'JDQJP', '8NXVP', '1IXZW', 'T16T7', 'KIMTR', '5BHST', 'PN5MB', 'ZLT36', '7JOLA', 'KV8DC', 'IEF9D', 'Y0GV5', '4PNP9', 'IST1H', 'NURTP', 'H03B6', 'QPMRW', 'W0BF6', 'UJR35', 'A24R8', 'PNSO6', '8IY6Z', 'W9L7O', 'WWPB3', 'IDRBB', 'SU3LR', 'Z98XV', 'O064F', 'CDW92', '7KFE6', 'KFBW7', '1TZSJ', '4XID4', 'UM4AY', 'Q0YLT', 'R9M8W', 'MRZR9', 'Q7GAZ', '24NI0', 'G79Y1', '0BLVW', '4LC4B', 'CPZ2B', 'ZW33H', 'FGUWO', 'RVB8D', 'WW35N', '79E99', 'DGC5U', '5O6XX', 'N4EG6', 'CD65H', '72ZOZ', 'JOE82', '9Y8CR', 'W1VXU', 'MBL6S', 'K3EO5', '9W2Z6', 'IQHC8', 'BN4WA', '9GF49', 'IRIBQ', '6893N', 'ABAAL', 'DJ8OG', 'D753N', 'WQPSP', 'UHXWZ', 'H1UE4', '8AKR4', 'YCZS4', 'A17P4', 'Z8V3E', '51WF8', '6KGKG', 'HJ5RI', '3BQ5A', 'SE5ZN', 'VQG69', 'P9M5K', '7CYJU', '94UTX', 'RYWP3', '08XMZ', 'QYM0Q', 'GZQCK', 'A5YLM', 'ITZMW', 'SYMX7', '9CUSS', 'VFEJR', 'ONTPJ', '45O5N', 'TON2U', '43AOD', '7FFCU', 'B92RJ', '6GXIK', 'KMYSF', 'TN2LL', 'V7RVR', '470DM', 'LAK1F', 'Q9ZVN', 'GZN97', 'PSEW8', '6ALTZ', 'JVKG1', 'P78ZW', '6EVTA', '3R05M', 'YUV9R', 'YNTLP', 'EZKKL', '3SUV0', 'LCBBW', '2X21H', 'LI9GG', 'XVVFC', 'RUGNR', 'Y2QSJ', 'F1UL3', 'H8MWT', '3B88D', 'QJQAV', 'YOMJ8', 'SGEH6', 'MHIVZ', 'MKU6M', '7WDMU', '5D7WY', 'G3LS1', 'I8ARW', 'RCRCN', '6PAXM', 'SLOQF', '0GK4Y', '40C4G', 'UT5U5', 'N7NVC', 'MN2KL', 'UODZJ', '1D80R', '3ORKZ', 'M5DA9', 'T8T9D', 'SWV2Q', 'WLZQE', 'ABKVD', 'ZI8UT', '7M2FO', 'ADCTF', '01OST', 'C7SHD', 'DKLS4', 'QUUVS', 'H35GX', 'WZ2PH', 'FJIJJ', 'VDO6I', 'XJ4Z9', '76LFO', '83G7W', 'LF14B', '8T3CU', 'JDRF9', 'BN645', 'FKTD2', 'M103K', 'DQGG7', 'XR7EZ', 'RY3JW', '0FVRQ', 'EK591', 'AYCSX', 'GFDNL', '4C4Z1', 'YJ1Q0', '2KZ2H', 'OPLGK', '0FOBK', 'SZYMJ', 'C4WWF', '4MGC1', 'TIXYX', '6GFEH', 'GWIKY', 'FZOQ2', '6AKDB', '5LL4K', 'VMAE1', 'ZDYLM', 'IBF77', '4VXAJ', 'EA3FR', 'R8FAK', 'P0PLG', 'OMAD6', 'TP2WW', 'VUAWP', 'F6CN7', 'ZL9P1', 'AWW0W', 'RIUD0', '68S2U', 'NAG8K', 'TV6FT', 'NQSOQ', '16EIB', 'BZRB1', 'RTDXS', '06VTC', 'ZIYO7', 'PKQMK', 'LVN17', '1BY8K', 'LSBYJ', '4N7R7', 'KHS50', 'Y0M1Z', '8R2NM', '71HLT', '4ZX7Q', 'U4HRR', 'GF5FN', 'XW33Q', 'LHEQE', 'BTFI1', 'XBOMD', 'S2QF0', 'ZBFR4', 'BH3XU', 'CY0UG', 'LNVVB', 'BNM1N', 'CCXHJ', 'HY8XX', 'FEJXO', 'LKHEH', 'M9V4G', 'KLEDD', 'WY6XH', 'L0A2S', 'FRIZU', 'E65SU', 'WBCAR', 'BM9NX', 'TKW3B', 'YFJSX', 'DA1FF', 'FFEG3', '90MJH', 'FMOI7', 'PHCTE', 'P818O', 'E0U71', '86ZTT', '512L5', 'DPGUC', 'GW8D4', '4YZL3', 'LSF5X', 'W6K7I', 'RC0OT', 'S5P98', 'DC7TD', 'ERB9R', 'ZO68D', 'LPOUL', '353YP', 'LO1P3', 'UQDHP', 'YTAOU', 'G0TI5', 'Q4MB9', 'LO55X', 'WLD2H', '7X3E1', 'MXKBG', 'RLP3I', 'J52C3', 'JLOVH', '2OP7I', 'P69FV', 'BE3N6', 'Z9NO0', 'CHU3Z', 'DF3YW', 'V5Q9Y', 'CBCV0', 'QXO1W', 'BLBU2', 'XDOEH', 'IAFQS', 'ONGZU', '9WFX5', 'RLYYW', '6FRRW', '3QNAM', '038IL', 'YQFJC', 'F68P7', '5ZZ06', '7V0A6', 'XAMIE', '84XX6', 'N5HH8', 'OELCK', 'NQ2MK', '6CB31', 'U242K', 'R75GT', '42YGG', 'PCNZT', 'OMCUR', 'E9SJE', 'PU3IO', 'HFRN1', 'WRRMA', 'HOVQQ', 'M9S3O', 'JH75G', '70TVU', '3XN3R', 'CF6FG', 'MA711', '8YKFV', '0E3V2', '89B6W', '7VMKL', 'PXIMI', 'FWIGS', 'MTFP1', '3CI62', 'UHS92', 'K4ZPT', 'WG2AO', 'S57HT', 'IDTPN', 'QTT6H', 'WAAOT', 'TTGAU', 'MWB8J', 'FEQFV', 'T2YRA', '66HRV', 'VHGFK', '4KQ2V', 'E9MO1', 'MMC88', 'XWZET', 'QNI5H', 'OE521', 'CD4KQ', '6CPO8', '71G69', 'H0A6E', '0XQOQ', 'RLLFA', '1SV58', '9C47L', '2AIC0', 'SX8E1', 'XDA48', 'TL2KJ', 'CDZ5Q', 'VCMEP', '6WVTP', '7PY1H', '5HJ3X', 'R8FOO', 'VB66J', '28YTS', 'MCTSW', 'LSVCX', 'XA13X', 'AEX3G', 'DES08', 'P5W7U', '4L80A', 'DYUHH', 'GFCYG', 'M0WAD', 'O1HGL', 'SO7VR', 'AZ7JM', 'O5H7K', 'VCCMV', 'NFLFP', 'IHR83', 'F010T', '6OZVF', 'NM0L0', 'C3QB9', 'YD40S', '1SPY6', '6N3LD', '9VXZM', 'UYOCF', '07TBC', 'CL8B9', 'ECDN7', 'T5UUV', 'MJ1BC', 'DITLB', 'ZWMPK', 'ZMD9F', 'UKAHT', 'BZ5QV', '2EDDX', '0GCOO', 'I4QWW', 'IQ3TV', 'BIL6V', 'RWQ5U', '9NMSB', 'PZ3F1', 'RMRK4', 'Y7V85', 'NNH9H', 'B5I5S', 'B9SUG', 'JXU5S', 'YCQEO', 'L6L47', 'KJS7U', '45BH4', 'XF8FZ', 'DWLOZ', '8R6JL', 'O8F9B', 'N23I3', 'B7OBF', 'QN9HL', 'DJS6T', 'H4WDI', 'IQ4HN', 'EHMCT', 'Z5M3J', 'JWG59', 'WFKUE', 'TF110', 'Q99R1', 'F8PGK', 'XKCR0', 'EP40V', 'JIMJ3', '12AT5', 'ALZW5', '4IQ8E', 'C71J6', '4UC8H', 'V0RVJ', 'QB55W', 'REJ78', '02XWQ', 'YLGAX', 'T7PF6', 'AMBK5', '1FOYM', 'MSMUT', '5OF7J', 'AXG9S', 'WTY9H', 'VG6OS', 'GFLQJ', 'MUGXD', '3UEKR', '5NYOH', 'BKEYF', 'HGUS4', 'SJTEN', 'FT49S', 'I1KHM', 'SOAYE', 'TL7VY', 'WAWOK', 'YKXU1', 'FKDUT', 'VUVNQ', 'LZ01C', 'EZACC', 'XG81A', '2P81R', 'H3VQ5', '60BRJ', '636Z1', 'UWEZ3', 'V2Q0Z', 'HWFDG', 'YZIUM', '90RGL', 'UCWDL', 'VFR0N', 'QT4FO', 'TETVH', 'EXFFN', 'QYWPQ', 'CPJOC', '5WRX9', 'GAZSK', 'FNM3V', 'OCGI9', 'NKOOQ', 'FXF8G', '7GC8D', '9LGO7', 'XGWU3', '2759L', 'Y5T9L', 'ZFGWH', 'H6Z8A', 'WKBXS', 'OQPO4', 'TU56N', 'GNOAC', '5FZ1C', 'JAPQV', '4FM9A', 'ZWBT6', '958K9', 'ZIRA5', 'TOGNQ', 'L3FZH', '4NOEU', '4MD09', '66808', 'JI69U', 'SL2DO', 'NH5AG', 'KHIIQ', 'S6UZQ', 'O0JR8', 'DOAQC', 'DI2PR', 'H717G', '2MQX8', 'LM5BB', 'MECIE', 'WT2TI', 'UICYQ', 'LZ67V', 'G3KAX', 'H31TF', 'NTUL8', 'BDA21', 'GNLI0', 'Y244I', '5NDEL', 'AUICO', 'TSFJL', '35EQY', 'X8GPF', 'GZSD6', 'TDNS2', 'A4OXV', 'SSI46', 'S94O4', 'U4IY0', 'Y6YX5', 'UGLRI', 'A8T0T', '3CDMG', 'R1JNV', 'CXHUH', 'YIUII', 'YSDP5', 'XB7DR', '32H9J', 'EJ5ND', '1O5YK', 'MHJVJ', '3DG7V', 'H5PQ4', 'CUOPD', 'RL5DH', 'JKM5R', '0OPNW', 'WJ6NX', '1TO4R', 'JFJBU', 'R0BBZ', '0VQON', '5CZ7X', '5BPIK', 'QD6PV', 'OW6DL', 'Y1LMQ', 'DMGI4', 'CWYYX', 'KHY61', 'TA9Y5', 'EFUJO', '46M9G', '77SV5', '5QC0Y', 'MAYWR', 'B2PKT', 'QHBSM', 'QJDIS', 'HZM3U', 'T4BV2', '38YDT', 'AWNA8', 'YXY1U', 'GUVXC', 'DGEA9', 'YFGE6', 'AAUWT', 'NYRTZ', '78R45', 'JR097', 'AB3I0', 'LVVY7', '7ZN5Y', 'EZLOI', 'NYVEE', 'IPB96', 'LKTGL', '0HPXW', 'Z0MV0', 'DZP4C', 'AKM9U', '0LTFV', 'FS7BG', 'IA8D5', 'CNRHO', 'LXXGK', '4W4VB', '4C5DM', '92MVX', '2I2AM', 'OMWAX', 'GU2T9', 'YKI4R', 'JB6Z5', 'W0GD8', 'WEC4I', '67RHF', 'ZNPEI', 'S8DFT', 'GAOIA', 'ZZTIL', 'DVDNL', '4QT9G', 'U2MU7', '15ZEW', 'H2CSF', 'IVK72', '01FCY', 'FD3BC', 'GBH33', 'EGEFV', 'UAZ77', 'LHLJ7', 'AX34B', 'DLUHA', 'V695V', 'J3LCX', 'CIETC', 'GOTT9', '455OR', 'JHLUV', 'WOW87', 'Y9SDT', 'LMJT6', 'ZI0ZX', 'DA1NJ', 'KCK0G', 'YJ2UN', 'QGNF0', 'S2GTL', 'KHOAW', 'DC9V5', 'BLXSJ', 'MJLM3', '2EO1F', 'TKJ3B', 'TAAZ7', 'QGLWP', '7BR1F', 'Y5UM2', 'RLC4X', 'YCB3B', 'CNJY1', '120AX', '2WNES', 'UP8NR', 'JDNXU', 'C7EOZ', '6OG62', 'UHJW9', '8Z80L', 'ASLFO', '06IMG', '2CBUL', 'Z1R8V', 'RO3SY', '9QUAV', '9VB70', '139DT', 'B48WD', '2ZF5B', 'NUE29', 'ICUNC', '3IB9C', '5BJNJ', 'GML6P', 'XVUD8', 'IJKMP', '4LCPO', 'U95Z2', 'WX1HZ', 'EF1M2', '0G4ER', 'P3FZH', 'OE918', '8WCEC', 'VFSCC', 'HWFZK', '66PG1', 'NYOAP', 'AD92N', 'VUZEF', 'WMEPW', 'ZRA7W', '6T3IN', 'WQYB9', 'T4A06', '7KOGD', 'KR0WC', '9VJFJ', 'ZG2PL', '5S4RP', 'OX6SW', 'CHYI5', '9Q062', 'S7W6F', 'ETKD6', 'KGE9Y', 'UEO8P', 'RC3YK', 'EZYON', 'MXUEZ', 'K794S', 'NOVLH', 'F0QUE', 'CQS9V', 'TWJ5G', '9FGEU', 'QVSR4', '6F6C9', '7XNAE', 'C1TUF', 'IK0RI', '39R9X', 'BII2Z', 'GKVO9', 'QNJ9L', 'HLHBP', '54HY4', 'XYVB0', 'SJOGC', '7ZC21', 'I4P1B', 'FZIM3', 'SXFZS', 'BE5TW', '1CHWQ', '2C1D3', '6ZI0L', 'K87W4', 'LVWM3', 'FNVPX', '0C9JZ', '8OOBD', 'AB6AJ', '6W97J', '5QGPK', 'RSVGS', 'UJUD8', 'SSHB1', 'PAJB5', 'MOF8E', 'TIMMU', 'G0MVC', 'DTU82', 'E9P01', 'SM9KX', '93PY9', 'XQ0RT', '4UK3A', 'ZR0SL', 'I9JSW', 'HXGW1', 'H2ZT4', 'NSDSL', 'OWH70', '0C8AC', 'IFCFV', 'D6K61', '01SX1', '1JT4S', 'PD830', 'W4QSU', 'PS6TE', 'K7DLX', 'A2D7U', 'RCGWC', 'WOLVO', '7DNL9', 'C3M5O', 'C5KD7', 'QVPF3', 'WHBMM', 'C8UV7', 'ZJBXH', '498VM', 'WX2YP', 'Z7C8A', 'UAL55', 'I9C0Q', '6OVZH', 'VN9NM', 'HNU27', '3XH7H', '1F0V8', 'O3GF0', 'E75WJ', 'QSY9E', 'UB7XB', 'UQLKZ', 'OEG5G', 'J2DVL', 'GKBKY', 'P3JQP', 'NCJH3', 'B2BSP', 'VLTEE', 'S2O1L', 'NIE03', 'MAD6J', 'UCSBT', 'GEX78', 'JDTWH', 'HUQU1', 'N6JAQ', 'PGT5K', 'IEBZ6', '7TFLK', 'MWZQW', '2FF8P', 'G5Z0W', 'Q9DUM', 'Q41BX', 'R6O3W', '5SOSM', 'KQREC', 'FNNMW', '3LUWE', 'HGG7X', '7KY0E', 'WSRXU', 'TYSKT', 'KEB7Q', 'NM2G9', '2G68C', 'FJWNU', 'KTHFP', '92DCP', 'L9FHP', 'NCI96', '1A78U', 'QU5XV', '5VYDQ', 'X6Z9Z', 'IV4ED', 'UTGC1', 'RML2U', 'J18SO', 'EP4ST', 'T6ZH5', '9ZXFF', '4FV28', 'HVRS7', 'DECHI', 'X7SZ5', 'NVF7Q', '894EH', 'ZCEGM', 'SS2HU', 'AN70Z', '2D1VS', 'MVQ5E', '605R3', 'BI4YM', 'PFE0N', '5X077', '0Q4AE', '49SF8', '3K0MY', 'W17A5', 'J6RIB', 'Y6MKI', 'P9H0J', 'TP2BL', 'TTU0K', 'K3BDL', 'A9EK3', '15Z99', 'O0V3E', 'E01E3', '2H0T1', 'DCJYN', '9R8S5', 'VX1YX', 'THJWB', '0FAJN', 'GJDDA', 'J65AB', '5RU2P', 'Z6BX1', 'AD5T1', 'H7E7D', 'CWSWN', 'YL0FM', 'EQ27L', 'YP77I', 'RQFV7', 'HJ58S', '9M0PT', '7JMVD', 'VN6CC', 'LPYPN', 'Y12B2', '6WQMG', '4DCQU', 'HNVIF', '01IZ4', '65PQB', 'HXDUC', 'L9THG', 'JXP1U', 'WU7Y5', 'LZJPH', '1KY2H', 'COOC6', 'RVDEE', 'NI54O', 'EO0KL', '2S0Z4', 'QR3LY', 'T64ZN', 'FMGPB', 'SPZJQ', 'Z75G1', 'U1AX6', 'PO65K', 'USI98', 'K6X9W', 'IYUAX', 'EXBXB', 'ID5XW', 'NUDZX', 'D5ZM8', '94C1J', 'TRJ5O', 'S888U', 'QNCGE', 'NWMVC', 'PMQNP', 'MV0M1', 'RZWQH', 'A3W8Q', '2HRRM', '1O8XF', 'AC54A', 'JBR9H', 'WYMNI', '5OWNM', 'YR867', '05UEZ', '3BXLO', 'L8S7L', 'ZCGJR', 'QE31G', 'VCEX0', 'C12J2', '30VV9', '2DP53', 'YD3RL', 'ISFXW', 'KAHYK', 'X7NQ8', 'Z53NX', 'JFJIV', 'U4T9B', 'GXQAJ', 'UN4NF', '7B67T', '7IFXN', '42WV7', 'YT32Q', 'VDUXW', 'S9QX8', '2UM7M', '04HU1', 'BUEY6', '63DT1', '7UXGR', 'UZ6Y5', 'LO2BW', 'PGSBQ', 'EYXTH', 'NTLWP', 'B9W64', 'A89RW', 'AA0AQ', 'I8HAO', 'QBY1A', 'Z1FJS', 'ULN48', 'RIB43', '2DRV9', 'W1EWA', '8FU3Z', '9P0AS', 'TF77L', 'UVDNU', 'W65Q8', 'RQXCM', '7RGRS', 'VLW9E', '34ISY', 'I6H23', 'OOBWU', 'HSHUY', 'W31AS', 'LHBAE', '77JH7', 'AIOA8', 'SR2SQ', 'ILBJ9', '5UUPQ', 'OQRUY', '0M9PD', '109U1', 'FLI3L', 'LIH7T', '1PLWK', 'I90LJ', '4SK6D', 'RONA8', 'PRU5R', 'OOPUF', '4VU6A', 'C3LR1', 'ML4ZN', 'U1WMI', '0Q71J', 'H1OYU', '6LIZH', '1M67Z', 'ZGJ46', 'KZ0RG', 'PUH3B', 'DB3JD', '5CJIC', 'XWLGE', 'MULC7', 'L34QG', 'JAJ4L', 'FD44E', 'CKSDI', 'S2S9V', 'H2VJZ', '5GZWL', 'TZUWH', 'Q3K4S', 'R2RPW', 'NBUMJ', 'BT71L', 'OGMNS', '4B27G', '7GU0F', 'XVYSJ', '3BABF', 'BARG3', 'MQBIR', 'U14DG', 'ULZUM', '01ZP1', 'UW19S', '4IYJ9', 'GUZU9', 'HE2MQ', 'CMSCW', '4JU27', 'D1GGP', '6OXZY', 'OH6NI', 'BQ61O', 'MG15H', '5XIZP', 'ESTKZ', '877LG', 'B3DY3', 'N4SMQ', 'QJGUD', '7KTH4', 'VAFPE', 'L995Y', 'CLNMY', 'KRCRX', 'DNVHA', '88N1E', 'N60LF', 'OPCVK', 'JY73P', 'X7FQL', '70SS0', '9LN5S', '3WHO8', 'V7YZ3', 'IAQ8L', 'RKLHQ', 'RTVZ8', 'NAMUL', 'W0CI5', 'DZ575', 'B2BTB', 'KR1I3', '1CUEM', '64M3M', 'UOJ6Q', 'VE1YM', 'WJA4H', 'V8303', 'FU2YE', 'A4DQU', 'KAUFS', '6B5A6', '2NDKJ', 'O4RZ5', '5KC49', 'UJ43Q', 'ZS1U8', '2IQ1L', 'P1FF3', '4G3QL', 'F4WTN', 'ZTAS3', 'WJNTW', 'OV66V', '196EO', 'DP1CB', 'OAGKX', '3H72P', 'HHY87', 'E8YPQ', '0743F', '7RP0J', '7L0XJ', 'PKUL7', 'MUNC3', '67OR3', 'QWEYO', 'LBTZU', 'VKWM1', 'HPWKT', 'FC6IP', 'K25ER', 'IU70G', 'X7HD1', 'SR1Z2', 'HF2OL', 'HILFW', '71O6H', 'Z5LPS', '1G6TN', 'BUWKF', '46YOR', 'XGUE0', 'S8XZP', '9L4SW', 'DCM3Z', '739K3', 'BYXON', 'Z21SU', '8XLNV', 'XSW3X', '9N7UW', 'LEPM8', '1336O', 'P7ENX', 'S4XD5', 'CWGBQ', 'DFPYS', 'RUBE3', 'BNHIQ', 'KDE7T', 'QG274', 'WOLZD', 'YK2J0', 'ZUHOU', 'B9EFB', 'IWTU8', 'CFYO5', 'WA2SL', 'SVVQM', 'BSBFM', 'YLUW0', 'V9ZPS', 'KMBPH', '13XTX', 'GWY51', 'A4BZD', 'XMW1K', 'YF3L1', 'DRCD7', 'EQMBL', '542LZ', 'LIH26', 'XETLP', 'IHHSS', 'KC8O8', 'AB5S0', 'NQKT9', 'N4KV2', '42CL9', '022JN', 'D84F7', 'STJN8', '5QK3X', 'W28NF', '4DU43', 'PLYUS', 'HF1LB', '2V8AM', 'WR0M1', 'HDPL0', 'W6ABX', 'N5SX4', 'CM2FT', 'JHJM4', '06X1S', 'XTWCN', '67G23', 'JX4BR', '1X1EI', 'XMH2A', 'Y84SA', 'NU7V2', 'ZFOEW', 'WI3LC', 'ZQ4P3', 'M2RL5', 'O9RXT', 'C1JCV', 'NWBEA', 'ASMS4', 'GR3KP', 'XXDOS', 'EIRQA', 'YL3OC', 'ECL1K', 'G65HY', 'CXQGE', 'FQQZ6', 'GO05E', 'DX6UG', 'XSH4V', 'AE4UQ', 'F7W4A', '3N6DN', 'HFHD3', '8KYJ9', 'IOUNP', 'SEQLB', 'XCKX2', 'WH0TN', 'ULBJF', 'HKMJ9', 'OSL59', 'QV1CF', 'GTJGO', '17L7A', '5FMNM', 'OG5NV', 'ENWMD', 'P7HJH', 'X9SWK', '455I5', 'KKEXN', 'FQL9H', 'NQYRM', 'SEXYC', 'THQQY', '4IBMM', '7JU7R', '9NDLR', '3RQBE', 'VQH91', '6MY5B', '40LJY', '0CS6T', '86UAV', 'GUAX6', 'VTYL3', '5BQNB', 'JSAU0', '6TF92', '0WK9Z', '6XX57', '9GDMN', 'CYA1O', 'YDZWA', 'DMOLV', 'CHH8S', 'DVS46', 'FH11Q', 'QW912', 'RGGR9', 'FGQBL', '7G49O', '4QB8R', 'UFCUF', 'XV8KV', 'KPEQ5', 'WOG5B', 'RF902', 'B33J5', 'YAH73', '283X5', '0MS4F', 'VO7E0', 'O5OVW', 'QQRH4', 'LW7DJ', '847Y6', 'G3M9J', '7Y0P9', '0JOIT', 'XLEBP', 'EUA3C', 'TF1JP', '0K0PO', 'MRPEI', 'OA3V1', '6UNOS', 'HXBU9', 'DYFR6', 'JUWUR', '52LW2', 'U2ZMU', 'WEUBK', 'D0F63', 'LACGB', '98EKP', '8LM20', 'EMPA0', 'UVTZG', '2BXVZ', '20IGG', 'PYWDC', 'ZKIIQ', '4O7DO', 'PY0DD', 'DPIF8', '09G8U', '74DSU', 'GZ5N5', '88JWO', '1QSBJ', 'SFS15', '6COI0', 'YMONY', 'EUS20', 'UVYVS', 'RTLHI', '556X0', 'EBOQR', 'GD4Q1', '70REI', 'BGJ62', 'WC0DP', 'ZCGWR', 'K73OT', '97H6P', 'TNPV6', '9DYBP', 'SQL2U', '0EKDW', 'M6ZD7', 'ZDNID', 'XTSC6', 'NXL88', 'YSQB8', 'FT6RZ', 'XKHRD', 'KLZRC', '1H6MV', 'KEG6O', 'W0Y02', 'ML4Y3', '09JS4', 'JOA9U', '8COV3', 'ABWFR', '4RMO5', '0JXFX', '1XDAD', 'OZRYG', 'KRTJA', '4EVYY', '7KLFF', 'OW837', '1Y4SW', '8TU9J', 'DBQBJ', 'FUWCC', 'JX32K', 'VWB6M', 'D75BM', 'W6UG1', 'WFKT7', 'H6A7P', '214RF', 'HBWMD', '9G3L4', '7MZ6J', 'URM9A', '4EQKN', 'ZKV1V', 'NIYH2', '2ZD7C', 'W3XP3', 'ZPZMF', 'ND383', 'OD1Q0', 'UCGYU', 'YHT62', 'HVM4M', '57FZA', 'M24S9', '5Y9KY', 'FD6QR', 'LZ2T2', 'CG9DD', 'F85CA', 'RFXJF', 'QKPTO', '9LS0F', 'MG1D9', 'XD27Z', 'UV8BP', 'NH9AM', '1XW3J', 'QXBXN', 'GF1XM', 'STF1X', 'WEH2A', '4TJPH', '0X7EJ', 'LXYX0', 'LKZ5A', '0PP8V', 'U6KCU', 'NBKTP', 'P6OW7', 'PZV7S', '0EVYI', 'SBV2H', 'XKV89', 'J74W5', 'ZVKPY', '6V6NW', 'N6Z5W', '2QPT8', 'XSRUN', 'K77ZJ', '2W5R3', '8N28F', 'OARY7', 'L4LWU', 'L4WQ6', '06WTA', '0TWSJ', 'UWIY8', 'CVIBB', 'X97A0', '0LJS2', 'K0W5Z', 'BI2W2', '5IWL1', 'SKEDK', 'BCM6W', 'C803Y', 'BNW45', 'BE2W5', 'PEPLZ', 'SCI3F', 'MXC2Z', 'LYFEZ', '5854U', 'TDL61', 'MKR3R', 'JLJ0I', '00XZO', 'IDPBX', 'LIHUZ', 'A9NEO', '39QED', 'WSBNI', '0013M', 'NVJ15', 'SY3II', '0E9ZD', 'TAJ45', 'ZQA5N', '9G8GL', 'R6N5L', 'WCKPP', 'H8AUG', '5ZVE5', '79QVD', 'PGSLN', '2U89W', 'HI75W', 'K0FNX', 'XM58T', 'BPQP8', 'VGHK7', 'ZNSMQ', 'ZKBOH', 'RDK4T', 'NBWW2', '9AT4C', '7OZDQ', 'FLHT6', 'D9YY2', 'MRXMS', 'KDKRD', 'CBYB0', 'D981Z', '2UDLY', '87HU0', 'ORJK0', 'EJC3Z', 'KHGY7', '31Q4I', 'OXBS7', 'DTBPW', '2XY9V', 'F5UNJ', 'T47T1', 'GWTEU', 'UPU3B', '6XCUY', 'CHXUK', '4WQA9', '6WZ5E', 'SYEEE', 'IZX1I', 'CA8ZW', 'ZDS9U', '06NBW', 'BD8I4', '5OJDB', 'SIKV3', '6YNO0', 'BEVSC', '2DQDW', '7SFOC', 'BOW7G', 'TB0QG', 'R9XJH', 'NY78C', '0ROC3', 'QCUW3', 'QKQCN', 'NIVY5', 'XEDIM', '76CNC', 'C8IIT', '29GJ7', 'XYI3L', 'P0MQR', '3D2NV', 'JPW5L', 'G7DZ1', 'BYZNO', '6D77B', 'SRVNO', '4P8IE', 'VBVJV', '2OJAH', 'PCQCF', 'GL33I', 'G9G9I', 'Y5DEF', 'UIAP4', 'XWI4F', 'S3JEF', '1RMQJ', 'RSK8M', 'MT6P7', 'UTVIT', 'F1RN0', '2PDHA', 'A0D5V', 'KBL3R', '0UQVN', '3CKDW', '2B0K8', '03JI1', '1ZWYS', 'PP3OR', '5VX5T', '2XMGF', '6NIKA', '1689G', 'J0ZPD', 'N106O', 'Q7238', 'GNPFD', '9PQHJ', 'VPE3U', 'V9S69', 'J183R', 'NZBF3', '7XTCD', 'P918K', '2SQ3A', 'BGRNV', 'N5ODM', 'YNEWY', 'A7PDI', '2SNMU', '2ZL46', 'KT0F3', 'VH2B8', 'BXD4U', 'DA8LH', 'VOOMN', 'JEDT6', 'F9832', 'ZCVKV', 'K7MOE', 'JYTS9', 'B9T2Z', 'JU1FA', '80NQ0', 'J1QU3', 'IY1YS', 'WKRXI', 'T6NMK', 'GL72X', 'RVWSN', '6ZIM9', 'WU7L2', '6N3LE', 'PJQE5', 'J1U89', '0ZUN9', 'E5M4X', '1ITPL', 'F0YSF', 'XUS3R', '0QENK', '1FMZY', '7M6C6', '0KPA7', '5NWWL', 'ZB6V0', 'WKNUI', 'HKNKE', 'G6UL8', 'ON77G', '6475W', 'YANRJ', 'KXOGH', 'G5HAE', '0O59Z', 'WJZIN', '6KXU7', 'B6JBA', 'VZRN2', 'NX7NT', 'SP31N', '877Q3', 'FICBN', 'UU3YV', '17L9F', '6NKSX', 'W7QUU', 'YLSGZ', 'SLQ02', 'NPOYC', 'E1C72', '307RJ', '4SK3N', 'I61Q3', 'WA4YD', 'Q8QVE', '5F0VJ', 'LB22W', 'VTNOG', '4ZNFK', 'B2O0J', 'PPFE4', '05GH0', 'DH0ID', 'IQIWW', '7EJVS', 'I1UD4', '0KFMC', 'T0E7T', 'B3FLG', 'M0U6M', '68I1C', 'EYTNX', 'AJXKY', '0XXOH', '86HH3', 'UE8G1', 'D99PL', 'NRXT2', '0WGC1', 'W5IBY', 'ZBGV2', 'TN8R4', 'VHBR7', '6X7GQ', '7MX40', 'ZFVQ2', 'LPL0G', '0HNN3', 'BCR64', 'FG0IK', 'EY9AH', '0MGKR', '21S92', 'FI3RJ', '42XMQ', '24MDY', 'GXSCN', '2D7UZ', 'YT5N2', '6ZDPF', 'PNMY8', 'ZGUOR', 'L8H5M', 'H997H', 'RZUYM', 'SH87T', 'IVEBB', 'VBCY6', 'A62WP', 'ROX3G', 'C1E1B', '80209', 'J2WDK', 'UDI87', '6A0BQ', 'UD8CA', '6I52N', 'FK4M8', 'VK361', 'TWT12', 'ZT4VQ', '34851', '1BGSK', '1NR0I', 'BHPKG', 'CBQNE', 'ZEJ7C', 'GFW73', 'LF9UC', 'VOR8H', 'H4RTD', '3SMS0', 'DEC23', '6HEBG', 'MD2OL', 'LECDW', 'EX8C6', 'ORM4P', 'QVHUF', 'PQKTL', '3L9ZY', 'XLOVN', '353RL', 'XXE0W', 'JE9R2', '34WPK', '1ZK6D', 'J93E7', 'TS8TC', 'CI4K7', '8LUY3', '84BM0', '66T9C', '191N0', '5MD23']
    },
    'InitialCodeRegistrationPolicy':{
        'name':'Initial Code Registration Policy',
        'active':True,
        'module':'userprofiles.registrationpolicies.initialcoderegistrationpolicy',
        'codes':['ZM26R'],
        'usage_limit':50
    },
}

LOGIN_POLICY = {
    'module':'userprofiles.loginpolicies.defaultloginpolicy'
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
    from settings_production import *