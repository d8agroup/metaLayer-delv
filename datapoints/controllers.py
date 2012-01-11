from django.conf import settings
from urllib2 import Request, urlopen
from urllib import urlencode
from django.utils import simplejson as json
from logger import Logger

class DataPointController(object):
    def __init__(self, data_point):
        self.data_point = data_point

    @classmethod
    def GetAllForTemplateOptions(cls, options):
        #TODO: need to take account of options
        return [DataPointController.LoadDataPoint(dp).get_unconfigured_config() for dp in settings.DATA_POINTS_CONFIG['enbaled_data_points']]

    def is_valid(self):
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        passed, errors = data_point.validate_config(self.data_point)
        return passed, errors

    def get_configured_display_name(self):
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        return data_point.generate_configured_display_name(self.data_point)

    def data_point_added(self):
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        data_point.data_point_added(self.data_point)

    def data_point_removed(self):
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        data_point.data_point_removed(self.data_point)

    def generate_configured_guid(self):
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        return data_point.generate_configured_guid(self.data_point)

    def get_content_item_template(self):
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        return data_point.get_content_item_template()

    def run_data_point(self):
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        return data_point.tick(self.data_point)

    @classmethod
    def LoadDataPoint(cls, data_point_name):
        def custom_import(name):
            mod = __import__(name)
            components = name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod
        data_point = custom_import('dashboard.datapoints.lib.%s.datapoint' % data_point_name)
        data_point = getattr(data_point, 'DataPoint')()
        return data_point

    
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
    def AddSourceToAggregator(cls, type, sub_type, config):
        add_source_endpoint_url = settings.ENDPOINTS['datapoints']['metalayer_aggregator']['add_source']
        status = cls._call_aggregator(add_source_endpoint_url, config, sub_type, type)
        if status == 'failure':
            Logger.Error('AddSourceToAggregator Failed - type = %s, config = %s, sub_type = %s' % (type, json.dumps(config), sub_type))

    @classmethod
    def RemoveSourceFromAggregator(cls, type, sub_type, config):
        remove_source_endpoint_url = settings.ENDPOINTS['datapoints']['metalayer_aggregator']['remove_source']
        status = cls._call_aggregator(remove_source_endpoint_url, config, sub_type, type)
        if status == 'failure':
            Logger.Error('RemoveSourceFromAggregator Failed - type = %s, config = %s, sub_type = %s' % (type, json.dumps(config), sub_type))

