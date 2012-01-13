from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'run_all_dashboards', run_all_dashboards),
)