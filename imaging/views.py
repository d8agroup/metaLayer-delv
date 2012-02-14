from django.http import HttpResponse
from dashboards.controllers import DashboardsController
from imaging.controllers import ImagingController

def insight_image(request, dashboard_id, width='0', height='0', fill_color=None):
    dashboard = DashboardsController.GetDashboardById(dashboard_id)
    image = ImagingController(dashboard, int(width), int(height), fill_color).insight_image() if dashboard else ImagingController.GenerateNotFoundImage(int(width), int(height), fill_color)
    return HttpResponse(image, mimetype="image/png")

def insight_image_for_facebook(request, dashboard_id):
    dashboard = DashboardsController.GetDashboardById(dashboard_id)
    image = ImagingController(dashboard, 200, 200).insight_image() if dashboard else ImagingController.GenerateNotFoundImage(200, 200)
    return HttpResponse(image, mimetype="image/png")