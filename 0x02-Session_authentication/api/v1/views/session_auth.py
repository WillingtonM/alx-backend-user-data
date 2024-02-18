#!/usr/bin/env python3
"""
Module: contains views for Session authentication routes
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def get_user_for_session_auth():
    """
    Function tets user based on request data
    """
    mail = request.form.get('email')
    pwd = request.form.get('password')
    if mail == "" or mail is None:
        return jsonify({"error": "email missing"}), 400
    if pwd == "" or pwd is None:
        return jsonify({"error": "password missing"}), 400
    usrs = User.search({'email': mail})
    if len(usrs) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for usr in usrs:
        if usr.is_valid_password(pwd):
            from api.v1.app import auth
            cook = os.getenv('SESSION_NAME')
            sess = auth.create_session(usr.id)
            resp = jsonify(usr.to_json())
            resp.set_cookie(cook, sess)
            return resp
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete_user_session():
    """
    Function deletes user's session
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
