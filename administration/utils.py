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

def safe_extract_user_profile(user):
    try:
        return user.profile
    except:
        return None