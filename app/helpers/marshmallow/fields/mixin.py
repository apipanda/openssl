"""Module that provides a mixin that can help define Marshmallow fields."""

from marshmallow import fields

from ...missing import MISSING


class SchemaFieldMixin(fields.Field):

    def get_field_value(self, key: str, default: object = MISSING) -> object:

        meta_value = self.metadata.get(key)
        context_value = self.context.get(key)

        if context_value is not None:
            return context_value
        elif meta_value is not None:
            return meta_value

        return default
