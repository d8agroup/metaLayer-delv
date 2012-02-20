YOUR_CODE_ROOT = '/projects/metalayer/dashboard/'
########################################################################################################################

DEBUG = True

COMPRESS_ENABLED = False

SITE_ID=u'4f13fca68451d31efe00001d'

SITE_HOST='localhost:8000'

SITE_HOST_SHORT = SITE_HOST

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
        'ENGINE': 'django_mongodb_engine',
        'NAME': 'ml_dashboard_tmcneal', 
        'USER': '',
        'PASSWORD': '',
        'HOST': 'mongodb://metalayer:M3taM3ta@staff.mongohq.com:10063/ml_dashboard_tmcneal', 
        'PORT': 10063,
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



