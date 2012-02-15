import cairo
import rsvg
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

def crop(request, dashboard_id, width, height):
    width = int(width)
    height = int(height)
    dashboard = DashboardsController.GetDashboardById(dashboard_id)
    if not dashboard or not dashboard.has_visualizations():
        return ImagingController.GenerateNotFoundImage(width, height, None)
    visualization_svg = dashboard.visualization_for_image()
    svg = rsvg.Handle(data=visualization_svg)
    image_height = svg.props.height
    required_height = height * 1.5
    scale = (float(required_height) / float(image_height))
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)
    context.scale(scale, scale)
    context.translate((width / 2) * -1, (height / 2) * -1)
    svg.render_cairo(context)
    response = HttpResponse(mimetype='image/png')
    surface.write_to_png(response)
    return response

def shrink(request, dashboard_id, max_width, max_height):
    max_width = int(max_width)
    max_height = int(max_height)
    dashboard = DashboardsController.GetDashboardById(dashboard_id)
    if not dashboard or not dashboard.has_visualizations():
        return ImagingController.GenerateNotFoundImage(width, height, None)
    visualization_svg = dashboard.visualization_for_image()
    svg = rsvg.Handle(data=visualization_svg)
    x = width = svg.props.width
    y = height = svg.props.height
    y_scale = x_scale = 1
    if (max_height != 0 and width > max_width) or (max_height != 0 and height > max_height):
        x = max_width
        y = float(max_width)/float(width) * height
        if y > max_height:
            y = max_height
            x = float(max_height)/float(height) * width
        x_scale = float(x)/svg.props.width
        y_scale = float(y)/svg.props.height
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, x, y)
    context = cairo.Context(surface)
    context.scale(x_scale, y_scale)
    svg.render_cairo(context)
    response = HttpResponse(mimetype='image/png')
    surface.write_to_png(response)
    return response
