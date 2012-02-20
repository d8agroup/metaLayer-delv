import datetime
from threading import Thread
from django.conf import settings
from minimongo.model import Model

def async(gen):
    def func(*args, **kwargs):
        it = gen(*args, **kwargs)
        result = it.next()
        Thread(target=lambda: list(it)).start()
        return result
    return func



class Logger(object):
    @classmethod
    @async
    def Error(cls, message):
        if settings.DB_LOGGING:
            yield
            if settings.DB_LOGGING['logging_level'] >= 0:
                LogMessage.Create('ERROR', message)
        else:
            import logging
            logger = logging.getLogger(__name__)
            logger.error('USER %s' % message)
            yield

    @classmethod
    @async
    def Info(cls, message):
        if settings.DB_LOGGING:
            yield
            if settings.DB_LOGGING['logging_level'] > 0:
                LogMessage.Create('INFO', message)
        else:
            import logging
            logger = logging.getLogger(__name__)
            logger.error('USER %s' % message)
            yield

    @classmethod
    @async
    def Debug(cls, message):
        if settings.DB_LOGGING:
            yield
            if settings.DB_LOGGING['logging_level'] > 1:
                LogMessage.Create('DEBUG', message)
        else:
            import logging
            logger = logging.getLogger(__name__)
            logger.error('USER %s' % message)
            yield


class LogMessage(Model):
    host = settings.DB_LOGGING['database_host']
    port = settings.DB_LOGGING['database_port']
    database = settings.DB_LOGGING['database_name']
    collection = 'log_messages'
    #indices = ( Index('username'), )

    @classmethod
    def Create(cls, level, message):
        lm = LogMessage({
            'date':datetime.datetime.utcnow(),
            'level':level,
            'message':message
        })
        lm.save()