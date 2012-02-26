from threading import Thread

def async(gen):
    def func(*args, **kwargs):
        it = gen(*args, **kwargs)
        result = it.next()
        Thread(target=lambda: list(it)).start()
        return result
    return func



class Logger(object):
    @classmethod
    def Error(cls, message):
        import logging
        logger = logging.getLogger(__name__)
        logger.error('USER %s' % message)

    @classmethod
    def Info(cls, message):
        import logging
        logger = logging.getLogger(__name__)
        logger.error('USER %s' % message)

    @classmethod
    def Debug(cls, message):
        import logging
        logger = logging.getLogger(__name__)
        logger.error('USER %s' % message)