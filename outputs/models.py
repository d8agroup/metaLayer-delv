import random
import string
from django.conf import settings
from minimongo import Model, Index
from logger import Logger

class ShortUrl(Model):
    class Meta:
        host = settings.DATABASES['default']['HOST']
        port = settings.DATABASES['default']['PORT']
        database = settings.DATABASES['default']['NAME']
        collection = 'outputs_shorturl'
        indices = ( Index('url_identifier'), )

    @classmethod
    def Create(cls, dashboard_id, collection_id, output_id):
        def generate_random_string():
            return "".join( [random.choice(string.letters[:26]) for i in xrange(12)] )
        Logger.Info('%s - ShortUrl.Create - started' % __name__)
        Logger.Debug('%s - ShortUrl.Create - started with dashboard_id:%s and collection_id:%s and output_id:%s' % (__name__, dashboard_id, collection_id, output_id))
        url_identifier = generate_random_string()
        while ShortUrl.collection.find_one({'url_identifier':url_identifier}):
            url_identifier = generate_random_string()
        short_url = ShortUrl({
            'url_identifier':url_identifier,
            'dashboard_id':dashboard_id,
            'collection_id':collection_id,
            'output_id':output_id
        })
        short_url.save()
        Logger.Info('%s - ShortUrl.Create - finished' % __name__)
        return short_url

    @classmethod
    def Load(cls, url_identifier):
        Logger.Info('%s - ShortUrl.Load - started' % __name__)
        Logger.Debug('%s - ShortUrl.Load - started with url_identifier:%s' % (__name__, url_identifier))
        short_url = ShortUrl.collection.find_one({'url_identifier':url_identifier})
        Logger.Info('%s - ShortUrl.Load - finished' % __name__)
        return short_url

    @classmethod
    def Delete(cls, dashboard_id, collection_id, output_id):
        Logger.Info('%s - ShortUrl.Delete - started' % __name__)
        Logger.Info('%s - ShortUrl.Delete - started with dashboard_id:%s and collection_id:%s and output_id:%s' % (__name__, dashboard_id, collection_id, output_id))
        short_url = ShortUrl.collection.find_one({
            'dashboard_id':dashboard_id,
            'collection_id':collection_id,
            'output_id':output_id
        })
        if short_url:
            short_url.remove()
        Logger.Info('%s - ShortUrl.Delete - finished' % __name__)