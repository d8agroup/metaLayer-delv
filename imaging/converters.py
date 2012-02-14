

class SVGToPNGConverter(object):
    @classmethod
    def Convert(cls, svg_data, max_width=0, max_height=0, fill_color=None):
        import cairo
        import rsvg
        import StringIO
        svg = rsvg.Handle(data=svg_data)
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

        if fill_color:
            from imaging.controllers import ImagingController
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, max_width, max_height)
            context = cairo.Context(surface)
            rgb = ImagingController._html_color_to_rgb(fill_color)
            context.set_source_rgb(rgb[0]/255, rgb[1]/255, rgb[2]/255)
            context.rectangle(0, 0, width, height)
            context.fill()
            context.translate((max_width - x)/2, (max_height - y)/2)
            context.scale(x_scale, y_scale)
        else:
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, x, y)
            context = cairo.Context(surface)
            context.scale(x_scale, y_scale)
        svg.render_cairo(context)
        output = StringIO.StringIO()
        surface.write_to_png(output)
        output.seek(0)
        return output