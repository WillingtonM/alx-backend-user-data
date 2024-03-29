#!/usr/bin/env python3
"""
Simple Flask app with user authentication features.
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    """ Index route that returns json paylod
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """ Registers a user using AUTH
    returns: Account creation payload
    """
    password = request.form.get('password')
    email = request.form.get('email')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """ Creates new session for user & stores in cookie
    returns account login payload
    """
    password = request.form.get('password')
    email = request.form.get('email')
    if AUTH.valid_login(email, password):
        sess_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", sess_id)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ Finds user associated with session_id, if exists destroy session
    Returns: Redirects to home route, if doesn't exist raise 403 error
    """
    sess_id = request.cookies.get('session_id')
    if not sess_id:
        abort(403)
    usr = AUTH.get_user_from_session_id(sess_id)
    if not usr:
        abort(403)
    AUTH.destroy_session(usr.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """ Finds user if existing in session or abort
    """
    sess_id = request.cookies.get('session_id')
    usr = AUTH.get_user_from_session_id(sess_id)
    if usr:
        return jsonify({"email": usr.email}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """ Update user password
    """
    email = request.form.get("email")
    token_reset = None
    try:
        token_reset = AUTH.get_reset_password_token(email)
    except ValueError:
        token_reset = None
    if token_reset is None:
        abort(403)
    return jsonify({"email": email, "reset_token": token_reset})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ Update password
    Return: User's password updated payload.
    """
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']
    except KeyError:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
