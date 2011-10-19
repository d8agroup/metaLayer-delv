from django.shortcuts import render_to_response
from django.utils import simplejson
from core.utils import JSONResponse
from core.utils import format_template_and_json_response
from core.utils import get_widget_config
from core.utils import save_widget_config
from core.utils import reconfigure_widget
import feedparser
import urllib2
import urllib

def widget_data():
    return {
        'id':'googlenews',
        'display_name':'Google News'}
    
def render(request):
    collection = request.GET['collection']
    widget_config  = get_widget_config(request, collection, 'inputwidgets', 'googlenews')
    context = { 'widget_data':widget_data(), 'widget_config':widget_config, 'collection':collection }
    
    if widget_config:
        try:
            context['articles'] = [{'title':a['title']} for a in feedparser.parse('http://news.google.com/news?hl=en&gl=us&q=%s&safe=on&output=rss' % widget_config['search']).items()[8][1]]
        except KeyError, e:
            context['widget_config'] = None

    return render_to_response('inputwidget_googlenews.html', context)
        
def render_js(request):
    collection = request.GET['collection']
    widget_config  = get_widget_config(request, collection, 'inputwidgets', 'googlenews')
    return render_to_response('inputwidget_googlenews.js')

def reconfigure(request):
    collection = request.GET['collection']
    reconfigure_widget(request, collection, 'inputwidgets', 'googlenews')
    return JSONResponse({'status':'success'})

def save_config(request):
    search = request.GET.get('search')
    if search == '':
        return JSONResponse({'status':'error'})
    config = simplejson.dumps({'search':search})
    collection = request.GET['collection']
    save_widget_config(request, collection, 'inputwidgets', 'googlenews', config)
    return JSONResponse({'status':'success'})

    