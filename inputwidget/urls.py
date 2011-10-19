from django.conf.urls.defaults import patterns, include, url
from inputwidget.views import render_input_widget
from inputwidget.views import add_new_input
from inputwidget.views import configure_input
from inputwidget.views import render_js
from inputwidget.views import clear_configuration_for_input
from inputwidget.views import remove_input 

urlpatterns = patterns('',
    url(r'/js', render_js),
    url(r'/add', add_new_input),
    url(r'/remove', remove_input),
    url(r'/configure', configure_input),
    url(r'/clearconfig', clear_configuration_for_input),
    url(r'/render', render_input_widget),             
)