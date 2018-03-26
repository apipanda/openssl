from flask import current_app
from flask import request
from functools import wraps
from werkzeug import LocalProxy
from werkzeug.exceptions import Forbidden


class Allows(object):

    def __init__(self, app=None, identity_loader=None,
                 throws=Forbidden, on_fail=None):
        self._identity_loader = identity_loader
        self.throws = throws

        self.on_fail = _make_callable(on_fail)

        if app:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['allows'] = self

    def requires(self, *requirements, **opts):

        def raiser():
            raise opts.get('throws', self.throws)

        def fail(*args, **kwargs):
            f = _make_callable(opts.get('on_fail', self.on_fail))
            res = f(*args, **kwargs)

            if res is not None:
                return res

            raiser()

        def decorator(f):
            @wraps(f)
            def allower(*args, **kwargs):
                if self.fulfill(requirements):
                    return f(*args, **kwargs)
                else:
                    return fail(*args, **kwargs)
            return allower
        return decorator

    def identity_loader(self, f):
        "Provides an identity loader for the instance"
        self._identity_loader = f
        return f

    def fulfill(self, requirements, identity=None):
        "Runs each requirement until one is not fulfilled"
        identity = identity or self._identity_loader()
        return all(r(identity, request) for r in requirements)


def __get_allows():
    "Internal helper"
    try:
        return current_app.extensions['allows']
    except (AttributeError, KeyError):
        raise RuntimeError("Not configured.")


def _make_callable(func_or_value):
    if not callable(func_or_value):
        return lambda *a, **k: func_or_value
    return func_or_value


_allows = LocalProxy(__get_allows, name="allows")
