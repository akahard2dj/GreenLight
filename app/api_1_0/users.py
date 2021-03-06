from flask import g, jsonify, request

import cryptography.exceptions
import os
import random
import string

from app.api_1_0 import api
from app.api_1_0.errors import unauthorized, forbidden, not_acceptable, bad_request
from app.api_1_0.text_cipher import RSACipher
from app.api_1_0.authentication import auth
from app.models.user import User
from app import db

rsa_cipher = RSACipher(os.path.join(os.getcwd(), 'greenlight.key'))


@api.route('/users/add', methods=['GET', 'POST'])
def add_user():
    data = request.json['data']

    try:
        token_data = rsa_cipher.decrypt(data)
    except cryptography.exceptions.InvalidKey:
        return unauthorized('invalid public key')

    username = token_data.split(':')[0]
    password = token_data.split(':')[1]

    user_query = User.query.filter_by(email=username).first()

    if user_query is not None:
        return not_acceptable('user already exists')
    else:
        random_user_name = ''.join(random.SystemRandom()
                                   .choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                                   for _ in range(7))
        user = User(email=username, username=random_user_name, password=password)
        db.session.add(user)

        response = jsonify({'message': 'success'})
        response.status_code = 200

        return response


@api.route('/users/test', methods=['GET'])
def test_user():
    return jsonify({'result': 'success'})


@api.route('/users')
def get_user():
    try:
        token_flag = g.token_used
    except AttributeError:
        return forbidden('Unconfirmed account')
    else:
        if token_flag:
            user = g.current_user
            return jsonify(user.to_json())
        else:
            return unauthorized('Invalid credentials')


@api.route('/users/login_test', methods=['GET'])
@auth.login_required
def user_login_test():
    return jsonify({'message':'ok'})


@api.route('/users/reset_username', methods=['GET', 'POST'])
@auth.login_required
def reset_username():
    data = request.json['data']

    try:
        token_data = rsa_cipher.decrypt(data)
    except cryptography.exceptions.InvalidKey:
        return unauthorized('invalid public key')

    username = token_data
    user_query = User.query.filter_by(username=username).first()
    if user_query is not None:
        return not_acceptable('username already exists')
    else:
        user = User.query.filter_by(id=g.current_user.id).first()
        user.reset_username(username)

    response = jsonify({'message': 'success'})
    response.status_code = 200

    return response


@api.route('/users/reset_password', methods=['GET', 'POST'])
@auth.login_required
def reset_password():
    data = request.json['data']

    try:
        token_data = rsa_cipher.decrypt(data)
    except cryptography.exceptions.InvalidKey:
        return unauthorized('invalid public key')

    password = token_data
    user = User.query.filter_by(id=g.current_user.id).first()

    is_success = user.reset_password(password)
    if is_success:
        response = jsonify({'message': 'success'})
        response.status_code = 200

        return response
    else:
        return bad_request('db is not corresponding')
