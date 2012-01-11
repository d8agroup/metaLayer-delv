from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from userprofiles.models import UserStatistics

class UserController(object):
    def __init__(self, user):
        self.user = user

    @classmethod
    def LoginUser(cls, request, username, password):
        user = authenticate(username=username, password=password)
        if user is None:
            return False, ['Sorry, we didn\'t recognize that email and password']
        elif not user.is_active:
            return False, ['Sorry, your account is not currently active']
        login(request, user)
        return True, []

    @classmethod
    def GetAllUsers(cls):
        return User.objects.all()

    def logout_user(self, request):
        logout(request)
        return

    def register_dashboard_template_use(self, dashboard_template_id):
        user_statistics = UserStatistics.GetForUsername(self.user.username)
        user_statistics.increment_dashboard_template_usage(dashboard_template_id)
        user_statistics.save()