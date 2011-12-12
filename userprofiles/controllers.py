from django.contrib.auth import authenticate, login, logout

class UserController(object):
    def login_user(self, request, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            return False, ['Sorry, we didn\'t recognize that email and password']
        elif not user.is_active:
            return False, ['Sorry, your account is not currently active']
        login(request, user)
        return True, []

    def logout_user(self, request):
        logout(request)
        return