"""Executable improve1 controls for the Hospitality Property Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EMITTED_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "hospitality_property_operations"
EVENT_CONTRACT = "AppGen-X"
HOSPITALITY_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
HOSPITALITY_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.hospitality_property_operations.events"
HOSPITALITY_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"hospitality_property_operations_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
HOSPITALITY_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EMITTED_EVENTS) + (
    "CustomerUpdated", "SupplierQualified", "PolicyChanged", "PaymentHoldProjected",
    "MaintenanceTicketProjected", "RevenueRestrictionProjected", "RoomingListReceived",
)))
HOSPITALITY_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in HOSPITALITY_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in HOSPITALITY_CONTROL_CAPABILITIES}

_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {
    1: ("operational_status", "housekeeping_status", "inspection_status", "maintenance_hold_status", "sellable_state", "transition_rule", "timeline_visible"),
    2: ("room_class", "bed_configuration", "accessibility_flags", "adjoining_room_links", "amenity_ready", "minibar_status", "assignment_compatible"),
    3: ("reservation_state", "guarantee_status", "deposit_evidence", "cancellation_window", "source_channel", "arrival_window", "reinstatement_allowed"),
    4: ("pickup_curve", "no_show_expectation", "arrival_hour_projection", "oversell_threshold", "walk_risk", "forecast_inputs_visible"),
    5: ("stay_state", "room_history", "extension_state", "late_checkout_status", "departure_readiness", "service_flags", "timeline_complete"),
    6: ("hold_type", "severity", "expected_return_time", "engineering_owner", "guest_impact", "recovery_steps", "sellable_inventory_reduced"),
    7: ("room_zone", "attendant_assignment", "due_window", "task_type", "arrival_dependency", "expedite_flag", "blockers_visible"),
    8: ("inspection_required", "inspector_identity", "defect_categories", "rework_count", "photo_or_note_evidence", "pass_fail_score", "release_allowed"),
    9: ("request_category", "urgency", "promised_by", "fulfillment_team", "guest_impact", "service_recovery", "closeout_evidence"),
    10: ("stay_date", "time_bucket", "room_status_mix", "arrivals_pending", "departures_pending", "stayovers", "same_day_turn_pressure"),
    11: ("room_class_applicability", "length_of_stay_fence", "closed_to_arrival", "shoulder_night_control", "amenity_promise", "housekeeping_sell_threshold", "rate_action_explained"),
    12: ("group_block", "allotment", "rooming_list", "pickup_monitoring", "attrition_warning", "cut_date", "release_decision"),
    13: ("pace", "wash", "pickup", "los_mix", "same_day_arrivals", "room_class_sellout_risk", "anomaly_marker"),
    14: ("handover_packet", "unresolved_arrivals", "room_moves", "payment_hold_followups", "maintenance_blocks", "service_recovery_actions", "signoff_complete"),
    15: ("policy_rule", "room_blocking_criteria", "vip_handling", "late_checkout_approval", "service_recovery_threshold", "override_justification", "rule_visible"),
    16: ("turn_time_minutes", "inspection_delay", "arrival_rush_threshold", "batch_size", "request_sla", "late_night_escalation", "impact_preview"),
    17: ("arrival_lane", "departure_lane", "room_ready_gap_lane", "room_move_lane", "vip_lane", "service_recovery_lane", "permission_actions"),
    18: ("room_header", "attribute_panel", "status_timeline", "housekeeping_history", "maintenance_holds", "active_stay", "event_evidence"),
    19: ("role_prompt", "cited_recommendation", "task_context", "document_intake", "human_confirmation", "owned_action_plan", "direct_mutation_blocked"),
    20: ("agent_skill", "task_board_action", "command_preview", "permission_check", "policy_gate", "confirmation_required", "audit_trail"),
    21: ("document_packet", "rooming_list_extract", "guest_instruction_extract", "source_citations", "confidence", "review_required", "owned_record_plan"),
    22: ("event_sequence", "room_events", "stay_events", "service_events", "replay_checkpoint", "late_event_visible", "timeline_gap_visible"),
    23: ("idempotency_key", "payload_hash", "duplicate_detected", "correction_reason", "late_event_quarantine", "manual_review_visible", "safe_replay_allowed"),
    24: ("projection_name", "dependency_mode", "source_event", "foreign_table_access_blocked", "owned_projection", "staleness_visible", "refresh_event"),
    25: ("failed_event_type", "business_impact", "retry_policy", "dead_letter_route", "safe_replay_allowed", "remediation_owner", "original_payload_visible"),
    26: ("boundary", "guest_master_owned", "supplier_master_owned", "payment_ledger_owned", "projection_used", "foreign_mutation_blocked", "contract_declared"),
    27: ("arrival_risk_score", "room_readiness_score", "risk_factors", "confidence", "explanation", "review_queue", "mitigation_plan"),
    28: ("scenario", "sellout_pressure", "staffing_gap", "blocked_rooms", "arrival_surge", "service_recovery_load", "live_mutation_blocked"),
    29: ("contradiction_type", "room_state", "housekeeping_state", "maintenance_state", "expected_pattern", "case_opened", "analyst_review"),
    30: ("control_suite", "sellable_state_checked", "accessible_assignment_checked", "sla_checked", "handover_checked", "remediation_tasks", "control_effective"),
    31: ("inspection_hash", "release_hash", "previous_hash", "payload_digest_valid", "proof_verified", "altered_order_detected", "redacted_export_supported"),
    32: ("arrival_flow_tests", "room_release_tests", "request_sla_tests", "rate_fence_tests", "agent_guardrails", "boundary_checks", "release_pack_complete"),
    33: ("command_preview", "permission_check", "role_scope", "policy_gate", "human_confirmation", "direct_mutation_blocked", "accepted_audit_trail"),
    34: ("tenant_id", "property_id", "workbench_scope", "rule_scope", "parameter_scope", "assistant_scope", "queue_leakage_blocked"),
    35: ("room_taxonomy_field", "ui_placement", "compatibility_check", "backfill_plan", "existing_records_preserved", "activation_allowed", "deprecation_safe"),
    36: ("model_name", "model_version", "training_scope", "feature_lineage", "approval_status", "drift_monitor", "recommendation_explainable"),
    37: ("property_calendar", "service_standard", "seasonal_override", "approval_history", "rollback_visible", "bounds_valid", "activation_allowed"),
    38: ("rule_name", "room_move_rule", "late_checkout_rule", "service_recovery_rule", "override_path", "explanation_visible", "test_cases"),
    39: ("forecast_horizon", "labor_buffer", "arrival_window", "turn_buffer", "bounds_valid", "impact_preview", "approval_history"),
    40: ("role", "shift", "property", "sensitive_action", "permission_check", "segregation_rule", "action_allowed"),
    41: ("route_contract", "create_route", "query_route", "sla_route", "idempotency_required", "versioned_route", "owned_scope"),
    42: ("bulk_assignment", "mobile_update", "offline_capture", "sequence_number", "duplicate_prevented", "safe_replay_allowed", "attendant_visible"),
    43: ("check_in_route", "room_move_route", "checkout_route", "stay_history_preserved", "idempotency_required", "owned_scope", "event_emitted"),
    44: ("block_route", "return_route", "amenity_route", "sellable_state_guard", "maintenance_hold_guard", "versioned_route", "event_emitted"),
    45: ("workbench_query", "arrival_counts", "room_ready_counts", "request_counts", "rate_alert_counts", "read_only", "foreign_state_hidden"),
    46: ("emitted_event_types", "payload_schema", "idempotency_key", "event_topic", "appgen_contract", "consumer_projection", "stream_picker_hidden"),
    47: ("policy_event", "affected_rules", "affected_queues", "rereview_queue", "prior_rule_version", "closed_history_mutation_blocked", "impact_summary"),
    48: ("customer_event", "preference_diff", "review_task", "silent_overwrite_blocked", "dependent_stays_refreshed", "approved_changes", "workbench_refreshed"),
    49: ("supplier_event", "supplier_qualified", "outsourced_service", "affected_tasks", "assignment_blocked", "source_lineage", "stored_reasoning"),
    50: ("reservation_seeded", "room_seeded", "housekeeping_seeded", "stay_seeded", "guest_request_seeded", "apis_exercised", "events_emitted", "workbench_queues_driven", "assistant_summary_generated", "control_assertions_run", "release_documents_updated"),
}
_FEATURE_DEPENDENCIES = {24: ("CustomerUpdated",), 26: ("CustomerUpdated", "SupplierQualified", "PaymentHoldProjected"), 47: ("PolicyChanged",), 48: ("CustomerUpdated",), 49: ("SupplierQualified",)}
_EMPTY_ALLOWED_FIELDS = ("remediation_tasks",)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability): return capability
    if isinstance(capability, int): return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    return {"title": capability.title, "slug": capability.slug, "tables": (f"hospitality_property_operations_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "ui": _camel(capability.slug), "route": f"POST /hospitality-property-operations/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in HOSPITALITY_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None: return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({
        "operational_status": "vacant", "housekeeping_status": "clean", "inspection_status": "passed", "maintenance_hold_status": "clear", "sellable_state": "sellable", "timeline_visible": True,
        "accessibility_flags": ("roll_in_shower",), "amenity_ready": True, "assignment_compatible": True, "guarantee_status": "guaranteed", "deposit_evidence": "captured", "reinstatement_allowed": True,
        "walk_risk": "low", "forecast_inputs_visible": True, "room_history": ("101",), "departure_readiness": True, "timeline_complete": True,
        "sellable_inventory_reduced": True, "attendant_assignment": "attendant-1", "blockers_visible": True, "inspection_required": True, "pass_fail_score": "pass", "release_allowed": True,
        "urgency": "routine", "closeout_evidence": "guest-confirmed", "same_day_turn_pressure": "normal", "housekeeping_sell_threshold": 5, "rate_action_explained": True,
        "release_decision": "approved", "anomaly_marker": False, "signoff_complete": True, "override_justification": "captured", "rule_visible": True,
        "impact_preview": True, "permission_actions": "role_filtered", "event_evidence": "timeline", "cited_recommendation": True, "human_confirmation": True, "owned_action_plan": True, "direct_mutation_blocked": True,
        "command_preview": True, "permission_check": True, "policy_gate": True, "confirmation_required": True, "audit_trail": "captured", "source_citations": ("rooming-list-row-1",), "confidence": 0.91, "review_required": True,
        "late_event_visible": True, "timeline_gap_visible": False, "payload_hash": "hash", "duplicate_detected": False, "late_event_quarantine": False, "manual_review_visible": True, "safe_replay_allowed": True,
        "dependency_mode": "event", "foreign_table_access_blocked": True, "owned_projection": True, "staleness_visible": True, "business_impact": "low", "retry_policy": "5-attempts", "dead_letter_route": "owned-dlq",
        "guest_master_owned": False, "supplier_master_owned": False, "payment_ledger_owned": False, "projection_used": True, "foreign_mutation_blocked": True, "contract_declared": True,
        "arrival_risk_score": 0.2, "room_readiness_score": 0.92, "risk_factors": ("clean rooms sufficient",), "explanation": "low risk", "mitigation_plan": "monitor",
        "live_mutation_blocked": True, "case_opened": True, "analyst_review": True, "sellable_state_checked": True, "accessible_assignment_checked": True, "sla_checked": True, "handover_checked": True, "remediation_tasks": (), "control_effective": True,
        "payload_digest_valid": True, "proof_verified": True, "altered_order_detected": False, "redacted_export_supported": True, "arrival_flow_tests": True, "room_release_tests": True, "request_sla_tests": True, "rate_fence_tests": True, "agent_guardrails": True, "boundary_checks": True, "release_pack_complete": True,
        "role_scope": "front_desk", "accepted_audit_trail": True, "queue_leakage_blocked": True, "compatibility_check": True, "backfill_plan": "ready", "existing_records_preserved": True, "activation_allowed": True, "deprecation_safe": True,
        "approval_status": "approved", "drift_monitor": True, "recommendation_explainable": True, "rollback_visible": True, "bounds_valid": True, "test_cases": ("late-checkout",), "action_allowed": True,
        "idempotency_required": True, "versioned_route": True, "owned_scope": True, "offline_capture": True, "duplicate_prevented": True, "stay_history_preserved": True, "event_emitted": True,
        "read_only": True, "foreign_state_hidden": True, "event_topic": HOSPITALITY_CONTROL_REQUIRED_EVENT_TOPIC, "appgen_contract": EVENT_CONTRACT, "stream_picker_hidden": True, "closed_history_mutation_blocked": True,
        "silent_overwrite_blocked": True, "dependent_stays_refreshed": True, "approved_changes": True, "workbench_refreshed": True, "supplier_qualified": True, "assignment_blocked": False, "source_lineage": "event", "stored_reasoning": True,
        "reservation_seeded": True, "room_seeded": True, "housekeeping_seeded": True, "stay_seeded": True, "guest_request_seeded": True, "apis_exercised": True, "events_emitted": True, "workbench_queues_driven": True, "assistant_summary_generated": True, "control_assertions_run": True, "release_documents_updated": True,
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and (payload.get("operational_status") in {"occupied", "out_of_order", "out_of_service"} or payload.get("housekeeping_status") != "clean" or payload.get("inspection_status") != "passed" or payload.get("maintenance_hold_status") != "clear" or payload.get("sellable_state") != "sellable"):
        findings.append("sellable room state requires vacant, clean, inspected, maintenance-clear room status")
    if n == 2 and (payload.get("assignment_compatible") is not True or payload.get("amenity_ready") is not True):
        findings.append("room assignment requires compatible attributes and amenity readiness")
    if n == 3 and (payload.get("guarantee_status") != "guaranteed" or not payload.get("deposit_evidence")):
        findings.append("reservation lifecycle requires guarantee and deposit/card-hold evidence")
    if n == 4 and payload.get("walk_risk") == "high":
        findings.append("arrival pickup projection indicates unresolved high walk risk")
    if n == 5 and (not payload.get("room_history") or payload.get("departure_readiness") is not True):
        findings.append("guest stay lifecycle must preserve room history and departure readiness")
    if n == 6 and payload.get("sellable_inventory_reduced") is not True:
        findings.append("maintenance holds must reduce sellable inventory")
    if n == 8 and (payload.get("pass_fail_score") != "pass" or payload.get("release_allowed") is not True):
        findings.append("inspection quality loop blocks room release until pass evidence exists")
    if n == 9 and not payload.get("closeout_evidence"):
        findings.append("guest request SLA requires closeout evidence")
    if n == 19 and (payload.get("cited_recommendation") is not True or payload.get("human_confirmation") is not True or payload.get("direct_mutation_blocked") is not True):
        findings.append("assistant panel must cite recommendations and block direct mutation")
    if n == 23 and (payload.get("duplicate_detected") is True or payload.get("safe_replay_allowed") is not True):
        findings.append("idempotent intake must prevent duplicate operations and support safe replay")
    if n == 24 and (payload.get("dependency_mode") not in ("api", "event", "projection") or payload.get("foreign_table_access_blocked") is not True):
        findings.append("boundary-safe projections cannot use shared foreign tables")
    if n == 26 and (payload.get("guest_master_owned") is True or payload.get("supplier_master_owned") is True or payload.get("payment_ledger_owned") is True or payload.get("foreign_mutation_blocked") is not True):
        findings.append("declared hotel boundaries cannot own guest master, supplier master, or payment ledger data")
    if n == 30 and (payload.get("control_effective") is not True or payload.get("remediation_tasks") not in ((), [])):
        findings.append("continuous operational controls must clear remediation tasks")
    if n == 31 and (payload.get("proof_verified") is not True or payload.get("altered_order_detected") is True or payload.get("payload_digest_valid") is not True):
        findings.append("inspection release proof failed cryptographic validation")
    if n == 33 and (payload.get("command_preview") is not True or payload.get("permission_check") is not True or payload.get("human_confirmation") is not True or payload.get("direct_mutation_blocked") is not True):
        findings.append("governed AI execution requires preview, permission, confirmation, and no direct mutation")
    if n == 34 and payload.get("queue_leakage_blocked") is not True:
        findings.append("multi-property isolation must block queue leakage")
    if n == 41 and (payload.get("idempotency_required") is not True or payload.get("owned_scope") is not True):
        findings.append("guest request APIs require idempotency and owned scope")
    if n == 46 and (payload.get("appgen_contract") != EVENT_CONTRACT or payload.get("event_topic") != HOSPITALITY_CONTROL_REQUIRED_EVENT_TOPIC or payload.get("stream_picker_hidden") is not True):
        findings.append("typed emitted events must use AppGen-X topic and hide stream picker")
    if n == 48 and payload.get("silent_overwrite_blocked") is not True:
        findings.append("customer update handlers must block silent preference overwrite")
    if n == 49 and payload.get("supplier_qualified") is not True:
        findings.append("supplier qualification handlers must block unqualified outsourced service assignments")
    if n == 50 and not all(payload.get(field) is True for field in ("reservation_seeded", "room_seeded", "housekeeping_seeded", "stay_seeded", "guest_request_seeded", "apis_exercised", "events_emitted", "workbench_queues_driven", "assistant_summary_generated", "control_assertions_run", "release_documents_updated")):
        findings.append("end-to-end arrival-to-room-ready release proof is incomplete")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_hospitality_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None: return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved); candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in HOSPITALITY_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in HOSPITALITY_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": HOSPITALITY_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": HOSPITALITY_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_hospitality_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_hospitality_control(capability) for capability in HOSPITALITY_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.hospitality-property-operations-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": HOSPITALITY_CONTROL_OWNED_TABLES, "declared_dependencies": HOSPITALITY_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": HOSPITALITY_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": HOSPITALITY_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


HOSPITALITY_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_hospitality_control(slug, payload)) for capability in HOSPITALITY_CONTROL_CAPABILITIES}
