#!/usr/bin/env python3
""" Class: Session database
"""
from datetime import datetime, timedelta, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Class: SessionDBAuth
    """
    def create_session(self, user_id=None):
        """ Generator: Session ID
        """
        sess_id = super().create_session(user_id)
        if user_id is None:
            return None
        usr_sess = UserSession(user_id=user_id, session_id=sess_id)
        usr_sess.save()
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns user_id from session_id
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        is_usr_valid = UserSession.search({'session_id': session_id})
        if not is_usr_valid:
            return None
        is_usr_valid = is_usr_valid[0]
        strt_time = is_usr_valid.created_at
        delta_tme = timedelta(seconds=self.session_duration)
        if (strt_time + delta_tme) < datetime.now():
            return None
        return is_usr_valid.user_id

    def destroy_session(self, request=None):
        """ User session destroy from session_id from request cookie
        """
        cookie_info = self.session_cookie(request)
        if cookie_info is None:
            return False
        if not self.user_id_for_session_id(cookie_info):
            return False
        usr_sess = UserSession.search({'session_id': cookie_info})
        if not usr_sess:
            return False
        usr_sess = usr_sess[0]
        try:
            usr_sess.remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
    