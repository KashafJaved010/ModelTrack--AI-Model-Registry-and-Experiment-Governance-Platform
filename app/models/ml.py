from app.extensions import db
from .base import AuditMixin


class ModelFamily(AuditMixin, db.Model):
    __tablename__ = "model_families"
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)


class MLModel(AuditMixin, db.Model):
    __tablename__ = "ml_models"
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    family_id = db.Column(db.Integer, db.ForeignKey("model_families.id"))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class ModelVersion(AuditMixin, db.Model):
    __tablename__ = "model_versions"
    model_id = db.Column(db.Integer, db.ForeignKey("ml_models.id"), nullable=False)
    version = db.Column(db.String(30), nullable=False)
    dataset_version_id = db.Column(db.Integer, db.ForeignKey("dataset_versions.id"))
    trained_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    accuracy = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    notes = db.Column(db.Text)


class Experiment(AuditMixin, db.Model):
    __tablename__ = "experiments"
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created_by_user = db.Column(db.Integer, db.ForeignKey("users.id"))


class ExperimentRun(AuditMixin, db.Model):
    __tablename__ = "experiment_runs"
    experiment_id = db.Column(
        db.Integer, db.ForeignKey("experiments.id"), nullable=False
    )
    model_version_id = db.Column(db.Integer, db.ForeignKey("model_versions.id"))
    environment_id = db.Column(db.Integer, db.ForeignKey("environments.id"))
    run_number = db.Column(db.Integer, default=1)
    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)
    status_note = db.Column(db.String(120))


class RunParameter(AuditMixin, db.Model):
    __tablename__ = "run_parameters"
    run_id = db.Column(
        db.Integer, db.ForeignKey("experiment_runs.id"), nullable=False
    )
    key = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(255))


class RunMetric(AuditMixin, db.Model):
    __tablename__ = "run_metrics"
    run_id = db.Column(
        db.Integer, db.ForeignKey("experiment_runs.id"), nullable=False
    )
    name = db.Column(db.String(80), nullable=False)
    value = db.Column(db.Float)


class Artifact(AuditMixin, db.Model):
    __tablename__ = "artifacts"
    run_id = db.Column(db.Integer, db.ForeignKey("experiment_runs.id"))
    model_version_id = db.Column(db.Integer, db.ForeignKey("model_versions.id"))
    name = db.Column(db.String(120), nullable=False)
    kind = db.Column(db.String(50))  # weights, plot, log, report
    uri = db.Column(db.String(500))


class ModelReview(AuditMixin, db.Model):
    __tablename__ = "model_reviews"
    model_version_id = db.Column(
        db.Integer, db.ForeignKey("model_versions.id"), nullable=False
    )
    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    decision = db.Column(db.String(20), default="pending")
    comment = db.Column(db.Text)


class ModelDeployment(AuditMixin, db.Model):
    __tablename__ = "model_deployments"
    model_version_id = db.Column(
        db.Integer, db.ForeignKey("model_versions.id"), nullable=False
    )
    environment_id = db.Column(db.Integer, db.ForeignKey("environments.id"))
    deployed_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    endpoint = db.Column(db.String(255))
    deployed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)