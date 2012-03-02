from django.conf import settings
from userprofiles.models import UserProfile

class RegistrationPolicy(object):
    def post_registration(self, user, registration_form_values):
        if 'register_code' not in registration_form_values or not registration_form_values['register_code']:
            return

        register_code = registration_form_values['register_code']
        register_code = register_code.upper()
        if register_code not in settings.REGISTRATION_POLICIES['InitialCodeRegistrationPolicy']['codes']:
            return

        user_profile = user.profile
        usage_limit = settings.REGISTRATION_POLICIES['InitialCodeRegistrationPolicy']['usage_limit']
        if UserProfile.objects.filter(registration_code='METALAYER - %s' % register_code).count() >= usage_limit:
            user_profile.registration_status = 'DECLINED'
            user_profile.save()
            return

        user_profile.registration_code = 'METALAYER - %s' % register_code
        user_profile.registration_status = 'APPROVED'
        user_profile.save()