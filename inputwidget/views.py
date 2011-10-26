from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from core.utils import set_collection_config
from core.utils import JSONResponse
from core.utils import get_config_ensuring_collection
from inputwidget.utils import run_all_inputs_and_combine_results
from inputwidget.utils import apply_actions
from inputwidget.utils import apply_visuals
import inputs.sources as sources

def render_js(request):
    return render_to_response('js/inputwidget.js')

def add_new_input(request):
    collection_id = request.GET['collection_id']
    type = request.GET['type']
    source_bridge = getattr(sources, type)()
    input_config = source_bridge.generate_unconfigured_config()
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['inputs'].append(input_config)
    set_collection_config(request, config)
    return HttpResponse()

def remove_input(request):
    input_id = request.GET['input_id']
    collection_id = request.GET['collection_id']
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['inputs'] = [input for input in config['collections'][collection_id]['inputs'] if input['id'] != input_id]
    set_collection_config(request, config)
    return_data = { 'was_last_input':False } if len(config['collections'][collection_id]['inputs']) else { 'was_last_input':True }
    return JSONResponse(return_data)

def configure_input(request):
    type = request.GET['type']
    input_id = request.GET['id']
    collection_id = request.GET['collection_id']
    source_bridge = getattr(sources, type)()
    input_config = source_bridge.parse_request_to_config(request)
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['inputs'] = [input for input in config['collections'][collection_id]['inputs'] if input['id'] != input_id]
    config['collections'][collection_id]['inputs'].append(input_config)
    set_collection_config(request, config)
    return HttpResponse()

def clear_configuration_for_input(request):
    input_id = request.GET['input_id']
    input_type = request.GET['input_type']
    collection_id = request.GET['collection_id']
    source_bridge = getattr(sources, input_type)()
    input_config = source_bridge.generate_unconfigured_config()
    config = get_config_ensuring_collection(request, collection_id)
    for input in config['collections'][collection_id]['inputs']:
        if input['id'] == input_id:
            input['config']['configured'] = False
    set_collection_config(request, config)
    return HttpResponse()
    
def render_input_widget(request):
    collection_id = request.GET['collection_id']
    config = get_config_ensuring_collection(request, collection_id)
    un_configured_inputs = [input for input in config['collections'][collection_id]['inputs'] if input['config']['configured'] == False]
    if un_configured_inputs:
        return render_to_response('html/inputwidget_configure.html', { 'input':un_configured_inputs[0], 'collection_id':collection_id })
    un_configured_actions = [action for action in config['collections'][collection_id]['actions'] if action['config']['configured'] == False]
    if un_configured_actions:
        return HttpResponseRedirect('/widget/actionwidgets/%s/render_config?collection_id=%s&id=%s' % (un_configured_actions[0]['type'], collection_id, un_configured_actions[0]['id']))
    inputs = config['collections'][collection_id]['inputs']
    actions = config['collections'][collection_id]['actions']
    visuals = config['collections'][collection_id]['visuals']
    content = run_all_inputs_and_combine_results(inputs)
    content = apply_actions(request, collection_id, content, actions)
    visuals = apply_visuals(request, collection_id, content, visuals) 
    return render_to_response(
        'html/inputwidget_display.html',
        {
            'inputs': inputs,
            'actions':actions,
            'content':content,
            'visuals':visuals,
            'collection_id':collection_id 
        })

def move_input_widget(request):
    new_collection_id = request.GET['new_collection_id']
    old_collection_id = request.GET['old_collection_id']
    config = get_config_ensuring_collection(request, new_collection_id)
    for type in ['inputs', 'actions', 'visuals']:
        config['collections'][new_collection_id][type] = config['collections'][new_collection_id][type] + [i for i in config['collections'][old_collection_id][type]]
        config['collections'][old_collection_id][type] = []
    set_collection_config(request, config)
    return HttpResponse()
    