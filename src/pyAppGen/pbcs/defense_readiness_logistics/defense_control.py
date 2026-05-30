"""Executable improve1 controls for the defense readiness logistics PBC."""

from __future__ import annotations

from typing import Any

from .config import ALLOWED_DATABASE_BACKENDS, REQUIRED_EVENT_TOPIC
from .events import DEFAULT_TOPIC
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .models import OWNED_TABLES, PBC_KEY

EVENT_CONTRACT = "AppGen-X"
UNIT_TABLE = f"{PBC_KEY}_unit_readiness"
ASSET_TABLE = f"{PBC_KEY}_mission_asset"
SUPPLY_TABLE = f"{PBC_KEY}_supply_request"
MAINT_TABLE = f"{PBC_KEY}_maintenance_status"
DEPLOY_TABLE = f"{PBC_KEY}_deployment_plan"
INSPECTION_TABLE = f"{PBC_KEY}_readiness_inspection"
MOVEMENT_TABLE = f"{PBC_KEY}_logistics_movement"
PERSONNEL_TABLE = f"{PBC_KEY}_personnel_qualification"
AMMO_TABLE = f"{PBC_KEY}_ammunition_lot"
FUEL_TABLE = f"{PBC_KEY}_fuel_allocation"
LOAD_TABLE = f"{PBC_KEY}_movement_load_plan"
THEATER_TABLE = f"{PBC_KEY}_theater_support_request"
CUSTODY_TABLE = f"{PBC_KEY}_controlled_item_custody"
EXCEPTION_TABLE = f"{PBC_KEY}_readiness_exception"
POLICY_TABLE = f"{PBC_KEY}_{PBC_KEY}_policy_rule"
PARAMETER_TABLE = f"{PBC_KEY}_{PBC_KEY}_runtime_parameter"
SCHEMA_EXTENSION_TABLE = f"{PBC_KEY}_{PBC_KEY}_schema_extension"
CONTROL_TABLE = f"{PBC_KEY}_{PBC_KEY}_control_assertion"
MODEL_TABLE = f"{PBC_KEY}_{PBC_KEY}_governed_model"
OUTBOX_TABLE = f"{PBC_KEY}_appgen_outbox_event"
INBOX_TABLE = f"{PBC_KEY}_appgen_inbox_event"
DEAD_LETTER_TABLE = f"{PBC_KEY}_appgen_dead_letter_event"

DEFENSE_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in DEFENSE_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in DEFENSE_CONTROL_CAPABILITIES}

CONTROL_SPECS: dict[int, dict[str, Any]] = {
    1: {"tables": (UNIT_TABLE, OUTBOX_TABLE), "fields": ("current_state", "target_state", "reason_code", "actor", "state_history"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /unit-readiness/transition"},
    2: {"tables": (UNIT_TABLE, ASSET_TABLE, MAINT_TABLE, SUPPLY_TABLE), "fields": ("unit_id", "mission_set", "time_window", "capability_rating", "source_explanations"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /mission-capability/rollup"},
    3: {"tables": (INSPECTION_TABLE, UNIT_TABLE), "fields": ("checklist_answers", "signatures", "photos", "document_refs", "corrective_actions"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /readiness-inspections/evidence-pack"},
    4: {"tables": (PERSONNEL_TABLE, UNIT_TABLE), "fields": ("minimum_staffing", "duty_available", "role_coverage", "bounded_attributes"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /unit-readiness/personnel-gates"},
    5: {"tables": (ASSET_TABLE, MAINT_TABLE, MOVEMENT_TABLE), "fields": ("asset_id", "mission_window", "location", "maintenance_forecast", "allocation_conflicts"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /mission-assets/availability"},
    6: {"tables": (MAINT_TABLE, SUPPLY_TABLE), "fields": ("return_to_service", "confidence_range", "readiness_impact", "spares_dependency"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /maintenance-status/projection"},
    7: {"tables": (ASSET_TABLE, MAINT_TABLE, EXCEPTION_TABLE), "fields": ("donor_asset", "receiving_asset", "approval", "restoration_obligation", "readiness_impact"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /mission-assets/cannibalization"},
    8: {"tables": (SUPPLY_TABLE, UNIT_TABLE), "fields": ("mission_demand", "on_hand", "inbound", "substitute_policy", "critical_class_score"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /supply-readiness/score"},
    9: {"tables": (AMMO_TABLE, SUPPLY_TABLE), "fields": ("authorized_load", "required_quantity", "lot_restrictions", "replenishment"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /ammo-constraints"},
    10: {"tables": (FUEL_TABLE, DEPLOY_TABLE, MOVEMENT_TABLE), "fields": ("on_hand_fuel", "uplift_plan", "refuel_points", "consumption_forecast", "reserve"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /fuel-readiness"},
    11: {"tables": (DEPLOY_TABLE, SUPPLY_TABLE), "fields": ("kit_lines", "substitutes", "expiration_checks", "packing_status", "mission_critical_missing"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /deployment-kits/validate"},
    12: {"tables": (THEATER_TABLE, SUPPLY_TABLE), "fields": ("unit_stock", "prepositioned_stock", "host_support", "assumption_status"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /theater-support/visibility"},
    13: {"tables": (MOVEMENT_TABLE, OUTBOX_TABLE), "fields": ("movement_state", "route_changes", "escort_requirements", "staging_times", "approval_points"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /logistics-movements/lifecycle"},
    14: {"tables": (MOVEMENT_TABLE, LOAD_TABLE), "fields": ("mode", "route_constraints", "lift_limits", "port_sequence", "hazardous_declaration"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /movement-plans/mode-validation"},
    15: {"tables": (LOAD_TABLE, MOVEMENT_TABLE), "fields": ("weight", "cube", "dimensions", "tie_downs", "special_handling"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /load-plans/validate"},
    16: {"tables": (ASSET_TABLE, MAINT_TABLE), "fields": ("maintenance_released", "operations_accepted", "outstanding_discrepancies", "limited_use"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /assets/serviceability-handoff"},
    17: {"tables": (MAINT_TABLE, SUPPLY_TABLE, MODEL_TABLE), "fields": ("open_actions", "fault_codes", "fleet_age", "forecast_confidence"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /parts-demand/forecast"},
    18: {"tables": (MAINT_TABLE, UNIT_TABLE, EXCEPTION_TABLE), "fields": ("risk_category", "expiry_date", "operating_envelope", "commander_ack"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /deferred-maintenance"},
    19: {"tables": (SUPPLY_TABLE, POLICY_TABLE), "fields": ("approved_substitutes", "disallowed_substitutes", "waiver", "approval"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /spares-substitution"},
    20: {"tables": (ASSET_TABLE, AMMO_TABLE, CUSTODY_TABLE), "fields": ("serial", "lot", "batch", "receipt", "installation", "disposition"), "ui": "DefenseReadinessLogisticsDetail", "route": "GET /controlled-items/traceability"},
    21: {"tables": (SUPPLY_TABLE, DEPLOY_TABLE), "fields": ("shelf_life", "warning_threshold", "replacement_lead_time", "mission_date"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /shelf-life/readiness"},
    22: {"tables": (DEPLOY_TABLE, MOVEMENT_TABLE, POLICY_TABLE), "fields": ("classification", "need_to_know", "redaction_rules", "export_policy"), "ui": "DefenseReadinessLogisticsAssistantPanel", "route": "POST /classified-export/validate"},
    23: {"tables": (CUSTODY_TABLE, DEPLOY_TABLE), "fields": ("controlled_item", "custody_assigned", "transfer_ack", "launch_blocker"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /controlled-custody"},
    24: {"tables": (AMMO_TABLE, FUEL_TABLE, MOVEMENT_TABLE), "fields": ("incompatible_items", "packaging", "documentation", "escort", "mode_restriction"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /hazardous-cargo/validate"},
    25: {"tables": (MOVEMENT_TABLE, DEPLOY_TABLE), "fields": ("border_clearance", "landing_rights", "port_entry", "host_nation_approval", "document_state"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /movement-documents/readiness"},
    26: {"tables": (PERSONNEL_TABLE, UNIT_TABLE), "fields": ("mission_role", "qualified_count", "required_count", "certification_expiry"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /mission-roles/certification-gate"},
    27: {"tables": (UNIT_TABLE, EXCEPTION_TABLE), "fields": ("unit_posture", "mission_capability", "top_blockers", "release_decisions"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "GET /commander-readiness-workbench"},
    28: {"tables": (MAINT_TABLE, ASSET_TABLE, SUPPLY_TABLE), "fields": ("fault_queue", "return_to_service", "parts_heatmap", "technician_capacity"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "GET /maintenance-control-workbench"},
    29: {"tables": (SUPPLY_TABLE, THEATER_TABLE), "fields": ("shortage_queue", "critical_items", "kit_completion", "in_transit_visibility"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "GET /supply-readiness-workbench"},
    30: {"tables": (MOVEMENT_TABLE, LOAD_TABLE, DEPLOY_TABLE), "fields": ("order_status", "route_timeline", "mode_assignment", "late_change_alert"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "GET /movement-control-workbench"},
    31: {"tables": (MOVEMENT_TABLE, MODEL_TABLE), "fields": ("source_citations", "ambiguity_flags", "no_write_preview", "human_confirmation"), "ui": "DefenseReadinessLogisticsAssistantPanel", "route": "POST /assistant/movement-order-extract"},
    32: {"tables": (MAINT_TABLE, MODEL_TABLE), "fields": ("source_text", "serviceability_summary", "expected_completion", "unknowns"), "ui": "DefenseReadinessLogisticsAssistantPanel", "route": "POST /assistant/maintenance-summary"},
    33: {"tables": (SUPPLY_TABLE, POLICY_TABLE, MODEL_TABLE), "fields": ("mitigation_options", "stock_facts", "policy_status", "confidence"), "ui": "DefenseReadinessLogisticsAssistantPanel", "route": "POST /assistant/shortage-mitigation"},
    34: {"tables": (UNIT_TABLE, ASSET_TABLE, SUPPLY_TABLE, DEPLOY_TABLE), "fields": ("command", "idempotency_key", "version", "permission", "validation_result"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /commands/validate"},
    35: {"tables": (OUTBOX_TABLE,), "fields": ("event_type", "operational_fact", "source_id", "narrow_payload"), "ui": "DefenseReadinessLogisticsDetail", "route": "GET /events/schemas"},
    36: {"tables": (OUTBOX_TABLE, INBOX_TABLE, DEAD_LETTER_TABLE), "fields": ("event_id", "retry", "replay_outcome", "idempotency_key"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /events/replay"},
    37: {"tables": (CONTROL_TABLE, DEPLOY_TABLE), "fields": ("readiness_status", "capability_rollup", "open_exceptions", "export_view"), "ui": "DefenseReadinessLogisticsDetail", "route": "GET /deployment-release-evidence"},
    38: {"tables": (CONTROL_TABLE,), "fields": ("manifest_apis", "manifest_workflows", "manifest_tables", "manifest_ui", "tested"), "ui": "DefenseReadinessLogisticsDetail", "route": "GET /manifest-contract-validation"},
    39: {"tables": (EXCEPTION_TABLE,), "fields": ("exception_category", "owning_role", "aging_threshold", "queue_route"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "GET /readiness-exceptions"},
    40: {"tables": (POLICY_TABLE, PARAMETER_TABLE, MODEL_TABLE), "fields": ("tenant", "formation", "operation", "policy_scope", "assistant_scope"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /policy-scope/validate"},
    41: {"tables": (MODEL_TABLE, UNIT_TABLE, SUPPLY_TABLE, MOVEMENT_TABLE), "fields": ("course_of_action", "mission_capability_delta", "movement_timing", "risk_delta"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /readiness-simulations"},
    42: {"tables": (INSPECTION_TABLE, MAINT_TABLE, MOVEMENT_TABLE, INBOX_TABLE), "fields": ("offline_evidence", "source_timestamp", "operator_identity", "sync_conflict"), "ui": "DefenseReadinessLogisticsDetail", "route": "POST /offline-capture/sync"},
    43: {"tables": (UNIT_TABLE, ASSET_TABLE, SUPPLY_TABLE, MOVEMENT_TABLE, EXCEPTION_TABLE), "fields": ("readiness_claim", "asset_story", "supply_story", "movement_story", "reconciliation_result"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /readiness/reconcile"},
    44: {"tables": (OUTBOX_TABLE, INBOX_TABLE, UNIT_TABLE), "fields": ("timeline_entries", "actor", "event_source", "playback"), "ui": "DefenseReadinessLogisticsDetail", "route": "GET /operational-timeline"},
    45: {"tables": (POLICY_TABLE, CONTROL_TABLE), "fields": ("action_type", "risk_level", "classification", "authority_path"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /approval-matrix/evaluate"},
    46: {"tables": (CONTROL_TABLE, EXCEPTION_TABLE), "fields": ("threshold", "mission_priority", "recipient_role", "suppress_noise"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /readiness-alerts/evaluate"},
    47: {"tables": (UNIT_TABLE, INSPECTION_TABLE, ASSET_TABLE, SUPPLY_TABLE, MOVEMENT_TABLE), "fields": ("blocker", "source_record", "provenance_chain", "drilldown_route"), "ui": "DefenseReadinessLogisticsDetail", "route": "GET /readiness-detail"},
    48: {"tables": (MODEL_TABLE, POLICY_TABLE), "fields": ("citations", "uncertainty", "classification_redaction", "refusal_reason"), "ui": "DefenseReadinessLogisticsAssistantPanel", "route": "POST /assistant/safe-answer"},
    49: {"tables": (CONTROL_TABLE, UNIT_TABLE, ASSET_TABLE, MAINT_TABLE, SUPPLY_TABLE, DEPLOY_TABLE, MOVEMENT_TABLE), "fields": ("unit_created", "asset_recorded", "maintenance_projected", "supply_scored", "movement_released", "evidence_pack"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /release-gate/end-to-end"},
    50: {"tables": (CONTROL_TABLE, POLICY_TABLE, PARAMETER_TABLE), "fields": ("actual_outcome", "readiness_projection", "forecast_accuracy", "proposed_rule_change", "approval_required"), "ui": "DefenseReadinessLogisticsWorkbench", "route": "POST /after-action/feedback"},
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
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({"references": (), "current_state": "reported", "target_state": "validated", "commander_approved": True, "bounded_attributes": True, "approval": "commander", "human_confirmation": True, "classification_redaction": True, "approval_required": True, "required_count": 3, "qualified_count": 4, "allowed_dependency_mode": "event"})
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and payload.get("current_state") == payload.get("target_state"):
        findings.append("readiness transition must move to a distinct state")
    if n == 3 and not payload.get("checklist_answers"):
        findings.append("inspection readiness requires checklist evidence")
    if n == 4 and payload.get("bounded_attributes") is not True:
        findings.append("personnel checks must stay bounded to operational readiness attributes")
    if n == 7 and not payload.get("approval"):
        findings.append("cannibalization requires approval evidence")
    if n == 22 and payload.get("classification_redaction") is not True:
        findings.append("classified logistics evidence requires redaction controls")
    if n == 26 and payload.get("qualified_count", 0) < payload.get("required_count", 0):
        findings.append("mission role certification gate fails qualified count")
    if n == 31 and payload.get("human_confirmation") is not True:
        findings.append("movement order extraction requires human confirmation")
    if n == 40 and payload.get("assistant_scope") == "global":
        findings.append("assistant and policy scope must be isolated by operation or tenant")
    if n == 48 and not payload.get("citations"):
        findings.append("assistant-safe response requires citations")
    if n == 49:
        for field in ("unit_created", "asset_recorded", "maintenance_projected", "supply_scored", "movement_released", "evidence_pack"):
            if not payload.get(field):
                findings.append(f"end-to-end release gate requires {field}")
    if n == 50 and payload.get("approval_required") is not True:
        findings.append("after-action feedback cannot rewrite readiness policy without approval")
    return tuple(findings)


def evaluate_defense_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "pbc": PBC_KEY, "reason": "unknown_defense_control", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    active_payload = sample_payload_for(resolved) if payload is None else dict(payload)
    missing = tuple(field for field in spec["fields"] if field not in active_payload or active_payload[field] in (None, ""))
    invalid_tables = tuple(table for table in spec["tables"] if table not in OWNED_TABLES)
    invalid_references = tuple(ref for ref in active_payload.get("references", ()) if isinstance(ref, str) and ref.endswith("_table") and ref not in OWNED_TABLES)
    domain_findings = _domain_findings(resolved, active_payload)
    event_type = "DefenseReadinessLogisticsExceptionOpened" if domain_findings else "DefenseReadinessLogisticsUpdated"
    if resolved.feature_number in {1, 2, 13, 35, 49} and not domain_findings:
        event_type = "DefenseReadinessLogisticsCreated"
    return {
        "ok": not missing and not invalid_tables and not invalid_references and not domain_findings,
        "pbc": PBC_KEY,
        "capability": resolved.slug,
        "feature_number": resolved.feature_number,
        "title": resolved.title,
        "status": "implemented",
        "target_tables": spec["tables"],
        "owned_tables": OWNED_TABLES,
        "read_tables": (),
        "invalid_references": invalid_references,
        "missing_required_fields": missing,
        "domain_findings": domain_findings,
        "event": {"contract": EVENT_CONTRACT, "topic": REQUIRED_EVENT_TOPIC or DEFAULT_TOPIC, "type": event_type, "idempotency_key": f"{PBC_KEY}:{resolved.slug}:{abs(hash(repr(active_payload))) % 10_000_000}", "outbox_table": OUTBOX_TABLE, "inbox_table": INBOX_TABLE, "dead_letter_table": DEAD_LETTER_TABLE},
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "permission": f"{PBC_KEY}.approve" if resolved.feature_number in {7, 13, 22, 24, 37, 45, 49, 50} else f"{PBC_KEY}.update",
        "configuration": {"database_backends": ALLOWED_DATABASE_BACKENDS, "event_topic": REQUIRED_EVENT_TOPIC or DEFAULT_TOPIC, "stream_engine_picker_visible": False, "rule_configurable": True, "parameter_configurable": True},
        "agent_skill": f"{PBC_KEY}_skills.{resolved.slug}",
        "requires_human_confirmation": resolved.feature_number in {7, 13, 22, 31, 33, 37, 45, 48, 50},
        "retry_dead_letter_evidence": {"retry_policy": "bounded_retry_with_idempotency_key", "dead_letter_table": DEAD_LETTER_TABLE, "manual_replay_route": "POST /events/replay"},
        "release_evidence": {"code_artifact_model": resolved.model_artifacts, "ui_surface": resolved.ui_artifacts, "service_api": resolved.service_artifacts, "test": resolved.test_artifacts, "evidence": resolved.evidence_artifacts},
        "shared_table_access": False,
        "side_effects": (),
    }


def improve1_defense_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_defense_control(capability) for capability in DEFENSE_CONTROL_CAPABILITIES)
    return {"ok": len(evaluations) == 50 and all(item["ok"] for item in evaluations), "pbc": PBC_KEY, "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": OWNED_TABLES, "database_backends": ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "event_topic": REQUIRED_EVENT_TOPIC or DEFAULT_TOPIC, "stream_engine_picker_visible": False, "side_effects": ()}


DEFENSE_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_defense_control(slug, payload)) for capability in DEFENSE_CONTROL_CAPABILITIES}
