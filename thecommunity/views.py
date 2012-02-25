from random import randint
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from dashboards.controllers import DashboardsController
from logger import Logger
from userprofiles.controllers import UserController
from utils import JSONResponse, serialize_to_json, my_import

def _base_template_data():
    return {
        'short_url':settings.SITE_HOST_SHORT,
        'site_url':settings.SITE_HOST,
        'image_url':settings.IMAGE_HOST,
        'facebook_app_id':settings.FACEBOOK_SETTINGS['api_key'],
        'social_sharing_services':settings.SOCIAL_SHARING_SERVICES,
        'cache_timeout':settings.CACHE_TIMEOUT,
    }

def xd_receiver(request):
    return render_to_response('thecommunity/xd_receiver.html')

def user_home(request, user_name):
    if 'insight' in request.GET:
        insight_id = request.GET['insight']
        if user_name != request.user.username:
            DashboardsController.RecordDashboardView(insight_id)
        return redirect('/delv/%s#%s' % (user_name, insight_id))

    template_data = _base_template_data()

    uc = UserController
    user = uc.GetUserByUserName(user_name)
    template_data['profile_user'] = user
    template_data['my_creations'] = DashboardsController(user).get_saved_dashboards(3)
    trending_insights = DashboardsController.GetTendingDashboards(9)
    template_data['trending_insights_1'] = trending_insights[0:3]
    template_data['trending_insights_2'] = trending_insights[3:6]
    template_data['trending_insights_3'] = trending_insights[6:9]
    template_data['my_activity'] = DashboardsController(user).get_saved_dashboards(20)
    return render_to_response(
        'thecommunity/profile_page/profile_page.html',
        template_data,
        context_instance=RequestContext(request)
    )

def insight(request, user_name, insight_id):
    template_data = _base_template_data()
    DashboardsController.RecordDashboardView(insight_id)
    user = UserController.GetUserByUserName(user_name)
    dashboard = DashboardsController.GetDashboardById(insight_id)
    dashboard_json = serialize_to_json(dashboard)
    template_data['profile_user'] = user
    template_data['insight'] = dashboard
    template_data['insight_json'] = dashboard_json
    template_data['trending_insights'] = DashboardsController.GetTendingDashboards(9)
    return render_to_response(
        'thecommunity/insight_page/insight_page.html',
        template_data,
        context_instance=RequestContext(request)
    )

@login_required(login_url='/')
def user_account(request):
    template_data = _base_template_data()
    template_data['facebook_api_key'] = settings.FACEBOOK_SETTINGS['api_key']
    template_data['facebook_permissions'] = ','.join(settings.FACEBOOK_SETTINGS['requested_permissions'])
    template_data['twitter_api_key'] = settings.TWITTER_SETTINGS['api_key']
    
    return render_to_response(
        'thecommunity/account_page/account_page.html',
        template_data,
        context_instance=RequestContext(request)
    )

@login_required(login_url='/')
@csrf_exempt
def link_facebook_profile(request):
    """
    Associates a Facebook profile to a metaLayer user account.
    
    """
    
    if not request.method == 'POST':
        return redirect('/delv/%s' % request.user.username)
    
    facebook_id = request.POST.get('facebook_id')
    access_token = request.POST.get('access_token')
    
    controller = UserController(request.user)
    passed, errors = controller.link_facebook_profile(facebook_id, access_token)
    
    # return profile pic location to caller so front-end can display profile picture
    if passed:
        return JSONResponse({'profile_picture': request.user.profile.profile_image() })
    else:
        return JSONResponse({'errors': errors })

def community_page(request):
    template_data = _base_template_data()

    categories = [{'name': c, 'count': DashboardsController.GetCategoryCount(c)} for c in  settings.INSIGHT_CATEGORIES]
    template_data['category_list_1'] = categories[:int(len(categories)/2)]
    template_data['category_list_2'] = categories[int(len(categories)/2):]

    top_insights = DashboardsController.GetTopDashboards(4)
    if top_insights:
        template_data['top_insights_main'] = top_insights[0]
    if len(top_insights) > 1:
        template_data['top_insights_list'] = top_insights[1:]

    template_data['trending_insights'] = DashboardsController.GetTendingDashboards(3)
    template_data['recent_challenges'] = DashboardsController.GetRecentDashboards(3)

    if request.user.is_authenticated():
        template_data['your_creations'] = DashboardsController(request.user).get_saved_dashboards(4)

    return render_to_response(
        'thecommunity/community_page/community_page.html',
        template_data,
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
            'thecommunity/login_or_register/login_or_register.html',
            context_instance=RequestContext(request)
        )
    else:
        if 'login' in request.POST:
            username = request.POST.get('login_username')
            password = request.POST.get('login_password')
            passed, errors = UserController.LoginUser(request, username, password)
            if not passed:
                return render_to_response(
                    'thecommunity/login_or_register/login_or_register.html',
                    { 'login_errors':errors },
                    context_instance=RequestContext(request)
                )
            user = UserController.GetUserByUserName(username)
            login_policy = getattr(my_import(settings.LOGIN_POLICY['module']), 'LoginPolicy')()
            return login_policy.process_login(user, request)
        elif 'register' in request.POST:
            username = request.POST.get('register_username')
            password1 = request.POST.get('register_password1')
            password2 = request.POST.get('register_password2')
            registration_code = request.POST.get('register_code')
            passed, errors = UserController.RegisterUser(request, username, password1, password2, registration_code)
            if not passed:
                return render_to_response(
                    'thecommunity/login_or_register/login_or_register.html',
                    { 'register_errors':errors },
                    context_instance=RequestContext(request)
                )
            user = UserController.GetUserByUserName(username)
            for registration_policy in [getattr(my_import(rp['module']), 'RegistrationPolicy')() for rp in settings.REGISTRATION_POLICIES.values() if rp['active']]:
                registration_policy.post_registration(user, {'register_code':registration_code})
            login_policy = getattr(my_import(settings.LOGIN_POLICY['module']), 'LoginPolicy')()
            return login_policy.process_login(user, request, True)

@login_required(login_url='/')
def change_password(request):
    """
    Allows logged-in user to change their password.
    
    """
    
    Logger.Info("%s - change_password - started" % __name__)
    if not request.method == 'POST':
        return redirect('/delv/%s' % request.user.username)
    
    current_password = request.POST.get('current_password')
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')
    
    controller = UserController(request.user)
    passed, errors = controller.change_password(current_password, new_password, confirm_password)
    
    template_data = _base_template_data()
    
    if errors:
        template_data['messages'] = errors
        template_data['current_password'] = current_password
        template_data['new_password'] = new_password
        template_data['confirm_password'] = confirm_password
    else:
        template_data['messages'] = ['Your password has been changed successfully!']
    
    template_data['facebook_api_key'] = settings.FACEBOOK_SETTINGS['api_key']
    template_data['facebook_permissions'] = ','.join(settings.FACEBOOK_SETTINGS['requested_permissions'])
    template_data['twitter_api_key'] = settings.TWITTER_SETTINGS['api_key']
    
    Logger.Info('%s - change_password - finished' % __name__)
    
    return render_to_response(
        'thecommunity/account_page/account_page.html',
        template_data,
        context_instance=RequestContext(request)
    )

def change_email_opt_in(request):    
    """
    Allows user to opt in or opt out of email newsletters.
    
    """
    
    Logger.Info("%s - change_email_opt_in - started" % __name__)
    if not request.method == 'POST':
        return redirect('/delv/%s' % request.user.username)
    
    opt_in_status = request.POST.get('opt_in_status')
    
    controller = UserController(request.user)
    passed, errors = controller.change_email_opt_in(opt_in_status)
    
    template_data = _base_template_data()
    
    if errors:
        template_data['messages'] = errors
        template_data['opt_in_status'] = opt_in_status
    else:
        template_data['messages'] = ['Your email opt-in status has been updated successfully.']
    
    template_data['facebook_api_key'] = settings.FACEBOOK_SETTINGS['api_key']
    template_data['facebook_permissions'] = ','.join(settings.FACEBOOK_SETTINGS['requested_permissions'])
    template_data['twitter_api_key'] = settings.TWITTER_SETTINGS['api_key']
    
    Logger.Info('%s - change_email_opt_in - finished' % __name__)
    
    return render_to_response(
        'thecommunity/account_page/account_page.html',
        template_data,
        context_instance=RequestContext(request)
    )

def logout(request):
    uc = UserController(request.user)
    uc.logout_user(request)
    return redirect(community_page)

def create_from_template(request):
    template_name = request.POST['template_name']
    template = [t for t in settings.DASHBOARD_TEMPLATES if t['name'] == template_name][0]
    template = template['template']
    template['username'] = request.user.username
    for collection in template['collections']:
        for visualization in collection['visualizations']:
            for element in visualization['elements']:
                if element['name'] == 'colorscheme':
                    element['value'] = element['values'][randint(0, len(element['values']) - 1)]
    dc = DashboardsController(request.user)
    db = dc.create_new_dashboard_from_settings(template)
    return redirect('/dashboard/%s' % db.id)


def delete_insight(request, insight_id):
    Logger.Info('%s - dashboard_delete - started' % __name__)
    Logger.Debug('%s - dashboard_delete - started with id:%s' % (__name__, id))
    dc = DashboardsController(request.user)
    db = dc.get_dashboard_by_id(insight_id)
    if db and db['username'] == request.user.username:
        db.delete()
    Logger.Info('%s - dashboard_delete - finished' % __name__)
    return redirect(user_home, request.user.username)

@login_required(login_url='/')
def current_subscription(request):
    user = request.user
    uc = UserController(user)
    user_subscriptions = uc.get_user_subscriptions()
    current_active_subscription_name = user_subscriptions['active_subscription']
    current_active_subscription = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][current_active_subscription_name]
    return render_to_response(
        'thecommunity/account_page/_old/account_page_user_account_management_current_subscription.html',
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
                'thecommunity/account_page/_old/account_page_user_account_management_list_available_subscriptions.html',
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
    template_data = _base_template_data()
    template_data['insights']  = DashboardsController.GetRemixes(insight_id, int(count))
    return render_to_response( 'thecommunity/profile_page/insight_remixes.html', template_data )

def no_access(request):
    template_data = _base_template_data()
    return render_to_response(
        'thecommunity/no_access/no_access.html',
        template_data,
        context_instance=RequestContext(request)
    )

def no_access_with_code(request):
    template_data = _base_template_data()
    template_data['code'] = True
    return render_to_response(
        'thecommunity/no_access/no_access.html',
        template_data,
        context_instance=RequestContext(request)
    )

def site_down(request):
    template_data = _base_template_data()
    return render_to_response(
        'thecommunity/site_down/site_down.html',
        template_data,
        context_instance=RequestContext(request)
    )