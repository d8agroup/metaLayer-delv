from bson.objectid import ObjectId
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
            'collections':template['collections'] if template else {},
            'widgets':template['widgets'] if template else {}
        })
        dashboard.save()
        dashboard['id'] = '%s' % dashboard._id
        dashboard.save()
        return dashboard

    @classmethod
    def AllForUser(cls, user):
        dashboards = Dashboard.collection.find({'username': user.username})
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        return dashboards

    @classmethod
    def Load(cls, id, increment_load_count = False):
        dashboard = Dashboard.collection.find_one({'_id':ObjectId(id)})
        if dashboard and increment_load_count:
            dashboard['accessed'] += 1
            dashboard.save()
        return dashboard

    def save(self, *args, **kwargs):
        self['last_saved'] = time.time()
        return super(Dashboard, self).save(*args, **kwargs)

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