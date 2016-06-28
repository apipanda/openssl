from __future__ import unicode_literals

from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'api'
    verbose_name = 'Api Application'

    def ready(self):
        from .signals import create_api_key
