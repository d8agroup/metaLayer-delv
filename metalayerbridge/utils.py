from metalayerbridge.models import SentimentCache, TaggingCache
from django.utils import simplejson
from hashlib import md5 
import urllib, urllib2

from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers
import urllib
import StringIO

def get_sentiment_from_text(text):
    text = unicode(text).encode('ascii', 'ignore')
    text_hash = md5(text).hexdigest()
    try:
        return_data = float(SentimentCache.objects.get(text_hash=text_hash).sentiment)
        return return_data
    except SentimentCache.DoesNotExist:
        data = { 'text':text }
        request = urllib2.Request('http://api.metalayer.com/s/dashboard/1/sentiment', data=urllib.urlencode(data))
        response = simplejson.loads(urllib2.urlopen(request).read())
        sentiment = "%s" % response['response']['datalayer']['sentiment']
        cache = SentimentCache()
        cache.text_hash = text_hash
        cache.sentiment = sentiment
        cache.save()
        return float(sentiment)
    
def get_tags_from_text(text):
    text = unicode(text).encode('ascii', 'ignore')
    text_hash = md5(text).hexdigest()
    try:
        return_data = simplejson.loads(TaggingCache.objects.get(text_hash=text_hash).json)
        return return_data
    except TaggingCache.DoesNotExist:
        data = { 'text':text }
        request = urllib2.Request('http://api.metalayer.com/s/dashboard/1/tagging', data=urllib.urlencode(data))
        response = simplejson.loads(urllib2.urlopen(request).read())
        tags = response['response']['datalayer']['tags']
        cache = TaggingCache()
        cache.text_hash = text_hash
        cache.json = simplejson.dumps(tags)
        cache.save()
        return tags
    
def get_faces_from_image(image_url):
    image_hash = md5(image_url).hexdigest()
    try:
        return_data = simplejson.loads(TaggingCache.objects.get(text_hash=image_hash).json)
    except TaggingCache.DoesNotExist:
        register_openers()
        image = StringIO.StringIO(urllib.urlopen(image_url).read())
        image_id = 'temp'
        items = []
        items.append(MultipartParam(name='image_id', value=image_id))
        items.append(MultipartParam(name='image', filename='image.tiff', fileobj=image))
        datagen, headers = multipart_encode(items)
        request = urllib2.Request('http://api.metalayer.com/s/imglayer/1/dashboardfaces', datagen, headers)
        raw_json = urllib2.urlopen(request).read()
        cache = TaggingCache()
        cache.text_hash = image_hash
        cache.json = raw_json
        cache.save()
        return_data = simplejson.loads(raw_json)
    return len(return_data['response']['objectdetection']['faces']) > 0
    