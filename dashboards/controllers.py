from dashboards.models import Dashboard, DashboardTemplate

class DashboardsController(object):
    def __init__(self, user):
        self.user = user

    def get_saved_dashboards(self):
        return Dashboard.AllForUser(self.user)

    def get_dashboard_by_id(self, id):
        return Dashboard.Load(id, True)

    def delete_dashboard_by_id(self, id):
        dashboard = Dashboard.Load(id)
        dashboard['active'] = False
        dashboard.save()

    def get_dashboard_templates(self):
        return DashboardTemplate.AllForUser(self.user)

    def create_new_dashboard_from_template(self, template_id):
        template = DashboardTemplate.GetTemplateById(template_id)
        dashboard = Dashboard.Create(self.user, template)
        return dashboard

    def update_dashboard(self, dashboard):
        db = Dashboard.Load(dashboard['id'])
        db['collections'] = dashboard['collections']
        db.save()
        return

    def delete_dashboards_to_match_subscription(self, maximum_number_of_dashboards):
        dashboards_to_be_deleted = self.get_saved_dashboards()[maximum_number_of_dashboards:]
        for dashboard in dashboards_to_be_deleted:
            dashboard['active'] = False
            dashboard.save()

