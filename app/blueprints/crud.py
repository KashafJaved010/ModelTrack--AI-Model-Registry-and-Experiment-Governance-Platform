from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, abort, g, current_app
)
from app.extensions import db
from app.models.registry import MODEL_REGISTRY, get_model_meta, HIDDEN_FIELDS
from app.models.core import AuditLog
from app.utils.auth import login_required
from app.utils.forms import apply_form_to_model


bp = Blueprint("crud", __name__, url_prefix="/m")

ADMIN_ONLY_MODELS = {"users", "roles", "permissions", "user_roles", "role_permissions"}


def _require_admin_for(model):
    if model in ADMIN_ONLY_MODELS and not g.user.has_role("Admin"):
        flash("Only administrators can manage this section.", "danger")
        return redirect(url_for("crud.index"))
    return None


def _log(action, entity, entity_id, details=None):
    log = AuditLog(
        user_id=g.user.id if getattr(g, "user", None) else None,
        action=action,
        entity_type=entity,
        entity_id=entity_id,
        details=details,
        created_by=g.user.id if getattr(g, "user", None) else None,
    )
    db.session.add(log)


def _load_fk_options(meta):
    """For each FK field, return [(id, label), ...] from the referenced table."""
    options = {}
    for f in meta["fields"]:
        if not f["fk"]:
            continue
        ref_table, _ = f["fk"].split(".")
        ref_meta = MODEL_REGISTRY.get(ref_table)
        if not ref_meta:
            continue
        RefModel = ref_meta["model"]
        display_field = None
        for col in RefModel.__table__.columns:
            if col.name == "id" or col.name in HIDDEN_FIELDS:
                continue
            if "String" in type(col.type).__name__:
                display_field = col.name
                break
        rows = RefModel.query.filter_by(is_deleted=False).limit(300).all()
        options[f["name"]] = [
            (
                row.id,
                f"#{row.id} — {getattr(row, display_field, '')}"
                if display_field else f"#{row.id}",
            )
            for row in rows
        ]
    return options


@bp.route("/")
@login_required
def index():
    modules = {}
    for key, meta in MODEL_REGISTRY.items():
        modules.setdefault(meta["module"], []).append(meta)
    return render_template("crud/index.html", modules=modules)


@bp.route("/<model>/")
@login_required
def list_items(model):
    meta = get_model_meta(model)
    if not meta:
        abort(404)
    redir = _require_admin_for(model)
    if redir:
        return redir
    Model = meta["model"]

    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config.get("ITEMS_PER_PAGE", 10)

    query = Model.query.filter_by(is_deleted=False)
    if status:
        query = query.filter(Model.status == status)

    if q and meta["list_fields"]:
        first = meta["list_fields"][0]
        col = getattr(Model, first)
        if hasattr(col, "ilike"):
            query = query.filter(col.ilike(f"%{q}%"))

    pagination = query.order_by(Model.id.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return render_template(
        "crud/list.html",
        meta=meta,
        items=pagination.items,
        pagination=pagination,
        q=q,
        status=status,
    )


@bp.route("/<model>/new", methods=["GET", "POST"])
@login_required
def create_item(model):
    meta = get_model_meta(model)
    if not meta:
        abort(404)
    redir = _require_admin_for(model)
    if redir:
        return redir
    if model == "users":
        flash("Use the registration page to create new users.", "info")
        return redirect(url_for("auth.register"))

    Model = meta["model"]

    if request.method == "POST":
        obj = Model()
        apply_form_to_model(obj, request.form, meta["fields"], g.user.id)
        obj.created_by = g.user.id
        try:
            db.session.add(obj)
            db.session.flush()
            _log("create", model, obj.id, f"Created {meta['label']}")
            db.session.commit()
            flash(f"{meta['label']} created.", "success")
            return redirect(url_for("crud.list_items", model=model))
        except Exception as exc:
            db.session.rollback()
            flash(f"Save failed: {exc}", "danger")

    return render_template(
        "crud/form.html",
        meta=meta,
        item=None,
        mode="create",
        fk_options=_load_fk_options(meta),
    )


@bp.route("/<model>/<int:id>")
@login_required
def detail(model, id):
    meta = get_model_meta(model)
    if not meta:
        abort(404)
    redir = _require_admin_for(model)
    if redir:
        return redir
    Model = meta["model"]
    # B7 fix: allow viewing soft-deleted records so teacher can see the warning
    item = Model.query.filter_by(id=id).first_or_404()
    return render_template("crud/detail.html", meta=meta, item=item)


@bp.route("/<model>/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(model, id):
    meta = get_model_meta(model)
    if not meta:
        abort(404)
    redir = _require_admin_for(model)
    if redir:
        return redir
    Model = meta["model"]
    item = Model.query.filter_by(id=id, is_deleted=False).first_or_404()

    if request.method == "POST":
        try:
            apply_form_to_model(item, request.form, meta["fields"], g.user.id)
            _log("update", model, item.id, f"Updated {meta['label']}")
            db.session.commit()
            flash(f"{meta['label']} updated.", "success")
            return redirect(url_for("crud.detail", model=model, id=item.id))
        except Exception as exc:
            db.session.rollback()
            flash(f"Update failed: {exc}", "danger")

    return render_template(
        "crud/form.html",
        meta=meta,
        item=item,
        mode="edit",
        fk_options=_load_fk_options(meta),
    )


@bp.route("/<model>/<int:id>/delete", methods=["POST"])
@login_required
def delete_item(model, id):
    meta = get_model_meta(model)
    if not meta:
        abort(404)
    redir = _require_admin_for(model)
    if redir:
        return redir
    Model = meta["model"]
    item = Model.query.filter_by(id=id, is_deleted=False).first_or_404()
    try:
        item.soft_delete(g.user.id)
        _log("soft_delete", model, item.id, f"Soft-deleted {meta['label']}")
        db.session.commit()
        flash(f"{meta['label']} soft-deleted.", "info")
    except Exception as exc:
        db.session.rollback()
        flash(f"Delete failed: {exc}", "danger")
    return redirect(url_for("crud.list_items", model=model))