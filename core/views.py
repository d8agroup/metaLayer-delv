from django.shortcuts import render_to_response
from dashboards.controllers import DashboardsController

def index(request):
    return render_to_response(
        '../templates/core_index.html'
    )

def dashboard(request, id):
    dc = DashboardsController(request.user)
    return dc.render_dashboard(id)