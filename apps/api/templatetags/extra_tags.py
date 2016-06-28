from django import template
from django.core import serializers
from django.utils.safestring import mark_safe
from django.utils.html import escapejs


register = template.Library()


@register.filter(name='json', needs_autoescape=True)
def to_json(data, autoescape=True):

    dump = serializers.serialize(
        'json', data)

    return mark_safe(escapejs(dump))
