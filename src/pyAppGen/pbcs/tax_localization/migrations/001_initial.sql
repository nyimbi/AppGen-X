CREATE SCHEMA IF NOT EXISTS tax_localization;

CREATE TABLE tax_localization_tax_jurisdiction (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_jurisdiction_topology (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_authority_channel (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_authority_submission (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_filing_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_nexus_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_rule_version (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_rule_impact_analysis (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_product_taxability (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_counterparty_tax_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_exemption_review (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_calculation (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_calculation_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_invoice_tax_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_exemption_certificate (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_reverse_charge_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_withholding_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_environmental_levy (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_cross_border_duty (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_duty_classification (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_landed_cost_component (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_filing (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_filing_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_reconciliation (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_remittance_batch (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_payment_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_refund_claim (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_notice (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_digital_tax_document (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_document_parse (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_liability_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_policy_simulation (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_cross_border_federation (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_identity_credential (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_audit_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_model_registry (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_tax_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tax_jurisdiction_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (tax_jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(id)
);

CREATE TABLE tax_localization_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE tax_localization_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE tax_localization_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);
