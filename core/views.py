from django.shortcuts import render_to_response
from core.utils import format_template_and_json_response
from core.utils import get_widget_data_by_widget_type
from core.utils import get_collection_config as utils_get_collection_config 
from core.utils import set_collection_config as utils_set_collection_config
from core.utils import JSONResponse

def home_page(request):
    return render_to_response('html/home.html')

def core_javascript(request):
    return render_to_response('js/core.js')

def widget_picker_render(request):
    return format_template_and_json_response(
        'html/widgetpicker.html',
        {
            'input_widgets':get_widget_data_by_widget_type('inputwidgets'),
            'action_widgets':get_widget_data_by_widget_type('actionwidgets'),
            'visual_widgets':get_widget_data_by_widget_type('visualwidgets'),
            'output_widgets':get_widget_data_by_widget_type('outputwidgets'),
        },
        {})

def widget_picker_javascript(request):
    return render_to_response('js/widgetpicker.js')

def get_collection_config(request):
    return JSONResponse(utils_get_collection_config(request))

def set_collection_config(request):
    utils_set_collection_config(request, request.GET['config'])
    return JSONResponse()

def clear_collection_config(request):
    utils_set_collection_config(request, {"collections":{}})
    return JSONResponse()