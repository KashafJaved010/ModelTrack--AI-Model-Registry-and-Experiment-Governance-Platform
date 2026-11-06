import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.core import User, Role
from app.models.registry import MODEL_REGISTRY
from app.utils.auth import login_user, logout_user

bp = Blueprint("auth", __name__, url_prefix="/auth")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        errors = []
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        if not errors:
            user = User.query.filter_by(username=username, is_deleted=False).first()
            if user and user.check_password(password) and user.is_active:
                login_user(user)
                flash(f"Welcome back, {user.username}!", "success")
                return redirect(url_for("dashboard.index"))
            errors.append("Invalid username or password.")
        for e in errors:
            flash(e, "danger")
    return render_template("auth/login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        full_name = request.form.get("full_name", "").strip()
        pw = request.form.get("password", "")
        pw2 = request.form.get("password2", "")
        errors = []
        if len(username) < 3:
            errors.append("Username must be at least 3 characters.")
        if User.query.filter_by(username=username).first():
            errors.append("Username already exists.")
        if not EMAIL_RE.match(email):
            errors.append("Invalid email address.")
        if User.query.filter_by(email=email).first():
            errors.append("Email already registered.")
        if len(pw) < 6:
            errors.append("Password must be at least 6 characters.")
        if pw != pw2:
            errors.append("Passwords do not match.")
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("auth/register.html", form=request.form)

        # Assign the default ML Engineer role
        default_role = Role.query.filter_by(name="ML Engineer").first()
        user = User(
            username=username, email=email, full_name=full_name,
            created_by=1, status="active",
        )
        user.set_password(pw)
        if default_role:
            user.roles.append(default_role)
        from app.extensions import db
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please log in.", "success")
        return redirect(url_for("auth.login"))  # PRG
    return render_template("auth/register.html", form={})


@bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))