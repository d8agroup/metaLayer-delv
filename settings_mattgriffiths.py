import logging

SITE_DOWN = False

#ROOT_URLCONF = 'dashboard.urls_admin'

DEBUG = True

COMPRESS_ENABLED = False

SITE_ID=u'4f4350a1c845b31cd500001d'

SITE_HOST='localhost:8000'

SITE_HOST_SHORT = SITE_HOST

IMAGE_HOST = SITE_HOST

STATIC_ROOT = '/home/matt/code/metaLayer/dashboard/static/'

DYNAMIC_IMAGES_ROOT = '/home/matt/code/metaLayer/dashboard/imaging/CACHE/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

SENTRY_DSN = 'http://cb7488e51e224f0ab7a04d53f8dede4b:b1a294ea3aab42148f4cab2b21c0c429@108.166.111.61:9000/4'

INTERNAL_IPS = ('127.0.0.1',)

CACHES = {
    'default':{
        'BACKEND':'django.core.cache.backends.dummy.DummyCache',
    }
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

TWITTER_SETTINGS = {
    'api_key': 'lFEg1EXUmGlOqSto656Etw'
}


