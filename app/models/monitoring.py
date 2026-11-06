from app.extensions import db
from .base import AuditMixin


class MonitoringAlert(AuditMixin, db.Model):
    __tablename__ = "monitoring_alerts"
    model_version_id = db.Column(db.Integer, db.ForeignKey("model_versions.id"))
    severity = db.Column(db.String(20), default="info")  # info/warning/critical
    metric_name = db.Column(db.String(80))
    threshold = db.Column(db.Float)
    actual_value = db.Column(db.Float)
    message = db.Column(db.Text)
    acknowledged = db.Column(db.Boolean, default=False)


class ModelIncident(AuditMixin, db.Model):
    __tablename__ = "model_incidents"
    model_version_id = db.Column(db.Integer, db.ForeignKey("model_versions.id"))
    title = db.Column(db.String(150), nullable=False)
    severity = db.Column(db.String(20), default="medium")
    reported_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    resolved_at = db.Column(db.DateTime)
    description = db.Column(db.Text)


class IncidentUpdate(AuditMixin, db.Model):
    __tablename__ = "incident_updates"
    incident_id = db.Column(
        db.Integer, db.ForeignKey("model_incidents.id"), nullable=False
    )
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    note = db.Column(db.Text)