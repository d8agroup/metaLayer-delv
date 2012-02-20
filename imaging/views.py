import StringIO
from django.conf import settings
import cairo
import rsvg
from django.http import HttpResponse
from dashboards.controllers import DashboardsController
from imaging.controllers import ImagingController

def insight_image_for_facebook(request, dashboard_id):
    return crop(request, dashboard_id, 200, 200)

def crop(request, dashboard_id, width, height):
    dashboard = DashboardsController.GetDashboardById(dashboard_id, False)
    if not dashboard or not dashboard.has_visualizations():
        return ImagingController.GenerateNotFoundImage(width, height, None)
    file_name = '%s/crop_%s_%s_%s.png' % (settings.DYNAMIC_IMAGES_ROOT, dashboard_id, width, height)
    image_data = ImagingController.ReadImageFromCache(file_name, dashboard['last_saved'])
    if not image_data:
        width = int(width)
        height = int(height)
        dashboard = DashboardsController.GetDashboardById(dashboard_id, False)
        if not dashboard or not dashboard.has_visualizations():
            return ImagingController.GenerateNotFoundImage(width, height, None)
        visualization_svg = dashboard.visualization_for_image()
        svg = rsvg.Handle(data=visualization_svg)
        image_height = svg.props.height
        required_height = height * 1.8
        scale = (float(required_height) / float(image_height))
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)
        context.scale(scale, scale)
        context.translate((width + width/4) * -1, (height / 2) * -1)
        svg.render_cairo(context)
        image_data = StringIO.StringIO()
        surface.write_to_png(image_data)
        ImagingController.WriteImageDataToCache(file_name, image_data)
    response = HttpResponse(image_data, mimetype='image/png')
    return response

def shrink(request, dashboard_id, max_width, max_height):
    dashboard = DashboardsController.GetDashboardById(dashboard_id, False)
    if not dashboard or not dashboard.has_visualizations():
        return ImagingController.GenerateNotFoundImage(max_width, max_height, None)
    file_name = '%s/shrink_%s_%s_%s.png' % (settings.DYNAMIC_IMAGES_ROOT, dashboard_id, max_width, max_height)
    image_data = ImagingController.ReadImageFromCache(file_name, dashboard['last_saved'])
    if not image_data:
        max_width = int(max_width)
        max_height = int(max_height)
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
        image_data = StringIO.StringIO()
        surface.write_to_png(image_data)
        ImagingController.WriteImageDataToCache(file_name, image_data)
    response = HttpResponse(image_data, mimetype='image/png')
    return response
