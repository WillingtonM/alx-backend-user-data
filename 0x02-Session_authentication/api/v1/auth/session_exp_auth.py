#!/usr/bin/env python3
"""
Module for session expiration
"""


import os
from datetime import datetime as dt, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth is class that extends functionality of the
    """

    def __init__(self):
        """
        Constructor for SessionExpAuth class.
        Initializes session_duration attribute.

        """
        super().__init__()

        self.session_duration = int(os.environ.get("SESSION_DURATION", 0))

    def create_session(self, user_id: int) -> str:
        """
        Creates a new session for user & assigns session ID.
        """

        sess_id = super().create_session(user_id)

        if sess_id is None:
            return None
        
        self.user_id_by_session_id[sess_id] = {
            'user_id': user_id,
            'created_at': dt.now()
        }

        return sess_id

    def user_id_for_session_id(self, session_id: str) -> int:
        """
        Gets the user_id associated with a session ID.
        Returns: user_id associated with session ID if session is
        valid, None otherwise
        """

        if session_id is None:
            return None
        
        if session_id not in self.user_id_by_session_id:
            return None
        sess_dict = self.user_id_by_session_id.get(session_id)
        if sess_dict is None:
            return None
        
        if self.session_duration <= 0:
            return sess_dict.get("user_id")
        
        date_created = sess_dict.get('created_at')

        if date_created is None:
            return None
        
        now = dt.now()
        if date_created + timedelta(seconds=self.session_duration) < now:
            return None
        
        exp_at = sess_dict["created_at"] + \
            timedelta(seconds=self.session_duration)
        
        if exp_at < dt.now():
            return None
        
        return sess_dict.get("user_id", None)
