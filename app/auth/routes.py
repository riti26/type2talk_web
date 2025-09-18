from app.decorators import logged_out_required, no_cache
from app.forms.auth_forms import ForgotPasswordForm, LoginForm, SignupForm
from app.utils.email.smtp_service import send_email
from app.utils.password.password_generator import generate_random_password
from db.user_dao import EmailExistsError, UserDAO, UsernameExistsError
from flask import Blueprint, render_template, redirect, url_for, flash

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
@logged_out_required
@no_cache
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user, result = UserDAO.login(form.username.data, form.password.data)
        if user is None:
            # result can indicate which field failed
            if result == "username":
                flash("Invalid username", "user_error")
            elif result == "password":
                flash("Invalid password", "password_error")
            else:
                # fallback generic error
                flash("Invalid credentials", "danger")
            return render_template("auth/login.html", form=form)

        # login successful
        return redirect(url_for("main.home"))

    return render_template("auth/login.html", form=form)

@auth_bp.route("/signup", methods=["GET", "POST"])
@logged_out_required
@no_cache
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            UserDAO.register_user(form.username.data, form.email.data, form.password.data)
            flash("Account created! Please log in.", "success")
        except UsernameExistsError:
            form.username.errors.append("Username already exists!")
        except EmailExistsError:
            form.email.errors.append("Email already registered!")
    return render_template("auth/signup.html", form=form)

@auth_bp.route("/forgot_password", methods=["GET", "POST"])
@logged_out_required
@no_cache
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = UserDAO.get_user_by_email(form.email.data)

        if not user:
            flash("No account found with that email", "error")
            return redirect(url_for("auth.forgot_password"))

        # Generate + reset password
        password = generate_random_password()
        UserDAO.force_reset_password(user.user_id, password)

        message_body = f"Your new password is: {password}"
        if send_email(user.email, "Reset Password", message_body):
            flash("A reset link has been sent to your email", "success")
        else:
            flash("Error sending email. Please try again later.", "error")
            # **Redirect after POST**
        return redirect(url_for("auth.forgot_password"))
    return render_template("auth/forgot_password.html", form=form)