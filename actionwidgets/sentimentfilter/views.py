from metalayerbridge.utils import get_sentiment_from_text
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response
from core.utils import get_config_ensuring_collection
from core.utils import set_collection_config
from hashlib import md5
import random

def widget_data():
    return { 'type':'sentimentfilter', 'display_name':'Sentiment' }

def generate_unconfigured_config():
    return {
        'id':md5('%s' % random.random()).hexdigest(),
        'type':'sentimentfilter', 
        'display_name':'Sentiment Analysis and Filter',
        'config':{ 
            'configured':False,
            'elements':[
                { 'name':'filter' },
                { 'name':'include_neutral' }
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
    
    return_content = []
    for item in content:
        sentiment = get_sentiment_from_text(item['title'] + item['text'])
        item['sentiment'] = sentiment
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
 
