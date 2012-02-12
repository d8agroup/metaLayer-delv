from django.http import HttpResponse
from dashboards.controllers import DashboardsController
from imaging.controllers import ImagingController

def insight_image(request, dashboard_id):
    dashboard = DashboardsController.GetDashboardById(dashboard_id)
    image = ImagingController(dashboard).insight_image() if dashboard else ImagingController.GenerateNotFoundImage()
    return HttpResponse(image, mimetype="image/png")