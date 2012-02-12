from django.conf import settings
from imaging.converters import SVGToPNGConverter

class ImagingController(object):
    @classmethod
    def GenerateNotFoundImage(cls):
        pass

    def __init__(self, dashboard, max_width=0, max_height=0):
        self.dashboard = dashboard
        self.max_width = max_width
        self.max_height = max_height

    def insight_image(self):
        if self._dashboard_has_visualizations():
            visualization_svg = self.extract_visualization_svg()
            image_string_io = SVGToPNGConverter.Convert(visualization_svg, self.max_width, self.max_height)
            return image_string_io.read()
        else:
            pass

    def _dashboard_has_visualizations(self):
        for collection in [c for c in self.dashboard['collections'] if c['data_points']]:
            if collection['visualizations']:
                return True
        return False

    def extract_visualization_svg(self):
        for visualization_type in settings.VISUALIZATIONS_CONFIG['visualization_display_hierarchy']:
            for collection in [c for c in self.dashboard['collections'] if c['data_points']]:
                for visualization in collection['visualizations']:
                    if visualization['name'] == visualization_type and visualization['snapshot']:
                        return visualization['snapshot']
        return None

