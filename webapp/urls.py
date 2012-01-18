from django.conf.urls.defaults import patterns, url
from dashboard.webapp.views import *

urlpatterns = patterns('',
    #user profile urls
    url(r'logout$', user_logout),
    url(r'current_subscription', current_subscription),
    url(r'change_subscription', change_subscription),
    url(r'dashboard_management/saved_dashboards', user_saved_dashboards),
    url(r'dashboard_management/delete_dashboard', user_delete_dashboard),
    url(r'dashboard_management/new_dashboard_from_template/(\w+)$', user_new_dashboard_from_template),
    url(r'dashboard_management/get_dashboard_templates$', user_dashboard_templates),

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