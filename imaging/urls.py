from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'(\w{24})\.png$', insight_image),
)