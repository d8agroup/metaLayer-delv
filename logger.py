class Logger(object):
    @classmethod
    def Error(cls, message):
        import logging
        logger = logging.getLogger(__name__)
        logger.error(message)

    @classmethod
    def Info(cls, message):
        import logging
        logger = logging.getLogger(__name__)
        logger.info(message)

    @classmethod
    def Debug(cls, message):
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(message)
