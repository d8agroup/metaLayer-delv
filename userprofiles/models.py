from minimongo import Model, Index
import time

class UserStatistics(Model):
    class Meta:
        database = 'ml_dashboard'
        collection = 'user_statistics'
        indices = ( Index('username'), )

    @classmethod
    def GetForUsername(cls, username):
        user_statistics = UserStatistics.collection.find_one({'username':username})
        if not user_statistics:
            user_statistics = UserStatistics({
                'username':username,
                'dashboard_template_usage':{}
            })
        return user_statistics


    def increment_dashboard_template_usage(self, dashboard_template_id):
        if not dashboard_template_id in self['dashboard_template_usage'].keys():
            self['dashboard_template_usage'][dashboard_template_id] = {
                'count':0,
                'last_used':0
            }
        self['dashboard_template_usage'][dashboard_template_id]['count'] += 1
        self['dashboard_template_usage'][dashboard_template_id]['last_used'] = time.time()