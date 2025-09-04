from flask import render_template, redirect, url_for, session
from db.category_dao import CategoryDAO
from ui.phrase_toolbar import PhraseToolbar
from flask import Blueprint, request, flash
from db.user_dao import UserDAO
from db.user_session_dao import UserSessionDAO
from utils.add_data_manager import AppDataManager

# -------------------------
# RouteManager
# -------------------------
class Route:
    def __init__(self, path, template=None, view_func=None, login_required=False, endpoint=None):
        self.path = path
        self.template = template
        self.view_func = view_func
        self.login_required = login_required
        self.endpoint = endpoint or (view_func.__name__ if view_func else template)

class RouteManager:
    routes = []

    @classmethod
    def register(cls, route: Route):
        cls.routes.append(route)

    @classmethod
    def init_routes(cls, app):
        for r in cls.routes:
            if r.view_func:
                view = r.view_func
                if r.login_required:
                    def wrapped(*args, **kwargs):
                        if not session.get("session_token"):
                            return redirect(url_for("login.login"))
                        return view(*args, **kwargs)
                    app.add_url_rule(r.path, view_func=wrapped, endpoint=r.endpoint)
                else:
                    app.add_url_rule(r.path, view_func=view, endpoint=r.endpoint)
            elif r.template:
                def auto_view():
                    if r.login_required and not session.get("session_token"):
                        return redirect(url_for("login.login"))
                    return render_template(r.template, toolbar_phrase=PhraseToolbar.get_phrase())
                app.add_url_rule(r.path, view_func=auto_view, endpoint=r.endpoint)

# -------------------------
# Login Blueprint
# -------------------------
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
        return redirect(url_for("home"))

    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.clear()
    AppDataManager.clear_session()
    return redirect(url_for("login.login"))

@login_bp.route("/skip")
def skip_login():
    return redirect(url_for("home"))

def home_view():
    token = AppDataManager.load_session()
    if not token:
        return redirect(url_for("login.login"))

    user_info = UserSessionDAO.get_user_info(token)
    user_id = user_info["user_id"] if user_info else None

    # Fetch categories from DB
    categories = CategoryDAO.get_all(user_id=user_id)

    # Set default icon if missing
    for cat in categories:
        if not cat.icon_path:
            cat.icon_path = "/static/assets/default.png"

    # Toolbar phrases
    toolbar_phrase = PhraseToolbar.get_phrase()  # returns list of dicts

    # Example recent activity
    activities = [
        {"text": "Issue #123 updated"},
        {"text": "RFI #456 closed"},
        {"text": "Document XYZ uploaded"}
    ]

    # Pass categories directly (not cards)
    return render_template(
        "home.html",
        categories=categories,
        toolbar_phrase=toolbar_phrase,
        activities=activities,
        user=user_info
    )
