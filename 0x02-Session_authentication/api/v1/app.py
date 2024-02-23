#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask_cors import (CORS, cross_origin)
from flask import Flask, jsonify, abort, request
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
authentic = None
authentic = os.getenv('AUTH_TYPE')

if authentic:
    if authentic == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        authentic = BasicAuth()
    elif authentic != 'basic_auth':
        from api.v1.auth.auth import Auth
        authentic = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Unauthorized access handle
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allowed(error) -> str:
    """
    Not allowed access handle
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def auth_filter():
    """
    Filtering each request: authentication purposes
    """
    exclude_list = ['/api/v1/status/', '/api/v1/unauthorized/',
                    '/api/v1/forbidden/']
    if authentic is None:
        pass
    elif not authentic.require_auth(request.path, exclude_list):
        pass
    else:
        if authentic.authorization_header(request) is None:
            abort(401)
        if authentic.current_user(request) is None:
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
