from django.conf.urls.defaults import patterns, include, url
from dashboard.webapp.views import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^user/login$', user_login),
    url(r'^user/logout$', user_logout),
    url(r'^user/home$', user_home),

    url(r'dashboard/(\w+)$', dashboard),
    url(r'new_dashboard/(\w+)$', new_dashboard),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),

    url(r'^$', index),
)