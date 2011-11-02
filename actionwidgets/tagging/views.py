from inputwidget.utils import run_all_inputs_and_combine_results
from inputwidget.utils import apply_actions
from metalayerbridge.utils import get_sentiment_from_text
from metalayerbridge.utils import get_tags_from_text
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response
from core.utils import get_config_ensuring_collection
from core.utils import set_collection_config
from hashlib import md5
from Queue import Queue
import threading
import random
import time

type = 'tagging'

def widget_data():
    return { 'type':type, 'display_name':'Tagging' }

def generate_unconfigured_config():
    return {
        'id':md5('%s' % random.random()).hexdigest(),
        'type':type, 
        'display_name':'Tagging and Taxonomy',
        'config':{ 
            'configured':True
        }
    }
    
def run_action_for_content(request, collection_id, action_id, content):
    return_content = []
    n = 10
    for r in [content[i:i+n] for i in range(0, len(content), n)]:
        return_content = return_content + threaded_get_tags(r)
        
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

def render_config(request):
    collection_id = request.GET['collection_id']
    id = request.GET['id']
    config = get_config_ensuring_collection(request, collection_id)
    return render_to_response(
        'tagging_configure.html',
        { 'action':[c for c in config['collections'][collection_id]['actions'] if c['id'] == id][0], 'collection_id':collection_id })

def save_config(request):
    collection_id = request.GET['collection_id']
    id = request.GET['id']
    action_config = {
        'id':id,
        'type':'tagging', 
        'display_name':'Tagging and Taxonomy',
        'config':{ 
            'configured':True,
            'elements':[]
        }
    }    
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['actions'] = [a for a in config['collections'][collection_id]['actions'] if a['id'] != id]
    config['collections'][collection_id]['actions'].append(action_config)
    set_collection_config(request, config)
    return HttpResponse()
 
def chart_barchart_configuration():
    return {
        'name':'Popular Tags',
        'config':{
            'type':type,
            'module':'actionwidgets.tagging.views',
            'function':'chart_barchart_tags',
            'elements':[]
        }
    } 

def chart_barchart_tags(request, collection_id, content, visual_id):
    config = get_config_ensuring_collection(request, collection_id)
    visual = [v for v in config['collections'][collection_id]['visuals'] if v['id'] == visual_id][0]
    
    if not visual['config']['configured']:
        return chart_source_type(request, collection_id, content, visual_id)
    
    url = '/widget/actionwidgets/tagging/chart_barchart_tags_js?collection_id=%s&visual_id=%s' % (collection_id, visual_id)
    visual_data = {
        'id':visual_id,
        'type':visual['type'],
        'url':url,
        'display_name':'Popular Tags'
    }
    return render_to_response('chartwidget_base.html', { 'visual':visual_data, 'collection_id':collection_id })

def chart_barchart_tags_js(request):
    collection_id = request.GET['collection_id']
    visual_id = request.GET['visual_id']
    config = get_config_ensuring_collection(request, collection_id)
    inputs = config['collections'][collection_id]['inputs']
    actions = config['collections'][collection_id]['actions']
    content = run_all_inputs_and_combine_results(inputs)
    content = apply_actions(request, collection_id, content, actions)
    return_data = {}
    
    for item in content:
        if not 'tags' in item:
            continue
        for tag in item['tags']:
            tag = str(tag.lower())
            if tag not in return_data:
                return_data[tag] = 0;
        return_data[tag] = return_data[tag] + 1
    for key in return_data.keys():
        if return_data[key] == 0:
            return_data.pop(key)
    return_data = [(x, return_data[x]) for x in return_data.keys()]
    return_data = sorted(return_data, key=lambda x: -1 * x[1])[0:3]
    values = [x[1] for x in return_data]
    names = [x[0] for x in return_data]
    return render_to_response('render_barchart.js', { 'values':values, 'names':names, 'id':visual_id })
 
def threaded_get_tags(content):
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
        try_count = 0
        worked = False
        while try_count < 3 and not worked:
            try:
                try_count = try_count + 1 
                tags = get_tags_from_text(self.item['title'] + self.item['text'])
                worked = True
            except:
                time.sleep(1)
        self.item['tags'] = tags if worked else []