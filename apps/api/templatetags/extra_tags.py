from django import template
from django.core import serializers
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(name='json', needs_autoescape=True)
def to_json(data, autoescape=True):
    dump = serializers.serialize(
        'json', data, fields=['title', 'slug', 'author', 'markup', 'section', ])

    return mark_safe(dump)
