class VisualizationBase(object):
    def visualization_removed(self):
        pass

    def generate_search_query_data(self, config, search_configuration):
        data_queries = [{'name':dd['value']['value'], 'type':'basic_facet'} for dd in config['data_dimensions'] if dd['value']]
        return [data_queries]

    def render_javascript_based_visualization(self, config, search_results_collection):
        pass