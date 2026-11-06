from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.extensions import db
from app.models.core import User, Role
from app.utils.auth import login_required, role_required

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/users")
@role_required("Admin")
def users():
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    query = User.query.filter_by(is_deleted=False)
    if q:
        query = query.filter(User.username.ilike(f"%{q}%"))
    pagination = query.order_by(User.id.desc()).paginate(page=page, per_page=10, error_out=False)
    roles = Role.query.filter_by(is_deleted=False).all()
    return render_template(
        "admin/users.html", pagination=pagination, roles=roles, q=q
    )


@bp.route("/users/<int:id>/toggle", methods=["POST"])
@role_required("Admin")
def toggle_user(id):
    user = User.query.get_or_404(id)
    user.is_active = not user.is_active
    user.updated_by = g.user.id
    db.session.commit()
    flash(f"User {user.username} is now {'active' if user.is_active else 'disabled'}.", "info")
    return redirect(url_for("admin.users"))


@bp.route("/users/<int:id>/role", methods=["POST"])
@role_required("Admin")
def set_role(id):
    user = User.query.get_or_404(id)
    role_name = request.form.get("role")
    role = Role.query.filter_by(name=role_name).first()
    if role and role not in user.roles:
        user.roles.append(role)
        db.session.commit()
        flash(f"Added role {role_name} to {user.username}.", "success")
    return redirect(url_for("admin.users"))


@bp.route("/users/<int:id>/soft-delete", methods=["POST"])
@role_required("Admin")
def soft_delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == g.user.id:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for("admin.users"))
    user.soft_delete(g.user.id)
    db.session.commit()
    flash(f"User {user.username} soft-deleted.", "info")
    return redirect(url_for("admin.users"))