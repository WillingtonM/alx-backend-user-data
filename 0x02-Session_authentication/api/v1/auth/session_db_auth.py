#!/usr/bin/env python3
"""Module for session database authentication
"""
from datetime import datetime, timedelta

from models.user_session import UserSession

from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """
    Session authentication class wth database storage & expiration support.
    """

    def create_session(self, user_id: str) -> str:
        """
        Creates & stores session id for the user.

        Args:
            user_id: User id to be associated with session.
        Returns: Session id.
        """
        sess_id = super().create_session(user_id)

        if isinstance(sess_id, str):
            kwargs = {
                'user_id': user_id,
                'sess_id': sess_id,
            }
            usr_sess = UserSession(**kwargs)
            usr_sess.save()
            return sess_id

    def user_id_for_session_id(self, session_id: str) -> str:
        """
        Retrieves user id of user associated with given session id.

        Args:
            session_id: Session id.
        Returns: User id associated with the session id.
        """
        try:
            sessns = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessns) <= 0:
            return None
        
        cur_time = datetime.now()
        span_time = timedelta(seconds=self.session_duration)
        time_exp = sessns[0].created_at + span_time
        if time_exp < cur_time:
            return None
        
        return sessns[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroys authenticated session.

        Args:
            request: Request object.
        Returns: Indicates if session was destroyed successfully.
        """
        sess_id = self.session_cookie(request)
        try:
            sessns = UserSession.search({'session_id': sess_id})
        except Exception:
            return False
        if len(sessns) <= 0:
            return False
        
        sessns[0].remove()
        return True
