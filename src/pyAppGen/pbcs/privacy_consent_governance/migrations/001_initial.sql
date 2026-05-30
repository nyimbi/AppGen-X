CREATE SCHEMA IF NOT EXISTS privacy_consent_governance;

CREATE TABLE privacy_consent_governance_data_subject (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  subject_identifier TEXT NOT NULL,
  region TEXT NOT NULL,
  email TEXT,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_consent_capture (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  data_subject_id TEXT NOT NULL,
  purpose_code TEXT NOT NULL,
  lawful_basis_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  consent_state TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_subject_id) REFERENCES privacy_consent_governance_data_subject(id)
);

CREATE TABLE privacy_consent_governance_consent_preference (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  data_subject_id TEXT NOT NULL,
  channel TEXT NOT NULL,
  preference_state TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_subject_id) REFERENCES privacy_consent_governance_data_subject(id)
);

CREATE TABLE privacy_consent_governance_consent_revocation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  consent_capture_id TEXT NOT NULL,
  revocation_reason TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (consent_capture_id) REFERENCES privacy_consent_governance_consent_capture(id)
);

CREATE TABLE privacy_consent_governance_processing_purpose (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  data_category TEXT NOT NULL,
  purpose_owner TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_lawful_basis_registry (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  purpose_code TEXT NOT NULL,
  jurisdiction TEXT NOT NULL,
  basis_type TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_privacy_notice (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  notice_family TEXT NOT NULL,
  locale TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_policy_version (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  notice_id TEXT NOT NULL,
  version_label TEXT NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (notice_id) REFERENCES privacy_consent_governance_privacy_notice(id)
);

CREATE TABLE privacy_consent_governance_dsar_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  data_subject_id TEXT NOT NULL,
  request_type TEXT NOT NULL,
  due_at TIMESTAMP NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_subject_id) REFERENCES privacy_consent_governance_data_subject(id)
);

CREATE TABLE privacy_consent_governance_dsar_task (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  dsar_case_id TEXT NOT NULL,
  owner TEXT NOT NULL,
  task_type TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (dsar_case_id) REFERENCES privacy_consent_governance_dsar_case(id)
);

CREATE TABLE privacy_consent_governance_erasure_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  data_subject_id TEXT NOT NULL,
  legal_hold_state TEXT NOT NULL,
  decision TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_subject_id) REFERENCES privacy_consent_governance_data_subject(id)
);

CREATE TABLE privacy_consent_governance_retention_schedule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  data_category TEXT NOT NULL,
  retention_days INTEGER NOT NULL,
  legal_basis TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_retention_decision (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  retention_schedule_id TEXT NOT NULL,
  decision TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (retention_schedule_id) REFERENCES privacy_consent_governance_retention_schedule(id)
);

CREATE TABLE privacy_consent_governance_cross_border_restriction (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  destination_country TEXT NOT NULL,
  transfer_mechanism TEXT NOT NULL,
  restriction_level TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_disclosure_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  data_subject_id TEXT NOT NULL,
  recipient TEXT NOT NULL,
  jurisdiction TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (data_subject_id) REFERENCES privacy_consent_governance_data_subject(id)
);

CREATE TABLE privacy_consent_governance_audit_proof (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  control_name TEXT NOT NULL,
  proof_hash TEXT NOT NULL,
  proof_scope TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_ai_document_intake (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  document_digest TEXT NOT NULL,
  document_kind TEXT NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_ai_instruction_plan (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  document_intake_id TEXT NOT NULL,
  target_operation TEXT NOT NULL,
  confirmation_required BOOLEAN NOT NULL,
  status TEXT NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (document_intake_id) REFERENCES privacy_consent_governance_ai_document_intake(id)
);

CREATE TABLE privacy_consent_governance_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  event_type TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  payload TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  event_type TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  payload TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE privacy_consent_governance_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  event_type TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  payload TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
