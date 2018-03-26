# ~*~ coding: utf-8 ~*~
"""Module that defines a Marshmallow field that deserialzes a date string into
an Arrow object.
"""

from __future__ import absolute_import

import arrow
from marshmallow import ValidationError, fields

from .mixin import SchemaFieldMixin


class ArrowField(fields.DateTime, SchemaFieldMixin):

    def _jsonschema_type_mapping(self) -> dict:
        """Define the JSON Schema type for this field."""
        return {
            'type': 'string',
            'format': 'date-time',
        }

    def _serialize(self, value, attr, obj):
        """Convert the Arrow object into a string."""
        if isinstance(value, arrow.arrow.Arrow):
            value = value.datetime

        return super(ArrowField, self)._serialize(value, attr, obj)

    def _deserialize(self, value, attr, data):
        """Deserializes a string into an Arrow object."""
        if not self.context.get('convert_dates', True) or not value:
            return value

        value = super(ArrowField, self)._deserialize(value, attr, data)
        timezone = self.get_field_value('timezone')
        target = arrow.get(value)

        if timezone and str(target.to(timezone)) != str(target):
            raise ValidationError(
                "The provided datetime is not in the "
                "{} timezone.".format(timezone)
            )

        return target
