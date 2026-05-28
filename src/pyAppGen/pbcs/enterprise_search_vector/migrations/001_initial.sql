CREATE SCHEMA IF NOT EXISTS enterprise_search_vector;

CREATE TABLE enterprise_search_vector_search_index (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  index_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  locale VARCHAR(255) NOT NULL,
  ranking_mode VARCHAR(255) NOT NULL,
  document_count INTEGER NOT NULL,
  ready_document_count INTEGER NOT NULL,
  feedback_count INTEGER NOT NULL,
  last_embedding_job_id VARCHAR(255) NOT NULL,
  last_refresh_id VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_embedding_job (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  job_id VARCHAR(255) NOT NULL,
  index_id VARCHAR(255) NOT NULL,
  document_ids VARCHAR(255) NOT NULL,
  document_count INTEGER NOT NULL,
  vector_dimensions TEXT NOT NULL,
  started_at TIMESTAMP NOT NULL,
  completed_at TIMESTAMP NOT NULL,
  failure_reason VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_vector_document (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  document_id VARCHAR(255) NOT NULL,
  index_id VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  locale VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  body VARCHAR(255) NOT NULL,
  chunks VARCHAR(255) NOT NULL,
  token_count INTEGER NOT NULL,
  chunk_count INTEGER NOT NULL,
  embedding VARCHAR(255) NOT NULL,
  acl VARCHAR(255) NOT NULL,
  embedding_job_id VARCHAR(255) NOT NULL,
  feedback_score DECIMAL(18, 4) NOT NULL,
  freshness_score DECIMAL(18, 4) NOT NULL,
  authority_score DECIMAL(18, 4) NOT NULL,
  quality_review_status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_query_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  query_id VARCHAR(255) NOT NULL,
  index_id VARCHAR(255) NOT NULL,
  query_text VARCHAR(255) NOT NULL,
  locale VARCHAR(255) NOT NULL,
  principal_permissions VARCHAR(255) NOT NULL,
  ranking_mode VARCHAR(255) NOT NULL,
  result_count INTEGER NOT NULL,
  results VARCHAR(255) NOT NULL,
  explanations TEXT NOT NULL,
  feedback VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_ranking_simulation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  simulation_id VARCHAR(255) NOT NULL,
  query_id VARCHAR(255) NOT NULL,
  weight_overrides VARCHAR(255) NOT NULL,
  baseline_top_result VARCHAR(255) NOT NULL,
  simulated_results VARCHAR(255) NOT NULL,
  simulation_status VARCHAR(255) NOT NULL,
  reviewed_by VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_freshness_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  forecast_id VARCHAR(255) NOT NULL,
  index_id VARCHAR(255) NOT NULL,
  horizon_days VARCHAR(255) NOT NULL,
  current_freshness_score DECIMAL(18, 4) NOT NULL,
  projected_freshness_score DECIMAL(18, 4) NOT NULL,
  recommended_refresh_before_days VARCHAR(255) NOT NULL,
  forecast_method VARCHAR(255) NOT NULL,
  confidence_score DECIMAL(18, 4) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_quality_remediation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  remediation_id VARCHAR(255) NOT NULL,
  document_id VARCHAR(255) NOT NULL,
  index_id VARCHAR(255) NOT NULL,
  issue VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  result VARCHAR(255) NOT NULL,
  assigned_team VARCHAR(255) NOT NULL,
  control_status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_search_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  screening_id VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  locale VARCHAR(255) NOT NULL,
  principal_permissions VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  policy_rule_id VARCHAR(255) NOT NULL,
  required_acl VARCHAR(255) NOT NULL,
  decision_reason VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_relevance_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  query_id VARCHAR(255) NOT NULL,
  top_score DECIMAL(18, 4) NOT NULL,
  threshold DECIMAL(18, 4) NOT NULL,
  result_count INTEGER NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  control_status VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_index_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  proof_id VARCHAR(255) NOT NULL,
  index_id VARCHAR(255) NOT NULL,
  document_count INTEGER NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  verification_status VARCHAR(255) NOT NULL,
  proof_algorithm VARCHAR(255) NOT NULL,
  sealed_by VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_federated_search_view (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  view_id VARCHAR(255) NOT NULL,
  index_id VARCHAR(255) NOT NULL,
  source_counts VARCHAR(255) NOT NULL,
  query_count INTEGER NOT NULL,
  declared_dependencies VARCHAR(255) NOT NULL,
  view_status VARCHAR(255) NOT NULL,
  federation_policy VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_query_intent_risk (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  risk_id VARCHAR(255) NOT NULL,
  query_id VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  risk_reasons VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  policy_action VARCHAR(255) NOT NULL,
  review_required VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_retention_deletion_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  document_id VARCHAR(255) NOT NULL,
  index_id VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  disposition_status VARCHAR(255) NOT NULL,
  retention_basis VARCHAR(255) NOT NULL,
  legal_hold VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_search_audit_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  entry_id VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  payload_digest TEXT NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  sealed_at TIMESTAMP NOT NULL,
  actor VARCHAR(255) NOT NULL,
  channel VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_search_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_type VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  approval_status VARCHAR(255) NOT NULL,
  evidence_hash TEXT NOT NULL,
  validation_dataset VARCHAR(255) NOT NULL,
  risk_rating VARCHAR(255) NOT NULL,
  audit_proof VARCHAR(255) NOT NULL
);

CREATE TABLE enterprise_search_vector_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  published_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_search_vector_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  consumed_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_search_vector_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  failure_reason VARCHAR(255) NOT NULL
);
