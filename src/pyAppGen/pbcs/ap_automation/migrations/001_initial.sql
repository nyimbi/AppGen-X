CREATE SCHEMA IF NOT EXISTS ap_automation;

CREATE TABLE ap_automation_vendor (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  approval_status VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (vendor_id));

CREATE TABLE ap_automation_vendor_site (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  site_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  address TEXT NOT NULL,
  remit_to VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_vendor_bank_account (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  bank_account_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  rail VARCHAR(255) NOT NULL,
  masked_account VARCHAR(255) NOT NULL,
  validation_status VARCHAR(255) NOT NULL,
  token_ref VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_vendor_tax_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  tax_profile_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  withholding_code VARCHAR(255) NOT NULL,
  exemption_status VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_vendor_risk_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  signal_type VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  source VARCHAR(255) NOT NULL,
  observed_at TIMESTAMP NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_purchase_order (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  po_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  total DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
,
  UNIQUE (po_id));

CREATE TABLE ap_automation_purchase_order_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  po_line_id VARCHAR(255) NOT NULL,
  po_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price DECIMAL(18, 4) NOT NULL,
  account VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id),
  FOREIGN KEY (po_id) REFERENCES ap_automation_purchase_order(po_id)
);

CREATE TABLE ap_automation_goods_receipt (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  receipt_id VARCHAR(255) NOT NULL,
  po_id VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL,
  received_at TIMESTAMP NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id),
  FOREIGN KEY (po_id) REFERENCES ap_automation_purchase_order(po_id)
,
  UNIQUE (receipt_id));

CREATE TABLE ap_automation_goods_receipt_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  receipt_line_id VARCHAR(255) NOT NULL,
  receipt_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  exception_code VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id),
  FOREIGN KEY (receipt_id) REFERENCES ap_automation_goods_receipt(receipt_id)
);

CREATE TABLE ap_automation_invoice (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  po_id VARCHAR(255) NOT NULL,
  receipt_id VARCHAR(255) NOT NULL,
  subtotal DECIMAL(18, 4) NOT NULL,
  total DECIMAL(18, 4) NOT NULL,
  approval_status VARCHAR(255) NOT NULL,
  payment_status VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
,
  UNIQUE (invoice_id));

CREATE TABLE ap_automation_invoice_line (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  invoice_line_id VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  sku VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price DECIMAL(18, 4) NOT NULL,
  account VARCHAR(255) NOT NULL,
  tax_code VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id),
  FOREIGN KEY (invoice_id) REFERENCES ap_automation_invoice(invoice_id)
);

CREATE TABLE ap_automation_invoice_capture_artifact (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  artifact_id VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  artifact_type VARCHAR(255) NOT NULL,
  source_hash VARCHAR(255) NOT NULL,
  extraction_confidence DECIMAL(18, 4) NOT NULL,
  storage_ref VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_invoice_match_result (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  match_id VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  po_id VARCHAR(255) NOT NULL,
  receipt_id VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  explanation_hash VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_payment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  payment_id VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  rail VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id),
  FOREIGN KEY (invoice_id) REFERENCES ap_automation_invoice(invoice_id)
);

CREATE TABLE ap_automation_payment_batch (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  batch_id VARCHAR(255) NOT NULL,
  rail VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  scheduled_date TIMESTAMP NOT NULL,
  total_amount DECIMAL(18, 4) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_payment_rail_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) NOT NULL,
  payment_id VARCHAR(255) NOT NULL,
  rail VARCHAR(255) NOT NULL,
  cost DECIMAL(18, 4) NOT NULL,
  latency INTEGER NOT NULL,
  risk VARCHAR(255) NOT NULL,
  selected BOOLEAN NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_discount_opportunity (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  opportunity_id VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  discount_rate DECIMAL(18, 4) NOT NULL,
  discount_value DECIMAL(18, 4) NOT NULL,
  net_benefit DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_vendor_statement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  statement_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  statement_hash VARCHAR(255) NOT NULL,
  reconciled_amount DECIMAL(18, 4) NOT NULL,
  exception_count INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_withholding_tax (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  withholding_id VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  amount DECIMAL(18, 4) NOT NULL,
  rate DECIMAL(18, 4) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_e_invoice_submission (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  submission_id VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  jurisdiction VARCHAR(255) NOT NULL,
  standard VARCHAR(255) NOT NULL,
  submission_hash VARCHAR(255) NOT NULL,
  accepted BOOLEAN NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_exception_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  case_id VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  reason TEXT NOT NULL,
  decision VARCHAR(255) NOT NULL,
  suggestion TEXT NOT NULL,
  audit_trace TEXT NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id),
  FOREIGN KEY (invoice_id) REFERENCES ap_automation_invoice(invoice_id)
);

CREATE TABLE ap_automation_approval_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  approval_id VARCHAR(255) NOT NULL,
  invoice_id VARCHAR(255) NOT NULL,
  assignee VARCHAR(255) NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  decided_at TIMESTAMP NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_cash_forecast_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  available_cash DECIMAL(18, 4) NOT NULL,
  as_of TIMESTAMP NOT NULL,
  source_event_id VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  predicate TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  value TEXT NOT NULL,
  bounds TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) NOT NULL,
  table_name VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  control_id VARCHAR(255) NOT NULL,
  assertion TEXT NOT NULL,
  evidence_hash VARCHAR(255) NOT NULL,
  tested_at TIMESTAMP NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  feature_lineage TEXT NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  governance_status VARCHAR(255) NOT NULL,
  vendor_id VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(vendor_id)
);

CREATE TABLE ap_automation_outbox (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ap_automation_inbox (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ap_automation_dead_letter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  reason TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP,
  updated_at TIMESTAMP NOT NULL
);
