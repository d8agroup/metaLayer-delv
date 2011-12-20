from urllib2 import urlopen
from django.conf import settings
from search.parsers import SearchDataPointParser, SearchQueryParser, SearchResultsParser
from django.utils import simplejson as json

class SearchController(object):
    def __init__(self, configuration):
        self.configuration = configuration

    def run_search_and_return_results(self):
        data_points = self.configuration['data_points']
        sdpp = SearchDataPointParser(data_points)

        search_filters = self.configuration['search_filters']
        sqp = SearchQueryParser(search_filters)

        search_components = [
            settings.SOLR_CONFIG['solr_params'],
            '&'.join(['facet.field=%s' % facet for facet in settings.SOLR_CONFIG['solr_facets'].keys() if settings.SOLR_CONFIG['solr_facets'][facet]['enabled']]),
            sdpp.parse_data_points(),
            sqp.parse_query()
        ]

        search_url = '%s/select/?%s' % (settings.SOLR_CONFIG['solr_url'], '&'.join(search_components))

        response = urlopen(search_url).read()
        response = json.loads(response)

        srp = SearchResultsParser(response, '/search', search_filters)
        return srp.search_results()

