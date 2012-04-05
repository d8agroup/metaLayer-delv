from django.conf import settings
import time
from metalayercore.dashboards.controllers import DashboardsController
from logger import Logger
from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import DictField, ListField

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    linked_accounts = DictField()
    api_keys = ListField()
    registration_code = models.TextField()
    registration_status = models.TextField()
    contact_options = DictField()
    followers = ListField() # Accounts that are following the user
    accounts_followed_by_user = ListField() # Accounts that the user is following.
    
    def is_following(self, user):
        """
        Returns true if the current user is following a user with the specified id.
        
        """
        for id in self.accounts_followed_by_user:
            if id == user.id:
                return True
                
        return False

    def community_values(self):
        dc = DashboardsController(self.user)
        return {
            'number_of_insights':len(dc.get_saved_dashboards())
        }
    
    def profile_image(self):
        """
        Returns the URL of the user's profile image.
        
        Note that we do not include the protocol in the profile image URL so that 
        the caller can determine whether to use 'http' or 'https'.
        
        """
        
        if 'facebook' in self.linked_accounts and 'facebook_id' in self.linked_accounts['facebook']:
            return 'graph.facebook.com/%s/picture?type=normal' % self.linked_accounts['facebook']['facebook_id']
        
        if 'twitter' in self.linked_accounts and 'screen_name' in self.linked_accounts['twitter']:
            return 'api.twitter.com/1/users/profile_image/%s?type=large' % self.linked_accounts['twitter']['screen_name']
        
        return None
    
    def email_opt_in(self):
        """
        Returns whether or not the user has opted to receive e-mail campaigns.
        
        """
        
        if 'email' in self.contact_options and 'opt_in_status' in self.contact_options['email'] \
                and self.contact_options['email']['opt_in_status'] == True:
            return True
        
        return False
    
    def linked_via_facebook(self):
        """
        Returns true if the user has linked their metaLayer account with their Facebook profile.
        
        """
        return 'facebook' in self.linked_accounts and 'facebook_id' in self.linked_accounts['facebook']
    
    def linked_via_twitter(self):
        """
        Returns true if the user has linked their metaLayer account with their Twitter profile.
        
        """
        return 'twitter' in self.linked_accounts and 'screen_name' in self.linked_accounts['twitter']


    def get_registration_type(self):
        if self.registration_code:
            for key in settings.REGISTRATION_CODES['codes']:
                if self.registration_code in settings.REGISTRATION_CODES['codes'][key]:
                    return key
            return 'UNRECOGNISED'
        return None

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class UserStatistics(models.Model):
    username = models.TextField()
    dashboard_template_usage = DictField()

    @classmethod
    def GetForUsername(cls, username):
        Logger.Info('%s - UserStatistics.GetForUsername - started' % __name__)
        Logger.Debug('%s - UserStatistics.GetForUsername - started with username:%s' % (__name__, username))
        try:
            user_statistics = UserStatistics.objects.get(username=username)
        except UserStatistics.DoesNotExist:
            user_statistics = UserStatistics(username=username)
            user_statistics.save()
        Logger.Info('%s - UserStatistics.GetForUsername - finished' % __name__)
        return user_statistics


    def increment_dashboard_template_usage(self, dashboard_template_id):
        Logger.Info('%s - UserStatistics.increment_dashboard_template_usage - started' % __name__)
        Logger.Debug('%s - UserStatistics.increment_dashboard_template_usage - started with dashboard_template_id:%s' % (__name__, dashboard_template_id))
        if not dashboard_template_id in self.dashboard_template_usage.keys():
            self.dashboard_template_usage[dashboard_template_id] = {
                'count':0,
                'last_used':0
            }
        self.dashboard_template_usage[dashboard_template_id]['count'] += 1
        self.dashboard_template_usage[dashboard_template_id]['last_used'] = time.time()
        self.save()
        Logger.Info('%s - UserStatistics.increment_dashboard_template_usage - finished' % __name__)

class UserSubscriptions(models.Model):
    username = models.TextField()
    active_subscription = models.TextField()
    subscription_history = ListField()

    @classmethod
    def InitForUsername(cls, username):
        Logger.Info('%s - UserSubscriptions.InitForUsername - started' % __name__)
        Logger.Info('%s - UserSubscriptions.InitForUsername - started with username:%s' % (__name__, username))
        user_subscriptions = UserSubscriptions(
            username=username,
            active_subscription='subscription_type_1',
            subscription_history=[
                {
                    'subscription_id':'subscription_type_1',
                    'start_time':time.time(),
                    'extensions':{'note':'Initial Signup'}
                }
            ]
        )
        user_subscriptions.save()
        Logger.Info('%s - UserSubscriptions.InitForUsername - finished' % __name__)
        return user_subscriptions

    @classmethod
    def GetForUsername(cls, username):
        Logger.Info('%s - UserSubscriptions.GetForUsername - started' % __name__)
        Logger.Debug('%s - UserSubscriptions.GetForUsername - started with username:%s' % (__name__, username))
        try:
            user_subscriptions = UserSubscriptions.objects.get(username=username)
        except UserSubscriptions.DoesNotExist:
            user_subscriptions = UserSubscriptions.InitForUsername(username)
        Logger.Info('%s - UserSubscriptions.GetForUsername - finished' % __name__)
        return user_subscriptions

    def get_active_subscription(self):
        Logger.Info('%s - UserSubscriptions.get_active_subscription - started' % __name__)
        return_value = None
        for subscription in self.subscription_history:
            if 'end_time' not in subscription:
                return_value = subscription
        Logger.Info('%s - UserSubscriptions.get_active_subscription - finished' % __name__)
        return return_value

    def get_active_subscription_id(self):
        Logger.Info('%s - UserSubscriptions.get_active_subscription_id - started' % __name__)
        subscription = self.get_active_subscription()
        subscription_id = None
        for key in ['subscription_created', 'subscription_migrated_to']:
            if key in subscription['extensions']['chargify']:
                subscription_id = subscription['extensions']['chargify'][key]['subscription']['id']
        Logger.Info('%s - UserSubscriptions.get_active_subscription_id - finished' % __name__)
        return subscription_id

    def subscription_changed(self, new_subscription_id, old_subscription_extension=None, new_subscription_extensions=None):
        Logger.Info('%s - UserSubscriptions.subscription_changed - started' % __name__)
        Logger.Debug('%s - UserSubscriptions.subscription_changed - started with new_subscription_id:%s old_subscription_extension:%s and new_subscription_extensions:%s' % (__name__, new_subscription_id, old_subscription_extension, new_subscription_extensions))
        self.active_subscription = new_subscription_id
        for subscription in self.subscription_history:
            if 'end_time' not in subscription:
                subscription['end_time'] = time.time()
                subscription['extensions'] = old_subscription_extension
        self.subscription_history.append({
            'subscription_id':new_subscription_id,
            'start_time':time.time(),
            'extensions':new_subscription_extensions
        })
        self.save()
        Logger.Info('%s - UserSubscriptions.subscription_changed - finished' % __name__)
