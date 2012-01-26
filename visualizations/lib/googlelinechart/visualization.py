import time
from utils import get_pretty_date
from visualizations.classes import VisualizationBase
from django.utils import simplejson as json

class Visualization(VisualizationBase):
    def get_unconfigured_config(self):
        return {
            'name':'googlelinechart',
            'display_name_short':'Line Chart',
            'display_name_long':'Google Line Chart',
            'image_small':'http://www.mricons.com/store/png/120627_38550_64_google_icon.png',
            'unconfigurable_message':'There is no linea data available to be mapped.',
            'type':'javascript',
            'configured':False,
            'elements':[
                {
                    'name':'xaxis',
                    'display_name':'x-axis',
                    'help':'Choose a metric to base the x-axis on',
                    'type':'select',
                    'values':[
                        'Time - minutes',
                        'Time - hours',
                        'Time - days',
                    ],
                    'value':'Time - minutes'
                }
            ],
            'data_dimensions':[
                {
                    'name':'line1',
                    'display_name':'1st Line',
                    'type':'int',
                    'help':''
                }
            ]
        }

    def generate_search_query_data(self, config, search_configuration):
        end, start, time_increment = self._parse_time_parameters(config)
        return_data = []
        for dimension in config['data_dimensions']:
            query_data = [{
                'name': 'time',
                'gap': time_increment,
                'start': start,
                'end': end
            }]
            if dimension['value'] != 'total_count':
                query_data.append({
                    'name':dimension['value']['name'],
                    'value':dimension['value']['name']
                })
            return_data.append(query_data)
        return return_data

    def render_javascript_based_visualization(self, config, search_results_collection):
        js = ""\
            "$.getScript\n"\
            "(\n"\
            "   'https://www.google.com/jsapi',\n"\
            "   function()"\
            "   {\n"\
            "       google.load('visualization', '1', {'packages': ['corechart'], 'callback':drawchart_" + config['id'] + "});\n"\
            "       function drawchart_" + config['id'] + "()\n"\
            "       {\n"\
            "           if(!document.getElementById('" + config['id'] + "'))\n"\
            "               return;\n"\
            "           var data = new google.visualization.DataTable();\n"\
            "           {data_columns}\n"\
            "           data.addRows(\n"\
            "               {data_rows}\n"\
            "           );\n"\
            "           var options = {options};\n"\
            "           var chart = new google.visualization.LineChart(document.getElementById('" + config['id'] + "'));\n"\
            "           chart.draw(data, options);\n"\
            "       }\n"\
            "   }\n"\
            ");\n"

        end, start, time_increment = self._parse_time_parameters(config)
        series_titles = [{'name':'Time', 'type':'string'}]
        collections_of_values = [[get_pretty_date(x)] for x in range(start, end, time_increment)]

        for x in range(len(config['data_dimensions'])):
            series_titles.append({'name':config['data_dimensions'][x]['value'], 'type':'number'})
            candidate_facet_groups = [fg for fg in search_results_collection[x]['facet_range_groups'] if fg['name'] == 'time']
            if len(candidate_facet_groups) != 1:
                values = range(5)
            else:
                values = [f['count'] for f in candidate_facet_groups[0]['facets']]
            for y in range(5):
                collections_of_values[y].append(values[y])


        data_columns = '\n'.join(["data.addColumn('%s', '%s');" % (t['type'], t['name']) for t in series_titles])
        data_rows = json.dumps(collections_of_values)

        options = json.dumps({
            'backgroundColor':'#333333',
            'colors':['#FF0000', '#FFFF00', '#FF00FF', '#0000FF', '#00FFFF', '#00FF00'],
            'title':'Content items collected over time',
            'titleTextStyle':{
                'color':'#FFFFFF'
            },
            'hAxis':{
                'baselineColor':'#DDDDDD',
                'textStyle':{
                    'color':'#DDDDDD'
                },
                'slantedText':True,
                'gridlines.color':'#AAAAAA',
            },
            'legend':{
                'position':'right',
                'textStyle':{
                    'color':'#DDDDDD'
                }
            },
            'vAxis':{
                'title':'Content items produced',
                'titleTextStyle':{
                    'color':'#DDDDDD'
                },
                'baselineColor':'#DDDDDD',
                'format':'#',
                'textStyle':{
                    'color':'#DDDDDD'
                },
                'minValue':0
            }
        })

        js = js.replace('{data_columns}', data_columns)
        js = js.replace('{data_rows}', data_rows)
        js = js.replace('{options}', options)
        return js

    def _parse_time_parameters(self, config):
        time_increment = [e for e in config['elements'] if e['name'] == 'xaxis'][0]['value']
        if time_increment == 'Time - minutes':
            time_increment = 60 * 10 #ten minutes
        elif time_increment == 'Time - hours':
            time_increment = 60 * 60 * 2 #two hours
        elif time_increment == 'Time - days':
            time_increment = 60 * 60 * 24 #one day
        end = int(time.time())
        start = end - (5 * time_increment) #5 steps
        return end, start, time_increment

