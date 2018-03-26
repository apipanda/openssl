from .base import *


class ProdConfig(Config):
    ''' Configuration class for site testing environment '''

    DEBUG = False
    TEST = False
    SQLALCHEMY_ECHO = False
    MONGO_URI = os.getenv('MONGO_URI')

    MAX_RETRY_COUNT = 3

    # Configuring sentry logging
    SENTRY_DSN = os.getenv(
        'SENTRY_DSN')
    SENTRY_INCLUDE_PATHS = ['sslme']
    SENTRY_USER_ATTRS = ['username', 'full_name', 'email']

    FLASKS3_USE_HTTPS = True
