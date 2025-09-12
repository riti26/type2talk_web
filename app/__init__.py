from threading import Thread
from flask import Flask

from app.ui.main_toolbar import MainToolbar
from app.utils.add_data_manager import AppDataManager
from config import DB_PATH, SECRET_KEY
from db.schema import init_db
from db.user_session_dao import UserSessionDAO
from .core.routes import core_bp
from .auth.routes import auth_bp
from .main.routes import main_bp
from .components.custom_card_routes import custom_card_bp
from .components.actions_toolbar_routes import actions_toolbar_bp
from .ui.phrase_toolbar import PhraseToolbar

def create_app():
    app = Flask(__name__, 
                static_folder="static",     # ✅ tell Flask your static path
                instance_relative_config=True)

    app.config.from_mapping(
            SECRET_KEY=SECRET_KEY,  # Change in production
            SQLALCHEMY_DATABASE_URI=DB_PATH,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    # Blueprint registration
    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(custom_card_bp)
    app.register_blueprint(actions_toolbar_bp)

    # Initialize DB in background
    Thread(target=init_db_thread, args=(app,), daemon=True).start()

    # Global context
    @app.context_processor
    def inject_phrase_toolbar():
        return { "phrase_toolbar": PhraseToolbar()}
    
    @app.context_processor
    def inject_main_toolbar():
        # Create the toolbar object
        toolbar = MainToolbar()

        token = AppDataManager.load_session()
        username = "Guest"
        # Load user info
        if AppDataManager.load_session():
            user_info = UserSessionDAO.get_user_info(token)
            username = user_info.username if user_info else "Guest"

        # Return both toolbar and username
        return {
            "main_toolbar": toolbar,
            "username": username
        }


    return app

def init_db_thread(app):
    """Heavy DB initialization or pre-loading"""
    with app.app_context():
        try:
            init_db()
        except Exception as e:
            print("Background DB init failed:", e)
        