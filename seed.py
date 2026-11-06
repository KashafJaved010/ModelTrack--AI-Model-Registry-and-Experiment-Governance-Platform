"""Seed the database with roles, admin user, and demo data.

Run once after installing requirements:
    python seed.py
"""
from datetime import datetime

from app import create_app
from app.extensions import db
from app.models.core import User, Role, Permission
from app.models.organization import Organization, Team, Project
from app.models.data import DataSource, Dataset, DatasetVersion, Tag, DatasetTag
from app.models.ml import (
    ModelFamily, MLModel, ModelVersion, Experiment,
    ExperimentRun, RunMetric, ModelDeployment, ModelReview,
)
from app.models.compute import Environment, ComputeCluster
from app.models.monitoring import MonitoringAlert


app = create_app()


with app.app_context():
    db.create_all()

    # ---- Roles & permissions ----
    roles = {}
    for name in ["Admin", "Project Manager", "ML Engineer", "Reviewer"]:
        role = Role.query.filter_by(name=name).first()
        if not role:
            role = Role(name=name, created_by=1)
            db.session.add(role)
        roles[name] = role

    if not Permission.query.filter_by(code="manage_all").first():
        db.session.add(Permission(code="manage_all", description="Full control"))
    db.session.commit()

    # ---- Admin user ----
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@modeltrack.local",
            full_name="System Administrator",
            created_by=1,
            is_active=True,
        )
        admin.set_password("Admin@123")
        admin.roles.append(roles["Admin"])
        admin.roles.append(roles["Project Manager"])
        db.session.add(admin)
        db.session.commit()
        print("Created admin (admin / Admin@123)")

    # ---- Demo data ----
    if not Organization.query.first():
        org = Organization(name="Academix AI Lab", slug="academix", created_by=admin.id)
        db.session.add(org)
        db.session.commit()

        team = Team(organization_id=org.id, name="Vision Team",
                    lead_user_id=admin.id, created_by=admin.id)
        db.session.add(team)
        db.session.commit()

        project = Project(organization_id=org.id, team_id=team.id,
                          name="Traffic Sign Classifier",
                          owner_id=admin.id, created_by=admin.id)
        db.session.add(project)
        db.session.commit()

        src = DataSource(name="Public CV Repository", kind="api",
                         uri="https://example.com/data", created_by=admin.id)
        db.session.add(src)
        db.session.commit()

        ds = Dataset(project_id=project.id, source_id=src.id,
                     name="TrafficSigns-2024", owner_id=admin.id,
                     created_by=admin.id)
        db.session.add(ds)
        db.session.commit()

        dsv = DatasetVersion(dataset_id=ds.id, version="v1.0",
                             row_count=45000,
                             size_bytes=1024 * 1024 * 900,
                             created_by=admin.id)
        db.session.add(dsv)
        db.session.commit()

        tag = Tag(name="vision", color="#0d6efd", created_by=admin.id)
        db.session.add(tag)
        db.session.commit()
        db.session.add(DatasetTag(dataset_id=ds.id, tag_id=tag.id,
                                  created_by=admin.id))

        env = Environment(name="py311-torch", version="1.0",
                          python_version="3.11", created_by=admin.id)
        db.session.add(env)
        db.session.commit()

        cluster = ComputeCluster(name="gpu-cluster-1", provider="local",
                                 region="lab", created_by=admin.id)
        db.session.add(cluster)
        db.session.commit()

        fam = ModelFamily(name="CNN Family", created_by=admin.id)
        db.session.add(fam)
        db.session.commit()

        m = MLModel(project_id=project.id, family_id=fam.id,
                    name="CNN-Traffic", owner_id=admin.id,
                    created_by=admin.id)
        db.session.add(m)
        db.session.commit()

        mv = ModelVersion(model_id=m.id, version="v0.1",
                          dataset_version_id=dsv.id, trained_by=admin.id,
                          accuracy=0.93, f1_score=0.91, created_by=admin.id)
        db.session.add(mv)
        db.session.commit()

        exp = Experiment(project_id=project.id, name="Baseline CNN",
                         created_by_user=admin.id, created_by=admin.id)
        db.session.add(exp)
        db.session.commit()

        run = ExperimentRun(experiment_id=exp.id, model_version_id=mv.id,
                            environment_id=env.id,
                            started_at=datetime.utcnow(),
                            created_by=admin.id)
        db.session.add(run)
        db.session.commit()

        db.session.add_all([
            RunMetric(run_id=run.id, name="accuracy", value=0.93,
                      created_by=admin.id),
            RunMetric(run_id=run.id, name="f1", value=0.91,
                      created_by=admin.id),
            RunMetric(run_id=run.id, name="loss", value=0.21,
                      created_by=admin.id),
        ])

        dep = ModelDeployment(model_version_id=mv.id, environment_id=env.id,
                              deployed_by=admin.id,
                              endpoint="/predict/traffic",
                              deployed_at=datetime.utcnow(),
                              created_by=admin.id)
        db.session.add(dep)

        db.session.add(ModelReview(model_version_id=mv.id,
                                   reviewer_id=admin.id,
                                   decision="approved",
                                   comment="Looks good.",
                                   created_by=admin.id))
        db.session.add(MonitoringAlert(model_version_id=mv.id,
                                       severity="warning",
                                       metric_name="latency_p95",
                                       threshold=200, actual_value=280,
                                       message="Latency above threshold",
                                       created_by=admin.id))
        db.session.commit()
        print("Demo data seeded.")

    print(f"Models registered: {len(db.metadata.tables)}")
    print("Done. Run: python run.py")