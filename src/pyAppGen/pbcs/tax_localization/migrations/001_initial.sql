CREATE SCHEMA IF NOT EXISTS tax_localization;

CREATE TABLE tax_localization_tax_jurisdiction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  country VARCHAR(255) NOT NULL,
  region VARCHAR(255) NOT NULL,
  locality VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_jurisdiction_topology (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  topology_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  parent VARCHAR(255) NOT NULL,
  authority_channel VARCHAR(255) NOT NULL,
  nexus_nodes VARCHAR(255) NOT NULL,
  network_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(jurisdiction_id)
);

CREATE TABLE tax_localization_tax_authority_channel (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  channel_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  channel_type VARCHAR(255) NOT NULL,
  endpoint VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  sla VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(jurisdiction_id)
);

CREATE TABLE tax_localization_tax_authority_submission (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  submission_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  filing_id VARCHAR(255) NOT NULL,
  channel_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  acknowledgement VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (filing_id) REFERENCES tax_localization_tax_filing(filing_id)
);

CREATE TABLE tax_localization_tax_filing_calendar (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  calendar_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  frequency VARCHAR(255) NOT NULL,
  due_day VARCHAR(255) NOT NULL,
  holiday_policy VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(jurisdiction_id)
);

CREATE TABLE tax_localization_tax_nexus_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  nexus_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  sales_threshold DECIMAL(18, 4) NOT NULL,
  transaction_threshold DECIMAL(18, 4) NOT NULL,
  active VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tax_type VARCHAR(255) NOT NULL,
  product_class VARCHAR(255) NOT NULL,
  rate DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (jurisdiction_id) REFERENCES tax_localization_tax_jurisdiction(jurisdiction_id)
);

CREATE TABLE tax_localization_tax_rule_version (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_version_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  version INTEGER NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (rule_id) REFERENCES tax_localization_tax_rule(rule_id)
);

CREATE TABLE tax_localization_tax_rule_impact_analysis (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  impact_id VARCHAR(255) PRIMARY KEY NOT NULL,
  rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  proposed_rate DECIMAL(18, 4) NOT NULL,
  current_tax VARCHAR(255) NOT NULL,
  simulated_tax VARCHAR(255) NOT NULL,
  delta_tax VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_product_taxability (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  taxability_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_class VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  review_state VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_counterparty_tax_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  profile_id VARCHAR(255) PRIMARY KEY NOT NULL,
  counterparty_id VARCHAR(255) PRIMARY KEY NOT NULL,
  registration_id VARCHAR(255) NOT NULL,
  exemption_state VARCHAR(255) NOT NULL,
  nexus_state VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_exemption_review (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  review_id VARCHAR(255) PRIMARY KEY NOT NULL,
  certificate_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  expires VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_calculation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  calculation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  order_id VARCHAR(255) NOT NULL,
  tax_total VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_calculation_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  calculation_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  calculation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) NOT NULL,
  taxable_amount DECIMAL(18, 4) NOT NULL,
  tax_amount DECIMAL(18, 4) NOT NULL,
  rate DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (calculation_id) REFERENCES tax_localization_tax_calculation(calculation_id)
);

CREATE TABLE tax_localization_invoice_tax_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  calculation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  tax_total VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  recorded_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (calculation_id) REFERENCES tax_localization_tax_calculation(calculation_id)
);

CREATE TABLE tax_localization_exemption_certificate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  certificate_id VARCHAR(255) PRIMARY KEY NOT NULL,
  counterparty_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  expires VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_reverse_charge_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reverse_charge_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  counterparty_type VARCHAR(255) NOT NULL,
  tax_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_withholding_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  withholding_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  income_type VARCHAR(255) NOT NULL,
  rate DECIMAL(18, 4) NOT NULL,
  treaty_code VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_environmental_levy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  levy_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_class VARCHAR(255) NOT NULL,
  rate DECIMAL(18, 4) NOT NULL,
  basis VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_cross_border_duty (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  duty_id VARCHAR(255) PRIMARY KEY NOT NULL,
  origin VARCHAR(255) NOT NULL,
  destination VARCHAR(255) NOT NULL,
  goods_value VARCHAR(255) NOT NULL,
  duty_rate DECIMAL(18, 4) NOT NULL,
  duty VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_duty_classification (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  classification_id VARCHAR(255) PRIMARY KEY NOT NULL,
  product_id VARCHAR(255) PRIMARY KEY NOT NULL,
  hs_code VARCHAR(255) NOT NULL,
  origin VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_landed_cost_component (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  component_id VARCHAR(255) PRIMARY KEY NOT NULL,
  duty_id VARCHAR(255) PRIMARY KEY NOT NULL,
  component_type VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_filing (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  filing_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  period TIMESTAMP NOT NULL,
  liability DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_filing_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  filing_line_id VARCHAR(255) PRIMARY KEY NOT NULL,
  filing_id VARCHAR(255) PRIMARY KEY NOT NULL,
  calculation_id VARCHAR(255) NOT NULL,
  tax_total VARCHAR(255) NOT NULL,
  line_type VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (filing_id) REFERENCES tax_localization_tax_filing(filing_id)
);

CREATE TABLE tax_localization_tax_reconciliation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  reconciliation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  accrued VARCHAR(255) NOT NULL,
  collected VARCHAR(255) NOT NULL,
  remitted VARCHAR(255) NOT NULL,
  variance VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_remittance_batch (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  batch_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  due_date TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_payment_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  payment_evidence_id TEXT PRIMARY KEY NOT NULL,
  batch_id VARCHAR(255) PRIMARY KEY NOT NULL,
  payment_reference VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  paid_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (batch_id) REFERENCES tax_localization_tax_remittance_batch(batch_id)
);

CREATE TABLE tax_localization_tax_refund_claim (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  refund_claim_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_adjustment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  adjustment_id VARCHAR(255) PRIMARY KEY NOT NULL,
  calculation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_notice (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  notice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  notice_type VARCHAR(255) NOT NULL,
  received_at TIMESTAMP NOT NULL,
  resolution_state VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_digital_tax_document (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  document_id VARCHAR(255) PRIMARY KEY NOT NULL,
  invoice_id VARCHAR(255) PRIMARY KEY NOT NULL,
  clearance_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  authority VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_document_parse (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parse_id VARCHAR(255) PRIMARY KEY NOT NULL,
  document_id VARCHAR(255) PRIMARY KEY NOT NULL,
  certificate_id VARCHAR(255) NOT NULL,
  rate_percent DECIMAL(18, 4) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_liability_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  forecast_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  horizon VARCHAR(255) NOT NULL,
  expected_liability DECIMAL(18, 4) NOT NULL,
  tail_risk VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_policy_simulation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  simulation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  proposed_rate DECIMAL(18, 4) NOT NULL,
  delta_tax VARCHAR(255) NOT NULL,
  objective_score DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_cross_border_federation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  federation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  external_system VARCHAR(255) NOT NULL,
  projection_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_identity_credential (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  credential_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  did VARCHAR(255) NOT NULL,
  issuer VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_audit_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) PRIMARY KEY NOT NULL,
  filing_id VARCHAR(255) PRIMARY KEY NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  public_claims TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  allocation_id VARCHAR(255) PRIMARY KEY NOT NULL,
  liability_id DECIMAL(18, 4) PRIMARY KEY NOT NULL,
  party VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  clearing_bid VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_id VARCHAR(255) PRIMARY KEY NOT NULL,
  signal_type VARCHAR(255) NOT NULL,
  entropy VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_model_registry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  feature_lineage VARCHAR(255) NOT NULL,
  auc VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  seed_id VARCHAR(255) PRIMARY KEY NOT NULL,
  jurisdiction_pack VARCHAR(255) NOT NULL,
  tax_type VARCHAR(255) NOT NULL,
  product_class VARCHAR(255) NOT NULL,
  rate DECIMAL(18, 4) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_rule_id VARCHAR(255) PRIMARY KEY NOT NULL,
  scope VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  predicate TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_parameter (
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

CREATE TABLE tax_localization_tax_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) PRIMARY KEY NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  retry_limit VARCHAR(255) NOT NULL,
  authority_channels VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_tax_schema_extension (
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

CREATE TABLE tax_localization_tax_control_assertion (
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

CREATE TABLE tax_localization_tax_governed_model (
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

CREATE TABLE tax_localization_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE tax_localization_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  reason VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
