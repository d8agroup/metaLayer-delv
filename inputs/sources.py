from django.utils import simplejson
from dateutil import parser as dateutil_parser
from hashlib import md5
from core.models import CacheEntry
import datetime
import feedparser
import random
import urllib2
import urllib
import time
import re

def safe_json_dumps(obj):
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    return simplejson.dumps(obj, default=dthandler)

class twittersearch(object):
    def source_data(self):
        return {
            'type':'twittersearch',
            'display_name':'Twitter Search',
        }
    
    def run_for_input(self, input_config):
        search = input_config['config']['elements'][0]['value']
        cache_key = 'twittersearch_%s' % search
        
        try:
            cache_entry = CacheEntry.objects.get(key=cache_key)
            if int(time.time()) - cache_entry.time > 120:
                cache_entry.delete()
                raise CacheEntry.DoesNotExist
            tweets = simplejson.loads(cache_entry.cache)
        except CacheEntry.DoesNotExist:
            raw_json = urllib2.urlopen('http://search.twitter.com/search.json?rpp=50&q=%s' % urllib.quote(search)).read()
            tweets = simplejson.loads(raw_json)
            cache_entry = CacheEntry()
            cache_entry.cache = raw_json
            cache_entry.key = cache_key
            cache_entry.time = int(time.time())
            cache_entry.save()
            
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
        cache_key = 'twitteruser_%s' % user_name
        
        try:
            cache_entry = CacheEntry.objects.get(key=cache_key)
            if int(time.time()) - cache_entry.time > 120:
                cache_entry.delete()
                raise CacheEntry.DoesNotExist
            tweets = simplejson.loads(cache_entry.cache)
        except CacheEntry.DoesNotExist:
            raw_json = urllib2.urlopen('http://search.twitter.com/search.json?rpp=50&q=from:%s' % urllib.quote(user_name)).read()
            tweets = simplejson.loads(raw_json)
            cache_entry = CacheEntry()
            cache_entry.cache = raw_json
            cache_entry.key = cache_key
            cache_entry.time = int(time.time())
            cache_entry.save()

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
        cache_key = 'fee_%s' % md5(feed_url).hexdigest(),
        
        try:
            cache_entry = CacheEntry.objects.get(key=cache_key)
            if int(time.time()) - cache_entry.time > 120:
                cache_entry.delete()
                raise CacheEntry.DoesNotExist
            items = simplejson.loads(cache_entry.cache)
        except CacheEntry.DoesNotExist:
            items = [{'title':i['title'], 'date':int(time.mktime(dateutil_parser.parse(i['date']).timetuple())) } for i in feedparser.parse(feed_url)['items']]
            cache_entry = CacheEntry()
            cache_entry.cache = safe_json_dumps(items)
            cache_entry.key = cache_key
            cache_entry.time = int(time.time())
            cache_entry.save()
            
        return [
            {
                'type':'feed',
                'time':int(item['date']),
                'image_url':'/media/images/icon-feed.png',
                'author':'',
                'title':item['title'],
                'text':''
            } for item in items]
    
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
        cache_key = 'googlenews_%s' % md5(feed_url).hexdigest(),
        
        try:
            cache_entry = CacheEntry.objects.get(key=cache_key)
            if int(time.time()) - cache_entry.time > 120:
                cache_entry.delete()
                raise CacheEntry.DoesNotExist
            items = simplejson.loads(cache_entry.cache)
        except CacheEntry.DoesNotExist:
            items = [{'title':i['title'], 'date':int(time.mktime(dateutil_parser.parse(i['date']).timetuple())) } for i in feedparser.parse(feed_url)['items']]
            cache_entry = CacheEntry()
            cache_entry.cache = safe_json_dumps(items)
            cache_entry.key = cache_key
            cache_entry.time = int(time.time())
            cache_entry.save()
            
        return [
            {
                'type':'googlenews',
                'time':int(item['date']),
                'image_url':'/media/images/icon-googlenews.png',
                'author':'',
                'title':item['title'],
                'text':''
            } for item in items]
    
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
        cache_key = 'gmail_%s' % user_name
        
        from lib.gmail import extract_email_subjects
        
        try:
            cache_entry = CacheEntry.objects.get(key=cache_key)
            if int(time.time()) - cache_entry.time > 120:
                cache_entry.delete()
                raise CacheEntry.DoesNotExist
            emails = simplejson.loads(cache_entry.cache)
        except CacheEntry.DoesNotExist:
            emails = extract_email_subjects(user_name, password)
            cache_entry = CacheEntry()
            cache_entry.cache = safe_json_dumps(emails)
            cache_entry.key = cache_key
            cache_entry.time = int(time.time())
            cache_entry.save()

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
        
class flickrsearch(object):
    def source_data(self):
        return { 'type':'flickrsearch', 'display_name':'Flickr Search' }
    
    def run_for_input(self, input_config):
        search = input_config['config']['elements'][0]['value']
        cache_key = 'flickrsearch_%s' % search
        
        try:
            cache_entry = CacheEntry.objects.get(key=cache_key)
            if int(time.time()) - cache_entry.time > 120:
                cache_entry.delete()
                raise CacheEntry.DoesNotExist
            pics = simplejson.loads(cache_entry.cache)
        except CacheEntry.DoesNotExist:
            raw_json = urllib2.urlopen('http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=ff9c57320434f28ec322da1838161da6&text=%s&format=json&nojsoncallback=1&sort=date-posted-desc&extras=date_upload,tags' % urllib.quote(search)).read()
            pics = simplejson.loads(raw_json)
            cache_entry = CacheEntry()
            cache_entry.cache = raw_json
            cache_entry.key = cache_key
            cache_entry.time = int(time.time())
            cache_entry.save()
        return [
            {
                'type':'flickrsearch',
                'time':int(pic['dateupload']),
                'image_url':'http://farm%i.static.flickr.com/%s/%s_%s_s.jpg' % (pic['farm'], pic['server'], pic['id'], pic['secret']),
                'author':'',
                'title':pic['title'] + " ".join([tag for tag in pic['tags'].split() if not re.search(':', tag)]),
                'text':'',
            } for pic in pics['photos']['photo']]
    
    def parse_request_to_config(self, request):
        return {
            'id':request.GET['id'],
            'type':'flickrsearch', 
            'display_name':'Flickr Search for: %s' % request.GET['search'],
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
            'type':'flickrsearch', 
            'display_name':'Flickr Search',
            'config':{ 
                'configured':False,
                'elements':[
                    { 'name':'search', 'display_name':'Keywords', 'type':'text' }
                ]
            }
        }