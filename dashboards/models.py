from bson.objectid import ObjectId
from datetime import datetime
from django.conf import settings
from minimongo import Model, Index
import time
from logger import Logger
from utils import get_pretty_date

class Dashboard(Model):
    class Meta:
        host = settings.DATABASES['default']['HOST']
        port = settings.DATABASES['default']['PORT']
        database = settings.DATABASES['default']['NAME']
        collection = 'dashboards_dashboards'
        indices = ( Index('username'), )

    @classmethod
    def Create(cls, user, template=None):
        Logger.Info('%s - Dashboard.Create - started' % __name__)
        Logger.Debug('%s - Dashboard.Create - started with user:%s and template:%s' % (__name__, user, template))
        dashboard = Dashboard({
            'username': user.username,
            'created': time.time(),
            'accessed':1,
            'last_saved_pretty':'Not yet used',
            'collections':template['collections'] if template else {},
            'widgets':template['widgets'] if template else {},
            'active':True,
            'name':template['name']
        })
        for collection in dashboard['collections']:
            collection['id'] = '%s' % ObjectId()
        dashboard.save()
        dashboard['id'] = '%s' % dashboard._id
        dashboard.save()
        Logger.Info('%s - Dashboard.Create - finished' % __name__)
        return dashboard

    @classmethod
    def AllForUser(cls, user):
        Logger.Info('%s - Dashboard.AllForUser - started' % __name__)
        Logger.Debug('%s - Dashboard.AllForUser - started with user:%s' % (__name__, user))
        dashboards = Dashboard.collection.find({'username': user.username})
        for dashboard in dashboards:
            should_remove = True
            for collection in dashboard['collections']:
                if 'data_points' in collection:
                    should_remove = False
            if should_remove:
                dashboard.remove()
        dashboards = Dashboard.collection.find({'username': user.username})
        dashboards = [d for d in dashboards if d['active']]
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        for dashboard in dashboards:
            dashboard['last_saved_pretty'] = dashboard._pretty_date(dashboard['last_saved'])
        Logger.Info('%s - Dashboard.AllForUser - finished' % __name__)
        return dashboards

    @classmethod
    def Load(cls, id, increment_load_count = False):
        Logger.Info('%s - Dashboard.Load - started' % __name__)
        Logger.Debug('%s - Dashboard.Load - started with is:%s and increment_load_count:%s' % (__name__, id, increment_load_count))
        dashboard = Dashboard.collection.find_one({'_id':ObjectId(id)})
        dashboard['last_saved_pretty'] = dashboard._pretty_date(dashboard['last_saved'])
        dashboard['created_pretty'] = dashboard._pretty_date(dashboard['created'])
        if dashboard and increment_load_count:
            dashboard['accessed'] += 1
            dashboard.save()
        Logger.Info('%s - Dashboard.Load - finished' % __name__)
        return dashboard

    @classmethod
    def Trending(cls, count):
        Logger.Info('%s - Dashboard.Trending - started' % __name__)
        Logger.Debug('%s - Dashboard.Trending - started with count:%s' % (__name__, count))
        dashboards = Dashboard.collection.find()
        dashboards = [d for d in dashboards if d['active']]
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        dashboards = dashboards[:int(count)]
        for dashboard in dashboards:
            dashboard['last_saved_pretty'] = dashboard._pretty_date(dashboard['last_saved'])
        Logger.Info('%s - Dashboard.Trending - finished' % __name__)
        return dashboards

    @classmethod
    def Top(cls, count):
        Logger.Info('%s - Dashboard.Top - started' % __name__)
        Logger.Debug('%s - Dashboard.Top - started with count:%s' % (__name__, count))
        dashboards = Dashboard.collection.find()
        dashboards = [d for d in dashboards if d['active']]
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        dashboards = dashboards[:int(count)]
        for dashboard in dashboards:
            dashboard['last_saved_pretty'] = dashboard._pretty_date(dashboard['last_saved'])
        Logger.Info('%s - Dashboard.Top - finished' % __name__)
        return dashboards

    @classmethod
    def Recent(cls, count):
        Logger.Info('%s - Dashboard.Recent - started' % __name__)
        Logger.Debug('%s - Dashboard.Recent - started with count:%s' % (__name__, count))
        dashboards = Dashboard.collection.find()
        dashboards = [d for d in dashboards if d['active']]
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        dashboards = dashboards[:int(count)]
        for dashboard in dashboards:
            dashboard['last_saved_pretty'] = dashboard._pretty_date(dashboard['last_saved'])
        Logger.Info('%s - Dashboard.Recent - finished' % __name__)
        return dashboards


    def save(self, *args, **kwargs):
        self['last_saved'] = time.time()
        return super(Dashboard, self).save(*args, **kwargs)

    def _pretty_date(self, time=False):
        return get_pretty_date(time)

class DashboardTemplate(Model):
    class Meta:
        host = settings.DATABASES['default']['HOST']
        port = settings.DATABASES['default']['PORT']
        database = settings.DATABASES['default']['NAME']
        collection = 'dashboard_templates'
        #indices = ( Index(''), )

    @classmethod
    def AllForUser(cls, user):
        Logger.Info('%s - DashboardTemplate.AllForUser - started' % __name__)
        Logger.Debug('%s - DashboardTemplate.AllForUser - started with user:%s' % (__name__, user))
        #TODO this is a mock up
        Logger.Info('%s - DashboardTemplate.AllForUser - finished' % __name__)
        return [
            {
                'id':'g8f7h76j6hj5h45k46hjkhj87',
                'display_name':'Empty Dashboard',
                'description':'A blank dashboard ready for anything!',
                'image':'dashboard_template_images/empty_dashboard.gif',
                'collections':[{}, {}],
                'widgets':{'something':{}},
                'name':'Untitled Insight'
            }
        ]

    @classmethod
    def GetTemplateById(cls, id):
        Logger.Info('%s - DashboardTemplate.GetTemplateById - started' % __name__)
        Logger.Debug('%s - DashboardTemplate.GetTemplateById - started with id:%s' % (__name__, id))
        #TODO this is a mock up
        Logger.Info('%s - DashboardTemplate.GetTemplateById - finished' % __name__)
        return DashboardTemplate.AllForUser(None)[0]