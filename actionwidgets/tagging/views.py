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

def widget_data():
    return { 'type':'tagging', 'display_name':'Tagging' }

def generate_unconfigured_config():
    return {
        'id':md5('%s' % random.random()).hexdigest(),
        'type':'tagging', 
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