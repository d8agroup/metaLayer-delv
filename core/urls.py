from django.conf.urls.defaults import patterns, include, url
from dashboard.core.views import *

urlpatterns = patterns('',
    url(r'^$', index),
)