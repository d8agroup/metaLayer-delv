from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseServerError
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
    user = request.user
    dc = DashboardsController(user)
    saved_dashboards = dc.get_saved_dashboards()
    uc = UserController(user)
    maximum_number_of_saved_dashboards = uc.maximum_number_of_saved_dashboards_allowed_by_subscription()
    return JSONResponse({
        'maximum_number_of_saved_dashboards':maximum_number_of_saved_dashboards,
        'saved_dashboards':saved_dashboards
    })

@login_required(login_url='/')
def user_delete_dashboard(request):
    user = request.user
    dashboard_id = request.GET['dashboard_id']
    dc = DashboardsController(user)
    dc.delete_dashboard_by_id(dashboard_id)
    return JSONResponse()

@login_required(login_url='/')
def user_dashboard_templates(request):
    dc = DashboardsController(request.user)
    dashboard_templates = dc.get_dashboard_templates()
    return JSONResponse({'dashboard_templates':dashboard_templates})

@login_required(login_url='/')
def current_subscription(request):
    user = request.user
    uc = UserController(user)
    user_subscriptions = uc.get_user_subscriptions()
    current_active_subscription_name = user_subscriptions['active_subscription']
    current_active_subscription = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][current_active_subscription_name]
    return render_to_response(
        'parts/user_account_management_current_subscription.html',
        { 'subscription':current_active_subscription }
    )

@login_required(login_url='/')
def change_subscription(request):
    user = request.user
    if request.method == 'GET':
        if not 'subscription_id' in request.GET:
            uc = UserController(user)
            user_subscriptions = uc.get_user_subscriptions()
            current_active_subscription_name = user_subscriptions['active_subscription']
            available_subscriptions = [settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][sub] for sub in settings.SUBSCRIPTIONS_SETTINGS['subscriptions'].keys() if sub != current_active_subscription_name]
            return render_to_response(
                'parts/user_account_management_list_available_subscriptions.html',
                { 'subscriptions':available_subscriptions }
            )
        else:
            subscription_id = request.GET['subscription_id']
            subscription = [sub for sub in settings.SUBSCRIPTIONS_SETTINGS['subscriptions'].values() if sub['id'] == subscription_id][0]
            uc = UserController(user)
            subscription_migration_direction = uc.subscription_migration_direction(subscription['id'])
            template_name = 'parts/change_subscriptions/%s' % subscription['templates'][subscription_migration_direction]
            return render_to_response(
                template_name,
                {
                    'subscription':subscription,
                    'show_credit_card_form':uc.need_to_ask_for_credit_card_details()
                },
                context_instance=RequestContext(request)
            )
    else:
        if 'credit_card_number' in request.POST:
            credit_card_number = request.POST['credit_card_number']
            if credit_card_number != '0' and credit_card_number != '1':
                #TODO: this is just for the tests
                return JSONResponse({'errors':['Enter credit card number "1" to pass and "0" to fail']})

            first_name = request.POST['first_name'].strip()
            last_name = request.POST['last_name'].strip()

            if not first_name or not last_name:
                return JSONResponse({'errors':['You must provide your first and last name']})

            user.first_name = first_name
            user.last_name = last_name
            user.save()
            credit_card_data = {
                'number':credit_card_number,
                'expiry_month':request.POST['credit_card_expiry_month'],
                'expiry_year':int(request.POST['credit_card_expiry_year'])
            }
        else:
            credit_card_data = None

        new_subscription_id = request.POST['subscription_id']
        uc = UserController(user)
        subscription_changed = uc.change_user_subscription(
            new_subscription_id,
            credit_card_data
        )
        if not subscription_changed:
            return JSONResponse({'errors':['There was an error process your card details, please try again later']})

        maximum_number_of_dashboards = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][new_subscription_id]['config']['number_of_saved_dashboards']
        dc = DashboardsController(user)
        dc.delete_dashboards_to_match_subscription(maximum_number_of_dashboards)

        return JSONResponse()

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