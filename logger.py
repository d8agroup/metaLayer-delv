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
    @async
    def Error(cls, message, request=None, exception=None):
        yield
        import logging
        logger = logging.getLogger(__name__)
        if not request:
            logger.error('USER %s' % message, exc_info=True)
            if exception:
                logger.error(exception, exc_info=True)
        else:
            logger.error('USER %s' % message, exc_info=True, extra={'request':request})
            if exception:
                logger.error(exception, exc_info=True, extra={'request':request})

    @classmethod
    @async
    def Warn(cls, message, request=None, exception=None):
        yield
        import logging
        logger = logging.getLogger(__name__)
        if not request:
            logger.warn('USER %s' % message, exc_info=True)
            if exception:
                logger.warn(exception, exc_info=True)
        else:
            logger.warn('USER %s' % message, exc_info=True, extra={'request':request})
            if exception:
                logger.warn(exception, exc_info=True, extra={'request':request})

    @classmethod
    @async
    def Info(cls, message):
        yield
        import logging
        logger = logging.getLogger(__name__)
        logger.info('USER %s' % message)

    @classmethod
    @async
    def Debug(cls, message):
        yield
        import logging
        logger = logging.getLogger(__name__)
        logger.debug('USER %s' % message)