from functools import wraps

from .allows import _allows, _make_callable


def requires(*requirements, **opts):

    def raiser():
        raise opts.get('throws', _allows.throws)

    def fail(*args, **kwargs):
        f = _make_callable(opts.get('on_fail', _allows.on_fail))
        res = f(*args, **kwargs)

        if res is not None:
            return res

        raiser()

    def decorator(f):

        @wraps(f)
        def allower(*args, **kwargs):
            if _allows.fulfill(requirements, identity=opts.get('identity')):
                return f(*args, **kwargs)
            return fail(*args, **kwargs)

        return allower

    return decorator
