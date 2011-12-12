from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
from dashboards.models import Dashboard, DashboardTemplate

class DashboardsController(object):
    def __init__(self, user):
        self.user = user

    def get_saved_dashboards(self):
        return Dashboard.AllForUser(self.user)

    def get_dashboard_by_id(self, id):
        return Dashboard.Load(id)

    def get_dashboard_templates(self):
        return DashboardTemplate.AllForUser(self.user)