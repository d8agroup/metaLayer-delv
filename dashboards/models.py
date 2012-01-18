from bson.objectid import ObjectId
from datetime import datetime
from minimongo import Model, Index
import time
from logger import Logger

class Dashboard(Model):
    class Meta:
        database = 'ml_dashboard'
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
            'active':True
        })
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
        dashboards = [d for d in dashboards if d['active']]
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        Logger.Info('%s - Dashboard.AllForUser - finished' % __name__)
        return dashboards

    @classmethod
    def Load(cls, id, increment_load_count = False):
        Logger.Info('%s - Dashboard.Load - started' % __name__)
        Logger.Debug('%s - Dashboard.Load - started with is:%s and increment_load_count:%s' % (__name__, id, increment_load_count))
        dashboard = Dashboard.collection.find_one({'_id':ObjectId(id)})
        dashboard['last_saved_pretty'] = dashboard._pretty_date(dashboard['last_saved'])
        if dashboard and increment_load_count:
            dashboard['accessed'] += 1
            dashboard.save()
        Logger.Info('%s - Dashboard.Load - finished' % __name__)
        return dashboard

    def save(self, *args, **kwargs):
        self['last_saved'] = time.time()
        return super(Dashboard, self).save(*args, **kwargs)

    def _pretty_date(self, time=False):
        """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
        Logger.Info('%s - Dashboard._pretty_date - started' % __name__)
        Logger.Debug('%s - Dashboard._pretty_date - started with time:%s' % (__name__, time))
        now = datetime.now()
        if type(time) is int:
            diff = now - datetime.fromtimestamp('%i' % time)
        elif type(time) is float:
            diff = now - datetime.fromtimestamp('%i' % int(time))
        elif isinstance(time,datetime):
            diff = now - time
        else:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if not day_diff:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(second_diff) + " seconds ago"
            if second_diff < 120:
                return  "a minute ago"
            if second_diff < 3600:
                return str( second_diff / 60 ) + "%f minutes ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str( second_diff / 3600 ) + " hours ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(day_diff) + " days ago"
        if day_diff < 31:
            return str(day_diff/7) + " weeks ago"
        if day_diff < 365:
            return str(day_diff/30) + " months ago"
        return_string = str(day_diff / 365) + " years ago"
        Logger.Info('%s - Dashboard._pretty_date - finished' % __name__)
        return return_string


class DashboardTemplate(Model):
    class Meta:
        database = 'ml_dashboard'
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
                'collections':[{}, {}, {}, {}],
                'widgets':{'something':{}},
            }
        ]

    @classmethod
    def GetTemplateById(cls, id):
        Logger.Info('%s - DashboardTemplate.GetTemplateById - started' % __name__)
        Logger.Debug('%s - DashboardTemplate.GetTemplateById - started with id:%s' % (__name__, id))
        #TODO this is a mock up
        Logger.Info('%s - DashboardTemplate.GetTemplateById - finished' % __name__)
        return DashboardTemplate.AllForUser(None)[0]