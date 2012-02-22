from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import email_re
from django.conf import settings
from chargifyapi.chargify import Chargify
from logger import Logger
from userprofiles.models import UserStatistics, UserSubscriptions, UserProfile
from utils import empty
import constants
from integrations import facebook

class UserController(object):
    def __init__(self, user):
        Logger.Info('%s - UserController.__init__ - started' % __name__)
        Logger.Debug('%s - UserController.__init__ - started with user:%s' % (__name__, user))
        self.user = user
        Logger.Info('%s - UserController.__init__ - finished' % __name__)

    @classmethod
    def LoginUser(cls, request, username, password):
        Logger.Info('%s - UserController.LoginUser - started' % __name__)
        Logger.Debug('%s - UserController.LoginUser - started with request:%s and username:%s and password:%s' % (__name__, request, username, password))
        user = authenticate(username=username, password=password)
        return_values = True, []
        if user is None:
            Logger.Info('%s - UserController.LoginUser - finished' % __name__)
            return False, ['Sorry, we didn\'t recognize that email and password']
        elif not user.is_active:
            Logger.Info('%s - UserController.LoginUser - finished' % __name__)
            return False, ['Sorry, your account is not currently active']
        login(request, user)
        Logger.Info('%s - UserController.LoginUser - finished' % __name__)
        return return_values

    @classmethod
    def GetAllUsers(cls, user_subscription_filter=None):
        Logger.Info('%s - UserController.GetAllUsers - started' % __name__)
        Logger.Debug('%s - UserController.GetAllUsers - started with user_subscription_filter:%s' % (__name__, user_subscription_filter))
        def user_is_with_filter(user, subscription_filter):
            uc = UserController(user)
            subscription_migration_direction = uc.subscription_migration_direction(subscription_filter)
            return bool(subscription_migration_direction == 'downgrade' or not subscription_migration_direction)
        users = User.objects.all()
        if user_subscription_filter:
            users = [user for user in users if user_is_with_filter(user, user_subscription_filter)]
        Logger.Info('%s - UserController.GetAllUsers - finished' % __name__)
        return users

    @classmethod
    def RegisterUser(cls, request, username, password1, password2, registration_code=None):
        Logger.Info('%s - UserController.RegisterUser - started' % __name__)
        Logger.Debug('%s - UserController.RegisterUser - started with request:%s and username:%s and password1:%s and password2:%s' % (__name__, request, username, password1, password2))
        errors = []
        if empty(username) or not bool(email_re.search(username)):
            errors.append('You have not entered a valid email address')
        try:
            User.objects.get(username=username)
            errors.append('Sorry, that email address is already being used')
        except User.DoesNotExist:
            pass
        if errors:
            Logger.Info('%s - UserController.RegisterUser - finished' % __name__)
            return False, errors
        
        passed, rules_errors = _check_password_rules(password1)
        if not passed:
            errors += rules_errors
        if password1 != password2:
            errors.append('The passwords you entered don\'t match')
        if errors:
            Logger.Info('%s - UserController.RegisterUser - finished' % __name__)
            return False, errors
        User.objects.create_user(username, username, password1)
        UserSubscriptions.InitForUsername(username)
        UserController.LoginUser(request, username, password1)
        user = UserController.GetUserByUserName(username)
        if registration_code:
            user.profile.registration_code = registration_code
        Logger.Info('%s - UserController.RegisterUser - finished' % __name__)
        return True, []

    @classmethod
    def GetUserByUserName(cls, user_name):
        return User.objects.get(username=user_name)
        
    def change_password(self, password, new_password1, new_password2):
        Logger.Info('%s - UserController.ChangePassword - started' % __name__)
        Logger.Debug('%s - UserController.ChangePassword - started with password:%s and new_password1:%s and new_password2:%s' 
                % (__name__, password, new_password1, new_password2))
        errors = []
        if not self.user:
            errors.append(constants.USER_DOES_NOT_EXIST)
        
        if empty(password):
            errors.append(constants.PASSWORD_BLANK)
        
        if empty(new_password1):
            errors.append(constants.NEW_PASSWORD_BLANK)
        
        if empty(new_password2):
            errors.append(constants.CONFIRM_PASSWORD_BLANK)
        
        if new_password1 != new_password2:
            errors.append(constants.NEW_PASSWORD_MISMATCH)
        
        if len(errors) > 0:
            return False, errors
        
        if not self.user.check_password(password):
            return False, [constants.PASSWORD_INCORRECT]
        
        # Verify password rules
        passed, rules_errors = _check_password_rules(new_password1)
        if not passed:
            return False, rules_errors
        
        # Request is valid. Let's change the password.
        self.user.set_password(new_password1)
        self.user.save()
        
        return True, []
    
    def link_facebook_profile(self, facebook_id, access_token):
        Logger.Info('%s - UserController.link_facebook_profile - started' % __name__)
        Logger.Debug('%s - UserController.link_facebook_profile - started with facebook_id:%s and access_token:%s'
                % (__name__, facebook_id, access_token))
        
        errors = []
        if not self.user:
            errors.append(constants.USER_DOES_NOT_EXIST)
        
        if empty(facebook_id):
            errors.append(constants.FACEBOOK_ID_MISSING)
        
        if empty(access_token):
            errors.append(constants.FACEBOOK_ACCESS_TOKEN_MISSING)
        
        if len(errors) > 0:
            return False, errors
        
        # save Facebook metadata to user profile
        profile = self.user.profile
        profile.linked_accounts = { 'facebook': { 'facebook_id': facebook_id, 'access_token': access_token } }
        profile.save()
        
        Logger.Info('%s - UserController.link_facebook_profile - finished' % __name__)
        return True, []
    
    def link_twitter_profile(self, twitter_id, access_token):
        Logger.Info('%s - UserController.link_twitter_profile - started' % __name__)
        Logger.Debug('%s - UserController.link_twitter_profile - started with facebook_id:%s and access_token:%s'
                % (__name__, facebook_id, access_token))
        
        
        
        Logger.Info('%s - UserController.link_twitter_profile - finished' % __name__)
        return True, []

    def logout_user(self, request):
        Logger.Info('%s - UserController.logout_user - started' % __name__)
        logout(request)
        Logger.Info('%s - UserController.logout_user - finished' % __name__)
        return

    def register_dashboard_template_use(self, dashboard_template_id):
        Logger.Info('%s - UserController.register_dashboard_template_use - started' % __name__)
        Logger.Debug('%s - UserController.register_dashboard_template_use - started with dashboard_template_id:%s' % (__name__, dashboard_template_id))
        user_statistics = UserStatistics.GetForUsername(self.user.username)
        user_statistics.increment_dashboard_template_usage(dashboard_template_id)
        Logger.Info('%s - UserController.register_dashboard_template_use - finished' % __name__)

    def get_user_subscriptions(self):
        Logger.Info('%s - UserController.get_user_subscriptions - started' % __name__)
        user_subscriptions = UserSubscriptions.GetForUsername(self.user.username)
        Logger.Info('%s - UserController.get_user_subscriptions - finished' % __name__)
        return user_subscriptions

    def change_user_subscription(self, new_subscription_id, credit_card=None):
        Logger.Info('%s - UserController.change_user_subscription - started' % __name__)
        Logger.Debug('%s - UserController.change_user_subscription - started with new_subscription_id:%s and credit_card:%s' % (__name__, new_subscription_id, credit_card))
        user_subscriptions = UserSubscriptions.GetForUsername(self.user.username)
        active_subscription = user_subscriptions.get_active_subscription()
        active_subscription_config = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][active_subscription['subscription_id']]
        new_subscription_config = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][new_subscription_id]
        chargify = Chargify(settings.CHARGIFY_SETTINGS['api_key'], settings.CHARGIFY_SETTINGS['subdomain'])
        try:
            if not settings.SUBSCRIPTIONS_SETTINGS['allow_subscription_migrations']:
                raise Exception()
            elif not active_subscription_config['chargify_config']: #Moving from free to paid
                result = chargify.subscriptions.create(data={
                    'subscription':{
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
                    }
                })
                Logger.Debug('%s' % result)
                user_subscriptions.subscription_changed(
                    new_subscription_id,
                    active_subscription['extensions'],
                    { 'chargify':{'subscription_created':result}}
                )
            elif not new_subscription_config['chargify_config']: #Moving to free from paid
                chargify_subscription_id = user_subscriptions.get_active_subscription_id()
                result = chargify.subscriptions.delete(subscription_id=chargify_subscription_id)
                active_subscription['extensions']['chargify']['subscription_deleted'] = result
                user_subscriptions.subscription_changed(
                    new_subscription_id,
                    active_subscription['extensions'],
                    {}
                )
            else: #Migrating up or down subscriptions
                chargify_subscription_id = user_subscriptions.get_active_subscription_id()
                result = chargify.subscriptions.migrations.create(
                    subscription_id=chargify_subscription_id,
                    data={ 'product_id':new_subscription_config['chargify_config']['product_id'] }
                )
                active_subscription['extensions']['chargify']['subscription_migrated_from'] = result
                user_subscriptions.subscription_changed(
                    new_subscription_id,
                    active_subscription['extensions'],
                        { 'chargify':{'subscription_migrated_to':result}}
                )
            Logger.Info('%s - UserController.change_user_subscription - finished' % __name__)
            return True
        except Exception, e:
            Logger.Error('%s' % e)
            Logger.Info('%s - UserController.change_user_subscription - finished' % __name__)
            return False

    def subscription_migration_direction(self, new_subscription_id):
        Logger.Info('%s - UserController.subscription_migration_direction - started' % __name__)
        Logger.Debug('%s - UserController.subscription_migration_direction - started with new_subscription_id:%s' % (__name__, new_subscription_id))
        current_active_subscription_id = self.get_user_subscriptions()['active_subscription']
        found_current_subscription = False
        for subscription_id in settings.SUBSCRIPTIONS_SETTINGS['subscriptions'].keys():
            if subscription_id == current_active_subscription_id:
                found_current_subscription = True
            if subscription_id == new_subscription_id:
                Logger.Info('%s - UserController.subscription_migration_direction - finished' % __name__)
                return 'upgrade' if found_current_subscription else 'downgrade'
        Logger.Info('%s - UserController.subscription_migration_direction - finished' % __name__)
        return None

    def need_to_ask_for_credit_card_details(self):
        Logger.Info('%s - UserController.need_to_ask_for_credit_card_details - started' % __name__)
        active_subscription_id = self.get_user_subscriptions()['active_subscription']
        ask_for_credit_card_details = bool(active_subscription_id == 'subscription_type_1')
        Logger.Info('%s - UserController.need_to_ask_for_credit_card_details - finished' % __name__)
        return ask_for_credit_card_details

    def maximum_number_of_saved_dashboards_allowed_by_subscription(self):
        Logger.Info('%s - UserController.maximum_number_of_saved_dashboards_allowed_by_subscription - started' % __name__)
        active_subscription_id = self.get_user_subscriptions()['active_subscription']
        active_subscription_config = settings.SUBSCRIPTIONS_SETTINGS['subscriptions'][active_subscription_id]
        number_of_saved_dashboards = active_subscription_config['config']['number_of_saved_dashboards']
        Logger.Info('%s - UserController.maximum_number_of_saved_dashboards_allowed_by_subscription - finished' % __name__)
        return number_of_saved_dashboards


def _check_password_rules(new_password):
    """
    Verify that the given password matches the rules for this site.
    
    """
    
    if len(new_password) < 6:
        return False, [constants.PASSWORD_TOO_SHORT]
    
    return True, []




