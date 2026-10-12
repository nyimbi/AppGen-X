CREATE SCHEMA IF NOT EXISTS education_student_lifecycle;

CREATE TABLE education_student_lifecycle_student_applicant (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  student_applicant_id VARCHAR(255) NOT NULL,
  applicant_number VARCHAR(255) NOT NULL,
  application_round VARCHAR(255) NOT NULL,
  program_choice VARCHAR(255) NOT NULL,
  intake_term VARCHAR(255) NOT NULL,
  applicant_type VARCHAR(255) NOT NULL,
  residency_status VARCHAR(255) NOT NULL,
  prior_credential VARCHAR(255) NOT NULL,
  required_documents VARCHAR(255) NOT NULL,
  document_review_status VARCHAR(255) NOT NULL,
  decision_status VARCHAR(255) NOT NULL,
  offer_conditions VARCHAR(255) NOT NULL,
  acceptance_deadline TIMESTAMP,
  withdrawal_reason VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
,
  UNIQUE (student_applicant_id));

CREATE TABLE education_student_lifecycle_enrollment (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  enrollment_id VARCHAR(255) NOT NULL,
  student_applicant_id VARCHAR(255) NOT NULL,
  program_code VARCHAR(255) NOT NULL,
  campus_code VARCHAR(255) NOT NULL,
  modality VARCHAR(255) NOT NULL,
  credit_load DECIMAL(18, 4) NOT NULL,
  cohort_code VARCHAR(255) NOT NULL,
  catalog_year VARCHAR(255) NOT NULL,
  status_reason VARCHAR(255),
  effective_date TIMESTAMP NOT NULL,
  readmission_link VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (student_applicant_id) REFERENCES education_student_lifecycle_student_applicant(student_applicant_id)
,
  UNIQUE (enrollment_id));

CREATE TABLE education_student_lifecycle_curriculum_plan (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  curriculum_plan_id VARCHAR(255) NOT NULL,
  student_applicant_id VARCHAR(255) NOT NULL,
  program_code VARCHAR(255) NOT NULL,
  concentration VARCHAR(255) NOT NULL,
  catalog_year VARCHAR(255) NOT NULL,
  plan_version VARCHAR(255) NOT NULL,
  requirement_groups VARCHAR(255) NOT NULL,
  elective_rule VARCHAR(255) NOT NULL,
  prerequisites VARCHAR(255) NOT NULL,
  substitution_rule VARCHAR(255) NOT NULL,
  waiver_rule VARCHAR(255) NOT NULL,
  approval_state VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (student_applicant_id) REFERENCES education_student_lifecycle_student_applicant(student_applicant_id)
);

CREATE TABLE education_student_lifecycle_advising_case (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  advising_case_id VARCHAR(255) NOT NULL,
  student_applicant_id VARCHAR(255) NOT NULL,
  case_type VARCHAR(255) NOT NULL,
  urgency VARCHAR(255) NOT NULL,
  case_owner VARCHAR(255) NOT NULL,
  student_goal VARCHAR(255) NOT NULL,
  barrier VARCHAR(255) NOT NULL,
  action_plan TEXT NOT NULL,
  risk_score DECIMAL(18, 4) NOT NULL,
  next_contact_at TIMESTAMP,
  closure_evidence VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (student_applicant_id) REFERENCES education_student_lifecycle_student_applicant(student_applicant_id)
);

CREATE TABLE education_student_lifecycle_course_attempt (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  course_attempt_id VARCHAR(255) NOT NULL,
  enrollment_id VARCHAR(255) NOT NULL,
  section_code VARCHAR(255) NOT NULL,
  grade_mode VARCHAR(255) NOT NULL,
  attempt_number INTEGER NOT NULL,
  repeat_rule VARCHAR(255) NOT NULL,
  grade_points DECIMAL(18, 4) NOT NULL,
  attempted_credits DECIMAL(18, 4) NOT NULL,
  earned_credits DECIMAL(18, 4) NOT NULL,
  transcript_visible BOOLEAN NOT NULL,
  withdrawal_date TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (enrollment_id) REFERENCES education_student_lifecycle_enrollment(enrollment_id)
,
  UNIQUE (course_attempt_id));

CREATE TABLE education_student_lifecycle_assessment_result (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assessment_result_id VARCHAR(255) NOT NULL,
  course_attempt_id VARCHAR(255) NOT NULL,
  assessment_type VARCHAR(255) NOT NULL,
  rubric_code VARCHAR(255) NOT NULL,
  scorer VARCHAR(255) NOT NULL,
  score DECIMAL(18, 4) NOT NULL,
  competency_code VARCHAR(255) NOT NULL,
  moderation_status VARCHAR(255) NOT NULL,
  appeal_state VARCHAR(255) NOT NULL,
  finalized BOOLEAN NOT NULL,
  finalized_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (course_attempt_id) REFERENCES education_student_lifecycle_course_attempt(course_attempt_id)
);

CREATE TABLE education_student_lifecycle_credential (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  credential_id VARCHAR(255) NOT NULL,
  student_applicant_id VARCHAR(255) NOT NULL,
  credential_type VARCHAR(255) NOT NULL,
  audit_status VARCHAR(255) NOT NULL,
  approver VARCHAR(255) NOT NULL,
  conferral_date TIMESTAMP,
  honors VARCHAR(255),
  certificate_number VARCHAR(255),
  correction_reason VARCHAR(255),
  revocation_reason VARCHAR(255),
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL,
  FOREIGN KEY (student_applicant_id) REFERENCES education_student_lifecycle_student_applicant(student_applicant_id)
);

CREATE TABLE education_student_lifecycle_policy_rule (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  rule_id VARCHAR(255) NOT NULL,
  rule_name VARCHAR(255) NOT NULL,
  predicate_text TEXT NOT NULL,
  ambiguity_flag BOOLEAN NOT NULL,
  approver_role VARCHAR(255) NOT NULL,
  effective_from TIMESTAMP,
  effective_to TIMESTAMP,
  compiled_hash VARCHAR(255) NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE education_student_lifecycle_runtime_parameter (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  parameter_name VARCHAR(255) NOT NULL,
  parameter_value VARCHAR(255) NOT NULL,
  scope VARCHAR(255) NOT NULL,
  bounded BOOLEAN NOT NULL,
  effective_from TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE education_student_lifecycle_schema_extension (
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

CREATE TABLE education_student_lifecycle_control_assertion (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  assertion_id VARCHAR(255) NOT NULL,
  control_name VARCHAR(255) NOT NULL,
  assertion_result VARCHAR(255) NOT NULL,
  severity VARCHAR(255) NOT NULL,
  remediation_task VARCHAR(255) NOT NULL,
  evaluated_at TIMESTAMP NOT NULL,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE education_student_lifecycle_governed_model (
  id INTEGER PRIMARY KEY NOT NULL,
  tenant VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  model_name VARCHAR(255) NOT NULL,
  model_version VARCHAR(255) NOT NULL,
  governance_state VARCHAR(255) NOT NULL,
  approved_by VARCHAR(255) NOT NULL,
  approved_at TIMESTAMP,
  status VARCHAR(255) NOT NULL,
  version INTEGER NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE education_student_lifecycle_appgen_outbox_event (
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

CREATE TABLE education_student_lifecycle_appgen_inbox_event (
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

CREATE TABLE education_student_lifecycle_appgen_dead_letter_event (
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
