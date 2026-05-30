"""Executable improve1 controls for the Environment Health and Safety PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .standalone import ALLOWED_DATABASE_BACKENDS, CONSUMED_EVENT_TYPES, EMITTED_EVENT_TYPES, OWNED_TABLES, REQUIRED_EVENT_TOPIC

PBC_KEY = "environment_health_safety"
EVENT_CONTRACT = "AppGen-X"
EHS_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
EHS_REQUIRED_EVENT_TOPIC = REQUIRED_EVENT_TOPIC
EHS_OWNED_TABLES = OWNED_TABLES
EHS_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(CONSUMED_EVENT_TYPES) + tuple(EMITTED_EVENT_TYPES) + (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "POST /notifications/messages",
    "GET /workforce/qualifications/{id}",
    "GET /maintenance/assets/{id}",
    "GET /sustainability/environmental-reports/{id}",
)))

EHS_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in EHS_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in EHS_CONTROL_CAPABILITIES}

_SPEC_ROWS: tuple[tuple[int, tuple[str, ...], tuple[str, ...], str, str, tuple[str, ...]], ...] = (
    (1, ('environment_health_safety_ehs_incident',), ('lifecycle_state', 'severity_code', 'recordability_code', 'notification_status', 'closure_gate', 'queue_card'), 'IncidentLifecycleQueue', 'POST /ehs-incidents/lifecycle', ()),
    (2, ('environment_health_safety_ehs_incident',), ('jurisdiction', 'notification_clock', 'escalation_path', 'regulator_contact_pack', 'sent_acknowledgement', 'overdue_exception'), 'SeriousIncidentNotificationClock', 'POST /ehs-incidents/notifications', ()),
    (3, ('environment_health_safety_ehs_incident',), ('chronology', 'witness_statements', 'equipment_state', 'immediate_cause', 'basic_cause', 'root_cause', 'failed_barriers', 'evidence_links'), 'InvestigationDossier', 'POST /ehs-incidents/investigation', ()),
    (4, ('environment_health_safety_hazard', 'environment_health_safety_ehs_incident'), ('near_miss_cluster', 'unsafe_condition', 'task_pattern', 'control_failure_pattern', 'duplicate_hazard_lineage', 'promotion_rationale'), 'NearMissHazardPromotion', 'POST /hazards/promote-near-miss', ()),
    (5, ('environment_health_safety_corrective_action',), ('owner', 'due_date', 'hierarchy_of_controls', 'verification_step', 'effectiveness_window', 'verifier_evidence', 'reopen_logic'), 'CorrectiveActionEffectivenessGate', 'POST /corrective-actions/verify', ()),
    (6, ('environment_health_safety_hazard',), ('site', 'area', 'process', 'task_step', 'exposed_population', 'energy_source', 'existing_controls', 'residual_risk', 'duplicate_detection'), 'HazardRegisterHierarchy', 'POST /hazards', ()),
    (7, ('environment_health_safety_hazard', 'environment_health_safety_permit'), ('active_hazards', 'temporary_controls', 'permit_conditions', 'isolation_state', 'site_alerts', 'residual_risk_decision', 'signoff'), 'DynamicRiskAssessment', 'POST /hazards/dynamic-risk-assessment', ()),
    (8, ('environment_health_safety_inspection',), ('template', 'recurrence_rule', 'mandatory_evidence', 'route_scope', 'finding_severity', 'due_queue', 'overdue_escalation'), 'InspectionProgramScheduler', 'POST /inspections/schedule', ()),
    (9, ('environment_health_safety_inspection',), ('offline_submission_id', 'photos', 'measurements', 'signature', 'capture_time', 'sync_idempotency_key', 'conflict_resolution', 'stale_form_warning'), 'OfflineInspectionSync', 'POST /inspections/offline-sync', ()),
    (10, ('environment_health_safety_permit',), ('permit_type', 'area', 'time_window', 'energy_source', 'gas_test_status', 'rescue_readiness', 'simops', 'isolation_boundary', 'conflict_rule'), 'PermitConflictMatrix', 'POST /permits/dry-run', ()),
    (11, ('environment_health_safety_permit',), ('permit_state', 'suspension_reason', 'extension_limit', 'handback_evidence', 'supervisor_acknowledgement', 'return_to_service', 'area_acceptance'), 'PermitHandbackControl', 'POST /permits/handback', ()),
    (12, ('environment_health_safety_permit', 'environment_health_safety_safety_training'), ('gas_test_window', 'lockout_verification', 'role_coverage', 'equipment_readiness', 'rescue_plan', 'training_validity', 'missing_prerequisites'), 'HighRiskPermitPrerequisites', 'POST /permits/validate-prerequisites', ()),
    (13, ('environment_health_safety_safety_training', 'environment_health_safety_hazard'), ('hazard_family', 'permit_type', 'emergency_role', 'contractor_category', 'refresher_interval', 'qualification_reason', 'task_eligibility'), 'TrainingHazardPermitMatrix', 'POST /training/eligibility-check', ()),
    (14, ('environment_health_safety_safety_training',), ('expiry_date', 'grace_window', 'restricted_duty_flag', 'site_override', 'mandatory_retraining', 'mid_job_lapse_flag', 'exception_opened'), 'TrainingExpiryGovernance', 'POST /training/expiry-check', ()),
    (15, ('environment_health_safety_schema_extension',), ('exposure_sample', 'similar_exposure_group', 'dose_calculation', 'task_duration', 'control_type', 'action_threshold', 'exceedance_status'), 'ExposureMonitoringExtension', 'POST /schema-extensions/exposure-samples', ()),
    (16, ('environment_health_safety_policy_rule',), ('trigger_status', 'exposure_threshold', 'respirator_enrollment', 'substance_category', 'completion_evidence', 'bounded_operational_status', 'health_detail_excluded'), 'MedicalSurveillanceTriggerBoundary', 'POST /policy-rules/medical-surveillance-trigger', ()),
    (17, ('environment_health_safety_ehs_incident',), ('release_type', 'quantity_estimate', 'containment_status', 'reportability', 'waste_classification', 'environmental_handoff', 'federated_handoff_record'), 'SpillWasteEmissionsBoundary', 'POST /ehs-incidents/environmental-release', ()),
    (18, ('environment_health_safety_ehs_incident', 'environment_health_safety_permit'), ('active_permit_id', 'isolation_step', 'task_owner', 'area_conditions', 'loss_of_containment', 'incident_permit_navigation', 'closure_context_gate'), 'IncidentPermitLinkage', 'POST /ehs-incidents/link-permit', ()),
    (19, ('environment_health_safety_policy_rule',), ('obligation_type', 'jurisdiction', 'recurrence', 'owner', 'due_date', 'evidence_expectation', 'submitted_evidence', 'open_exception'), 'ComplianceObligationRegister', 'POST /compliance-obligations', ()),
    (20, ('environment_health_safety_policy_rule',), ('jurisdiction', 'site_class', 'contractor_presence', 'hazard_profile', 'effective_dates', 'comparison_view', 'approval_status', 'simulation_impact'), 'JurisdictionPolicyPackStudio', 'POST /policy-packs/simulate', ('PolicyChanged',)),
    (21, ('environment_health_safety_runtime_parameter',), ('risk_score_band', 'notification_countdown', 'inspection_grace_period', 'permit_extension_limit', 'capa_aging', 'parameter_history', 'unsafe_range_rejected'), 'EhsRuntimeParameterConsole', 'POST /runtime-parameters', ()),
    (22, ('environment_health_safety_ehs_incident', 'environment_health_safety_permit', 'environment_health_safety_inspection'), ('role_lane', 'active_incidents', 'open_permits', 'overdue_inspections', 'at_risk_actions', 'training_expiries', 'exposure_exceedances', 'obligations'), 'RoleBasedEhsWorkbench', 'GET /environment-health-safety-workbench', ()),
    (23, ('environment_health_safety_ehs_incident', 'environment_health_safety_permit', 'environment_health_safety_audit_finding'), ('chronology', 'linked_hazards', 'linked_permits', 'corrective_actions', 'attachments', 'approvals', 'event_provenance', 'source_badges'), 'EvidenceFirstEhsDetail', 'GET /environment-health-safety/records/{record_id}', ()),
    (24, ('environment_health_safety_ehs_incident',), ('incident_status', 'open_actions', 'affected_area', 'controls_in_place', 'unanswered_questions', 'source_citations', 'unsupported_claim_refusal'), 'AssistantIncidentShiftSummary', 'POST /assistant/incident-summary', ()),
    (25, ('environment_health_safety_permit',), ('draft_permit_package', 'missing_prerequisites', 'pre_start_briefing_points', 'validation_only', 'human_confirmation', 'no_auto_issue'), 'AssistantPermitReviewCoach', 'POST /assistant/permit-review', ()),
    (26, ('environment_health_safety_hazard', 'environment_health_safety_permit'), ('source_document', 'extracted_controls', 'ppe_requirements', 'inspection_criteria', 'permit_prerequisites', 'source_excerpts', 'confidence', 'review_state'), 'EhsDocumentIntake', 'POST /assistant/document-intake', ()),
    (27, ('environment_health_safety_ehs_incident',), ('investigation_id', 'missing_evidence', 'contradictory_timestamps', 'next_interviews', 'next_documents', 'citations', 'no_direct_mutation'), 'AssistantInvestigationGapCheck', 'POST /assistant/investigation-gap-check', ()),
    (28, ('environment_health_safety_ehs_incident',), ('search_read_model', 'validation_only_command', 'bulk_close_path', 'reopen_path', 'evidence_export', 'rule_failures', 'idempotency_key'), 'EhsApiExpansion', 'POST /ehs-incidents/dry-run', ()),
    (29, ('environment_health_safety_hazard', 'environment_health_safety_inspection', 'environment_health_safety_safety_training'), ('batch_id', 'row_validation', 'row_idempotency', 'accepted_rows', 'rejected_rows', 'resumable_failures', 'correction_workflow'), 'EhsBulkIntake', 'POST /hazards/bulk-intake', ()),
    (30, ('environment_health_safety_appgen_outbox_event',), ('typed_event_schema', 'incident_severity_changed', 'permit_issued', 'inspection_failed', 'action_overdue', 'exposure_exceeded', 'training_lapsed', 'audit_finding_reopened'), 'TypedEhsEventCatalog', 'GET /events/ehs-event-schemas', ()),
    (31, ('environment_health_safety_appgen_inbox_event', 'environment_health_safety_policy_rule'), ('policy_event_id', 'affected_records', 'old_policy_version', 'new_policy_version', 'recomputed_state', 'opened_exceptions', 'idempotent_replay'), 'PolicyChangeReevaluationHandler', 'POST /events/policy-changed/replay', ('PolicyChanged',)),
    (32, ('environment_health_safety_appgen_inbox_event', 'environment_health_safety_audit_finding'), ('sealed_bundle_id', 'read_only_state', 'amendment_required', 'original_bundle', 'new_revision', 'edit_blocked'), 'AuditSealEvidenceLock', 'POST /events/audit-sealed/replay', ('AuditEventSealed',)),
    (33, ('environment_health_safety_appgen_inbox_event', 'environment_health_safety_control_assertion'), ('kpi_event_id', 'risk_score_delta', 'anomaly_baseline', 'queue_priority', 'affected_site', 'affected_task', 'event_lineage'), 'OperationalKpiRiskReprioritization', 'POST /events/operational-kpi/replay', ('OperationalKpiChanged',)),
    (34, ('environment_health_safety_appgen_dead_letter_event',), ('failure_reason', 'last_attempt', 'replay_safety', 'domain_impact', 'operator_decision', 'poison_quarantine', 'retry_log'), 'EhsDeadLetterReplayOps', 'POST /events/dead-letter/replay', ()),
    (35, ('environment_health_safety_ehs_incident', 'environment_health_safety_control_assertion'), ('actor', 'command', 'event', 'projection_checkpoint', 'policy_version', 'timeline_hash', 'replay_result'), 'EhsEventSourcedTimeline', 'GET /timeline/ehs-operating-history', ()),
    (36, ('environment_health_safety_governed_model', 'environment_health_safety_hazard'), ('leading_indicators', 'site_score', 'task_score', 'hazard_cluster_score', 'interpretable_drivers', 'record_drilldown', 'model_evaluation'), 'PredictiveEhsRiskScore', 'POST /risk-scores/predict', ()),
    (37, ('environment_health_safety_governed_model', 'environment_health_safety_control_assertion'), ('exposure_outlier', 'waste_outlier', 'permit_duration_outlier', 'capa_aging_outlier', 'baseline_window', 'observed_deviation', 'affected_records', 'explainable_alert'), 'EhsAnomalyDetection', 'POST /anomalies/detect', ()),
    (38, ('environment_health_safety_governed_model', 'environment_health_safety_hazard'), ('control_options', 'incident_likelihood', 'permit_restrictions', 'exposure_reduction', 'operational_disruption', 'non_authoritative_marker', 'approval_required'), 'EhsCounterfactualControlSimulation', 'POST /control-simulations', ()),
    (39, ('environment_health_safety_control_assertion',), ('serious_notification_assertion', 'expired_permit_assertion', 'overdue_capa_assertion', 'lapsed_training_assertion', 'exposure_exceedance_assertion', 'exception_event', 'affected_records'), 'ContinuousEhsControlTesting', 'POST /control-assertions/run', ()),
    (40, ('environment_health_safety_control_assertion',), ('hash_chain', 'evidence_package', 'approvals', 'event_payloads', 'release_bundle', 'tamper_check', 'redacted_export_validation'), 'CryptographicEhsProofBundle', 'POST /proof-bundles/verify', ()),
    (41, ('environment_health_safety_policy_rule',), ('tenant_scope', 'site_scope', 'jurisdiction_scope', 'policy_isolation', 'parameter_isolation', 'assistant_context_isolation', 'negative_access_tests'), 'TenantSiteJurisdictionIsolation', 'POST /isolation/prove', ()),
    (42, ('environment_health_safety_schema_extension',), ('local_field', 'validation_rules', 'migration_preview', 'projection_impact', 'rollback_metadata', 'backfill_evidence', 'old_record_readability'), 'ControlledEhsSchemaEvolution', 'POST /schema-extensions/dry-run', ()),
    (43, ('environment_health_safety_governed_model',), ('approved_agent_skills', 'blocked_decisions', 'human_checkpoints', 'prompt_provenance', 'model_version', 'no_autonomous_permit_issue', 'no_autonomous_closure'), 'GovernedEhsAgentExecution', 'POST /agent/guardrails/check', ()),
    (44, ('environment_health_safety_audit_finding',), ('audit_plan', 'finding_taxonomy', 'recurrence_cluster', 'owner_escalation', 'linked_incidents', 'linked_hazards', 'linked_actions', 'closure_condition_changed'), 'AuditRepeatFindingMemory', 'POST /audit-findings/cluster', ()),
    (45, ('environment_health_safety_policy_rule',), ('submission_due_date', 'draft_status', 'approver', 'submitted_artifact', 'regulator_acknowledgement', 'late_filing_justification', 'overdue_exception'), 'ComplianceCalendarSubmissionEvidence', 'POST /compliance-calendar/submissions', ()),
    (46, ('environment_health_safety_appgen_inbox_event', 'environment_health_safety_appgen_outbox_event'), ('federation_contract', 'incoming_operational_signal', 'outgoing_spill_event', 'outgoing_waste_event', 'outgoing_exposure_event', 'freshness_rule', 'ownership_rule', 'foreign_table_access'), 'CrossPbcEhsFederation', 'POST /federation/contracts', ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')),
    (47, ('environment_health_safety_control_assertion',), ('incident_investigation_pack', 'permit_cycle_pack', 'overdue_training_block', 'inspection_failure', 'audit_finding', 'resulting_events', 'verifier_notes'), 'EhsReleaseEvidencePack', 'POST /release/ehs-evidence-pack', ()),
    (48, ('environment_health_safety_control_assertion',), ('specification_surface', 'manifest_surface', 'route_registration', 'event_schema', 'ui_route', 'pass_fail_matrix', 'broken_declaration_detection'), 'SpecificationContractChecks', 'POST /contracts/verify-specification', ()),
    (49, ('environment_health_safety_control_assertion',), ('hazard_recorded', 'permit_issued', 'inspection_failed', 'incident_opened', 'corrective_action_assigned', 'lapsed_training_blocked', 'sealed_evidence', 'deterministic_output'), 'EndToEndEhsReleaseScenario', 'POST /release/end-to-end-scenario', ()),
    (50, ('environment_health_safety_ehs_incident', 'environment_health_safety_permit', 'environment_health_safety_inspection'), ('high_risk_permits_active', 'inspection_overdue_rate', 'notification_timeliness', 'corrective_action_aging', 'training_expiry_exposure', 'exposure_exceedances', 'repeat_audit_findings', 'open_obligations', 'metric_drilldown'), 'OperationalSafetyComplianceMetrics', 'GET /environment-health-safety-workbench/metrics', ()),
)

CONTROL_SPECS: dict[int, dict[str, Any]] = {number: {"tables": tables, "fields": fields, "ui": ui, "route": route, "dependencies": deps} for number, tables, fields, ui, route, deps in _SPEC_ROWS}
_EMPTY_ALLOWED_FIELDS = (
    "blocked_decisions",
    "contradictory_timestamps",
    "expired_permit_assertion",
    "exposure_exceedance_assertion",
    "exposure_exceedances",
    "failed_barriers",
    "foreign_table_access",
    "late_filing_justification",
    "lapsed_training_assertion",
    "missing_evidence",
    "missing_prerequisites",
    "next_documents",
    "next_interviews",
    "old_record_readability",
    "open_obligations",
    "overdue_capa_assertion",
    "overdue_exception",
    "poison_quarantine",
    "site_alerts",
    "simops",
    "open_exception",
    "rejected_rows",
    "resumable_failures",
    "opened_exceptions",
    "repeat_audit_findings",
    "unsafe_range_rejected",
)


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
        "lifecycle_state": "investigation-open", "severity_code": "hospitalization", "recordability_code": "recordable", "notification_status": "acknowledged", "closure_gate": "open", "queue_card": "visible",
        "jurisdiction": "osha", "notification_clock": "PT8H", "escalation_path": "site-lead", "regulator_contact_pack": "complete", "sent_acknowledgement": "ack-1", "overdue_exception": (),
        "chronology": ("alarm", "response"), "witness_statements": ("operator",), "equipment_state": "isolated", "immediate_cause": "guard missing", "basic_cause": "maintenance gap", "root_cause": "inspection drift", "failed_barriers": ("guarding",), "evidence_links": ("ehs://proof/1",),
        "near_miss_cluster": ("INC-1", "INC-2"), "unsafe_condition": "ventilation failure", "task_pattern": "solvent changeover", "control_failure_pattern": "repeat", "duplicate_hazard_lineage": "linked", "promotion_rationale": "cluster threshold met",
        "owner": "ehs-owner", "due_date": "2026-06-30", "hierarchy_of_controls": "engineering", "verification_step": "verify airflow", "effectiveness_window": "P30D", "verifier_evidence": "proof", "reopen_logic": "enabled",
        "site": "Plant 7", "area": "Coating", "process": "paint", "task_step": "mix", "exposed_population": "operators", "energy_source": "chemical", "existing_controls": ("LEV",), "residual_risk": "medium", "duplicate_detection": "clear",
        "active_hazards": ("haz-1",), "temporary_controls": ("barrier",), "permit_conditions": "met", "isolation_state": "verified", "site_alerts": (), "residual_risk_decision": "proceed_with_controls", "signoff": "supervisor",
        "template": "weekly-round", "recurrence_rule": "weekly", "mandatory_evidence": ("photo",), "route_scope": "area", "finding_severity": "major", "due_queue": "scheduled", "overdue_escalation": "enabled",
        "offline_submission_id": "offline-1", "photos": ("photo-1",), "measurements": {"noise": 80}, "signature": "inspector", "capture_time": "2026-05-30T08:00:00Z", "sync_idempotency_key": "idem-1", "conflict_resolution": "server-merge", "stale_form_warning": "none",
        "permit_type": "hot_work", "time_window": "2026-05-30T08:00/PT4H", "gas_test_status": "clear", "rescue_readiness": "ready", "simops": (), "isolation_boundary": "LOTO-1", "conflict_rule": "passed",
        "permit_state": "handed-back", "suspension_reason": "weather", "extension_limit": "PT2H", "handback_evidence": "complete", "supervisor_acknowledgement": True, "return_to_service": "accepted", "area_acceptance": "accepted",
        "gas_test_window": "valid", "lockout_verification": "verified", "role_coverage": "complete", "equipment_readiness": "ready", "rescue_plan": "ready", "training_validity": "current", "missing_prerequisites": (),
        "hazard_family": "confined_space", "emergency_role": "rescuer", "contractor_category": "qualified", "refresher_interval": "P1Y", "qualification_reason": "current training", "task_eligibility": True,
        "expiry_date": "2026-12-31", "grace_window": "P7D", "restricted_duty_flag": False, "site_override": "none", "mandatory_retraining": "scheduled", "mid_job_lapse_flag": False, "exception_opened": False,
        "exposure_sample": "sample-1", "similar_exposure_group": "paint", "dose_calculation": "below_limit", "task_duration": "PT2H", "control_type": "engineering", "action_threshold": "85dBA", "exceedance_status": "clear",
        "trigger_status": "required", "exposure_threshold": "met", "respirator_enrollment": "active", "substance_category": "isocyanate", "completion_evidence": "complete", "bounded_operational_status": True, "health_detail_excluded": True,
        "release_type": "spill", "quantity_estimate": "10L", "containment_status": "contained", "reportability": "notifiable", "waste_classification": "hazardous", "environmental_handoff": "sent", "federated_handoff_record": "projection-only",
        "active_permit_id": "PERM-1", "isolation_step": "LOTO-1", "task_owner": "supervisor", "area_conditions": "wet", "loss_of_containment": True, "incident_permit_navigation": "linked", "closure_context_gate": "passed",
        "obligation_type": "report", "recurrence": "monthly", "evidence_expectation": "filed report", "submitted_evidence": "artifact", "open_exception": (),
        "site_class": "manufacturing", "contractor_presence": True, "hazard_profile": "chemical", "effective_dates": ("2026-05-30",), "comparison_view": "available", "approval_status": "approved", "simulation_impact": "known",
        "risk_score_band": "high", "notification_countdown": "PT8H", "inspection_grace_period": "PT24H", "permit_extension_limit": "PT2H", "capa_aging": "30d", "parameter_history": "versioned", "unsafe_range_rejected": True,
        "role_lane": "supervisor", "active_incidents": "visible", "open_permits": "visible", "overdue_inspections": "visible", "at_risk_actions": "visible", "training_expiries": "visible", "exposure_exceedances": (), "obligations": "visible",
        "linked_hazards": ("haz-1",), "linked_permits": ("perm-1",), "corrective_actions": ("ca-1",), "attachments": ("att-1",), "approvals": ("approval-1",), "event_provenance": "outbox", "source_badges": "linked",
        "incident_status": "open", "open_actions": ("ca-1",), "affected_area": "Coating", "controls_in_place": ("barrier",), "unanswered_questions": ("interview contractor",), "source_citations": ("INC-1",), "unsupported_claim_refusal": True,
        "draft_permit_package": "pkg-1", "pre_start_briefing_points": ("gas test",), "validation_only": True, "human_confirmation": True, "no_auto_issue": True,
        "source_document": "sds.pdf", "extracted_controls": ("ventilation",), "ppe_requirements": ("respirator",), "inspection_criteria": ("check LEV",), "permit_prerequisites": ("gas test",), "source_excerpts": ("section 8",), "confidence": 0.88, "review_state": "pending",
        "investigation_id": "INC-1", "missing_evidence": (), "contradictory_timestamps": (), "next_interviews": (), "next_documents": (), "citations": ("INC-1",), "no_direct_mutation": True,
        "search_read_model": "available", "validation_only_command": True, "bulk_close_path": "governed", "reopen_path": "governed", "evidence_export": "available", "rule_failures": ("none",), "idempotency_key": "idem-1",
        "batch_id": "batch-1", "row_validation": "passed", "row_idempotency": "per-row", "accepted_rows": 10, "rejected_rows": (), "resumable_failures": (), "correction_workflow": "available",
        "typed_event_schema": "valid", "incident_severity_changed": "schema", "permit_issued": "schema", "inspection_failed": "schema", "action_overdue": "schema", "exposure_exceeded": "schema", "training_lapsed": "schema", "audit_finding_reopened": "schema",
        "policy_event_id": "policy-1", "affected_records": ("INC-1",), "old_policy_version": "v1", "new_policy_version": "v2", "recomputed_state": "complete", "opened_exceptions": (), "idempotent_replay": True,
        "sealed_bundle_id": "bundle-1", "read_only_state": True, "amendment_required": "if_changed", "original_bundle": "bundle-1", "new_revision": "revision-2", "edit_blocked": True,
        "kpi_event_id": "kpi-1", "risk_score_delta": 12, "anomaly_baseline": "baseline", "queue_priority": "recalculated", "affected_site": "Plant 7", "affected_task": "Line break", "event_lineage": "kpi-1",
        "failure_reason": "bad payload", "last_attempt": 3, "replay_safety": "safe", "domain_impact": "none", "operator_decision": "quarantine", "poison_quarantine": "enabled", "retry_log": ("attempt-1",),
        "actor": "ehs-lead", "command": "close_incident", "event": "EnvironmentHealthSafetyUpdated", "projection_checkpoint": "chk-1", "policy_version": "v2", "timeline_hash": "sha256:timeline", "replay_result": "exact",
        "leading_indicators": ("near_miss",), "site_score": 72, "task_score": 80, "hazard_cluster_score": 76, "interpretable_drivers": ("overdue CAs",), "record_drilldown": ("CA-1",), "model_evaluation": "approved",
        "exposure_outlier": False, "waste_outlier": False, "permit_duration_outlier": False, "capa_aging_outlier": False, "baseline_window": "P90D", "observed_deviation": "none", "explainable_alert": "not_required",
        "control_options": ("ventilation",), "incident_likelihood": "reduced", "permit_restrictions": "none", "exposure_reduction": "30%", "operational_disruption": "low", "non_authoritative_marker": True, "approval_required": True,
        "serious_notification_assertion": "passed", "expired_permit_assertion": (), "overdue_capa_assertion": (), "lapsed_training_assertion": (), "exposure_exceedance_assertion": (), "exception_event": "none",
        "hash_chain": ("h1", "h2"), "evidence_package": "bundle", "event_payloads": ("evt",), "release_bundle": "release", "tamper_check": "passed", "redacted_export_validation": "passed",
        "tenant_scope": "tenant-a", "site_scope": "Plant 7", "jurisdiction_scope": "osha", "policy_isolation": True, "parameter_isolation": True, "assistant_context_isolation": True, "negative_access_tests": "passed",
        "local_field": "site_custom", "validation_rules": "compiled", "migration_preview": "available", "projection_impact": "none", "rollback_metadata": "available", "backfill_evidence": "complete", "old_record_readability": True,
        "approved_agent_skills": ("draft",), "blocked_decisions": ("issue_permit", "close_incident"), "human_checkpoints": ("approve",), "prompt_provenance": "captured", "model_version": "ehs-agent-1", "no_autonomous_permit_issue": True, "no_autonomous_closure": True,
        "audit_plan": "annual", "finding_taxonomy": "repeat", "recurrence_cluster": "ventilation", "owner_escalation": "EHS manager", "linked_incidents": ("INC-1",), "closure_condition_changed": True,
        "submission_due_date": "2026-06-30", "draft_status": "ready", "approver": "EHS lead", "submitted_artifact": "report.pdf", "regulator_acknowledgement": "ack", "late_filing_justification": (),
        "federation_contract": "declared", "incoming_operational_signal": "OperationalKpiChanged", "outgoing_spill_event": "SpillReported", "outgoing_waste_event": "WasteClassified", "outgoing_exposure_event": "ExposureExceeded", "freshness_rule": "PT1H", "ownership_rule": "EHS-owned", "foreign_table_access": (),
        "incident_investigation_pack": "complete", "permit_cycle_pack": "complete", "overdue_training_block": "proved", "inspection_failure": "proved", "audit_finding": "proved", "resulting_events": ("EnvironmentHealthSafetyCreated",), "verifier_notes": "passed",
        "specification_surface": "matched", "manifest_surface": "matched", "route_registration": "matched", "event_schema": "matched", "ui_route": "matched", "pass_fail_matrix": "passed", "broken_declaration_detection": "proved",
        "hazard_recorded": "done", "permit_issued": "done", "inspection_failed": "done", "incident_opened": "done", "corrective_action_assigned": "done", "lapsed_training_blocked": "done", "sealed_evidence": "done", "deterministic_output": "stable",
        "high_risk_permits_active": 1, "inspection_overdue_rate": 0.0, "notification_timeliness": "on_time", "corrective_action_aging": "green", "training_expiry_exposure": 0, "repeat_audit_findings": (), "open_obligations": (), "metric_drilldown": "available",
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and payload.get("lifecycle_state") not in {"draft", "triaged", "recordability-review", "regulator-notified", "investigation-open", "corrective-action-open", "closed", "reopened"}:
        findings.append("incident lifecycle state is not supported")
    if n == 2 and payload.get("notification_clock") in (None, ""):
        findings.append("serious incident notification clock is required")
    if n == 3 and not payload.get("root_cause"):
        findings.append("investigation dossier requires root cause")
    if n == 5 and not payload.get("verifier_evidence"):
        findings.append("corrective action cannot close without verifier evidence")
    if n == 7 and payload.get("signoff") in (None, ""):
        findings.append("dynamic risk assessment requires signoff")
    if n == 10 and payload.get("conflict_rule") != "passed":
        findings.append("permit conflict matrix blocked issuance")
    if n == 12 and payload.get("missing_prerequisites"):
        findings.append("high-risk permit has unmet prerequisites")
    if n == 14 and payload.get("mid_job_lapse_flag"):
        findings.append("active permit has lapsed training qualification")
    if n == 16 and payload.get("health_detail_excluded") is not True:
        findings.append("medical surveillance boundary must exclude health details")
    if n == 24 and not payload.get("source_citations"):
        findings.append("assistant summary requires source citations")
    if n == 25 and payload.get("no_auto_issue") is not True:
        findings.append("assistant permit review must not auto-issue permits")
    if n == 27 and payload.get("no_direct_mutation") is not True:
        findings.append("investigation gap skill must be preview-only")
    if n == 31 and payload.get("idempotent_replay") is not True:
        findings.append("policy-change consumption must be idempotent")
    if n == 32 and payload.get("edit_blocked") is not True:
        findings.append("sealed audit evidence cannot be silently edited")
    if n == 39 and any(payload.get(field) not in ("passed", (), "none") for field in ("serious_notification_assertion", "expired_permit_assertion", "overdue_capa_assertion", "lapsed_training_assertion", "exposure_exceedance_assertion")):
        findings.append("continuous EHS controls have unresolved failing assertions")
    if n == 40 and payload.get("tamper_check") != "passed":
        findings.append("cryptographic proof bundle failed tamper validation")
    if n == 41 and payload.get("negative_access_tests") != "passed":
        findings.append("tenant/site/jurisdiction isolation proof failed")
    if n == 43 and (payload.get("no_autonomous_permit_issue") is not True or payload.get("no_autonomous_closure") is not True):
        findings.append("governed EHS agent attempted autonomous restricted action")
    if n == 46 and payload.get("foreign_table_access"):
        findings.append("cross-PBC federation cannot use foreign tables")
    if n == 49 and not all(payload.get(field) == "done" for field in ("hazard_recorded", "permit_issued", "inspection_failed", "incident_opened", "corrective_action_assigned", "lapsed_training_blocked", "sealed_evidence")):
        findings.append("end-to-end EHS release scenario is incomplete")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_ehs_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in EHS_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in EHS_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": EHS_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": EHS_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {
        "ok": ok,
        "pbc": PBC_KEY,
        "feature_number": resolved.feature_number,
        "slug": resolved.slug,
        "title": resolved.title,
        "capability": resolved.as_traceability_row(),
        "payload": candidate,
        "evidence": evidence,
        "missing_fields": missing_fields,
        "foreign_tables": foreign_tables,
        "undeclared_dependencies": undeclared_dependencies,
        "findings": findings,
        "side_effects": (),
    }


def improve1_ehs_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_ehs_control(capability) for capability in EHS_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.environment-health-safety-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": EHS_OWNED_TABLES,
        "declared_dependencies": EHS_DECLARED_DEPENDENCIES,
        "allowed_database_backends": EHS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": EHS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


EHS_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_ehs_control(slug, payload)) for capability in EHS_CONTROL_CAPABILITIES}
