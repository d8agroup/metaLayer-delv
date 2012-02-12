class SVGToPNGConverter(object):
    @classmethod
    def Convert(cls, svg_data, max_width=0, max_height=0):
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
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, x, y)
        context = cairo.Context(surface)
        context.scale(x_scale, y_scale)
        svg.render_cairo(context)
        output = StringIO.StringIO()
        surface.write_to_png(output)
        output.seek(0)
        return output