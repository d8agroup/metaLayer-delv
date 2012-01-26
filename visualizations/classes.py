class VisualizationBase(object):
    def visualization_removed(self):
        pass

    def generate_search_query_data(self, config):
        data_queries = [{'name':dd['value']} for dd in config['data_dimensions'] if dd['value']]
        return data_queries

    def render_javascript_based_visualization(self, config, facets):
        pass