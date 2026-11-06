from app.extensions import db
from .base import AuditMixin


class ComputeCluster(AuditMixin, db.Model):
    __tablename__ = "compute_clusters"
    name = db.Column(db.String(120), nullable=False)
    provider = db.Column(db.String(60))  # aws, gcp, local
    region = db.Column(db.String(60))
    description = db.Column(db.Text)


class ComputeNode(AuditMixin, db.Model):
    __tablename__ = "compute_nodes"
    cluster_id = db.Column(db.Integer, db.ForeignKey("compute_clusters.id"))
    hostname = db.Column(db.String(120), nullable=False)
    gpu_model = db.Column(db.String(60))
    cpu_cores = db.Column(db.Integer)
    ram_gb = db.Column(db.Integer)


class Environment(AuditMixin, db.Model):
    __tablename__ = "environments"
    name = db.Column(db.String(120), nullable=False)
    version = db.Column(db.String(30))
    python_version = db.Column(db.String(20))


class EnvironmentPackage(AuditMixin, db.Model):
    __tablename__ = "environment_packages"
    environment_id = db.Column(db.Integer, db.ForeignKey("environments.id"))
    package_name = db.Column(db.String(120), nullable=False)
    package_version = db.Column(db.String(30))


class JobQueue(AuditMixin, db.Model):
    __tablename__ = "job_queues"
    name = db.Column(db.String(120), nullable=False)
    priority = db.Column(db.Integer, default=1)


class Job(AuditMixin, db.Model):
    __tablename__ = "jobs"
    queue_id = db.Column(db.Integer, db.ForeignKey("job_queues.id"))
    node_id = db.Column(db.Integer, db.ForeignKey("compute_nodes.id"))
    run_id = db.Column(db.Integer, db.ForeignKey("experiment_runs.id"))
    name = db.Column(db.String(120), nullable=False)
    status_note = db.Column(db.String(40))
    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime)