from dashboards.models import Dashboard, DashboardTemplate

class DashboardsController(object):
    def __init__(self, user):
        self.user = user

    def get_saved_dashboards(self):
        return Dashboard.AllForUser(self.user)

    def get_dashboard_by_id(self, id):
        return Dashboard.Load(id, True)

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