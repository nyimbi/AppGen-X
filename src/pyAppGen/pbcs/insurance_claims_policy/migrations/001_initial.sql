CREATE SCHEMA IF NOT EXISTS insurance_claims_policy;

CREATE TABLE insurance_claims_policy_insurance_policy (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  policy_number TEXT NOT NULL,
  product_code TEXT NOT NULL,
  policy_state TEXT NOT NULL,
  premium_status TEXT NOT NULL DEFAULT 'current',
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_policy_holder (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  policy_id TEXT NOT NULL,
  holder_role TEXT NOT NULL,
  party_name TEXT NOT NULL,
  authority_status TEXT NOT NULL DEFAULT 'verified',
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_policy_coverage (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  policy_id TEXT NOT NULL,
  coverage_code TEXT NOT NULL,
  peril_code TEXT NOT NULL,
  limit_amount DECIMAL(18,2) NOT NULL,
  deductible_amount DECIMAL(18,2) NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_policy_endorsement (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  policy_id TEXT NOT NULL,
  endorsement_code TEXT NOT NULL,
  requested_change TEXT NOT NULL,
  premium_delta DECIMAL(18,2) NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_premium_schedule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  policy_id TEXT NOT NULL,
  billing_frequency TEXT NOT NULL,
  installment_amount DECIMAL(18,2) NOT NULL,
  due_date TIMESTAMP NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_premium_payment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  policy_id TEXT NOT NULL,
  schedule_id TEXT,
  amount_paid DECIMAL(18,2) NOT NULL,
  paid_at TIMESTAMP NOT NULL,
  payment_status TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (policy_id) REFERENCES insurance_claims_policy_insurance_policy(id),
  FOREIGN KEY (schedule_id) REFERENCES insurance_claims_policy_premium_schedule(id)
);

CREATE TABLE insurance_claims_policy_claim_record (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  policy_id TEXT NOT NULL,
  claim_number TEXT NOT NULL,
  loss_date TIMESTAMP NOT NULL,
  severity_band TEXT NOT NULL,
  claim_stage TEXT NOT NULL DEFAULT 'fnol',
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (policy_id) REFERENCES insurance_claims_policy_insurance_policy(id)
);

CREATE TABLE insurance_claims_policy_loss_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  occurred_at TIMESTAMP NOT NULL,
  location_code TEXT NOT NULL,
  catastrophe_flag BOOLEAN NOT NULL DEFAULT FALSE,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_claimant (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  claimant_role TEXT NOT NULL,
  claimant_name TEXT NOT NULL,
  relationship_to_insured TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_claim_document (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  document_type TEXT NOT NULL,
  source_channel TEXT NOT NULL,
  received_at TIMESTAMP NOT NULL,
  verification_status TEXT NOT NULL DEFAULT 'pending',
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_coverage_determination (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  policy_id TEXT NOT NULL,
  claim_id TEXT NOT NULL,
  decision TEXT NOT NULL,
  covered_amount DECIMAL(18,2) NOT NULL,
  reasoning_hash TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (policy_id) REFERENCES insurance_claims_policy_insurance_policy(id),
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_claim_reserve (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  reserve_type TEXT NOT NULL,
  recommended_amount DECIMAL(18,2) NOT NULL,
  approved_amount DECIMAL(18,2) NOT NULL,
  adequacy_band TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_reserve_change (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  reserve_id TEXT NOT NULL,
  delta_amount DECIMAL(18,2) NOT NULL,
  reason_code TEXT NOT NULL,
  authority_level TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id),
  FOREIGN KEY (reserve_id) REFERENCES insurance_claims_policy_claim_reserve(id)
);

CREATE TABLE insurance_claims_policy_claim_adjudication (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  decision TEXT NOT NULL,
  liability_position TEXT NOT NULL,
  reviewer_role TEXT NOT NULL,
  reviewed_at TIMESTAMP NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_settlement_offer (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  offer_amount DECIMAL(18,2) NOT NULL,
  negotiation_status TEXT NOT NULL,
  authority_required TEXT NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_settlement_payment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  settlement_offer_id TEXT NOT NULL,
  payee_name TEXT NOT NULL,
  payment_amount DECIMAL(18,2) NOT NULL,
  payment_status TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id),
  FOREIGN KEY (settlement_offer_id) REFERENCES insurance_claims_policy_settlement_offer(id)
);

CREATE TABLE insurance_claims_policy_subrogation_recovery (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  target_party TEXT NOT NULL,
  recovery_amount DECIMAL(18,2) NOT NULL,
  recovery_stage TEXT NOT NULL,
  statute_deadline TIMESTAMP NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_claim_communication (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  channel TEXT NOT NULL,
  recipient_role TEXT NOT NULL,
  response_due_at TIMESTAMP,
  delivery_status TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_fraud_indicator (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  signal_type TEXT NOT NULL,
  score DECIMAL(18,2) NOT NULL,
  disposition TEXT NOT NULL,
  review_status TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_claim_exception_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  claim_id TEXT NOT NULL,
  exception_type TEXT NOT NULL,
  severity TEXT NOT NULL,
  queue_name TEXT NOT NULL,
  resolution_status TEXT NOT NULL DEFAULT 'open',
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (claim_id) REFERENCES insurance_claims_policy_claim_record(id)
);

CREATE TABLE insurance_claims_policy_insurance_policy_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  rule_scope TEXT NOT NULL,
  rule_type TEXT NOT NULL,
  compiled_hash TEXT NOT NULL,
  activation_status TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_insurance_runtime_parameter (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  parameter_name TEXT NOT NULL,
  value_type TEXT NOT NULL,
  current_value TEXT NOT NULL,
  bounded BOOLEAN NOT NULL DEFAULT TRUE,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_insurance_schema_extension (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  target_table TEXT NOT NULL,
  extension_key TEXT NOT NULL,
  approval_status TEXT NOT NULL,
  extension_payload TEXT,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_insurance_control_assertion (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  control_name TEXT NOT NULL,
  control_status TEXT NOT NULL,
  last_checked_at TIMESTAMP NOT NULL,
  evidence_ref TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_insurance_governed_model (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  version INTEGER NOT NULL DEFAULT 1,
  model_name TEXT NOT NULL,
  model_purpose TEXT NOT NULL,
  model_version TEXT NOT NULL,
  approval_status TEXT NOT NULL,
  payload TEXT,
  effective_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  aggregate_type TEXT NOT NULL,
  event_type TEXT NOT NULL,
  topic TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  attempt_count INTEGER NOT NULL DEFAULT 0,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  aggregate_type TEXT NOT NULL,
  event_type TEXT NOT NULL,
  topic TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  attempt_count INTEGER NOT NULL DEFAULT 0,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE insurance_claims_policy_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  aggregate_type TEXT NOT NULL,
  event_type TEXT NOT NULL,
  topic TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  attempt_count INTEGER NOT NULL DEFAULT 0,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
