import logging

DEBUG = False

SESSION_COOKIE_SECURE = False

SITE_ID=u'4f1d5db8c845b30a5600001d'

SITE_HOST='50.57.164.87'

SITE_HOST_SHORT = SITE_HOST

IMAGE_HOST = SITE_HOST

STATIC_HOST = SITE_HOST

STATIC_ROOT = '/usr/local/metaLayer-dashboard/dashboard/static/'

logging.basicConfig(
    level = logging.ERROR,
    format = '%(asctime)s %(levelname)s %(message)s',
)

DB_LOGGING = {
    'logging_level':0, #0=ERROR, 1=INFO, 2=DEBUG
    'database_name':'ml_dashboard_staging',
    'database_host':'mongodb://metalayer:M3taM3ta@staff.mongohq.com:10081/ml_dashboard_staging',
    'database_port':10081
}

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

TEMPLATE_DIRS = (
    '/usr/local/metaLayer-dashboard/dashboard/static/html/'
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

CHARGIFY_SETTINGS = {
    'api_key':'eWdDw0im7NE0lfXeiXhS',
    'subdomain':'metalayer-dashboard'
}

FACEBOOK_SETTINGS = {
    'api_key': '140737952711154',
    'requested_permissions': ['offline_access']
}

TWITTER_SETTINGS = {
    'api_key': 'lFEg1EXUmGlOqSto656Etw'
}

