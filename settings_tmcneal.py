YOUR_CODE_ROOT = '/projects/metalayer/dashboard/'
########################################################################################################################

DEBUG = True

COMPRESS_ENABLED = False

SITE_ID=u'4f13fca68451d31efe00001d'

SITE_HOST='localhost:8000'

SITE_HOST_SHORT = SITE_HOST

IMAGE_HOST = '50.57.227.192'

STATIC_ROOT = '%sstatic/' % YOUR_CODE_ROOT

DYNAMIC_IMAGES_ROOT = '%simaging/CACHE/' % YOUR_CODE_ROOT

DB_LOGGING = {
    'logging_level':0, #0=ERROR, 1=INFO, 2=DEBUG
    'database_name':'ml_dashboard_dev',
    'database_host':'mongodb://metalayer:M3taM3ta@staff.mongohq.com:10049/ml_dashboard_dev',
    'database_port':10049
}

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ml_dashboard_dev', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'mongodb://metalayer:M3taM3ta@staff.mongohq.com:10049/ml_dashboard_dev',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': 10049,                      # Set to empty string for default. Not used with sqlite3.
    }
}

TEMPLATE_DIRS = (
    '%sstatic/html/' % YOUR_CODE_ROOT
)

SOLR_CONFIG = {
    'default_page_size':20,
    'solr_url':'http://50.57.164.216:8080/solr',
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
    'api_key': '109882859079797',
    'requested_permissions': ['offline_access']
}

