#!/usr/bin/env python3
""" Session Authentication
"""
from typing import Dict
from flask.globals import session
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session class inherits Auth
    """
    user_id_by_session_id: Dict[str, str] = {}

    def create_session(self, user_id: str = None) -> str:
        """ Generator: Session ID
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns session_id based on user_id
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """ Returns user based cookie value
        """
        cookie = self.session_cookie(request)
        sess_usr_id = self.user_id_for_session_id(cookie)
        usr_id = User.get(sess_usr_id)
        return usr_id

    def destroy_session(self, request=None):
        """ Destroys user session
        """
        cookie_info = self.session_cookie(request)
        if cookie_info is None:
            return False
        if not self.user_id_for_session_id(cookie_info):
            return False
        del self.user_id_by_session_id[cookie_info]
        return True
