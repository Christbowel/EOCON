from flask import session
from app.models.user import find_user_by_id


def login_user(user_id):
    session["user_id"] = user_id


def logout_user():
    session.pop("user_id", None)


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return find_user_by_id(user_id)


def require_auth():
    return current_user()


def require_role(role):
    user = current_user()
    if user is None:
        return None
    if user["role"] != role and user["role"] != "admin":
        return None
    return user
