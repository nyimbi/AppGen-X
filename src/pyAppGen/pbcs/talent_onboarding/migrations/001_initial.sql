CREATE SCHEMA IF NOT EXISTS talent_onboarding;

CREATE TABLE talent_onboarding_job_requisition (
  id INTEGER PRIMARY KEY NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE talent_onboarding_job_requisition_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_job_requisition_budget (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_job_requisition_skill (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_sourcing_campaign (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_candidate_source (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_candidate (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_candidate_consent (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_candidate_profile (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_candidate_skill (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_candidate_stage_history (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_candidate_duplicate_check (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_candidate_privacy_request (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_interview_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_interview_panel (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_interview_schedule (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_interview_feedback (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_evaluation_evidence (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_candidate_scorecard (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_background_check (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_background_check_package (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_background_check_adjudication (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_adverse_action_notice (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_offer (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_offer_approval (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_offer_acceptance (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_compensation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_onboarding_task (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_onboarding_task_template (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_onboarding_checklist (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_equipment_request (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_access_preload_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_welcome_notification_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_personnel_identity_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_payroll_worker_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_role_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_policy_screening (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_audit_trace (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_candidate_proof (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_federation_projection (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_carbon_schedule_window (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_pipeline_optimization (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_interview_allocation (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_anomaly_signal (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_candidate_risk_model (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_hiring_forecast (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_parsed_instruction (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_seed_data (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_configuration (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_onboarding_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_onboarding_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_talent_onboarding_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  job_requisition_id INTEGER NOT NULL,
  code VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (job_requisition_id) REFERENCES talent_onboarding_job_requisition(id)
);

CREATE TABLE talent_onboarding_appgen_outbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE talent_onboarding_appgen_inbox_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);

CREATE TABLE talent_onboarding_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  processed_at TIMESTAMP
);
