import logging
import os

from flask import Flask
from flask_assets import Environment
from flask_compress import Compress
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from raven.contrib.flask import Sentry

from .extensions.allows import Allows
from .extensions.babel import Babel
from .extensions.gzip import Gzip
from .extensions.json import JSONEncoder
# from .extensions.minify import HTMLMIN
from .extensions.redis import RedisExtension
from .extensions.response import Response


# App factories
SENTRY_DSN = ('https://00d8a063e7cc433f8fd0821fc8432c33:'
              'dfd25db9211a4f08a79aba497ba423ea@sentry.io/272338')


mail = Mail()
moment = Moment()
compress = Compress()
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.session_protection = 'strong'  # use strong session protection
login_manager.login_view = 'auth.login'


def create_app(app_name, config_obj):
    """ Generates and configures the main shop application. All additional """
    # Launching application
    factory = Flask(app_name)
    factory.config.from_object(config_obj)
    factory.json_encoder = JSONEncoder

    mail.init_app(factory)
    moment.init_app(factory)
    # minify.init_app(factory)
    compress.init_app(factory)
    csrf.init_app(factory)
    login_manager.init_app(factory)

    # register 'main' blueprint
    from .views.main import main as main_blueprint
    factory.register_blueprint(main_blueprint)

    # register 'auth' blueprint
    from .views.auth import auth as auth_blueprint
    factory.register_blueprint(auth_blueprint)

    # register 'api' blueprint
    from .views.api import api as api_blueprint
    factory.register_blueprint(api_blueprint, url_prefix='/_api')

    # add CORS support
    CORS(factory)

    # add GZip support
    Gzip(factory)

    # Assets
    Environment(factory)

    # Authorisation decorator
    Allows(factory)

    # Redis extension
    redis = RedisExtension(
        factory, **{'decode_responses': True,
                    'charset': 'utf-8'})

    factory.redis = redis._redis_client

    factory.mongo = PyMongo(factory)
    # Add custom response formatter
    Response(factory)

    # Add translation support
    Babel(factory)

    # Initialize Logging
    if factory.debug:
        from logging.handlers import RotatingFileHandler
        from flask_debugtoolbar import DebugToolbarExtension

        DebugToolbarExtension(factory)
        os.environ.setdefault('FLASK_SETTINGS_MODULE', 'app.config.DevConfig')
        file_handler = RotatingFileHandler(
            "%s/logs/%s.log" % (
                factory.config.get('BASE_DIR'),
                factory.config.get(
                    "LOGFILE_NAME",
                    app_name)),
            maxBytes=500 * 1024)

        file_handler.setLevel(logging.WARNING)
        from logging import Formatter
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        factory.logger.addHandler(file_handler)
    else:
        # from flask_sslify import SSLify
        # SSLify(factory)
        # Enable Sentry logging
        sentry = Sentry(
            app=factory, dsn=SENTRY_DSN,
            logging=True, level=logging.WARN)
        factory.sentry = sentry

    return factory
