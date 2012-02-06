from visualizations.classes import VisualizationBase
from django.utils import simplejson as json

class Visualization(VisualizationBase):

    def get_unconfigured_config(self):
        return {
            'name':'googlepiechart',
            'display_name_short':'Pie Chart',
            'display_name_long':'Pie Chart',
            'image_small':'/static/images/lib/Impressions/pie_chart.png',
            'unconfigurable_message':'There is no category data available to be plotted. Try adding something like sentiment analysis',
            'type':'javascript',
            'configured':False,
            'elements':[],
            'data_dimensions':[
                {
                    'name':'category1',
                    'display_name':'Slices',
                    'type':'string',
                    'help':''
                }
            ]
        }

    def generate_search_query_data(self, config, search_configuration):
        return_data = []
        for dimension in config['data_dimensions']:
            return_data.append([{
                'name':dimension['value']['value'],
                'type':'basic_facet',
                'limit':20
            }])
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
             "           var chart = new google.visualization.PieChart(document.getElementById('" + config['id'] + "'));\n"\
             "           chart.draw(data, options);\n"\
             "       }\n"\
             "   }\n"\
             ");\n"

        #TODO this only support one data dimension at the moment
        search_result = search_results_collection[0]
        data_dimensions_value = config['data_dimensions'][0]['value']
        facets = [fg for fg in search_result['facet_groups'] if fg['name'] == data_dimensions_value['value']][0]['facets']
        data_columns = [{'type':'string', 'name':data_dimensions_value['name']}, {'type':'number', 'name':'count'}]
        data_rows = [[f['name'], f['count']] for f in facets]
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