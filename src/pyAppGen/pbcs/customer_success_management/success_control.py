"""Executable customer success controls for improve1 execution.

Every function here is side-effect free and maps one improve1 success capability
to owned customer-success tables, AppGen-X event metadata, UI/API surfaces,
agent skills, configuration handles, retry/dead-letter evidence, and
traceability artifacts.
"""
from __future__ import annotations

import hashlib
import json
from typing import Callable, Mapping

from .improve1_capabilities import IMPROVE1_CAPABILITIES

PBC_KEY = "customer_success_management"
EVENT_CONTRACT = "AppGen-X"
REQUIRED_EVENT_TOPIC = "pbc.customer_success_management.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
OWNED_TABLES = (
    "customer_success_management_customer_success_account",
    "customer_success_management_success_plan",
    "customer_success_management_onboarding_milestone",
    "customer_success_management_customer_touchpoint",
    "customer_success_management_adoption_signal",
    "customer_success_management_health_score",
    "customer_success_management_health_score_component",
    "customer_success_management_success_playbook",
    "customer_success_management_playbook_task",
    "customer_success_management_customer_escalation",
    "customer_success_management_renewal_motion",
    "customer_success_management_expansion_opportunity",
    "customer_success_management_executive_business_review",
    "customer_success_management_customer_objective",
    "customer_success_management_customer_value_realization",
    "customer_success_management_churn_risk_signal",
    "customer_success_management_success_exception_case",
    "customer_success_management_success_policy_rule",
    "customer_success_management_success_runtime_parameter",
    "customer_success_management_success_schema_extension",
    "customer_success_management_success_control_assertion",
    "customer_success_management_success_governed_model",
    "customer_success_management_appgen_outbox_event",
    "customer_success_management_appgen_inbox_event",
    "customer_success_management_appgen_dead_letter_event",
)
SUCCESS_CONTROL_CAPABILITIES = tuple(capability.slug for capability in IMPROVE1_CAPABILITIES)
SLUG_BY_NUMBER = {capability.feature_number: capability.slug for capability in IMPROVE1_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in IMPROVE1_CAPABILITIES}
FIELD_SETS: tuple[tuple[str, ...], ...] = (
    ("tenant", "customer_projection", "account_identity", "lifecycle_stage", "owner"),
    ("account_id", "current_state", "target_state", "actor", "idempotency_key"),
    ("plan_id", "objectives", "stakeholders", "value_hypotheses", "approval_state"),
    ("milestone_id", "state", "due_date", "dependencies", "required_evidence"),
    ("signal_id", "source", "metric", "timestamp", "component_link"),
    ("score_id", "formula_version", "components", "weights", "score"),
    ("component_id", "source_signals", "trend", "threshold", "recommended_actions"),
    ("factor_id", "causal_factor", "evidence", "confidence", "health_delta"),
    ("risk_id", "risk_type", "severity", "source", "mitigation_owner"),
    ("forecast_id", "account_id", "renewal_window", "probability", "confidence_interval"),
    ("policy_id", "trigger", "thresholds", "playbook", "criteria_explanation"),
    ("playbook_id", "state", "target_segment", "task_template", "version"),
    ("task_id", "assignee", "due_date", "dependency", "completion_proof"),
    ("escalation_id", "state", "severity", "owner", "resolution_evidence"),
    ("analysis_id", "root_cause", "product_area", "corrective_action", "preventive_playbook"),
    ("renewal_id", "state", "renewal_date", "health_gate", "value_evidence"),
    ("simulation_id", "intervention", "probability", "revenue_impact", "assumptions"),
    ("opportunity_id", "adoption_growth", "product_gap", "objective_link", "confidence"),
    ("expansion_id", "state", "hypothesis", "commercial_handoff", "boundary_evidence"),
    ("review_id", "objectives", "value_realization", "adoption_trend", "evidence_links"),
    ("objective_id", "owner", "business_outcome", "baseline", "target"),
    ("value_id", "hypothesis", "realized_metric", "calculation_method", "proof"),
    ("forecast_id", "objective", "adoption_trend", "milestone_progress", "confidence"),
    ("graph_id", "accounts", "objectives", "playbooks", "temporal_edges"),
    ("payment_event", "risk_signal", "playbook_trigger", "health_component", "communication_task"),
    ("ticket_event", "severity", "resolution_time", "sentiment", "health_effect"),
    ("subscription_event", "account_setup", "milestones", "owner_assignment", "baseline_health"),
    ("customer_event", "freshness", "changed_fields", "owner_reassignment", "idempotency_key"),
    ("rule_id", "tenant", "scope", "triggers", "compiled_hash"),
    ("parameter_id", "bounds", "impact_simulation", "approver", "rollback_plan"),
    ("extension_id", "owned_table", "field_validation", "ui_preview", "api_review"),
    ("inbox_id", "schema_version", "idempotency_key", "retry_evidence", "dead_letter_policy"),
    ("outbox_id", "ordering_group", "payload_hash", "retry_attempts", "delivery_proof"),
    ("boundary_id", "dependency", "dependency_mode", "freshness_rule", "retention_rule"),
    ("audit_id", "hash_chain", "decision_records", "event_deliveries", "replay_pointer"),
    ("proof_id", "proof_type", "verifier", "expiry", "selective_disclosure"),
    ("model_id", "purpose", "feature_lineage", "validation_metrics", "approval_status"),
    ("anomaly_id", "signal", "pattern", "risk", "review_state"),
    ("exposure_id", "account", "distribution", "risk_drivers", "mitigation"),
    ("document_id", "document_type", "candidate_facts", "confidence", "preview_state"),
    ("plan_id", "command", "owned_tables", "expected_event", "human_confirmation"),
    ("workbench_id", "panels", "events", "rules", "release_evidence"),
    ("cockpit_id", "health_trend", "components", "source_signals", "remediation_actions"),
    ("room_id", "renewal_date", "value_evidence", "risk_signals", "simulation_output"),
    ("builder_id", "objectives", "value_metrics", "executive_summary", "audit_proof"),
    ("assertion_id", "control_population", "failure_type", "owner", "release_gate"),
    ("drill_id", "failure_mode", "recovery_action", "dead_letter_recovery", "degraded_mode"),
    ("guardrail_id", "customer_value", "unresolved_risk", "expansion_pressure", "approval_policy"),
    ("score_id", "health_ready", "event_health", "boundary_proof", "agent_safety"),
    ("proof_id", "account_to_renewal", "health_to_playbook", "ui_evidence", "boundary_verification"),
)
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = dict(zip(SUCCESS_CONTROL_CAPABILITIES, FIELD_SETS))
CAPABILITY_TABLES = {
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[0] for i in (1, 2, 24, 27, 28, 42, 49, 50)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[1] for i in (3, 20, 40, 41)},
    SLUG_BY_NUMBER[4]: OWNED_TABLES[2], SLUG_BY_NUMBER[5]: OWNED_TABLES[4],
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[5] for i in (6, 8, 10, 23, 43)},
    SLUG_BY_NUMBER[7]: OWNED_TABLES[6],
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[15] for i in (9, 25, 26, 38, 39)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[7] for i in (11, 12)},
    SLUG_BY_NUMBER[13]: OWNED_TABLES[8],
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[9] for i in (14, 15)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[10] for i in (16, 17, 44)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[11] for i in (18, 19, 48)},
    SLUG_BY_NUMBER[21]: OWNED_TABLES[13], SLUG_BY_NUMBER[22]: OWNED_TABLES[14],
    SLUG_BY_NUMBER[29]: OWNED_TABLES[17], SLUG_BY_NUMBER[30]: OWNED_TABLES[18], SLUG_BY_NUMBER[31]: OWNED_TABLES[19],
    SLUG_BY_NUMBER[32]: OWNED_TABLES[23], SLUG_BY_NUMBER[33]: OWNED_TABLES[22], SLUG_BY_NUMBER[34]: OWNED_TABLES[20],
    SLUG_BY_NUMBER[35]: OWNED_TABLES[20], SLUG_BY_NUMBER[36]: OWNED_TABLES[20], SLUG_BY_NUMBER[37]: OWNED_TABLES[21],
    SLUG_BY_NUMBER[45]: OWNED_TABLES[12], SLUG_BY_NUMBER[46]: OWNED_TABLES[20], SLUG_BY_NUMBER[47]: OWNED_TABLES[24],
}
CAPABILITY_EVENTS = {capability: "CustomerSuccess" + "".join(part.capitalize() for part in capability.split("_")) for capability in SUCCESS_CONTROL_CAPABILITIES}
ALLOWED_ACCOUNT_STATES = {"onboarding", "active", "monitored", "growth", "at_risk", "renewal", "suspended", "churned", "archived"}
DECLARED_DEPENDENCY_MODES = {"api", "event", "projection", "package_metadata"}


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _to_float(value: object, default: float = 0.0) -> float:
    try: return float(value)
    except (TypeError, ValueError): return default


def _invalid_references(references: object) -> tuple[str, ...]:
    if not references: return ()
    refs = (references,) if isinstance(references, str) else tuple(str(item) for item in references)
    return tuple(ref for ref in refs if ref.endswith("_table") and ref not in OWNED_TABLES and not ref.startswith(f"{PBC_KEY}_"))


def _base_checks(capability: str, payload: Mapping[str, object]) -> tuple[bool, tuple[str, ...], tuple[str, ...]]:
    missing = tuple(field for field in REQUIRED_FIELDS[capability] if payload.get(field) in (None, "", (), []))
    invalid = _invalid_references(payload.get("referenced_tables", ()))
    return not missing and not invalid, missing, invalid


def _domain_findings(capability: str, payload: Mapping[str, object]) -> tuple[str, ...]:
    findings: list[str] = []
    if capability == SLUG_BY_NUMBER[1] and not payload.get("customer_projection"):
        findings.append("success_account_requires_customer_projection")
    if capability == SLUG_BY_NUMBER[2] and payload.get("target_state") not in ALLOWED_ACCOUNT_STATES:
        findings.append("success_account_lifecycle_state_invalid")
    if capability == SLUG_BY_NUMBER[6] and not payload.get("components"):
        findings.append("health_score_requires_components")
    if capability == SLUG_BY_NUMBER[13] and payload.get("completion_proof") in (None, ""):
        findings.append("playbook_task_requires_completion_proof")
    if capability == SLUG_BY_NUMBER[14] and not payload.get("owner"):
        findings.append("escalation_requires_owner")
    if capability == SLUG_BY_NUMBER[16] and not payload.get("value_evidence"):
        findings.append("renewal_motion_requires_value_evidence")
    if capability == SLUG_BY_NUMBER[29] and not payload.get("compiled_hash"):
        findings.append("success_rule_requires_compiled_hash")
    if capability == SLUG_BY_NUMBER[31] and str(payload.get("owned_table", "")).endswith("_table") and payload.get("owned_table") not in OWNED_TABLES:
        findings.append("schema_extension_must_target_owned_success_table")
    if capability == SLUG_BY_NUMBER[32] and not payload.get("idempotency_key"):
        findings.append("inbox_reliability_requires_idempotency_key")
    if capability == SLUG_BY_NUMBER[34] and payload.get("dependency_mode") not in DECLARED_DEPENDENCY_MODES:
        findings.append("cross_pbc_boundary_must_use_api_event_or_projection")
    if capability == SLUG_BY_NUMBER[40] and _to_float(payload.get("confidence")) < 0.8:
        findings.append("semantic_account_plan_extraction_requires_review")
    if capability == SLUG_BY_NUMBER[41] and payload.get("human_confirmation") is not True:
        findings.append("agent_success_plan_requires_human_confirmation")
    if capability == SLUG_BY_NUMBER[46] and payload.get("failure_type") == "agent_preview_bypass":
        findings.append("continuous_control_blocks_agent_preview_bypass")
    if capability == SLUG_BY_NUMBER[48] and payload.get("unresolved_risk") is True and payload.get("expansion_pressure") == "high":
        findings.append("ethics_guardrail_blocks_expansion_over_unresolved_risk")
    if capability == SLUG_BY_NUMBER[49] and payload.get("agent_safety") is not True:
        findings.append("readiness_score_requires_agent_safety")
    if capability == SLUG_BY_NUMBER[50] and payload.get("boundary_verification") is not True:
        findings.append("end_to_end_success_proof_requires_boundary_verification")
    return tuple(findings)


def evaluate_success_control(capability: str, payload: Mapping[str, object] | None = None) -> dict:
    if capability not in SUCCESS_CONTROL_CAPABILITIES:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_success_control", "side_effects": ()}
    payload = dict(payload or {})
    base_ok, missing, invalid = _base_checks(capability, payload)
    findings = _domain_findings(capability, payload)
    table = CAPABILITY_TABLES[capability]
    meta = CAPABILITY_BY_SLUG[capability]
    return {"ok": base_ok, "pbc": PBC_KEY, "capability": capability, "feature_number": meta.feature_number, "title": meta.title, "status": "ready" if base_ok and not findings else "review_required", "target_table": table, "owned_tables": (table,), "read_tables": (), "invalid_references": invalid, "missing_required_fields": missing, "domain_findings": findings, "event": {"event_type": CAPABILITY_EVENTS[capability], "event_contract": EVENT_CONTRACT, "topic": REQUIRED_EVENT_TOPIC, "idempotency_key": _digest((capability, payload))}, "ui_surface": f"{PBC_KEY}.ui.improve1.{capability}", "service_api": f"{PBC_KEY}.services.{capability}", "route": f"/workbench/pbcs/{PBC_KEY}/improve1/{capability.replace('_', '-')}", "permission": f"{PBC_KEY}.{capability}.operate", "configuration": {"rule_id": f"{capability}_policy", "parameter_id": f"{capability}_parameter", "database_backends": ALLOWED_DATABASE_BACKENDS}, "agent_skill": f"{PBC_KEY}_skills.{capability}", "requires_human_confirmation": bool(findings or "agent" in capability or "renewal" in capability or "expansion" in capability), "retry_dead_letter_evidence": {"inbox_table": "customer_success_management_appgen_inbox_event", "dead_letter_table": "customer_success_management_appgen_dead_letter_event", "max_attempts": 5}, "release_evidence": {"code_artifact": "customer_success_management/success_control.py", "ui_artifact": "customer_success_management/ui.py", "service_artifact": "customer_success_management/services.py", "test_artifact": "customer_success_management/tests/test_domain_behavior.py", "traceability": "customer_success_management/IMPROVE1_TRACEABILITY.md"}, "stream_engine_picker_visible": False, "shared_table_access": False, "side_effects": ()}


def sample_payload_for(capability: str) -> dict:
    if capability not in SUCCESS_CONTROL_CAPABILITIES: raise KeyError(capability)
    payload = {field: f"{field}_evidence" for field in REQUIRED_FIELDS[capability]}
    payload["referenced_tables"] = (CAPABILITY_TABLES[capability],)
    if capability == SLUG_BY_NUMBER[1]: payload["customer_projection"] = "customer_projection"
    if capability == SLUG_BY_NUMBER[2]: payload["target_state"] = "active"
    if capability == SLUG_BY_NUMBER[6]: payload["components"] = ("adoption", "support", "billing")
    if capability == SLUG_BY_NUMBER[13]: payload["completion_proof"] = "call-notes"
    if capability == SLUG_BY_NUMBER[14]: payload["owner"] = "csm.owner"
    if capability == SLUG_BY_NUMBER[16]: payload["value_evidence"] = "roi-summary"
    if capability == SLUG_BY_NUMBER[29]: payload["compiled_hash"] = "sha256:rule"
    if capability == SLUG_BY_NUMBER[31]: payload["owned_table"] = "customer_success_management_customer_success_account"
    if capability == SLUG_BY_NUMBER[32]: payload["idempotency_key"] = "customer-updated-1"
    if capability == SLUG_BY_NUMBER[34]: payload["dependency_mode"] = "event"
    if capability == SLUG_BY_NUMBER[40]: payload["confidence"] = 0.91
    if capability == SLUG_BY_NUMBER[41]: payload["human_confirmation"] = True
    if capability == SLUG_BY_NUMBER[46]: payload["failure_type"] = "none"
    if capability == SLUG_BY_NUMBER[48]: payload.update({"unresolved_risk": False, "expansion_pressure": "moderate"})
    if capability == SLUG_BY_NUMBER[49]: payload["agent_safety"] = True
    if capability == SLUG_BY_NUMBER[50]: payload["boundary_verification"] = True
    return payload


def _make_runner(capability: str) -> Callable[[Mapping[str, object] | None], dict]:
    def runner(payload: Mapping[str, object] | None = None) -> dict:
        return evaluate_success_control(capability, payload)
    runner.__name__ = f"run_{capability}"
    return runner

for _capability in SUCCESS_CONTROL_CAPABILITIES:
    globals()[f"run_{_capability}"] = _make_runner(_capability)

SUCCESS_CONTROL_FUNCTIONS: Mapping[str, Callable[[Mapping[str, object] | None], dict]] = {capability: globals()[f"run_{capability}"] for capability in SUCCESS_CONTROL_CAPABILITIES}


def improve1_success_control_contract() -> dict:
    samples = tuple(SUCCESS_CONTROL_FUNCTIONS[capability](sample_payload_for(capability)) for capability in SUCCESS_CONTROL_CAPABILITIES)
    return {"format": "appgen.customer-success-management.improve1-success-control.v1", "ok": len(samples) == 50 and all(item["ok"] for item in samples), "pbc": PBC_KEY, "capability_count": len(SUCCESS_CONTROL_CAPABILITIES), "capabilities": SUCCESS_CONTROL_CAPABILITIES, "owned_tables": OWNED_TABLES, "event_contract": EVENT_CONTRACT, "database_backends": ALLOWED_DATABASE_BACKENDS, "stream_engine_picker_visible": False, "shared_table_access": False, "samples": samples, "side_effects": ()}
