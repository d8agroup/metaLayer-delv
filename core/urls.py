from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from core.views import home_page, core_javascript
from core.views import widget_picker_render
from core.views import widget_picker_javascript
from core.views import get_collection_config
from core.views import set_collection_config
from core.views import clear_collection_config
from core.views import login
from core.views import register 
from core.utils import run_widget_url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
          
    url(r'^inputs', include('inputwidget.urls')),
    
    url(r'feedback', include('feedbackandhelp.urls')),
    url(r'help', include('feedbackandhelp.urls')),
          
    url(r'^config/clear', clear_collection_config),             
    url(r'^config/get', get_collection_config),
    url(r'^config/set', set_collection_config),
    
    url(r'^widget/(\w+)/(\w+)/(\w+)', run_widget_url),
    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    
    url(r'^core/js$', core_javascript),
    url(r'^core/widgetpicker/render', widget_picker_render),
    url(r'^core/widgetpicker/script', widget_picker_javascript),
    
    url(r'^login', login),
    url(r'^register', register),
    
    
    url(r'^$', home_page),
                       
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),
    # url(r'^dashboard/', include('dashboard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
