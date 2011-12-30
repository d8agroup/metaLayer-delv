from django.conf import settings
from urllib import quote
from datapoints.controllers import DataPointController
from datetime import datetime

class SearchDataPointParser(object):
    def __init__(self, data_points):
        self.data_points = data_points

    def parse_data_points(self):
        return '&'.join([self._parse_data_point(dp) for dp in self.data_points])

    def _parse_data_point(self, data_point):
        dpc = DataPointController(data_point)
        return 'fq=source_id:%s' % dpc.generate_configured_guid()


class SearchQueryParser(object):
    def __init__(self, query_params):
        self.params = query_params
        self.not_facets = ['keywords', 'start', 'pagesize']

    def parse_query(self):
        return '&'.join([part for part in [self._parse_keywords(), self._parse_pagination(), self._parse_facets()] if part != ''])

    def _parse_keywords(self):
        return 'q=%s' % (quote(self.params['keywords'])) if 'keywords' in self.params and self.params['keywords'] != '' and self.params['keywords'] != None else 'q=*'

    def _parse_pagination(self):
        parsed_params = []
        for pair in [('start','start'),('pagesize','rows')]:
            if pair[0] in self.params:
                parsed_params.append('%s=%s' % (pair[1], self.params[pair[0]]))
        return '&'.join(parsed_params)

    def _parse_facets(self):
        parsed_facets = ['fq=%s:%s' % (k, self.params[k]) for k in self.params.keys() if k not in self.not_facets]
        return '&'.join(parsed_facets)

class SearchResultsParser(object):
    def __init__(self, solr_response, request_base, current_request_args):
        self.solr_response = solr_response
        self.request_base = request_base
        self.current_request_args = current_request_args

    def search_results(self):
        return {
            'content_items':self._extract_content_items(self.solr_response),
            'facet_groups':self._extract_facets(self.solr_response),
            'breadcrumbs':self._extract_breadcrumbs(self.current_request_args),
            'pagination':self._extract_pagination(self.solr_response),
            'keywords':self._extract_keywords(self.solr_response),
            }

    def _extract_content_items(self, solr_response):
        return [self._apply_late_fixes(item) for item in solr_response['response']['docs']]

    def _extract_facets(self, solr_response):
        if not solr_response:
            return []
        facet_groups = [{'name':f, 'display_name':f, 'facets':[]} for f in solr_response['facet_counts']['facet_fields'].keys()]
        for fg in facet_groups:
            for x in range(0, len(solr_response['facet_counts']['facet_fields'][fg['name']]), 2):
                fg['facets'].append({
                    'name':solr_response['facet_counts']['facet_fields'][fg['name']][x],
                    'count':solr_response['facet_counts']['facet_fields'][fg['name']][x+1],
                    'link':self._construct_facet_link(self.request_base, self.current_request_args, fg['name'], solr_response['facet_counts']['facet_fields'][fg['name']][x])
                })
        return facet_groups

    def _extract_breadcrumbs(self, args):
        if not args:
            return []
        breadcrumbs = [{'type':key, 'display_type':key, 'value':args[key], 'link':self._construct_breadcrumb_link(self.request_base, args, key, args[key])} for key in args.keys()]
        return breadcrumbs

    def _extract_keywords(self, solr_response):
        params = solr_response['responseHeader']['params']
        return params['q'] if 'q' in params and params['q'] != '*' else None

    def _extract_pagination(self, solr_response):
        return {
            'start':solr_response['response']['start'],
            'pagesize':solr_response['responseHeader']['params']['rows'] if 'rows' in solr_response['responseHeader']['params'] else settings.SOLR_CONFIG['default_page_size'],
            'total':solr_response['response']['numFound']
        }

    def _construct_facet_link(self, request_base, current_request_args, facet_name, facet_value):
        link = '%s?%s' % (request_base, '&'.join(['%s=%s' % (k, current_request_args[k]) for k in current_request_args.keys()]))
        link += '&%s=%s' % (facet_name, facet_value)
        link = link.replace('?&', '?')
        return link

    def _construct_breadcrumb_link(self, request_base, current_request_args, facet_name, facet_value):
        link = '%s?%s' % (request_base, '&'.join(['%s=%s' % (k, current_request_args[k]) for k in current_request_args.keys() if k != facet_name and current_request_args[k] != facet_value]))
        return link if not link.endswith('?') else link[0:-1]

    def _apply_late_fixes(self, item):
        item['date'] = datetime.fromtimestamp(item['time']).strftime('%Y-%m-%d %H:%M:%S')
        return item


