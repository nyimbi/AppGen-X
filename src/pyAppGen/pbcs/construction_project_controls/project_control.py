"""Executable construction project controls for improve1 execution.

The functions in this module are side-effect free. They bind every improve1
capability to owned project-control tables, AppGen-X events, UI/API surfaces,
agent skills, configuration handles, retry/dead-letter evidence, and package
traceability artifacts.
"""

from __future__ import annotations

import hashlib
import json
from typing import Callable, Mapping

from .improve1_capabilities import IMPROVE1_CAPABILITIES

PBC_KEY = "construction_project_controls"
EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "construction_project_controls_construction_project",
    "construction_project_controls_work_package",
    "construction_project_controls_rfi",
    "construction_project_controls_submittal",
    "construction_project_controls_site_progress",
    "construction_project_controls_change_event",
    "construction_project_controls_schedule_risk",
    "construction_project_controls_construction_project_controls_policy_rule",
    "construction_project_controls_construction_project_controls_runtime_parameter",
    "construction_project_controls_construction_project_controls_schema_extension",
    "construction_project_controls_construction_project_controls_control_assertion",
    "construction_project_controls_construction_project_controls_governed_model",
    "construction_project_controls_appgen_outbox_event",
    "construction_project_controls_appgen_inbox_event",
    "construction_project_controls_appgen_dead_letter_event",
)
PROJECT_CONTROL_CAPABILITIES = tuple(capability.slug for capability in IMPROVE1_CAPABILITIES)
SLUG_BY_NUMBER = {capability.feature_number: capability.slug for capability in IMPROVE1_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in IMPROVE1_CAPABILITIES}
FIELD_SETS: tuple[tuple[str, ...], ...] = (
    ("project_id", "wbs_code", "parent_wbs_code", "control_account", "rollup_method"),
    ("project_id", "baseline_version", "approved_by", "freeze_reason", "effective_date"),
    ("work_package_id", "measurement_method", "planned_quantity", "installed_quantity", "evidence_bundle"),
    ("work_package_id", "planned_value", "earned_value", "actual_cost", "forecast_at_completion"),
    ("work_package_id", "commitment_value", "actual_cost", "remaining_cost", "cost_cutoff"),
    ("project_id", "etc_method", "etc_value", "eac_value", "confidence_band"),
    ("trend_id", "change_event_id", "cost_impact", "time_impact", "approval_state"),
    ("trend_id", "source_notice", "potential_cost", "potential_delay_days", "owner"),
    ("submission_id", "contractor", "work_package_id", "measurement_date", "evidence_bundle"),
    ("schedule_update_id", "data_date", "logic_check", "open_ends", "negative_float_count"),
    ("activity_id", "current_float_days", "prior_float_days", "critical_path", "mitigation_owner"),
    ("project_id", "lookahead_window", "constraint_count", "ready_work_count", "owner"),
    ("rfi_id", "work_package_id", "schedule_activity", "impact_assessment", "required_answer_date"),
    ("submittal_id", "work_package_id", "approval_state", "constraint_date", "approver"),
    ("risk_id", "issue_id", "register_type", "probability", "impact"),
    ("scenario_id", "baseline_version", "recovery_actions", "cost_delta", "finish_delta_days"),
    ("period_id", "project_id", "cutoff_timestamp", "freeze_owner", "status"),
    ("calendar_id", "weighting_rule", "measurement_unit", "precision", "approval_state"),
    ("progress_id", "evidence_bundle", "source_timestamp", "reviewer", "audit_hash"),
    ("milestone_id", "work_package_id", "valuation_basis", "earned_amount", "approval_state"),
    ("benchmark_id", "work_package_id", "unit_rate", "productivity_index", "comparison_set"),
    ("project_id", "wbs_code", "dashboard_level", "rollup_metric", "drilldown_target"),
    ("portfolio_id", "baseline_health", "risk_exposure", "forecast_variance", "executive_owner"),
    ("persona", "queue", "project_id", "visible_actions", "exception_count"),
    ("variance_id", "source_metrics", "citations", "narrative", "human_approval"),
    ("change_event_id", "impacted_wbs", "cost_impact", "time_impact", "source_citations"),
    ("triage_id", "record_type", "due_date", "impact_level", "recommended_action"),
    ("api_contract", "baseline_route", "forecast_route", "dashboard_route", "schema_version"),
    ("route_name", "legacy_route", "canonical_route", "handler", "compatibility_test"),
    ("event_type", "schema_version", "payload_fields", "idempotency_key", "topic"),
    ("consumed_event", "handler", "policy_projection", "kpi_projection", "idempotency_key"),
    ("revision_id", "record_type", "prior_hash", "new_hash", "projection_version"),
    ("submission_id", "idempotency_key", "dedupe_scope", "accepted_mutation", "replay_status"),
    ("policy_id", "cost_threshold", "float_threshold", "approval_route", "simulation_result"),
    ("parameter_id", "reporting_calendar", "base_currency", "weighting_logic", "tenant_scope"),
    ("assertion_id", "control_population", "failing_records", "exception_owner", "remediation_due"),
    ("anomaly_id", "claim_type", "signal", "review_state", "model_version"),
    ("extension_id", "snapshot_type", "snapshot_hash", "source_record_range", "schema_version"),
    ("document_id", "document_type", "source_spans", "draft_action", "confirmation_state"),
    ("tenant_id", "project_id", "contractor_scope", "access_model", "event_scope"),
    ("proof_id", "reporting_period", "bundle_hash", "signature", "published_at"),
    ("release_pack_id", "api_evidence", "event_evidence", "ui_evidence", "known_limitations"),
    ("role", "action", "threshold", "permission", "denial_reason"),
    ("dependency_name", "dependency_mode", "authoritative_record", "inbound_contract", "outbound_contract"),
    ("forecast_id", "confidence_band", "principal_drivers", "exposure_amount", "risk_links"),
    ("change_event_id", "liability_class", "cost_dimension", "time_dimension", "responsibility_party"),
    ("project_id", "closeout_state", "punch_status", "final_account_status", "archive_blockers"),
    ("scenario_id", "scenario_type", "linked_records", "dashboard_signature", "regression_case"),
    ("contract_id", "route_checks", "event_schema_checks", "ui_fragment_checks", "failure_key"),
    ("scorecard_id", "data_model_ready", "api_ready", "event_ready", "control_pass_rate"),
)
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = dict(zip(PROJECT_CONTROL_CAPABILITIES, FIELD_SETS))
CAPABILITY_TABLES = {
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[1] for i in (1, 3, 4, 5, 13, 20, 21, 22)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[0] for i in (2, 6, 12, 16, 17, 23, 24, 40, 47, 48, 50)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[5] for i in (7, 8, 26, 46)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[4] for i in (9, 18, 19, 25, 33, 37)},
    **{SLUG_BY_NUMBER[i]: OWNED_TABLES[6] for i in (10, 11, 15, 27, 45)},
    SLUG_BY_NUMBER[14]: OWNED_TABLES[3],
    SLUG_BY_NUMBER[28]: OWNED_TABLES[11],
    SLUG_BY_NUMBER[29]: OWNED_TABLES[11],
    SLUG_BY_NUMBER[30]: OWNED_TABLES[12],
    SLUG_BY_NUMBER[31]: OWNED_TABLES[13],
    SLUG_BY_NUMBER[32]: OWNED_TABLES[10],
    SLUG_BY_NUMBER[34]: OWNED_TABLES[7],
    SLUG_BY_NUMBER[35]: OWNED_TABLES[8],
    SLUG_BY_NUMBER[36]: OWNED_TABLES[10],
    SLUG_BY_NUMBER[38]: OWNED_TABLES[9],
    SLUG_BY_NUMBER[39]: OWNED_TABLES[11],
    SLUG_BY_NUMBER[41]: OWNED_TABLES[10],
    SLUG_BY_NUMBER[42]: OWNED_TABLES[10],
    SLUG_BY_NUMBER[43]: OWNED_TABLES[7],
    SLUG_BY_NUMBER[44]: OWNED_TABLES[13],
    SLUG_BY_NUMBER[49]: OWNED_TABLES[10],
}
CAPABILITY_EVENTS = {
    capability: "ConstructionProjectControls" + "".join(part.capitalize() for part in capability.split("_"))
    for capability in PROJECT_CONTROL_CAPABILITIES
}
ALLOWED_MEASUREMENT_METHODS = {"quantity_installed", "weighted_steps", "physical_percent", "milestone"}
DECLARED_DEPENDENCY_MODES = {"api", "event", "projection", "package_metadata"}
AUTHORIZED_ROLES = {"project_engineer", "scheduler", "cost_engineer", "project_controls_manager", "project_director", "executive", "auditor", "admin"}
ALLOWED_LIABILITY_CLASSES = {"compensable", "non_compensable", "pending_liability"}


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _to_float(value: object, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _invalid_references(references: object) -> tuple[str, ...]:
    if not references:
        return ()
    refs = (references,) if isinstance(references, str) else tuple(str(item) for item in references)
    return tuple(ref for ref in refs if ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_"))


def _base_checks(capability: str, payload: Mapping[str, object]) -> tuple[bool, tuple[str, ...], tuple[str, ...]]:
    missing = tuple(field for field in REQUIRED_FIELDS[capability] if payload.get(field) in (None, "", (), []))
    invalid = _invalid_references(payload.get("referenced_tables", ()))
    return not missing and not invalid, missing, invalid


def _domain_findings(capability: str, payload: Mapping[str, object]) -> tuple[str, ...]:
    findings: list[str] = []
    if capability == SLUG_BY_NUMBER[1] and payload.get("parent_wbs_code") == payload.get("wbs_code"):
        findings.append("wbs_cannot_parent_itself")
    if capability == SLUG_BY_NUMBER[2] and payload.get("approved_by") in (None, "draft", ""):
        findings.append("baseline_freeze_requires_authorized_approval")
    if capability == SLUG_BY_NUMBER[3]:
        if payload.get("measurement_method") not in ALLOWED_MEASUREMENT_METHODS:
            findings.append("unsupported_progress_measurement_method")
        if _to_float(payload.get("installed_quantity")) > _to_float(payload.get("planned_quantity")):
            findings.append("installed_quantity_exceeds_plan")
    if capability == SLUG_BY_NUMBER[4] and _to_float(payload.get("planned_value")) <= 0:
        findings.append("earned_value_requires_positive_planned_value")
    if capability == SLUG_BY_NUMBER[6] and payload.get("confidence_band") not in {"low", "medium", "high"}:
        findings.append("forecast_confidence_band_required")
    if capability == SLUG_BY_NUMBER[7] and payload.get("approval_state") != "approved" and (_to_float(payload.get("cost_impact")) or _to_float(payload.get("time_impact"))):
        findings.append("change_impact_cannot_hit_forecast_before_approval")
    if capability == SLUG_BY_NUMBER[9] and not payload.get("evidence_bundle"):
        findings.append("contractor_progress_requires_evidence_bundle")
    if capability == SLUG_BY_NUMBER[10] and _to_float(payload.get("open_ends")) > 0:
        findings.append("schedule_update_has_open_ended_logic")
    if capability == SLUG_BY_NUMBER[11] and _to_float(payload.get("current_float_days")) < 0 and not payload.get("mitigation_owner"):
        findings.append("negative_float_requires_mitigation_owner")
    if capability == SLUG_BY_NUMBER[17] and payload.get("status") != "frozen":
        findings.append("reporting_period_must_freeze_before_publication")
    if capability == SLUG_BY_NUMBER[19] and not payload.get("audit_hash"):
        findings.append("progress_evidence_requires_audit_hash")
    if capability == SLUG_BY_NUMBER[25] and (not payload.get("citations") or payload.get("human_approval") is not True):
        findings.append("assistant_variance_narrative_requires_citations_and_approval")
    if capability == SLUG_BY_NUMBER[29] and payload.get("legacy_route") != "POST /site-progresss":
        findings.append("legacy_site_progresss_alias_missing")
    if capability == SLUG_BY_NUMBER[30] and payload.get("topic") != f"pbc.{PBC_KEY}.events":
        findings.append("typed_event_must_use_appgen_x_topic")
    if capability == SLUG_BY_NUMBER[31] and not payload.get("idempotency_key"):
        findings.append("consumed_event_handler_requires_idempotency_key")
    if capability == SLUG_BY_NUMBER[33] and payload.get("replay_status") not in {"new", "replayed"}:
        findings.append("duplicate_submission_must_return_replay_status")
    if capability == SLUG_BY_NUMBER[34] and _to_float(payload.get("float_threshold")) > 20:
        findings.append("float_policy_threshold_outside_controls_tolerance")
    if capability == SLUG_BY_NUMBER[35] and payload.get("base_currency") in (None, ""):
        findings.append("runtime_parameter_requires_base_currency")
    if capability == SLUG_BY_NUMBER[37] and payload.get("review_state") == "auto_approved":
        findings.append("anomaly_detection_must_route_to_review")
    if capability == SLUG_BY_NUMBER[39] and payload.get("confirmation_state") != "confirmed":
        findings.append("document_instruction_requires_confirmed_preview")
    if capability == SLUG_BY_NUMBER[40] and payload.get("access_model") not in {"tenant_project", "contractor_scoped"}:
        findings.append("tenant_project_isolation_required")
    if capability == SLUG_BY_NUMBER[41] and not payload.get("signature"):
        findings.append("published_pack_requires_cryptographic_signature")
    if capability == SLUG_BY_NUMBER[43] and payload.get("role") not in AUTHORIZED_ROLES:
        findings.append("unauthorized_project_controls_role")
    if capability == SLUG_BY_NUMBER[44] and payload.get("dependency_mode") not in DECLARED_DEPENDENCY_MODES:
        findings.append("adjacent_system_boundary_must_use_api_event_or_projection")
    if capability == SLUG_BY_NUMBER[45] and _to_float(payload.get("exposure_amount")) > 0 and not payload.get("risk_links"):
        findings.append("forecast_exposure_requires_risk_linkage")
    if capability == SLUG_BY_NUMBER[46] and payload.get("liability_class") not in ALLOWED_LIABILITY_CLASSES:
        findings.append("change_liability_classification_required")
    if capability == SLUG_BY_NUMBER[47] and payload.get("archive_blockers") not in (None, "", (), [], "none", "cleared"):
        findings.append("closeout_archive_blocked_by_open_items")
    if capability == SLUG_BY_NUMBER[50] and _to_float(payload.get("control_pass_rate")) < 0.95:
        findings.append("go_live_scorecard_blocks_low_control_pass_rate")
    return tuple(findings)


def evaluate_project_control(capability: str, payload: Mapping[str, object] | None = None) -> dict:
    if capability not in PROJECT_CONTROL_CAPABILITIES:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_project_control", "side_effects": ()}
    payload = dict(payload or {})
    base_ok, missing, invalid = _base_checks(capability, payload)
    findings = _domain_findings(capability, payload)
    table = CAPABILITY_TABLES[capability]
    capability_meta = CAPABILITY_BY_SLUG[capability]
    requires_review = bool(findings or "assistant" in capability or "approval" in capability or payload.get("requires_review"))
    return {
        "ok": base_ok,
        "pbc": PBC_KEY,
        "capability": capability,
        "feature_number": capability_meta.feature_number,
        "title": capability_meta.title,
        "status": "ready" if base_ok and not findings else "review_required",
        "target_table": table,
        "owned_tables": (table,),
        "read_tables": (),
        "invalid_references": invalid,
        "missing_required_fields": missing,
        "domain_findings": findings,
        "event": {
            "event_type": CAPABILITY_EVENTS[capability],
            "event_contract": EVENT_CONTRACT,
            "topic": f"pbc.{PBC_KEY}.events",
            "idempotency_key": _digest((capability, payload)),
        },
        "ui_surface": f"{PBC_KEY}.ui.improve1.{capability}",
        "service_api": f"{PBC_KEY}.services.{capability}",
        "route": f"/workbench/pbcs/{PBC_KEY}/improve1/{capability.replace('_', '-')}",
        "permission": f"{PBC_KEY}.{capability}.operate",
        "configuration": {
            "rule_id": f"{capability}_policy",
            "parameter_id": f"{capability}_parameter",
            "database_backends": ("postgresql", "mysql", "mariadb"),
        },
        "agent_skill": f"{PBC_KEY}_skills.{capability}",
        "requires_human_confirmation": requires_review,
        "retry_dead_letter_evidence": {
            "inbox_table": "construction_project_controls_appgen_inbox_event",
            "dead_letter_table": "construction_project_controls_appgen_dead_letter_event",
            "max_attempts": 5,
        },
        "release_evidence": {
            "code_artifact": "construction_project_controls/project_control.py",
            "ui_artifact": "construction_project_controls/ui.py",
            "service_artifact": "construction_project_controls/services.py",
            "test_artifact": "construction_project_controls/tests/test_domain_behavior.py",
            "traceability": "construction_project_controls/IMPROVE1_TRACEABILITY.md",
        },
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def sample_payload_for(capability: str) -> dict:
    if capability not in PROJECT_CONTROL_CAPABILITIES:
        raise KeyError(capability)
    payload = {field: f"{field}_evidence" for field in REQUIRED_FIELDS[capability]}
    payload["referenced_tables"] = (CAPABILITY_TABLES[capability],)
    if capability == SLUG_BY_NUMBER[1]:
        payload.update({"wbs_code": "1.1", "parent_wbs_code": "1", "rollup_method": "earned_value"})
    if capability == SLUG_BY_NUMBER[2]:
        payload.update({"approved_by": "project_controls_manager", "freeze_reason": "board baseline", "effective_date": "2026-06-01"})
    if capability == SLUG_BY_NUMBER[3]:
        payload.update({"measurement_method": "quantity_installed", "planned_quantity": 100, "installed_quantity": 45, "evidence_bundle": {"photos": 3}})
    if capability == SLUG_BY_NUMBER[4]:
        payload.update({"planned_value": 100000, "earned_value": 45000, "actual_cost": 42000})
    if capability == SLUG_BY_NUMBER[6]:
        payload.update({"confidence_band": "high", "etc_value": 55000, "eac_value": 97000})
    if capability == SLUG_BY_NUMBER[7]:
        payload.update({"approval_state": "approved", "cost_impact": 0, "time_impact": 0})
    if capability == SLUG_BY_NUMBER[10]:
        payload.update({"open_ends": 0, "negative_float_count": 0})
    if capability == SLUG_BY_NUMBER[11]:
        payload.update({"current_float_days": 4, "prior_float_days": 8, "mitigation_owner": "scheduler"})
    if capability == SLUG_BY_NUMBER[17]:
        payload["status"] = "frozen"
    if capability == SLUG_BY_NUMBER[19]:
        payload["audit_hash"] = "sha256:progress-pack"
    if capability == SLUG_BY_NUMBER[25]:
        payload.update({"citations": ("EV-1",), "human_approval": True})
    if capability == SLUG_BY_NUMBER[29]:
        payload.update({"legacy_route": "POST /site-progresss", "canonical_route": "POST /site-progress"})
    if capability == SLUG_BY_NUMBER[30]:
        payload.update({"topic": f"pbc.{PBC_KEY}.events", "payload_fields": ("id", "project_id")})
    if capability == SLUG_BY_NUMBER[31]:
        payload["idempotency_key"] = "policy-evt-1"
    if capability == SLUG_BY_NUMBER[33]:
        payload["replay_status"] = "new"
    if capability == SLUG_BY_NUMBER[34]:
        payload.update({"float_threshold": 10, "cost_threshold": 50000, "approval_route": "project_director"})
    if capability == SLUG_BY_NUMBER[35]:
        payload.update({"base_currency": "USD", "reporting_calendar": "monthly", "tenant_scope": "tenant-project"})
    if capability == SLUG_BY_NUMBER[37]:
        payload.update({"review_state": "needs_review", "model_version": "controls-anomaly-v1"})
    if capability == SLUG_BY_NUMBER[39]:
        payload.update({"source_spans": ("page:1:line:4",), "confirmation_state": "confirmed"})
    if capability == SLUG_BY_NUMBER[40]:
        payload.update({"access_model": "tenant_project", "event_scope": "project"})
    if capability == SLUG_BY_NUMBER[41]:
        payload.update({"signature": "sig-ed25519", "bundle_hash": "sha256:period-pack"})
    if capability == SLUG_BY_NUMBER[43]:
        payload.update({"role": "project_controls_manager", "permission": "approve_baseline"})
    if capability == SLUG_BY_NUMBER[44]:
        payload.update({"dependency_mode": "event", "inbound_contract": "schedule-import.v1", "outbound_contract": "forecast-export.v1"})
    if capability == SLUG_BY_NUMBER[45]:
        payload.update({"confidence_band": "medium", "exposure_amount": 125000, "risk_links": ("RISK-1",)})
    if capability == SLUG_BY_NUMBER[46]:
        payload.update({"liability_class": "compensable", "responsibility_party": "owner"})
    if capability == SLUG_BY_NUMBER[47]:
        payload.update({"archive_blockers": "cleared", "closeout_state": "final_account_ready"})
    if capability == SLUG_BY_NUMBER[50]:
        payload.update({"data_model_ready": True, "api_ready": True, "event_ready": True, "control_pass_rate": 0.99})
    return payload


def _make_runner(capability: str) -> Callable[[Mapping[str, object] | None], dict]:
    def runner(payload: Mapping[str, object] | None = None) -> dict:
        return evaluate_project_control(capability, payload)

    runner.__name__ = f"run_{capability}"
    return runner


for _capability in PROJECT_CONTROL_CAPABILITIES:
    globals()[f"run_{_capability}"] = _make_runner(_capability)

PROJECT_CONTROL_FUNCTIONS: Mapping[str, Callable[[Mapping[str, object] | None], dict]] = {
    capability: globals()[f"run_{capability}"] for capability in PROJECT_CONTROL_CAPABILITIES
}


def improve1_project_control_contract() -> dict:
    samples = tuple(PROJECT_CONTROL_FUNCTIONS[capability](sample_payload_for(capability)) for capability in PROJECT_CONTROL_CAPABILITIES)
    return {
        "format": "appgen.construction-project-controls.improve1-project-control.v1",
        "ok": len(samples) == 50 and all(item["ok"] for item in samples),
        "pbc": PBC_KEY,
        "capability_count": len(PROJECT_CONTROL_CAPABILITIES),
        "capabilities": PROJECT_CONTROL_CAPABILITIES,
        "owned_tables": OWNED_TABLES,
        "event_contract": EVENT_CONTRACT,
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "samples": samples,
        "side_effects": (),
    }
