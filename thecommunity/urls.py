from django.conf.urls.defaults import patterns, url
from dashboard.thecommunity.views import *

urlpatterns = patterns('',
    url(r'restricted_access$', no_access),
    url(r'welcome$', login_or_register),
    url(r'logout', logout),
    url(r'current_subscription', current_subscription),
    url(r'change_subscription', change_subscription),
    url(r'create_from_template$', create_from_template),
    url(r'insights/load/([a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})$', load_dashboards),
    url(r'insights/load/([a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})/(\d+)$', load_dashboards),
    url(r'trending_insights/(\d+)$', load_tending_insights),
    url(r'top_insights/(\d+)$', load_top_insights),
    url(r'recent_insights/(\d+)$', load_recent_insights),
    url(r'remixes/(\w{24})/(\d+)$', load_remixes),
    url(r'delete_insight/(\w{24})$', delete_insight),
    url(r'[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}/account$', user_account),
    url(r'([a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})$', user_home),
    url(r'([a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})/(\w{24})$', insight),
    url(r'([\w ]+)', category_page),
    url(r'^$', community_page),
)