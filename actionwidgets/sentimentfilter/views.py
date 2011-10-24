from metalayerbridge.utils import get_sentiment_from_text
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
    return { 'type':'sentimentfilter', 'display_name':'Sentiment' }

def generate_unconfigured_config():
    return {
        'id':md5('%s' % random.random()).hexdigest(),
        'type':'sentimentfilter', 
        'display_name':'Sentiment Analysis and Filter',
        'config':{ 
            'configured':True,
            'elements':[
                { 'name':'filter', 'value':'any' },
                { 'name':'include_neutral', 'value':'on' }
            ]
        }
    }
    
def run_action_for_content(request, collection_id, action_id, content):
    config = get_config_ensuring_collection(request, collection_id)
    config = [a for a in config['collections'][collection_id]['actions'] if a['id'] == action_id][0]
    
    if config['config']['elements'][0]['value'] == 'pp':
        sentiment_condition = [5, 2]
    elif config['config']['elements'][0]['value'] == 'p':
        sentiment_condition = [5, 0]
    elif config['config']['elements'][0]['value'] == 'n': 
        sentiment_condition = [-0.1, -5.1]
    elif config['config']['elements'][0]['value'] == 'nn': 
        sentiment_condition = [-2.1, -5.1]
    else:
        sentiment_condition = False
    
    include_neutral = True if config['config']['elements'][1]['value'] == 'on' else False

    all_content = []
    
    n = 10
    for r in [content[i:i+n] for i in range(0, len(content), n)]:
        all_content = all_content + threaded_get_sentiment(r)

    return_content = []
    
    for item in all_content:
        sentiment = item['sentiment']
        if not sentiment_condition:
            return_content.append(item)
            continue
        if sentiment == 0 and include_neutral:
            return_content.append(item)
            continue
        if sentiment <= sentiment_condition[0] and sentiment > sentiment_condition[1]:
            return_content.append(item)
            continue

    return return_content 
    
    
def clear_config(request):
    collection_id = request.GET['collection_id']
    id = request.GET['action_id']
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['actions'] = [a for a in config['collections'][collection_id]['actions'] if a['id'] != id]
    config['collections'][collection_id]['actions'].append(generate_unconfigured_config())
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
        'sentimentfilter_configure.html',
        { 'action':[c for c in config['collections'][collection_id]['actions'] if c['id'] == id][0], 'collection_id':collection_id })

def save_config(request):
    collection_id = request.GET['collection_id']
    id = request.GET['id']
    filter = request.GET['filter']
    include_neutral = request.GET['include_neutral'] if 'include_neutral' in request.GET else 'off' 
    if filter == 'pp':
        display_name = 'Sentiment Filter - Extremely Positive Only'
    elif filter == 'p':
        display_name = 'Sentiment Filter - Positive Only'
    elif filter == 'n':
        display_name = 'Sentiment Filter - Negative Only'
    elif filter == 'nn':
        display_name = 'Sentiment Filter - Extremely Negative Only'
    else:
        display_name = 'Sentiment'
    
    action_config = {
        'id':id,
        'type':'sentimentfilter', 
        'display_name':display_name,
        'config':{ 
            'configured':True,
            'elements':[
                { 'name':'filter', 'value':filter },
                { 'name':'include_neutral', 'value':include_neutral }
            ]
        }
    }
    
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['actions'] = [a for a in config['collections'][collection_id]['actions'] if a['id'] != id]
    config['collections'][collection_id]['actions'].append(action_config)
    set_collection_config(request, config)
    return HttpResponse()
 
 
def threaded_get_sentiment(content):
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
                sentiment = get_sentiment_from_text(self.item['title'] + self.item['text'])
                worked = True
            except:
                time.sleep(1)
        self.item['sentiment'] = sentiment if worked else 0