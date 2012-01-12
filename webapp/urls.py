from django.conf.urls.defaults import patterns, url
from dashboard.webapp.views import *

urlpatterns = patterns('',
    #user profile urls
    url(r'login$', user_login),
    url(r'logout$', user_logout),
    url(r'saved_dashbaords$', user_saved_dashboards),
    url(r'dashboard_templates$', user_dashboard_templates),
    url(r'new_dashboard_from_template/(\w+)$', user_new_dashboard_from_template),

    #dashboard urls
    url(r'load/(\w+)$', dashboard),
    url(r'data_points/get_all$', dashboard_get_all_data_points),
    url(r'data_points/validate$', dashboard_validate_data_point),
    url(r'data_points/get_configured_name$', dashboard_get_configured_data_point_name),
    url(r'data_points/remove_data_point$', dashboard_remove_data_point),
    url(r'data_points/add_data_point$', dashboard_add_data_point),
    url(r'run_search$', dashboard_run_search),
    url(r'data_points/get_content_item_template/(\w+)/(\w+)', dashboard_get_content_item_template),
    url(r'save$', dashboard_save),
    url(r'ajax_bridge$', ajax_bridge),
)