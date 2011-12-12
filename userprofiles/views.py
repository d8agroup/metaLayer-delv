from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dashboards.controllers import DashboardsController

def user_login(request):
    data_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            data_dict['errors'] = ['Sorry, we didn\'t recognize that email and password']
        elif not user.is_active:
            data_dict['errors'] = ['Sorry, your account is not currently active']
        else:
            login(request, user)
            return redirect('/users/home')
    return render_to_response(
        '../templates/user_login.html',
        data_dict,
        context_instance=RequestContext(request)
    )

@login_required(login_url='/users/login')
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/users/login')
def user_home(request):
    dc = DashboardsController(request.user)
    saved_dashboards = dc.render_saved_dashboards()
    return render_to_response(
        '../templates/user_home.html',
        {
            'saved_dashboards':saved_dashboards,
        }
    )