CREATE SCHEMA IF NOT EXISTS insurance_claims_policy;

CREATE TABLE insurance_claims_policy_insurance_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_claim_intake (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_coverage_validation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_reserve (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_adjuster_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_fraud_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_settlement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_audit_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insurance_policy_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

-- World-class domain depth supplemental tables
CREATE SCHEMA IF NOT EXISTS insurance_claims_policy;

CREATE TABLE insurance_claims_policy_insurance_policy (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_policy_holder (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_policy_coverage (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_policy_endorsement (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_premium_schedule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_premium_payment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_loss_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claimant (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_document (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_coverage_determination (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_reserve (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_reserve_change (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_adjudication (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_settlement_offer (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_settlement_payment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_subrogation_recovery (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_communication (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_fraud_indicator (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_claim_exception_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_insurance_policy_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_insurance_runtime_parameter (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_insurance_schema_extension (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_insurance_control_assertion (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_insurance_governed_model (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  insurance_id TEXT NOT NULL,
  status TEXT NOT NULL,
  version INTEGER NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (insurance_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);
