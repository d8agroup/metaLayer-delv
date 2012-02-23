from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'facebook/(\w{24})\.png$', insight_image_for_facebook),
    url(r'c/(?P<width>\d+)/(?P<height>\d+)/(?P<dashboard_id>\w{24})\.png$', crop),
    url(r's/(?P<max_width>\d+)/(?P<max_height>\d+)/(?P<dashboard_id>\w{24})\.png$', shrink),
    url(r's/(?P<max_width>\d+)/(?P<max_height>\d+)/(?P<dashboard_id>\w{24})/(?P<visualization_id>\w+)\.png$', shrink),
)