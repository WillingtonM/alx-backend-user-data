#!/usr/bin/env python3
"""
Simple end-to-end (E2E) integration.
"""
import requests


BASE_URL = "http://0.0.0.0:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
    Tests register a user.
    """
    req_url = "{}/users".format(BASE_URL)
    data = {
        'email': email,
        'password': password,
    }
    
    res = requests.post(req_url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}

    msg = {"message": "email already registered"}
    res = requests.post(req_url, data=data)
    assert res.status_code == 400
    assert res.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test for validating log in with wrong password.
    """
    req_url = "{}/sessions".format(BASE_URL)
    data = {
        'email': email,
        'password': password,
    }
    res = requests.post(req_url, data=data)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Test for validating log in.
    """
    req_url = "{}/sessions".format(BASE_URL)
    data = {
        'email': email,
        'password': password,
    }
    res = requests.post(req_url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Test for validating profile request without log in.
    """
    req_url = "{}/profile".format(BASE_URL)
    res = requests.get(req_url)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Tests retrieving profile information whilst logged in.
    """
    req_url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.get(req_url, cookies=req_cookies)
    assert res.status_code == 200
    assert "email" in res.json()


def log_out(session_id: str) -> None:
    """
    Tests logging out from session.
    """
    req_url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    res = requests.delete(req_url, cookies=req_cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Test for validating password reset.
    """
    req_url = "{}/reset_password".format(BASE_URL)
    data = {'email': email}
    res = requests.post(req_url, data=data)
    assert res.status_code == 200
    assert "email" in res.json()
    assert res.json()["email"] == email
    assert "reset_token" in res.json()
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests updating a user's password reset.
    """
    req_url = "{}/reset_password".format(BASE_URL)
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(req_url, data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    session_id = log_in(EMAIL, PASSWD)
    reset_token = reset_password_token(EMAIL)

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    profile_logged(session_id)
    log_out(session_id)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
