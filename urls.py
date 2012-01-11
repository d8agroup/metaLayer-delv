from django.conf.urls.defaults import patterns, include, url
from dashboard.webapp.views import index
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^user/', include('dashboard.webapp.urls')),
    url(r'^dashboard/', include('dashboard.webapp.urls')),

    url(r'^aggregator/', include('dashboard.aggregator.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),

    url(r'^$', index),
)