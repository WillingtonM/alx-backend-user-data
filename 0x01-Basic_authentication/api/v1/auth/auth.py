#!/usr/bin/env python3
"""
Module that creates a class to manage
API authentication
"""
from flask import request
from typing import List, Optional, TypeVar
import os


class Auth:
    """
    Class template for authentication system
    """

    def require_auth(self, path: str, excluded_path: List[str]) -> bool:
        """ Returns False if path is in excluded_path
        """
        if path is None:
            return True
        if excluded_path is None or len(excluded_path) == 0:
            return True
        if path:
            for excl in excluded_path:
                lst_tag = excl.split('/')[-1]
                if lst_tag.endswith('*'):
                    lst_tag = lst_tag[0:-1]
                    if lst_tag in path:
                        return False
            if path in excluded_path or path + '/' in excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> Optional[str]:
        """ Function returns None or str based on request
        """
        if not request:
            return None
        authorisation = request.headers.get('Authorization')
        if authorisation:
            return authorisation
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None or User based on request
        """
        print("should not be called")
        return None
