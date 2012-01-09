DEBUG = True

ADMIN_MEDIA_PREFIX = '/static/admin/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/home/matt/code/metaLayer/dashboard/dashboard.db', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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
    'default_page_size':20,
    'solr_url':'http://md.dev.01:8080/solr',
    'solr_params':'wt=json&facet=on',
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



