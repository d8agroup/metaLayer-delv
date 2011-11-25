from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from core.utils import format_template_and_json_response
from core.utils import get_widget_data_by_widget_type
from core.utils import get_collection_config as utils_get_collection_config 
from core.utils import set_collection_config as utils_set_collection_config
from core.utils import JSONResponse
from core.models import RegisteredEmail
import re

def home_page(request):
    if 'email' not in request.session:
        return HttpResponseRedirect('/login')
    return render_to_response(
        'html/home.html',
        {
            'email': request.session['email'],
            'view_type': 'large-view' if 'large' in request.GET else None
        })

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

def login(request):
    if 'email' not in request.GET:
        return render_to_response('html/login.html')
    if not re.search(r'^[_.0-9a-z-]+@([0-9a-z][0-9a-z-]+.)+[a-z]{2,4}$', request.GET['email']):
        return render_to_response('html/login.html', { 'login_error':'Sorry, you did not enter a valid email address' })
    try:
        email = request.GET['email']
        user = RegisteredEmail.objects.get(email=email)
        if not user.approved:
            return render_to_response('html/login.html', { 'login_error':'Sorry, looks like you\'re not in the private beta. Join the waiting list below.' })
        request.session['email'] = user.id
        return HttpResponseRedirect('/')
    except:
        return render_to_response('html/login.html', { 'login_error':'Sorry, looks like you\'re not in the private beta. Join the waiting list below.' })

def register(request):
    if not re.search(r'^[_.0-9a-z-]+@([0-9a-z][0-9a-z-]+.)+[a-z]{2,4}$', request.GET['email']):
        return render_to_response('html/login.html', { 'register_error':'Sorry, you did not enter a valid email address' })
    email = request.GET['email']
    try:
        user = RegisteredEmail.objects.get(email=email)
        return render_to_response('html/login.html', { 'registered':True })
    except:
        user = RegisteredEmail()
        user.email = email
        user.save() 
        return render_to_response('html/login.html', { 'registered':True })
    
def logout(request):
    request.session.pop('email')
    return HttpResponseRedirect('/')
