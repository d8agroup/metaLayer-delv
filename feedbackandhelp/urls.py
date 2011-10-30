from django.conf.urls.defaults import patterns, include, url
from feedbackandhelp.views import give_feedback 

urlpatterns = patterns('',
    url(r'/givefeedback', give_feedback),
)