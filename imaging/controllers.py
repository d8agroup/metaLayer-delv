from django.conf import settings
from imaging.converters import SVGToPNGConverter
import cairo
import StringIO

class ImagingController(object):
    @classmethod
    def GenerateNotFoundImage(cls, width, height, fill_color):
        text_sizes = (14, 10) if width > 100 else (10, 7)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)
        rgb = ImagingController._html_color_to_rgb(fill_color)
        context.set_source_rgb(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        context.rectangle(0, 0, width, height)
        context.fill()
        text = 'metaLayer'
        context.set_source_rgb(1.0, 1.0, 1.0) # white
        context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        context.set_font_size(text_sizes[0])
        x, y, w, h = context.text_extents(text)[:4]
        context.move_to((width / 2) - (w / 2) - x, (height / 2) - (h / 2) - y)
        context.show_text(text)
        text = 'no image'
        context.set_source_rgb(1.0, 1.0, 1.0) # white
        context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(text_sizes[1])
        x, y, w, h = context.text_extents(text)[:4]
        context.move_to((width / 2) - (w / 2) - x, (height / 2) - (h / 2) - y + 14)
        context.show_text(text)
        string_io = StringIO.StringIO()
        surface.write_to_png(string_io)
        string_io.seek(0)
        return string_io

    def __init__(self, dashboard, max_width=0, max_height=0, fill_color=None):
        self.dashboard = dashboard
        self.max_width = max_width
        self.max_height = max_height
        self.fill_color = fill_color

    def insight_image(self):
        if self.dashboard.has_visualizations():
            visualization_svg = self.dashboard.visualization_for_image()
            image_string_io = SVGToPNGConverter.Convert(visualization_svg, self.max_width, self.max_height, self.fill_color)
            return image_string_io
        else:
            return ImagingController.GenerateNotFoundImage(self.max_width, self.max_height, self.fill_color)

    @classmethod
    def _html_color_to_rgb(self, color_string):
        """ convert RRGGBB to an (R, G, B) tuple """
        color_string = color_string.strip()
        r, g, b = color_string[:2], color_string[2:4], color_string[4:]
        r, g, b = [int(n, 16) for n in (r, g, b)]
        return (float(r), float(g), float(b))

