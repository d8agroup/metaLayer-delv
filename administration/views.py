import datetime
import re
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from administration.utils import staff_member_required, _base_template_data, safe_extract_user_profile
from administration.utils import dashboard_is_using_action, dashboard_is_using_data_point, dashboard_is_using_visualization
from metalayercore.dashboards.models import Dashboard


@staff_member_required
def home(request):
    template_data = _base_template_data(request)
    return render_to_response('administration/home.html', template_data, context_instance=RequestContext(request))

@staff_member_required
def users(request):
    template_data = _base_template_data(request)
    user_objects = User.objects.filter(is_staff=False)
    users_past_1 = [u for u in user_objects if u.date_joined >= (datetime.datetime.now() + datetime.timedelta(days=-7))]
    users_past_2 = [u for u in user_objects if u.date_joined < (datetime.datetime.now() + datetime.timedelta(days=-7)) and u.date_joined >= (datetime.datetime.now() + datetime.timedelta(days=-14))]
    users_past_3 = [u for u in user_objects if u.date_joined < (datetime.datetime.now() + datetime.timedelta(days=-14)) and u.date_joined >= (datetime.datetime.now() + datetime.timedelta(days=-21))]
    users_past_4 = [u for u in user_objects if u.date_joined < (datetime.datetime.now() + datetime.timedelta(days=-21)) and u.date_joined >= (datetime.datetime.now() + datetime.timedelta(days=-28))]

    template_data['registrations_overall_total'] = user_objects.count()
    template_data['registrations_overall_past_1'] = len(users_past_1)
    template_data['registrations_overall_past_2'] = len(users_past_2)
    template_data['registrations_overall_past_3'] = len(users_past_3)
    template_data['registrations_overall_past_4'] = len(users_past_4)

    user_profiles = [up for up in [safe_extract_user_profile(u) for u in user_objects] if up]
    template_data['by_registration_status'] = []
    for status in [('Held', r'[WAITING|DECLINED]'), ('Let in','APPROVED')]:
        template_data['by_registration_status'].append(
            {
                'name':status[0],
                'total':len([u for u in user_profiles if re.search(status[1], u.registration_status)])
            }
        )

    template_data['by_registration_type'] = []
    for status in [('TED Code', r'^TED.*'), ('METALAYER Code', r'^METALAYER.*'), ('Invited', r'^INVITE.*')]:
        template_data['by_registration_type'].append(
            {
                'name':status[0],
                'total':len([u for u in user_profiles if re.search(status[1], u.registration_code)])
            }
        )

    sorted([u for u in user_objects], key=lambda a: a.username)
    template_data['all_users'] = user_objects

    user_email_domains = {}
    for user in user_objects:
        user_email_domain = user.username.split('@')[1]
        if not user_email_domain in user_email_domains:
            user_email_domains[user_email_domain] = { 'held':0, 'let_in':0 }
        for user_profile in user_profiles:
            if user_profile.user == user:
                if user_profile.registration_status == 'APPROVED':
                    user_email_domains[user_email_domain]['let_in'] += 1
                else:
                    user_email_domains[user_email_domain]['held'] += 1

    user_email_domains = [{'name':k,'held':v['held'],'let_in':v['let_in']} for k, v in user_email_domains.items()]
    template_data['user_email_domains'] = user_email_domains

    return render_to_response('administration/users.html', template_data, context_instance=RequestContext(request))

def insights(request):
    def filter_by_past(dbs, start, end):
        return [d for d in dbs if
                datetime.datetime.fromtimestamp(d.created) < (datetime.datetime.now() + datetime.timedelta(days=(start * -1))) and
                datetime.datetime.fromtimestamp(d.created) >= (datetime.datetime.now() + datetime.timedelta(days=(end * -1)))]

    template_data = _base_template_data(request)
    dashboards = Dashboard.objects.all()

    dashboards_past_1 = filter_by_past(dashboards, 0, 7)
    dashboards_past_2 = filter_by_past(dashboards, 7, 14)
    dashboards_past_3 = filter_by_past(dashboards, 14, 21)
    dashboards_past_4 = filter_by_past(dashboards, 21, 28)

    template_data['stats'] = [
        {
            'name':'Total Created',
            'total':len(dashboards),
            'past1':len(dashboards_past_1),
            'past2':len(dashboards_past_2),
            'past3':len(dashboards_past_3),
            'past4':len(dashboards_past_4)
        },
        {
            'name':'Total live on Delv',
            'total':len([d for d in dashboards if d.deleted == False]),
            'past1':len([d for d in dashboards_past_1 if d.deleted == False]),
            'past2':len([d for d in dashboards_past_2 if d.deleted == False]),
            'past3':len([d for d in dashboards_past_3 if d.deleted == False]),
            'past4':len([d for d in dashboards_past_4 if d.deleted == False]),
        },
        {
            'name':'Total Always On',
            'total':len([d for d in dashboards if 'live' in d.config and d.config['live'] == True]),
            'past1':len([d for d in dashboards_past_1 if 'live' in d.config and d.config['live'] == True]),
            'past2':len([d for d in dashboards_past_2 if 'live' in d.config and d.config['live'] == True]),
            'past3':len([d for d in dashboards_past_3 if 'live' in d.config and d.config['live'] == True]),
            'past4':len([d for d in dashboards_past_4 if 'live' in d.config and d.config['live'] == True]),
        },
    ]

    template_data['data_point_usage'] = [
        {
            'name':'Twitter',
            'total':len([d for d in dashboards if dashboard_is_using_data_point(d, 'twittersearch')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_data_point(d, 'twittersearch')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_data_point(d, 'twittersearch')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_data_point(d, 'twittersearch')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_data_point(d, 'twittersearch')]),
        },
        {
            'name':'Feed',
            'total':len([d for d in dashboards if dashboard_is_using_data_point(d, 'feed')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_data_point(d, 'feed')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_data_point(d, 'feed')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_data_point(d, 'feed')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_data_point(d, 'feed')]),
        },
        {
            'name':'Google News',
            'total':len([d for d in dashboards if dashboard_is_using_data_point(d, 'googlenewssearch')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_data_point(d, 'googlenewssearch')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_data_point(d, 'googlenewssearch')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_data_point(d, 'googlenewssearch')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_data_point(d, 'googlenewssearch')]),
        },
        {
            'name':'Google Plus',
            'total':len([d for d in dashboards if dashboard_is_using_data_point(d, 'googleplusactivitysearch')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_data_point(d, 'googleplusactivitysearch')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_data_point(d, 'googleplusactivitysearch')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_data_point(d, 'googleplusactivitysearch')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_data_point(d, 'googleplusactivitysearch')]),
        },
    ]
    
    template_data['action_usage'] = [
        {
            'name':'Tagging',
            'total':len([d for d in dashboards if dashboard_is_using_action(d, 'datalayertagging')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_action(d, 'datalayertagging')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_action(d, 'datalayertagging')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_action(d, 'datalayertagging')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_action(d, 'datalayertagging')]),
        },
        {
            'name':'Language',
            'total':len([d for d in dashboards if dashboard_is_using_action(d, 'languagedetection')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_action(d, 'languagedetection')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_action(d, 'languagedetection')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_action(d, 'languagedetection')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_action(d, 'languagedetection')]),
        },
        {
            'name':'Sentiment',
            'total':len([d for d in dashboards if dashboard_is_using_action(d, 'localsentimentanalysis')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_action(d, 'localsentimentanalysis')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_action(d, 'localsentimentanalysis')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_action(d, 'localsentimentanalysis')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_action(d, 'localsentimentanalysis')]),
        },
        {
            'name':'Location',
            'total':len([d for d in dashboards if dashboard_is_using_action(d, 'yahooplacemaker')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_action(d, 'yahooplacemaker')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_action(d, 'yahooplacemaker')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_action(d, 'yahooplacemaker')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_action(d, 'yahooplacemaker')]),
        },
    ]

    template_data['visualization_usage'] = [
        {
            'name':'Words',
            'total':len([d for d in dashboards if dashboard_is_using_visualization(d, 'd3cloud')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_visualization(d, 'd3cloud')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_visualization(d, 'd3cloud')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_visualization(d, 'd3cloud')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_visualization(d, 'd3cloud')]),
        },
        {
            'name':'Area Chart',
            'total':len([d for d in dashboards if dashboard_is_using_visualization(d, 'googleareachart')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_visualization(d, 'googleareachart')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_visualization(d, 'googleareachart')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_visualization(d, 'googleareachart')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_visualization(d, 'googleareachart')]),
        },
        {
            'name':'Bar Chart',
            'total':len([d for d in dashboards if dashboard_is_using_visualization(d, 'googlebarchart')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_visualization(d, 'googlebarchart')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_visualization(d, 'googlebarchart')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_visualization(d, 'googlebarchart')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_visualization(d, 'googlebarchart')]),
        },
        {
            'name':'Map',
            'total':len([d for d in dashboards if dashboard_is_using_visualization(d, 'googlegeochart')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_visualization(d, 'googlegeochart')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_visualization(d, 'googlegeochart')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_visualization(d, 'googlegeochart')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_visualization(d, 'googlegeochart')]),
        },
        {
            'name':'Pie',
            'total':len([d for d in dashboards if dashboard_is_using_visualization(d, 'googlepiechart')]),
            'past1':len([d for d in dashboards_past_1 if dashboard_is_using_visualization(d, 'googlepiechart')]),
            'past2':len([d for d in dashboards_past_2 if dashboard_is_using_visualization(d, 'googlepiechart')]),
            'past3':len([d for d in dashboards_past_3 if dashboard_is_using_visualization(d, 'googlepiechart')]),
            'past4':len([d for d in dashboards_past_4 if dashboard_is_using_visualization(d, 'googlepiechart')]),
        },
    ]


    return render_to_response('administration/insights.html', template_data, context_instance=RequestContext(request))
