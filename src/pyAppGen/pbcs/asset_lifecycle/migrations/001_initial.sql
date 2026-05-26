CREATE SCHEMA IF NOT EXISTS asset_lifecycle;

CREATE TABLE asset_lifecycle_fixed_asset (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE asset_lifecycle_asset_component (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_component_history (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_book (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_book_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_acquisition (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_capitalization (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_lease_right_of_use (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_depreciation_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_depreciation_schedule_line (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_depreciation_run (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_depreciation_journal (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_transfer (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_valuation_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_impairment_indicator (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_maintenance_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_insurance_warranty (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_claim (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_retirement (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_disposal_proceeds (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_physical_verification (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_physical_verification_exception (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_location_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_custodian_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_cost_center_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_audit_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_cross_system_federation (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_identity_credential (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_carbon_utilization (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_portfolio_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_allocation_mechanism (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_asset_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  fixed_asset_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (fixed_asset_id) REFERENCES asset_lifecycle_fixed_asset(id)
);

CREATE TABLE asset_lifecycle_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE asset_lifecycle_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE asset_lifecycle_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);
