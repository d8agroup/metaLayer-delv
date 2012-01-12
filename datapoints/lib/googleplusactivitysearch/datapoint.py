from hashlib import md5
from urllib2 import urlopen
from urllib import quote
from aggregator.views import run_aggregator_for_data_point
from logger import Logger
from django.utils import simplejson as json
from dateutil import parser as dateutil_parser
import time

class DataPoint(object):
    def get_unconfigured_config(self):
        return {
            'type':'googleplusactivitysearch',
            'sub_type':'googleplusactivitysearch',
            'short_display_name':'Google+ Search',
            'full_display_name':'Google+ Activity Stream Search',
            'instructions':'Use this data point to search the public Google+ activity stream.',
            'image_large':'http://www.pcsaudavel.com/images/Google-Plus.png',
            'image_small':'http://www.ethankociela.com/images/icons/google-plus.png',
            'configured':False,
            'elements':[
                {
                    'name':'keywords',
                    'display_name':'What to search for',
                    'help':'The keywords or hashtags that you want to use to search Google+',
                    'type':'text',
                    'value':''
                },
                {
                    'name':'api_key',
                    'display_name':'Your Google+ api key',
                    'help':'Searching Google+ requires and api key. If you don\'t have one visit <a href="https://developers.google.com/+/api/" target="_blank">here</a>.',
                    'type':'text',
                    'value':''
                },
            ]
        }

    def get_content_item_template(self):
        return ""\
                "<li style='width:100%;'>"\
                    "<img src='${author_image}' style='width:50px; padding:1px; box-shadow: 3px 3px 3px #333;' align='left' class='helper_corner' />" \
                    "<p style='float:left; padding:2px 0 0 8px;font-weight:bold;width:50%;overflow:hidden;height:12px;'>${author_display_name}</p>"\
                    "<p style='margin-bottom:2px;text-align:right'>"\
                        "<span style='position:relative;bottom:4px;right:10px;'>${pretty_date}</span>"\
                        "<img src='http://www.ethankociela.com/images/icons/google-plus.png' style='width:15px; box-shadow: 2px 2px 3px #333;'/>"\
                    "</p>"\
                    "<p style='padding-left:60px;'>${title}</p>"\
                "</li>"


    def generate_configured_guid(self, config):
        base_string = ' '.join([e['value'] for e in config['elements']])
        return md5(base_string).hexdigest()

    def generate_configured_display_name(self, config):
        keywords = [e for e in config['elements'] if e['name'] == 'keywords'][0]['value']
        return '%s: %s' % (config['short_display_name'], keywords)

    def validate_config(self, config):
        keywords = [e for e in config['elements'] if e['name'] == 'keywords'][0]['value']
        api_key = [e for e in config['elements'] if e['name'] == 'api_key'][0]['value']

        errors = { 'keywords':[], 'api_key':[] }
        if not keywords or not keywords.strip():
            errors['keywords'].append('You must search for something.')

        if not api_key or not api_key.strip():
            errors['api_key'].append('You must provide an api key')

        #TODO should validate the api key here

        if errors['keywords'] or errors['api_key']:
            return False, errors
        return True, {}

    def data_point_added(self, config):
        #todo this is a hack
        run_aggregator_for_data_point(config)
        pass

    def data_point_removed(self, config):
        pass

    def tick(self, config):
        Logger.Debug('%s - tick - started - with config: %s' % (__name__, config))
        api_key = [e for e in config['elements'] if e['name'] == 'api_key'][0]['value']
        keywords = [e for e in config['elements'] if e['name'] == 'keywords'][0]['value']
        keywords = quote(keywords)
        url = 'https://www.googleapis.com/plus/v1/activities?query=%s&pp=1&key=%s' % (keywords, api_key)
        response = urlopen(url).read()
        Logger.Debug('%s - tick - raw response: %s' % (__name__, response))
        response = json.loads(response)
        Logger.Debug('%s - tick - JSON response: %s' % (__name__, response))
        content = [self._map_googleplus_item_to_content_item(config, item) for item in response['items']]
        Logger.Debug('%s - tick - finished' % __name__)
        return content

    def _map_googleplus_item_to_content_item(self, config, item):
        return {
            'id':item['id'],
            'text':[ { 'title':item['title'], } ],
            'time': time.mktime(dateutil_parser.parse(item['updated']).timetuple()),
            'link':item['url'],
            'author':{
                'display_name':item['actor']['displayName'],
                'link':item['actor']['url'],
                'image':item['actor']['image']['url']
            },
            'channel':{
                'id':md5(config['type'] + config['sub_type']).hexdigest(),
                'type':config['type'],
                'sub_type':config['sub_type']
            },
            'source':{
                'id':self.generate_configured_guid(config),
                'display_name':self.generate_configured_display_name(config),
            }
        }