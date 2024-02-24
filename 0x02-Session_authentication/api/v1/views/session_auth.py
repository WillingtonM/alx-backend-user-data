#!/usr/bin/env python3
"""
Session authentication route handlers
"""
from werkzeug import exceptions
from api.v1.views import app_views
from models.user import User
from flask import jsonify, request
from os import abort, environ, getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """ POST /api/v1/auth/session/login
    Return user instance, 400 if missing
    """
    usr_email = request.form.get('email', None)
    usr_pass = request.form.get('password', None)

    if usr_email is None or usr_email == "":
        return jsonify({"error": "email missing"}), 400
    if usr_pass is None or usr_pass == "":
        return jsonify({"error": "password missing"}), 400

    is_valid_usr = User.search({'email': usr_email})

    if not is_valid_usr:
        return jsonify({"error": "no user found for this email"}), 404

    is_valid_usr = is_valid_usr[0]

    if not is_valid_usr.is_valid_password(usr_pass):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    sess_id = auth.create_session(is_valid_usr.id)
    cookie_resp = getenv('SESSION_NAME')
    usr_dict = jsonify(is_valid_usr.to_json())

    usr_dict.set_cookie(cookie_resp, sess_id)
    return usr_dict


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False)
def session_logout() -> str:
    """ DELETE /api/v1/auth/session/logout
    Returns deleted json (if correctly done)
    404 if fails
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
