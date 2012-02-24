import logging

DEBUG = False

#If admin deployment, enable admin urls
import socket
if socket.gethostbyname(socket.gethostname()) in ['50.57.128.82']:
    ROOT_URLCONF = 'dashboard.urls_admin'
    DEBUG = True

COMPRESS_ENABLED = True

SESSION_COOKIE_SECURE =False

SITE_ID=u'4f421f767a9c1b687b00001d'

SITE_HOST='metalayer.com'

SITE_HOST_SHORT = 'mlyr.co'

IMAGE_HOST = SITE_HOST

STATIC_ROOT = '/usr/local/metaLayer-dashboard/dashboard/static/'

DYNAMIC_IMAGES_ROOT = '/usr/local/metaLayer-dashboard/dashboard/imaging/CACHE/'

CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION':'108.166.125.118:11211',
    }
}

DB_LOGGING = {
    'logging_level':0, #0=ERROR, 1=INFO, 2=DEBUG
    'database_name':'ml_dashboard_production_logging',
    'database_host':'mongodb://metalayer:M3taM3ta@arrow.mongohq.com:27094/ml_dashboard_production_logging',
    'database_port':27094
}

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ml_dashboard_production', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'mongodb://metalayer:M3taM3ta@arrow.mongohq.com:27093/ml_dashboard_production',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 27093,                      # Set to empty string for default. Not used with sqlite3.
    }
}

TEMPLATE_DIRS = (
    '/usr/local/metaLayer-dashboard/dashboard/static/html/'
)

SOLR_CONFIG = {
    'default_page_size':100,
    'solr_url':'http://108.166.104.151:8080/solr',
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
    'api_key': '301310309930630',
    'requested_permissions': ['offline_access']
}

TWITTER_SETTINGS = {
    'api_key': 'lFEg1EXUmGlOqSto656Etw'
}

