from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'users$', users),
    url(r'insights$', insights),
    url(r'emaillists$', emaillists),
    url(r'$', home),
)