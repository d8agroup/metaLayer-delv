from django.conf.urls.defaults import patterns, url
from dashboard.thecommunity.views import *

urlpatterns = patterns('',
    url(r'welcome$', login_or_register),
    url(r'logout', logout),
    url(r'current_subscription', current_subscription),
    url(r'change_subscription', change_subscription),
    url(r'insights/load', load_dashboards),
    url(r'[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}/account$', user_account),
    url(r'[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', user_home),
    url(r'^$', community_page),
)