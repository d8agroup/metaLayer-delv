from django.shortcuts import redirect
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
        request_parameter = 'register' if is_registration else 'login'
        return redirect('/delv/%s?%s=true' % (user.username, request_parameter))