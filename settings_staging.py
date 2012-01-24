import logging

DEBUG = False

COMPRESS_ENABLED = True

SESSION_COOKIE_SECURE = True

SITE_ID=u'4f1d5db8c845b30a5600001d'

SITE_HOST='50.57.164.87'

STATIC_ROOT = '/usr/local/metaLayer-dashboard/dashboard/webapp/static/'

logging.basicConfig(
    level = logging.ERROR,
    format = '%(asctime)s %(levelname)s %(message)s',
)

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ml_dashboard_staging', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'mongodb://metalayer:M3taM3ta@staff.mongohq.com:10081/ml_dashboard_staging',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 10081,                      # Set to empty string for default. Not used with sqlite3.
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
    '/usr/local/metaLayer-dashboard/dashboard/webapp/static/html/'
)

SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://50.57.164.216:8080/solr',
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
        #'feed',
        'googleplusactivitysearch',
        'twittersearch',
        'googlenewssearch',
        ]
}

ACTIONS_CONFIG = {
    'enabled_actions':[
        'datalayersentimentanalysis'
    ]
}

OUTPUTS_CONFIG = {
    'enabled_outputs':[
        'atomoutput',
        'jsonoutput'
    ]
}

CHARGIFY_SETTINGS = {
    'api_key':'eWdDw0im7NE0lfXeiXhS',
    'subdomain':'metalayer-dashboard'
}



