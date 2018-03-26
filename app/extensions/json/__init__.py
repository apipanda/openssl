# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import decimal
import io
import uuid

from flask import current_app
from flask import json as _json
from flask import request

import arrow
import pendulum
import phonenumbers

text_type = str


def _wrap_reader_for_text(fp, encoding):
    if isinstance(fp.read(0), bytes):
        fp = io.TextIOWrapper(io.BufferedReader(fp), encoding)
    return fp


def _wrap_writer_for_text(fp, encoding):
    try:
        fp.write('')
    except TypeError:
        fp = io.TextIOWrapper(fp, encoding)
    return fp


class JSONEncoder(_json.JSONEncoder):

    """Custom JSON encoder that will serialize more complex datatypes.

    This class adds support for the following datatypes:

    - ``phonenumbers.phonenumber.PhoneNumber``: This will be serialized to
        a E.164 phonenumber. This will only be run if ``phonenumbers`` is
        installed.
    - ``decimal.Decimal``: This will serialize to a pretty decimal number with
        no trailing zeros and no unnecessary values. For example:
        - 2.01 -> 2.01
        - 2.0 -> 2
        - 2.010 -> 2.01
        - 2.000 -> 2
    - ``arrow.Arrow``: This will be serialized to an ISO8601 datetime string
        with the offset included.
    - ``datetime.datetime``: This will be serialized to an ISO8601 datetime
        string with the offset included.
    - ``datetime.date``: This will be serialized to an ISO8601 date string.

    Extended from http://flask.pocoo.org/snippets/119.

    """

    def __init__(self, *args, **kwargs):
        super(JSONEncoder, self).__init__(*args, **kwargs)

        self.use_decimal = False

    def default(self, obj):
        """
        Encode individual objects into their JSON representation.

        This method is used by :class:`flask.json.JSONEncoder` to encode
        individual items in the JSON object.

        Args:
            obj (object): Any Python object we wish to convert to JSON.

        Returns:
            str: The stringified, valid JSON representation of our provided
                object.
        """

        if isinstance(obj, decimal.Decimal):
            obj = format(obj, 'f')
            str_digit = str(obj)

            return (str_digit.rstrip('0').rstrip('.')
                    if '.' in str_digit
                    else str_digit)

        elif isinstance(obj, phonenumbers.PhoneNumber):
            return phonenumbers.format_number(
                obj,
                phonenumbers.PhoneNumberFormat.E164
            )

        elif isinstance(obj, pendulum.Pendulum):
            return str(obj)

        elif isinstance(obj, arrow.Arrow):
            return str(obj)

        if isinstance(obj, datetime.datetime):
            print(obj)
            if obj.tzinfo:
                # eg: '2015-09-25T23:14:42.588601+00:00'
                return obj.isoformat('T')
            else:
                # No timezone present - assume UTC.
                # eg: '2015-09-25T23:14:42.588601Z'
                return obj.isoformat('T') + 'Z'

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        elif isinstance(obj, uuid.UUID):
            return str(obj)

        try:
            return list(iter(obj))
        except TypeError:
            pass

        return super(JSONEncoder, self).default(obj)


def _dump_arg_defaults(kwargs):
    """Inject default arguments for dump functions."""
    if current_app:
        kwargs.setdefault('cls', current_app.json_encoder)
        if not current_app.config['JSON_AS_ASCII']:
            kwargs.setdefault('ensure_ascii', False)
        kwargs.setdefault('sort_keys', current_app.config['JSON_SORT_KEYS'])
    else:
        kwargs.setdefault('sort_keys', True)
        kwargs.setdefault('cls', JSONEncoder)


def dumps(obj, **kwargs):
    """Serialize ``obj`` to a JSON formatted ``str`` by using the application's
    configured encoder (:attr:`~flask.Flask.json_encoder`) if there is an
    application on the stack.

    This function can return ``unicode`` strings or ascii-only bytestrings by
    default which coerce into unicode strings automatically.  That behavior by
    default is controlled by the ``JSON_AS_ASCII`` configuration variable
    and can be overridden by the simplejson ``ensure_ascii`` parameter.
    """
    _dump_arg_defaults(kwargs)
    encoding = kwargs.pop('encoding', None)
    rv = _json.dumps(obj, **kwargs)
    if encoding is not None and isinstance(rv, text_type):
        rv = rv.encode(encoding)
    return rv


def dump(obj, fp, **kwargs):
    """Like :func:`dumps` but writes into a file object."""
    _dump_arg_defaults(kwargs)
    encoding = kwargs.pop('encoding', None)
    if encoding is not None:
        fp = _wrap_writer_for_text(fp, encoding)
    _json.dump(obj, fp, **kwargs)


def jsonify(*args, **kwargs):
    """
    copied from the flask jsonify function with modifcations added
    """

    indent = None
    separators = (',', ':')

    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR']\
            and not request.is_xhr:
        indent = 2
        separators = (', ', ': ')

    if args and kwargs:
        raise TypeError(
            'jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:  # single args are passed directly to dumps()
        data = args[0]
    else:
        data = args or kwargs

    return current_app.response_class(
        (dumps(data, indent=indent, separators=separators), '\n'),
        mimetype=current_app.config['JSONIFY_MIMETYPE']
    )
