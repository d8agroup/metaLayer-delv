import random
import string
from bson.objectid import ObjectId
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
    def Create(cls, user, template=None, template_is_dashboard=False):
        Logger.Info('%s - Dashboard.Create - started' % __name__)
        Logger.Debug('%s - Dashboard.Create - started with user:%s and template:%s' % (__name__, user, template))
        dashboard = Dashboard({
            'username': user.username,
            'created': time.time(),
            'accessed':1,
            'last_saved_pretty':'Not yet used',
            'last_saved':time.time(),
            'collections':template['collections'] if template else {},
            'widgets':template['widgets'] if template else {},
            'active':False,
            'deleted':False,
            'name':template['name'],
            'config':{}
        })
        dashboard._ensure_community_defaults()
        for collection in dashboard['collections']:
            collection['id'] = '%s' % ObjectId()
        if template_is_dashboard:
            dashboard['community']['parent'] = template['id']
        dashboard.save()
        dashboard['id'] = '%s' % dashboard._id
        dashboard['short_url'] = DashboardShortUrl.Create(dashboard['id'])
        dashboard.save()
        Logger.Info('%s - Dashboard.Create - finished' % __name__)
        return dashboard

    @classmethod
    def AllForUser(cls, user):
        Logger.Info('%s - Dashboard.AllForUser - started' % __name__)
        Logger.Debug('%s - Dashboard.AllForUser - started with user:%s' % (__name__, user))
        dashboards = Dashboard.collection.find({'username': user.username})
        dashboards = [d for d in dashboards if d['active'] == True and d['deleted'] == False]
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
        if dashboard:
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
        dashboards = [d for d in dashboards if d['active'] and not d['deleted']]
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
        dashboards = [d for d in dashboards if d['active'] and not d['deleted']]
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
        dashboards = [d for d in dashboards if d['active'] and not d['deleted']]
        dashboards = sorted(dashboards, key=lambda dashboard: dashboard['last_saved'], reverse=True)
        dashboards = dashboards[:int(count)]
        for dashboard in dashboards:
            dashboard['last_saved_pretty'] = dashboard._pretty_date(dashboard['last_saved'])
        Logger.Info('%s - Dashboard.Recent - finished' % __name__)
        return dashboards

    def delete(self):
        self['deleted'] = True
        self['active'] = False
        self['config']['live'] = False
        self.save()

    def save(self, *args, **kwargs):
        self['active'] = True if sum([len(c['data_points']) for c in self['collections'] if 'data_points' in c]) else False
        return super(Dashboard, self).save(*args, **kwargs)

    def change_community_value(self, value_type, value_change):
        self['community'][value_type] += value_change
        self.save()

    def has_visualizations(self):
        for collection in [c for c in self['collections'] if c['data_points']]:
            if collection['visualizations']:
                return True
        return False

    def visualization_for_image(self):
        for visualization_type in settings.VISUALIZATIONS_CONFIG['visualization_display_hierarchy']:
            for collection in [c for c in self['collections'] if c['data_points']]:
                for visualization in collection['visualizations']:
                    if visualization['name'] == visualization_type and visualization['snapshot']:
                        return visualization['snapshot']
        return None

    def single_data_point_for_image(self):
        for collection in self['collections']:
            for data_point in collection['data_points']:
                return data_point['image_medium']
        return 'http://%s/80/80/no_image.png' % settings.SITE_HOST

    def four_data_points_for_image(self):
        data_points = []
        for collection in self['collections']:
            for data_point in collection['data_points']:
                data_points.append(data_point['image_medium'])
        return data_points[:4]

    def tz(self):
        start_times = [c['search_filters']['time'].split('%20TO%20')[0].strip('[') for c in self['collections'] if 'time' in c['search_filters']]
        end_times = [c['search_filters']['time'].split('%20TO%20')[1].strip(']') for c in self['collections'] if 'time' in c['search_filters']]
        start_time = self._pretty_date(min([int(t) for t in start_times])) if not '*' in start_times else 'Historic'
        end_time = self._pretty_date(max([int(t) for t in end_times])) if not '*' in end_times else 'Now'
        if start_time == end_time:
            return start_time
        return '%s to %s' % (start_time, end_time)

    def _pretty_date(self, time=False):
        return get_pretty_date(time)

    def _ensure_community_defaults(self):
        if not 'community' in self:
            self['community'] = {
                'views':0,
                'remixes':0,
                'challenges':0,
                'comments':0
            }

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

class DashboardShortUrl(Model):
    class Meta:
        host = settings.DATABASES['default']['HOST']
        port = settings.DATABASES['default']['PORT']
        database = settings.DATABASES['default']['NAME']
        collection = 'dashboards_shorturl'
        indices = ( Index('url_identifier'), )

    @classmethod
    def Create(cls, dashboard_id):
        def generate_random_string():
            return "".join( [random.choice(string.letters[:26]) for i in xrange(12)] )
        Logger.Info('%s - ShortUrl.Create - started' % __name__)
        Logger.Debug('%s - ShortUrl.Create - started with dashboard_id:%s ' % (__name__, dashboard_id))
        url_identifier = generate_random_string()
        while DashboardShortUrl.collection.find_one({'url_identifier':url_identifier}):
            url_identifier = generate_random_string()
        short_url = DashboardShortUrl({
            'url_identifier':url_identifier,
            'dashboard_id':dashboard_id
        })
        short_url.save()
        Logger.Info('%s - ShortUrl.Create - finished' % __name__)
        return short_url

    @classmethod
    def Load(cls, url_identifier):
        Logger.Info('%s - ShortUrl.Load - started' % __name__)
        Logger.Debug('%s - ShortUrl.Load - started with url_identifier:%s' % (__name__, url_identifier))
        short_url = DashboardShortUrl.collection.find_one({'url_identifier':url_identifier})
        Logger.Info('%s - ShortUrl.Load - finished' % __name__)
        return short_url

    @classmethod
    def Delete(cls, dashboard_id):
        Logger.Info('%s - ShortUrl.Delete - started' % __name__)
        Logger.Info('%s - ShortUrl.Delete - started with dashboard_id:%s' % (__name__, dashboard_id))
        short_url = DashboardShortUrl.collection.find_one({
            'dashboard_id':dashboard_id,
        })
        if short_url:
            short_url.remove()
        Logger.Info('%s - ShortUrl.Delete - finished' % __name__)