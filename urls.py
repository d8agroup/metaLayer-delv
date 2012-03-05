from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to
from django.conf import settings
from thecommunity.views import xd_receiver

if settings.SITE_DOWN:
    from thecommunity.views import site_down
    urlpatterns = patterns('',
        url(r'', site_down),
    )
else:
    urlpatterns = patterns('',
        url(r'^delv/', include('dashboard.thecommunity.urls')),
        url(r'^user/', include('dashboard.thedashboard.urls')),
        url(r'^dashboard/', include('dashboard.thedashboard.urls')),

        url(r'^system/aggregator/', include('dashboard.metalayercore.aggregator.urls')),

        url(r'^o/', include('dashboard.metalayercore.outputs.urls')),
        url(r'^i/', include('dashboard.imaging.urls')),
        url(r'^d/', include('dashboard.metalayercore.dashboards.urls')),

        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),

        url(r'^xd_receiver\.html$', xd_receiver),

        url(r'^community/', redirect_to, {'url':'/delv/'} ),
        url(r'^$', redirect_to, {'url':'/delv/'} ),
    )