from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'c/(?P<width>\d+)/(?P<height>\d+)/(?P<dashboard_id>\w{24})\.png$', crop),
    url(r's/(?P<max_width>\d+)/(?P<max_height>\d+)/(?P<dashboard_id>\w{24})\.png$', shrink),
    url(r'facebook/(\w{24})\.png$', insight_image_for_facebook),
    url(r'(?P<width>\d+)/(?P<height>\d+)/(?P<fill_color>[0-9a-fA-F]{6})/(?P<dashboard_id>\w{24})\.png$', insight_image),
    url(r'(?P<width>\d+)/(?P<height>\d+)/(?P<dashboard_id>\w{24})\.png$', insight_image),
    url(r'(\w{24})\.png$', insight_image),
)