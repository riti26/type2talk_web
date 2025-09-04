# routes/register.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db.user_dao import EmailExistsError, UserDAO, UsernameExistsError
from utils.password.hash import encrypt_password

register_bp = Blueprint("register", __name__, template_folder="../templates")

def validate_inputs(username, email, password):
    errors = {}

    # Username validation
    if not username:
        errors["username_error"] = "Please enter username"

    # Email validation
    if not email:
        errors["email_error"] = "Please enter email"
    elif "@" not in email or "." not in email:
        errors["email_error"] = "Invalid email format"

    # Password validation
    if not password:
        errors["password_error"] = "Please enter password"
    elif len(password) < 8:
        errors["password_error"] = "Password must be at least 8 characters"

    return errors

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        errors = validate_inputs(username, email, password)

        if errors:
            # Pass errors and previously entered data back to template
            return render_template("register.html", errors=errors, username=username, email=email)

        try:
            encrypted_password = encrypt_password(password)
            UserDAO.register_user(username, email, encrypted_password)
            flash("Registration successful!", "success")
            return redirect(url_for("login.login"))
        except UsernameExistsError:
            errors["username_error"] = "Username already exists!"
        except EmailExistsError:
            errors["email_error"] = "Email already registered!"

        return render_template("register.html", errors=errors, username=username, email=email)

    return render_template("register.html")
