from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from userprofiles.controllers import UserController
from dashboards.controllers import DashboardsController

def index(request):
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
    return render_to_response(
        'dashboards_dashboard.html',
        {
            'dashboard':db
        }
    )

@login_required(login_url='/user/login')
def new_dashboard(request, id):
    pass

########################################################################################################################
# USER ACCOUNT FUNCTIONS
########################################################################################################################
@login_required(login_url='/user/login')
def user_home(request):
    dc = DashboardsController(request.user)
    saved_dashboards = dc.get_saved_dashboards()
    dashboard_templates = dc.get_dashboard_templates()
    return render_to_response(
        'site.html',
        {
            'saved_dashboards':saved_dashboards,
            'dashboard_templates':dashboard_templates,
        }
    )

def user_login(request):
    data_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        uc = UserController()
        passed, errors = uc.login_user(request, username, password)
        if passed:
            return redirect('/user/home')
        data_dict['errors'] = errors
    return render_to_response(
        'index.html',
        data_dict,
        context_instance=RequestContext(request)
    )

@login_required(login_url='/user/login')
def user_logout(request):
    uc = UserController()
    uc.logout_user(request)
    return redirect('/')