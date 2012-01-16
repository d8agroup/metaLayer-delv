from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotAllowed
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from django.conf import settings
from datapoints.controllers import DataPointController
from logger import Logger
from search.controllers import SearchController
from userprofiles.controllers import UserController
from dashboards.controllers import DashboardsController
from utils import JSONResponse
from urllib2 import urlopen

def index(request):
    if not request.user.is_authenticated():
        if not request.method == 'POST':
            return render_to_response('login_or_register.html', context_instance=RequestContext(request))
        else:
            if 'login' in request.POST:
                username = request.POST.get('login_username')
                password = request.POST.get('login_password')
                passed, errors = UserController.LoginUser(request, username, password)
                if not passed:
                    return render_to_response(
                        'login_or_register.html',
                        { 'login_errors':errors },
                        context_instance=RequestContext(request)
                    )
            elif 'register' in request.POST:
                username = request.POST.get('register_username')
                password1 = request.POST.get('register_password1')
                password2 = request.POST.get('register_password2')
                passed, errors = UserController.RegisterUser(request, username, password1, password2)
                if not passed:
                    return render_to_response(
                        'login_or_register.html',
                        { 'register_errors':errors },
                        context_instance=RequestContext(request)
                    )
    return render_to_response('site.html',context_instance=RequestContext(request))

def ajax_bridge(request):
    request_url = request.POST['request_url']
    try:
        response = urlopen(request_url).read()
        return HttpResponse(response)
    except Exception, e:
        Logger.Error('%s - ajax_bridge - error: %s' % (__name__, e))
        return HttpResponseServerError()

@login_required(login_url='/')
def dashboard(request, id):
    dc = DashboardsController(request.user)
    db = dc.get_dashboard_by_id(id)
    return JSONResponse({'dashboard':db})

@login_required(login_url='/')
def dashboard_get_all_data_points(request):
    #TODO: Need to get the options from the request.user and pass them to the controller
    data_points = DataPointController.GetAllForTemplateOptions(None)
    return JSONResponse({'data_points':data_points})

@login_required(login_url='/')
def dashboard_validate_data_point(request):
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    passed, errors = dpc.is_valid();
    return JSONResponse({'passed':passed, 'errors':errors})

@login_required(login_url='/')
def dashboard_get_configured_data_point_name(request):
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    configured_display_name = dpc.get_configured_display_name()
    return JSONResponse({'configured_display_name':configured_display_name})

@login_required(login_url='/')
def dashboard_remove_data_point(request):
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    dpc.data_point_removed()
    return JSONResponse()

@login_required(login_url='/')
def dashboard_add_data_point(request):
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    dpc.data_point_added()
    return JSONResponse()

@login_required(login_url='/')
def dashboard_run_search(request):
    configuration = {
        'data_points':json.loads(request.POST['data_points']),
        'search_filters':json.loads(request.POST['search_filters'])
    }
    sc = SearchController(configuration)
    search_results = sc.run_search_and_return_results()
    return JSONResponse({'search_results':search_results})

@login_required(login_url='/')
def dashboard_get_content_item_template(request, type, sub_type):
    data_point = { 'type':type, 'sub_type':sub_type }
    dpc = DataPointController(data_point)
    template = dpc.get_content_item_template()
    return JSONResponse({'template':template, 'type':type, 'sub_type':sub_type})

@login_required(login_url='/')
def dashboard_save(request):
    dashboard = json.loads(request.POST['dashboard'])
    user = request.user
    dbc = DashboardsController(user)
    dbc.update_dashboard(dashboard)
    return JSONResponse()

########################################################################################################################
# USER ACCOUNT FUNCTIONS
########################################################################################################################
@login_required(login_url='/')
def user_saved_dashboards(request):
    dc = DashboardsController(request.user)
    saved_dashboards = dc.get_saved_dashboards()
    return render_to_response('parts/user_saved_dashboards.html', { 'saved_dashboards':saved_dashboards, })

@login_required(login_url='/')
def user_dashboard_templates(request):
    dc = DashboardsController(request.user)
    dashboard_templates = dc.get_dashboard_templates()
    return render_to_response('parts/user_dashboard_templates.html', { 'dashboard_templates':dashboard_templates, })

@login_required(login_url='/')
def current_subscription(request):
    user = request.user
    uc = UserController(user)
    user_subscriptions = uc.get_user_subscriptions()
    current_active_subscription_name = user_subscriptions['active_subscription']
    current_active_subscription = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][current_active_subscription_name]
    return render_to_response(
        'parts/user_current_subscription.html',
        { 'subscription':current_active_subscription }
    )

@login_required(login_url='/')
def change_subscription(request):
    user = request.user
    uc = UserController(user)
    user_subscriptions = uc.get_user_subscriptions()
    current_active_subscription_name = user_subscriptions['active_subscription']
    available_subscriptions = [settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][sub] for sub in settings.SUBSCRIPTIONS_SETTINGS['subscriptions'].keys() if sub != current_active_subscription_name]
    return render_to_response(
        'parts/user_list_available_subscriptions.html',
        { 'subscriptions':available_subscriptions }
    )

@login_required(login_url='/')
def user_logout(request):
    uc = UserController(request.user)
    uc.logout_user(request)
    return redirect('/')

@login_required(login_url='/')
def user_new_dashboard_from_template(request, dashboard_template_id):
    uc = UserController(request.user)
    uc.register_dashboard_template_use(dashboard_template_id)
    dc = DashboardsController(request.user)
    db = dc.create_new_dashboard_from_template(dashboard_template_id)
    return JSONResponse({'dashboard_id':db['id']})