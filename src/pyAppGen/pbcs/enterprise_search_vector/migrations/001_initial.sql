CREATE SCHEMA IF NOT EXISTS enterprise_search_vector;

CREATE TABLE enterprise_search_vector_search_index (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(120) NOT NULL,
  index_id VARCHAR(160) NOT NULL,
  name VARCHAR(240) NOT NULL,
  source VARCHAR(80) NOT NULL,
  locale VARCHAR(40) NOT NULL,
  ranking_mode VARCHAR(80) NOT NULL,
  document_count INTEGER NOT NULL,
  ready_document_count INTEGER NOT NULL,
  feedback_count INTEGER NOT NULL,
  last_embedding_job_id VARCHAR(160),
  last_refresh_id VARCHAR(160),
  audit_proof VARCHAR(200) NOT NULL,
  status VARCHAR(80) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_search_vector_embedding_job (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(120) NOT NULL,
  job_id VARCHAR(160) NOT NULL,
  index_id VARCHAR(160) NOT NULL,
  document_ids TEXT NOT NULL,
  document_count INTEGER NOT NULL,
  vector_dimensions INTEGER NOT NULL,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  failure_reason TEXT,
  audit_proof VARCHAR(200) NOT NULL,
  status VARCHAR(80) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_search_vector_vector_document (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(120) NOT NULL,
  document_id VARCHAR(160) NOT NULL,
  index_id VARCHAR(160) NOT NULL,
  source VARCHAR(80) NOT NULL,
  locale VARCHAR(40) NOT NULL,
  title VARCHAR(500) NOT NULL,
  body TEXT NOT NULL,
  chunks TEXT NOT NULL,
  token_count INTEGER NOT NULL,
  chunk_count INTEGER NOT NULL,
  embedding TEXT,
  acl TEXT NOT NULL,
  embedding_job_id VARCHAR(160),
  feedback_score DECIMAL(12,4) NOT NULL,
  freshness_score DECIMAL(12,4) NOT NULL,
  authority_score DECIMAL(12,4) NOT NULL,
  quality_review_status VARCHAR(80) NOT NULL,
  audit_proof VARCHAR(200) NOT NULL,
  status VARCHAR(80) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_search_vector_query_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(120) NOT NULL,
  query_id VARCHAR(160) NOT NULL,
  index_id VARCHAR(160),
  query_text TEXT NOT NULL,
  locale VARCHAR(40) NOT NULL,
  principal_permissions TEXT NOT NULL,
  ranking_mode VARCHAR(80) NOT NULL,
  result_count INTEGER NOT NULL,
  results TEXT NOT NULL,
  explanations TEXT NOT NULL,
  feedback TEXT,
  audit_proof VARCHAR(200) NOT NULL,
  status VARCHAR(80) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE enterprise_search_vector_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  tenant VARCHAR(120) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(80) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  published_at TIMESTAMP
);

CREATE TABLE enterprise_search_vector_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  tenant VARCHAR(120) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(80) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  consumed_at TIMESTAMP
);

CREATE TABLE enterprise_search_vector_dead_letter_event (
  id INTEGER PRIMARY KEY,
  tenant VARCHAR(120) NOT NULL,
  event_id VARCHAR(255),
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255),
  attempts INTEGER NOT NULL,
  failure_reason TEXT NOT NULL,
  status VARCHAR(80) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
