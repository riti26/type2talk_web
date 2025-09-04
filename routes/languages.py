from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db.language_dao import LanguageDAO
from db.user_dao import UserDAO
from db.user_session_dao import UserSessionDAO
from utils.add_data_manager import AppDataManager

language_bp = Blueprint("languages", __name__, template_folder="templates")

@language_bp.route("/languages", methods=["GET", "POST"])
def view_languages():
    token = session.get("session_token")
    user_id = UserSessionDAO.get_user_id(token) if token else None

    # Load all languages from database
    all_languages = LanguageDAO.get_all()

    # Handle search filter
    search_query = request.args.get("search", "").lower()
    if search_query:
        filtered_languages = [
            lang for lang in all_languages if search_query in lang.name.lower()
        ]
    else:
        filtered_languages = all_languages

    # Handle language selection
    if request.method == "POST":
        selected_code = request.form.get("language_code")
        if selected_code and user_id:
            # Update language in database
            UserDAO.update_language(user_id, selected_code)
            AppDataManager.save_language(selected_code)
            flash(f"Selected language: {selected_code}", "success")
            return redirect(url_for("home.home"))

    return render_template(
        "languages.html",
        languages=filtered_languages,
        search_query=search_query
    )
