from django.utils import simplejson
from dateutil import parser as dateutil_parser
from hashlib import md5
import feedparser
import random
import urllib2
import urllib
import time
import re

class twittersearch(object):
    def source_data(self):
        return {
            'type':'twittersearch',
            'display_name':'Twitter Search',
        }
    
    def run_for_input(self, input_config):
        search = input_config['config']['elements'][0]['value']
        tweets = simplejson.loads(urllib2.urlopen('http://search.twitter.com/search.json?rpp=50&q=%s' % urllib.quote(search)).read())
        return [
            {
                'type':'twittersearch',
                'time':int(time.mktime(dateutil_parser.parse(tweet['created_at']).timetuple())),
                'image_url':tweet['profile_image_url'],
                'author':tweet['from_user'],
                'title':tweet['text'],
                'text':''
            } for tweet in tweets['results']]
    
    def parse_request_to_config(self, request):
        return {
            'id':request.GET['id'],
            'type':'twittersearch', 
            'display_name':'Twitter Search for: %s' % request.GET['search'],
            'config':{
                'configured':True,
                'elements':[
                    { 'name':'search', 'display_name':'Keywords', 'type':'text', 'value':request.GET['search']}
                ]
            }
        }
        
    def generate_unconfigured_config(self):
        return {
            'id':md5('%s' % random.random()).hexdigest(),
            'type':'twittersearch', 
            'display_name':'Twitter Search',
            'config':{ 
                'configured':False,
                'elements':[
                    { 'name':'search', 'display_name':'Keywords', 'type':'text' }
                ]
            }
        }

  
class twitteruser(object):
    def source_data(self):
        return { 'type':'twitteruser', 'display_name':'Twitter User' }
    
    def run_for_input(self, input_config):
        user_name = input_config['config']['elements'][0]['value']
        tweets = simplejson.loads(urllib2.urlopen('http://search.twitter.com/search.json?rpp=50&q=from:%s' % urllib.quote(user_name)).read())
        return [
            {
                'type':'twitteruser',
                'time':int(time.mktime(dateutil_parser.parse(tweet['created_at']).timetuple())),
                'image_url':tweet['profile_image_url'],
                'author':tweet['from_user'],
                'title':tweet['text'],
                'text':''
            } for tweet in tweets['results']]
    
    def parse_request_to_config(self, request):
        return {
            'id':request.GET['id'],
            'type':'twitteruser', 
            'display_name':'Twitter User: %s' % request.GET['user_name'],
            'config':{
                'configured':True,
                'elements':[
                    { 'name':'user_name', 'display_name':'User Name', 'type':'text', 'value':request.GET['user_name']}
                ]
            }
        }
        
    def generate_unconfigured_config(self):
        return {
            'id':md5('%s' % random.random()).hexdigest(),
            'type':'twitteruser', 
            'display_name':'Twitter User',
            'config':{ 
                'configured':False,
                'elements':[
                    { 'name':'user_name', 'display_name':'User Name', 'type':'text' }
                ]
            }
        }
              
        
class feed(object):
    def source_data(self):
        return {
            'type':'feed',
            'display_name':'RSS/ATOM',
        }
    
    def run_for_input(self, input_config):
        feed_url = input_config['config']['elements'][0]['value']
        feed = feedparser.parse(feed_url)
        return [
            {
                'type':'twittersearch',
                'time':int(time.mktime(dateutil_parser.parse(item['date']).timetuple())),
                'image_url':'/media/images/icon-feed.png',
                'author':'',
                'title':item['title'],
                'text':''
            } for item in feed['items']]
    
    def parse_request_to_config(self, request):
        return {
            'id':request.GET['id'],
            'type':'feed', 
            'display_name':'Feed for: %s' % request.GET['feed_url'],
            'config':{
                'configured':True,
                'elements':[
                    { 'name':'feed_url', 'display_name':'Feed URL', 'type':'text', 'value':request.GET['feed_url']}
                ]
            }
        }
        
    def generate_unconfigured_config(self):
        return {
            'id':md5('%s' % random.random()).hexdigest(),
            'type':'feed', 
            'display_name':'Feed URL',
            'config':{ 
                'configured':False,
                'elements':[
                    { 'name':'feed_url', 'display_name':'Feed URL', 'type':'text' }
                ]
            }
        }
        

class googlenews(object):
    def source_data(self):
        return {
            'type':'googlenews',
            'display_name':'Google News',
        }
    
    def run_for_input(self, input_config):
        feed_url = 'http://news.google.com/news?hl=en&gl=us&q=%s&safe=on&output=rss' % input_config['config']['elements'][0]['value']
        feed = feedparser.parse(feed_url)
        return [
            {
                'type':'googlenews',
                'time':int(time.mktime(dateutil_parser.parse(item['date']).timetuple())),
                'image_url':'/media/images/icon-googlenews.png',
                'author':'',
                'title':item['title'],
                'text':''
            } for item in feed['items']]
    
    def parse_request_to_config(self, request):
        return {
            'id':request.GET['id'],
            'type':'googlenews', 
            'display_name':'Google News Search for: %s' % request.GET['search'],
            'config':{
                'configured':True,
                'elements':[
                    { 'name':'search', 'display_name':'Keywords', 'type':'text', 'value':request.GET['search']}
                ]
            }
        }
        
    def generate_unconfigured_config(self):
        return {
            'id':md5('%s' % random.random()).hexdigest(),
            'type':'googlenews', 
            'display_name':'Google News Search',
            'config':{ 
                'configured':False,
                'elements':[
                    { 'name':'search', 'display_name':'Keywords', 'type':'text' }
                ]
            }
        }
        
class gmail(object):
    def source_data(self):
        return {
            'type':'gmail',
            'display_name':'Google Mail',
        }
    
    def run_for_input(self, input_config):
        user_name = input_config['config']['elements'][0]['value']
        password = input_config['config']['elements'][1]['value']
        from lib.gmail import extract_email_subjects
        emails = extract_email_subjects(user_name, password)
        return [
            {
                'type':'gmail',
                'time':int(time.mktime(dateutil_parser.parse(item['date']).timetuple())),
                'image_url':'/media/images/icon-gmail.png',
                'author':'',
                'title':item['subject'],
                'text':''
            } for item in emails]
    
    def parse_request_to_config(self, request):
        user_name = request.GET['user_name'] if re.search('@', request.GET['user_name']) else request.GET['user_name'] + "@gmail.com"
        return {
            'id':request.GET['id'],
            'type':'gmail', 
            'display_name':'Google Mail: %s' % user_name,
            'config':{
                'configured':True,
                'elements':[
                    { 'name':'user_name', 'display_name':'Username', 'type':'text', 'value':user_name },
                    { 'name':'password', 'display_name':'Password', 'type':'password', 'value':request.GET['password'] }
                ]
            }
        }
        
    def generate_unconfigured_config(self):
        return {
            'id':md5('%s' % random.random()).hexdigest(),
            'type':'gmail', 
            'display_name':'Google Mail',
            'config':{ 
                'configured':False,
                'elements':[
                    { 'name':'user_name', 'display_name':'Username', 'type':'text' },
                    { 'name':'password', 'display_name':'Password', 'type':'password' }
                ]
            }
        }