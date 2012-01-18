from django.conf import settings
from urllib2 import Request, urlopen
from urllib import urlencode
from django.utils import simplejson as json
from logger import Logger

class DataPointController(object):
    def __init__(self, data_point):
        Logger.Info('%s - DataPointController.__init__ - started' % __name__)
        Logger.Debug('%s - DataPointController.__init__ - started with data_point:%s' % (__name__, data_point))
        self.data_point = data_point
        Logger.Info('%s - DataPointController.__init__ - finished' % __name__)


    @classmethod
    def GetAllForTemplateOptions(cls, options):
        #TODO: need to take account of options
        Logger.Info('%s - DataPointController.GetAllForTemplateOptions - started' % __name__)
        Logger.Debug('%s - DataPointController.GetAllForTemplateOptions - started with options:%s' % (__name__, options))
        data_points = [DataPointController.LoadDataPoint(dp).get_unconfigured_config() for dp in settings.DATA_POINTS_CONFIG['enabled_data_points']]
        Logger.Info('%s - DataPointController.GetAllForTemplateOptions - finished' % __name__)
        return data_points

    def is_valid(self):
        Logger.Info('%s - DataPointController.is_valid - started' % __name__)
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        passed, errors = data_point.validate_config(self.data_point)
        Logger.Info('%s - DataPointController.is_valid - finished' % __name__)
        return passed, errors

    def get_configured_display_name(self):
        Logger.Info('%s - DataPointController.get_configured_display_name - started' % __name__)
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        display_name = data_point.generate_configured_display_name(self.data_point)
        Logger.Info('%s - DataPointController.get_configured_display_name - finished' % __name__)
        return display_name

    def data_point_added(self):
        Logger.Info('%s - DataPointController.data_point_added - started' % __name__)
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        data_point.data_point_added(self.data_point)
        Logger.Info('%s - DataPointController.data_point_added - finished' % __name__)

    def data_point_removed(self):
        Logger.Info('%s - DataPointController.data_point_removed - started' % __name__)
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        data_point.data_point_removed(self.data_point)
        Logger.Info('%s - DataPointController.data_point_removed - finished' % __name__)

    def generate_configured_guid(self):
        Logger.Info('%s - DataPointController.generate_configured_guid - started' % __name__)
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        guid = data_point.generate_configured_guid(self.data_point)
        Logger.Info('%s - DataPointController.generate_configured_guid - finished' % __name__)
        return guid

    def get_content_item_template(self):
        Logger.Info('%s - DataPointController.get_content_item_template - started' % __name__)
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        item_template = data_point.get_content_item_template()
        Logger.Info('%s - DataPointController.get_content_item_template - finished' % __name__)
        return item_template

    def run_data_point(self):
        Logger.Info('%s - DataPointController.run_data_point - started' % __name__)
        type = self.data_point['type']
        data_point = DataPointController.LoadDataPoint(type)
        content_items = data_point.tick(self.data_point)
        Logger.Info('%s - DataPointController.run_data_point - finished' % __name__)
        return content_items

    @classmethod
    def LoadDataPoint(cls, data_point_name):
        Logger.Info('%s - DataPointController.LoadDataPoint - started' % __name__)
        Logger.Debug('%s - DataPointController.LoadDataPoint - started with data_point_name:%s' % (__name__, data_point_name))
        def custom_import(name):
            mod = __import__(name)
            components = name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod
        data_point = custom_import('dashboard.datapoints.lib.%s.datapoint' % data_point_name)
        data_point = getattr(data_point, 'DataPoint')()
        Logger.Info('%s - DataPointController.LoadDataPoint - finished' % __name__)
        return data_point

    
class MetaLayerAggregatorController(object):
    @classmethod
    def _call_aggregator(cls, add_source_endpoint_url, config, sub_type, type):
        Logger.Info('%s - MetaLayerAggregatorController._call_aggregator - started' % __name__)
        Logger.Debug('%s - MetaLayerAggregatorController._call_aggregator - started with add_source_endpoint_url:%s and config:%s and sub_type:%s and type:%s' % (__name__, add_source_endpoint_url, config, sub_type, type))
        source = {'type': type, 'config': config}
        if sub_type:
            source['sub_type'] = sub_type
        data = urlencode({'source': json.dumps(source)})
        request = Request(add_source_endpoint_url, data)
        try:
            response = urlopen(request).read()
            response = json.loads(response)
            status = response['status']
        except Exception, e:
            Logger.Error('%s - MetaLayerAggregatorController._call_aggregator - Error:%s while contacting url:%s' % (__name__, e, add_source_endpoint_url))
            status = 'failure'
        Logger.Info('%s - MetaLayerAggregatorController._call_aggregator - finished' % __name__)
        return status

    @classmethod
    def AddSourceToAggregator(cls, type, sub_type, config):
        Logger.Info('%s - MetaLayerAggregatorController.AddSourceToAggregator - started' % __name__)
        Logger.Debug('%s - MetaLayerAggregatorController.AddSourceToAggregator - started with config:%s and sub_type:%s and type:%s' % (__name__, config, sub_type, type))
        add_source_endpoint_url = settings.ENDPOINTS['datapoints']['metalayer_aggregator']['add_source']
        status = cls._call_aggregator(add_source_endpoint_url, config, sub_type, type)
        if status == 'failure':
            Logger.Error('%s MetaLayerAggregatorController.AddSourceToAggregator - Error type = %s, config = %s, sub_type = %s' % (__name__, type, json.dumps(config), sub_type))
        Logger.Info('%s - MetaLayerAggregatorController.AddSourceToAggregator - finished' % __name__)

    @classmethod
    def RemoveSourceFromAggregator(cls, type, sub_type, config):
        Logger.Info('%s - MetaLayerAggregatorController.RemoveSourceFromAggregator - started' % __name__)
        Logger.Debug('%s - MetaLayerAggregatorController.RemoveSourceFromAggregator - started with config:%s and sub_type:%s and type:%s' % (__name__, config, sub_type, type))
        remove_source_endpoint_url = settings.ENDPOINTS['datapoints']['metalayer_aggregator']['remove_source']
        status = cls._call_aggregator(remove_source_endpoint_url, config, sub_type, type)
        if status == 'failure':
            Logger.Error('%s MetaLayerAggregatorController.AddSourceToAggregator - Error type = %s, config = %s, sub_type = %s' % (__name__, type, json.dumps(config), sub_type))
        Logger.Info('%s - MetaLayerAggregatorController.RemoveSourceFromAggregator - finished' % __name__)

