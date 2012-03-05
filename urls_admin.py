from django.conf import settings
from django.conf.urls.defaults import  include, url, patterns
from django.contrib import admin
from urls import urlpatterns

#admin.autodiscover()

urlpatterns += patterns('',
    url(r'%s/' % settings.CUSTOM_ADMIN_ROOT, include('dashboard.administration.urls')),
#    url(r'^admin/', include(admin.site.urls)),
    url(r'^emails/', include('dashboard.emails.urls')),
)