from django.conf.urls.defaults import patterns, url
from views import *

urlpatterns = patterns('',
    url(r'view/invite$', view_invite),
    url(r'$', email_list),
)