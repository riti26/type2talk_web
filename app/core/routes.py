from flask import Blueprint, redirect, url_for
from app.utils.add_data_manager import AppDataManager
from db.user_session_dao import UserSessionDAO

core_bp = Blueprint("core", __name__)

@core_bp.route("/")
def index():
    # Redirect to dashboard if logged in, otherwise login page
    session_token = AppDataManager.load_session()
    if session_token:
        user_session = UserSessionDAO.get_session(session_token)
        if user_session:
            return redirect(url_for("main.home"))
    return redirect(url_for("auth.login"))
