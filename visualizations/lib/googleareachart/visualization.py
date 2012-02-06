import time
from utils import get_pretty_date
from visualizations.classes import VisualizationBase
from django.utils import simplejson as json

class Visualization(VisualizationBase):

    bar_limit = 5
    steps_backwards = 5

    def get_unconfigured_config(self):
        return {
            'name':'googleareachart',
            'display_name_short':'Area Chart',
            'display_name_long':'Area Chart',
            'image_small':'/static/images/site/area_chart.png',
            'unconfigurable_message':'There is no category data available to be plotted. Try adding something like sentiment analysis',
            'type':'javascript',
            'configured':False,
            'elements':[
                {
                    'name':'time',
                    'display_name':'Visualize over time?',
                    'help':'',
                    'type':'select',
                    'values':[
                        'Breakdown by minutes',
                        'Breakdown by hours',
                        'Breakdown by days'
                    ],
                    'value':'Breakdown by minutes'
                }
            ],
            'data_dimensions':[
                {
                    'name':'category1',
                    'display_name':'Areas',
                    'type':'string',
                    'help':''
                }
            ]
        }

    def generate_search_query_data(self, config, search_configuration):
        time_variable = [e for e in config['elements'] if e['name'] == 'time'][0]['value']
        return_data = []
        end, start, time_increment = self._parse_time_parameters(time_variable)
        for s in range(start, end, time_increment):
            this_search = []
            for dimension in config['data_dimensions']:
                this_search.append({
                    'name':dimension['value']['value'],
                    'type':'basic_facet',
                    'limit':10
                })
            this_search.append({
                'name':'time',
                'range':{
                    'start':s,
                    'end':(s + time_increment - 1)
                },
                'type':'range_query'
            })
            return_data.append(this_search)
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
             "           var chart = new google.visualization.AreaChart(document.getElementById('" + config['id'] + "'));\n"\
             "           chart.draw(data, options);\n"\
             "       }\n"\
             "   }\n"\
             ");\n"

        #TODO this only support one data dimension at the moment
        time_variable = [e for e in config['elements'] if e['name'] == 'time'][0]['value']
        data_columns = [{'type':'string', 'name':'Time'}]
        data_rows = []
        data_dimensions_value = config['data_dimensions'][0]['value']
        end, start, time_increment = self._parse_time_parameters(time_variable)
        array_of_start_times = range(start, end, time_increment)
        results_data_columns = []
        for search_result in search_results_collection:
            facets = [fg for fg in search_result['facet_groups'] if fg['name'] == data_dimensions_value['value']][0]['facets']
            for f in facets:
                if f['name'] not in results_data_columns:
                    results_data_columns.append(f['name'])
        data_columns += [{'type':'number', 'name':'%s' % c } for c in results_data_columns]
        number_of_empty_ranges = 0
        for x in range(len(array_of_start_times)):
            search_result = search_results_collection[x]
            start_time_pretty = get_pretty_date(array_of_start_times[x] + time_increment)
            data_row = [start_time_pretty]
            facets = [fg for fg in search_result['facet_groups'] if fg['name'] == data_dimensions_value['value']][0]['facets']
            dynamic_data_rows = []
            for c in results_data_columns:
                candidate_facet = [f for f in facets if f['name'] == c]
                if candidate_facet:
                    dynamic_data_rows.append(candidate_facet[0]['count'])
                else:
                    dynamic_data_rows.append(0)
            if not sum(dynamic_data_rows):
                number_of_empty_ranges += 1
            data_row += dynamic_data_rows
            data_rows.append(data_row)
        if number_of_empty_ranges == len(array_of_start_times):
            return "$('#" + config['id'] + "').html(\"<div class='empty_dataset'>Sorry, there is no data to visualize</div>\");"

        data_columns = '\n'.join(["data.addColumn('%s', '%s');" % (t['type'], t['name']) for t in data_columns])
        data_rows = json.dumps(data_rows)

        options = json.dumps({
            'backgroundColor':'#333333',
            'title':config['data_dimensions'][0]['value']['name'],
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
                'baselineColor':'#DDDDDD',
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

    def _parse_time_parameters(self, time_increment):
        if time_increment == 'Breakdown by minutes':
            time_increment = 60 * 10 #ten minutes
        elif time_increment == 'Breakdown by hours':
            time_increment = 60 * 60 * 2 #two hours
        elif time_increment == 'Breakdown by days':
            time_increment = 60 * 60 * 24 #one day
        end = int(time.time())
        start = end - (self.steps_backwards * time_increment)
        return end, start, time_increment
