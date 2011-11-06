from inputwidget.utils import run_all_inputs_and_combine_results
from inputwidget.utils import apply_actions
from visualwidgets.piechart.views import chart_source_type
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response
from core.utils import get_config_ensuring_collection
from core.utils import set_collection_config
from core.models import CacheEntry
from hashlib import md5
from Queue import Queue
import urllib2
import threading
import random
import time

type ='klout' 
supported_types = ['twittersearch', 'twitteruser']

def widget_data():
    return { 'type':type, 'display_name':'Influence' }

def generate_unconfigured_config():
    return {
        'id':md5('%s' % random.random()).hexdigest(),
        'type':type, 
        'display_name':'Influence (Klout)',
        'config':{ 
            'configured':True
        }
    }
    
def run_action_for_content(request, collection_id, action_id, content):
    config = get_config_ensuring_collection(request, collection_id)
    klout_condition = config['collections'][collection_id]['search'][type] if type in config['collections'][collection_id]['search'] else 'all'

    config = [a for a in config['collections'][collection_id]['actions'] if a['id'] == action_id][0]
        
    all_content = []
    
    n = 2
    for r in [content[i:i+n] for i in range(0, len(content), n)]:
        all_content = all_content + threaded_get_klout(r)

    return_content = []
    
    for item in all_content:
        if klout_condition == 'all':
            return_content.append(item)
            continue
        if klout_condition == 'influential':
            if 'influence' in item and item['influence'] > 40: 
                return_content.append(item)
                continue

    return return_content 
    
    
def clear_config(request):
    collection_id = request.GET['collection_id']
    id = request.GET['action_id']
    config = get_config_ensuring_collection(request, collection_id)
    this_config = [a for a in config['collections'][collection_id]['actions'] if a['id'] == id][0]
    this_config['config']['configured'] = False
    config['collections'][collection_id]['actions'] = [a for a in config['collections'][collection_id]['actions'] if a['id'] != id]
    config['collections'][collection_id]['actions'].append(this_config)
    set_collection_config(request, config)
    return HttpResponse()
    
def add_new(request):
    collection_id = request.GET['collection_id']
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['actions'].append(generate_unconfigured_config())
    set_collection_config(request, config)
    return HttpResponse()

def remove(request):
    collection_id = request.GET['collection_id']
    id = request.GET['action_id']
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['actions'] = [a for a in config['collections'][collection_id]['actions'] if a['id'] != id]
    set_collection_config(request, config)
    return HttpResponse()
 
def chart_piechart_configuration():
    return {
        'name':'Influential Contributors',
        'config':{
            'type':type,
            'module':'actionwidgets.klout.views',
            'function':'chart_piechart_influence',
            'elements':[]
        }
    } 

def chart_piechart_influence(request, collection_id, content, visual_id):
    config = get_config_ensuring_collection(request, collection_id)
    visual = [v for v in config['collections'][collection_id]['visuals'] if v['id'] == visual_id][0]
    
    if not visual['config']['configured']:
        return chart_source_type(request, collection_id, content, visual_id)
    
    url = '/widget/actionwidgets/klout/chart_piechart_influence_js?collection_id=%s&visual_id=%s' % (collection_id, visual_id)
    visual_data = {
        'id':visual_id,
        'type':visual['type'],
        'url':url,
        'display_name':'Influential Contributors'
    }
    return render_to_response('chartwidget_base.html', { 'visual':visual_data, 'collection_id':collection_id })

def chart_piechart_influence_js(request):
    collection_id = request.GET['collection_id']
    visual_id = request.GET['visual_id']
    config = get_config_ensuring_collection(request, collection_id)
    inputs = config['collections'][collection_id]['inputs']
    actions = config['collections'][collection_id]['actions']
    content = run_all_inputs_and_combine_results(inputs)
    content = apply_actions(request, collection_id, content, actions)
    return_data = {}
    for item in content:
        if 'influence' in item and item['influence'] > 40:
            type = 'high influence'
        elif 'influence' in item:
            type = 'low influence'
        else:
            type = 'no influence'
        if type not in return_data:
            return_data[type] = 0;
        return_data[type] = return_data[type] + 1
    return_data = [[k,return_data[k]] for k in return_data.keys()]
    return render_to_response('render_piechart.js', { 'chart_data':return_data, 'id':visual_id })

 
def threaded_get_klout(content):
    def producer(q, _items):
        for _item in _items:
            thread = ServiceRunner(_item)
            thread.start()
            q.put(thread, True)
 
    finished = []
    
    def consumer(q, total_items):
        while len(finished) < total_items:
            thread = q.get(True)
            thread.join()
            finished.append(thread.get_result())
 
    q = Queue()
    prod_thread = threading.Thread(target=producer, args=(q, content))
    cons_thread = threading.Thread(target=consumer, args=(q, len(content)))
    prod_thread.start()
    cons_thread.start()
    prod_thread.join()
    cons_thread.join()    

    all_content = []
    
    for result in finished:
        all_content.append(result) 
    return all_content

class ServiceRunner(threading.Thread):
    def __init__(self, item):
        self.item = item
        threading.Thread.__init__(self)
    
    def get_result(self):
        return self.item
    
    def run(self):
        if self.item['type'] not in supported_types:
            return
        
        cache_key = 'klout_%s' % self.item['author']
        try:
            cache_entry = CacheEntry.objects.get(key=cache_key)
            if int(time.time()) - cache_entry.time > 86400: # cache for 24 hours
                cache_entry.delete()
                raise CacheEntry.DoesNotExist
            klout = cache_entry.cache
        except CacheEntry.DoesNotExist:
            try_count = 0
            got_result = False
            while not got_result and try_count < 3:
                try_count = try_count + 1
                try:
                    raw_json = urllib2.urlopen('http://api.klout.com/1/klout.json?users=%s&key=mer6tdvh3fex4tkww39k8wte' % self.item['author']).read()
                    got_result = True
                except Exception, e:
                    time.sleep(1)
                    
            if not got_result:
                return
            
            #Try to get from cache one more time - race condition
            try:
                cache_entry = CacheEntry.objects.get(key=cache_key)
                return cache_entry.cache
            except CacheEntry.DoesNotExist:
                pass
            
	    try:
            	klout = simplejson.loads(raw_json)['users'][0]['kscore']
	    except:
		return

            cache_entry = CacheEntry()
            cache_entry.cache =  klout
            cache_entry.key = cache_key
            cache_entry.time = int(time.time())
            cache_entry.save()
            
        self.item['influence'] = float(klout)
