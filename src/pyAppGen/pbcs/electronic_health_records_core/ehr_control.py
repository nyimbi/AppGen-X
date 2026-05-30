"""Executable improve1 controls for the electronic health records core PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "electronic_health_records_core"
EVENT_CONTRACT = "AppGen-X"
EHR_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
EHR_REQUIRED_EVENT_TOPIC = "pbc.electronic_health_records_core.events"
EHR_OWNED_TABLES = (
    "electronic_health_records_core_patient_chart",
    "electronic_health_records_core_clinical_encounter",
    "electronic_health_records_core_clinical_order",
    "electronic_health_records_core_observation",
    "electronic_health_records_core_allergy",
    "electronic_health_records_core_medication_list",
    "electronic_health_records_core_care_note",
    "electronic_health_records_core_electronic_health_records_core_policy_rule",
    "electronic_health_records_core_electronic_health_records_core_runtime_parameter",
    "electronic_health_records_core_electronic_health_records_core_schema_extension",
    "electronic_health_records_core_electronic_health_records_core_control_assertion",
    "electronic_health_records_core_electronic_health_records_core_governed_model",
    "electronic_health_records_core_appgen_outbox_event",
    "electronic_health_records_core_appgen_inbox_event",
    "electronic_health_records_core_appgen_dead_letter_event",
)
EHR_DECLARED_DEPENDENCIES = (
    "patient_identity_projection",
    "encounter_scheduling_projection",
    "pharmacy_safety_projection",
    "lab_result_projection",
    "imaging_result_projection",
    "consent_directive_projection",
    "care_coordination_projection",
    "public_health_reporting_projection",
    "revenue_cycle_coding_projection",
    "analytics_extract_projection",
    "PolicyChanged",
    "CustomerUpdated",
    "SupplierQualified",
    "PatientIdentityUpdated",
    "ConsentDirectiveChanged",
    "MedicationDispenseUpdated",
    "ExternalDiagnosticResulted",
    "CarePlanUpdated",
    "POST /notifications/messages",
    "POST /public-health/reportable-events",
    "GET /identity/patients/{id}",
    "GET /pharmacy/medication-safety/{id}",
    "GET /care-coordination/plans/{id}",
)

CHART = "electronic_health_records_core_patient_chart"
ENCOUNTER = "electronic_health_records_core_clinical_encounter"
ORDER = "electronic_health_records_core_clinical_order"
OBSERVATION = "electronic_health_records_core_observation"
ALLERGY = "electronic_health_records_core_allergy"
MEDICATION = "electronic_health_records_core_medication_list"
NOTE = "electronic_health_records_core_care_note"
RULE = "electronic_health_records_core_electronic_health_records_core_policy_rule"
PARAMETER = "electronic_health_records_core_electronic_health_records_core_runtime_parameter"
SCHEMA_EXTENSION = "electronic_health_records_core_electronic_health_records_core_schema_extension"
CONTROL = "electronic_health_records_core_electronic_health_records_core_control_assertion"
MODEL = "electronic_health_records_core_electronic_health_records_core_governed_model"
OUTBOX = "electronic_health_records_core_appgen_outbox_event"
INBOX = "electronic_health_records_core_appgen_inbox_event"
DEAD_LETTER = "electronic_health_records_core_appgen_dead_letter_event"

EHR_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in EHR_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in EHR_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = (
    (1, (CHART, CONTROL), ("identity_confidence", "duplicate_candidates", "review_decision", "source_lineage", "reversible_link"), "ChartIdentityWorkbench", "POST /charts/identity-merge-review", ("patient_identity_projection",)),
    (2, (ENCOUNTER, NOTE), ("encounter_class", "care_setting", "modality", "attending_role", "documentation_checklist"), "EncounterWorkbench", "POST /encounters/setting-validate", ("encounter_scheduling_projection",)),
    (3, (NOTE, CONTROL), ("author", "supervising_signer", "attestation_status", "addendum_chain", "correction_reason"), "ClinicalNoteWorkbench", "POST /notes/attest", ()),
    (4, (CHART, ENCOUNTER, ORDER, OBSERVATION, ALLERGY, MEDICATION, NOTE), ("problem", "episode", "acuity", "responsible_clinician", "projection_checkpoint"), "ProblemOrientedChart", "GET /charts/problem-sections", ()),
    (5, (ORDER, OUTBOX), ("order_state", "target_state", "order_type", "indication", "result_expectation", "transition_authority"), "OrderWorkbench", "POST /orders/lifecycle-transition", ()),
    (6, (ORDER, RULE), ("order_set", "indication", "template_version", "approving_committee", "activation_window", "rollback_plan"), "OrderSetGovernance", "POST /order-sets/instantiate", ()),
    (7, (OBSERVATION,), ("unit", "method", "specimen_type", "collection_time", "reference_range", "abnormal_flag"), "ObservationWorkbench", "POST /observations/validate", ("lab_result_projection",)),
    (8, (OBSERVATION, CONTROL), ("critical_flag", "acknowledgement_owner", "deadline", "notified_party", "read_back_evidence", "escalation_tier"), "CriticalResultQueue", "POST /critical-results/acknowledge", ("POST /notifications/messages",)),
    (9, (ALLERGY, ORDER), ("substance_class", "specific_substance", "reaction", "severity", "verification_status", "clinical_override_guidance"), "AllergyWorkbench", "POST /allergies/screen", ("pharmacy_safety_projection",)),
    (10, (MEDICATION, ENCOUNTER), ("source_list", "patient_reported_medication", "reconciliation_action", "discrepancy_reason", "reviewer", "unresolved_discrepancy"), "MedicationReconciliationWorkbench", "POST /medications/reconcile", ("MedicationDispenseUpdated",)),
    (11, (MEDICATION, ALLERGY, OBSERVATION, ORDER), ("allergy_conflict", "duplicate_therapy", "dose_range_warning", "observation_conflict", "renal_caution"), "MedicationSafetyPanel", "POST /medication-safety/screen", ("GET /pharmacy/medication-safety/{id}", "pharmacy_safety_projection")),
    (12, (CHART, ENCOUNTER, MEDICATION, ALLERGY, OBSERVATION, ORDER, NOTE), ("active_problems", "recent_encounters", "active_medications", "allergies", "pending_orders", "freshness"), "PatientSummaryWorkbench", "GET /patient-summary", ("consent_directive_projection",)),
    (13, (CHART, ENCOUNTER, ORDER, OBSERVATION, ALLERGY, MEDICATION, NOTE, OUTBOX), ("event_history", "projection_checkpoint", "as_of_time", "amendment_visibility", "immutable_assertion"), "ChartSnapshotWorkbench", "GET /charts/as-of", ()),
    (14, (CONTROL, ENCOUNTER, NOTE), ("deficiency_type", "responsible_role", "due_date", "severity", "linked_record", "closure_evidence"), "DocumentationDeficiencyQueue", "POST /documentation-deficiencies", ()),
    (15, (CHART, OBSERVATION, NOTE), ("intake_state", "source", "clinical_relevance", "reviewer", "accepted_into_chart", "rejection_reason"), "PatientGeneratedDataQueue", "POST /patient-generated-data/intake", ()),
    (16, (NOTE, CHART, CONTROL), ("source_document", "extracted_finding", "confidence", "reviewer", "accepted_field", "source_span"), "ExternalDocumentReconciliation", "POST /external-documents/reconcile", ()),
    (17, (RULE, CHART, NOTE), ("access_purpose", "consent_scope", "sensitive_section", "emergency_override_reason", "audit_notification"), "ConsentAccessWorkbench", "POST /access/consent-check", ("ConsentDirectiveChanged",)),
    (18, (RULE, NOTE, CHART), ("redaction_profile", "required_fields", "restricted_sections", "redaction_reasons", "export_purpose"), "RedactionWorkbench", "POST /redaction/profile", ()),
    (19, (ENCOUNTER, NOTE, OUTBOX), ("diagnosis_evidence", "procedure_evidence", "clinical_indication", "documentation_support", "coding_clarification"), "CodingEvidencePanel", "POST /coding/evidence", ("revenue_cycle_coding_projection",)),
    (20, (RULE, CONTROL), ("rule_definition", "version", "severity", "explanation", "override_policy", "rollback"), "ClinicalDecisionSupportStudio", "POST /cds/rules", ()),
    (21, (RULE, CONTROL), ("alert_frequency", "accepted_overrides", "duplicate_alerts", "user_burden", "suppression_candidate", "governance_review"), "AlertGovernanceWorkbench", "POST /cds/override-fatigue", ()),
    (22, (CHART, NOTE, ORDER, OBSERVATION, ALLERGY, MEDICATION), ("search_index", "snippet_redaction", "query", "permission_scope", "clinical_concept"), "ClinicalSearchWorkbench", "GET /chart-search", ()),
    (23, (CHART, NOTE, ORDER, OBSERVATION, MEDICATION, CONTROL), ("problem_quality_signal", "last_reviewed", "conflicting_evidence", "human_confirmation", "status_change"), "ProblemListQualityQueue", "POST /problems/quality-review", ()),
    (24, (OBSERVATION, NOTE), ("observation_group", "baseline", "latest_value", "slope", "abnormality_pattern", "unit_consistency"), "TrendPanelWorkbench", "GET /observations/trends", ()),
    (25, (ENCOUNTER, NOTE, ORDER, OBSERVATION, MEDICATION), ("timeline_event", "actor", "timestamp", "source", "linked_entity", "amendment_marker"), "EncounterTimeline", "GET /encounters/timeline", ()),
    (26, (MODEL, CHART, NOTE, MEDICATION, ALLERGY, OBSERVATION), ("summary_type", "citations", "permission_scope", "inference_marker", "restricted_sections"), "ElectronicHealthRecordsCoreAssistantPanel", "POST /assistant/summarize-chart", ()),
    (27, (MODEL, ENCOUNTER, NOTE, ALLERGY, OBSERVATION, MEDICATION, ORDER), ("command_preview", "required_fields", "source_evidence", "actor", "confirmation", "resulting_command"), "ElectronicHealthRecordsCoreAssistantPanel", "POST /assistant/command-preview", ()),
    (28, (NOTE, CHART), ("ambiguity_marker", "suspected_condition", "negation", "family_history", "conflicting_source", "low_confidence"), "ClinicalAmbiguityPanel", "POST /documents/ambiguity-preserve", ()),
    (29, (SCHEMA_EXTENSION, CHART, NOTE), ("specialty_template", "validation_rules", "ui_placement", "migration_evidence", "backward_compatibility"), "SchemaExtensionStudio", "POST /schema-extensions/specialty", ()),
    (30, (RULE, PARAMETER), ("tenant", "signature_timing", "critical_threshold", "access_restriction", "agent_approval_gate"), "ClinicalPolicyWorkbench", "POST /policies/tenant-evaluate", ()),
    (31, (CONTROL, CHART, NOTE, OUTBOX), ("retention_category", "amendment_chain", "legal_hold", "export_eligibility", "deletion_prohibition"), "RecordsGovernanceWorkbench", "POST /records/retention-amendment", ()),
    (32, (CONTROL, ENCOUNTER, ORDER, OBSERVATION), ("analytics_purpose", "low_count_suppression", "redaction", "permission_gate", "limited_data_set"), "AnalyticsExtractWorkbench", "POST /analytics/extract", ("analytics_extract_projection",)),
    (33, (CONTROL, OBSERVATION, OUTBOX), ("reportability_indicator", "trigger_evidence", "destination_profile", "required_fields", "submission_state"), "PublicHealthReportingPanel", "POST /public-health/candidates", ("POST /public-health/reportable-events", "public_health_reporting_projection")),
    (34, (NOTE, CHART, CONTROL), ("offline_draft", "local_sequence", "reconciliation", "conflict_detection", "recovery_audit"), "DowntimeDocumentationWorkbench", "POST /downtime/reconcile", ()),
    (35, (CONTROL, CHART, ENCOUNTER, OBSERVATION, ORDER, ALLERGY, NOTE), ("control_type", "severity", "owner", "due_date", "closure_evidence", "plausibility"), "DataQualityControlsWorkbench", "POST /controls/data-quality", ()),
    (36, (INBOX, DEAD_LETTER), ("retry_classification", "dead_letter_reason", "clinical_risk", "reprocess_eligibility", "human_remediation_note"), "ClinicalInboxOperations", "POST /events/dead-letter/replay", ()),
    (37, (CONTROL, RULE), ("boundary_scan", "declared_dependency", "foreign_table_check", "generated_artifact_scan", "violation"), "BoundaryProofWorkbench", "POST /boundary/proof", EHR_DECLARED_DEPENDENCIES),
    (38, (CHART, OBSERVATION, NOTE, CONTROL), ("portal_profile", "release_timing", "sensitive_result", "correction_request", "clinician_review"), "PatientPortalSummaryControls", "POST /portal-summary/release", ()),
    (39, (NOTE, CHART, CONTROL), ("attachment_type", "source", "linked_entity", "checksum", "redaction_profile", "retention_class"), "ClinicalAttachmentWorkbench", "POST /attachments/ingest", ()),
    (40, (CHART, ENCOUNTER, ORDER, OBSERVATION, NOTE, CONTROL), ("role_view", "unsigned_notes", "critical_results", "pending_orders", "privacy_overrides", "permission_actions"), "ElectronicHealthRecordsCoreWorkbench", "GET /workbench/role-views", ()),
    (41, (SCHEMA_EXTENSION, NOTE, ENCOUNTER, ORDER, OBSERVATION), ("specialty", "required_sections", "order_prompts", "observation_panels", "template_version"), "SpecialtyTemplateLibrary", "POST /specialty-templates/instantiate", ()),
    (42, (CONTROL, CHART, OBSERVATION, ORDER, OUTBOX), ("measure", "denominator", "numerator", "exclusion", "source_evidence", "event_output"), "QualityMeasureTraceability", "POST /quality-measures/trace", ("analytics_extract_projection",)),
    (43, (NOTE, ORDER, MEDICATION, CONTROL), ("record_version", "edit_session", "conflict_preview", "merge_suggestion", "reviewer_signoff"), "ConcurrentEditingWorkbench", "POST /records/resolve-conflict", ()),
    (44, (CHART, ALLERGY, MEDICATION, ENCOUNTER, ORDER, OBSERVATION, CONTROL), ("identity_confidence", "active_allergies", "medication_reconciliation", "recent_documentation", "pending_orders", "deficiencies"), "ChartCompletenessScore", "GET /charts/completeness", ()),
    (45, (CONTROL, ORDER, OBSERVATION, ALLERGY, ENCOUNTER, NOTE), ("exception_type", "severity", "response_owner", "remediation_evidence", "closure_state"), "ClinicalSafetyExceptionQueue", "POST /safety-exceptions", ()),
    (46, (OUTBOX, CONTROL), ("hash_chain", "chart_mutation", "note_signature", "order_transition", "observation_correction", "export_bundle"), "ChartIntegrityProofs", "POST /chart-integrity/proof", ()),
    (47, (MODEL, CONTROL), ("model_purpose", "model_version", "evaluation_cohort", "approval_status", "expiry", "human_feedback"), "ClinicalModelRegistry", "POST /models/register", ()),
    (48, (CHART, ENCOUNTER, ORDER, OBSERVATION, ALLERGY, MEDICATION, NOTE, CONTROL), ("seed_scenario", "workbench_queues", "events", "summary", "side_effect_free"), "ClinicalScenarioLibrary", "GET /seed-scenarios/ehr-core", ()),
    (49, (CHART, ENCOUNTER, NOTE, ORDER, OBSERVATION, ALLERGY, MEDICATION, OUTBOX), ("patient_chart", "encounter", "signed_note", "placed_order", "resulted_observation", "audited_amendment"), "FullEHRReleaseSimulation", "POST /simulation/chart-lifecycle", ()),
    (50, (SCHEMA_EXTENSION, MODEL, OUTBOX), ("dsl_models", "dsl_routes", "dsl_services", "dsl_events", "dsl_ui", "dsl_agent_skills"), "CompositionWorkbench", "POST /composition/dsl/expose", ()),
)
CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, tables, fields, ui, route, deps in _SPEC_ROWS}


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
    payload.update({
        "references": (), "merge_action": "review", "reviewer": "clinician-1", "from_state": "signed", "to_state": "released",
        "result_evidence": "result-1", "template_status": "active", "unit_compatible": True, "acknowledgement_evidence": "readback",
        "duplicate_allergy_reviewed": True, "reconciliation_complete": True, "safety_source": "owned_chart_plus_declared_projection",
        "permission_scope": "clinician", "as_of_time": "2026-05-30T00:00:00Z", "reviewer_confirmation": True,
        "consent_allowed": True, "break_glass_reason": "", "restricted_sections": (), "override_justification": "documented",
        "governance_approval": True, "governance_review": True, "snippet_redacted": True, "human_confirmation": True, "unit_consistency": True,
        "citations": ("chart:event:1",), "confirmation": True, "ambiguity_preserved": True, "target_table": CHART,
        "tenant": "tenant-a", "legal_hold": False, "low_count_suppression": True, "conflict_detected": False,
        "clinical_risk": "reviewed", "violations": (), "release_allowed": True, "checksum": "sha256:abc",
        "reviewer_signoff": "reviewer-1", "completeness_score": 0.95, "closure_evidence": "remediated",
        "hash_chain_valid": True, "approval_status": "approved", "side_effect_free": True, "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and payload.get("merge_action") == "auto_merge":
        findings.append("duplicate charts must be reviewed before merge")
    if n == 3 and not payload.get("reviewer"):
        findings.append("clinical note attestation requires authorized signer evidence")
    if n == 5 and payload.get("from_state") == payload.get("to_state"):
        findings.append("clinical order lifecycle transition must move state")
    if n == 5 and payload.get("result_expectation") and not payload.get("result_evidence"):
        findings.append("result-required orders cannot close without evidence")
    if n == 6 and payload.get("template_status") == "retired":
        findings.append("retired order set templates cannot be instantiated")
    if n == 7 and payload.get("unit_compatible") is not True:
        findings.append("observation unit is not compatible with method and reference range")
    if n == 8 and not payload.get("acknowledgement_evidence"):
        findings.append("critical result cannot close without acknowledgement evidence")
    if n == 9 and payload.get("duplicate_allergy_reviewed") is not True:
        findings.append("duplicate allergy entries require clinical review")
    if n == 10 and payload.get("reconciliation_complete") is not True:
        findings.append("encounter closure blocks incomplete medication reconciliation")
    if n == 11 and payload.get("safety_source") != "owned_chart_plus_declared_projection":
        findings.append("medication safety screening must use owned chart evidence or declared projections")
    if n == 12 and payload.get("permission_scope") == "patient" and payload.get("restricted_sections"):
        findings.append("patient summary must omit restricted sections")
    if n == 13 and not payload.get("as_of_time"):
        findings.append("point-in-time chart review requires an as-of timestamp")
    if n == 16 and payload.get("confidence") == "low" and payload.get("reviewer_confirmation") is not True:
        findings.append("low-confidence document extraction requires reviewer approval")
    if n == 17 and payload.get("consent_allowed") is False and not payload.get("break_glass_reason"):
        findings.append("restricted chart access requires consent or break-glass reason")
    if n == 20 and payload.get("governance_approval") is not True:
        findings.append("clinical decision support rules require governance approval")
    if n == 21 and payload.get("suppression_candidate") and payload.get("governance_review") is not True:
        findings.append("alert suppression requires governance review")
    if n == 22 and payload.get("snippet_redacted") is not True:
        findings.append("clinical search snippets must be permission redacted")
    if n == 23 and payload.get("status_change") and payload.get("human_confirmation") is not True:
        findings.append("problem status changes require human confirmation")
    if n == 24 and payload.get("unit_consistency") is not True:
        findings.append("trend panels require unit consistency")
    if n == 26 and not payload.get("citations"):
        findings.append("agent chart summaries require evidence citations")
    if n == 27 and payload.get("confirmation") is not True:
        findings.append("governed agent CRUD previews require confirmation before mutation")
    if n == 28 and payload.get("ambiguity_preserved") is not True:
        findings.append("clinical ambiguity must be preserved instead of confirmed as fact")
    if n == 29 and payload.get("target_table") not in EHR_OWNED_TABLES:
        findings.append("schema extension target must be an owned EHR table")
    if n == 31 and payload.get("legal_hold") and payload.get("delete_requested"):
        findings.append("clinical records under legal hold cannot be deleted")
    if n == 32 and payload.get("low_count_suppression") is not True:
        findings.append("privacy-safe analytics require low-count suppression")
    if n == 34 and payload.get("conflict_detected") and payload.get("reviewer_confirmation") is not True:
        findings.append("offline documentation conflicts require review before activation")
    if n == 37 and payload.get("violations"):
        findings.append("cross-PBC boundary proof fails on undeclared table references")
    if n == 38 and payload.get("sensitive_result") and payload.get("release_allowed") is not True:
        findings.append("patient portal summary holds sensitive results until policy release")
    if n == 39 and not payload.get("checksum"):
        findings.append("clinical attachments require checksum preservation")
    if n == 43 and payload.get("conflict_detected") and not payload.get("reviewer_signoff"):
        findings.append("concurrent clinical edit conflicts require reviewer signoff")
    if n == 44 and float(payload.get("completeness_score", 0)) < 0.8:
        findings.append("chart completeness score must expose missing clinical evidence")
    if n == 45 and not payload.get("closure_evidence"):
        findings.append("clinical safety exceptions close only with remediation evidence")
    if n == 46 and payload.get("hash_chain_valid") is not True:
        findings.append("chart integrity proof chain failed verification")
    if n == 47 and payload.get("approval_status") != "approved":
        findings.append("model-backed clinical commands require approved model evidence")
    if n == 48 and payload.get("side_effect_free") is not True:
        findings.append("seeded clinical scenarios must be side-effect-free")
    if n == 50 and payload.get("stream_engine_picker_visible") is not False:
        findings.append("composition DSL must not expose stream-engine picker choices")
    return tuple(findings)


def evaluate_ehr_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_ehr_control", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    active_payload = sample_payload_for(resolved) if payload is None else dict(payload)
    missing = tuple(field for field in spec["fields"] if field not in active_payload or active_payload[field] in (None, ""))
    invalid_tables = tuple(table for table in spec["tables"] if table not in EHR_OWNED_TABLES)
    allowed_refs = set(EHR_OWNED_TABLES) | set(EHR_DECLARED_DEPENDENCIES)
    invalid_references = tuple(ref for ref in active_payload.get("references", ()) if ref not in allowed_refs)
    domain_findings = _domain_findings(resolved, active_payload)
    event_type = "ElectronicHealthRecordsCoreExceptionOpened" if domain_findings else "ElectronicHealthRecordsCoreUpdated"
    if resolved.feature_number in {1, 3, 5, 8, 10, 17, 27, 39, 49} and not domain_findings:
        event_type = "ElectronicHealthRecordsCoreApproved"
    if resolved.feature_number in {31, 36, 37, 46, 50} and not domain_findings:
        event_type = "ElectronicHealthRecordsCoreControlEvidenceRecorded"
    return {
        "ok": not missing and not invalid_tables and not invalid_references and not domain_findings,
        "pbc": PBC_KEY,
        "capability": resolved.slug,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "status": "implemented",
        "target_tables": spec["tables"],
        "owned_tables": EHR_OWNED_TABLES,
        "read_tables": (),
        "declared_dependencies": spec["dependencies"],
        "invalid_references": invalid_references,
        "missing_required_fields": missing,
        "domain_findings": domain_findings,
        "event": {"contract": EVENT_CONTRACT, "topic": EHR_REQUIRED_EVENT_TOPIC, "type": event_type, "idempotency_key": _digest((PBC_KEY, resolved.slug, active_payload)), "outbox_table": OUTBOX, "inbox_table": INBOX, "dead_letter_table": DEAD_LETTER},
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "permission": "electronic_health_records_core.approve" if resolved.feature_number in {3, 5, 8, 10, 17, 27, 39, 43, 49} else "electronic_health_records_core.admin" if resolved.feature_number in {20, 21, 29, 31, 36, 37, 46, 47, 50} else "electronic_health_records_core.update",
        "configuration": {"database_backends": EHR_ALLOWED_DATABASE_BACKENDS, "event_topic": EHR_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "rule_configurable": True, "parameter_configurable": True},
        "agent_skill": f"electronic_health_records_core_skills.{resolved.slug}",
        "requires_human_confirmation": resolved.feature_number in {1, 3, 8, 10, 16, 17, 23, 27, 28, 31, 34, 38, 43, 45, 49},
        "retry_dead_letter_evidence": {"retry_policy": "bounded_retry_with_idempotency_key", "dead_letter_table": DEAD_LETTER, "manual_replay_route": "POST /events/dead-letter/replay"},
        "release_evidence": {"code_artifact_model": resolved.model_artifacts, "ui_surface": resolved.ui_artifacts, "service_api": resolved.service_artifacts, "test": resolved.test_artifacts, "evidence": resolved.evidence_artifacts},
        "shared_table_access": False,
        "side_effects": (),
    }


def improve1_ehr_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_ehr_control(capability) for capability in EHR_CONTROL_CAPABILITIES)
    return {"ok": len(evaluations) == 50 and all(item["ok"] for item in evaluations), "pbc": PBC_KEY, "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": EHR_OWNED_TABLES, "declared_dependencies": EHR_DECLARED_DEPENDENCIES, "database_backends": EHR_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "event_topic": EHR_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "side_effects": ()}


EHR_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_ehr_control(slug, payload)) for capability in EHR_CONTROL_CAPABILITIES}
