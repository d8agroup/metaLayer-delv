from Queue import Queue
import json
import threading
from urllib import urlencode
from urllib2 import Request, urlopen
from actions.classes import BaseAction

class Action(BaseAction):
    def get_unconfigured_config(self):
        return {
            'name':'datalayersentimentanalysis',
            'display_name_short':'Sentiment',
            'display_name_long':'Sentiment Analysis',
            'image_large':'/static/images/thedashboard/actions/sentiment_large.png',
            'image_small':'/static/images/thedashboard/actions/sentiment_small.png',
            'instructions':'This actions does not need configuring.',
            'configured':True,
            'elements':[],
            'content_properties':{
                'added':[
                    {
                        'display_name':'Sentiment',
                        'name':'sentiment',
                        'type':'string'
                    }
                ]
            }
        }

    def run(self, config, content):
        def producer(q, content):
            for item in content:
                thread = SentimentGetter(item)
                thread.start()
                q.put(thread, True)
        finished = []
        def consumer(q, content_count):
            while len(finished) < content_count:
                thread = q.get(True)
                thread.join()
                content_id, sentiment = thread.get_result()
                finished.append({'id':content_id, 'sentiment':sentiment})
        q = Queue(3)
        producer_thread = threading.Thread(target=producer, args=(q, content))
        consumer_thread = threading.Thread(target=consumer, args=(q, len(content)))
        producer_thread.start()
        consumer_thread.start()
        producer_thread.join()
        consumer_thread.join()
        return finished

class SentimentGetter(threading.Thread):
    def __init__(self, content):
        self.content = content
        self.result = None
        threading.Thread.__init__(self)

    def get_result(self):
        return self.content['id'], self.result

    def run(self):
        try:
            text = self.extract_content()
            text = text.encode('ascii', 'ignore')
            url = 'http://50.57.101.174/getsentiment'
            post_data = urlencode({ 'text':text })
            request = Request(url, post_data)
            response = json.loads(urlopen(request).read())
            self.result = self._map_sentiment(response['sentiment']) if response['status'] == 'success' else False
            """
            text = self.extract_content()
            text = text.encode('ascii', 'ignore')
            url = 'http://api.metalayer.com/s/dashboard/1/sentiment'
            post_data = urlencode({ 'text':text })
            request = Request(url, post_data)
            response = urlopen(request)
            response = json.loads(response.read())
            self.result = self._map_sentiment(response['response']['datalayer']['sentiment']) if response['status'] == 'success' else False
            """
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

    def _map_sentiment(self, sentiment):
        if sentiment >= 0.5:
            return 'positive'
        elif sentiment <= 0.5:
            return 'negative'
        return 'neutral'

