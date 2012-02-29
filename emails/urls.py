from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'view/(\w+)$', view_email),
    url(r'view/(\w+)/([a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})$', test_email),
    url(r'$', email_list),
)