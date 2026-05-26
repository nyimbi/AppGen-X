CREATE SCHEMA IF NOT EXISTS personnel_identity;

CREATE TABLE personnel_identity_personnel_department (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE personnel_identity_personnel_department_hierarchy (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_position (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_job (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_employee (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_employee_contact (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_employee_document (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_employment_lifecycle (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_employment_status_history (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_manager_relationship (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_org_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_work_location (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_cost_center_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_role_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_role_catalog (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_role_review (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_role_separation_check (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_identity_attribute (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_identity_assurance (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_identity_verification (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_identity_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_access_policy_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_access_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_provisioning_event (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_provisioning_replay (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_directory_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_org_chart_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_privacy_consent (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_residency_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_retention_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_carbon_processing_window (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_role_access_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_manager_capacity_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_identity_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_workforce_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_workforce_risk_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_parsed_event (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_identity_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_identity_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_personnel_identity_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  personnel_department_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (personnel_department_id) REFERENCES personnel_identity_personnel_department(id)
);

CREATE TABLE personnel_identity_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE personnel_identity_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE personnel_identity_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);
