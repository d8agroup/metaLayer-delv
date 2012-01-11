from datapoints.controllers import MetaLayerAggregatorController
from urlparse import urlparse
from hashlib import md5
import feedparser
from logger import Logger

class DataPoint(object):
    def get_unconfigured_config(self):
        return {
            'type':'feed',
            'sub_type':'feed',
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

    def get_content_item_template(self):
        return "" \
            "<li style='width:100%;'>" \
                "<img src='http://imgur.com/images/blog_rss.png' style='width:20px; padding-right:10px;' align='left'/>" \
                "<p style='margin-bottom:2px;'>${source_display_name}</p>" \
                "<p style='padding-left:30px;'>${author_display_name}<span style='font-weight:bold'> ${title}</span></p>" \
            "</li>"

    def generate_configured_guid(self, config):
        url = [e for e in config['elements'] if e['name'] == 'url'][0]['value']
        return md5(url).hexdigest()

    def generate_configured_display_name(self, config):
        url = [e for e in config['elements'] if e['name'] == 'url'][0]['value']
        parsed_url = urlparse(url)
        return 'Web Feed: %s%s' % (parsed_url.netloc, parsed_url.path)

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

    def data_point_added(self, config):
        type = config['type']
        sub_type = config['sub_type']
        config = { 'url':[e for e in config['elements'] if e['name'] == 'url'][0]['value'] }
        MetaLayerAggregatorController.AddSourceToAggregator(type, sub_type, config)

    def data_point_removed(self, config):
        type = config['type']
        sub_type = config['sub_type']
        config = { 'url':[e for e in config['elements'] if e['name'] == 'url'][0]['value'] }
        MetaLayerAggregatorController.RemoveSourceFromAggregator(type, sub_type, config)

    def tick(self, config):
        Logger.Debug('%s - tick - started - with config: %s' % (__name__, config))
        Logger.Debug('%s - tick - finished' % __name__)
        #Tick is controlled by the aggregator
        return []