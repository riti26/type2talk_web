from flask import Flask, session, redirect, url_for, render_template
from db.schema import init_db
from db.user_session_dao import UserSessionDAO
from db.category_dao import CategoryDAO
from db.menu_dao import MenuDAO
from utils.add_data_manager import AppDataManager
from routes.routes import RouteManager, login_bp
from routes.toolbar_routes import toolbar_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"

    # Initialize DB
    init_db()

    # Register blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(toolbar_bp)

    # Init routes from RouteManager
    RouteManager.init_routes(app)

    # ---------------- Home ----------------
    @app.route("/home")
    def home():
        token = session.get("session_token") or AppDataManager.load_session()
        if token:
            user_session = UserSessionDAO.validate_session(token)
            if user_session:
                user_info = UserSessionDAO.get_user_info(token)
                user_id = user_info["user_id"]

                # Fetch categories for dashboard
                categories = CategoryDAO.get_all(user_id=user_id)

                # Example recent activity
                activities = [
                    {"text": "Issue #123 updated"},
                    {"text": "RFI #456 closed"},
                    {"text": "Document XYZ uploaded"}
                ]

                # Phrase toolbar placeholder
                toolbar_phrase = []  # Or fetch from DB/session

                # Load menu structure dynamically
                root_menus = MenuDAO.get_root_menus()
                menu_structure = []
                for root in root_menus:
                    children = MenuDAO.get_children(root.id)
                    menu_structure.append({"root": root, "children": children})

                return render_template(
                    "home.html",
                    user=user_info,
                    categories=categories,
                    activities=activities,
                    toolbar_phrase=toolbar_phrase,
                    menu_structure=menu_structure
                )
        return redirect(url_for("login.login"))

    # ---------------- Index ----------------
    @app.route("/")
    def index():
        token = AppDataManager.load_session()
        if token:
            user_session = UserSessionDAO.get_session(token)
            if user_session:
                return redirect(url_for("home"))
        return redirect(url_for("login.login"))

    # ---------------- Category Items ----------------
    @app.route("/category/<int:category_id>")
    def category_items_view(category_id):
        category = CategoryDAO.get_by_id(category_id)
        if not category:
            return "Category not found", 404

        items = []  # Replace with DB call for items in this category
        toolbar_phrase = []  # Optionally fetch relevant toolbar phrases

        return render_template(
            "category_items.html",
            category=category,
            items=items,
            toolbar_phrase=toolbar_phrase
        )

    return app

# ---------------- Run App ----------------
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
