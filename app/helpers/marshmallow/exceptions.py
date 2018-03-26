# -*- coding: utf-8 -*-


class MarshmallowSQLAlchemyError(Exception):
    """Base exception class from which all exceptions inherits.
    """
    pass


class ModelConversionError(MarshmallowSQLAlchemyError):
    """Raised when an error occurs in converting a SQLAlchemy construct
    to a marshmallow object.
    """
    pass
