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
            'created': time.time()
        })
        dashboard.save()
        return dashboard

    @classmethod
    def AllForUser(cls, user):
        dashboards = Dashboard.collection.find({'username': user.username})
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        return dashboards

    def save(self, *args, **kwargs):
        self['last_saved'] = time.time()
        return super(Dashboard, self).save(*args, **kwargs)
