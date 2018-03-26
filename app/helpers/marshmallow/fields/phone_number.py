# ~*~ coding: utf-8 ~*~
"""Module that defines a Marshmallow field for working with phone numbers."""

import re

import phonenumbers
from marshmallow import ValidationError, fields

from .mixin import SchemaFieldMixin


class PhoneNumberField(fields.String, SchemaFieldMixin):

    def _jsonschema_type_mapping(self):
        """Define the JSON Schema type for this field."""
        return {
            'type': 'string',
        }

    def _format_phone_number(self, value, attr):
        """Format and validate a phone number."""
        strict_validation = self.get_field_value(
            'strict_phone_validation',
            default=False
        )
        strict_region = self.get_field_value(
            'strict_phone_region',
            default=strict_validation
        )
        region = self.get_field_value('region', 'US')
        phone_number_format = self.get_field_value(
            'phone_number_format',
            default=phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

        # Remove excess special chars, except for the plus sign
        stripped_value = re.sub(r'[^\w+]', '', value)

        try:
            if not stripped_value.startswith('+') and not strict_region:
                phone = phonenumbers.parse(stripped_value, region)
            else:
                phone = phonenumbers.parse(stripped_value)

            if (not phonenumbers.is_possible_number(phone) or
                    not phonenumbers.is_valid_number(phone) and
                    strict_validation):
                raise ValidationError(
                    "The value for {} ({}) is not a valid phone "
                    "number.".format(attr, value)
                )

            return phonenumbers.format_number(phone, phone_number_format)

        except phonenumbers.phonenumberutil.NumberParseException as exc:
            if strict_validation or strict_region:
                raise ValidationError(exc)

    def _deserialize(self, value, attr, data):
        """Format and validate the phone number using libphonenumber."""
        if value:
            value = self._format_phone_number(value, attr)

        return super(PhoneNumberField, self)._deserialize(value, attr, data)

    def _serialize(self, value, attr, obj):
        """Format and validate the phone number user libphonenumber."""
        value = super(PhoneNumberField, self)._serialize(value, attr, obj)

        if value:
            value = self._format_phone_number(value, attr)

        return value
