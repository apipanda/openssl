from flask import Blueprint, current_app

main = Blueprint(
    'main',
    __name__
)


from . import errors
from . import views
from ...models import Permission


# from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(permission=Permission)
