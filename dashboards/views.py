from django.conf import settings
from django.shortcuts import redirect
from dashboards.controllers import DashboardsController
from dashboards.models import DashboardShortUrl

def redirect_to_dashboard(request, url_id):
    short_url = DashboardShortUrl.Load(url_id)
    dashboard = DashboardsController.GetDashboardById(short_url['dashboard_id'])
    return redirect('http://%s/delv/%s/%s' % (settings.SITE_HOST, dashboard['username'], dashboard['id']))