CREATE SCHEMA IF NOT EXISTS service_ticketing;

CREATE TABLE service_ticketing_support_ticket (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  ticket_id VARCHAR(255) NOT NULL UNIQUE,
  customer_id VARCHAR(255) NOT NULL,
  subject VARCHAR(500) NOT NULL,
  description TEXT NOT NULL,
  channel VARCHAR(80) NOT NULL,
  priority VARCHAR(80) NOT NULL,
  region VARCHAR(80) NOT NULL,
  queue VARCHAR(120) NOT NULL,
  assignment_id VARCHAR(255),
  sla_policy_id VARCHAR(255) NOT NULL,
  status VARCHAR(80) NOT NULL,
  breach_risk NUMERIC(10,4) NOT NULL,
  next_best_response TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_service_queue (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  queue_id VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  assignment_mode VARCHAR(120) NOT NULL,
  service_tier VARCHAR(120) NOT NULL,
  default_owner VARCHAR(255),
  workbench_limit INTEGER NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_sla_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  sla_policy_id VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  priority VARCHAR(80) NOT NULL,
  first_response_minutes INTEGER NOT NULL,
  resolution_target_hours INTEGER NOT NULL,
  status VARCHAR(80) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_service_priority (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  priority_id VARCHAR(255) NOT NULL UNIQUE,
  display_order INTEGER NOT NULL,
  severity_score NUMERIC(10,4) NOT NULL,
  default_response_minutes INTEGER NOT NULL,
  default_resolution_hours INTEGER NOT NULL,
  status VARCHAR(80) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_case_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assignment_id VARCHAR(255) NOT NULL UNIQUE,
  ticket_id VARCHAR(255) NOT NULL,
  owner VARCHAR(255) NOT NULL,
  queue VARCHAR(120) NOT NULL,
  skills TEXT NOT NULL,
  assignment_score NUMERIC(10,4) NOT NULL,
  status VARCHAR(80) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ticket_id) REFERENCES service_ticketing_support_ticket(ticket_id)
);

CREATE TABLE service_ticketing_escalation_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  escalation_id VARCHAR(255) NOT NULL UNIQUE,
  ticket_id VARCHAR(255) NOT NULL,
  reason TEXT NOT NULL,
  breach_risk NUMERIC(10,4) NOT NULL,
  queue VARCHAR(120) NOT NULL,
  status VARCHAR(80) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ticket_id) REFERENCES service_ticketing_support_ticket(ticket_id)
);

CREATE TABLE service_ticketing_ticket_interaction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  interaction_id VARCHAR(255) NOT NULL UNIQUE,
  ticket_id VARCHAR(255) NOT NULL,
  interaction_type VARCHAR(120) NOT NULL,
  channel VARCHAR(80) NOT NULL,
  actor VARCHAR(255) NOT NULL,
  summary TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ticket_id) REFERENCES service_ticketing_support_ticket(ticket_id)
);

CREATE TABLE service_ticketing_knowledge_suggestion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  suggestion_id VARCHAR(255) NOT NULL UNIQUE,
  ticket_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  source VARCHAR(120) NOT NULL,
  article_ref VARCHAR(500) NOT NULL,
  recommendation TEXT NOT NULL,
  confidence NUMERIC(10,4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_entitlement_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL UNIQUE,
  customer_id VARCHAR(255) NOT NULL,
  tier VARCHAR(120) NOT NULL,
  entitlements TEXT NOT NULL,
  coverage_status VARCHAR(120) NOT NULL,
  source_event VARCHAR(255),
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_case_lifecycle_state (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  ticket_id VARCHAR(255) NOT NULL UNIQUE,
  stage VARCHAR(120) NOT NULL,
  status VARCHAR(80) NOT NULL,
  history TEXT NOT NULL,
  current_owner VARCHAR(255),
  current_queue VARCHAR(120),
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (ticket_id) REFERENCES service_ticketing_support_ticket(ticket_id)
);

CREATE TABLE service_ticketing_field_service_handoff (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  handoff_id VARCHAR(255) NOT NULL UNIQUE,
  ticket_id VARCHAR(255) NOT NULL,
  assignment_id VARCHAR(255),
  handoff_reason TEXT NOT NULL,
  target_team VARCHAR(255) NOT NULL,
  status VARCHAR(80) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_customer_update (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  update_id VARCHAR(255) NOT NULL UNIQUE,
  ticket_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  update_type VARCHAR(120) NOT NULL,
  delivery_channel VARCHAR(80) NOT NULL,
  message TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_resolution_record (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  resolution_id VARCHAR(255) NOT NULL UNIQUE,
  ticket_id VARCHAR(255) NOT NULL,
  resolution TEXT NOT NULL,
  resolved_by VARCHAR(255) NOT NULL,
  resolution_code VARCHAR(120) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_csat_response (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  survey_id VARCHAR(255) NOT NULL UNIQUE,
  ticket_id VARCHAR(255) NOT NULL,
  customer_id VARCHAR(255) NOT NULL,
  status VARCHAR(80) NOT NULL,
  sent_at TIMESTAMP NOT NULL,
  score NUMERIC(10,4),
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_ticket_audit_log (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  audit_id VARCHAR(255) NOT NULL UNIQUE,
  entity_table VARCHAR(255) NOT NULL,
  entity_id VARCHAR(255) NOT NULL,
  action VARCHAR(120) NOT NULL,
  payload_digest VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_automation_insight (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  insight_id VARCHAR(255) NOT NULL UNIQUE,
  ticket_id VARCHAR(255) NOT NULL,
  insight_type VARCHAR(120) NOT NULL,
  score NUMERIC(10,4) NOT NULL,
  recommended_action TEXT NOT NULL,
  explanation TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_service_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL UNIQUE,
  scope VARCHAR(120) NOT NULL,
  status VARCHAR(80) NOT NULL,
  allowed_regions TEXT NOT NULL,
  allowed_channels TEXT NOT NULL,
  allowed_priorities TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_service_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL UNIQUE,
  parameter_value TEXT NOT NULL,
  bounds TEXT NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_service_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL UNIQUE,
  database_backend VARCHAR(80) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  event_contract VARCHAR(80) NOT NULL,
  assignment_mode VARCHAR(80) NOT NULL,
  default_region VARCHAR(80) NOT NULL,
  default_timezone VARCHAR(80) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE service_ticketing_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  retry_count INTEGER NOT NULL,
  status VARCHAR(80) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE service_ticketing_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  retry_count INTEGER NOT NULL,
  status VARCHAR(80) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE service_ticketing_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  reason TEXT NOT NULL,
  retry_count INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL
);
