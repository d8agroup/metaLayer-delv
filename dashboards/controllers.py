from dashboards.models import Dashboard, DashboardTemplate
from logger import Logger

class DashboardsController(object):
    def __init__(self, user):
        Logger.Info('%s - DashboardsController - started' % __name__)
        Logger.Debug('%s - DashboardsController - started with user:%s' % (__name__, user))
        self.user = user
        Logger.Info('%s - DashboardsController - finished' % __name__)

    @classmethod
    def GetDashboardById(cls, id):
        Logger.Info('%s - DashboardsController.GetDashboardById - started' % __name__)
        Logger.Debug('%s - DashboardsController.GetDashboardById - started with id:%s' % (__name__, id))
        dashboard = Dashboard.Load(id, True)
        Logger.Info('%s - DashboardsController.GetDashboardById - finished' % __name__)
        return dashboard

    def get_saved_dashboards(self):
        Logger.Info('%s - get_saved_dashboards - started' % __name__)
        saved_dashboards = Dashboard.AllForUser(self.user)
        Logger.Info('%s - get_saved_dashboards - finished' % __name__)
        return saved_dashboards

    def get_dashboard_by_id(self, id):
        Logger.Info('%s - get_dashboard_by_id - started' % __name__)
        Logger.Debug('%s - get_dashboard_by_id - started with id:%s' % (__name__, id))
        dashboard = DashboardsController.GetDashboardById(id)
        Logger.Info('%s - get_dashboard_by_id - finished' % __name__)
        return dashboard

    def delete_dashboard_by_id(self, id):
        Logger.Info('%s - delete_dashboard_by_id - started' % __name__)
        Logger.Debug('%s - delete_dashboard_by_id - started with id:%s' % (__name__, id))
        dashboard = Dashboard.Load(id)
        dashboard['active'] = False
        dashboard.save()
        Logger.Info('%s - delete_dashboard_by_id - finished' % __name__)

    def get_dashboard_templates(self):
        Logger.Info('%s - get_dashboard_templates - started' % __name__)
        dashboard_templates = DashboardTemplate.AllForUser(self.user)
        Logger.Info('%s - get_dashboard_templates - finished' % __name__)
        return dashboard_templates

    def create_new_dashboard_from_template(self, template_id):
        Logger.Info('%s - create_new_dashboard_from_template - started' % __name__)
        Logger.Debug('%s - create_new_dashboard_from_template - started with template_id:%s' % (__name__, template_id))
        template = DashboardTemplate.GetTemplateById(template_id)
        dashboard = Dashboard.Create(self.user, template)
        Logger.Info('%s - get_dashboard_templates - finished' % __name__)
        return dashboard

    def update_dashboard(self, dashboard):
        Logger.Info('%s - update_dashboard - started' % __name__)
        Logger.Debug('%s - update_dashboard - started with dashboard:%s' % (__name__, dashboard))
        db = Dashboard.Load(dashboard['id'])
        db['collections'] = dashboard['collections']
        db.save()
        Logger.Info('%s - update_dashboard - finished' % __name__)

    def delete_dashboards_to_match_subscription(self, maximum_number_of_dashboards):
        Logger.Info('%s - delete_dashboards_to_match_subscription - started' % __name__)
        Logger.Debug('%s - delete_dashboards_to_match_subscription - started with maximum_number_of_dashboards:%s' % (__name__, maximum_number_of_dashboards))
        dashboards_to_be_deleted = self.get_saved_dashboards()[maximum_number_of_dashboards:]
        for dashboard in dashboards_to_be_deleted:
            dashboard['active'] = False
            dashboard.save()
        Logger.Info('%s - delete_dashboards_to_match_subscription - finished' % __name__)

