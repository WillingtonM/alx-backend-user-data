#!/usr/bin/env python3
"""
Module containing class BasicAuth inheriting from Auth & implementing
BasicAuth for REST API
"""
from typing import Optional, Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """
    Contains BasicAuth implementation
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> Optional[str]:
        """
        Function base64 part of authorization header for:
        Basic authentication
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is str:
            return None
        auth_ls = authorization_header.split(" ")
        if auth_ls[0] != 'Basic':
            return None
        else:
            return auth_ls[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> Optional[str]:
        """
        function returns decoded value of Base64 string of
        base64_authorization_header
        """
        print(base64_authorization_header)
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is str:
            return None
        try:
            decd = base64.b64decode(base64_authorization_header)
            print(decd)
        except Exception as e:
            return None
        try:
            decd = decd.decode(encoding='utf-8')
        except Exception as e:
            return None
        return decd

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header:
            str) -> Tuple[Optional[str], Optional[str]]:
        """
        Returns user email & password from Base64 decoded val
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        usr_cred = decoded_base64_authorization_header.split(':')
        user_pwd = ':'.join(usr_cred[1:])
        return usr_cred[0], user_pwd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> Optional[TypeVar('User')]:
        """
        Returns user instance associated with user_email & user_pwd
        """
        if user_email is None or type(user_email) is str:
            return None
        if user_pwd is None or type(user_pwd) is str:
            return None
        attrib = {'email': user_email}
        if User.count() == 0:
            return None
        usrs = User.search(attrib)
        if len(usrs) == 0:
            return None
        for usr in usrs:
            if usr.is_valid_password(user_pwd):
                return usr
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Overloads Auth, and retrieves User instance for request
        """
        auth_head = self.authorization_header(request)
        auth_base_64 = self.extract_base64_authorization_header(auth_head)
        decd = self.decode_base64_authorization_header(auth_base_64)
        usr_cred = self.extract_user_credentials(decd)
        usr = self.user_object_from_credentials(usr_cred[0], usr_cred[1])
        return usr
