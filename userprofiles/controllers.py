from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import email_re
from django.conf import settings
from chargifyapi.chargify import Chargify
from userprofiles.models import UserStatistics, UserSubscriptions

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

    @classmethod
    def RegisterUser(cls, request, username, password1, password2):
        errors = []
        if not username or not username.strip() or not bool(email_re.search(username)):
            errors.append('You have not entered a valid email address')
        try:
            User.objects.get(username=username)
            errors.append('Sorry, that email address is already being used')
        except User.DoesNotExist:
            pass
        if errors:
            return False, errors
        if len(password1) < 6:
            errors.append('Your password must be at least 6 characters long')
        if password1 != password2:
            errors.append('The passwords you entered don\'t match')
        if errors:
            return False, errors
        User.objects.create_user(username, username, password1)
        UserSubscriptions.InitForUsername(username)
        return UserController.LoginUser(request, username, password1)

    def logout_user(self, request):
        logout(request)
        return

    def register_dashboard_template_use(self, dashboard_template_id):
        user_statistics = UserStatistics.GetForUsername(self.user.username)
        user_statistics.increment_dashboard_template_usage(dashboard_template_id)

    def get_user_subscriptions(self):
        user_subscriptions = UserSubscriptions.GetForUsername(self.user.username)
        return user_subscriptions

    def change_user_subscription(self, new_subscription_id, credit_card=None):
        user_subscriptions = UserSubscriptions.GetForUsername(self.user.username)
        active_subscription = user_subscriptions.get_active_subscription()
        active_subscription_config = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][active_subscription['subscription_id']]
        new_subscription_config = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][new_subscription_id]
        chargify = Chargify(settings.CHARGIFY_SETTINGS['api_key'], settings.CHARGIFY_SETTINGS['subdomain'])
        try:
            if not settings.SUBSCRIPTIONS_SETTINGS['allow_subscription_migrations']:
                raise Exception()
            elif not active_subscription_config['chargify_config']: #Moving from free to paid
                result = chargify.subscriptions.create({
                    'product_handle':new_subscription_config['chargify_config']['product_handle'],
                    'customer_attributes':{
                        'first_name':self.user.first_name,
                        'last_name':self.user.last_name,
                        'email':self.user.email
                    },
                    'credit_card_attributes':{
                        'full_number':credit_card['number'],
                        'expiration_month':credit_card['expiry_month'],
                        'expiration_year':credit_card['expiry_year']
                    }
                })
                user_subscriptions.subscription_changed(
                    new_subscription_id,
                    active_subscription['extensions'],
                    { 'chargify':{'subscription_created':result}}
                )
            elif not new_subscription_config['chargify_config']: #Moving to free from paid
                chargify_subscription_id = active_subscription['extensions']['chargify']['subscription_ceated']['subscription']['id']
                result = chargify.subscriptions.delete(subscription_id=chargify_subscription_id)
                active_subscription['extensions']['chargify']['subscription_deleted'] = result
                user_subscriptions.subscription_changed(
                    new_subscription_id,
                    active_subscription['extensions'],
                    {}
                )
            else: #Migrating up or down subscriptions
                chargify_subscription_id = active_subscription['extensions']['chargify']['subscription_ceated']['subscription']['id']
                result = chargify.subscriptions.migrations.create(
                    subscription_id=123,
                    data={ 'product_id':new_subscription_config['chargify_config']['product_id'] }
                )
                active_subscription['extensions']['chargify']['subscription_migrated_from'] = result
                user_subscriptions.subscription_changed(
                    new_subscription_id,
                    active_subscription['extensions'],
                        { 'chargify':{'subscription_migrated_to':result}}
                )
            return True
        except:
            #TODO Log
            return False

