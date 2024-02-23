#!/usr/bin/env python3
"""
User module
"""
import hashlib
from models.base import Base


class User(Base):
    """
    User class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize User instance
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    @property
    def password(self) -> str:
        """
        Getter of password
        """
        return self._password

    @password.setter
    def password(self, psw: str):
        """
        Setter of new password: encrypt in SHA256
        """
        if psw is None or type(psw) is not str:
            self._password = None
        else:
            self._password = hashlib.sha256(psw.encode()).hexdigest().lower()

    def is_valid_password(self, psw: str) -> bool:
        """
        Validate  password
        """
        if psw is None or type(psw) is not str:
            return False
        if self.password is None:
            return False
        psw_e = psw.encode()
        return hashlib.sha256(psw_e).hexdigest().lower() == self.password

    def display_name(self) -> str:
        """
        Display User's name based on email/first_name/last_name
        """
        if self.email is None and self.first_name is None \
                and self.last_name is None:
            return ""
        if self.first_name is None and self.last_name is None:
            return "{}".format(self.email)
        if self.last_name is None:
            return "{}".format(self.first_name)
        if self.first_name is None:
            return "{}".format(self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)
