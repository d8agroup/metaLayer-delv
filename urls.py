from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.contrib import admin
from django.conf import settings
from thecommunity.views import xd_receiver

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^community/', include('dashboard.thecommunity.urls')),
    url(r'^user/', include('dashboard.thedashboard.urls')),
    url(r'^dashboard/', include('dashboard.thedashboard.urls')),

    url(r'^system/aggregator/', include('dashboard.aggregator.urls')),

    url(r'^o/', include('dashboard.outputs.urls')),
    url(r'^i/', include('dashboard.imaging.urls')),
    url(r'^d/', include('dashboard.dashboards.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),

    url(r'^xd_receiver\.html$', xd_receiver),

    url(r'^$', redirect_to, {'url':'/community/'} ),
)