from bson.objectid import ObjectId
from datetime import datetime
from minimongo import Model, Index
import time

class Dashboard(Model):
    class Meta:
        database = 'ml_dashboard'
        collection = 'dashboards_dashboards'
        #indices = ( Index(''), )

    @classmethod
    def Create(cls, user, template=None):
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
        return dashboard

    @classmethod
    def AllForUser(cls, user):
        dashboards = Dashboard.collection.find({'username': user.username})
        dashboards = [d for d in dashboards if d['active']]
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        return dashboards

    @classmethod
    def Load(cls, id, increment_load_count = False):
        dashboard = Dashboard.collection.find_one({'_id':ObjectId(id)})
        dashboard['last_saved_pretty'] = dashboard._pretty_date(dashboard['last_saved'])
        if dashboard and increment_load_count:
            dashboard['accessed'] += 1
            dashboard.save()
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
        now = datetime.now()
        if type(time) is int:
            diff = now - datetime.fromtimestamp(time)
        elif type(time) is float:
            diff = now - datetime.fromtimestamp(int(time))
        elif isinstance(time,datetime):
            diff = now - time
        elif not time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(second_diff) + " seconds ago"
            if second_diff < 120:
                return  "a minute ago"
            if second_diff < 3600:
                return str( second_diff / 60 ) + " minutes ago"
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
        return str(day_diff/365) + " years ago"


class DashboardTemplate(Model):
    class Meta:
        database = 'ml_dashboard'
        collection = 'dashboard_templates'
        #indices = ( Index(''), )

    @classmethod
    def AllForUser(cls, user):
        #TODO this is a mock up
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
        #TODO this is a mock up
        return DashboardTemplate.AllForUser(None)[0]