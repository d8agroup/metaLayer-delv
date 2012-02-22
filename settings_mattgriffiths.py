import logging

DEBUG = True

COMPRESS_ENABLED = False

SITE_ID=u'4f1408ebc845b317df00000d'

SITE_HOST='localhost:8000'

SITE_HOST_SHORT = SITE_HOST

IMAGE_HOST = SITE_HOST

STATIC_ROOT = '/home/matt/code/metaLayer/dashboard/static/'

DYNAMIC_IMAGES_ROOT = '/home/matt/code/metaLayer/dashboard/imaging/CACHE/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s %(levelname)s %(message)s',
)

DB_LOGGING = {
    'logging_level':0, #0=ERROR, 1=INFO, 2=DEBUG
    'database_name':'ml_dashboard',
    'database_host':'localhost',
    'database_port':27017
}

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
    '/home/matt/code/metaLayer/dashboard/static/html/'
)

SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://50.57.164.216:8080/solr',
    #'solr_url':'http://md.dev.01:8080/solr',
    'solr_params':'wt=json&facet=on&sort=time+desc&rows=100&facet.mincount=1',
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

CHARGIFY_SETTINGS = {
   'api_key':'eWdDw0im7NE0lfXeiXhS',
   'subdomain':'metalayer-dashboard'
}

FACEBOOK_SETTINGS = {
    'api_key': '140737952711154',
    'requested_permissions': ['offline_access']
}



