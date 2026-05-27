CREATE SCHEMA IF NOT EXISTS ap_automation;

CREATE TABLE ap_automation_vendor (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE ap_automation_vendor_site (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_vendor_bank_account (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_vendor_tax_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_vendor_risk_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_purchase_order (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_purchase_order_line (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_goods_receipt (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_goods_receipt_line (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_invoice (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_invoice_line (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_invoice_capture_artifact (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_invoice_match_result (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_payment (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_payment_batch (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_payment_rail_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_discount_opportunity (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_vendor_statement (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_withholding_tax (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_e_invoice_submission (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_exception_case (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_approval_task (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_cash_forecast_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  vendor_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (vendor_id) REFERENCES ap_automation_vendor(id)
);

CREATE TABLE ap_automation_outbox (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE ap_automation_inbox (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE ap_automation_dead_letter (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);
