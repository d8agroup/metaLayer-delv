from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from dashboards.models import Dashboard

class DashboardsController(object):
    def __init__(self, user):
        self.user = user

    def render_saved_dashboards(self):
        template = get_template('../templates/dashboards_summary.html')
        dashboards = [template.render(Context(dashboard)) for dashboard in Dashboard.AllForUser(self.user)]
        return dashboards

    def render_dashboard(self, id):
        dashboard = Dashboard.Load(id)
        return render_to_response(
            '../templates/dashboards_dashboard.html',
            {'dashboard': dashboard}
        )