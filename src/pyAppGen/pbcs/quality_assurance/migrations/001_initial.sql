CREATE SCHEMA IF NOT EXISTS quality_assurance;

CREATE TABLE quality_assurance_inspection_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  sampling_method VARCHAR(255) NOT NULL,
  sample_size VARCHAR(255) NOT NULL,
  revision VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_sampling_scheme (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  scheme_id VARCHAR(255) PRIMARY KEY NOT NULL,
  plan_id VARCHAR(255) PRIMARY KEY NOT NULL,
  acceptance_method VARCHAR(255) NOT NULL,
  sample_size VARCHAR(255) NOT NULL,
  aql VARCHAR(255) NOT NULL,
  rejection_number VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (plan_id) REFERENCES quality_assurance_inspection_plan(plan_id)
);

CREATE TABLE quality_assurance_lot_batch_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  lot_batch_id VARCHAR(255) PRIMARY KEY NOT NULL,
  lot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item VARCHAR(255) NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  manufactured_at TIMESTAMP NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_inspection_test_definition (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  test_id VARCHAR(255) PRIMARY KEY NOT NULL,
  plan_id VARCHAR(255) PRIMARY KEY NOT NULL,
  measurement_key VARCHAR(255) NOT NULL,
  lower_spec VARCHAR(255) NOT NULL,
  upper_spec VARCHAR(255) NOT NULL,
  criticality VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (plan_id) REFERENCES quality_assurance_inspection_plan(plan_id)
);

CREATE TABLE quality_assurance_inspection_result (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  result_id VARCHAR(255) PRIMARY KEY NOT NULL,
  plan_id VARCHAR(255) PRIMARY KEY NOT NULL,
  lot_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  inspector VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (plan_id) REFERENCES quality_assurance_inspection_plan(plan_id)
);

CREATE TABLE quality_assurance_inspection_measurement_series (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  series_id VARCHAR(255) PRIMARY KEY NOT NULL,
  result_id VARCHAR(255) PRIMARY KEY NOT NULL,
  measurement_key VARCHAR(255) NOT NULL,
  sample_count INTEGER NOT NULL,
  mean VARCHAR(255) NOT NULL,
  sigma VARCHAR(255) NOT NULL,
  cpk VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (result_id) REFERENCES quality_assurance_inspection_result(result_id)
);

CREATE TABLE quality_assurance_quality_hold (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  hold_id VARCHAR(255) PRIMARY KEY NOT NULL,
  lot_id VARCHAR(255) PRIMARY KEY NOT NULL,
  item VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_non_conformance (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  nonconformance_id VARCHAR(255) PRIMARY KEY NOT NULL,
  result_id VARCHAR(255) PRIMARY KEY NOT NULL,
  defect_class VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  root_cause VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (result_id) REFERENCES quality_assurance_inspection_result(result_id)
);

CREATE TABLE quality_assurance_quality_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rule_type VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  enabled VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_quality_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) PRIMARY KEY NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  changed_by VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_quality_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  event_contract VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_timezone VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_quality_capa (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  capa_id VARCHAR(255) PRIMARY KEY NOT NULL,
  nonconformance_id VARCHAR(255) PRIMARY KEY NOT NULL,
  owner VARCHAR(255) NOT NULL,
  due_at TIMESTAMP NOT NULL,
  effectiveness_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (nonconformance_id) REFERENCES quality_assurance_non_conformance(nonconformance_id)
);

CREATE TABLE quality_assurance_quality_release (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  release_id VARCHAR(255) PRIMARY KEY NOT NULL,
  hold_id VARCHAR(255) PRIMARY KEY NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  disposition VARCHAR(255) NOT NULL,
  released_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (hold_id) REFERENCES quality_assurance_quality_hold(hold_id)
);

CREATE TABLE quality_assurance_calibration_asset (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_code VARCHAR(255) NOT NULL,
  asset_type VARCHAR(255) NOT NULL,
  site VARCHAR(255) NOT NULL,
  last_calibrated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_calibration_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  procedure_id VARCHAR(255) NOT NULL,
  due_at TIMESTAMP NOT NULL,
  window_days VARCHAR(255) NOT NULL,
  completion_status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES quality_assurance_calibration_asset(asset_id),
  FOREIGN KEY (procedure_id) REFERENCES quality_assurance_procedure_revision(procedure_id)
);

CREATE TABLE quality_assurance_procedure_revision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  procedure_id VARCHAR(255) PRIMARY KEY NOT NULL,
  revision_id VARCHAR(255) PRIMARY KEY NOT NULL,
  title VARCHAR(255) NOT NULL,
  revision VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  owner VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_supplier_quality_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  supplier_quality_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_score DECIMAL(18, 4) NOT NULL,
  ppm VARCHAR(255) NOT NULL,
  audit_status VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_supplier_quality_incident (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  incident_id VARCHAR(255) PRIMARY KEY NOT NULL,
  supplier_quality_id VARCHAR(255) PRIMARY KEY NOT NULL,
  lot_id VARCHAR(255) NOT NULL,
  defect_class VARCHAR(255) NOT NULL,
  containment_action VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (supplier_quality_id) REFERENCES quality_assurance_supplier_quality_profile(supplier_quality_id)
);

CREATE TABLE quality_assurance_customer_quality_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  customer_case_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  result_id VARCHAR(255) NOT NULL,
  complaint_code VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (result_id) REFERENCES quality_assurance_inspection_result(result_id)
);

CREATE TABLE quality_assurance_audit_evidence_packet (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  evidence_id TEXT PRIMARY KEY NOT NULL,
  reference_id VARCHAR(255) PRIMARY KEY NOT NULL,
  reference_type VARCHAR(255) NOT NULL,
  disclosure_level VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (reference_id) REFERENCES quality_assurance_quality_compliance_package(package_id)
);

CREATE TABLE quality_assurance_quality_compliance_package (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  package_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scope VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  approval_status VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_quality_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  seed_id VARCHAR(255) PRIMARY KEY NOT NULL,
  seed_type VARCHAR(255) NOT NULL,
  seed_key VARCHAR(255) NOT NULL,
  seed_value VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_quality_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  auc VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  regulated VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_quality_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) PRIMARY KEY NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  asserted_at TIMESTAMP NOT NULL,
  assertion_status VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE quality_assurance_quality_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) PRIMARY KEY NOT NULL,
  table_name VARCHAR(255) PRIMARY KEY NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  revision VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
