from .base import InformResponse
from .util import auto_response
from .util import error
from .util import is_error
from .util import is_fail
from .util import make_error
from .util import is_success


__all__ = ['is_error', 'is_success', 'is_fail', 'make_error']


class Response(object):
    """docstring for Response extension"""

    def __init__(self, app=None):

        if app:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'response'):
            app.response = self

        app.response_class = InformResponse

    def success(self, data={}, code=200, headers=None):

        if not isinstance(data, dict):
            raise ValueError('data must be the dict type')
        return auto_response(
            body={'status': 'success', 'data': data, 'code': code},
            code=code, headers=headers)

    def fail(self, data={}, code=400, headers=None):
        if not isinstance(data, dict):
            raise ValueError('data must be the dict type')
        return auto_response(
            body={'status': 'fail', 'data': data, 'code': code},
            code=code, headers=headers)

    def error(self, message='', code=None, data=None, headers=None):
        return error(message='', code=None, data=None, headers=None)
