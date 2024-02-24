#!/usr/bin/env python3
""" Module containing class BasicAuth inheriting from Auth & implementing
BasicAuth for REST API.
"""
from typing import TypeVar, Tuple
from base64 import b64decode, decode
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """ Contains BasicAuth implementation.
    """

    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """ Function base64 part of authorization header for:
        Basic authentication.
        """
        if auth_header is None or not isinstance(auth_header, str):
            return None
        if 'Basic ' not in auth_header:
            return None
        return auth_header[6:]

    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """ Function returns decoded value of Base64 string of
        base64_authorization_header.
        """
        if b64_auth_header is None or not isinstance(b64_auth_header, str):
            return None
        try:
            b64_res = base64.b64decode(b64_auth_header)
            b64_dec = b64_res.decode('utf-8')
        except Exception:
            return None
        return b64_dec

    def extract_user_credentials(
            self, decoded_b64_auth_header: str) -> (str, str):
        """Returns user email & password from Base64 decoded val.
        """
        if decoded_b64_auth_header is None or not isinstance(
                decoded_b64_auth_header, str) \
           or ':' not in decoded_b64_auth_header:
            return (None, None)
        return decoded_b64_auth_header.split(':', 1)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns user object from credentials
        """
        if user_email is None or not isinstance(
                user_email, str) or user_pwd is None or not isinstance(
                    user_pwd, str):
            return None
        try:
            usrs = User.search({'email': user_email})
        except Exception:
            return None
        for usr in usrs:
            if usr.is_valid_password(user_pwd):
                return usr
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Basic authentication
        """
        header_auth = self.authorization_header(request)
        if not header_auth:
            return None
        base64_extract = self.extract_base64_authorization_header(header_auth)
        base64_decode = self.decode_base64_authorization_header(base64_extract)
        usr_credentials = self.extract_user_credentials(base64_decode)
        usr_email = usr_credentials[0]
        usr_pwd = usr_credentials[1]
        user_credentials = self.user_object_from_credentials(
            usr_email, usr_pwd)
        return user_credentials
