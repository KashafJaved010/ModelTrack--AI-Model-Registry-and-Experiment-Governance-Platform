-- Auto-generated MySQL DDL for ModelTrack
-- 40 tables

CREATE TABLE compute_clusters (
	name VARCHAR(120) NOT NULL, 
	provider VARCHAR(60), 
	region VARCHAR(60), 
	description TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE data_schemas (
	name VARCHAR(120) NOT NULL, 
	version VARCHAR(30), 
	description TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE data_sources (
	name VARCHAR(120) NOT NULL, 
	kind VARCHAR(50), 
	uri VARCHAR(500), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE environments (
	name VARCHAR(120) NOT NULL, 
	version VARCHAR(30), 
	python_version VARCHAR(20), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE job_queues (
	name VARCHAR(120) NOT NULL, 
	priority INTEGER, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE model_families (
	name VARCHAR(120) NOT NULL, 
	description TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id)
);

CREATE TABLE organizations (
	name VARCHAR(120) NOT NULL, 
	slug VARCHAR(60), 
	description TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (slug)
);

CREATE TABLE permissions (
	code VARCHAR(80) NOT NULL, 
	description VARCHAR(255), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (code)
);

CREATE TABLE roles (
	name VARCHAR(50) NOT NULL, 
	description VARCHAR(255), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);

CREATE TABLE tags (
	name VARCHAR(60) NOT NULL, 
	color VARCHAR(20), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);

CREATE TABLE users (
	username VARCHAR(60) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	full_name VARCHAR(120), 
	password_hash VARCHAR(255) NOT NULL, 
	is_active BOOL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);

CREATE TABLE approvals (
	target_type VARCHAR(60) NOT NULL, 
	target_id INTEGER NOT NULL, 
	requested_by INTEGER, 
	reviewer_id INTEGER, 
	decision VARCHAR(20), 
	comment TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(requested_by) REFERENCES users (id), 
	FOREIGN KEY(reviewer_id) REFERENCES users (id)
);

CREATE TABLE audit_logs (
	user_id INTEGER, 
	action VARCHAR(50) NOT NULL, 
	entity_type VARCHAR(60), 
	entity_id INTEGER, 
	details TEXT, 
	ip_address VARCHAR(45), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE compute_nodes (
	cluster_id INTEGER, 
	hostname VARCHAR(120) NOT NULL, 
	gpu_model VARCHAR(60), 
	cpu_cores INTEGER, 
	ram_gb INTEGER, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cluster_id) REFERENCES compute_clusters (id)
);

CREATE TABLE environment_packages (
	environment_id INTEGER, 
	package_name VARCHAR(120) NOT NULL, 
	package_version VARCHAR(30), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(environment_id) REFERENCES environments (id)
);

CREATE TABLE notifications (
	user_id INTEGER, 
	title VARCHAR(120) NOT NULL, 
	message TEXT, 
	is_read BOOL, 
	link VARCHAR(255), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE role_permissions (
	role_id INTEGER NOT NULL, 
	permission_id INTEGER NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(role_id) REFERENCES roles (id), 
	FOREIGN KEY(permission_id) REFERENCES permissions (id)
);

CREATE TABLE teams (
	organization_id INTEGER, 
	name VARCHAR(120) NOT NULL, 
	lead_user_id INTEGER, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(organization_id) REFERENCES organizations (id), 
	FOREIGN KEY(lead_user_id) REFERENCES users (id)
);

CREATE TABLE user_roles (
	user_id INTEGER NOT NULL, 
	role_id INTEGER NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
);

CREATE TABLE projects (
	organization_id INTEGER, 
	team_id INTEGER, 
	name VARCHAR(120) NOT NULL, 
	description TEXT, 
	owner_id INTEGER, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(organization_id) REFERENCES organizations (id), 
	FOREIGN KEY(team_id) REFERENCES teams (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);

CREATE TABLE team_members (
	team_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	role_in_team VARCHAR(50), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(team_id) REFERENCES teams (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE datasets (
	project_id INTEGER, 
	source_id INTEGER, 
	schema_id INTEGER, 
	name VARCHAR(120) NOT NULL, 
	description TEXT, 
	owner_id INTEGER, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(project_id) REFERENCES projects (id), 
	FOREIGN KEY(source_id) REFERENCES data_sources (id), 
	FOREIGN KEY(schema_id) REFERENCES data_schemas (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);

CREATE TABLE experiments (
	project_id INTEGER, 
	name VARCHAR(120) NOT NULL, 
	description TEXT, 
	created_by_user INTEGER, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(project_id) REFERENCES projects (id), 
	FOREIGN KEY(created_by_user) REFERENCES users (id)
);

CREATE TABLE ml_models (
	project_id INTEGER, 
	family_id INTEGER, 
	name VARCHAR(120) NOT NULL, 
	description TEXT, 
	owner_id INTEGER, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(project_id) REFERENCES projects (id), 
	FOREIGN KEY(family_id) REFERENCES model_families (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
);

CREATE TABLE project_members (
	project_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	project_role VARCHAR(50), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(project_id) REFERENCES projects (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE workspaces (
	project_id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	description TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(project_id) REFERENCES projects (id)
);

CREATE TABLE dataset_tags (
	dataset_id INTEGER NOT NULL, 
	tag_id INTEGER NOT NULL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(dataset_id) REFERENCES datasets (id), 
	FOREIGN KEY(tag_id) REFERENCES tags (id)
);

CREATE TABLE dataset_versions (
	dataset_id INTEGER NOT NULL, 
	version VARCHAR(30) NOT NULL, 
	row_count INTEGER, 
	size_bytes BIGINT, 
	notes TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(dataset_id) REFERENCES datasets (id)
);

CREATE TABLE data_quality_checks (
	dataset_version_id INTEGER NOT NULL, 
	check_name VARCHAR(120) NOT NULL, 
	result VARCHAR(20), 
	details TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(dataset_version_id) REFERENCES dataset_versions (id)
);

CREATE TABLE model_versions (
	model_id INTEGER NOT NULL, 
	version VARCHAR(30) NOT NULL, 
	dataset_version_id INTEGER, 
	trained_by INTEGER, 
	accuracy FLOAT, 
	f1_score FLOAT, 
	notes TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(model_id) REFERENCES ml_models (id), 
	FOREIGN KEY(dataset_version_id) REFERENCES dataset_versions (id), 
	FOREIGN KEY(trained_by) REFERENCES users (id)
);

CREATE TABLE experiment_runs (
	experiment_id INTEGER NOT NULL, 
	model_version_id INTEGER, 
	environment_id INTEGER, 
	run_number INTEGER, 
	started_at DATETIME, 
	finished_at DATETIME, 
	status_note VARCHAR(120), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(experiment_id) REFERENCES experiments (id), 
	FOREIGN KEY(model_version_id) REFERENCES model_versions (id), 
	FOREIGN KEY(environment_id) REFERENCES environments (id)
);

CREATE TABLE model_deployments (
	model_version_id INTEGER NOT NULL, 
	environment_id INTEGER, 
	deployed_by INTEGER, 
	endpoint VARCHAR(255), 
	deployed_at DATETIME, 
	notes TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(model_version_id) REFERENCES model_versions (id), 
	FOREIGN KEY(environment_id) REFERENCES environments (id), 
	FOREIGN KEY(deployed_by) REFERENCES users (id)
);

CREATE TABLE model_incidents (
	model_version_id INTEGER, 
	title VARCHAR(150) NOT NULL, 
	severity VARCHAR(20), 
	reported_by INTEGER, 
	resolved_at DATETIME, 
	description TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(model_version_id) REFERENCES model_versions (id), 
	FOREIGN KEY(reported_by) REFERENCES users (id)
);

CREATE TABLE model_reviews (
	model_version_id INTEGER NOT NULL, 
	reviewer_id INTEGER, 
	decision VARCHAR(20), 
	comment TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(model_version_id) REFERENCES model_versions (id), 
	FOREIGN KEY(reviewer_id) REFERENCES users (id)
);

CREATE TABLE monitoring_alerts (
	model_version_id INTEGER, 
	severity VARCHAR(20), 
	metric_name VARCHAR(80), 
	threshold FLOAT, 
	actual_value FLOAT, 
	message TEXT, 
	acknowledged BOOL, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(model_version_id) REFERENCES model_versions (id)
);

CREATE TABLE artifacts (
	run_id INTEGER, 
	model_version_id INTEGER, 
	name VARCHAR(120) NOT NULL, 
	kind VARCHAR(50), 
	uri VARCHAR(500), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(run_id) REFERENCES experiment_runs (id), 
	FOREIGN KEY(model_version_id) REFERENCES model_versions (id)
);

CREATE TABLE incident_updates (
	incident_id INTEGER NOT NULL, 
	author_id INTEGER, 
	note TEXT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(incident_id) REFERENCES model_incidents (id), 
	FOREIGN KEY(author_id) REFERENCES users (id)
);

CREATE TABLE jobs (
	queue_id INTEGER, 
	node_id INTEGER, 
	run_id INTEGER, 
	name VARCHAR(120) NOT NULL, 
	status_note VARCHAR(40), 
	started_at DATETIME, 
	finished_at DATETIME, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(queue_id) REFERENCES job_queues (id), 
	FOREIGN KEY(node_id) REFERENCES compute_nodes (id), 
	FOREIGN KEY(run_id) REFERENCES experiment_runs (id)
);

CREATE TABLE run_metrics (
	run_id INTEGER NOT NULL, 
	name VARCHAR(80) NOT NULL, 
	value FLOAT, 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(run_id) REFERENCES experiment_runs (id)
);

CREATE TABLE run_parameters (
	run_id INTEGER NOT NULL, 
	`key` VARCHAR(80) NOT NULL, 
	value VARCHAR(255), 
	id INTEGER NOT NULL AUTO_INCREMENT, 
	created_at DATETIME NOT NULL, 
	created_by INTEGER, 
	updated_at DATETIME, 
	updated_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	is_deleted BOOL NOT NULL, 
	deleted_at DATETIME, 
	deleted_by INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(run_id) REFERENCES experiment_runs (id)
);

