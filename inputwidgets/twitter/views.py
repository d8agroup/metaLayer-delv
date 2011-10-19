from django.shortcuts import render_to_response
from django.utils import simplejson
from core.utils import JSONResponse
from core.utils import format_template_and_json_response
from core.utils import get_widget_config
from core.utils import save_widget_config
from core.utils import reconfigure_widget
import urllib2
import urllib

def widget_data():
    return {
        'id':'twitter',
        'display_name':'Twitter'}
    
def render(request):
    collection = request.GET['collection']
    widget_config  = get_widget_config(request, collection, 'inputwidgets', 'twitter')
    context = { 'widget_data':widget_data(), 'widget_config':widget_config, 'collection':collection }
    
    if widget_config:
        try:
            if widget_config['type'] == 'search':
                hashtag = urllib.quote(widget_config['hashtag'])
                context['tweets'] = simplejson.loads(urllib2.urlopen('http://search.twitter.com/search.json?q=%s' % hashtag).read())
            elif widget_config['type'] == 'follow':
                user_name = urllib.quote(widget_config['user_name'])
                context['tweets'] = simplejson.loads(urllib2.urlopen('http://search.twitter.com/search.json?q=from:%s' % user_name).read())
        except KeyError, e:
            context['widget_config'] = None

    return render_to_response('inputwidget_twitter.html', context)
        
def render_js(request):
    collection = request.GET['collection']
    widget_config  = get_widget_config(request, collection, 'inputwidgets', 'twitter')
    return render_to_response('inputwidget_twitter.js')

def reconfigure(request):
    collection = request.GET['collection']
    reconfigure_widget(request, collection, 'inputwidgets', 'twitter')
    return JSONResponse({'status':'success'})

def save_config(request):
    if 'hashtag' in request.GET:
        hashtag = request.GET.get('hashtag')
        if hashtag == '':
            return JSONResponse({'status':'error'})
        config = simplejson.dumps({'type':'search', 'hashtag':hashtag})
    else:
        user_name = request.GET.get('user_name')
        if user_name == '':
            return JSONResponse({'status':'error'})
        config = simplejson.dumps({'type':'follow', 'user_name':user_name})
    collection = request.GET['collection']
    save_widget_config(request, collection, 'inputwidgets', 'twitter', config)
    return JSONResponse({'status':'success'})

    