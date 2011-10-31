from django.core.mail import EmailMultiAlternatives
from inputwidget.utils import run_all_inputs_and_combine_results
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from inputwidget.utils import apply_actions
from django.shortcuts import render_to_response
from django.http import HttpResponse
from core.utils import get_config_ensuring_collection
from core.utils import set_collection_config
from hashlib import md5
import datetime
import random
import xlwt

type = 'embed'

def widget_data():
    return { 'type':type, 'display_name':'Embed' }

def generate_unconfigured_config():
    return {
        'id':md5('%s' % random.random()).hexdigest(),
        'type':type, 
        'display_name':'Embed',
        'config':{
            'configured':True,
            'elements':[]
        }
    }
    
def add_new(request):
    collection_id = request.GET['collection_id']
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['outputs'].append(generate_unconfigured_config())
    set_collection_config(request, config)
    return HttpResponse()

def remove(request):
    collection_id = request.GET['collection_id']
    id = request.GET['output_id']
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['outputs'] = [a for a in config['collections'][collection_id]['outputs'] if a['id'] != id]
    set_collection_config(request, config)
    return HttpResponse()

def render(collection_id, output_id):
    config = generate_unconfigured_config()
    config['id'] = output_id
    return render_to_response('embed_basic.html', { 'output':config, 'collection_id':collection_id })