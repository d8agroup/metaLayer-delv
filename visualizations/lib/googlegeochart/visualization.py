from visualizations.classes import BaseVisualization

class Visualization(BaseVisualization):
    def get_unconfigured_config(self):
        return {
            'name':'googlegeochart',
            'display_name_short':'GeoChart',
            'display_name_long':'Google GeoChart',

        }