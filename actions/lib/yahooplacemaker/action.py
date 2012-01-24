from Queue import Queue
import json
import threading
from urllib import urlencode
from urllib2 import Request, urlopen
import re
from actions.classes import BaseAction

class Action(BaseAction):
    def get_unconfigured_config(self):
        return {
            'name':'yahooplacemaker',
            'display_name_short':'Location',
            'display_name_long':'Yahoo Placemaker Location Detection',
            'image_large':'http://webmail.mozdev.org/images/misc/Yahoo-SmallIcon.png',
            'image_small':'http://webmail.mozdev.org/images/misc/Yahoo-SmallIcon.png',
            'instructions':'Yahoo Placemaker will extract location based information from content allowing you to visualize content on a map',
            'configured':False,
            'elements':[
                {
                    'name':'api_key',
                    'display_name':'Your Yahoo API key',
                    'help':'Using Yahoo Placemaker requires an API key, if you don\'t have one, visit <a href="http://developer.yahoo.com/geo/placemaker/" target="_blank">here</a>',
                    'type':'text',
                    'value':''
                },
                {
                    'name':'collection_type',
                    'display_name':'Location type',
                    'help':'Choose the type of location data to collect',
                    'type':'select',
                    'values':[
                        'Countries',
                        'Places'
                    ],
                    'value':''

                }
            ],
            'content_properties':{
                'added':[
                    {
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
            api_key = [e for e in self.config['elements'] if e['name'] == 'api_key'][0]['value']
            url = 'http://wherein.yahooapis.com/v1/document'
            post_data = urlencode({ 'documentContent':text, 'documentType':'text/plain', 'outputType':'json', 'appid':api_key })
            request = Request(url, post_data)
            response = urlopen(request)
            response = json.loads(response.read())
            result = self._map_location(self.config, response)
            self.result = result
        except Exception, e:
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
        collection_type = [e for e in config['elements'] if e['name'] == 'collection_type'][0]['value']
        if collection_type == 'Countries':
            potential_countries = [c for c in response['document']['localScopes']['localScope']['ancestors'] if c['ancestor']['type'] == 'Country']
            if potential_countries:
                return potential_countries[0]['ancestor']['name']
            return False
        location = response['document']['localScopes']['localScope']['name']
        location = re.sub(r'\(\w+\)', '', location).strip()
        return location


