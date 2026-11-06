from flask import Blueprint, render_template, jsonify, g
from datetime import datetime, timedelta
from app.models.core import AuditLog
from app.models.data import Dataset
from app.models.ml import MLModel, ModelVersion, Experiment, ModelDeployment
from app.models.monitoring import MonitoringAlert, ModelIncident
from app.utils.auth import login_required, current_user

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    logs = (
        AuditLog.query.filter_by(is_deleted=False)
        .order_by(AuditLog.id.desc())
        .limit(10)
        .all()
    )
    alerts = (
        MonitoringAlert.query.filter_by(is_deleted=False)
        .order_by(MonitoringAlert.id.desc())
        .limit(5)
        .all()
    )
    return render_template("dashboard/index.html", logs=logs, alerts=alerts, user=g.user)


@bp.route("/api/stats")
def api_stats():
    # B2 fix: return JSON 401 instead of redirecting to login (which breaks fetch)
    if not current_user():
        return jsonify({"error": "unauthorized"}), 401
    cutoff = datetime.utcnow() - timedelta(days=7)
    return jsonify({
        "models": MLModel.query.filter_by(is_deleted=False).count(),
        "versions": ModelVersion.query.filter_by(is_deleted=False).count(),
        "experiments": Experiment.query.filter_by(is_deleted=False).count(),
        "deployments": ModelDeployment.query.filter_by(is_deleted=False).count(),
        "datasets": Dataset.query.filter_by(is_deleted=False).count(),
        "open_alerts": MonitoringAlert.query.filter_by(
            is_deleted=False, acknowledged=False
        ).count(),
        "open_incidents": ModelIncident.query.filter_by(
            is_deleted=False, resolved_at=None
        ).count(),
        "recent_deployments": ModelDeployment.query.filter_by(is_deleted=False)
            .filter(ModelDeployment.created_at >= cutoff).count(),
        "server_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    })