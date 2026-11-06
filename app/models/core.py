from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from .base import AuditMixin


class Role(AuditMixin, db.Model):
    __tablename__ = "roles"
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Role {self.name}>"


class Permission(AuditMixin, db.Model):
    __tablename__ = "permissions"
    code = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Permission {self.code}>"


class User(AuditMixin, db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    roles = db.relationship(
        "Role", secondary="user_roles", backref="users", lazy="joined"
    )

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def has_role(self, name):
        return any(r.name == name for r in self.roles)

    def has_any_role(self, names):
        return any(r.name in names for r in self.roles)

    def __repr__(self):
        return f"<User {self.username}>"


class UserRole(AuditMixin, db.Model):
    __tablename__ = "user_roles"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)


class RolePermission(AuditMixin, db.Model):
    __tablename__ = "role_permissions"
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey("permissions.id"), nullable=False)


class Notification(AuditMixin, db.Model):
    __tablename__ = "notifications"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(255))


class AuditLog(AuditMixin, db.Model):
    __tablename__ = "audit_logs"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    action = db.Column(db.String(50), nullable=False)
    entity_type = db.Column(db.String(60))
    entity_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))