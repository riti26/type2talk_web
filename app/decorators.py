from functools import wraps
from os import abort
from flask import redirect, url_for, flash, session
from db.user_session_dao import UserSessionDAO

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = session.get("session_token")  # directly from Flask session
        user_session = UserSessionDAO.get_session(session_token)
        if not user_session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
