#!/usr/bin/env python3
"""Module containing class BasicAuth inheriting from Auth & implementing
BasicAuth for REST API.
"""
import re
import base64
import binascii
from typing import Tuple, TypeVar

from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Contains BasicAuth implementation.
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """ Function base64 part of authorization header for:
        Basic authentication.
        """
        if type(authorization_header) is str:
            pttn = r'Basic (?P<token>.+)'
            match_fld = re.fullmatch(pttn, authorization_header.strip())
            if match_fld is not None:
                return match_fld.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str,
    ) -> str:
        """Function returns decoded value of Base64 string of
        base64_authorization_header.
        """
        if type(base64_authorization_header) is str:
            try:
                reslt = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return reslt.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str,
    ) -> Tuple[str, str]:
        """Returns user email & password from Base64 decoded val.
        """
        if type(decoded_base64_authorization_header) is str:
            pttn = r'(?P<user>[^:]+):(?P<password>.+)'
            match_fld = re.fullmatch(
                pttn,
                decoded_base64_authorization_header.strip(),
            )
            if match_fld is not None:
                user = match_fld.group('user')
                password = match_fld.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns user instance associated with user_email & user_pwd.
        """
        if type(user_email) is str and type(user_pwd) is str:
            try:
                usrs = User.search({'email': user_email})
            except Exception:
                return None
            if len(usrs) <= 0:
                return None
            if usrs[0].is_valid_password(user_pwd):
                return usrs[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Basic authentication """
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
