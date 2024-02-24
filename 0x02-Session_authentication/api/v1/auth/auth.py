#!/usr/bin/env python3
""" Module: creates class to manage API authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """ Class template for authentication system
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Function returns False if path is in excluded_path
        """
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True

        if path[-1] != '/':
            path += '/'
        if excluded_paths[-1] != '/':
            excluded_paths += '/'

        astrcks = [strs[:-1]
                     for strs in excluded_paths if strs[-1] == '*']

        for strs in astrcks:
            if path.startswith(strs):
                return False

        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Function returns None or str accrding to request
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Flask request object """
        return None

    def session_cookie(self, request=None):
        """ Returns request value of a cookie
        """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
