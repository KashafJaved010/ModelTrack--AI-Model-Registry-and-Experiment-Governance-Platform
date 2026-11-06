from app.extensions import db
from .base import AuditMixin


class DataSource(AuditMixin, db.Model):
    __tablename__ = "data_sources"
    name = db.Column(db.String(120), nullable=False)
    kind = db.Column(db.String(50))  # s3, database, manual, api
    uri = db.Column(db.String(500))


class DataSchema(AuditMixin, db.Model):
    __tablename__ = "data_schemas"
    name = db.Column(db.String(120), nullable=False)
    version = db.Column(db.String(30))
    description = db.Column(db.Text)


class Dataset(AuditMixin, db.Model):
    __tablename__ = "datasets"
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    source_id = db.Column(db.Integer, db.ForeignKey("data_sources.id"))
    schema_id = db.Column(db.Integer, db.ForeignKey("data_schemas.id"))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class DatasetVersion(AuditMixin, db.Model):
    __tablename__ = "dataset_versions"
    dataset_id = db.Column(db.Integer, db.ForeignKey("datasets.id"), nullable=False)
    version = db.Column(db.String(30), nullable=False)
    row_count = db.Column(db.Integer)
    size_bytes = db.Column(db.BigInteger)
    notes = db.Column(db.Text)


class Tag(AuditMixin, db.Model):
    __tablename__ = "tags"
    name = db.Column(db.String(60), unique=True, nullable=False)
    color = db.Column(db.String(20), default="#0d6efd")


class DatasetTag(AuditMixin, db.Model):
    __tablename__ = "dataset_tags"
    dataset_id = db.Column(db.Integer, db.ForeignKey("datasets.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)


class DataQualityCheck(AuditMixin, db.Model):
    __tablename__ = "data_quality_checks"
    dataset_version_id = db.Column(
        db.Integer, db.ForeignKey("dataset_versions.id"), nullable=False
    )
    check_name = db.Column(db.String(120), nullable=False)
    result = db.Column(db.String(20))  # pass/fail/warning
    details = db.Column(db.Text)