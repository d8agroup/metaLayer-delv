import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

from views import category_page
from django.http import HttpRequest, HttpResponseRedirect

request = HttpRequest()

def setup():
    pass

def test_category_page_bogus_category():
    
    response = category_page(request, "bogus category")
    
    assert isinstance(response, HttpResponseRedirect), "category page did not redirect"