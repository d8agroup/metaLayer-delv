import datetime
import re
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from administration.utils import staff_member_required, _base_template_data, safe_extract_user_profile
from dashboards.models import Dashboard


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

    return render_to_response('administration/users.html', template_data, context_instance=RequestContext(request))

def insights(request):
    template_data = _base_template_data(request)
    dashboards = Dashboard.objects.all()

    template_data['overall_stats'] = {
        'total_created':len(dashboards),
        'total_currently_on_site':len([d for d in dashboards if d.deleted == False]),
        'total_always_on':len([d for d in dashboards if 'live' in d.config and d.config['live'] == True])
    }

    return render_to_response('administration/insights.html', template_data, context_instance=RequestContext(request))