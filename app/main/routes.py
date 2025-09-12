from flask import Blueprint, flash, jsonify, redirect, render_template, session, url_for, request

from app.decorators import login_required, no_cache
from app.main.services import get_communication_item, get_category_data, get_user_id
from app.models.card_items import CardItem
from db.language_dao import LanguageDAO
from db.user_dao import UserDAO
from db.user_session_dao import UserSessionDAO
from app.utils.add_data_manager import AppDataManager
from app.utils.translator.deep_translator_service import _translate_sync
from app.forms.main_forms import ChangePasswordForm
from app.models.user import User

main_bp = Blueprint("main", __name__, url_prefix="/main")

@main_bp.route("/home")
@login_required
@no_cache
def home():# Reset toolbar on entering Home
    session["toolbar_expanded"] = False
    categories = get_category_data()
    user_info = UserSessionDAO.get_user_info(AppDataManager.load_session())
    username = user_info.username if user_info else "Guest"
    cardData: list[CardItem] = []
    for item in categories:
        translated_text = _translate_sync(  # <-- use sync translation
            item.text,
            AppDataManager.get_language()
        )
        cardData.append(
            CardItem(
                id=item.category_id,
                type="category",
                text=translated_text,   # use translated text here
                image_source=item.icon_path,
                is_standalone=item.is_standalone
            )
        )
    return render_template("main/home.html",
                           cardData=cardData,
                           username=username,
                           toolbar_expanded=session["toolbar_expanded"])

@main_bp.route("/communication-items/<int:category_id>")
@login_required
def communication_items(category_id):# Reset toolbar on entering Home
    session["toolbar_expanded"] = False
    items = get_communication_item(category_id)
    cardData: list[CardItem] = []

    for item in items:
        translated_text = _translate_sync(  # <-- use sync translation
            item.text,
            AppDataManager.get_language()
        )
        cardData.append(
            CardItem(
                id=item.item_id,
                type="category",
                text=translated_text,   # use translated text here
                image_source=item.icon_path,
                is_standalone=True
            )
        )

    return render_template("main/communication_items.html",
                           cardData=cardData,
                           toolbar_expanded=session["toolbar_expanded"])

@main_bp.route("/settings")
@login_required
def settings():
    return render_template("main/settings.html")

@main_bp.route("/language")
@login_required
def language():
    all_languages = LanguageDAO.get_all()  # fetch all languages
    return render_template("main/language.html", languages=all_languages)

@main_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    token = AppDataManager.load_session()
    if UserSessionDAO.logout(token):
        return jsonify({"logged_out": True})
    return jsonify({"logged_out": False})

@main_bp.route("/select-language", methods=["POST"])
@login_required
def select_language():
    data = request.get_json()
    language_code = data.get("code")
    
    if not language_code:
        return jsonify({"success": False, "message": "No language code provided"}), 400

    # Save the selected language in session
    AppDataManager.save_language(language_code)

    return jsonify({"success": True, "message": f"Language {language_code} selected"})

@main_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user_id = get_user_id()
        if user_id:
            success, message = UserDAO.change_password(user_id, form.current_password.data, form.new_password.data)
            if success:
                flash("Password changed successfully!", "success")
            else:
                flash(message, "danger")
    return render_template("main/change_password.html", form=form)

@main_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    token = AppDataManager.load_session()
    user = None
    if token:
        user = UserSessionDAO.get_user_info(token)

    if request.method == "POST":
        new_username = request.form.get("username")
        new_email = request.form.get("email")

        updated_user = User(user_id=user.user_id, username=new_username, email=new_email)
        success = UserDAO.update(updated_user)

        if not success:
            flash("Username or email already exists. Please choose another.", "danger")
            return redirect(url_for("main.profile"))

        flash("Profile updated successfully!", "success")
        return redirect(url_for("main.profile"))

    return render_template("main/profile.html", user=user)

@main_bp.route("/about")
@login_required
def about():
    return render_template("main/about.html")

@main_bp.route("/delete-profile", methods=["POST"])
@login_required
def delete_profile():
    token = AppDataManager.load_session()
    if token:
        user_id = get_user_id()
        if user_id:
            # delete user from DB
            result = UserDAO.delete(user_id)
            if result:
                AppDataManager.clear_session()
                flash("Profile deleted successfully.", "success")
                return redirect(url_for("auth.login"))
    flash("Unable to delete profile.", "danger")
    return redirect(url_for("main.profile"))