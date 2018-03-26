from .base import *


class TestConfig(Config):
    ''' Configuration class for site testing environment '''

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TEST = True
    SQLALCHEMY_ECHO = False
