from inputwidget.utils import run_all_inputs_and_combine_results
from inputwidget.utils import apply_actions
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from core.utils import get_config_ensuring_collection
from core.utils import set_collection_config
from core.utils import my_import
import inputs.sources as sources
from hashlib import md5
import urllib
import random
import re

type = 'barchart'

def widget_data():
    return { 'type':type, 'display_name':'Bar Chart' }

def generate_unconfigured_config(config, collection_id):
    return_data = {
        'id':urllib.quote(md5('%s' % random.random()).hexdigest()),
        'type':type, 
        'display_name':'Bar Chart',
        'config':{
            'configured':True,
            'active_chart_type':'Source Type',
            'chart_types':{
                'Source Type':{
                    'type':'native',
                    'module':'visualwidgets.barchart.views',
                    'function':'chart_source_type',
                    'elements':[]
                }
            }
        }
    }
    
    for views in [my_import('%s.views' % name) for name in settings.INSTALLED_APPS if re.search(r'actionwidgets\.', name)]:
        try:
            function = getattr(views, 'chart_barchart_configuration')
            additional_config = function()
            return_data['config']['chart_types'][additional_config['name']] = additional_config['config']
        except:
            pass
        
    #if there is more than one type then show the config first
    for t in return_data['config']['chart_types'].values():
        if t['type'] in [a['type'] for a in config['collections'][collection_id]['actions']]:
            return_data['config']['configured'] = False
    
    return return_data

def configure(request):
    collection_id = request.GET['collection_id']
    id = request.GET['visual_id']
    type = request.GET['type']
    config = get_config_ensuring_collection(request, collection_id)
    visuals = config['collections'][collection_id]['visuals']
    config['collections'][collection_id]['visuals'] = []
    for v in visuals:
        if v['id'] == id:
            v['config']['configured'] = True
            v['config']['active_chart_type'] = type 
        config['collections'][collection_id]['visuals'].append(v)
    set_collection_config(request, config)
    return HttpResponse()

    
def add_new(request):
    collection_id = request.GET['collection_id']
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['visuals'].append(generate_unconfigured_config(config, collection_id))
    set_collection_config(request, config)
    return HttpResponse()

def clear_config(request):
    collection_id = request.GET['collection_id']
    id = request.GET['visual_id']
    config = get_config_ensuring_collection(request, collection_id)
    visuals = config['collections'][collection_id]['visuals']
    config['collections'][collection_id]['visuals'] = []
    for v in visuals:
        if v['id'] == id:
            v['config']['configured'] = False
        config['collections'][collection_id]['visuals'].append(v)
    set_collection_config(request, config)
    return HttpResponse()

def remove(request):
    collection_id = request.GET['collection_id']
    id = request.GET['visual_id']
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['visuals'] = [a for a in config['collections'][collection_id]['visuals'] if a['id'] != id]
    set_collection_config(request, config)
    return HttpResponse()

def chart_source_type(request, collection_id, content, visual_id):
    config = get_config_ensuring_collection(request, collection_id)
    visual = [v for v in config['collections'][collection_id]['visuals'] if v['id'] == visual_id][0]
    
    if visual['config']['configured']:
        url = '/widget/visualwidgets/barchart/chart_source_type_js?collection_id=%s&visual_id=%s' % (collection_id, visual_id)
        visual_data = {
            'id':visual_id,
            'type':visual['type'],
            'url':url,
            'display_name':visual['config']['active_chart_type']
        }
        return render_to_response('chartwidget_base.html', { 'visual':visual_data, 'collection_id':collection_id })
    else:
        chart_types = visual['config']['chart_types']
        visual['config']['chart_types'] = {}
        for type in chart_types:
            if chart_types[type]['type'] == 'native' or [a for a in config['collections'][collection_id]['actions'] if a['type'] == chart_types[type]['type']]:
                visual['config']['chart_types'][type] = chart_types[type]
        return render_to_response('barchart_configure.html', { 'visual':visual, 'collection_id':collection_id })    
    
def chart_source_type_js(request):
    collection_id = request.GET['collection_id']
    visual_id = request.GET['visual_id']
    config = get_config_ensuring_collection(request, collection_id)
    inputs = config['collections'][collection_id]['inputs']
    actions = config['collections'][collection_id]['actions']
    content = run_all_inputs_and_combine_results(inputs)
    content = apply_actions(request, collection_id, content, actions)
    
    return_data = {}
    for item in content:
        type = item['type']
        if type not in return_data:
            return_data[type] = 0;
        return_data[type] = return_data[type] + 1
    #return_data = [[k,return_data[k]] for k in return_data.keys()]
    #return_data = sorted(return_data, key=lambda x: x[1])[0:5]
    return render_to_response('render_barchart.js', { 'values':return_data.values(), 'names':return_data.keys(), 'id':visual_id })
