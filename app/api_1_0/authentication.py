from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models.user import User
from . import api
from .errors import unauthorized, forbidden
from ..models import token_authentication

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    if not password or password.isspace() is True:
        is_pass_filled = False
    else:
        is_pass_filled = True

    if not email_or_token or email_or_token.isspace() is True:
        is_id_filled = False
    else:
        is_id_filled = True

    # First case
    # email/password is filled
    # usual login
    if is_id_filled is True and is_pass_filled is True:
        user = User.query.filter_by(email=email_or_token).first()
        if not user:
            return False
        g.current_user = user
        g.token_used = False
        return user.verify_password(password)

    # Second case
    # token(email) is filled
    # token login
    elif is_id_filled is True and is_pass_filled is False:
        g.current_user = token_authentication.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None

    # other case
    # all connection is refused
    else:
        return False

#todo http auth ip reject


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    # todo confirmed is email auth.
    if not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api.route('/token')
def get_token():
    if g.token_used:
        return unauthorized('Invalid credentials')
    timed_key = token_authentication.generate_auth_token(g.current_user, expiration=3600)
    return jsonify({'token': timed_key, 'expiration': 3600})
