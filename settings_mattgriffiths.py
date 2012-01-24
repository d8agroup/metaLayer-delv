import logging

DEBUG = True

COMPRESS_ENABLED = False

SITE_ID=u'4f1408ebc845b317df00000d'

SITE_HOST='localhost:8000'

STATIC_ROOT = '/home/matt/code/metaLayer/dashboard/webapp/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

logging.basicConfig(
    level = logging.ERROR,
    format = '%(asctime)s %(levelname)s %(message)s',
)

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ml_dashboard', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 27017,                      # Set to empty string for default. Not used with sqlite3.
    }
}

ENDPOINTS = {
    'datapoints':{
        'metalayer_aggregator':{
            'add_source':'http://md.dev.01/aggregator/sources/add',
            'remove_source':'http://md.dev.01/aggregator/sources/remove'
        }
    }
}

TEMPLATE_DIRS = (
    '/home/matt/code/metaLayer/dashboard/webapp/static/html/'
)

SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://md.dev.01:8080/solr',
    'solr_params':'wt=json&facet=on&sort=time+desc&rows=100',
    'solr_facets':{
        'source_display_name':{
            'display_name':'Source',
            'enabled':True,
            },
        'channel_type':{
            'display_name':'Type',
            'enabled':True,
            },
        'tags':{
            'display_name':'Tags',
            'enabled':True,
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
        'datalayersentimentanalysis',
        'yahooplacemaker',
        'languagedetection'
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
        'googlegeochart'
    ]
}

CHARGIFY_SETTINGS = {
   'api_key':'eWdDw0im7NE0lfXeiXhS',
   'subdomain':'metalayer-dashboard'
}



