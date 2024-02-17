#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Return: list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/:id
    Path parameter: User ID
    Return:
        User object JSON represented
        404 if User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    usr = User.get(user_id)
    if usr is None:
        abort(404)
    return jsonify(usr.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/:id
    Path parameter:
        User ID
    Return:
        empty JSON is User has been correctly deleted
        404 if User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    usr = User.get(user_id)
    if usr is None:
        abort(404)
    usr.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    POST /api/v1/users/
    JSON body:
        email
        password
        last_name (opt)
        first_name (opt)
    Return:
        User object JSON represented
        400 if can't create new User
    """
    req_json = None
    err_msg = None
    try:
        req_json = request.get_json()
    except Exception as e:
        req_json = None
    if req_json is None:
        err_msg = "Wrong format"
    if err_msg is None and req_json.get("email", "") == "":
        err_msg = "email missing"
    if err_msg is None and req_json.get("password", "") == "":
        err_msg = "password missing"
    if err_msg is None:
        try:
            usr = User()
            usr.email = req_json.get("email")
            usr.password = req_json.get("password")
            usr.first_name = req_json.get("first_name")
            usr.last_name = req_json.get("last_name")
            usr.save()
            return jsonify(usr.to_json()), 201
        except Exception as e:
            err_msg = "Can't create User: {}".format(e)
    return jsonify({'error': err_msg}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    PUT /api/v1/users/:id
    Path parameter:
        User ID
    JSON body:
        last_name (optional)
        first_name (optional)
    Return:
        User object JSON represented
        404 if User ID doesn't exist
        400 if can't update User
    """
    if user_id is None:
        abort(404)
    usr = User.get(user_id)
    if usr is None:
        abort(404)
    req_json = None
    try:
        req_json = request.get_json()
    except Exception as e:
        req_json = None
    if req_json is None:
        return jsonify({'error': "Wrong format"}), 400
    if req_json.get('first_name') is not None:
        usr.first_name = req_json.get('first_name')
    if req_json.get('last_name') is not None:
        usr.last_name = req_json.get('last_name')
    usr.save()
    return jsonify(usr.to_json()), 200
