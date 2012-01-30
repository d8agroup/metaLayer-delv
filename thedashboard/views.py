from threading import Thread
from django.shortcuts import render_to_response, redirect
from django.views.decorators.cache import never_cache
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils import simplejson as json
from django.conf import settings
import time
from actions.controllers import ActionController
from aggregator.controllers import AggregationController
from datapoints.controllers import DataPointController
from logger import Logger
from outputs.controllers import OutputController
from search.controllers import SearchController
from userprofiles.controllers import UserController
from dashboards.controllers import DashboardsController
from utils import JSONResponse
from visualizations.controllers import VisualizationController

################################################################################
# ASYNC REQUESTS                                                               #
################################################################################
def async(gen):
    def func(*args, **kwargs):
        it = gen(*args, **kwargs)
        result = it.next()
        Thread(target=lambda: list(it)).start()
        return result
    return func

def index(request):
    Logger.Info('%s - index - started' % __name__)
    if not request.user.is_authenticated():
        if not request.method == 'POST':
            Logger.Info('%s - index - finished' % __name__)
            return render_to_response('login_or_register.html', context_instance=RequestContext(request))
        else:
            if 'login' in request.POST:
                username = request.POST.get('login_username')
                password = request.POST.get('login_password')
                passed, errors = UserController.LoginUser(request, username, password)
                if not passed:
                    Logger.Info('%s - index - finished' % __name__)
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
                    Logger.Info('%s - index - finished' % __name__)
                    return render_to_response(
                        'login_or_register.html',
                        { 'register_errors':errors },
                        context_instance=RequestContext(request)
                    )
    Logger.Info('%s - index - finished' % __name__)
    return render_to_response('my_account.html',context_instance=RequestContext(request))

@login_required(login_url='/')
def dashboard_load(request, id):
    Logger.Info('%s - dashboard - started' % __name__)
    Logger.Debug('%s - dashboard - started with id:%s' % (__name__, id))
    dc = DashboardsController(request.user)
    db = dc.get_dashboard_by_id(id)
    Logger.Info('%s - dashboard - finished' % __name__)
    return render_to_response('dashboard.html',{ 'dashboard_id':db['id'] }, context_instance=RequestContext(request))

@login_required(login_url='/')
def dashboard(request, id):
    Logger.Info('%s - dashboard - started' % __name__)
    dc = DashboardsController(request.user)
    db = dc.get_dashboard_by_id(id)
    Logger.Info('%s - dashboard - finished' % __name__)
    return JSONResponse({'dashboard':db})

@login_required(login_url='/')
def dashboard_get_all_widgets(request):
    Logger.Info('%s - dashboard_get_all_data_points - started' % __name__)
    #TODO: Need to get the options from the request.user and pass them to the controller
    data_points = DataPointController.GetAllForTemplateOptions(None)
    actions = ActionController.GetAllForTemplateOptions(None)
    outputs = OutputController.GetAllForTemplateOptions(None)
    visualizations = VisualizationController.GetAllForTemplateOptions(None)
    Logger.Info('%s - dashboard_get_all_data_points - finished' % __name__)
    return JSONResponse({'data_points':data_points, 'actions':actions, 'outputs':outputs, 'visualizations':visualizations})

@login_required(login_url='/')
def dashboard_validate_data_point(request):
    Logger.Info('%s - dashboard_validate_data_point - started' % __name__)
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    passed, errors = dpc.is_valid()
    if not passed:
        Logger.Info('%s - dashboard_validate_data_point - finished' % __name__)
        return JSONResponse({'passed':passed, 'errors':errors})
    configured_display_name = dpc.get_configured_display_name()
    return JSONResponse({'passed':passed, 'errors':errors, 'configured_display_name':configured_display_name})

@login_required(login_url='/')
def dashboard_remove_data_point(request):
    Logger.Info('%s - dashboard_remove_data_point - started' % __name__)
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    dpc.data_point_removed()
    Logger.Info('%s - dashboard_remove_data_point - finished' % __name__)
    return JSONResponse()

@login_required(login_url='/')
def dashboard_add_data_point_with_actions(request):
    Logger.Info('%s - dashboard_add_data_point - started' % __name__)
    start_time = time.time()
    data_point = request.POST['data_point']
    data_point = json.loads(data_point)
    dpc = DataPointController(data_point)
    dpc.data_point_added()
    actions = request.POST['actions']
    actions = json.loads(actions)
    AggregationController.AggregateSingleDataPoint(data_point, actions)
    Logger.Debug('%s - dashboard_add_data_point - finished in %i seconds' % (__name__, int(time.time() - start_time)))
    Logger.Info('%s - dashboard_add_data_point - finished' % __name__)
    return JSONResponse()

@login_required(login_url='/')
def dashboard_validate_action(request):
    Logger.Info('%s - dashboard_validate_action - started' % __name__)
    action = request.POST['action']
    action = json.loads(action)
    ac = ActionController(action)
    passed, errors = ac.is_valid()
    if not passed:
        Logger.Info('%s - dashboard_validate_action - finished' % __name__)
        return JSONResponse({'passed':passed, 'errors':errors})
    configured_display_name = ac.get_configured_display_name()
    return JSONResponse({'passed':passed, 'errors':errors, 'configured_display_name':configured_display_name})

@login_required(login_url='/')
def dashboard_remove_action(request):
    Logger.Info('%s - dashboard_remove_action - started' % __name__)
    action = request.POST['action']
    action = json.loads(action)
    ac = ActionController(action)
    ac.action_removed()
    Logger.Info('%s - dashboard_remove_action - finished' % __name__)
    return JSONResponse()

@login_required(login_url='/')
def dashboard_add_action_to_data_points(request):
    Logger.Info('%s - dashboard_add_action_to_data_points - started' % __name__)
    action = request.POST['action']
    action = json.loads(action)
    data_points = request.POST['data_points']
    data_points = json.loads(data_points)
    ac = ActionController(action)
    ac.action_added()
    AggregationController.AggregateMultipleDataPointHistoryWithAction(action, data_points, 50)
    Logger.Info('%s - dashboard_add_action_to_data_points - finished' % __name__)
    return JSONResponse()

@login_required(login_url='/')
def dashboard_get_output_url(request):
    Logger.Info('%s - dashboard_get_output_url - started' % __name__)
    output = request.POST['output']
    output = json.loads(output)
    oc = OutputController(output)
    url = oc.generate_url()
    output['url'] = url
    Logger.Info('%s - dashboard_get_output_url - finished' % __name__)
    return JSONResponse({'output':output})

@login_required(login_url='/')
def dashboard_output_removed(request):
    Logger.Info('%s - dashboard_output_removed - started' % __name__)
    output = request.POST['output']
    output = json.loads(output)
    oc = OutputController(output)
    oc.output_removed()
    Logger.Info('%s - dashboard_output_removed - finished' % __name__)
    return JSONResponse()

@login_required(login_url='/')
def dashboard_remove_visualization(request):
    Logger.Info('%s - dashboard_visualization_removed - started' % __name__)
    visualization = request.POST['visualization']
    visualization = json.loads(visualization)
    vc = VisualizationController(visualization)
    vc.visualization_removed()
    Logger.Info('%s - dashboard_visualization_removed - finished' % __name__)
    return JSONResponse()

@never_cache
@login_required(login_url='/')
def dashboard_run_visualization(request):
    Logger.Info('%s - dashboard_run_visualization - started' % __name__)
    visualization = request.POST['visualization']
    visualization = json.loads(visualization)
    configuration = {
        'data_points':json.loads(request.POST['data_points']),
        'search_filters':json.loads(request.POST['search_filters'])
    }
    vc = VisualizationController(visualization)
    search_query_additions_collection = vc.get_search_query_additions_collection(configuration)
    sc = SearchController(configuration)
    search_results_collection = [sc.run_search_and_return_results(sqa) for sqa in search_query_additions_collection]
    content = vc.render_javascript_visualization_for_search_results_collection(search_results_collection)
    content_type = 'text/javascript; charset=UTF-8'
    Logger.Info('%s - dashboard_run_visualization - finished' % __name__)
    return HttpResponse(content=content, content_type=content_type)

@login_required(login_url='/')
def dashboard_run_search(request):
    Logger.Info('%s - dashboard_run_search - started' % __name__)
    start_time = time.time()
    configuration = {
        'data_points':json.loads(request.POST['data_points']),
        'search_filters':json.loads(request.POST['search_filters'])
    }
    sc = SearchController(configuration)
    search_results = sc.run_search_and_return_results()
    Logger.Debug('%s - dashboard_run_search - finished in %i seconds' % (__name__, int(time.time() - start_time)))
    Logger.Info('%s - dashboard_run_search - finished' % __name__)
    return JSONResponse({'search_results':search_results})

@login_required(login_url='/')
def dashboard_get_content_item_template(request, type, sub_type):
    Logger.Info('%s - dashboard_get_content_item_template - started' % __name__)
    data_point = { 'type':type, 'sub_type':sub_type }
    dpc = DataPointController(data_point)
    template = dpc.get_content_item_template()
    Logger.Info('%s - dashboard_get_content_item_template - finished' % __name__)
    return JSONResponse({'template':template, 'type':type, 'sub_type':sub_type})

@login_required(login_url='/')
@async
def dashboard_save(request):
    yield JSONResponse()
    Logger.Info('%s - dashboard_save - started' % __name__)
    dashboard = json.loads(request.POST['dashboard'])
    user = request.user
    dbc = DashboardsController(user)
    dbc.update_dashboard(dashboard)
    Logger.Info('%s - dashboard_save - finished' % __name__)

########################################################################################################################
# USER ACCOUNT FUNCTIONS
########################################################################################################################
@login_required(login_url='/')
def user_saved_dashboards(request):
    Logger.Info('%s - user_saved_dashboards - started' % __name__)
    user = request.user
    dc = DashboardsController(user)
    saved_dashboards = dc.get_saved_dashboards()
    uc = UserController(user)
    maximum_number_of_saved_dashboards = uc.maximum_number_of_saved_dashboards_allowed_by_subscription()
    Logger.Info('%s - user_saved_dashboards - finished' % __name__)
    return JSONResponse({
        'maximum_number_of_saved_dashboards':maximum_number_of_saved_dashboards,
        'saved_dashboards':saved_dashboards
    })

@login_required(login_url='/')
def user_delete_dashboard(request):
    Logger.Info('%s - user_delete_dashboard - started' % __name__)
    user = request.user
    dashboard_id = request.GET['dashboard_id']
    dc = DashboardsController(user)
    dc.delete_dashboard_by_id(dashboard_id)
    Logger.Info('%s - user_delete_dashboard - finished' % __name__)
    return JSONResponse()

@login_required(login_url='/')
def user_dashboard_templates(request):
    Logger.Info('%s - user_dashboard_templates - started' % __name__)
    dc = DashboardsController(request.user)
    dashboard_templates = dc.get_dashboard_templates()
    Logger.Info('%s - user_dashboard_templates - finished' % __name__)
    return JSONResponse({'dashboard_templates':dashboard_templates})

@login_required(login_url='/')
def current_subscription(request):
    Logger.Info('%s - current_subscription - started' % __name__)
    user = request.user
    uc = UserController(user)
    user_subscriptions = uc.get_user_subscriptions()
    current_active_subscription_name = user_subscriptions['active_subscription']
    current_active_subscription = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][current_active_subscription_name]
    Logger.Info('%s - current_subscription - finished' % __name__)
    return render_to_response(
        'parts/user_account_management_current_subscription.html',
        { 'subscription':current_active_subscription }
    )

@login_required(login_url='/')
def change_subscription(request):
    Logger.Info('%s - change_subscription - started' % __name__)
    user = request.user
    if request.method == 'GET':
        if not 'subscription_id' in request.GET:
            uc = UserController(user)
            user_subscriptions = uc.get_user_subscriptions()
            current_active_subscription_name = user_subscriptions['active_subscription']
            available_subscriptions = [settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][sub] for sub in settings.SUBSCRIPTIONS_SETTINGS['subscriptions'].keys() if sub != current_active_subscription_name]
            Logger.Info('%s - change_subscription - finished' % __name__)
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
            Logger.Info('%s - change_subscription - finished' % __name__)
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
                Logger.Info('%s - change_subscription - finished' % __name__)
                return JSONResponse({'errors':['Enter credit card number "1" to pass and "0" to fail']})

            first_name = request.POST['first_name'].strip()
            last_name = request.POST['last_name'].strip()

            if not first_name or not last_name:
                Logger.Info('%s - change_subscription - finished' % __name__)
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
            Logger.Info('%s - change_subscription - finished' % __name__)
            return JSONResponse({'errors':['There was an error process your card details, please try again later']})

        maximum_number_of_dashboards = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][new_subscription_id]['config']['number_of_saved_dashboards']
        dc = DashboardsController(user)
        dc.delete_dashboards_to_match_subscription(maximum_number_of_dashboards)

        Logger.Info('%s - change_subscription - finished' % __name__)
        return JSONResponse()

@login_required(login_url='/')
def user_logout(request):
    Logger.Info('%s - user_logout - started' % __name__)
    uc = UserController(request.user)
    uc.logout_user(request)
    Logger.Info('%s - user_logout - finished' % __name__)
    return redirect('/')

@login_required(login_url='/')
def user_new_dashboard_from_template(request, dashboard_template_id):
    Logger.Info('%s - user_new_dashboard_from_template - started' % __name__)
    uc = UserController(request.user)
    uc.register_dashboard_template_use(dashboard_template_id)
    dc = DashboardsController(request.user)
    db = dc.create_new_dashboard_from_template(dashboard_template_id)
    Logger.Info('%s - user_new_dashboard_from_template - finished' % __name__)
    return JSONResponse({'dashboard_id':db['id']})