from flask import Blueprint, render_template, request, redirect, url_for, flash
from db.user_dao import UserDAO
from utils.email.smtp_service import send_email
from utils.password.password_generator import generate_random_password

forgot_password_bp = Blueprint("forgot_password", __name__)

@forgot_password_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("reset_email", "").strip()

        if not email:
            flash("Please enter your email", "error")
            return redirect(url_for("forgot_password.forgot_password"))

        user = UserDAO.get_user_by_email(email)

        if not user:
            flash("No account found with that email", "error")
            return redirect(url_for("forgot_password.forgot_password"))

        # Generate + reset password
        password = generate_random_password()
        UserDAO.force_reset_password(user.user_id, password)

        message_body = f"Your new password is: {password}"
        if send_email(email, "Reset Password", message_body):
            flash("A reset link has been sent to your email", "success")
        else:
            flash("Error sending email. Please try again later.", "error")

        return redirect(url_for("login.login"))  # go to login after reset

    return render_template("forgot_password.html")
