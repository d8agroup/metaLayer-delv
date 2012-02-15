import time

class VisualizationBase(object):
    def visualization_removed(self):
        pass

    def generate_search_query_data(self, config, search_configuration):
        data_queries = [
            {'name':dd['value']['value'], 'type':'basic_facet'} for dd in config['data_dimensions'] if dd['value']
        ]
        return [data_queries]

    def _parse_time_parameters(self, time_increment, steps_backwards, search_time_parameter):
        if time_increment == 'minutes':
            time_increment = 60 * 10 #ten minutes
        elif time_increment == 'hours':
            time_increment = 60 * 60 * 2 #two hours
        elif time_increment == 'days':
            time_increment = 60 * 60 * 24 #one day

        search_end_time = search_time_parameter.split('%20TO%20')[1].strip(']')
        end = int(time.time()) if search_end_time == '*' else int(search_end_time)
        start = end - (steps_backwards * time_increment)
        search_start_time = search_time_parameter.split('%20TO%20')[0].strip('[')
        if search_start_time != '*' and int(search_start_time) > start:
            start = int(search_start_time)
        return end, start, time_increment

    def _extract_time_bounds_from_search_configuration(self, search_configuration):
        search_end_time = search_configuration['search_filters']['time'].split('%20TO%20')[1].strip(']')
        if search_end_time == "*":
            search_end_time = int(time.time())
        else:
            search_end_time = int(search_end_time)
        search_start_time = int(search_configuration['search_filters']['time'].split('%20TO%20')[0].strip('['))
        return search_start_time, search_end_time
