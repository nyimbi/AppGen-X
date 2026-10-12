CREATE SCHEMA IF NOT EXISTS research_grants_management;

CREATE TABLE research_grants_management_grant_proposal (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  grant_proposal_id VARCHAR(255) NOT NULL,
  opportunity_reference VARCHAR(255),
  sponsor_program_code VARCHAR(255) NOT NULL,
  notice_version VARCHAR(255),
  proposal_type VARCHAR(255) NOT NULL,
  principal_investigator VARCHAR(255) NOT NULL,
  department VARCHAR(255) NOT NULL,
  sponsor_deadline TIMESTAMP,
  internal_routing_deadline TIMESTAMP,
  submission_state VARCHAR(255) NOT NULL,
  required_section_count INTEGER NOT NULL,
  approved_section_count INTEGER NOT NULL,
  compliance_matrix_state VARCHAR(255) NOT NULL,
  cost_share_required BOOLEAN NOT NULL,
  cost_share_amount DECIMAL(18, 4) NOT NULL,
  total_budget_requested DECIMAL(18, 4) NOT NULL,
  budget_currency VARCHAR(255) NOT NULL,
  routing_state VARCHAR(255) NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  proposal_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (grant_proposal_id));

CREATE TABLE research_grants_management_research_award (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  research_award_id VARCHAR(255) NOT NULL,
  grant_proposal_id VARCHAR(255),
  sponsor_name VARCHAR(255) NOT NULL,
  award_number VARCHAR(255) NOT NULL,
  award_type VARCHAR(255) NOT NULL,
  project_period_start TIMESTAMP NOT NULL,
  project_period_end TIMESTAMP NOT NULL,
  award_amount DECIMAL(18, 4) NOT NULL,
  obligated_amount DECIMAL(18, 4) NOT NULL,
  award_currency VARCHAR(255) NOT NULL,
  amendment_count INTEGER NOT NULL,
  readiness_state VARCHAR(255) NOT NULL,
  pre_award_spending_approved BOOLEAN NOT NULL,
  compliance_dependency_count INTEGER NOT NULL,
  closeout_readiness_score DECIMAL(18, 4) NOT NULL,
  award_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (grant_proposal_id) REFERENCES research_grants_management_grant_proposal(grant_proposal_id)
,
  UNIQUE (research_award_id));

CREATE TABLE research_grants_management_sponsor_budget (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  sponsor_budget_id VARCHAR(255) NOT NULL,
  research_award_id VARCHAR(255) NOT NULL,
  template_version VARCHAR(255) NOT NULL,
  budget_period_number INTEGER NOT NULL,
  budget_category VARCHAR(255) NOT NULL,
  budgeted_amount DECIMAL(18, 4) NOT NULL,
  committed_amount DECIMAL(18, 4) NOT NULL,
  actual_amount DECIMAL(18, 4) NOT NULL,
  indirect_cost_rate DECIMAL(18, 4) NOT NULL,
  cost_share_amount DECIMAL(18, 4) NOT NULL,
  rebudget_pending BOOLEAN NOT NULL,
  prior_approval_required BOOLEAN NOT NULL,
  budget_currency VARCHAR(255) NOT NULL,
  budget_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (research_award_id) REFERENCES research_grants_management_research_award(research_award_id)
);

CREATE TABLE research_grants_management_compliance_requirement (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  compliance_requirement_id VARCHAR(255) NOT NULL,
  research_award_id VARCHAR(255) NOT NULL,
  requirement_type VARCHAR(255) NOT NULL,
  obligation_source VARCHAR(255) NOT NULL,
  due_date TIMESTAMP NOT NULL,
  gating_effect VARCHAR(255) NOT NULL,
  ethics_boundary_state VARCHAR(255) NOT NULL,
  protocol_status_source VARCHAR(255),
  expiration_date TIMESTAMP,
  responsible_role VARCHAR(255) NOT NULL,
  resolved_at TIMESTAMP,
  compliance_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (research_award_id) REFERENCES research_grants_management_research_award(research_award_id)
);

CREATE TABLE research_grants_management_subaward (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  subaward_id VARCHAR(255) NOT NULL,
  research_award_id VARCHAR(255) NOT NULL,
  subrecipient_name VARCHAR(255) NOT NULL,
  subrecipient_identifier VARCHAR(255) NOT NULL,
  risk_tier VARCHAR(255) NOT NULL,
  scope_of_work TEXT NOT NULL,
  subaward_amount DECIMAL(18, 4) NOT NULL,
  indirect_cost_treatment VARCHAR(255) NOT NULL,
  issuance_state VARCHAR(255) NOT NULL,
  monitoring_cadence VARCHAR(255) NOT NULL,
  audit_status VARCHAR(255),
  foreign_subrecipient BOOLEAN NOT NULL,
  monitoring_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (research_award_id) REFERENCES research_grants_management_research_award(research_award_id)
);

CREATE TABLE research_grants_management_milestone_report (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  milestone_report_id VARCHAR(255) NOT NULL,
  research_award_id VARCHAR(255) NOT NULL,
  deliverable_name VARCHAR(255) NOT NULL,
  report_type VARCHAR(255) NOT NULL,
  reporting_period VARCHAR(255) NOT NULL,
  due_date TIMESTAMP NOT NULL,
  submitted_at TIMESTAMP,
  predecessor_deliverable_id VARCHAR(255),
  report_state VARCHAR(255) NOT NULL,
  progress_percent DECIMAL(18, 4) NOT NULL,
  sponsor_acceptance_state VARCHAR(255) NOT NULL,
  report_notes TEXT,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (research_award_id) REFERENCES research_grants_management_research_award(research_award_id)
);

CREATE TABLE research_grants_management_effort_certification (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  effort_certification_id VARCHAR(255) NOT NULL,
  research_award_id VARCHAR(255) NOT NULL,
  certifier_name VARCHAR(255) NOT NULL,
  certification_period VARCHAR(255) NOT NULL,
  committed_effort_percent DECIMAL(18, 4) NOT NULL,
  certified_effort_percent DECIMAL(18, 4) NOT NULL,
  salary_cap_amount DECIMAL(18, 4) NOT NULL,
  certification_state VARCHAR(255) NOT NULL,
  overdue_flag BOOLEAN NOT NULL,
  exception_reason TEXT,
  certified_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (research_award_id) REFERENCES research_grants_management_research_award(research_award_id)
);

CREATE TABLE research_grants_management_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  example_text TEXT,
  approver_role VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE research_grants_management_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE research_grants_management_schema_extension (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  extension_id VARCHAR(255) NOT NULL,
  target_table VARCHAR(255) NOT NULL,
  field_name VARCHAR(255) NOT NULL,
  field_type VARCHAR(255) NOT NULL,
  registered_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE research_grants_management_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  remediation_task VARCHAR(255),
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE research_grants_management_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  model_type VARCHAR(255) NOT NULL,
  coverage_scope VARCHAR(255) NOT NULL,
  backtest_exception_count INTEGER NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255),
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE research_grants_management_appgen_outbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE research_grants_management_appgen_inbox_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  idempotency_key VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE research_grants_management_appgen_dead_letter_event (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  event_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  topic VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  reason VARCHAR(255) NOT NULL,
  attempts INTEGER NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
