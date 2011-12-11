from django.conf.urls.defaults import patterns, include, url
from dashboard.userprofiles.views import *

urlpatterns = patterns('',
    url(r'login$', user_login),
    url(r'logout$', user_logout),
    url(r'home$', user_home),
)