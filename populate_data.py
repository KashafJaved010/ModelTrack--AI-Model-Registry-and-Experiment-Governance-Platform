"""Yeh script database mein fake (demo) AI data dalne ke liye hai."""
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models.core import User, Role
from app.models.organization import Organization, Team, Project
from app.models.data import DataSource, Dataset, DatasetVersion
from app.models.ml import ModelFamily, MLModel, ModelVersion, Experiment, ExperimentRun, RunMetric, ModelDeployment
from app.models.monitoring import MonitoringAlert

app = create_app()

with app.app_context():
    print("Adding demo data...")
    
    # 1. Get Admin
    admin = User.query.filter_by(username="admin").first()
    eng_role = Role.query.filter_by(name="ML Engineer").first()

    # 2. Add 2 New Users
    if not User.query.filter_by(username="sara_ml").first():
        sara = User(username="sara_ml", email="sara@modeltrack.com", full_name="Sara Khan", created_by=admin.id)
        sara.set_password("Pass@123")
        sara.roles.append(eng_role)
        
        ali = User(username="ali_eng", email="ali@modeltrack.com", full_name="Ali Raza", created_by=admin.id)
        ali.set_password("Pass@123")
        ali.roles.append(eng_role)
        db.session.add_all([sara, ali])
        db.session.commit()

    # 3. Projects
    org = Organization.query.first()
    team = Team.query.first()
    
    p1 = Project(organization_id=org.id, team_id=team.id, name="Fraud Detection System", owner_id=admin.id, created_by=admin.id)
    p2 = Project(organization_id=org.id, team_id=team.id, name="Chatbot Assistant", owner_id=admin.id, created_by=admin.id)
    db.session.add_all([p1, p2])
    db.session.commit()

    # 4. Datasets
    d1 = Dataset(project_id=p1.id, name="Credit Card Transactions", owner_id=admin.id, created_by=admin.id)
    d2 = Dataset(project_id=p2.id, name="Customer Support Chats", owner_id=admin.id, created_by=admin.id)
    db.session.add_all([d1, d2])
    db.session.commit()

    dv1 = DatasetVersion(dataset_id=d1.id, version="v2.0", row_count=150000, created_by=admin.id)
    dv2 = DatasetVersion(dataset_id=d2.id, version="v1.5", row_count=50000, created_by=admin.id)
    db.session.add_all([dv1, dv2])
    db.session.commit()

    # 5. Models
    fam1 = ModelFamily(name="Random Forest", created_by=admin.id)
    fam2 = ModelFamily(name="Transformer", created_by=admin.id)
    db.session.add_all([fam1, fam2])
    db.session.commit()

    m1 = MLModel(project_id=p1.id, family_id=fam1.id, name="Fraud-RF-v1", owner_id=admin.id, created_by=admin.id)
    m2 = MLModel(project_id=p2.id, family_id=fam2.id, name="Support-BERT", owner_id=admin.id, created_by=admin.id)
    db.session.add_all([m1, m2])
    db.session.commit()

    # 6. Model Versions
    mv1 = ModelVersion(model_id=m1.id, version="v1.0", dataset_version_id=dv1.id, accuracy=0.96, f1_score=0.94, created_by=admin.id)
    mv2 = ModelVersion(model_id=m2.id, version="v1.0", dataset_version_id=dv2.id, accuracy=0.88, f1_score=0.85, created_by=admin.id)
    db.session.add_all([mv1, mv2])
    db.session.commit()

    # 7. Experiments & Runs
    exp1 = Experiment(project_id=p1.id, name="Tuning Hyperparameters", created_by_user=admin.id, created_by=admin.id)
    db.session.add(exp1)
    db.session.commit()

    run1 = ExperimentRun(experiment_id=exp1.id, model_version_id=mv1.id, started_at=datetime.utcnow(), created_by=admin.id)
    db.session.add(run1)
    db.session.commit()

    db.session.add_all([
        RunMetric(run_id=run1.id, name="Accuracy", value=0.96, created_by=admin.id),
        RunMetric(run_id=run1.id, name="Loss", value=0.12, created_by=admin.id)
    ])

    # 8. Alerts
    alert1 = MonitoringAlert(model_version_id=mv1.id, severity="critical", metric_name="False Positives", threshold=5.0, actual_value=8.5, message="Fraud model flagging too many valid transactions.", created_by=admin.id)
    db.session.add(alert1)

    db.session.commit()
    print("Success! Rich demo data added to the database.")