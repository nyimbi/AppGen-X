"""Executable improve1 controls for the Hotel Revenue Management PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .domain_depth import DOMAIN_CONSUMED_EVENTS, DOMAIN_EVENTS, DOMAIN_OWNED_TABLES
from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability

PBC_KEY = "hotel_revenue_management"
EVENT_CONTRACT = "AppGen-X"
REVENUE_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
REVENUE_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.hotel_revenue_management.events"
REVENUE_CONTROL_OWNED_TABLES = tuple(dict.fromkeys(tuple(DOMAIN_OWNED_TABLES) + tuple(
    f"hotel_revenue_management_{cap.slug}_control" for cap in IMPROVE1_CAPABILITIES
)))
REVENUE_CONTROL_DECLARED_DEPENDENCIES = tuple(dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + tuple(DOMAIN_EVENTS) + (
    "OperationalKpiChanged", "AuditEventSealed", "PolicyChanged", "RoomAvailabilityProjected",
    "ReservationPickupProjected", "ChannelRatePublished", "CompSetSignalProjected", "GroupBlockProjected",
)))
REVENUE_CONTROL_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in REVENUE_CONTROL_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in REVENUE_CONTROL_CAPABILITIES}

_FEATURE_FIELDS: dict[int, tuple[str, ...]] = {
    1: ("physical_rooms", "sellable_rooms", "maintenance_holdbacks", "complimentary_allotments", "substitute_room_types", "date_band", "pricing_excludes_blocked_rooms"),
    2: ("parent_rate_plan", "child_rate_plan", "price_inheritance", "fence_inheritance", "channel_scope", "override_markers", "conflict_blocked"),
    3: ("bar_order_valid", "discount_gap_valid", "refundability_valid", "member_fence_valid", "advance_purchase_valid", "field_reasons", "publish_allowed"),
    4: ("restriction_date", "cta", "ctd", "min_los", "max_los", "stay_through_exception", "itinerary_valid"),
    5: ("channel", "allotment", "stop_sell", "release_back_rule", "blackout_window", "reopen_approval", "direct_channel_preserved"),
    6: ("channel_rates", "parity_break", "reason_code", "approved_exception", "defect_queue", "noise_suppressed", "real_mismatch_visible"),
    7: ("stay_date", "booking_window", "room_type", "segment", "pickup_baseline", "live_pace", "deviation_exception"),
    8: ("transient_demand", "corporate_demand", "group_demand", "wholesale_demand", "house_use_demand", "confidence_band", "totals_reconcile"),
    9: ("event_tag", "compression_factor", "shoulder_spill", "post_event_wash", "baseline_view", "event_adjusted_view", "peak_replay_evidence"),
    10: ("room_type_cap", "day_of_week_adjustment", "arrival_day_protection", "recovery_hierarchy", "override_approval", "oversell_within_limit"),
    11: ("cancellation_curve", "no_show_curve", "early_departure_curve", "segment", "booking_window", "version", "oversell_recalculated"),
    12: ("group_block", "wash_percent", "pickup_checkpoint", "cutoff_date", "release_rule", "released_to_transient", "audit_trail"),
    13: ("group_quote", "transient_displacement", "shoulder_fill", "ancillary_value", "minimum_acceptable_rate", "scenario_comparison", "compression_adjusted"),
    14: ("market", "submarket", "star_class", "brand_position", "product_comparability", "approval", "out_of_bound_ignored"),
    15: ("hypothesis", "target_market", "eligible_channels", "holdout_design", "start_date", "end_date", "rollback_criteria", "outcome_snapshot"),
    16: ("forecast_inputs", "pickup_signals", "restrictions", "channel_state", "comp_set_version", "rule_references", "explanation_complete"),
    17: ("channel", "net_revenue_delta", "acquisition_cost", "pace", "room_type_scarcity", "recommended_action", "accepted_governed_change"),
    18: ("account_type", "room_type", "date_class", "protected_inventory", "stop_sell_exception", "policy_audit", "protected_access_retained"),
    19: ("shoulder_softness", "gap_night", "los_offer", "fenced_discount", "package_positioning", "accepted_rate_change", "peak_night_distinguished"),
    20: ("compression_night", "pace", "scarcity", "restriction_stance", "oversell_stance", "action_checklist", "stale_feed_visible"),
    21: ("source_room_type", "target_room_type", "upgrade_allowed", "downgrade_allowed", "revenue_impact", "protected_demand_preserved", "blocked_path_hidden"),
    22: ("package_component", "component_margin", "minimum_contribution", "base_bar_preserved", "approval_warning", "net_value_calculated", "low_margin_blocked"),
    23: ("negotiated_rate", "blackout_calendar", "exemption_list", "approval_flow", "protected_account", "crew_business_rule", "intended_dates_only"),
    24: ("override_reason", "expected_duration", "evidence_note", "required_approver", "expiry_date", "layered_value", "variance_threshold_approved"),
    25: ("scenario_name", "occupancy", "adr", "revpar", "room_revenue", "channel_mix", "oversell_exposure", "baseline_comparison"),
    26: ("snapshot_id", "source_decisions", "forecast_lineage", "rate_lineage", "channel_lineage", "policy_lineage", "lineage_complete"),
    27: ("forecast_timestamp", "pickup_timestamp", "freshness_threshold", "stale_forecast", "stale_pickup", "exception_opened", "decision_blocked"),
    28: ("correction_id", "idempotency_key", "payload_hash", "prior_inventory", "corrected_inventory", "duplicate_replay_prevented", "safe_replay_allowed"),
    29: ("rate_plan", "bar_valid", "fences_valid", "parity_checked", "approvals_complete", "events_ready", "publish_allowed"),
    30: ("failed_channel_event", "retry_policy", "dead_letter_route", "business_impact", "safe_replay_allowed", "remediation_owner", "original_payload_visible"),
    31: ("pace_panel", "forecast_panel", "restriction_panel", "yield_panel", "exceptions_panel", "permission_actions", "decision_drilldown"),
    32: ("channel_health", "parity_queue", "stop_sell_queue", "rate_publish_queue", "defect_reason", "channel_scope", "workbench_actionable"),
    33: ("group_block_panel", "event_calendar", "wash_alerts", "displacement_panel", "cutoff_queue", "release_actions", "scenario_compare"),
    34: ("draft_instruction", "source_document", "candidate_rate_plan", "source_citations", "command_preview", "human_confirmation", "direct_mutation_blocked"),
    35: ("pickup_anomaly", "baseline_citation", "driver_explanation", "triage_queue", "recommended_action", "human_confirmation", "audit_trail"),
    36: ("overbooking_explanation", "guest_recovery_options", "walk_cost", "protected_arrivals", "permission_check", "human_confirmation", "direct_mutation_blocked"),
    37: ("outbound_event", "payload_schema", "consumer_boundary", "event_topic", "appgen_contract", "idempotency_key", "stream_picker_hidden"),
    38: ("inbound_event", "handler_contract", "policy_effect", "kpi_effect", "idempotency_key", "dead_letter_route", "safe_replay_allowed"),
    39: ("assertion_suite", "bar_ladder_checked", "parity_checked", "overbooking_checked", "experiment_checked", "remediation_tasks", "control_effective"),
    40: ("season", "market", "parameter_set", "bounds_valid", "approval_history", "impact_preview", "activation_allowed"),
    41: ("tenant_id", "brand_id", "property_id", "market_id", "policy_scope", "queue_leakage_blocked", "assistant_scope"),
    42: ("restriction_type", "schema_extension", "ui_placement", "compatibility_check", "backfill_plan", "existing_records_preserved", "activation_allowed"),
    43: ("model_name", "model_version", "forecast_model", "optimization_model", "feature_lineage", "approval_status", "drift_monitor"),
    44: ("pricing_approval_hash", "override_hash", "previous_hash", "proof_verified", "altered_order_detected", "redacted_export_supported", "auditor_export"),
    45: ("forecast_query_route", "simulation_route", "scenario_route", "versioned_route", "idempotency_required", "owned_scope", "read_only_query"),
    46: ("pricing_change_tests", "inventory_change_tests", "forecast_override_tests", "agent_guardrails", "boundary_checks", "release_pack_complete", "documentation_updated"),
    47: ("drill_name", "forecast_failure", "peak_date", "fallback_model", "manual_override_queue", "recovery_evidence", "live_mutation_blocked"),
    48: ("consumer", "dependency_mode", "foreign_table_access_blocked", "api_contract", "event_contract", "projection_contract", "owned_scope"),
    49: ("kpi_library", "occupancy_definition", "adr_definition", "revpar_definition", "pickup_definition", "formula_version", "calculation_tests"),
    50: ("scorecard", "go_live_signoff", "pricing_seeded", "inventory_seeded", "forecast_seeded", "apis_exercised", "events_emitted", "workbench_queues_driven", "assistant_summary_generated", "control_assertions_run", "release_documents_updated"),
}
_FEATURE_DEPENDENCIES = {7: ("OperationalKpiChanged",), 18: ("PolicyChanged",), 26: ("AuditEventSealed",), 37: ("ChannelRatePublished",), 38: ("PolicyChanged", "OperationalKpiChanged"), 48: ("RoomAvailabilityProjected", "ReservationPickupProjected")}
_EMPTY_ALLOWED_FIELDS = ("remediation_tasks", "field_reasons")


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def _resolve(capability: Improve1Capability | str | int) -> Improve1Capability | None:
    if isinstance(capability, Improve1Capability): return capability
    if isinstance(capability, int): return CAPABILITY_BY_NUMBER.get(capability)
    return CAPABILITY_BY_SLUG.get(capability)


def _spec_for(capability: Improve1Capability) -> dict[str, Any]:
    return {"title": capability.title, "slug": capability.slug, "tables": (f"hotel_revenue_management_{capability.slug}_control",), "fields": _FEATURE_FIELDS[capability.feature_number], "ui": _camel(capability.slug), "route": f"POST /hotel-revenue-management/improve1/{capability.slug}", "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ())}


CONTROL_SPECS: dict[int, dict[str, Any]] = {capability.feature_number: _spec_for(capability) for capability in REVENUE_CONTROL_CAPABILITIES}


def sample_payload_for(capability: Improve1Capability | str | int) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None: return {}
    spec = CONTROL_SPECS[resolved.feature_number]
    payload = {field: f"{resolved.slug}_{field}" for field in spec["fields"]}
    payload.update({
        "physical_rooms": 100, "sellable_rooms": 92, "maintenance_holdbacks": 5, "complimentary_allotments": 3, "pricing_excludes_blocked_rooms": True,
        "conflict_blocked": True, "bar_order_valid": True, "discount_gap_valid": True, "refundability_valid": True, "member_fence_valid": True, "advance_purchase_valid": True, "field_reasons": (), "publish_allowed": True,
        "itinerary_valid": True, "allotment": 20, "stop_sell": False, "direct_channel_preserved": True, "parity_break": False, "approved_exception": True, "noise_suppressed": True, "real_mismatch_visible": True,
        "pickup_baseline": 12, "live_pace": 13, "deviation_exception": False, "transient_demand": 40, "corporate_demand": 20, "group_demand": 15, "wholesale_demand": 5, "house_use_demand": 2, "confidence_band": "0.85-0.95", "totals_reconcile": True,
        "compression_factor": 1.25, "peak_replay_evidence": True, "room_type_cap": 4, "arrival_day_protection": True, "override_approval": "approved", "oversell_within_limit": True, "oversell_recalculated": True,
        "released_to_transient": True, "audit_trail": "captured", "minimum_acceptable_rate": 250, "compression_adjusted": True, "approval": "approved", "out_of_bound_ignored": True,
        "rollback_criteria": "defined", "outcome_snapshot": True, "explanation_complete": True, "net_revenue_delta": 1200, "recommended_action": "open_direct_close_high_cost_ota", "accepted_governed_change": True,
        "protected_access_retained": True, "peak_night_distinguished": True, "action_checklist": "complete", "stale_feed_visible": True, "upgrade_allowed": True, "downgrade_allowed": False, "protected_demand_preserved": True, "blocked_path_hidden": True,
        "component_margin": 0.35, "minimum_contribution": 25, "base_bar_preserved": True, "net_value_calculated": True, "low_margin_blocked": False, "intended_dates_only": True, "required_approver": "rev-director", "layered_value": True, "variance_threshold_approved": True,
        "occupancy": 0.89, "adr": 180, "revpar": 160, "baseline_comparison": True, "lineage_complete": True, "stale_forecast": False, "stale_pickup": False, "exception_opened": False, "decision_blocked": False,
        "idempotency_key": "idem-1", "payload_hash": "hash", "duplicate_replay_prevented": True, "safe_replay_allowed": True, "parity_checked": True, "bar_valid": True, "fences_valid": True, "approvals_complete": True, "events_ready": True,
        "retry_policy": "5-attempts", "dead_letter_route": "owned-dlq", "business_impact": "low", "original_payload_visible": True, "permission_actions": "role_filtered", "decision_drilldown": True, "workbench_actionable": True,
        "source_citations": ("rate-sheet-1",), "command_preview": True, "human_confirmation": True, "direct_mutation_blocked": True, "baseline_citation": "pace-baseline", "driver_explanation": "pace above baseline", "permission_check": True,
        "event_topic": REVENUE_CONTROL_REQUIRED_EVENT_TOPIC, "appgen_contract": EVENT_CONTRACT, "stream_picker_hidden": True, "handler_contract": "declared", "idempotency_required": True, "bar_ladder_checked": True, "overbooking_checked": True, "experiment_checked": True, "remediation_tasks": (), "control_effective": True,
        "bounds_valid": True, "approval_history": "captured", "impact_preview": True, "activation_allowed": True, "queue_leakage_blocked": True, "compatibility_check": True, "backfill_plan": "ready", "existing_records_preserved": True,
        "approval_status": "approved", "drift_monitor": True, "proof_verified": True, "altered_order_detected": False, "redacted_export_supported": True, "auditor_export": True, "versioned_route": True, "owned_scope": True, "read_only_query": True,
        "pricing_change_tests": True, "inventory_change_tests": True, "forecast_override_tests": True, "agent_guardrails": True, "boundary_checks": True, "release_pack_complete": True, "documentation_updated": True,
        "forecast_failure": True, "fallback_model": "last_good_model", "manual_override_queue": True, "recovery_evidence": "captured", "live_mutation_blocked": True, "dependency_mode": "event", "foreign_table_access_blocked": True, "api_contract": "declared", "event_contract": EVENT_CONTRACT, "projection_contract": "declared",
        "formula_version": "v1", "calculation_tests": True, "go_live_signoff": True, "pricing_seeded": True, "inventory_seeded": True, "forecast_seeded": True, "apis_exercised": True, "events_emitted": True, "workbench_queues_driven": True, "assistant_summary_generated": True, "control_assertions_run": True, "release_documents_updated": True,
        "stream_engine_picker_visible": False,
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    n = capability.feature_number
    if n == 1 and (payload.get("sellable_rooms", 0) > payload.get("physical_rooms", 0) or payload.get("pricing_excludes_blocked_rooms") is not True):
        findings.append("sellable room-type inventory must keep sellable rooms within physical capacity and exclude blocked rooms")
    if n == 2 and payload.get("conflict_blocked") is not True:
        findings.append("rate-plan inheritance must block override conflicts")
    if n == 3 and not all(payload.get(field) is True for field in ("bar_order_valid", "discount_gap_valid", "refundability_valid", "member_fence_valid", "advance_purchase_valid", "publish_allowed")):
        findings.append("BAR ladder and price-fence validator blocks invalid public rates")
    if n == 5 and payload.get("direct_channel_preserved") is not True:
        findings.append("channel stop-sell must preserve direct-channel availability unless shared rules apply")
    if n == 6 and payload.get("parity_break") is True and payload.get("approved_exception") is not True:
        findings.append("channel parity breaks require approved exception reason")
    if n == 8 and payload.get("totals_reconcile") is not True:
        findings.append("segmented demand forecast totals must reconcile to the property forecast")
    if n == 10 and (payload.get("arrival_day_protection") is not True or payload.get("oversell_within_limit") is not True):
        findings.append("overbooking limits must respect arrival-day protection and room-type caps")
    if n == 13 and payload.get("compression_adjusted") is not True:
        findings.append("group displacement analysis must raise value on compression nights")
    if n == 14 and payload.get("out_of_bound_ignored") is not True:
        findings.append("comp-set governance ignores out-of-bound competitor inputs until approved")
    if n == 16 and payload.get("explanation_complete") is not True:
        findings.append("yield-decision explanation trail requires forecast, pickup, channel, comp-set, and rule references")
    if n == 18 and payload.get("protected_access_retained") is not True:
        findings.append("last-room-availability controls must retain protected account access")
    if n == 22 and (payload.get("low_margin_blocked") is True or payload.get("net_value_calculated") is not True):
        findings.append("package-rate margin controls must calculate net value and block low-margin packages only with evidence")
    if n == 24 and (not payload.get("required_approver") or payload.get("variance_threshold_approved") is not True):
        findings.append("forecast override workflow requires approver and threshold approval evidence")
    if n == 28 and (payload.get("duplicate_replay_prevented") is not True or payload.get("safe_replay_allowed") is not True):
        findings.append("inventory correction API requires idempotent replay protection")
    if n == 29 and not all(payload.get(field) is True for field in ("bar_valid", "fences_valid", "parity_checked", "approvals_complete", "events_ready", "publish_allowed")):
        findings.append("rate-plan publishing readiness gate is incomplete")
    if n in (34, 35, 36) and (payload.get("command_preview") is not True or payload.get("human_confirmation") is not True or payload.get("direct_mutation_blocked") is not True):
        findings.append("hotel revenue agent skills require preview, confirmation, citations, and no direct mutation")
    if n == 37 and (payload.get("appgen_contract") != EVENT_CONTRACT or payload.get("event_topic") != REVENUE_CONTROL_REQUIRED_EVENT_TOPIC or payload.get("stream_picker_hidden") is not True):
        findings.append("outbound revenue events must use AppGen-X topic and hide stream picker")
    if n == 39 and (payload.get("control_effective") is not True or payload.get("remediation_tasks") not in ((), [])):
        findings.append("continuous pricing governance assertions must clear remediation")
    if n == 41 and payload.get("queue_leakage_blocked") is not True:
        findings.append("multi-tenant hotel revenue isolation must block queue leakage")
    if n == 44 and (payload.get("proof_verified") is not True or payload.get("altered_order_detected") is True):
        findings.append("audit-proof sealing failed pricing approval tamper validation")
    if n == 48 and (payload.get("foreign_table_access_blocked") is not True or payload.get("dependency_mode") not in ("api", "event", "projection") or payload.get("owned_scope") is not True):
        findings.append("cross-PBC boundary rules require APIs/events/projections and no foreign table access")
    if n == 50 and not all(payload.get(field) is True for field in ("go_live_signoff", "pricing_seeded", "inventory_seeded", "forecast_seeded", "apis_exercised", "events_emitted", "workbench_queues_driven", "assistant_summary_generated", "control_assertions_run", "release_documents_updated")):
        findings.append("go-live scorecard and release signoff drill is incomplete")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    return tuple(findings)


def evaluate_revenue_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None: return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved); candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if field not in _EMPTY_ALLOWED_FIELDS and candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in REVENUE_CONTROL_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in REVENUE_CONTROL_DECLARED_DEPENDENCIES)
    findings = _domain_findings(resolved, candidate)
    evidence = {"evidence_id": _digest((PBC_KEY, resolved.feature_number, tuple(sorted(candidate))))[:20], "owned_tables": spec["tables"], "required_fields": spec["fields"], "ui_surface": spec["ui"], "service_api": spec["route"], "test": "tests/test_domain_behavior.py", "event_contract": EVENT_CONTRACT, "required_event_topic": REVENUE_CONTROL_REQUIRED_EVENT_TOPIC, "allowed_database_backends": REVENUE_CONTROL_ALLOWED_DATABASE_BACKENDS, "declared_dependencies": spec["dependencies"], "side_effects": ()}
    ok = not missing_fields and not foreign_tables and not undeclared_dependencies and not findings
    return {"ok": ok, "pbc": PBC_KEY, "feature_number": resolved.feature_number, "slug": resolved.slug, "title": resolved.title, "capability": resolved.as_traceability_row(), "payload": candidate, "evidence": evidence, "missing_fields": missing_fields, "foreign_tables": foreign_tables, "undeclared_dependencies": undeclared_dependencies, "findings": findings, "side_effects": ()}


def improve1_revenue_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_revenue_control(capability) for capability in REVENUE_CONTROL_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {"ok": not blocking, "pbc": PBC_KEY, "format": "appgen.hotel-revenue-management-improve1-control.v1", "capability_count": len(evaluations), "capabilities": evaluations, "owned_tables": REVENUE_CONTROL_OWNED_TABLES, "declared_dependencies": REVENUE_CONTROL_DECLARED_DEPENDENCIES, "allowed_database_backends": REVENUE_CONTROL_ALLOWED_DATABASE_BACKENDS, "event_contract": EVENT_CONTRACT, "required_event_topic": REVENUE_CONTROL_REQUIRED_EVENT_TOPIC, "stream_engine_picker_visible": False, "blocking_gaps": blocking, "side_effects": ()}


REVENUE_CONTROL_FUNCTIONS = {capability.slug: (lambda payload=None, slug=capability.slug: evaluate_revenue_control(slug, payload)) for capability in REVENUE_CONTROL_CAPABILITIES}
