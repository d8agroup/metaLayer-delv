from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from dashboards.controllers import DashboardsController
from logger import Logger
from userprofiles.controllers import UserController
from utils import JSONResponse, serialize_to_json

def xd_receiver(request):
    return render_to_response('thecommunity/xd_receiver.html')

def user_home(request, user_name):
    if 'insight' in request.GET:
        DashboardsController.RecordDashboardView(request.GET['insight'])
    uc = UserController
    user = uc.GetUserByUserName(user_name)
    dc = DashboardsController(user)
    user_community_values = {
        'number_of_insights':len(dc.get_saved_dashboards())
    }
    return render_to_response(
        'thecommunity/profile_page/profile.html',
        {
            'profile_user':user,
            'profile_user_community_values':user_community_values
        },
        context_instance=RequestContext(request)
    )

def insight(request, user_name, insight_id):
    DashboardsController.RecordDashboardView(insight_id)
    user = UserController.GetUserByUserName(user_name)
    dashboard = DashboardsController.GetDashboardById(insight_id)
    dashboard_json = serialize_to_json(dashboard)
    return render_to_response(
        'thecommunity/insight_page/insight_page.html',
        { 'profile_user':user, 'insight':dashboard, 'insight_json':dashboard_json },
        context_instance=RequestContext(request)
    )

@login_required(login_url='/')
def user_account(request):
    return render_to_response(
        'thecommunity/account_page/account_page.html',
            {},
        context_instance=RequestContext(request)
    )

def community_page(request):
    categories = [{'name': c, 'count': DashboardsController.GetCategoryCount(c)} for c in  settings.INSIGHT_CATEGORIES]
    return render_to_response(
        'thecommunity/community_page/community.html',
        {'categories': categories},
        context_instance=RequestContext(request)
    )

def category_page(request, category):
    if category not in settings.INSIGHT_CATEGORIES:
        return redirect(community_page)
    dashboards = DashboardsController.GetDashboardsInCategory(category)
    dashboards = serialize_to_json([d for d in dashboards])
    return render_to_response(
        'thecommunity/category_page/category_page.html',
        {
            'category':category,
            'insights_json':dashboards
        },
        context_instance=RequestContext(request)
    )

def login_or_register(request):
    if not request.method == 'POST':
        return render_to_response(
            'thecommunity/login_or_register.html',
            context_instance=RequestContext(request)
        )
    else:
        if 'login' in request.POST:
            username = request.POST.get('login_username')
            password = request.POST.get('login_password')
            passed, errors = UserController.LoginUser(request, username, password)
            if not passed:
                return render_to_response(
                    'thecommunity/login_or_register.html',
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
                    'thecommunity/login_or_register.html',
                    { 'register_errors':errors },
                    context_instance=RequestContext(request)
                )
        return redirect('/community/%s' % request.user.username)

def logout(request):
    uc = UserController(request.user)
    uc.logout_user(request)
    return redirect(community_page)

@login_required(login_url='/')
def current_subscription(request):
    user = request.user
    uc = UserController(user)
    user_subscriptions = uc.get_user_subscriptions()
    current_active_subscription_name = user_subscriptions['active_subscription']
    current_active_subscription = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][current_active_subscription_name]
    return render_to_response(
        'thecommunity/account_page/account_page_user_account_management_current_subscription.html',
        { 'subscription':current_active_subscription }
    )

@login_required(login_url='/')
def change_subscription(request):
    Logger.Info("%s - change_subscription - started" % __name__)
    user = request.user
    if request.method == 'GET':
        if not 'subscription_id' in request.GET:
            uc = UserController(user)
            user_subscriptions = uc.get_user_subscriptions()
            current_active_subscription_name = user_subscriptions['active_subscription']
            available_subscriptions = [settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][sub] for sub in settings.SUBSCRIPTIONS_SETTINGS['subscriptions'].keys() if sub != current_active_subscription_name]
            Logger.Info('%s - change_subscription - finished' % __name__)
            return render_to_response(
                'thecommunity/account_page/account_page_user_account_management_list_available_subscriptions.html',
                    { 'subscriptions':available_subscriptions }
            )
        else:
            subscription_id = request.GET['subscription_id']
            subscription = [sub for sub in settings.SUBSCRIPTIONS_SETTINGS['subscriptions'].values() if sub['id'] == subscription_id][0]
            uc = UserController(user)
            subscription_migration_direction = uc.subscription_migration_direction(subscription['id'])
            template_name = 'thedashboard/change_subscriptions/%s' % subscription['templates'][subscription_migration_direction]
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

def load_dashboards(request, username, count=None):
    Logger.Info('%s - load_dashboards - started' % __name__)
    user = UserController.GetUserByUserName(username)
    dc = DashboardsController(user)
    saved_dashboards = dc.get_saved_dashboards()
    if count:
        saved_dashboards = saved_dashboards[:int(count)]
    Logger.Info('%s - load_dashboards - finished' % __name__)
    return JSONResponse({ 'dashboards':saved_dashboards })

def load_tending_insights(request, count):
    trending_dashboards = DashboardsController.GetTendingDashboards(count)
    return JSONResponse({'trending_insights':trending_dashboards})

def load_top_insights(request, count):
    top_insights = DashboardsController.GetTopDashboards(count)
    return JSONResponse({'top_insights':top_insights})

def load_recent_insights(request, count):
    recent_insights = DashboardsController.GetRecentDashboards(count)
    return JSONResponse({'recent_insights':recent_insights})

def load_remixes(request, insight_id, count):
    insights = DashboardsController.GetRemixes(insight_id, int(count))
    return JSONResponse({'insights':insights})