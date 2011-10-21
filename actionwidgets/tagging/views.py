from metalayerbridge.utils import get_sentiment_from_text
from metalayerbridge.utils import get_tags_from_text
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response
from core.utils import get_config_ensuring_collection
from core.utils import set_collection_config
from hashlib import md5
import random

def widget_data():
    return { 'type':'tagging', 'display_name':'Tagging' }

def generate_unconfigured_config():
    return {
        'id':md5('%s' % random.random()).hexdigest(),
        'type':'tagging', 
        'display_name':'Tagging and Taxonomy',
        'config':{ 
            'configured':False,
            'elements':[]
        }
    }
    
def run_action_for_content(request, collection_id, action_id, content):
    return_content = []
    for item in content:
        tags = get_tags_from_text(item['title'] + item['text'])
        item['tags'] = tags
        return_content.append(item)
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
 
