import json

from flask import Response


def unauthorised_exception(exception):
    return Response(
        response=json.dumps(
            {
                'status': 'error',
                'code': 401,
                'message': ('Authentication error. \
                            Invalid Authentication token.')
            }),
        status=401,
        mimetype='application/json')
