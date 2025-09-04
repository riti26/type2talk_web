from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db.user_dao import UserDAO
from db.user_session_dao import UserSessionDAO
from utils.add_data_manager import AppDataManager

login_bp = Blueprint("login", __name__, template_folder="../templates")

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user, result = UserDAO.login(username, password)

        if user is None:
            if result == "username":
                flash("Invalid username", "user_error")
            elif result == "password":
                flash("Invalid password", "password_error")
            return render_template("login.html")
        
        # ✅ Successful login
        return redirect(url_for("home.home"))

    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.clear()
    AppDataManager.clear_session()
    return redirect(url_for("login.login"))

@login_bp.route("/skip")
def skip_login():
    # just redirect to home page (or whatever screen you want)
    return redirect(url_for("home.home"))
