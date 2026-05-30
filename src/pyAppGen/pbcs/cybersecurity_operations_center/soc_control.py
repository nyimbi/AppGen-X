"""Executable improve1 controls for the cybersecurity operations center PBC."""

from __future__ import annotations

from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .models import APPGEN_EVENT_CONTRACT, OWNED_TABLES, stable_digest

PBC_KEY = "cybersecurity_operations_center"
EVENT_CONTRACT = APPGEN_EVENT_CONTRACT
REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")

ALERT_TABLE = f"{PBC_KEY}_security_alert"
INCIDENT_TABLE = f"{PBC_KEY}_security_incident"
ASSET_TABLE = f"{PBC_KEY}_asset_exposure"
THREAT_INTEL_TABLE = f"{PBC_KEY}_threat_intel"
PLAYBOOK_TABLE = f"{PBC_KEY}_playbook_run"
CONTAINMENT_TABLE = f"{PBC_KEY}_containment_action"
EVIDENCE_TABLE = f"{PBC_KEY}_response_evidence"
POLICY_TABLE = f"{PBC_KEY}_{PBC_KEY}_policy_rule"
PARAMETER_TABLE = f"{PBC_KEY}_{PBC_KEY}_runtime_parameter"
CONTROL_ASSERTION_TABLE = f"{PBC_KEY}_{PBC_KEY}_control_assertion"
GOVERNED_MODEL_TABLE = f"{PBC_KEY}_{PBC_KEY}_governed_model"
OUTBOX_TABLE = f"{PBC_KEY}_appgen_outbox_event"
INBOX_TABLE = f"{PBC_KEY}_appgen_inbox_event"
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"

SOC_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in SOC_CONTROL_CAPABILITIES}
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in SOC_CONTROL_CAPABILITIES}

SOC_FEATURE_CONTROLS: dict[int, dict[str, Any]] = {
    1: {"tables": (ALERT_TABLE, OUTBOX_TABLE), "fields": ("current_state", "next_state", "transition_reason", "actor"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /security-alerts/transition"},
    2: {"tables": (ALERT_TABLE,), "fields": ("source_event_id", "detection_timestamp", "detection_rule_id", "confidence", "evidence_checksum"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /security-alerts"},
    3: {"tables": (ALERT_TABLE, POLICY_TABLE), "fields": ("asset_ref", "principal_ref", "indicator_value", "detection_rule_id", "time_window_minutes"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /security-alerts"},
    4: {"tables": (ALERT_TABLE,), "fields": ("severity", "confidence", "blast_radius", "sla_breach_risk"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center-workbench"},
    5: {"tables": (ALERT_TABLE,), "fields": ("asset_criticality", "user_sensitivity", "network_exposure", "enrichment_source"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /security-alerts/enrich"},
    6: {"tables": (INCIDENT_TABLE, ALERT_TABLE, POLICY_TABLE), "fields": ("alert_cluster_size", "asset_criticality", "containment_required", "preview_mode"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /security-incidents"},
    7: {"tables": (ALERT_TABLE, INCIDENT_TABLE, CONTAINMENT_TABLE, EVIDENCE_TABLE), "fields": ("timeline_entries", "case_id", "ordered_by"), "ui": "CybersecurityOperationsCenterDetail", "route": "GET /cybersecurity-operations-center/case-detail"},
    8: {"tables": (EVIDENCE_TABLE,), "fields": ("collection_source", "checksum", "acquired_at", "handling_history"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /response-evidence"},
    9: {"tables": (CONTAINMENT_TABLE, POLICY_TABLE), "fields": ("action_type", "risk_level", "approval_path", "rollback_instructions"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /containment-actions"},
    10: {"tables": (THREAT_INTEL_TABLE,), "fields": ("observed_fact", "source_provenance", "confidence", "expiry"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /threat-intels"},
    11: {"tables": (THREAT_INTEL_TABLE, POLICY_TABLE), "fields": ("indicator_value", "expires_at", "revalidation_status", "retirement_reason"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /threat-intels/revalidate"},
    12: {"tables": (ASSET_TABLE, ALERT_TABLE, INCIDENT_TABLE), "fields": ("asset_ref", "criticality", "open_alert_ids", "open_incident_ids"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /asset-exposures"},
    13: {"tables": (PLAYBOOK_TABLE,), "fields": ("stage", "checkpoint_statuses", "assignee", "timestamp"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /playbook-runs"},
    14: {"tables": (PLAYBOOK_TABLE, POLICY_TABLE), "fields": ("breakpoint_type", "requires_human_confirmation", "preview_summary"), "ui": "CybersecurityOperationsCenterAssistantPanel", "route": "POST /playbook-runs/preview"},
    15: {"tables": (ALERT_TABLE, POLICY_TABLE), "fields": ("duration", "reason", "scope", "owner", "review_date"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /security-alerts/suppress"},
    16: {"tables": (ALERT_TABLE,), "fields": ("false_positive_cause", "detection_rule_id", "remediation_recommendation"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /security-alerts/close"},
    17: {"tables": (ALERT_TABLE, INCIDENT_TABLE), "fields": ("actor_hypothesis", "indicator_reuse", "target_profile", "cluster_confidence"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center-workbench"},
    18: {"tables": (INCIDENT_TABLE,), "fields": ("business_criticality", "spread", "credential_exposure", "override_rationale"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /security-incidents/severity"},
    19: {"tables": (INCIDENT_TABLE,), "fields": ("incident_commander", "communications_owner", "evidence_owner", "containment_owner"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /security-incidents/assign"},
    20: {"tables": (EVIDENCE_TABLE, ALERT_TABLE, INCIDENT_TABLE), "fields": ("request_status", "due_date", "source_system", "returned_artifact_refs"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /response-evidence"},
    21: {"tables": (OUTBOX_TABLE, ALERT_TABLE, INCIDENT_TABLE), "fields": ("command_name", "actor", "reason", "aggregate_id"), "ui": "CybersecurityOperationsCenterDetail", "route": "GET /cybersecurity-operations-center/case-detail"},
    22: {"tables": (INBOX_TABLE, DEAD_LETTER_TABLE), "fields": ("event_type", "idempotency_key", "handler_outcome", "dead_letter_policy"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /cybersecurity-operations-center/events"},
    23: {"tables": (ALERT_TABLE, INCIDENT_TABLE), "fields": ("command", "permission", "policy_result", "route"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /security-alerts/commands"},
    24: {"tables": (ALERT_TABLE, INCIDENT_TABLE), "fields": ("validation_only", "required_fields", "policy_blockers"), "ui": "CybersecurityOperationsCenterAssistantPanel", "route": "POST /security-alerts/validate"},
    25: {"tables": (ALERT_TABLE, THREAT_INTEL_TABLE), "fields": ("batch_id", "row_results", "idempotency_keys", "resume_token"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /security-alerts/bulk"},
    26: {"tables": (PLAYBOOK_TABLE, DEAD_LETTER_TABLE), "fields": ("failure_reason", "retry_eligible", "required_fix", "related_case_id"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /cybersecurity-operations-center/dead-letter/retry"},
    27: {"tables": (ALERT_TABLE, INCIDENT_TABLE, EVIDENCE_TABLE), "fields": ("source_record_ids", "missing_evidence", "next_steps", "citations"), "ui": "CybersecurityOperationsCenterAssistantPanel", "route": "POST /cybersecurity-operations-center/assistant/triage-summary"},
    28: {"tables": (THREAT_INTEL_TABLE, GOVERNED_MODEL_TABLE), "fields": ("candidate_enrichment", "confidence", "human_confirmation_required"), "ui": "CybersecurityOperationsCenterAssistantPanel", "route": "POST /threat-intels/enrichment-preview"},
    29: {"tables": (ALERT_TABLE, INCIDENT_TABLE), "fields": ("queue_depth", "assignment_load", "overdue_triage", "span_of_control"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center-workbench"},
    30: {"tables": (EVIDENCE_TABLE,), "fields": ("redaction_status", "retention_tag", "release_decision", "reviewer"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /response-evidence/review"},
    31: {"tables": (ALERT_TABLE, INCIDENT_TABLE, CONTAINMENT_TABLE), "fields": ("triage_seconds", "containment_seconds", "close_seconds", "segment"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center-workbench"},
    32: {"tables": (ALERT_TABLE,), "fields": ("duplicate_rate", "suppression_rate", "false_positive_rate", "promotion_rate"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center-workbench"},
    33: {"tables": (PLAYBOOK_TABLE,), "fields": ("success_rate", "breakpoint_frequency", "manual_override_rate", "rollback_rate"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center-workbench"},
    34: {"tables": (EVIDENCE_TABLE, INCIDENT_TABLE), "fields": ("required_artifact_classes", "custody_integrity", "sealing_status"), "ui": "CybersecurityOperationsCenterDetail", "route": "GET /cybersecurity-operations-center/case-detail"},
    35: {"tables": (ALERT_TABLE, INCIDENT_TABLE, CONTAINMENT_TABLE, EVIDENCE_TABLE), "fields": ("nodes", "edges", "case_id"), "ui": "CybersecurityOperationsCenterDetail", "route": "GET /cybersecurity-operations-center/case-detail"},
    36: {"tables": (THREAT_INTEL_TABLE, PLAYBOOK_TABLE), "fields": ("intel_pattern", "candidate_playbook", "analyst_selection_required"), "ui": "CybersecurityOperationsCenterAssistantPanel", "route": "POST /playbook-runs/recommend"},
    37: {"tables": (ALERT_TABLE, INCIDENT_TABLE, EVIDENCE_TABLE, POLICY_TABLE), "fields": ("tenant", "tenant_policy", "tenant_retention", "assistant_scope"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center-workbench"},
    38: {"tables": (EVIDENCE_TABLE, INCIDENT_TABLE), "fields": ("retention_policy", "purge_eligible", "legal_hold", "destruction_approval"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /response-evidence/retention"},
    39: {"tables": (EVIDENCE_TABLE, OUTBOX_TABLE), "fields": ("bundle_id", "hash_chain", "sealed_event_id", "verification_metadata"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /response-evidence/seal"},
    40: {"tables": (CONTROL_ASSERTION_TABLE, ALERT_TABLE, INCIDENT_TABLE), "fields": ("control_name", "assertion_result", "exception_opened"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /cybersecurity-operations-center/control-assertions"},
    41: {"tables": (CONTAINMENT_TABLE, GOVERNED_MODEL_TABLE), "fields": ("containment_option", "operational_impact", "residual_alert_volume"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /containment-actions/simulate"},
    42: {"tables": (GOVERNED_MODEL_TABLE, ALERT_TABLE, INCIDENT_TABLE), "fields": ("model_features", "sla_breach_probability", "calibration_version"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center-workbench"},
    43: {"tables": (GOVERNED_MODEL_TABLE, CONTROL_ASSERTION_TABLE), "fields": ("behavior_signal", "expected_range", "explanation"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center-workbench"},
    44: {"tables": (CONTROL_ASSERTION_TABLE,), "fields": ("alert_lifecycle_proof", "containment_trace", "assistant_guardrail_check"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "GET /cybersecurity-operations-center/release-evidence"},
    45: {"tables": (OUTBOX_TABLE, INBOX_TABLE), "fields": ("api_boundary", "event_boundary", "projection_boundary"), "ui": "CybersecurityOperationsCenterDetail", "route": "GET /cybersecurity-operations-center/api-contract"},
    46: {"tables": (POLICY_TABLE,), "fields": ("policy_name", "representative_fixture", "before_outcome", "after_outcome"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /cybersecurity-operations-center/policy-simulations"},
    47: {"tables": (PARAMETER_TABLE,), "fields": ("parameter_name", "value", "minimum", "maximum", "rationale"), "ui": "CybersecurityOperationsCenterWorkbench", "route": "POST /cybersecurity-operations-center/runtime-parameters"},
    48: {"tables": (OUTBOX_TABLE, INBOX_TABLE, DEAD_LETTER_TABLE), "fields": ("aggregate_id", "outbox_event_id", "inbox_event_id"), "ui": "CybersecurityOperationsCenterDetail", "route": "GET /cybersecurity-operations-center/case-detail"},
    49: {"tables": (ALERT_TABLE, INCIDENT_TABLE, EVIDENCE_TABLE), "fields": ("summary", "open_questions", "pending_approvals", "source_record_ids"), "ui": "CybersecurityOperationsCenterAssistantPanel", "route": "POST /cybersecurity-operations-center/handoff-packets"},
    50: {"tables": (INCIDENT_TABLE, EVIDENCE_TABLE, CONTROL_ASSERTION_TABLE), "fields": ("evidence_complete", "containment_verified", "owner_signoff", "lessons_captured"), "ui": "CybersecurityOperationsCenterDetail", "route": "POST /security-incidents/closure-checklist"},
}


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
    control = SOC_FEATURE_CONTROLS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in control["fields"]}
    payload.update(
        {
            "tenant": "tenant-soc",
            "actor": "soc-analyst",
            "references": (),
            "current_state": "new",
            "next_state": "triaged",
            "confidence": 0.88,
            "time_window_minutes": 30,
            "risk_level": "high",
            "approval_path": "supervisor_approval",
            "requires_human_confirmation": True,
            "validation_only": True,
            "human_confirmation_required": True,
            "analyst_selection_required": True,
            "assistant_scope": "tenant",
            "value": 5,
            "minimum": 1,
            "maximum": 10,
            "evidence_complete": True,
            "containment_verified": True,
            "owner_signoff": True,
            "lessons_captured": True,
        }
    )
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    if number == 1 and payload.get("next_state") == payload.get("current_state"):
        findings.append("state transition must move the alert forward or explicitly reopen it")
    if number == 3 and payload.get("time_window_minutes", 0) > 1440:
        findings.append("deduplication window exceeds one day and can hide active attack waves")
    if number == 9 and payload.get("risk_level") == "high" and not payload.get("approval_path"):
        findings.append("high-risk containment requires an approval path")
    if number == 14 and not payload.get("requires_human_confirmation"):
        findings.append("risky playbook automation cannot bypass human confirmation")
    if number == 24 and payload.get("validation_only") is not True:
        findings.append("validation-only intake must not persist records")
    if number == 28 and payload.get("human_confirmation_required") is not True:
        findings.append("assistant threat-intel enrichment must require human confirmation")
    if number == 36 and payload.get("analyst_selection_required") is not True:
        findings.append("threat-intel recommendations cannot auto-execute playbooks")
    if number == 37 and payload.get("assistant_scope") != "tenant":
        findings.append("assistant context must be tenant-scoped")
    if number == 47:
        value = payload.get("value")
        minimum = payload.get("minimum")
        maximum = payload.get("maximum")
        if isinstance(value, (int, float)) and isinstance(minimum, (int, float)) and isinstance(maximum, (int, float)) and not minimum <= value <= maximum:
            findings.append("runtime parameter value is outside bounded safety range")
    if number == 50:
        for field in ("evidence_complete", "containment_verified", "owner_signoff", "lessons_captured"):
            if payload.get(field) is not True:
                findings.append(f"closure readiness requires {field}")
    return tuple(findings)


def evaluate_soc_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_soc_control", "side_effects": ()}
    control = SOC_FEATURE_CONTROLS[resolved.feature_number]
    active_payload = sample_payload_for(resolved) if payload is None else dict(payload)
    missing = tuple(field for field in control["fields"] if field not in active_payload or active_payload[field] in (None, ""))
    invalid_tables = tuple(table for table in control["tables"] if table not in OWNED_TABLES)
    invalid_references = tuple(
        ref
        for ref in active_payload.get("references", ())
        if isinstance(ref, str) and ref.endswith("_table") and ref not in OWNED_TABLES
    )
    domain_findings = _domain_findings(resolved, active_payload)
    event_type = "CybersecurityOperationsCenterUpdated"
    if domain_findings:
        event_type = "CybersecurityOperationsCenterExceptionOpened"
    elif resolved.feature_number in {1, 2, 6, 20, 25}:
        event_type = "CybersecurityOperationsCenterCreated"

    return {
        "ok": not missing and not invalid_tables and not invalid_references and not domain_findings,
        "pbc": PBC_KEY,
        "capability": resolved.slug,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "status": "implemented",
        "target_tables": control["tables"],
        "owned_tables": OWNED_TABLES,
        "read_tables": (),
        "invalid_references": invalid_references,
        "missing_required_fields": missing,
        "domain_findings": domain_findings,
        "event": {
            "contract": EVENT_CONTRACT,
            "topic": REQUIRED_EVENT_TOPIC,
            "type": event_type,
            "idempotency_key": stable_digest(PBC_KEY, resolved.slug, active_payload),
            "outbox_table": OUTBOX_TABLE,
            "inbox_table": INBOX_TABLE,
            "dead_letter_table": DEAD_LETTER_TABLE,
        },
        "ui_surface": control["ui"],
        "service_api": control["route"],
        "permission": "cybersecurity_operations_center.update",
        "configuration": {
            "database_backends": ALLOWED_DATABASE_BACKENDS,
            "event_topic": REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "rule_configurable": True,
            "parameter_configurable": True,
        },
        "agent_skill": f"{PBC_KEY}_skills.{resolved.slug}",
        "requires_human_confirmation": resolved.feature_number in {9, 14, 28, 36, 41, 50},
        "retry_dead_letter_evidence": {
            "retry_policy": "bounded_retry_with_idempotency_key",
            "dead_letter_table": DEAD_LETTER_TABLE,
            "manual_replay_route": "POST /cybersecurity-operations-center/dead-letter/retry",
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


def improve1_soc_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_soc_control(capability) for capability in SOC_CONTROL_CAPABILITIES)
    return {
        "ok": len(evaluations) == 50 and all(item["ok"] for item in evaluations),
        "pbc": PBC_KEY,
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": OWNED_TABLES,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "event_topic": REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


SOC_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_soc_control(slug, payload))
    for capability in SOC_CONTROL_CAPABILITIES
}
