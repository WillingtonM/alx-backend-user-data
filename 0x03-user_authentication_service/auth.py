#!/usr/bin/env python3
""" Module contains authentication methods for users
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
from typing import Optional


def _hash_password(password: str) -> bytes:
    """ Takes in password argument
    Returns: bytes which are salted hash of input
    """
    bytes_pass = password.encode()
    passwd_hash = bcrypt.hashpw(bytes_pass, bcrypt.gensalt())
    return passwd_hash


def _generate_uuid(self) -> str:
    """ Generates a UUID
    Returns: string representation
    """
    return str(uuid4())


class Auth:
    """ Auth class to interact with authentication database.
    """

    def __init__(self):
        """ Initialize instances of authentication
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Adds a new user to the database
        Returns: user, if user already exists raise ValueError
        """
        try:
            usr = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(usr.email))
        except (InvalidRequestError, NoResultFound):
            hashed_pwd = _hash_password(password)
            usr = self._db.add_user(email, hashed_pwd)
            return usr

    def valid_login(self, email: str, password: str) -> bool:
        """ Checks if a user's login details are correct and valid
        Returns: True otherwise False
        """
        try:
            usr = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), usr.hashed_password):
                return True
            else:
                return False
        except (InvalidRequestError, NoResultFound):
            return False


    def create_session(self, email: str) -> Optional[str]:
        """ Creates new session for user
        Returns: session id
        """
        try:
            usr = self._db.find_user_by(email=email)
            sess_id = self._generate_uuid()
            self._db.update_user(usr.id, session_id=sess_id)
            return usr.session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """ Retrieves user based on given session ID
        Returns: user in session_id or None if not found
        """
        try:
            usr = self._db.find_user_by(session_id=session_id)
            return usr
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys session associated with given user
        Returns: user corresponding to user_id as None
        """
        try:
            usr = self._db.find_user_by(id=user_id)
            self._db.update_user(usr.id, session_id=None)
        except Exception as e:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Updates user's password given user's reset token
        or raise a ValueError exception if user doesn't exists
        """
        try:
            usr = self._db.find_user_by(email=email)
            rst_token = self._generate_uuid()
            self._db.update_user(usr.id, reset_token=rst_token)
            return usr.reset_token
        except Exception as e:
            raise ValueError
