from app.extensions import db
from .base import AuditMixin


class Organization(AuditMixin, db.Model):
    __tablename__ = "organizations"
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)


class Team(AuditMixin, db.Model):
    __tablename__ = "teams"
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    name = db.Column(db.String(120), nullable=False)
    lead_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class TeamMember(AuditMixin, db.Model):
    __tablename__ = "team_members"
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role_in_team = db.Column(db.String(50))


class Project(AuditMixin, db.Model):
    __tablename__ = "projects"
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class ProjectMember(AuditMixin, db.Model):
    __tablename__ = "project_members"
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_role = db.Column(db.String(50))


class Workspace(AuditMixin, db.Model):
    __tablename__ = "workspaces"
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)


class Approval(AuditMixin, db.Model):
    __tablename__ = "approvals"
    target_type = db.Column(db.String(60), nullable=False)  # e.g. "ModelVersion"
    target_id = db.Column(db.Integer, nullable=False)
    requested_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    reviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    decision = db.Column(db.String(20), default="pending")  # pending/approved/rejected
    comment = db.Column(db.Text)