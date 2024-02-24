#!/usr/bin/env python3
""" class: Session Expiration
"""
from os import getenv
from datetime import datetime, timedelta, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session Expiration authentication
    """

    def __init__(self):
        """ Initialization
        """
        try:
            sess_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            sess_duration = 0
        self.session_duration = sess_duration

    def create_session(self, user_id=None):
        """ Generator of Session ID
        """
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        sess_dict = {'user_id': user_id, 'created_at': datetime.now()}
        SessionAuth.user_id_by_session_id[sess_id] = sess_dict
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns user_id for session_id
        """
        if session_id is None:
            return None
        if session_id not in SessionAuth.user_id_by_session_id.keys():
            return None
        sess_dict = SessionAuth.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return sess_dict["user_id"]
        if "created_at" not in sess_dict.keys():
            return None
        tme_create = sess_dict["created_at"]
        delta_time = timedelta(seconds=self.session_duration)
        if (tme_create + delta_time) < datetime.now():
            return None
        return sess_dict["user_id"]
