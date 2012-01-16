DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django_mongodb_engine', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ml_dashboard', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ENDPOINTS = {
    'datapoints':{
        'metalayer_aggregator':{
            'add_source':'http://localhost/aggregator/sources/add',
            'remove_source':'http://localhost/aggregator/sources/remove'
        }
    }
}

TEMPLATE_DIRS = (
    '/usr/local/metaLayer-dashboard/dashboard/webapp/static/html/'
)

SOLR_CONFIG = {
    'default_page_size':20,
    'solr_url':'http://localhost:8080/solr',
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
    'enbaled_data_points':[
        'feed',
        'googleplusactivitysearch',
        'twittersearch',
        'googlenewssearch',
    ]
}

CHARGIFY_SETTINGS = {
    'api_key':'eWdDw0im7NE0lfXeiXhS',
    'subdomain':'metalayer-dashboard'
}



