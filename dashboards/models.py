from bson.objectid import ObjectId
from minimongo import Model, Index
import time

class Dashboard(Model):
    class Meta:
        database = 'ml_dashboard'
        collection = 'dashboards'
        #indices = ( Index(''), )

    @classmethod
    def Create(cls, user):
        dashboard = Dashboard({
            'username': user.username,
            'created': time.time(),
            'accessed':1
        })
        dashboard.save()
        return dashboard

    @classmethod
    def AllForUser(cls, user):
        dashboards = Dashboard.collection.find({'username': user.username})
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        return dashboards

    @classmethod
    def Load(cls, id):
        dashboard = Dashboard.collection.find_one({'_id':ObjectId(id)})
        if dashboard:
            dashboard['accessed'] += 1
            dashboard.save()
        return dashboard

    def save(self, *args, **kwargs):
        self['last_saved'] = time.time()
        return super(Dashboard, self).save(*args, **kwargs)
