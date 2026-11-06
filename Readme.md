# ModelTrack — AI Model Registry & Experiment Governance Platform

A Flask + SQLAlchemy + MySQL web application that manages AI/ML projects,
datasets, model versions, experiments, deployments, approvals, and incidents.

## Stack
- Python 3.10+, Flask 3, Flask-SQLAlchemy
- MySQL (or SQLite for quick testing)
- Bootstrap 5, vanilla JavaScript

## Setup

1. Create a virtual environment:
   python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows


2. Install dependencies:
   pip install -r requirements.txt
   
3. Create the MySQL database:
CREATE DATABASE modeltrack CHARACTER SET utf8mb4;

4. Copy `.env.example` to `.env` and update `DATABASE_URL`.

5. Initialize database + seed data:
python seed.py

6. Run the app:
pyhton run.py


7. Open http://127.0.0.1:5000

## Default Login
- Username: `admin`
- Password: `Admin@123`

## Modules
- **Core**: users, roles, permissions, notifications, audit logs (7)
- **Organization**: organizations, teams, projects, workspaces, approvals (7)
- **Data**: data sources, schemas, datasets, versions, tags, quality checks (7)
- **ML**: model families, models, versions, experiments, runs, metrics, artifacts, reviews, deployments (10)
- **Compute**: clusters, nodes, environments, packages, queues, jobs (6)
- **Monitoring**: alerts, incidents, incident updates (3)

Total: **40 tables**, each with id, created_at, created_by, updated_at,
updated_by, status, is_deleted, deleted_at, deleted_by.

## Key Flask Concepts Demonstrated
- Application factory (`create_app`)
- Blueprints (auth, dashboard, crud, admin)
- Session-based authentication with hashed passwords
- Server-side validation, flash messages, PRG pattern
- SQLAlchemy relationships, FKs, junction tables
- Soft delete across all models
- Search with `.ilike()`, pagination, status filters
- `fetch()` live dashboard widget (`/api/stats`)
- Transactions with `commit()` / `rollback()` and audit logging