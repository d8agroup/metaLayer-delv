from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from datapoints.controllers import DataPointController
from search.controllers import SearchController
from userprofiles.controllers import UserController
from dashboards.controllers import DashboardsController
from webapp.utils import JSONResponse

def index(request):
    if request.user.is_authenticated():
        return render_to_response('site.html',{}, context_instance=RequestContext(request))
    data_dict = {}
    return render_to_response(
        'index.html',
        data_dict,
        context_instance=RequestContext(request)
    )

@login_required(login_url='/user/login')
def dashboard(request, id):
    dc = DashboardsController(request.user)
    db = dc.get_dashboard_by_id(id)
    return JSONResponse({'dashboard':db})

@login_required(login_url='/user/login')
def dashboard_get_all_data_points(request):
    #TODO: Need to get the options from the request.user and pass them to the controller
    data_points = DataPointController.GetAllForTemplateOptions(None)
    return JSONResponse({'data_points':data_points})

@login_required(login_url='/user/login')
def dashboard_validate_data_point(request):
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    passed, errors = dpc.is_valid();
    return JSONResponse({'passed':passed, 'errors':errors})

@login_required(login_url='/user/login')
def dashboard_get_configured_data_point_name(request):
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    configured_display_name = dpc.get_configured_display_name()
    return JSONResponse({'configured_display_name':configured_display_name})

@login_required(login_url='/user/login')
def dashboard_remove_data_point(request):
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    dpc.data_point_removed()
    return JSONResponse()

@login_required(login_url='/user/login')
def dashboard_add_data_point(request):
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    dpc.data_point_added()
    return JSONResponse()

@login_required(login_url='/user/login')
def dashboard_run_search(request):
    configuration = {
        'data_points':json.loads(request.POST['data_points']),
        'search_filters':json.loads(request.POST['search_filters'])
    }
    sc = SearchController(configuration)
    search_results = sc.run_search_and_return_results()
    return JSONResponse({'search_results':search_results})

@login_required(login_url='/user/login')
def dashboard_get_content_item_template(request, type, sub_type):
    data_point = { 'type':type, 'sub_type':sub_type }
    dpc = DataPointController(data_point)
    template = dpc.get_content_item_template()
    return JSONResponse({'template':template, 'type':type, 'sub_type':sub_type})

@login_required(login_url='/user/login')
def dashboard_save(request):
    dashboard = json.loads(request.POST['dashboard'])
    user = request.user
    dbc = DashboardsController(user)
    dbc.update_dashboard(dashboard)
    return JSONResponse()

########################################################################################################################
# USER ACCOUNT FUNCTIONS
########################################################################################################################
@login_required(login_url='/user/login')
def user_saved_dashboards(request):
    dc = DashboardsController(request.user)
    saved_dashboards = dc.get_saved_dashboards()
    return render_to_response('parts/user_saved_dashboards.html', { 'saved_dashboards':saved_dashboards, })

@login_required(login_url='/user/login')
def user_dashboard_templates(request):
    dc = DashboardsController(request.user)
    dashboard_templates = dc.get_dashboard_templates()
    return render_to_response('parts/user_dashboard_templates.html', { 'dashboard_templates':dashboard_templates, })

def user_login(request):
    data_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        passed, errors = UserController.LoginUser(request, username, password)
        if passed:
            return redirect('/')
        data_dict['errors'] = errors
    return render_to_response(
        'index.html',
        data_dict,
        context_instance=RequestContext(request)
    )

@login_required(login_url='/user/login')
def user_logout(request):
    uc = UserController(request.user)
    uc.logout_user(request)
    return redirect('/')

@login_required(login_url='/user/login')
def user_new_dashboard_from_template(request, dashboard_template_id):
    uc = UserController(request.user)
    uc.register_dashboard_template_use(dashboard_template_id)
    dc = DashboardsController(request.user)
    db = dc.create_new_dashboard_from_template(dashboard_template_id)
    return JSONResponse({'dashboard_id':db['id']})