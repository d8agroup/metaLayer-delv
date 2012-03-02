import datetime
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from administration.utils import staff_member_required, _base_template_data


@staff_member_required
def home(request):
    template_data = _base_template_data(request)
    return render_to_response('administration/home.html', template_data, context_instance=RequestContext(request))

@staff_member_required
def users(request):
    template_data = _base_template_data(request)
    users = User.objects.filter(is_staff=False)
    template_data['registrations_overall_total'] = users.count()
    template_data['registrations_overall_past_1'] = len([u for u in users if u.date_joined >= (datetime.datetime.now() + datetime.timedelta(days=-7))])
    template_data['registrations_overall_past_2'] = len([u for u in users if u.date_joined < (datetime.datetime.now() + datetime.timedelta(days=-7)) and u.date_joined >= (datetime.datetime.now() + datetime.timedelta(days=-14))])
    template_data['registrations_overall_past_3'] = len([u for u in users if u.date_joined < (datetime.datetime.now() + datetime.timedelta(days=-14)) and u.date_joined >= (datetime.datetime.now() + datetime.timedelta(days=-21))])
    template_data['registrations_overall_past_4'] = len([u for u in users if u.date_joined < (datetime.datetime.now() + datetime.timedelta(days=-21)) and u.date_joined >= (datetime.datetime.now() + datetime.timedelta(days=-28))])
    return render_to_response('administration/users.html', template_data, context_instance=RequestContext(request))