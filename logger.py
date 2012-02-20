from minimongo.model import Model

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
        logger.info('USER %s' % message)

    @classmethod
    def Debug(cls, message):
        import logging
        logger = logging.getLogger(__name__)
        logger.debug('USER %s' % message)


class LogMessage(Model):
