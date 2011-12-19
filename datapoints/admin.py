from django.contrib import admin
from datapoints.models import DataPoint

class DataPointAdmin(admin.ModelAdmin):
    pass

admin.site.register(DataPoint, DataPointAdmin)