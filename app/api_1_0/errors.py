from flask import jsonify
from app.exceptions import ValidationError

from app.api_1_0 import api


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def not_acceptable(message):
    response = jsonify({'error': 'not acceptable', 'message': message})
    response.status_code = 406
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
