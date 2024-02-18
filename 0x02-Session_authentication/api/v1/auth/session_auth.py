#!/usr/bin/env python3
"""
Module containing class SeesionAuth inheriting from Auth & implementing
Session Authentication
"""
from api.v1.auth.auth import Auth
from typing import Optional
from uuid import uuid4
from models.user import User
from typing import TypeVar, Optional


class SessionAuth(Auth):
    """
    Class contains session authentication implementation
    """
    usr_id_by_sess_id = {}

    def create_session(self, user_id: str = None) -> Optional[str]:
        """
        Creates Session ID for user_id
        """
        if not user_id or type(user_id) != str:
            return None
        sess_id = str(uuid4())
        self.usr_id_by_sess_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> Optional[str]:
        """
        Returns User ID based on Session ID
        """
        if not session_id or type(session_id) != str:
            return None
        usr_id = self.usr_id_by_sess_id.get(session_id)
        return usr_id

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns User based on cookie value
        """
        cook = self.session_cookie(request)
        usr_id = self.user_id_for_session_id(cook)
        usr = User.get(usr_id)
        return usr

    def destroy_session(self, request=None) -> bool:
        """
        Deletes user session for logout functionality
        """
        if request is None:
            return False
        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False
        if self.user_id_for_session_id(sess_id) is None:
            return False
        try:
            del self.usr_id_by_sess_id[sess_id]
        except Exception as e:
            pass
        return True
