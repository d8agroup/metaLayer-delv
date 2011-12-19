from django.conf import settings
from urllib2 import Request, urlopen
from urllib import urlencode
from django.utils import simplejson as json
from datapoints.models import DataPoint
from logger import Logger

class DataPointController(object):
    def __init__(self, data_point):
        self.data_point = data_point

    @classmethod
    def GetAllForTemplateOptions(cls, options):
        #TODO: need to take account of options
        return [dp.load_configuration() for dp in DataPoint.objects.all()]

    def is_valid(self):
        type = self.data_point['type']
        data_point = DataPoint.LoadDataPoint(type)
        passed, errors = data_point.validate_config(self.data_point)
        return passed, errors

    def get_configured_display_name(self):
        type = self.data_point['type']
        data_point = DataPoint.LoadDataPoint(type)
        return data_point.generate_configured_display_name(self.data_point)

    def data_point_added(self):
        type = self.data_point['type']
        data_point = DataPoint.LoadDataPoint(type)
        data_point.data_point_added(self.data_point)

    def data_point_removed(self):
        type = self.data_point['type']
        data_point = DataPoint.LoadDataPoint(type)
        data_point.data_point_removed(self.data_point)

class MetaLayerAggregatorController(object):
    @classmethod
    def _call_aggregator(cls, add_source_endpoint_url, config, sub_type, type):
        source = {'type': type, 'config': config}
        if sub_type:
            source['sub_type'] = sub_type
        data = urlencode({'source': json.dumps(source)})
        request = Request(add_source_endpoint_url, data)
        response = urlopen(request).read()
        response = json.loads(response)
        status = response['status']
        return status

    @classmethod
    def AddSourceToAggregator(cls, type, config, sub_type=None):
        add_source_endpoint_url = settings.ENDPOINTS['datapoints']['metalayer_aggregator']['add_source']
        status = cls._call_aggregator(add_source_endpoint_url, config, sub_type, type)
        if status == 'failure':
            Logger.Error('AddSourceToAggregator Failed - type = %s, config = %s, sub_type = %s' % (type, json.dumps(config), sub_type))

    @classmethod
    def RemoveSourceFromAggregator(cls, type, config, sub_type=None):
        remove_source_endpoint_url = settings.ENDPOINTS['datapoints']['metalayer_aggregator']['remove_source']
        status = cls._call_aggregator(remove_source_endpoint_url, config, sub_type, type)
        if status == 'failure':
            Logger.Error('RemoveSourceFromAggregator Failed - type = %s, config = %s, sub_type = %s' % (type, json.dumps(config), sub_type))

