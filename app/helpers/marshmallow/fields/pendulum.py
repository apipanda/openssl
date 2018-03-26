# ~*~ coding: utf-8 ~*~
"""Module that defines a Marshmallow field that deserializes a date string into
an Pendulum object.
"""

from __future__ import absolute_import

import pendulum
from marshmallow import ValidationError, fields

from .mixin import SchemaFieldMixin


class PendulumField(fields.DateTime, SchemaFieldMixin):

    def _jsonschema_type_mapping(self):
        """Define the JSON Schema type for this field."""
        return {
            'type': 'string',
            'format': 'date-time',
        }

    def _deserialize(self, value, attr, obj):
        """Deserializes a string into a Pendulum object."""
        if not self.context.get('convert_dates', True) or not value:
            return value

        value = super(PendulumField, self)._deserialize(value, attr, value)
        timezone = self.get_field_value('timezone')
        target = pendulum.instance(value)

        if (timezone and (str(target) !=
                          str(target.in_timezone(timezone)))):
            raise ValidationError(
                "The provided datetime is not in the "
                "{} timezone.".format(timezone)
            )

        return target
