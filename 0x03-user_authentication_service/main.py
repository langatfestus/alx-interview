#!/usr/bin/env python3
"""
Main file
"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    url = f"{BASE_URL}/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 200, f"Failed to register user: {response.text}"


def log_in_wrong_password(email: str, password: str) -> None:
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401, f"Login with wrong password should fail: {response.text}"


def log_in(email: str, password: str) -> str:
    url = f"{BASE_URL}/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)

    assert response.status_code == 200, f"Login failed: {response.text}"

    json_response = response.json()

    # Adjust the logic based on your actual server response structure
    session_id = json_response.get("session_id")

    if session_id is None:
        session_id = json_response.get("session_id_generated")
        if session_id is None:
            raise AssertionError(
                f"Session ID is missing in the response: {json_response}")

    return session_id


def profile_unlogged() -> None:
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403, f"Profile should be inaccessible when unlogged: {response.text}"


def profile_logged(session_id: str) -> None:
    url = f"{BASE_URL}/profile"
    headers = {"X-Session-ID": session_id}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Failed to access profile when logged in: {response.text}"


def log_out(session_id: str) -> None:
    url = f"{BASE_URL}/sessions"
    headers = {"X-Session-ID": session_id}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200, f"Failed to log out: {response.text}"


def reset_password_token(email: str) -> str:
    url = f"{BASE_URL}/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    assert response.status_code == 200, f"Failed to get reset token: {response.text}"
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    url = f"{BASE_URL}/update_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200, f"Failed to update password: {response.text}"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
