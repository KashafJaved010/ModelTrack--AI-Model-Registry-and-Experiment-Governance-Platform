from app.extensions import db
from .core import User, Role, Permission, UserRole, RolePermission, Notification, AuditLog
from .organization import Organization, Team, TeamMember, Project, ProjectMember, Workspace, Approval
from .data import DataSource, DataSchema, Dataset, DatasetVersion, Tag, DatasetTag, DataQualityCheck
from .ml import ModelFamily, MLModel, ModelVersion, Experiment, ExperimentRun, RunParameter, RunMetric, Artifact, ModelReview, ModelDeployment
from .compute import ComputeCluster, ComputeNode, Environment, EnvironmentPackage, JobQueue, Job
from .monitoring import MonitoringAlert, ModelIncident, IncidentUpdate

HIDDEN_FIELDS = {
    "id", "created_at", "created_by", "updated_at", "updated_by",
    "status", "is_deleted", "deleted_at", "deleted_by",
    "password_hash",
}

def _fields(model):
    out = []
    for col in model.__table__.columns:
        if col.name in HIDDEN_FIELDS:
            continue
        fk = None
        if col.foreign_keys:
            fk = list(col.foreign_keys)[0].target_fullname  # e.g. "users.id"
        out.append({
            "name": col.name,
            "type": type(col.type).__name__,
            "required": not col.nullable,
            "fk": fk,
        })
    return out

def _list_fields(model):
    cols = []
    for col in model.__table__.columns:
        if col.name in ("id", "is_deleted", "deleted_at", "deleted_by",
                        "created_at", "created_by", "updated_at", "updated_by",
                        "password_hash"):
            continue
        cols.append(col.name)
        if len(cols) >= 5:
            break
    return cols

MODELS = [
    # module, label, class
    ("Core", "User", User),
    ("Core", "Role", Role),
    ("Core", "Permission", Permission),
    ("Core", "User Role", UserRole),
    ("Core", "Role Permission", RolePermission),
    ("Core", "Notification", Notification),
    ("Core", "Audit Log", AuditLog),
    ("Organization", "Organization", Organization),
    ("Organization", "Team", Team),
    ("Organization", "Team Member", TeamMember),
    ("Organization", "Project", Project),
    ("Organization", "Project Member", ProjectMember),
    ("Organization", "Workspace", Workspace),
    ("Organization", "Approval", Approval),
    ("Data", "Data Source", DataSource),
    ("Data", "Data Schema", DataSchema),
    ("Data", "Dataset", Dataset),
    ("Data", "Dataset Version", DatasetVersion),
    ("Data", "Tag", Tag),
    ("Data", "Dataset Tag", DatasetTag),
    ("Data", "Data Quality Check", DataQualityCheck),
    ("ML", "Model Family", ModelFamily),
    ("ML", "ML Model", MLModel),
    ("ML", "Model Version", ModelVersion),
    ("ML", "Experiment", Experiment),
    ("ML", "Experiment Run", ExperimentRun),
    ("ML", "Run Parameter", RunParameter),
    ("ML", "Run Metric", RunMetric),
    ("ML", "Artifact", Artifact),
    ("ML", "Model Review", ModelReview),
    ("ML", "Model Deployment", ModelDeployment),
    ("Compute", "Compute Cluster", ComputeCluster),
    ("Compute", "Compute Node", ComputeNode),
    ("Compute", "Environment", Environment),
    ("Compute", "Environment Package", EnvironmentPackage),
    ("Compute", "Job Queue", JobQueue),
    ("Compute", "Job", Job),
    ("Monitoring", "Monitoring Alert", MonitoringAlert),
    ("Monitoring", "Model Incident", ModelIncident),
    ("Monitoring", "Incident Update", IncidentUpdate),
]

MODEL_REGISTRY = {}
for module, label, cls in MODELS:
    slug = cls.__name__.lower()
    # use table name as key for clarity
    MODEL_REGISTRY[cls.__tablename__] = {
        "model": cls,
        "module": module,
        "label": label,
        "slug": cls.__tablename__,
        "fields": _fields(cls),
        "list_fields": _list_fields(cls),
    }

def get_model_meta(name):
    return MODEL_REGISTRY.get(name)

assert len(MODEL_REGISTRY) == 40, f"Expected 40 models, found {len(MODEL_REGISTRY)}"