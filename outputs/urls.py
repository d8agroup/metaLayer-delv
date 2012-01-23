from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'(\w+)', generate_output),
)