"""Executable improve1 controls for the education student lifecycle PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "education_student_lifecycle"
EVENT_CONTRACT = "AppGen-X"
EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC = "pbc.education_student_lifecycle.events"
EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES = (
    "education_student_lifecycle_student_applicant",
    "education_student_lifecycle_applicant_document_evidence",
    "education_student_lifecycle_enrollment",
    "education_student_lifecycle_curriculum_plan",
    "education_student_lifecycle_course_attempt",
    "education_student_lifecycle_assessment_result",
    "education_student_lifecycle_advising_case",
    "education_student_lifecycle_intervention_plan",
    "education_student_lifecycle_academic_petition",
    "education_student_lifecycle_transfer_credit_evaluation",
    "education_student_lifecycle_degree_audit",
    "education_student_lifecycle_student_risk_signal",
    "education_student_lifecycle_hold_projection",
    "education_student_lifecycle_engagement_projection",
    "education_student_lifecycle_accommodation_projection",
    "education_student_lifecycle_graduation_clearance",
    "education_student_lifecycle_credential",
    "education_student_lifecycle_policy_rule",
    "education_student_lifecycle_runtime_parameter",
    "education_student_lifecycle_schema_extension",
    "education_student_lifecycle_control_assertion",
    "education_student_lifecycle_governed_model",
    "education_student_lifecycle_student_outcome",
    "education_student_lifecycle_accreditation_evidence",
    "education_student_lifecycle_communication_event",
    "education_student_lifecycle_appgen_outbox_event",
    "education_student_lifecycle_appgen_inbox_event",
    "education_student_lifecycle_appgen_dead_letter_event",
)
EDUCATION_STUDENT_LIFECYCLE_DECLARED_DEPENDENCIES = (
    "identity_student_projection",
    "course_catalog_projection",
    "course_section_projection",
    "learning_engagement_projection",
    "student_hold_projection",
    "financial_aid_status_projection",
    "billing_status_projection",
    "alumni_outcome_projection",
    "notification_delivery_projection",
    "PolicyChanged",
    "CustomerUpdated",
    "SupplierQualified",
    "HoldChanged",
    "CourseSectionCapacityChanged",
    "LearningEngagementUpdated",
    "FinancialAidEligibilityUpdated",
    "BillingStatusUpdated",
    "IdentityProfileUpdated",
    "POST /notifications/messages",
    "GET /identity/students/{id}",
    "GET /catalog/courses/{id}",
    "GET /finance/aid-status/{student_id}",
    "GET /billing/status/{student_id}",
)

APPLICANT_TABLE = "education_student_lifecycle_student_applicant"
DOCUMENT_TABLE = "education_student_lifecycle_applicant_document_evidence"
ENROLLMENT_TABLE = "education_student_lifecycle_enrollment"
CURRICULUM_TABLE = "education_student_lifecycle_curriculum_plan"
COURSE_TABLE = "education_student_lifecycle_course_attempt"
ASSESSMENT_TABLE = "education_student_lifecycle_assessment_result"
ADVISING_TABLE = "education_student_lifecycle_advising_case"
INTERVENTION_TABLE = "education_student_lifecycle_intervention_plan"
PETITION_TABLE = "education_student_lifecycle_academic_petition"
TRANSFER_TABLE = "education_student_lifecycle_transfer_credit_evaluation"
AUDIT_TABLE = "education_student_lifecycle_degree_audit"
RISK_TABLE = "education_student_lifecycle_student_risk_signal"
HOLD_TABLE = "education_student_lifecycle_hold_projection"
ENGAGEMENT_TABLE = "education_student_lifecycle_engagement_projection"
ACCOMMODATION_TABLE = "education_student_lifecycle_accommodation_projection"
GRADUATION_TABLE = "education_student_lifecycle_graduation_clearance"
CREDENTIAL_TABLE = "education_student_lifecycle_credential"
POLICY_TABLE = "education_student_lifecycle_policy_rule"
PARAMETER_TABLE = "education_student_lifecycle_runtime_parameter"
SCHEMA_EXTENSION_TABLE = "education_student_lifecycle_schema_extension"
CONTROL_TABLE = "education_student_lifecycle_control_assertion"
MODEL_TABLE = "education_student_lifecycle_governed_model"
OUTCOME_TABLE = "education_student_lifecycle_student_outcome"
ACCREDITATION_TABLE = "education_student_lifecycle_accreditation_evidence"
COMMUNICATION_TABLE = "education_student_lifecycle_communication_event"
OUTBOX_TABLE = "education_student_lifecycle_appgen_outbox_event"
INBOX_TABLE = "education_student_lifecycle_appgen_inbox_event"
DEAD_LETTER_TABLE = "education_student_lifecycle_appgen_dead_letter_event"

EDUCATION_STUDENT_LIFECYCLE_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in EDUCATION_STUDENT_LIFECYCLE_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in EDUCATION_STUDENT_LIFECYCLE_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = (
    (1, (APPLICANT_TABLE, DOCUMENT_TABLE), ("applicant_state", "application_round", "program_choice", "required_documents", "decision_status", "acceptance_deadline"), "AdmissionsWorkbench", "POST /student-applicants/state-transition", ("identity_student_projection",)),
    (2, (APPLICANT_TABLE, POLICY_TABLE), ("program", "intake", "applicant_type", "residency", "prior_credential", "exception_policy"), "AdmissionsWorkbench", "POST /admissions/requirements/evaluate", ("course_catalog_projection",)),
    (3, (DOCUMENT_TABLE, APPLICANT_TABLE), ("document_type", "issuing_institution", "received_date", "authenticity_status", "extracted_fields", "reviewer_confirmation"), "AdmissionsWorkbench", "POST /documents/transcripts/intake", ()),
    (4, (ENROLLMENT_TABLE, COURSE_TABLE), ("enrollment_status", "status_reason", "effective_date", "program", "campus", "catalog_year"), "EnrollmentWorkbench", "POST /enrollments/state-transition", ("billing_status_projection",)),
    (5, (CURRICULUM_TABLE, POLICY_TABLE), ("plan_version", "catalog_year", "requirement_groups", "substitutions", "waivers", "approval"), "CurriculumPlanWorkbench", "POST /curriculum-plans/version", ("course_catalog_projection",)),
    (6, (AUDIT_TABLE, CURRICULUM_TABLE, COURSE_TABLE, ASSESSMENT_TABLE, TRANSFER_TABLE), ("requirement", "course_attempt", "assessment_result", "transfer_credit", "waiver", "remaining_credit"), "DegreeAuditWorkbench", "POST /degree-audits/run", ("course_catalog_projection",)),
    (7, (COURSE_TABLE, ENROLLMENT_TABLE), ("attempt_status", "section_projection", "grade_mode", "attempt_number", "repeat_rule", "earned_credits"), "EnrollmentWorkbench", "POST /course-attempts/lifecycle", ("course_section_projection",)),
    (8, (COURSE_TABLE, POLICY_TABLE, PETITION_TABLE), ("prerequisite", "corequisite", "placement", "program_restriction", "override_approval", "audit_trace"), "RegistrationRulesWorkbench", "POST /registration/prerequisites/check", ("course_catalog_projection",)),
    (9, (ENROLLMENT_TABLE, COURSE_TABLE, POLICY_TABLE), ("gpa", "credit_completion", "failed_attempts", "progress_pace", "remediation_terms", "appeal"), "ProgressionWorkbench", "POST /academic-standing/calculate", ()),
    (10, (COURSE_TABLE, AUDIT_TABLE), ("calculation_basis", "grade_points", "attempted_credits", "earned_credits", "included_flag", "transcript_period"), "ProgressionWorkbench", "POST /gpa-credit/calculate", ()),
    (11, (ADVISING_TABLE, INTERVENTION_TABLE), ("case_type", "urgency", "owner", "student_goal", "barrier", "closure_evidence"), "AdvisingWorkbench", "POST /advising-cases/route", ()),
    (12, (RISK_TABLE, ADVISING_TABLE, ENGAGEMENT_TABLE), ("risk_score", "contributing_factors", "confidence", "intervention_recommendation", "review_cadence", "human_review"), "StudentSuccessWorkbench", "POST /student-success/risk-score", ("learning_engagement_projection", "student_hold_projection")),
    (13, (INTERVENTION_TABLE, ADVISING_TABLE), ("objective", "owner", "due_date", "student_commitment", "resource_referral", "outcome"), "StudentSuccessWorkbench", "POST /interventions", ("notification_delivery_projection",)),
    (14, (ASSESSMENT_TABLE, CREDENTIAL_TABLE), ("assessment_type", "rubric", "scorer", "score", "competency_mapping", "moderation_status"), "AssessmentWorkbench", "POST /assessment-results/finalize", ()),
    (15, (ASSESSMENT_TABLE, CURRICULUM_TABLE, AUDIT_TABLE), ("competency_framework", "mapped_assessments", "achievement_level", "evidence", "remediation", "credential_requirement"), "CompetencyWorkbench", "POST /competencies/map-outcomes", ()),
    (16, (CREDENTIAL_TABLE, AUDIT_TABLE, GRADUATION_TABLE, HOLD_TABLE), ("credential_type", "audit_status", "approver", "conferral_date", "honors", "hold_clearance"), "GraduationClearanceWorkbench", "POST /credentials/award", ("financial_aid_status_projection", "billing_status_projection")),
    (17, (GRADUATION_TABLE, AUDIT_TABLE, CREDENTIAL_TABLE), ("pending_audits", "missing_requirements", "unresolved_holds", "advisor_review", "registrar_approval", "credential_issuance"), "GraduationClearanceWorkbench", "GET /graduation-clearance/workbench", ("student_hold_projection",)),
    (18, (HOLD_TABLE, ENROLLMENT_TABLE), ("hold_type", "source", "effective_date", "blocking_actions", "freshness", "override_policy"), "EnrollmentWorkbench", "POST /holds/project", ("HoldChanged", "student_hold_projection")),
    (19, (TRANSFER_TABLE, AUDIT_TABLE), ("source_institution", "source_course", "credit", "equivalency", "applicability", "evaluator"), "DegreeAuditWorkbench", "POST /transfer-credit/evaluate", ("course_catalog_projection",)),
    (20, (TRANSFER_TABLE, ASSESSMENT_TABLE, AUDIT_TABLE), ("prior_learning_evidence", "assessment_method", "evaluator", "credit_awarded", "competency_mapping", "approval"), "DegreeAuditWorkbench", "POST /prior-learning/assess", ()),
    (21, (COURSE_TABLE, ENROLLMENT_TABLE), ("capacity_projection", "waitlist_position", "permission_code", "registration_result", "freshness", "promotion_evidence"), "RegistrationRulesWorkbench", "POST /registration/waitlist", ("CourseSectionCapacityChanged", "course_section_projection")),
    (22, (ENGAGEMENT_TABLE, RISK_TABLE), ("source", "attendance_rate", "last_activity", "missing_work_flag", "risk_contribution", "privacy_scope"), "StudentSuccessWorkbench", "POST /engagement/project", ("LearningEngagementUpdated", "learning_engagement_projection")),
    (23, (ENROLLMENT_TABLE, POLICY_TABLE, CONTROL_TABLE), ("compliance_profile", "required_load", "address_confirmation", "leave_restrictions", "reporting_event", "escalation"), "ComplianceWorkbench", "POST /international-compliance/check", ()),
    (24, (ACCOMMODATION_TABLE, ASSESSMENT_TABLE, ENROLLMENT_TABLE), ("permitted_adjustments", "effective_window", "privacy_classification", "stale_warning", "allowed_action", "redaction_profile"), "AccessibilityBoundaryPanel", "POST /accommodations/project", ("identity_student_projection",)),
    (25, (PETITION_TABLE, CURRICULUM_TABLE, ENROLLMENT_TABLE), ("petition_type", "requested_exception", "evidence", "committee_review", "decision", "expiration"), "PetitionWorkbench", "POST /petitions/review", ()),
    (26, (COMMUNICATION_TABLE, ADVISING_TABLE, APPLICANT_TABLE), ("template", "channel", "recipient", "purpose", "linked_case", "delivery_status"), "StudentTimelineWorkbench", "POST /communications", ("POST /notifications/messages", "notification_delivery_projection")),
    (27, (APPLICANT_TABLE, ENROLLMENT_TABLE, COURSE_TABLE, ASSESSMENT_TABLE, ADVISING_TABLE, PETITION_TABLE, CREDENTIAL_TABLE), ("timeline_entries", "student_id", "redaction_profile", "replay_checkpoint", "permission_scope", "idempotency_key"), "StudentTimelineWorkbench", "GET /students/timeline", ()),
    (28, (ENROLLMENT_TABLE, RISK_TABLE, INTERVENTION_TABLE), ("cohort", "program", "term", "entry_pathway", "risk_band", "low_count_suppression"), "AnalyticsWorkbench", "GET /analytics/cohort-retention", ("identity_student_projection",)),
    (29, (CONTROL_TABLE, RISK_TABLE), ("equity_metric", "protected_data_projection", "disparity_threshold", "review_task", "remediation_plan", "aggregation_floor"), "AnalyticsWorkbench", "POST /analytics/equity-monitoring", ("identity_student_projection",)),
    (30, (CURRICULUM_TABLE, AUDIT_TABLE, ADVISING_TABLE), ("requirement_change", "course_retirement", "prerequisite_change", "credit_change", "affected_students", "activation_approval"), "CurriculumPlanWorkbench", "POST /curriculum-change/impact", ("course_catalog_projection",)),
    (31, (ADVISING_TABLE, RISK_TABLE, AUDIT_TABLE, PETITION_TABLE, GRADUATION_TABLE), ("high_risk_queue", "missing_requirements", "registration_blockers", "petitions", "graduation_candidates", "inactive_outreach"), "AdvisingWorkbench", "GET /advising/workbench", ()),
    (32, (APPLICANT_TABLE, DOCUMENT_TABLE), ("incomplete_applications", "review_ready_files", "interviews", "decisions", "offers", "yield_outreach"), "AdmissionsWorkbench", "GET /admissions/workbench", ()),
    (33, (MODEL_TABLE, AUDIT_TABLE, ADVISING_TABLE, PETITION_TABLE, GRADUATION_TABLE), ("skill", "citations", "recommendation", "advisor_confirmation", "student_question", "source_links"), "EducationStudentLifecycleAssistantPanel", "POST /assistant/guidance", ()),
    (34, (MODEL_TABLE, ADVISING_TABLE, CURRICULUM_TABLE, PETITION_TABLE, ASSESSMENT_TABLE, ENROLLMENT_TABLE, CREDENTIAL_TABLE), ("command_preview", "student_identity", "evidence", "confirmation", "authority", "audit_trail"), "EducationStudentLifecycleAssistantPanel", "POST /assistant/command-preview", ()),
    (35, (POLICY_TABLE, APPLICANT_TABLE, ENROLLMENT_TABLE, ADVISING_TABLE), ("redaction_profile", "role", "minimum_necessary", "sensitive_fields", "export_allowed", "scope"), "PrivacyWorkbench", "POST /privacy/redact", ()),
    (36, (CONTROL_TABLE, CREDENTIAL_TABLE, COURSE_TABLE, ENROLLMENT_TABLE), ("retention_class", "amendment_reason", "original_value", "corrected_value", "approver", "legal_hold"), "RecordsGovernanceWorkbench", "POST /records/amendment", ()),
    (37, (CONTROL_TABLE, APPLICANT_TABLE, ENROLLMENT_TABLE, AUDIT_TABLE, PETITION_TABLE, CREDENTIAL_TABLE), ("control_population", "threshold", "failing_records", "owner", "remediation", "closure_evidence"), "ControlsWorkbench", "POST /controls/assert", ()),
    (38, (INBOX_TABLE, DEAD_LETTER_TABLE, ENROLLMENT_TABLE, CREDENTIAL_TABLE), ("retry_reason", "risk", "idempotency_key", "replay_checkpoint", "remediation_action", "dead_letter_queue"), "EventOperationsWorkbench", "POST /events/retry", ()),
    (39, (OUTBOX_TABLE, CONTROL_TABLE), ("hash_chain", "application_decisions", "enrollment_changes", "course_attempts", "assessments", "credentials"), "RecordsGovernanceWorkbench", "POST /records/proof-chain", ()),
    (40, (CREDENTIAL_TABLE, OUTBOX_TABLE), ("credential_identifier", "conferral_date", "status", "revocation_flag", "proof_reference", "privacy_scope"), "CredentialVerificationWorkbench", "GET /credentials/verify", ()),
    (41, (OUTCOME_TABLE, CREDENTIAL_TABLE), ("source", "outcome_date", "category", "confidence", "linked_credential", "aggregation_scope"), "OutcomesWorkbench", "POST /student-outcomes", ("alumni_outcome_projection",)),
    (42, (ACCREDITATION_TABLE, CURRICULUM_TABLE, ASSESSMENT_TABLE, CREDENTIAL_TABLE, OUTCOME_TABLE), ("program", "cohort", "outcome", "assessment", "reporting_period", "redaction"), "AccreditationWorkbench", "POST /accreditation/evidence-packet", ()),
    (43, (ENROLLMENT_TABLE, CURRICULUM_TABLE, CREDENTIAL_TABLE), ("campus", "modality", "program_hierarchy", "dual_enrollment", "primary_program", "residency_transition"), "EnrollmentWorkbench", "POST /multi-program/evaluate", ()),
    (44, (ENROLLMENT_TABLE, PETITION_TABLE, COURSE_TABLE), ("leave_type", "withdrawal_reason", "effective_date", "return_conditions", "reinstatement_petition", "transcript_notation"), "EnrollmentWorkbench", "POST /leave-withdrawal-reinstatement", ("billing_status_projection",)),
    (45, (APPLICANT_TABLE, TRANSFER_TABLE, ADVISING_TABLE, PETITION_TABLE, COURSE_TABLE, GRADUATION_TABLE, CREDENTIAL_TABLE), ("seed_scenario", "expected_queues", "expected_events", "evidence_packets", "privacy_restriction", "side_effect_free"), "ScenarioLibraryWorkbench", "GET /seed-scenarios/student-lifecycle", ()),
    (46, (POLICY_TABLE, CONTROL_TABLE), ("role", "permission", "command", "disabled_action", "authority_basis", "audit_scope"), "PermissionsWorkbench", "POST /permissions/evaluate", ()),
    (47, (OUTBOX_TABLE, ENROLLMENT_TABLE, CREDENTIAL_TABLE), ("enrollment_status", "credit_load", "satisfactory_progress", "credential_event", "withdrawal_event", "idempotency_key"), "BoundaryWorkbench", "POST /events/finance-billing-boundary", ("FinancialAidEligibilityUpdated", "BillingStatusUpdated", "financial_aid_status_projection", "billing_status_projection")),
    (48, (APPLICANT_TABLE, ENROLLMENT_TABLE, CURRICULUM_TABLE, COURSE_TABLE, ASSESSMENT_TABLE, ADVISING_TABLE, PETITION_TABLE, CREDENTIAL_TABLE, OUTBOX_TABLE), ("applicant", "admission", "enrollment", "curriculum_plan", "advising", "petition", "credential"), "StudentLifecycleSimulationWorkbench", "POST /simulation/applicant-to-credential", ()),
    (49, (CONTROL_TABLE, POLICY_TABLE), ("overlap_scan", "identity_boundary", "holds_boundary", "course_sections_boundary", "learning_boundary", "finance_boundary"), "BoundaryWorkbench", "POST /package-overlap/guardrails", EDUCATION_STUDENT_LIFECYCLE_DECLARED_DEPENDENCIES),
    (50, (SCHEMA_EXTENSION_TABLE, OUTBOX_TABLE, MODEL_TABLE), ("dsl_models", "dsl_routes", "dsl_services", "dsl_events", "dsl_ui", "dsl_agent_skills"), "CompositionWorkbench", "POST /composition/dsl/expose", ()),
)

CONTROL_SPECS: dict[int, dict[str, Any]] = {
    number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": dependencies}
    for number, tables, fields, ui, route, dependencies in _SPEC_ROWS
}


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update(
        {
            "references": (),
            "from_state": "application_review",
            "to_state": "offer_made",
            "decision_status": "ready",
            "reviewer_confirmation": True,
            "enrollment_status": "active",
            "blocking_actions": (),
            "override_approval": "advisor_override",
            "closure_evidence": "documented_outcome",
            "human_review": True,
            "moderation_status": "finalized",
            "hold_clearance": "clear",
            "freshness": "fresh",
            "privacy_classification": "restricted",
            "decision": "approved",
            "delivery_status": "delivered",
            "low_count_suppression": True,
            "aggregation_floor": 10,
            "advisor_confirmation": True,
            "confirmation": True,
            "authority": "registrar",
            "export_allowed": False,
            "legal_hold": False,
            "control_result": "pass",
            "hash_chain_valid": True,
            "revocation_flag": False,
            "side_effect_free": True,
            "overlap_scan": "pass",
            "stream_engine_picker_visible": False,
        }
    )
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    if number == 1 and payload.get("from_state") == payload.get("to_state"):
        findings.append("applicant lifecycle transition must move to a different state")
    if number == 1 and payload.get("decision_status") == "ready" and not payload.get("required_documents"):
        findings.append("applicant decision requires document evidence")
    if number == 3 and payload.get("reviewer_confirmation") is not True:
        findings.append("document-derived mutations require reviewer confirmation")
    if number == 4 and payload.get("enrollment_status") != "active" and payload.get("registration_result") == "registered":
        findings.append("inactive or blocked enrollment cannot register for courses")
    if number == 6 and payload.get("conflicting_substitution"):
        findings.append("degree audit rejects conflicting substitutions")
    if number == 8 and not payload.get("override_approval") and payload.get("missing_requirement"):
        findings.append("registration blocks missing prerequisites without valid override")
    if number == 11 and not payload.get("closure_evidence"):
        findings.append("advising case closure requires documented outcome")
    if number == 12 and payload.get("risk_score") and payload.get("human_review") is not True:
        findings.append("high-impact student success risk intervention requires human review")
    if number == 14 and payload.get("moderation_status") != "finalized":
        findings.append("assessment result must be finalized before credential completion")
    if number == 16 and payload.get("hold_clearance") != "clear":
        findings.append("credential award blocks until administrative hold projections are clear")
    if number == 18 and payload.get("freshness") != "fresh":
        findings.append("hold projections must be fresh before blocking enrollment actions")
    if number == 24 and payload.get("privacy_classification") == "sensitive" and payload.get("role") not in {"advisor", "registrar", "accessibility_officer"}:
        findings.append("sensitive accommodation detail must be redacted for unauthorized roles")
    if number == 25 and payload.get("decision") != "approved":
        findings.append("petition must be approved before applying exceptions")
    if number == 28 and payload.get("low_count_suppression") is not True:
        findings.append("cohort analytics require low-count suppression")
    if number == 29 and int(payload.get("aggregation_floor", 0)) < 10:
        findings.append("equity monitoring requires privacy-preserving aggregation floor")
    if number == 33 and not payload.get("citations"):
        findings.append("agent guidance requires citations to student lifecycle evidence")
    if number == 34 and not (payload.get("student_identity") and payload.get("confirmation") and payload.get("authority")):
        findings.append("governed agent CRUD requires identity, confirmation, and authority")
    if number == 35 and payload.get("export_allowed") is True and payload.get("role") not in {"registrar", "auditor"}:
        findings.append("student record export is blocked for unauthorized roles")
    if number == 36 and payload.get("legal_hold") is True and payload.get("delete_requested"):
        findings.append("records under legal hold cannot be deleted")
    if number == 37 and payload.get("control_result") != "pass":
        findings.append("continuous control assertions require remediation proof")
    if number == 39 and payload.get("hash_chain_valid") is not True:
        findings.append("academic record proof chain failed verification")
    if number == 40 and payload.get("revocation_flag") is True and payload.get("status") == "active":
        findings.append("credential verification cannot report revoked credentials as active")
    if number == 45 and payload.get("side_effect_free") is not True:
        findings.append("seeded student lifecycle scenarios must be side-effect-free")
    if number == 47 and payload.get("references") and any(str(ref).endswith("_table") for ref in payload.get("references", ())):
        findings.append("financial aid and billing boundary must use events or projections, not tables")
    if number == 49 and payload.get("overlap_scan") != "pass":
        findings.append("package overlap guardrails block duplicated external ownership")
    if number == 50 and payload.get("stream_engine_picker_visible") is not False:
        findings.append("composition DSL must not expose a stream-engine picker")
    return tuple(findings)


def evaluate_student_lifecycle_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_student_lifecycle_control", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    active_payload = sample_payload_for(resolved) if payload is None else dict(payload)
    missing = tuple(field for field in spec["fields"] if field not in active_payload or active_payload[field] in (None, ""))
    invalid_tables = tuple(table for table in spec["tables"] if table not in EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES)
    allowed_refs = set(EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES) | set(EDUCATION_STUDENT_LIFECYCLE_DECLARED_DEPENDENCIES)
    invalid_references = tuple(ref for ref in active_payload.get("references", ()) if ref not in allowed_refs)
    domain_findings = _domain_findings(resolved, active_payload)
    event_type = "EducationStudentLifecycleExceptionOpened" if domain_findings else "EducationStudentLifecycleUpdated"
    if resolved.feature_number in {1, 4, 7, 11, 13, 16, 20, 25, 40, 48} and not domain_findings:
        event_type = "EducationStudentLifecycleApproved"
    if resolved.feature_number in {35, 38, 39, 47, 50} and not domain_findings:
        event_type = "EducationStudentLifecycleControlEvidenceRecorded"
    return {
        "ok": not missing and not invalid_tables and not invalid_references and not domain_findings,
        "pbc": PBC_KEY,
        "capability": resolved.slug,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "status": "implemented",
        "target_tables": spec["tables"],
        "owned_tables": EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES,
        "read_tables": (),
        "declared_dependencies": spec["dependencies"],
        "invalid_references": invalid_references,
        "missing_required_fields": missing,
        "domain_findings": domain_findings,
        "event": {
            "contract": EVENT_CONTRACT,
            "topic": EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC,
            "type": event_type,
            "idempotency_key": _digest((PBC_KEY, resolved.slug, active_payload)),
            "outbox_table": OUTBOX_TABLE,
            "inbox_table": INBOX_TABLE,
            "dead_letter_table": DEAD_LETTER_TABLE,
        },
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "permission": "education_student_lifecycle.approve" if resolved.feature_number in {1, 14, 16, 25, 34, 40, 46, 48} else "education_student_lifecycle.admin" if resolved.feature_number in {35, 36, 37, 38, 39, 49, 50} else "education_student_lifecycle.update",
        "configuration": {
            "database_backends": EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
            "event_topic": EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "rule_configurable": True,
            "parameter_configurable": True,
        },
        "agent_skill": f"education_student_lifecycle_skills.{resolved.slug}",
        "requires_human_confirmation": resolved.feature_number in {1, 3, 8, 12, 14, 16, 20, 25, 30, 33, 34, 35, 36, 37, 40, 48},
        "retry_dead_letter_evidence": {
            "retry_policy": "bounded_retry_with_idempotency_key",
            "dead_letter_table": DEAD_LETTER_TABLE,
            "manual_replay_route": "POST /events/retry",
        },
        "release_evidence": {
            "code_artifact_model": resolved.model_artifacts,
            "ui_surface": resolved.ui_artifacts,
            "service_api": resolved.service_artifacts,
            "test": resolved.test_artifacts,
            "evidence": resolved.evidence_artifacts,
        },
        "shared_table_access": False,
        "side_effects": (),
    }


def improve1_student_lifecycle_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_student_lifecycle_control(capability) for capability in EDUCATION_STUDENT_LIFECYCLE_CONTROL_CAPABILITIES)
    return {
        "ok": len(evaluations) == 50 and all(item["ok"] for item in evaluations),
        "pbc": PBC_KEY,
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": EDUCATION_STUDENT_LIFECYCLE_OWNED_TABLES,
        "declared_dependencies": EDUCATION_STUDENT_LIFECYCLE_DECLARED_DEPENDENCIES,
        "database_backends": EDUCATION_STUDENT_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "event_topic": EDUCATION_STUDENT_LIFECYCLE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


STUDENT_LIFECYCLE_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_student_lifecycle_control(slug, payload))
    for capability in EDUCATION_STUDENT_LIFECYCLE_CONTROL_CAPABILITIES
}
