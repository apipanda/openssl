import os

from urllib.parse import urlparse


class Config(object):
    '''
    Base configuration class. Subclasses should include configurations for
    testing, development and production environments

    '''

    DEBUG = True
    FLASK_DEBUG = 1
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        '\x91c~\xc0-\xe3\'f\xe19PE\x91`6\x01/\x0c\xed\\\xbdk\xf8')

    DOMAIN = 'sslme.io'
    SQLALCHEMY_ECHO = False
    # Mail settings
    MAIL_SERVER = 'smtp.mailgun.org'
    MAIL_PORT = 587
    MAIL_USERNAME = 'postmaster@mysslme.mailgun.org'
    MAIL_PASSWORD = 'mysslme'
    DEFAULT_MAIL_CHANNEL = 'mailgun'
    MAIL_DEFAULT_SENDER = 'daemon@sslme.com'
    MAIL_SUPPRESS_SEND = True
    MAIL_FAIL_SILENTLY = False
    UPLOADS_DEFAULT_DEST = os.path.join(
        os.path.dirname(os.path.abspath(__name__)), 'uploads')

    CLOUDFILES_USERNAME = os.getenv('CLOUDFILES_USERNAME')
    CLOUDFILES_API_KEY = os.getenv('CLOUDFILES_API_KEY')

    PROTOCOL = 'http://'

    ADMIN_USERNAME = 'sslme'
    ADMIN_PASSWORD = 'sslme'
    ADMIN_EMAIL = '{0}@{1}'.format(ADMIN_USERNAME, DOMAIN)
    ADMIN_FULL_NAME = 'SSLME Admin'

    ASSETS_DEBUG = False  # not DEBUG

    REDIS_URL = os.getenv(
        'REDIS_URL',
        'redis://')

    if REDIS_URL:
        url = urlparse(REDIS_URL)
        REDIS_HOST = url.hostname
        REDIS_PORT = url.port
        REDIS_PASSWORD = url.password

    CELERY_TIMEZONE = 'Africa/Lagos'

    LOGFILE_NAME = 'sslme'

    LOGIN_VIEW = 'auth.login'

    # DOMAIN = 'sslme.dev:2500'
    WTF_CSRF_TIME_LIMIT = 36000000
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')

    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY')

    # FLASKS3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'sslme-bucket')

    # FLASK_ASSETS_USE_S3 = True
    # FLASKS3_USE_HTTPS = True
    # USE_S3 = True
    # FLASKS3_HEADERS = {
    #     'Expires': 'Thu, 15 Apr 2020 20:00:00 GMT',
    #     'Cache-Control': 'max-age=86400'
    # }
    # USE_S3_DEBUG = not USE_S3

    SETUP_DIR = os.path.join(os.path.dirname(
        os.path.abspath(__name__)), 'setup/')

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))

    TEMPLATE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(__name__)), 'templates/')
    STATIC_DIR = os.path.join(os.path.dirname(
        os.path.abspath(__name__)), 'static/')

    BABEL_DEFAULT_TIMEZONE = 'Africa/Lagos'
