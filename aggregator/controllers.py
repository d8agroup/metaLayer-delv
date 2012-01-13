from Queue import Queue
import threading
import urllib2
from django.conf import settings
from dashboards.controllers import DashboardsController
from datapoints.controllers import DataPointController
from logger import Logger
from userprofiles.controllers import UserController
from django.utils import simplejson as json

class AggregationController(object):
    def __init__(self):
        self.users = UserController.GetAllUsers()

    def aggregate(self):
        def producer(q, users):
            for user in users:
                thread = _UserThread(user)
                thread.start()
                q.put(thread, True)
        q = Queue(3)
        producer_thread = threading.Thread(target=producer, args=(q, self.users))
        producer_thread.start()

    @classmethod
    def AggregateSingleDataPoint(cls, data_point):
        run_aggregator_for_data_point(data_point)

class _UserThread(threading.Thread):
    def __init__(self, user):
        self.user = user
        threading.Thread.__init__(self)

    def run(self):
        all_data_points = []
        dc = DashboardsController(self.user)
        for dashboard in dc.get_saved_dashboards():
            for collection in dashboard['collections']:
                for data_point in collection['data_points']:
                    all_data_points.append(data_point)
        def producer(q, data_points):
            for data_point in data_points:
                thread = _DataPointThread(data_point)
                thread.start()
                q.put(thread, True)
        q = Queue(3)
        producer_thread = threading.Thread(target=producer, args=(q, all_data_points))
        producer_thread.start()

class _DataPointThread(threading.Thread):
    def __init__(self, data_point):
        self.data_point = data_point
        threading.Thread.__init__(self)

    def run(self):
        run_aggregator_for_data_point(self.data_point)


def run_aggregator_for_data_point(data_point):
    dpc = DataPointController(data_point)
    content = dpc.run_data_point()
    content = [_parse_content_item(item) for item in content]
    solr_url = settings.SOLR_CONFIG['solr_url']
    request_data = json.dumps(content)
    Logger.Debug('%s - run_all_dashboards - posting the following to solr: %s' % (__name__, request_data))
    request = urllib2.Request('%s/update/json/?commit=true' % solr_url, request_data, {'Content-Type': 'application/json'})
    response = urllib2.urlopen(request)
    response_stream = response.read()
    Logger.Debug('%s - run_all_dashboards - solr returned: %s' % (__name__, response_stream))

def _parse_content_item(content_item):
    return_data = {}
    for key in ['id', 'time', 'link']:
        if key in content_item and content_item[key]:
            return_data[key] = content_item[key]
    return_data.update(_map_text_from_content_item(content_item['text']))
    if 'author' in content_item:
        for key in ['display_name', 'link', 'image']:
            if key in content_item['author']:
                return_data['author_%s' % key] = content_item['author'][key]
    if 'channel' in content_item:
        for key in ['id', 'type', 'sub_type']:
            if key in content_item['channel']:
                return_data['channel_%s' % key] = content_item['channel'][key]
    if 'source' in content_item:
        for key in ['id', 'id_string', 'display_name']:
            if key in content_item['source']:
                return_data['source_%s' % key] = content_item['source'][key]
    return return_data

def _map_text_from_content_item(text_array):
    #TODO For now this does not support multi language
    if not len(text_array):
        return {}
    text = text_array[0]
    return_data = {}
    for key in ['language', 'title', 'text', 'tags']:
        if key in text and text[key]:
            return_data[key] = text[key]
    return return_data