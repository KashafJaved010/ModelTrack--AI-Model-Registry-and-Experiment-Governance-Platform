from functools import wraps
from flask import session, redirect, url_for, flash, g
from app.models.core import User


def login_user(user, remember=False):
    session["user_id"] = user.id
    session["username"] = user.username
    session["roles"] = [r.name for r in user.roles]


def logout_user():
    session.clear()


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return User.query.filter_by(id=uid, is_deleted=False).first()


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        g.user = user
        return view(*args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                flash("Please log in first.", "warning")
                return redirect(url_for("auth.login"))
            if user.has_role("Admin") or user.has_any_role(allowed_roles):
                g.user = user
                return view(*args, **kwargs)
            flash("You do not have permission for that action.", "danger")
            return redirect(url_for("dashboard.index"))
        return wrapper
    return decorator