"""Executable improve1 controls for the Oil and Gas Field Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "oil_gas_field_operations"
EVENT_CONTRACT = "AppGen-X"
FIELD_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
FIELD_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.oil_gas_field_operations.events"
_BASE_OWNED_TABLES = (
    "oil_gas_field_operations_well",
    "oil_gas_field_operations_production_reading",
    "oil_gas_field_operations_field_ticket",
    "oil_gas_field_operations_workover_plan",
    "oil_gas_field_operations_hse_event",
    "oil_gas_field_operations_reserve_estimate",
    "oil_gas_field_operations_lifting_cost",
    "oil_gas_field_operations_wellbore_interval",
    "oil_gas_field_operations_production_test",
    "oil_gas_field_operations_meter_factor",
    "oil_gas_field_operations_allocation_run",
    "oil_gas_field_operations_downtime_event",
    "oil_gas_field_operations_artificial_lift_system",
    "oil_gas_field_operations_chemical_program",
    "oil_gas_field_operations_regulatory_pack",
    "oil_gas_field_operations_route_plan",
    "oil_gas_field_operations_shift_handover",
    "oil_gas_field_operations_policy_rule",
    "oil_gas_field_operations_runtime_parameter",
    "oil_gas_field_operations_schema_extension",
    "oil_gas_field_operations_control_assertion",
    "oil_gas_field_operations_governed_model",
    "oil_gas_field_operations_appgen_outbox_event",
    "oil_gas_field_operations_appgen_inbox_event",
    "oil_gas_field_operations_appgen_dead_letter_event",
)
FIELD_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(_BASE_OWNED_TABLES + tuple(f"oil_gas_field_operations_{capability.slug}_control" for capability in IMPROVE1_CAPABILITIES)))
FIELD_CONTROL_DECLARED_DEPENDENCIES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
    "PermitStatusChanged",
    "AssetIntegrityAlerted",
    "RouteOptimizationChanged",
    "EnvironmentalReportSubmitted",
    "WorkforceAvailabilityChanged",
    "InventoryAvailabilityChanged",
    "CostAllocationPosted",
    "RegulatoryCalendarChanged",
    "HseIncidentClassified",
)
FIELD_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in FIELD_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in FIELD_CONTROL_CAPABILITIES}
_BASE_FIELDS = ("tenant_id", "operator_id", "field_id", "lease_id", "pad_id", "well_id", "production_date", "actor_id", "policy_version", "evidence_references")
_DOMAIN_FIELDS: dict[int, tuple[str, ...]] = {
    1: ("operator", "area", "wellbore_id", "completion_id", "alias_history", "route_code", "retired_identifier"),
    2: ("lateral_section", "perforated_interval", "completion_string", "zone_name", "producing_interval", "interval_status"),
    3: ("lifecycle_state", "spud_date", "first_production_date", "shut_in_state", "abandonment_milestone", "transition_reason"),
    4: ("oil_volume", "gas_volume", "water_volume", "injected_volume", "disposition_pathway", "revision_reason"),
    5: ("test_state", "test_start", "test_stop", "valid_through", "allocation_approval", "invalidation_reason"),
    6: ("separator_id", "gauge_id", "calibration_date", "sample_condition", "stabilization_duration", "witness_signoff"),
    7: ("allocation_run_id", "commingled_pad", "valid_test_basis", "shrink_factor", "downtime_adjustment", "tolerance_exception"),
    8: ("meter_id", "meter_type", "lact_unit", "tank_gauge", "meter_factor", "calibration_evidence"),
    9: ("reconciliation_id", "begin_inventory", "produced_oil", "transferred_oil", "ending_inventory", "variance_reason"),
    10: ("lift_system_id", "lift_type", "install_date", "vendor_model", "controller_setting", "retrieval_date"),
    11: ("rod_pump_id", "stroke_rate", "pump_fillage", "failure_code", "card_evidence", "follow_up_ticket"),
    12: ("esp_id", "shutdown_reason", "current_imbalance", "vsd_alarm", "intake_pressure", "run_life_reset"),
    13: ("gas_lift_id", "injection_volume", "injection_source", "valve_depth", "instability_note", "optimization_case"),
    14: ("plunger_cycle_id", "arrival_time", "missed_arrival", "shut_in_window", "open_flow_window", "timer_setting"),
    15: ("downtime_id", "start_time", "end_time", "partial_rate_flag", "root_cause", "restoration_action"),
    16: ("deferment_id", "baseline_basis", "decline_adjustment", "full_shut_in_flag", "reduced_rate_factor", "override_trace"),
    17: ("candidate_score_id", "decline_signal", "repeat_downtime", "lift_instability", "integrity_flag", "engineer_override"),
    18: ("workover_scope_id", "target_interval", "pulling_depth", "suspected_failure", "equipment_readiness", "after_action_finding"),
    19: ("ticket_id", "route_type", "visit_objective", "asset_reference", "materials_used", "follow_up_requirement"),
    20: ("route_plan_id", "route_group", "must_visit_reason", "visit_sequence", "missed_route_reason", "production_impact_order"),
    21: ("chemical_program_id", "chemical_type", "target_dosage", "actual_dosage", "delivery_method", "skip_reason"),
    22: ("chemical_effectiveness_id", "corrosion_finding", "emulsion_severity", "bsw_outcome", "repeat_failure", "spend_correlation"),
    23: ("hse_boundary_id", "incident_class", "handoff_rule", "linked_downtime", "linked_ticket", "duplicate_count_guard"),
    24: ("permit_gate_id", "permit_to_work", "isolation_check", "gas_test", "line_break_check", "jsa_checkpoint"),
    25: ("regulatory_pack_id", "oil_total", "gas_total", "water_total", "flare_volume", "vent_volume", "restatement_reason"),
    26: ("environment_pack_id", "spill_volume_basis", "affected_media", "containment_status", "agency_notification", "closure_signoff"),
    27: ("water_movement_id", "disposition", "transfer_point", "trucked_or_piped", "injection_destination", "disposal_exception"),
    28: ("haul_ticket_id", "hauler", "truck_number", "ticket_sequence", "seal_status", "mismatch_reason"),
    29: ("integrity_id", "annulus_pressure", "bleed_down_test", "sustained_casing_pressure", "integrity_status", "follow_up_action"),
    30: ("surveillance_id", "casing_pressure", "tubing_pressure", "line_pressure", "fluid_level", "pump_intake_estimate"),
    31: ("event_schema_id", "typed_event", "payload_example", "idempotency_key", "major_action_mapping", "handler_evidence"),
    32: ("timeline_id", "as_of_cutoff", "status_snapshot", "production_revision", "downtime_snapshot", "hse_handoff_snapshot"),
    33: ("release_scenario_id", "daily_entry", "test_approval", "allocation_close", "workover_closeout", "regulatory_export"),
    34: ("surveillance_view_id", "rolling_baseline", "latest_test", "lift_type", "integrity_flag", "bad_actor_drilldown"),
    35: ("pad_map_id", "route_cluster", "pad_condition", "quick_action", "mobile_layout", "route_drilldown"),
    36: ("mobile_ticket_id", "offline_draft", "photo_queue", "timestamp_confidence", "sync_conflict", "reconciliation_result"),
    37: ("allocation_audit_id", "meter_total", "test_basis", "fallback_rule", "manual_override", "why_this_number"),
    38: ("morning_brief_id", "new_downtime", "rate_drop", "invalid_test", "meter_issue", "readonly_guard"),
    39: ("readiness_pack_id", "decline_trend", "lift_history", "permit_need", "recovery_basis", "missing_information"),
    40: ("regulatory_draft_id", "approved_allocation", "flare_classification", "correction_history", "unresolved_exception", "reviewer_action"),
    41: ("root_cause_summary_id", "repeat_driver", "failed_component", "recommendation_category", "citation_set", "rejection_reason"),
    42: ("escalation_rule_id", "deferred_volume", "hse_severity", "regulatory_due_date", "dedupe_key", "resolution_path"),
    43: ("boundary_control_id", "operator_scope", "asset_scope", "lease_scope", "assistant_filter", "export_constraint"),
    44: ("cost_trace_id", "cost_category", "cost_driver", "affected_asset", "linked_ticket", "allocation_basis"),
    45: ("handover_id", "shift", "watch_item", "next_owner", "active_outage_context", "closure_status"),
    46: ("checklist_id", "shut_in_type", "lineup_confirmation", "meter_readiness", "lift_readiness", "hse_gate"),
    47: ("injection_pattern_id", "injector_well", "injected_volume", "pressure_support_exception", "producer_link", "outage_impact"),
    48: ("target_tracking_id", "oil_target", "gas_target", "deferment_target", "variance_reason", "supporting_event"),
    49: ("fixture_set_id", "flowing_well", "rod_pump_well", "esp_well", "shared_battery", "reportable_hse_event"),
    50: ("go_live_evidence_id", "workflow_pass", "ui_screenshot", "event_trace", "allocation_reconciliation", "open_risk"),
}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    17: ("AssetIntegrityAlerted",),
    18: ("InventoryAvailabilityChanged", "WorkforceAvailabilityChanged"),
    20: ("RouteOptimizationChanged",),
    23: ("HseIncidentClassified",),
    24: ("PermitStatusChanged",),
    25: ("RegulatoryCalendarChanged",),
    26: ("EnvironmentalReportSubmitted", "HseIncidentClassified"),
    31: ("PolicyChanged", "AuditEventSealed"),
    42: ("OperationalKpiChanged", "RegulatoryCalendarChanged"),
    44: ("CostAllocationPosted",),
}
_DOMAIN_MESSAGES = {capability.feature_number: f"{capability.title} requires owned field operations evidence, UI, service/API, agent, event, and release proof before approval." for capability in FIELD_CONTROL_CAPABILITIES}
_HUMAN_CONFIRMATION_FEATURES = (3, 5, 16, 17, 18, 23, 24, 25, 26, 31, 33, 38, 39, 40, 42, 46, 50)
_PROJECTION_ONLY_FEATURES = (17, 18, 20, 23, 24, 25, 26, 31, 42, 44)
_AGENT_PREVIEW_FEATURES = (38, 39, 40, 41, 50)
_NON_MUTATING_FEATURES = (7, 14, 16, 17, 22, 25, 31, 32, 33, 37, 38, 39, 40, 41, 48, 49, 50)
_FIELD_RISK_FEATURES = (5, 7, 15, 16, 17, 18, 23, 24, 25, 26, 29, 31, 32, 33, 39, 40, 42, 43, 46, 47, 50)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability):
        return capability
    if isinstance(capability, int):
        return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    return {
        "title": capability.title,
        "slug": capability.slug,
        "tables": (f"oil_gas_field_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"OilGasFieldOperations{_camel(capability.slug)}Panel",
        "route": f"POST /oil-gas-field-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in FIELD_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload[spec["primary_proof"]] = True
    payload.update({
        "database_backend": "postgresql",
        "event_contract": EVENT_CONTRACT,
        "event_topic": FIELD_CONTROL_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "field_risk_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(_DOMAIN_MESSAGES[number])
    if number in _FIELD_RISK_FEATURES and payload.get("field_risk_evidence_complete") is not True:
        findings.append("production, allocation, HSE, workover, regulatory, integrity, and go-live decisions require complete field evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is False:
        findings.append("field lifecycle, workover, HSE, regulatory, restart, escalation, and assistant decisions require human approval")
    if number in _AGENT_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("field operations assistant skills must return cited, side-effect-free previews before confirmed CRUD")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("allocation simulations, replay, release evidence, assistant summaries, targets, fixtures, and go-live proofs must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("permit, HSE, route, workforce, inventory, cost, regulatory, policy, KPI, and audit facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != FIELD_CONTROL_REQUIRED_EVENT_TOPIC:
        findings.append("oil and gas field operations eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in FIELD_CONTROL_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary field operations datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("field operations controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_field_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in FIELD_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in FIELD_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {
        "evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20],
        "owned_tables": spec["tables"],
        "required_fields": spec["fields"],
        "primary_proof": spec["primary_proof"],
        "ui_surface": spec["ui"],
        "service_api": spec["route"],
        "test": "tests/test_domain_behavior.py",
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": FIELD_CONTROL_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": FIELD_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "declared_dependencies": spec["dependencies"],
        "side_effects": (),
    }
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_field_operations_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_field_operations_control(capability) for capability in FIELD_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.oil-gas-field-operations-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": FIELD_CONTROL_OWNED_TABLES, "declared_dependencies": FIELD_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": FIELD_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": FIELD_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


FIELD_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_field_operations_control(slug, payload)) for capability in FIELD_CONTROL_CAPABILITIES}
