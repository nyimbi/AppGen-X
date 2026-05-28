CREATE SCHEMA IF NOT EXISTS case_knowledge_management;

CREATE TABLE case_knowledge_management_support_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  channel TEXT NOT NULL,
  status TEXT NOT NULL,
  title TEXT NOT NULL,
  summary TEXT NOT NULL,
  customer_ref TEXT NOT NULL,
  product_area TEXT NOT NULL,
  severity TEXT NOT NULL,
  impact_score NUMERIC NOT NULL,
  queue_code TEXT,
  owner_id TEXT,
  duplicate_of TEXT,
  knowledge_gap BOOLEAN NOT NULL DEFAULT FALSE,
  version INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_contact (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  role TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  authority_level TEXT NOT NULL,
  notification_preference TEXT NOT NULL,
  language TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_classification (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  taxonomy_code TEXT NOT NULL,
  product_component TEXT NOT NULL,
  symptom TEXT NOT NULL,
  confidence NUMERIC NOT NULL,
  rationale TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_queue (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  label TEXT NOT NULL,
  region TEXT NOT NULL,
  language TEXT NOT NULL,
  product_scope TEXT NOT NULL,
  capacity_limit INTEGER NOT NULL,
  active_load INTEGER NOT NULL DEFAULT 0,
  health TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_assignment (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  queue_id TEXT NOT NULL REFERENCES case_knowledge_management_case_queue(id),
  assignee_id TEXT NOT NULL,
  status TEXT NOT NULL,
  rationale TEXT NOT NULL,
  workload_score NUMERIC NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_sla (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  policy_code TEXT NOT NULL,
  first_response_due_at TIMESTAMP NOT NULL,
  resolution_due_at TIMESTAMP NOT NULL,
  paused BOOLEAN NOT NULL DEFAULT FALSE,
  risk_level TEXT NOT NULL,
  risk_score NUMERIC NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_sla_timer_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  sla_id TEXT NOT NULL REFERENCES case_knowledge_management_case_sla(id),
  timer_kind TEXT NOT NULL,
  event_kind TEXT NOT NULL,
  reason TEXT NOT NULL,
  event_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_interaction (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  channel TEXT NOT NULL,
  visibility TEXT NOT NULL,
  author_role TEXT NOT NULL,
  sentiment TEXT NOT NULL,
  summary TEXT NOT NULL,
  requires_follow_up BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_escalation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  level TEXT NOT NULL,
  reason TEXT NOT NULL,
  target_team TEXT NOT NULL,
  status TEXT NOT NULL,
  opened_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_resolution (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  resolution_type TEXT NOT NULL,
  summary TEXT NOT NULL,
  workaround TEXT,
  confirmed BOOLEAN NOT NULL DEFAULT FALSE,
  resolved_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_knowledge_article (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  title TEXT NOT NULL,
  audience TEXT NOT NULL,
  product_area TEXT NOT NULL,
  lifecycle_state TEXT NOT NULL,
  freshness_state TEXT NOT NULL,
  current_version INTEGER NOT NULL DEFAULT 1,
  quality_score NUMERIC NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_article_version (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  article_id TEXT NOT NULL REFERENCES case_knowledge_management_knowledge_article(id),
  version_number INTEGER NOT NULL,
  change_summary TEXT NOT NULL,
  body TEXT NOT NULL,
  reviewer TEXT,
  published_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_article_feedback (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  article_id TEXT NOT NULL REFERENCES case_knowledge_management_knowledge_article(id),
  source_case_id TEXT REFERENCES case_knowledge_management_support_case(id),
  rating INTEGER NOT NULL,
  theme TEXT NOT NULL,
  comment TEXT,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_article_quality_score (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  article_id TEXT NOT NULL REFERENCES case_knowledge_management_knowledge_article(id),
  readability NUMERIC NOT NULL,
  success_rate NUMERIC NOT NULL,
  deflection_rate NUMERIC NOT NULL,
  overall_score NUMERIC NOT NULL,
  calculated_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_root_cause (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  category TEXT NOT NULL,
  hypothesis TEXT NOT NULL,
  confidence NUMERIC NOT NULL,
  corrective_action TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_duplicate_link (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  duplicate_case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  confidence NUMERIC NOT NULL,
  disposition TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_exception_case (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  exception_type TEXT NOT NULL,
  reason TEXT NOT NULL,
  disposition TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_policy_rule (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  code TEXT NOT NULL,
  scope TEXT NOT NULL,
  status TEXT NOT NULL,
  condition TEXT NOT NULL,
  outcome TEXT NOT NULL,
  compiled_hash TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_runtime_parameter (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  key TEXT NOT NULL,
  scope TEXT NOT NULL,
  value JSON NOT NULL,
  value_type TEXT NOT NULL,
  bounded BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_schema_extension (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  table_name TEXT NOT NULL,
  field_name TEXT NOT NULL,
  field_type TEXT NOT NULL,
  reason TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_control_assertion (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  control_code TEXT NOT NULL,
  subject_ref TEXT NOT NULL,
  status TEXT NOT NULL,
  evidence TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_governed_model (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  model_name TEXT NOT NULL,
  use_case TEXT NOT NULL,
  status TEXT NOT NULL,
  grounding_required BOOLEAN NOT NULL DEFAULT TRUE,
  citation_mode TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_semantic_knowledge_index (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  article_id TEXT NOT NULL REFERENCES case_knowledge_management_knowledge_article(id),
  embedding_key TEXT NOT NULL,
  keywords JSON NOT NULL,
  quality_band TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_case_deflection_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  article_id TEXT REFERENCES case_knowledge_management_knowledge_article(id),
  search_query TEXT NOT NULL,
  outcome TEXT NOT NULL,
  elapsed_minutes INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_knowledge_approval (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  article_id TEXT NOT NULL REFERENCES case_knowledge_management_knowledge_article(id),
  approver_id TEXT NOT NULL,
  decision TEXT NOT NULL,
  reason TEXT,
  decided_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_content_freshness_signal (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  article_id TEXT NOT NULL REFERENCES case_knowledge_management_knowledge_article(id),
  signal_type TEXT NOT NULL,
  state TEXT NOT NULL,
  review_due_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_agent_assist_recommendation (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES case_knowledge_management_support_case(id),
  recommendation_type TEXT NOT NULL,
  confidence NUMERIC NOT NULL,
  citations JSON NOT NULL,
  recommended_actions JSON NOT NULL,
  accepted BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_appgen_outbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  event_type TEXT NOT NULL,
  aggregate_id TEXT NOT NULL,
  status TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  payload JSON NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_appgen_inbox_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  event_type TEXT NOT NULL,
  external_id TEXT NOT NULL,
  status TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  payload JSON NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE case_knowledge_management_appgen_dead_letter_event (
  id TEXT PRIMARY KEY NOT NULL,
  tenant TEXT NOT NULL,
  event_type TEXT NOT NULL,
  external_id TEXT NOT NULL,
  status TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  payload JSON NOT NULL,
  reason TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
