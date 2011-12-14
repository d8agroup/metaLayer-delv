from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from userprofiles.controllers import UserController
from dashboards.controllers import DashboardsController
from webapp.utils import JSONResponse

def index(request):
    if request.user.is_authenticated():
        return render_to_response('site.html')
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
def new_dashboard(request, id):
    pass

########################################################################################################################
# USER ACCOUNT FUNCTIONS
########################################################################################################################
@login_required(login_url='/user/login')
def user_saved_dashboards(request):
    dc = DashboardsController(request.user)
    saved_dashboards = dc.get_saved_dashboards()
    return render_to_response( 'parts/user_saved_dashboards.html', { 'saved_dashboards':saved_dashboards, })

@login_required(login_url='/user/login')
def user_dashboard_templates(request):
    dc = DashboardsController(request.user)
    dashboard_templates = dc.get_dashboard_templates()
    return render_to_response( 'parts/user_dashboard_templates.html', { 'dashboard_templates':dashboard_templates, })

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