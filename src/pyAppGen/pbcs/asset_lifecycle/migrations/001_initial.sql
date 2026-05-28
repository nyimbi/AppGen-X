CREATE SCHEMA IF NOT EXISTS asset_lifecycle;

CREATE TABLE asset_lifecycle_fixed_asset (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  legal_entity VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  category VARCHAR(255) NOT NULL,
  cost DECIMAL(18, 4) NOT NULL,
  book_value VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_component (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  component_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  component_name VARCHAR(255) NOT NULL,
  capitalization_split VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES asset_lifecycle_fixed_asset(asset_id)
);

CREATE TABLE asset_lifecycle_asset_component_history (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  component_history_id VARCHAR(255) PRIMARY KEY NOT NULL,
  component_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  effective_date TIMESTAMP NOT NULL,
  evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (component_id) REFERENCES asset_lifecycle_asset_component(component_id)
);

CREATE TABLE asset_lifecycle_asset_book (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  book_id VARCHAR(255) PRIMARY KEY NOT NULL,
  book_name VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  purpose VARCHAR(255) NOT NULL,
  default_method VARCHAR(255) NOT NULL,
  calendar VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_book_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assignment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  book_id VARCHAR(255) NOT NULL,
  assigned_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES asset_lifecycle_fixed_asset(asset_id)
);

CREATE TABLE asset_lifecycle_asset_acquisition (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  acquisition_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  receipt_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  capitalization_state VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES asset_lifecycle_fixed_asset(asset_id)
);

CREATE TABLE asset_lifecycle_asset_capitalization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  capitalization_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  capitalized_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_lease_right_of_use (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  lease_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  liability DECIMAL(18, 4) NOT NULL,
  term_months INTEGER NOT NULL,
  discount_rate DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_depreciation_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  book VARCHAR(255) NOT NULL,
  method VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES asset_lifecycle_fixed_asset(asset_id)
);

CREATE TABLE asset_lifecycle_asset_depreciation_schedule_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  schedule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  period TIMESTAMP NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  book_value VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (schedule_id) REFERENCES asset_lifecycle_asset_depreciation_schedule(schedule_id)
);

CREATE TABLE asset_lifecycle_asset_depreciation_run (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  run_id VARCHAR(255) PRIMARY KEY NOT NULL,
  period TIMESTAMP NOT NULL,
  book VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_depreciation_journal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  journal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  run_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) NOT NULL,
  period TIMESTAMP NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  route VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (run_id) REFERENCES asset_lifecycle_asset_depreciation_run(run_id)
);

CREATE TABLE asset_lifecycle_asset_transfer (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  transfer_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  location VARCHAR(255) NOT NULL,
  cost_center DECIMAL(18, 4) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES asset_lifecycle_fixed_asset(asset_id)
);

CREATE TABLE asset_lifecycle_asset_valuation_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  adjustment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  adjustment_type VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_impairment_indicator (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  indicator_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  market_indicator VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_maintenance_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  maintenance_adjustment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  useful_life_delta VARCHAR(255) NOT NULL,
  evidence TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_insurance_warranty (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  coverage_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  coverage VARCHAR(255) NOT NULL,
  warranty_months VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_claim (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  claim_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_retirement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  retirement_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  method VARCHAR(255) NOT NULL,
  proceeds DECIMAL(18, 4) NOT NULL,
  gain_loss VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES asset_lifecycle_fixed_asset(asset_id)
);

CREATE TABLE asset_lifecycle_asset_disposal_proceeds (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proceeds_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  received_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_physical_verification (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  verification_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  location VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES asset_lifecycle_fixed_asset(asset_id)
);

CREATE TABLE asset_lifecycle_asset_physical_verification_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  exception_id VARCHAR(255) PRIMARY KEY NOT NULL,
  verification_id VARCHAR(255) PRIMARY KEY NOT NULL,
  reason VARCHAR(255) NOT NULL,
  resolution_state VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_location_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  location_assignment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  location VARCHAR(255) NOT NULL,
  effective_date TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_custodian_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  custodian_assignment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  custodian VARCHAR(255) NOT NULL,
  effective_date TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_cost_center_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  cost_center_assignment_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  cost_center DECIMAL(18, 4) NOT NULL,
  effective_date TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  screening_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  policy VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_audit_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  public_claims TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_cross_system_federation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  federation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  external_system VARCHAR(255) NOT NULL,
  projection_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_identity_credential (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  credential_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  did VARCHAR(255) NOT NULL,
  issuer VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_carbon_utilization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  carbon_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  window TIMESTAMP NOT NULL,
  carbon_intensity VARCHAR(255) NOT NULL,
  selected VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_portfolio_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  portfolio_id VARCHAR(255) PRIMARY KEY NOT NULL,
  selected_asset VARCHAR(255) NOT NULL,
  objective_score DECIMAL(18, 4) NOT NULL,
  candidate_count INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_allocation_mechanism (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allocation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  clearing_bid VARCHAR(255) NOT NULL,
  allocated_hours VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  signal_type VARCHAR(255) NOT NULL,
  kl_divergence VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  risk_model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_id VARCHAR(255) PRIMARY KEY NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  explanations TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  seed_id VARCHAR(255) PRIMARY KEY NOT NULL,
  asset_category VARCHAR(255) NOT NULL,
  book VARCHAR(255) NOT NULL,
  method VARCHAR(255) NOT NULL,
  useful_life_months VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) PRIMARY KEY NOT NULL,
  table_name VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_id VARCHAR(255) PRIMARY KEY NOT NULL,
  assertion VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  tested_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  feature_lineage VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  governance_status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  predicate TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  value VARCHAR(255) NOT NULL,
  bounds VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  default_book VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
