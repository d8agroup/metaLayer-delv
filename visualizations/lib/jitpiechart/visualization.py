import time
from utils import get_pretty_date
from visualizations.classes import VisualizationBase
from django.utils import simplejson as json

class Visualization(VisualizationBase):

    bar_limit = 5
    steps_backwards = 5

    def get_unconfigured_config(self):
        return {
            'name':'jitpiechart',
            'display_name_short':'Pie Chart',
            'display_name_long':'Pie Chart',
            'image_small':'/static/images/lib/Impressions/pie_chart.png',
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
                        'No - Show totals only',
                        'Breakdown by minutes',
                        'Breakdown by hours',
                        'Breakdown by days'
                    ],
                    'value':'No - Show totals only'
                }
            ],
            'data_dimensions':[
                    {
                    'name':'category1',
                    'display_name':'Category',
                    'type':'string',
                    'help':''
                }
            ]
        }

    def generate_search_query_data(self, config, search_configuration):
        time_variable = [e for e in config['elements'] if e['name'] == 'time'][0]['value']
        return_data = []
        if time_variable == 'No - Show totals only':
            for dimension in config['data_dimensions']:
                return_data.append([{
                    'name':dimension['value']['value'],
                    'type':'basic_facet'
                }])
        else:
            end, start, time_increment = self._parse_time_parameters(time_variable)
            for s in range(start, end, time_increment):
                this_search = []
                for dimension in config['data_dimensions']:
                    this_search.append({
                        'name':dimension['value']['value'],
                        'type':'basic_facet'
                    })
                this_search.append({
                    'name':'time',
                    'range':{'start':s, 'end':(s + time_increment - 1)},
                    'type':'range_query'
                })
                return_data.append(this_search)
        return return_data

    def render_javascript_based_visualization(self, config, search_results_collection):
        js = ""\
            "if($('." + config['id'] + "_css').length == 0)\n" \
            "{\n" \
            "   var link = $('<link class=\"" + config['id'] + "_css\">');\n" \
            "   link.attr({type:'text/css', rel:'stylesheet', href:'/static/css/lib/jit_pie_chart.css'});\n" \
            "   $('head').append(link);\n" \
            "   $.getScript('/static/js/lib/jit.js');\n" \
            "}\n" \
            "function LoadChart_" + config['id'] + "()\n" \
            "{\n" \
            "   var data = {data};\n" \
            "   var pieChart = new $jit.PieChart({\n" \
            "       injectInto: '" + config['id'] + "',\n" \
            "       type:'stacked',\n" \
            "       showLabels:true,\n" \
            "       resizeLabels: 7,\n" \
            "       Label: { type: 'Native', size: 20, family: 'Arial', color: 'white' }\n" \
            "   });\n" \
            "   pieChart.loadJSON(data);\n" \
            "   var list = $jit.id('id-list');\n" \
            "   var legend = pieChart.getLegend(), listItems = [];\n" \
            "   for(var name in legend) {\n" \
            "       listItems.push('<div class=\"query-color\" style=\"background-color:' + legend[name] +';\">&nbsp;</div>' + name);\n" \
            "   }\n" \
            "   list.innerHTML = '<li>' + listItems.join('</li><li>') + '</li>';" \
            "}" \
            "setTimeout(function() {LoadChart_" + config['id'] + "(); }, 2000);" \
            ""


        #TODO this only support one data dimension at the moment
        time_variable = [e for e in config['elements'] if e['name'] == 'time'][0]['value']
        if time_variable == 'No - Show totals only':
            search_result = search_results_collection[0]
            data_dimensions_value = config['data_dimensions'][0]['value']
            facets = [fg for fg in search_result['facet_groups'] if fg['name'] == data_dimensions_value['value']][0]['facets']
            data = { 'labels':[], 'values':[] }
            for facet in facets:
                data['labels'].append(facet['name'])
                data['values'].append({
                    'label':facet['name'],
                    'values':[facet['count']]
                })
        else:
            data_dimensions_value = config['data_dimensions'][0]['value']
            end, start, time_increment = self._parse_time_parameters(time_variable)
            array_of_start_times = range(start, end, time_increment)
            results_data_columns = []
            for search_result in search_results_collection:
                facets = [fg for fg in search_result['facet_groups'] if fg['name'] == data_dimensions_value['value']][0]['facets']
                for f in facets:
                    if f['name'] not in results_data_columns:
                        results_data_columns.append(f['name'])
            data = { 'labels':[], 'values':[] }
            for x in range(len(array_of_start_times)):
                search_result = search_results_collection[x]
                start_time_pretty = get_pretty_date(array_of_start_times[x])
                data_values = {'label': start_time_pretty, 'values': []}
                facets = [fg for fg in search_result['facet_groups'] if fg['name'] == data_dimensions_value['value']][0]['facets']
                for c in results_data_columns:
                    candidate_facet = [f for f in facets if f['name'] == c]
                    if candidate_facet:
                        data_values['values'].append(candidate_facet[0]['count'])
                    else:
                        data_values['values'].append(0)
                if sum(data_values['values']) > 0:
                    data['labels'].append(start_time_pretty)
                    data['values'].append(data_values)

        data = json.dumps(data)
        js = js.replace('{data}', data)
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
