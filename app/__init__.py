import os
from datetime import datetime
from flask import Flask, render_template
from app.config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Import models so they register with SQLAlchemy metadata
    from app import models  # noqa: F401

    # Register blueprints
    from app.blueprints.auth import bp as auth_bp
    from app.blueprints.dashboard import bp as dash_bp
    from app.blueprints.crud import bp as crud_bp
    from app.blueprints.admin import bp as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(crud_bp)
    app.register_blueprint(admin_bp)

    # ---- Jinja filters (fix B1 and B8) ----
    @app.template_filter("field_value")
    def field_value(obj, name):
        if obj is None:
            return ""
        val = getattr(obj, name, None)
        if val is None:
            return ""
        if isinstance(val, datetime):
            return val.strftime("%Y-%m-%dT%H:%M")
        return val

    @app.template_filter("field_display")
    def field_display(obj, name):
        if obj is None:
            return "—"
        val = getattr(obj, name, None)
        if val is None or val == "":
            return "—"
        if isinstance(val, datetime):
            return val.strftime("%Y-%m-%d %H:%M")
        return val

    # ---- Error handlers ----
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # ---- Auto-bootstrap roles + admin (fix B3) ----
    with app.app_context():
        try:
            db.create_all()
            from app.models.core import Role, User
            if not Role.query.filter_by(name="Admin").first():
                for name in ["Admin", "Project Manager", "ML Engineer", "Reviewer"]:
                    db.session.add(Role(name=name, created_by=1))
                db.session.commit()
                admin_role = Role.query.filter_by(name="Admin").first()
                if not User.query.filter_by(username="admin").first():
                    admin = User(
                        username="admin",
                        email="admin@modeltrack.local",
                        full_name="System Administrator",
                        created_by=1,
                        is_active=True,
                    )
                    admin.set_password("Admin@123")
                    admin.roles.append(admin_role)
                    db.session.add(admin)
                    db.session.commit()
                    app.logger.info("Bootstrapped default admin (admin/Admin@123)")
        except Exception as exc:
            app.logger.warning(
                "Auto-bootstrap skipped: %s. "
                "Run `python seed.py` after fixing your database.", exc
            )

    return app