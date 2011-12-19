from django.db import models

class DataPoint(models.Model):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.display_name

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

    def load_configuration(self):
        data_point = DataPoint.LoadDataPoint(self.name)
        return data_point.get_unconfigured_config()
