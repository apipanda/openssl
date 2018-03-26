from flask import abort
from flask_login import current_user
from functools import wraps


def permission_required(permission):
    """
    Takes a permission function as an argument and returns a decorated
    function.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# def admin_required(f):
#     return permission_required(True)(f)
