from datetime import datetime
from app.extensions import db


class AuditMixin:
    """Every model inherits: id, audit fields, status, and soft-delete."""

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )
    updated_by = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default="active", nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    deleted_by = db.Column(db.Integer, nullable=True)

    def soft_delete(self, user_id=None):
        self.is_deleted = True
        self.status = "deleted"
        self.deleted_at = datetime.utcnow()
        self.deleted_by = user_id

    def to_dict(self):
        d = {}
        for col in self.__table__.columns:
            v = getattr(self, col.name)
            if isinstance(v, datetime):
                v = v.isoformat()
            d[col.name] = v
        return d