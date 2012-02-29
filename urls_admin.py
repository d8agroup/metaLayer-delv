from django.conf.urls.defaults import  include, url, patterns
from django.contrib import admin
from urls import urlpatterns

admin.autodiscover()

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^emails/', include('dashboard.emails.urls')),
)