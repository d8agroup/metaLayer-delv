from visualizations.classes import VisualizationBase
from django.utils import simplejson as json

class Visualization(VisualizationBase):
    def get_unconfigured_config(self):
        return {
            'name':'googlegeochart',
            'display_name_short':'Map',
            'display_name_long':'Map',
            'image_small':'/static/images/site/map.png',
            'unconfigurable_message':'There is no location data available, try adding a location detections action.',
            'type':'javascript',
            'configured':False,
            'elements':[
                {
                    'name':'map_mode',
                    'display_name':'Map type',
                    'help':'Region works best with country data while Marker works well with cities or other places',
                    'type':'select',
                    'values':[
                        'Regions',
                        'Markers'
                    ],
                    'value':'Regions'
                },
                {
                    'name':'focus',
                    'display_name':'Map focus',
                    'help':'Choose a geographic region to focus the map on',
                    'type':'select',
                    'values':[
                        'World',
                        'North America',
                        'Europe',
                        'Asia',
                        'Africa',
                        'Americas',
                        'Oceania'
                    ],
                    'value':'World'
                },
                {
                    'name':'color',
                    'display_name':'Color Scheme',
                    'help':'',
                    'type':'select',
                    'values':[
                        'Red',
                        'Blue',
                        'Green',
                        'Black and White'
                    ],
                    'value':'Red'
                }
            ],
            'data_dimensions':[
                {
                    'name':'locations',
                    'display_name':'Location',
                    'type':'location_string',
                    'help':''
                }
            ]
        }

    def render_javascript_based_visualization(self, config, search_results_collection):
        search_results = search_results_collection[0]
        facets = [f['facets'] for f in search_results['facet_groups'] if f['name'] == config['data_dimensions'][0]['value']['value']][0]
        js = "" \
            "$.getScript\n" \
            "(\n" \
            "   'https://www.google.com/jsapi',\n" \
            "   function()" \
            "   {\n" \
            "       google.load('visualization', '1', {'packages': ['geochart'], 'callback':drawRegionsMap_" + config['id'] + "});\n" \
            "       function drawRegionsMap_" + config['id'] + "()\n" \
            "       {\n" \
            "           if(!document.getElementById('" + config['id'] + "'))\n" \
            "               return;\n" \
            "           var data = new google.visualization.DataTable();\n" \
            "           data.addColumn('string', 'Country');\n" \
            "           data.addColumn('number', 'Mentions');\n" \
            "           data.addRows([\n" \
            "               {data_rows}\n" \
            "           ]);\n" \
            "           var options = {options};\n" \
            "           var chart = new google.visualization.GeoChart(document.getElementById('" + config['id'] + "'));\n" \
            "           chart.draw(data, options);\n" \
            "       }\n" \
            "   }\n" \
            ");\n"

        data_rows = ','.join(["['%s', %i]" % (f['name'], f['count']) for f in facets])
        js = js.replace("{data_rows}", data_rows)
        options = {
            'backgroundColor':'#333333',
            'datalessRegionColor':'#444444',
            'colorAxis':{
                'minValue':0,
                'colors':self._map_map_colors([e for e in config['elements'] if e['name'] == 'color'][0]['value'])
            },
            'region':self._map_map_focus([e for e in config['elements']][1]['value'])
        }
        if [e for e in config['elements']][0]['value'] == 'Markers':
            options['displayMode'] = 'markers'
        options = json.dumps(options)
        js = js.replace('{options}', options)
        return js

    def _map_map_focus(self, focus):
        if focus == 'Africa': return '002'
        if focus == 'Europe': return '150'
        if focus == 'Americas': return '019'
        if focus == 'North America': return '021'
        if focus == 'Asia': return '142'
        if focus == 'Oceania': return '009'
        return 'world'

    def _map_map_colors(self, color):
        if color == 'Blue': return ['#CCCCFF', '#0000FF']
        if color == 'Green': return ['#33CC66', '#006600']
        if color == 'Black and White': return ['#FFFFFF', '#000000']
        return ['#FFCC66', '#FF6600']

