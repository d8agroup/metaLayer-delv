from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
import constants
from invites.controllers import InviteController
from userprofiles.controllers import UserController

class LoginPolicy(object):
    def process_login(self, user, request, is_registration=False):
        user_profile = user.profile
        if user_profile.registration_status == 'WAITING':
            UserController(user).logout_user(request)
            return redirect('/delv/restricted_access')
        if user_profile.registration_status == 'DECLINED':
            UserController(user).logout_user(request)
            return redirect('/delv/restricted_access/with_code')

        if settings.INVITES['active']:
            remaining_invites_for_user = InviteController.InsightsRemainingForUser(user)
            if remaining_invites_for_user:
                messages.info(
                    request,
                    constants.USER_MESSAGES['invite_message_on_login'] % (
                        remaining_invites_for_user,
                        's' if remaining_invites_for_user > 1 else ''
                    ),
                    'left_arrow'
                )

        request_parameter = 'register' if is_registration else 'login'
        return redirect('/delv/%s?%s=true' % (user.username, request_parameter))