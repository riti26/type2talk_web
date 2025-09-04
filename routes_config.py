from flask import render_template, session, redirect, url_for
from routes import RouteManager
from routes.routes import Route

def home_view():
    token = session.get("session_token")
    if token:
        from db.user_session_dao import UserSessionDAO
        user_session = UserSessionDAO.validate_session(token)
        if user_session:
            user_info = UserSessionDAO.get_user_info(token)
            return render_template("home.html", user=user_info)
    return redirect(url_for("login.login"))

RouteManager.register(Route(
    path="/home",
    view_func=home_view,
    login_required=True,
    endpoint="home"
))
