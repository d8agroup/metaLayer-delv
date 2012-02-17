from django.conf import settings
from minimongo import Model, Index
import time
from dashboards.controllers import DashboardsController
from logger import Logger
from django.db import models
from django.contrib.auth.models import User
from djangotoolbox.fields import DictField, ListField

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    linked_accounts = DictField()
    api_keys = ListField()

    def community_values(self):
        dc = DashboardsController(self.user)
        return {
            'number_of_insights':len(dc.get_saved_dashboards())
        }

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class UserStatistics(Model):
    class Meta:
        host = settings.DATABASES['default']['HOST']
        port = settings.DATABASES['default']['PORT']
        database = settings.DATABASES['default']['NAME']
        collection = 'userprofiles_userstatistics'
        indices = ( Index('username'), )

    @classmethod
    def GetForUsername(cls, username):
        Logger.Info('%s - UserStatistics.GetForUsername - started' % __name__)
        Logger.Debug('%s - UserStatistics.GetForUsername - started with username:%s' % (__name__, username))
        user_statistics = UserStatistics.collection.find_one({'username':username})
        if not user_statistics:
            user_statistics = UserStatistics({
                'username':username,
                'dashboard_template_usage':{}
            })
        user_statistics.save()
        Logger.Info('%s - UserStatistics.GetForUsername - finished' % __name__)
        return user_statistics


    def increment_dashboard_template_usage(self, dashboard_template_id):
        Logger.Info('%s - UserStatistics.increment_dashboard_template_usage - started' % __name__)
        Logger.Debug('%s - UserStatistics.increment_dashboard_template_usage - started with dashboard_template_id:%s' % (__name__, dashboard_template_id))
        if not dashboard_template_id in self['dashboard_template_usage'].keys():
            self['dashboard_template_usage'][dashboard_template_id] = {
                'count':0,
                'last_used':0
            }
        self['dashboard_template_usage'][dashboard_template_id]['count'] += 1
        self['dashboard_template_usage'][dashboard_template_id]['last_used'] = time.time()
        self.save()
        Logger.Info('%s - UserStatistics.increment_dashboard_template_usage - finished' % __name__)

class UserSubscriptions(Model):
    class Meta:
        host = settings.DATABASES['default']['HOST']
        port = settings.DATABASES['default']['PORT']
        database = settings.DATABASES['default']['NAME']
        collection = 'userprofiles_usersubscriptions'
        indices = ( Index('username'), )

    @classmethod
    def InitForUsername(cls, username):
        Logger.Info('%s - UserSubscriptions.InitForUsername - started' % __name__)
        Logger.Info('%s - UserSubscriptions.InitForUsername - started with username:%s' % (__name__, username))
        user_subscriptions = UserSubscriptions({
            'username':username,
            'active_subscription':'subscription_type_1',
            'subscription_history':[
                {
                    'subscription_id':'subscription_type_1',
                    'start_time':time.time(),
                    'extensions':{
                        'note':'Initial Signup'
                    }
                }
            ]
        })
        user_subscriptions.save()
        Logger.Info('%s - UserSubscriptions.InitForUsername - finished' % __name__)
        return user_subscriptions

    @classmethod
    def GetForUsername(cls, username):
        Logger.Info('%s - UserSubscriptions.GetForUsername - started' % __name__)
        Logger.Debug('%s - UserSubscriptions.GetForUsername - started with username:%s' % (__name__, username))
        user_subscriptions = UserSubscriptions.collection.find_one({'username':username})
        if not user_subscriptions:
            user_subscriptions = UserSubscriptions.InitForUsername(username)
        Logger.Info('%s - UserSubscriptions.GetForUsername - finished' % __name__)
        return user_subscriptions

    def get_active_subscription(self):
        Logger.Info('%s - UserSubscriptions.get_active_subscription - started' % __name__)
        return_value = None
        for subscription in self['subscription_history']:
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
        self['active_subscription'] = new_subscription_id
        for subscription in self['subscription_history']:
            if 'end_time' not in subscription:
                subscription['end_time'] = time.time()
                subscription['extensions'] = old_subscription_extension
        self['subscription_history'].append({
            'subscription_id':new_subscription_id,
            'start_time':time.time(),
            'extensions':new_subscription_extensions
        })
        self.save()
        Logger.Info('%s - UserSubscriptions.subscription_changed - finished' % __name__)
