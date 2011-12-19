from urlparse import urlparse
import feedparser
from datapoints.controllers import MetaLayerAggregatorController

class DataPoint(object):
    def get_unconfigured_config(self):
        return {
            'type':'webfeed',
            'short_display_name':'Web Feed',
            'full_display_name':'Web Feed (rss/atom)',
            'instructions':'Use this data point to subscribe to any web feed published using either rss or atom syndication.',
            'image_large':'http://app.moogo.com/files/moogowebsite_copy.moogo.com/images/Blog/2010-06-15/rss-feed.png',
            'image_small':'http://imgur.com/images/blog_rss.png',
            'configured':False,
            'elements':[
                {
                    'name':'url',
                    'display_name':'The feed url',
                    'help':'The full url of the feed you want to subscribe to',
                    'type':'text',
                    'value':''
                }
            ]
        }

    def validate_config(self, config):
        url = [e for e in config['elements'] if e['name'] == 'url'][0]['value']
        if not url or url == '':
            return False, { 'url':['Url can not be empty'] }
        parsed_url = urlparse(url)
        if parsed_url.netloc == '':
            return False, { 'url':['The url did not parse correctly, it must be a full url'] }
        feed = feedparser.parse(url)
        if not feed['feed']:
            return False, { 'url':['This url does not seem to point to a feed?'] }
        return True, {}

    def save_config(self, config):
        type = config['type']
        config = { 'url':[e for e in config['elements'] if e['name'] == 'url'][0]['value'] }
        MetaLayerAggregatorController.AddSourceToAggregator(type, config)

    def remove_config(self, config):
        type = config['type']
        config = { 'url':[e for e in config['elements'] if e['name'] == 'url'][0]['value'] }
        MetaLayerAggregatorController.RemoveSourceFromAggregator(type, config)

    def tick(self, config):
        #Tick is controlled by the aggregator
        pass