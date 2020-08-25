import os
import logging


LOG_LEVEL = os.getenv('LOG_LEVEL', 'warn').upper()
logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    return logger


SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
