#!/usr/bin/env python3
"""
    Module for encrypting passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
        Hashes password using random salt.
        Returns: salted, hashed password, which is byte string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
        Checks and validates provided password matches hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
