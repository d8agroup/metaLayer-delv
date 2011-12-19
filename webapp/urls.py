from django.conf.urls.defaults import patterns, include, url
from dashboard.webapp.views import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^user/login$', user_login),
    url(r'^user/logout$', user_logout),
    url(r'^user/saved_dashbaords$', user_saved_dashboards),
    url(r'^user/dashboard_templates$', user_dashboard_templates),
    url(r'^user/new_dashboard_from_template/(\w+)$', user_new_dashboard_from_template),

    url(r'dashboard/load/(\w+)$', dashboard),
    url(r'dashboard/data_points/get_all$', dashboard_get_all_data_points),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),

    url(r'^$', index),
)