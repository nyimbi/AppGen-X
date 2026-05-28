CREATE SCHEMA IF NOT EXISTS talent_onboarding;

CREATE TABLE talent_onboarding_job_requisition (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  requisition_id VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  department VARCHAR(255) NOT NULL,
  manager_employee_id VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  location VARCHAR(255) NOT NULL,
  headcount VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_job_requisition_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  approval_id VARCHAR(255) NOT NULL,
  requisition_id VARCHAR(255) NOT NULL,
  approver VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  decided_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_job_requisition_budget (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  budget_id VARCHAR(255) NOT NULL,
  requisition_id VARCHAR(255) NOT NULL,
  budget VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  approved_amount DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_job_requisition_skill (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  skill_id VARCHAR(255) NOT NULL,
  requisition_id VARCHAR(255) NOT NULL,
  skill VARCHAR(255) NOT NULL,
  required_level VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_sourcing_campaign (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  campaign_id VARCHAR(255) NOT NULL,
  requisition_id VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  budget VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_candidate_source (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  referrer VARCHAR(255) NOT NULL,
  campaign_id VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_candidate (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  requisition_id VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  source VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  match_score DECIMAL(18, 4) NOT NULL,
  stage VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  identity_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_candidate_consent (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  consent_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  consent_type VARCHAR(255) NOT NULL,
  granted_at TIMESTAMP NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_candidate_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  profile_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  profile_hash VARCHAR(255) NOT NULL,
  portfolio_ref VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_candidate_skill (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  candidate_skill_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  skill VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_candidate_stage_history (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  history_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  from_stage VARCHAR(255) NOT NULL,
  to_stage VARCHAR(255) NOT NULL,
  actor VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_candidate_duplicate_check (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  duplicate_check_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  match_candidate_id VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_candidate_privacy_request (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  privacy_request_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  request_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  completed_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_interview_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  requisition_id VARCHAR(255) NOT NULL,
  panel_size VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_interview_panel (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  panel_id VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  interviewer_employee_id VARCHAR(255) NOT NULL,
  role VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_interview_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  schedule_id VARCHAR(255) NOT NULL,
  plan_id VARCHAR(255) NOT NULL,
  scheduled_at TIMESTAMP NOT NULL,
  timezone VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_interview_feedback (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  feedback_id VARCHAR(255) NOT NULL,
  schedule_id VARCHAR(255) NOT NULL,
  interviewer VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  recommendation VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_evaluation_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  evidence_id TEXT NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  evidence_type TEXT NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  evidence_hash TEXT NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_candidate_scorecard (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  scorecard_id DECIMAL(18, 4) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  weighted_score DECIMAL(18, 4) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_background_check (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  check_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  provider VARCHAR(255) NOT NULL,
  check_type VARCHAR(255) NOT NULL,
  confidence DECIMAL(18, 4) NOT NULL,
  result VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_background_check_package (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  package_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  provider VARCHAR(255) NOT NULL,
  package_type VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_background_check_adjudication (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  adjudication_id VARCHAR(255) NOT NULL,
  check_id VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  adjudicator VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_adverse_action_notice (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  notice_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  check_id VARCHAR(255) NOT NULL,
  notice_type VARCHAR(255) NOT NULL,
  sent_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_offer (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  offer_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  salary VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  start_date TIMESTAMP NOT NULL,
  expires_in_days VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_offer_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  approval_id VARCHAR(255) NOT NULL,
  offer_id VARCHAR(255) NOT NULL,
  approver VARCHAR(255) NOT NULL,
  decision VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_offer_acceptance (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  acceptance_id VARCHAR(255) NOT NULL,
  offer_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  accepted_by VARCHAR(255) NOT NULL,
  accepted_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_compensation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  projection_id VARCHAR(255) NOT NULL,
  offer_id VARCHAR(255) NOT NULL,
  salary VARCHAR(255) NOT NULL,
  currency VARCHAR(255) NOT NULL,
  pay_group_id VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_onboarding_task (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  task_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  task_type VARCHAR(255) NOT NULL,
  assignee VARCHAR(255) NOT NULL,
  due_in_days VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_onboarding_task_template (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  template_id VARCHAR(255) NOT NULL,
  task_type VARCHAR(255) NOT NULL,
  role_id VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  sla_days VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_onboarding_checklist (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  checklist_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  completion_percent VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_equipment_request (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  request_id VARCHAR(255) NOT NULL,
  candidate_id VARCHAR(255) NOT NULL,
  equipment_type VARCHAR(255) NOT NULL,
  fulfillment_status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_access_preload_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_welcome_notification_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_personnel_identity_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_payroll_worker_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_role_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_candidate_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_carbon_schedule_window (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_pipeline_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_interview_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_candidate_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_hiring_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_parsed_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  source_id VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  effective_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  compiled_hash VARCHAR(255) NOT NULL,
  enabled VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_talent_parameter (
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

CREATE TABLE talent_onboarding_talent_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  configuration_id VARCHAR(255) NOT NULL,
  database_backend VARCHAR(255) NOT NULL,
  event_topic VARCHAR(255) NOT NULL,
  event_contract VARCHAR(255) NOT NULL,
  stream_engine_picker_visible VARCHAR(255) NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_appgen_outbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  published_at TIMESTAMP NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_appgen_inbox_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_dead_letter_event (
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) PRIMARY KEY NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  audit_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
