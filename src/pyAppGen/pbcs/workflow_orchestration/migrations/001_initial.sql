CREATE SCHEMA IF NOT EXISTS workflow_orchestration;

CREATE TABLE workflow_orchestration_workflow_definition (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  owner_pbc VARCHAR(255) NOT NULL,
  semantic_version VARCHAR(255) NOT NULL,
  states VARCHAR(255) NOT NULL,
  transitions VARCHAR(255) NOT NULL,
  participants VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_version (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  version_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  semantic_version VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_instance (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  correlation_id VARCHAR(255) NOT NULL,
  current_state VARCHAR(255) NOT NULL,
  context_payload TEXT NOT NULL,
  history VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  signal_id VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  signal VARCHAR(255) NOT NULL,
  source_pbc VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  accepted VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_transition_guard (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  guard_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  from_state VARCHAR(255) NOT NULL,
  signal VARCHAR(255) NOT NULL,
  expression VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_timer_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  timer_id VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  deadline_seconds VARCHAR(255) NOT NULL,
  breach_risk VARCHAR(255) NOT NULL,
  retry_budget VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_retry_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  max_attempts VARCHAR(255) NOT NULL,
  backoff VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_sla_policy (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  policy_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  threshold_seconds DECIMAL(18, 4) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_escalation_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  escalation_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  trigger VARCHAR(255) NOT NULL,
  target_group VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_saga_step (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  step_id VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  participant_pbc VARCHAR(255) NOT NULL,
  command VARCHAR(255) NOT NULL,
  duration_ms VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_compensation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  compensation_id VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  step_id VARCHAR(255) NOT NULL,
  command VARCHAR(255) NOT NULL,
  reason VARCHAR(255) NOT NULL,
  side_effect_boundary VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_human_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  task_id VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  task_type VARCHAR(255) NOT NULL,
  assignee_group VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  sla_due_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_human_task_assignment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assignment_id VARCHAR(255) NOT NULL,
  task_id VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  assignee_group VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_approval_decision (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  decision_id VARCHAR(255) NOT NULL,
  task_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  decided_by VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_integration_endpoint (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  endpoint_id VARCHAR(255) NOT NULL,
  participant_pbc VARCHAR(255) NOT NULL,
  route VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_event_correlation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  correlation_id VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  source_event VARCHAR(255) NOT NULL,
  business_key VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_metric_snapshot (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  snapshot_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  instance_count INTEGER NOT NULL,
  completed_count INTEGER NOT NULL,
  compensation_count INTEGER NOT NULL,
  completion_rate DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_exception_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  case_id VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  case_type VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  recommended_action VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_simulation_run (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  simulation_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  scenario VARCHAR(255) NOT NULL,
  risk_delta VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  screening_id VARCHAR(255) NOT NULL,
  workflow_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_completion_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  proof_id VARCHAR(255) NOT NULL,
  instance_id VARCHAR(255) NOT NULL,
  proof_hash VARCHAR(255) NOT NULL,
  proof_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_audit_entry (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  audit_entry_id VARCHAR(255) NOT NULL,
  action VARCHAR(255) NOT NULL,
  payload_hash TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_governed_model_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  evidence_id TEXT NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  auc VARCHAR(255) NOT NULL,
  drift_score DECIMAL(18, 4) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  trigger VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  enabled VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  changed_by VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE workflow_orchestration_workflow_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  event_contract VARCHAR(255) NOT NULL,
  stream_engine_picker_visible VARCHAR(255) NOT NULL,
  default_timezone VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
