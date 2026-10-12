CREATE SCHEMA IF NOT EXISTS agri_supply_chain_traceability;

CREATE TABLE agri_supply_chain_traceability_farm_lot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  farm_lot_id VARCHAR(255) NOT NULL,
  grower_id VARCHAR(255) NOT NULL,
  site_name VARCHAR(255) NOT NULL,
  field_block VARCHAR(255) NOT NULL,
  crop VARCHAR(255) NOT NULL,
  season VARCHAR(255) NOT NULL,
  planting_window_start TIMESTAMP NOT NULL,
  planting_window_end TIMESTAMP NOT NULL,
  ownership_type VARCHAR(255) NOT NULL,
  irrigation_zone VARCHAR(255) NOT NULL,
  area_hectares DECIMAL(18, 4) NOT NULL,
  organic_flag BOOLEAN NOT NULL,
  sustainability_claim VARCHAR(255) NOT NULL,
  claim_basis VARCHAR(255) NOT NULL,
  lifecycle_state VARCHAR(255) NOT NULL,
  retired_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_input_batch (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  input_batch_id VARCHAR(255) NOT NULL,
  farm_lot_id VARCHAR(255) NOT NULL,
  supplier_id VARCHAR(255) NOT NULL,
  input_type VARCHAR(255) NOT NULL,
  product_name VARCHAR(255) NOT NULL,
  formulation VARCHAR(255) NOT NULL,
  active_ingredients TEXT NOT NULL,
  application_method VARCHAR(255) NOT NULL,
  operator_id VARCHAR(255) NOT NULL,
  dose_amount DECIMAL(18, 4) NOT NULL,
  dose_unit VARCHAR(255) NOT NULL,
  applied_at TIMESTAMP NOT NULL,
  pre_harvest_interval_days INTEGER NOT NULL,
  withholding_period_days INTEGER NOT NULL,
  harvest_after TIMESTAMP,
  withholding_breach BOOLEAN NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (farm_lot_id) REFERENCES agri_supply_chain_traceability_farm_lot(farm_lot_id)
);

CREATE TABLE agri_supply_chain_traceability_certification (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  certification_id VARCHAR(255) NOT NULL,
  certificate_type VARCHAR(255) NOT NULL,
  issuing_body VARCHAR(255) NOT NULL,
  holder_id VARCHAR(255) NOT NULL,
  covered_sites TEXT NOT NULL,
  covered_commodities TEXT NOT NULL,
  valid_from TIMESTAMP NOT NULL,
  valid_to TIMESTAMP,
  suspension_state VARCHAR(255) NOT NULL,
  superseded_by VARCHAR(255) NOT NULL,
  scope_state VARCHAR(255) NOT NULL,
  evidence_document VARCHAR(255) NOT NULL,
  verified_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_storage_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  storage_event_id VARCHAR(255) NOT NULL,
  farm_lot_id VARCHAR(255) NOT NULL,
  storage_zone VARCHAR(255) NOT NULL,
  container_id VARCHAR(255) NOT NULL,
  entry_at TIMESTAMP NOT NULL,
  exit_at TIMESTAMP,
  target_temperature_min DECIMAL(18, 4) NOT NULL,
  target_temperature_max DECIMAL(18, 4) NOT NULL,
  observed_temperature DECIMAL(18, 4) NOT NULL,
  observed_humidity DECIMAL(18, 4) NOT NULL,
  reading_source VARCHAR(255) NOT NULL,
  treatment_event VARCHAR(255) NOT NULL,
  exception_reason_code VARCHAR(255) NOT NULL,
  breach_duration_minutes INTEGER NOT NULL,
  quarantine_state VARCHAR(255) NOT NULL,
  disposition VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (farm_lot_id) REFERENCES agri_supply_chain_traceability_farm_lot(farm_lot_id)
);

CREATE TABLE agri_supply_chain_traceability_transport_leg (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  transport_leg_id VARCHAR(255) NOT NULL,
  shipment_id VARCHAR(255) NOT NULL,
  origin_site VARCHAR(255) NOT NULL,
  destination_site VARCHAR(255) NOT NULL,
  vehicle_identity VARCHAR(255) NOT NULL,
  driver_id VARCHAR(255) NOT NULL,
  seal_number VARCHAR(255) NOT NULL,
  seal_intact BOOLEAN NOT NULL,
  sanitation_check_state VARCHAR(255) NOT NULL,
  prior_load_category VARCHAR(255) NOT NULL,
  load_compatibility VARCHAR(255) NOT NULL,
  route_plan TEXT NOT NULL,
  dispatched_at TIMESTAMP NOT NULL,
  delivered_at TIMESTAMP,
  handoff_condition_notes TEXT NOT NULL,
  delivery_acceptance_state VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_recall_link (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  recall_link_id VARCHAR(255) NOT NULL,
  recall_id VARCHAR(255) NOT NULL,
  hazard_code VARCHAR(255) NOT NULL,
  source_reference VARCHAR(255) NOT NULL,
  affected_lot_id VARCHAR(255) NOT NULL,
  trace_direction VARCHAR(255) NOT NULL,
  contribution_percentage DECIMAL(18, 4) NOT NULL,
  affected_customer_count INTEGER NOT NULL,
  affected_location_count INTEGER NOT NULL,
  recalled_quantity DECIMAL(18, 4) NOT NULL,
  quantity_unit VARCHAR(255) NOT NULL,
  recall_scope_state VARCHAR(255) NOT NULL,
  opened_at TIMESTAMP NOT NULL,
  narrowed_at TIMESTAMP,
  closed_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (affected_lot_id) REFERENCES agri_supply_chain_traceability_farm_lot(farm_lot_id)
);

CREATE TABLE agri_supply_chain_traceability_provenance_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  provenance_proof_id VARCHAR(255) NOT NULL,
  farm_lot_id VARCHAR(255) NOT NULL,
  bundle_type VARCHAR(255) NOT NULL,
  geography VARCHAR(255) NOT NULL,
  grower_id VARCHAR(255) NOT NULL,
  custody_chain_digest VARCHAR(255) NOT NULL,
  certification_references TEXT NOT NULL,
  exception_count INTEGER NOT NULL,
  geospatial_evidence VARCHAR(255) NOT NULL,
  attestation_state VARCHAR(255) NOT NULL,
  signed_by VARCHAR(255) NOT NULL,
  issued_at TIMESTAMP NOT NULL,
  verification_state VARCHAR(255) NOT NULL,
  document_digest VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (farm_lot_id) REFERENCES agri_supply_chain_traceability_farm_lot(farm_lot_id)
);

CREATE TABLE agri_supply_chain_traceability_agri_supply_chain_traceability_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_rule_id VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  example_text TEXT NOT NULL,
  approver_role VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_agri_supply_chain_traceability_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  runtime_parameter_id VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_agri_supply_chain_traceability_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schema_extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_agri_supply_chain_traceability_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  remediation_task VARCHAR(255) NOT NULL,
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_agri_supply_chain_traceability_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  governed_model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE agri_supply_chain_traceability_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
