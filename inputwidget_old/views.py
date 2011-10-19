from django.shortcuts import render_to_response
from core.utils import get_collection_config

def render_input_widget(request):
    return render_to_response('inputwidget.html')

def render_input_widget_input_summary(request):
    return render_to_response(
        'inputwidget_input.html',
        {
            'collection_id':request.GET['collection_id'],
            'input_id':request.GET['input_id'],
            'title':request.GET['title'],
            'type':request.GET['type']
        })
    
    