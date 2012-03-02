import re
from django.conf import settings
from django.http import Http404

def staff_member_required(func):
    def check_staff_status(request, *args, **kwargs):
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return func(request, *args, **kwargs)
        raise Http404
    return check_staff_status

def _base_template_data(request):
    return {
        'admin_root':settings.CUSTOM_ADMIN_ROOT,
    }

def match_registration_status(regex, user):
    user_profile = user.profile
    registration_status = user_profile.registration_status
    return re.search(regex, registration_status)

def match_registration_code(regex, user_profile):
    registration_code = user_profile.registration_code
    return re.search(regex, registration_code)


