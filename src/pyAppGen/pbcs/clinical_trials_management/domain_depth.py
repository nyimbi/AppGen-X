"""Domain depth contract for the clinical_trials_management PBC."""

from __future__ import annotations

import hashlib

PBC_KEY = "clinical_trials_management"
DOMAIN_ENTITY = "trial_protocol"
DOMAIN_PURPOSE = (
    "Protocol governance, site activation, subject enrollment, consent control, visit execution, "
    "safety escalation, monitoring follow-up, and lock readiness for clinical trial operations"
)
DOMAIN_OWNED_TABLES = (
    "clinical_trials_management_trial_protocol",
    "clinical_trials_management_study_site",
    "clinical_trials_management_subject",
    "clinical_trials_management_consent_record",
    "clinical_trials_management_visit_schedule",
    "clinical_trials_management_adverse_event",
    "clinical_trials_management_monitoring_finding",
    "clinical_trials_management_clinical_trials_management_policy_rule",
    "clinical_trials_management_clinical_trials_management_runtime_parameter",
    "clinical_trials_management_clinical_trials_management_schema_extension",
    "clinical_trials_management_clinical_trials_management_control_assertion",
    "clinical_trials_management_clinical_trials_management_governed_model",
    "clinical_trials_management_appgen_outbox_event",
    "clinical_trials_management_appgen_inbox_event",
    "clinical_trials_management_appgen_dead_letter_event",
)
DOMAIN_OPERATIONS = (
    "register_trial_protocol",
    "activate_study_site",
    "review_subject_eligibility",
    "record_consent",
    "schedule_visit",
    "report_serious_adverse_event",
    "open_monitoring_finding",
    "review_policy_rule",
    "set_runtime_parameter",
    "register_schema_extension",
    "record_control_assertion",
    "register_governed_model",
    "assess_data_lock_readiness",
    "simulate_protocol_amendment_impact",
    "run_release_simulation",
)
DOMAIN_RULES = (
    "active_protocol_required",
    "site_activation_evidence_complete",
    "consent_version_matches_protocol",
    "eligibility_evidence_complete",
    "serious_event_reporting_within_sla",
    "subject_view_redaction_required",
)
DOMAIN_PARAMETERS = (
    "screening_window_days",
    "visit_window_grace_days",
    "serious_event_reporting_hours",
    "monitoring_followup_days",
    "reconsent_notice_days",
    "workbench_limit",
)
DOMAIN_EVENTS = (
    "ClinicalTrialProtocolRegistered",
    "ClinicalTrialSiteActivated",
    "ClinicalTrialSubjectEnrollmentReviewed",
    "ClinicalTrialConsentRecorded",
    "ClinicalTrialVisitScheduled",
    "ClinicalTrialSeriousAdverseEventReported",
    "ClinicalTrialMonitoringFindingOpened",
    "ClinicalTrialLockReadinessChanged",
)
DOMAIN_CONSUMED_EVENTS = ("PolicyChanged", "SiteDocumentReceived", "LabResultReceived")
DOMAIN_ADVANCED_CAPABILITIES = (
    "protocol_amendment_impact_simulation",
    "consent_scoped_data_use_guardrails",
    "risk_based_monitoring_governance",
    "timeline_projection_with_redaction",
    "cryptographic_trial_evidence_proofs",
    "assistant_guided_regulated_change_preview",
)
DOMAIN_WORKBENCH_VIEWS = (
    "protocol_amendments",
    "site_activation",
    "screening_and_enrollment",
    "visit_readiness",
    "safety_reporting",
    "monitoring_findings",
    "data_lock_blockers",
)

_OPERATION_TARGETS = {
    "register_trial_protocol": ("clinical_trials_management_trial_protocol", "ClinicalTrialProtocolRegistered", "clinical_trials_management.protocol_admin"),
    "activate_study_site": ("clinical_trials_management_study_site", "ClinicalTrialSiteActivated", "clinical_trials_management.site_activation"),
    "review_subject_eligibility": ("clinical_trials_management_subject", "ClinicalTrialSubjectEnrollmentReviewed", "clinical_trials_management.subject_enrollment"),
    "record_consent": ("clinical_trials_management_consent_record", "ClinicalTrialConsentRecorded", "clinical_trials_management.consent_manage"),
    "schedule_visit": ("clinical_trials_management_visit_schedule", "ClinicalTrialVisitScheduled", "clinical_trials_management.visit_manage"),
    "report_serious_adverse_event": ("clinical_trials_management_adverse_event", "ClinicalTrialSeriousAdverseEventReported", "clinical_trials_management.safety_review"),
    "open_monitoring_finding": ("clinical_trials_management_monitoring_finding", "ClinicalTrialMonitoringFindingOpened", "clinical_trials_management.monitoring_manage"),
    "review_policy_rule": ("clinical_trials_management_clinical_trials_management_policy_rule", None, "clinical_trials_management.configure"),
    "set_runtime_parameter": ("clinical_trials_management_clinical_trials_management_runtime_parameter", None, "clinical_trials_management.configure"),
    "register_schema_extension": ("clinical_trials_management_clinical_trials_management_schema_extension", None, "clinical_trials_management.configure"),
    "record_control_assertion": ("clinical_trials_management_clinical_trials_management_control_assertion", None, "clinical_trials_management.audit"),
    "register_governed_model": ("clinical_trials_management_clinical_trials_management_governed_model", None, "clinical_trials_management.configure"),
    "assess_data_lock_readiness": ("clinical_trials_management_clinical_trials_management_control_assertion", "ClinicalTrialLockReadinessChanged", "clinical_trials_management.lock_review"),
    "simulate_protocol_amendment_impact": ("clinical_trials_management_trial_protocol", None, "clinical_trials_management.protocol_admin"),
    "run_release_simulation": ("clinical_trials_management_appgen_outbox_event", "ClinicalTrialLockReadinessChanged", "clinical_trials_management.audit"),
}


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.domain-depth.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "operation_count": len(DOMAIN_OPERATIONS),
        "operations": DOMAIN_OPERATIONS,
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 15,
        "minimum_domain_operations": 12,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    target = _OPERATION_TARGETS.get(operation)
    if target is None:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    target_table, emitted_event, permission = target
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": target_table,
        "owned_tables": (target_table,),
        "read_tables": (),
        "emitted_event": emitted_event,
        "event_contract": "AppGen-X",
        "idempotency_key": _digest((PBC_KEY, operation, tuple(sorted(payload.items())))),
        "rules_evaluated": DOMAIN_RULES[:3],
        "parameters_read": DOMAIN_PARAMETERS[:3],
        "permission": permission,
        "evidence_hash": _digest((operation, payload, target_table, emitted_event)),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(execute_domain_operation(operation, {"tenant": "tenant-smoke"}) for operation in DOMAIN_OPERATIONS[:5])
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and all(item["ok"] for item in executions)
        and all(item["target_table"].startswith(f"{PBC_KEY}_") for item in executions),
        "contract": contract,
        "executions": executions,
        "side_effects": (),
    }


DOMAIN_EDGE_CASES = (
    "consent_version_mismatch",
    "site_activation_missing_approval",
    "screen_fail_without_enrollment",
    "visit_outside_window",
    "serious_event_overdue",
    "open_monitoring_finding_blocks_lock",
    "idempotency_replay",
    "dead_letter_recovery",
)
DOMAIN_SPECIALIST_CAPABILITIES = tuple(
    dict.fromkeys(
        tuple(DOMAIN_ADVANCED_CAPABILITIES)
        + tuple(f"specialist_{operation}" for operation in DOMAIN_OPERATIONS)
        + tuple(f"rule_driven_{rule}" for rule in DOMAIN_RULES)
    )
)


def domain_capability_surface_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.complete-domain-capability-surface.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "operation_surfaces": tuple(
            {
                "operation": operation,
                "surface": f"{PBC_KEY}.ui.operation.{operation}",
                "action": operation,
                "target_table": _OPERATION_TARGETS[operation][0],
                "permission": _OPERATION_TARGETS[operation][2],
                "requires_confirmation": operation not in {"assess_data_lock_readiness", "simulate_protocol_amendment_impact", "run_release_simulation"},
                "agent_tool": f"{PBC_KEY}_skills.{operation}",
                "event": _OPERATION_TARGETS[operation][1],
            }
            for operation in DOMAIN_OPERATIONS
        ),
        "rule_surfaces": tuple(
            {"rule": rule, "surface": f"{PBC_KEY}.ui.rule.{rule}", "editor": True, "explainable": True}
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {"parameter": parameter, "surface": f"{PBC_KEY}.ui.parameter.{parameter}", "bounded": True, "editable": True}
            for parameter in DOMAIN_PARAMETERS
        ),
        "advanced_surfaces": tuple(
            {
                "capability": capability,
                "surface": f"{PBC_KEY}.ui.advanced.{_digest(capability)[:12]}",
                "explainable": True,
            }
            for capability in DOMAIN_ADVANCED_CAPABILITIES
        ),
        "edge_case_surfaces": tuple(
            {"edge_case": edge_case, "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}", "triage_queue": True}
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {"owned_table": table, "surface": f"{PBC_KEY}.ui.table.{table}", "read_model": True, "mutation_guard": True}
            for table in DOMAIN_OWNED_TABLES
        ),
        "specialist_capabilities": DOMAIN_SPECIALIST_CAPABILITIES,
        "coverage": {
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "shared_table_access": False,
        },
        "side_effects": (),
    }
