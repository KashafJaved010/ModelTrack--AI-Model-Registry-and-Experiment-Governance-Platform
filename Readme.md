# ModelTrack: AI Model Registry & Experiment Governance Platform

> **"A centralized, enterprise-grade web application to track, manage, and monitor the complete lifecycle of Artificial Intelligence and Machine Learning models."**

## 1. Project Overview
In the modern AI landscape, companies manage thousands of models and datasets. **ModelTrack** is a comprehensive system designed to eliminate the "chaos" in AI teams. It provides a single, unified platform where ML Engineers, Data Scientists, and Project Managers can manage data, track model versions, log experiments, and monitor live deployments. 

Built with a robust **Flask + SQLAlchemy** backend and a modern **Bootstrap/JavaScript** frontend, it ensures complete reproducibility and governance.

---

## 2. Real-World Problem & Solution

| The Problem | The ModelTrack Solution |
| :--- | :--- |
| **Data Loss:** Tracking which dataset was used to train a specific model is difficult. | **Dataset Versioning:** Every dataset has distinct versions (v1.0, v2.0) linked to specific model runs. |
| **No Accountability:** It is unclear who approved a model for live deployment. | **Audit Logs:** Every action (Create, Update, Delete) is recorded with the User ID and timestamp. |
| **Accidental Data Loss:** Deleting a record breaks historical data and foreign keys. | **Soft Delete Architecture:** Records are never physically deleted from the database; they are flagged as `is_deleted`. |
| **Blind Deployments:** No way to know if a live model is failing. | **Real-Time Monitoring:** The system generates alerts (e.g., High Latency) for deployed models. |

---

## 3. Key Features

*   **Role-Based Access Control (RBAC):** Strict permissions across 4 distinct roles.
*   **Soft Delete Architecture:** Protects data integrity by hiding deleted records instead of removing them.
*   **Dynamic AJAX Dashboard:** Real-time statistics update every 10 seconds without reloading the page.
*   **Full CRUD Operations:** Intuitive Create, Read, Update, and Delete interfaces for all 40 tables.
*   **Advanced Search & Pagination:** Case-insensitive searching using `.ilike()` and seamless pagination.
*   **Transaction Safety:** Uses SQLAlchemy `commit()` and `rollback()` to prevent database corruption on errors.

---

## 4. Database Architecture (Exactly 40 Tables)

To meet academic requirements, the database contains **exactly 40 tables**, logically divided into 6 modules. Every table inherits an `AuditMixin` containing: `id`, `created_at`, `created_by`, `updated_at`, `updated_by`, `status`, `is_deleted`, `deleted_at`, and `deleted_by`.

| Module | Table Count | Purpose |
| :--- | :---: | :--- |
| **1. Core Security** | 7 | Users, Roles, Permissions, Audit Logs, Notifications. |
| **2. Organization** | 7 | Organizations, Teams, Projects, Workspaces, Approvals. |
| **3. Data Assets** | 7 | Data Sources, Datasets, Dataset Versions, Tags, Quality Checks. |
| **4. Machine Learning** | 10 | Model Families, Models, Versions, Experiments, Runs, Metrics, Artifacts, Deployments. |
| **5. Compute** | 6 | Clusters, Nodes, Environments, Packages, Job Queues. |
| **6. Monitoring** | 3 | Monitoring Alerts, Incidents, Incident Updates. |
| **Total** | **40** | **Fully connected via One-to-Many & Many-to-Many (Junction) relationships.** |

---

##  5. Technology Stack & Syllabus Coverage

This project was built to strictly fulfill the university's web engineering syllabus requirements:

*   **Backend:** Python 3, Flask (Application Factory Pattern, Blueprints).
*   **Database:** MySQL, Flask-SQLAlchemy (ORM, Foreign Keys, Relationships).
*   **Frontend:** HTML5, CSS3 (Custom Premium UI), Bootstrap 5.
*   **JavaScript:** Vanilla JS, Fetch API (Live Dashboard Widgets), DOM Manipulation.
*   **Security:** Werkzeug Password Hashing, Session Management, Flash Messages.

### 🎓 Key Academic Requirements Covered:
-  Primary Keys, Foreign Keys, and Junction Tables.
-  Audit Fields (Created/Updated/Deleted tracking).
-  Soft Delete functionality across all models.
-  `create_app()` factory and Flask Blueprints.
-  Server-Side Validation & Post/Redirect/Get (PRG) pattern.
-  Transaction Rollback testing.
-  Dynamic search using `.ilike()` and server-side pagination.

---

##  6. User Roles & Permissions

The system implements strict authorization based on the following roles:

1.  **Admin:** Full system access, including User Management and Role assignment.
2.  **Project Manager:** Can create projects, manage teams, and approve models.
3.  **ML Engineer:** Can register datasets, train models, and log experiments.
4.  **Reviewer:** Can review model versions and approve/reject deployments.

---

##  7. Local Setup Guide

To run this project locally on your machine:

1. **Clone the Repository:**
   git clone <repository-url>
   cd modeltrack
   
2. **Set Up Virtual Environment:**
   
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   
3. **Install Dependencies:**
   
   pip install -r requirements.txt
   
4. **Configure Database (`.env`):**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/modeltrack
   SECRET_KEY=your-secret-key
   ```
5. **Initialize Database & Seed Demo Data:**
   
   python verify.py    # Verifies 40 tables & relationships
   python seed.py      # Creates tables, admin account, and demo data
   
6. **Run the Application:**
   
   python run.py
   
   Open **`http://127.0.0.1:5000`** in your browser.

---

## 8. Demo Credentials

Use the following credentials to explore the system:

*   **Username:** `admin`
*   **Password:** `Admin@123`

---

### *"ModelTrack ensures that AI models don't just get built, but are governed, tracked, and deployed responsibly."*