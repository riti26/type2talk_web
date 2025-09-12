from functools import wraps
from os import abort
from flask import make_response, redirect, url_for, flash, session
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

def logged_out_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_token = session.get("session_token")  # directly from Flask session
        user_session = UserSessionDAO.get_session(session_token)
        if user_session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated_function

def no_cache(view):
    """Decorator to add no-cache headers to a Flask response."""
    @wraps(view)
    def decorated_function(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return decorated_function