#!/usr/bin/env python3
"""Authentication module.
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """ Class template for authentication system.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False if path is in excluded_path.
        """
        if path is None:
            return True

        if excld_paths is None or not excluded_paths:
            return True

        for excld_paths in excluded_paths:
            if fnmatch.fnmatch(path, excld_paths):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Function returns None or str based on request.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get user from request.
        """
        return None
