import json
from flask import current_app
from connexion.exceptions import ProblemException
from werkzeug.exceptions import HTTPException, InternalServerError

from ..json import jsonify
from dicttoxml import dicttoxml
from flask import Response
from flask import request


class Dict(dict):
    def stringify(self):
        return json.dumps(self)


def set_headers(res, headers):
    for key, value in headers.items():
        res.headers.add(key, value)
    return res


def make_error(exception, **kwargs):

    if hasattr(current_app, 'sentry'):
        current_app.sentry.captureException()

    if isinstance(exception, ProblemException):
        exception = exception.to_problem()
        payload = Dict(message=exception.detail,
                       code=exception.status, title=exception.name, **kwargs)
    else:
        if not isinstance(exception, HTTPException):
            exception = InternalServerError()

        payload = Dict(message=exception.description,
                       code=exception.code, **kwargs)

    return error(**payload)


def json_response(body={}, code=200, headers=None):
    response = Dict(**body)
    response.code = code

    if isinstance(headers, dict):
        response = set_headers(response, headers)

    return jsonify(**response), code


def xml_response(body={}, code=200, headers=None):
    if isinstance(body, dict):
        body = dicttoxml(body)

    response = Response(body, mimetype='text/xml')
    response.code = code

    if isinstance(headers, dict):
        response = set_headers(response, headers)

    return response, code


def auto_response(*args, **kwargs):
    mime_types = ['application/json', 'application/xml', 'text/html']
    accept_mime_types = request.accept_mimetypes
    accept_type = accept_mime_types.best_match(mime_types)

    if accept_type == mime_types[0]:
        return json_response(*args, **kwargs)
    elif accept_type == mime_types[1]:
        return xml_response(*args, **kwargs)

    data = jsonify(*args, **kwargs)
    return data


def loads(string):
    if not string:
        raise ValueError('invalid jsend string is given')

    try:
        json_data = json.loads(string)
    except (TypeError, ValueError):
        raise ValueError('failed to parse json string')

    if ('status' not in json_data or
            json_data['status'] not in ('success', 'fail', 'error')):
        raise ValueError('not in valid jsend type')

    return Dict(json_data)


def error(message='', code=None, data=None, headers=None):
    ret = {}

    if not isinstance(message, str):
        raise ValueError('message must be the str type')
    if code:
        if not isinstance(code, int):
            raise ValueError('code must be the int type')
    if data:
        if not isinstance(data, dict):
            raise ValueError('data must be the dict type')
        ret['data'] = data

    ret['status'] = 'error'
    ret['message'] = message
    ret['code'] = code
    return auto_response(body=ret, code=code, headers=headers)


def is_success(msg):
    return msg['status'] == 'success'


def is_fail(msg):
    return msg['status'] == 'fail'


def is_error(msg):
    return msg['status'] == 'error'
