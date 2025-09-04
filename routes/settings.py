# routes/settings.py
from flask import Blueprint, render_template, redirect, url_for, session

settings_bp = Blueprint("settings", __name__, template_folder="../templates")

# Example login check function
def user_logged_in():
    return "session_token" in session

# List of settings options (like in Kivy)
SETTINGS_OPTIONS = [
    {"id": 1, "title": "Change Password", "endpoint": "change_password.change_password"},
    {"id": 2, "title": "Other Settings", "endpoint": "other_settings.other_settings"}
]

@settings_bp.route("/settings")
def settings():
    if not user_logged_in():
        return redirect(url_for("login.login"))
    return render_template("settings.html", settings=SETTINGS_OPTIONS)
