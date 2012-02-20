from Queue import Queue
import json
import threading
from urllib import urlencode
from urllib2 import Request, urlopen
from actions.classes import BaseAction
from logger import Logger

class Action(BaseAction):
    def get_unconfigured_config(self):
        return {
            'name':'yahooplacemaker',
            'display_name_short':'Location',
            'display_name_long':'Location Detection',
            'image_large':'/static/images/thedashboard/actions/location_small.png',
            'image_small':'/static/images/thedashboard/actions/location_small.png',
            'instructions':'Yahoo Placemaker will extract location based information from content allowing you to visualize content on a map',
            'configured':False,
            'elements':[
                {
                    'name':'api_key',
                    'display_name':'Your Yahoo API key',
                    'help':'Using Yahoo Placemaker requires an API key, to get one or change your\'s, click '
                           '<a href="http://developer.yahoo.com/geo/placemaker/" target="_blank">here</a>'
                           '<br/><br/>'
                           '<span class="extra">Getting a Yahoo Placemaker API Key is a little tricky but nothing to '
                           'worry about.'
                           '<br/><br/> '
                           'First click on the link above and sign in with your Yahoo, Google or '
                           'Facebook id. <br/>On the next screen you can enter "metalayer" for the application name, '
                           'description and Application Owner (at the bottom). <br/>Then enter "http://metalayer.com" for '
                           'the Application URL and Application domain and "http://metalayer.com/favicon.ico" for the '
                           'Favicon URL. <br/>Finally enter "support@metalayer.com" for the Contact email. Then on the next '
                           'screen, copy the api into the box above and click "Save and Exit".<br/><br/> '
                           'You can of cause use your own details while singing up for an API key with Yahoo if you '
                           'want to.</span>',
                    'type':'api_key',
                    'value':''
                }
            ],
            'content_properties':{
                'added':[
                    {
                        'display_name':'Yahoo Placemaker Location',
                        'name':'location',
                        'type':'location_string',
                    }
                ]
            }
        }

    def validate_config(self, config):
        api_key = [e for e in config['elements'] if e['name'] == 'api_key'][0]['value']

        errors = { 'api_key':[] }
        if not api_key or not api_key.strip():
            errors['api_key'].append('You must provide an api key')

        #TODO should validate the api key here

        if errors['api_key']:
            return False, errors
        return True, {}

    def run(self, config, content):
        def producer(q, config, content):
            for item in content:
                thread = LocationGetter(config, item)
                thread.start()
                q.put(thread, True)
        finished = []
        def consumer(q, content_count):
            while len(finished) < content_count:
                thread = q.get(True)
                thread.join()
                content_id, location = thread.get_result()
                finished.append({'id':content_id, 'location':location})
        q = Queue(3)
        producer_thread = threading.Thread(target=producer, args=(q, config, content))
        consumer_thread = threading.Thread(target=consumer, args=(q, len(content)))
        producer_thread.start()
        consumer_thread.start()
        producer_thread.join()
        consumer_thread.join()
        return finished

class LocationGetter(threading.Thread):
    def __init__(self, config, content):
        self.config = config
        self.content = content
        self.result = None
        threading.Thread.__init__(self)

    def get_result(self):
        return self.content['id'], self.result

    def run(self):
        try:
            text = self.extract_content()
            text = text.encode('ascii', 'ignore')
            api_key = [e for e in self.config['elements'] if e['name'] == 'api_key'][0]['value']
            url = 'http://wherein.yahooapis.com/v1/document'
            post_data = urlencode({ 'documentContent':text, 'documentType':'text/plain', 'outputType':'json', 'appid':api_key})
            request = Request(url, post_data)
            response = urlopen(request)
            response = json.loads(response.read())
            Logger.Debug('%s - LocationGetter.run - sent to Yahoo:%s' % (__name__, text))
            Logger.Debug('%s - LocationGetter.run - return from Yahoo:%s' % (__name__, response))
            result = self._map_location(self.config, response)
            Logger.Debug('%s - LocationGetter.run - mapped location from Yahoo:%s' % (__name__, result))
            self.result = result
        except Exception, e:
            Logger.Error('%s - LocationGetter.run - error:%s' % (__name__, e))
            self.result = None

    def extract_content(self):
        text = ''
        if 'title' in self.content:
            text += ' ' + self.content['title']
        if 'text' in self.content:
            for t in self.content['text']:
                text += ' ' + t
        return text

    def _map_location(self, config, response):
        def countries(a,v):
            if isinstance(a, dict):
                if 'type' in a and a['type'] == 'Country':
                    if 'name' in a and a['name'] not in v:
                        v.append(a['name'])
                for key in a.keys():
                    countries(a[key], v)
            elif isinstance(a, list):
                for b in a:
                    countries(b, v)
            else:
                return
        def places(a,v):
            if isinstance(a, dict):
                if 'type' in a and a['type'] != 'Country':
                    if 'name' in a and a['name'] not in v:
                        v.append(a['name'])
                for key in a.keys():
                    places(a[key], v)
            elif isinstance(a, list):
                for b in a:
                    places(b, v)
            else:
                return

        if not isinstance(response['document'], dict):
            return False
        #collection_type = [e for e in config['elements'] if e['name'] == 'collection_type'][0]['value']
        locations = []
        countries(response, locations)
        places(response, locations)
        return locations
        """
        if collection_type == 'Countries':
            locations = []
            countries(response, locations)
            return sorted(locations)[0] if locations else False
        else:
            locations = []
            places(response, locations)
            return sorted(locations)[0] if locations else False
        """

