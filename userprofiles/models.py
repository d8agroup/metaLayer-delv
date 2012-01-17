from minimongo import Model, Index
import time

class UserStatistics(Model):
    class Meta:
        database = 'ml_dashboard'
        collection = 'userprofiles_userstatistics'
        indices = ( Index('username'), )

    @classmethod
    def GetForUsername(cls, username):
        user_statistics = UserStatistics.collection.find_one({'username':username})
        if not user_statistics:
            user_statistics = UserStatistics({
                'username':username,
                'dashboard_template_usage':{}
            })
        user_statistics.save()
        return user_statistics


    def increment_dashboard_template_usage(self, dashboard_template_id):
        if not dashboard_template_id in self['dashboard_template_usage'].keys():
            self['dashboard_template_usage'][dashboard_template_id] = {
                'count':0,
                'last_used':0
            }
        self['dashboard_template_usage'][dashboard_template_id]['count'] += 1
        self['dashboard_template_usage'][dashboard_template_id]['last_used'] = time.time()
        self.save()

class UserSubscriptions(Model):
    class Meta:
        database = 'ml_dashboard'
        collections = 'userprofiles_usersubscriptions'
        indices = ( Index('username'), )

    @classmethod
    def InitForUsername(cls, username):
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
        return user_subscriptions

    @classmethod
    def GetForUsername(cls, username):
        user_subscriptions = UserSubscriptions.collection.find_one({'username':username})
        if not user_subscriptions:
            user_subscriptions = UserSubscriptions.InitForUsername(username)
        return user_subscriptions

    def get_active_subscription(self):
        for subscription in self['subscription_history']:
            if 'end_time' not in subscription:
                return subscription
        return None

    def get_active_subscription_id(self):
        subscription = self.get_active_subscription()
        for key in ['subscription_created', 'subscription_migrated_to']:
            if key in subscription['extensions']['chargify']:
                return subscription['extensions']['chargify'][key]['subscription']['id']
        return None

    def subscription_changed(self, new_subscription_id, old_subscription_extension=None, new_subscription_extensions=None):
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
