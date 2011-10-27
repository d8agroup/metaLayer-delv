from visualwidgets.piechart.views import chart_source_type
from metalayerbridge.utils import get_sentiment_from_text
from metalayerbridge.utils import get_faces_from_image
from inputwidget.utils import run_all_inputs_and_combine_results
from inputwidget.utils import apply_actions
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

type ='facedetection' 
supported_types = ['flickrsearch']

def widget_data():
    return { 'type':type, 'display_name':'Face Detection' }

def generate_unconfigured_config():
    return {
        'id':md5('%s' % random.random()).hexdigest(),
        'type':'facedetection', 
        'display_name':'Face Detection',
        'config':{ 
            'configured':True
        }
    }
    
def run_action_for_content(request, collection_id, action_id, content):
    return_content = []
    n = 10
    for r in [content[i:i+n] for i in range(0, len(content), n)]:
        return_content = return_content + threaded_get_faces(r)
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
        'facedetection_configure.html',
        { 'action':[c for c in config['collections'][collection_id]['actions'] if c['id'] == id][0], 'collection_id':collection_id })

def save_config(request):
    collection_id = request.GET['collection_id']
    id = request.GET['id']
    action_config = {
        'id':id,
        'type':'facedetection', 
        'display_name':'Face Detection',
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

def chart_piechart_configuration():
    return {
        'name':'Pictures Containing Faces',
        'config':{
            'type':type,
            'module':'actionwidgets.facedetection.views',
            'function':'chart_piechart_withfaces',
            'elements':[]
        }
    } 

def chart_piechart_withfaces(request, collection_id, content, visual_id):
    config = get_config_ensuring_collection(request, collection_id)
    visual = [v for v in config['collections'][collection_id]['visuals'] if v['id'] == visual_id][0]
    
    if not visual['config']['configured']:
        return chart_source_type(request, collection_id, content, visual_id)
    
    url = '/widget/actionwidgets/facedetection/chart_piechart_withfaces_js?collection_id=%s&visual_id=%s' % (collection_id, visual_id)
    visual_data = {
        'id':visual_id,
        'type':visual['type'],
        'url':url,
        'display_name':'Pictures With Faces'
    }
    return render_to_response('chartwidget_base.html', { 'visual':visual_data, 'collection_id':collection_id })

def chart_piechart_withfaces_js(request):
    collection_id = request.GET['collection_id']
    visual_id = request.GET['visual_id']
    config = get_config_ensuring_collection(request, collection_id)
    inputs = config['collections'][collection_id]['inputs']
    actions = config['collections'][collection_id]['actions']
    content = run_all_inputs_and_combine_results(inputs)
    content = apply_actions(request, collection_id, content, actions)
    return_data = {}
    for item in content:
        if item['type'] not in supported_types:
            continue
        if 'has_faces' in item and item['has_faces']:
            type = 'With Faces'
        else:
            type = 'Without Faces'
        if type not in return_data:
            return_data[type] = 0;
        return_data[type] = return_data[type] + 1
    return_data = [[k,return_data[k]] for k in return_data.keys()]
    return render_to_response('render_piechart.js', { 'chart_data':return_data, 'id':visual_id })
 
def threaded_get_faces(content):
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
        try_count = 0
        worked = False
        while try_count < 3 and not worked:
            try:
                try_count = try_count + 1 
                has_faces = get_faces_from_image(self.item['image_url'].replace('_s.jpg', '_b.jpg'))
                worked = True
            except Exception, e:
                print e
                time.sleep(1)
        self.item['has_faces'] = has_faces if worked else False