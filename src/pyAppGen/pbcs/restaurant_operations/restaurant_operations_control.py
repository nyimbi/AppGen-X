"""Executable improve1 controls for the Restaurant Operations PBC."""

from __future__ import annotations

import hashlib
from typing import Any

from .improve1_capabilities import IMPROVE1_CAPABILITIES, Improve1Capability
from .runtime import (
    RESTAURANT_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    RESTAURANT_OPERATIONS_CONSUMED_EVENT_TYPES,
    RESTAURANT_OPERATIONS_OWNED_TABLES,
    RESTAURANT_OPERATIONS_REQUIRED_EVENT_TOPIC,
    RESTAURANT_OPERATIONS_RUNTIME_TABLES,
)

PBC_KEY = "restaurant_operations"
EVENT_CONTRACT = "AppGen-X"
RESTAURANT_ALLOWED_DATABASE_BACKENDS = RESTAURANT_OPERATIONS_ALLOWED_DATABASE_BACKENDS
RESTAURANT_REQUIRED_EVENT_TOPIC = RESTAURANT_OPERATIONS_REQUIRED_EVENT_TOPIC
RESTAURANT_CAPABILITIES: tuple[Improve1Capability, ...] = IMPROVE1_CAPABILITIES
CAPABILITY_BY_NUMBER = {capability.feature_number: capability for capability in RESTAURANT_CAPABILITIES}
CAPABILITY_BY_SLUG = {capability.slug: capability for capability in RESTAURANT_CAPABILITIES}
RESTAURANT_OWNED_TABLES = tuple(
    dict.fromkeys(
        RESTAURANT_OPERATIONS_OWNED_TABLES
        + RESTAURANT_OPERATIONS_RUNTIME_TABLES
        + tuple(f"restaurant_operations_{capability.slug}_control" for capability in RESTAURANT_CAPABILITIES)
    )
)
RESTAURANT_DECLARED_DEPENDENCIES = tuple(
    dict.fromkeys(
        RESTAURANT_OPERATIONS_CONSUMED_EVENT_TYPES
        + (
            "PolicyChanged",
            "AuditEventSealed",
            "OperationalKpiChanged",
            "InventoryPositionChanged",
            "StaffingSignalChanged",
            "DeliveryMarketplaceOrderReceived",
            "DeliveryMarketplaceStatusChanged",
            "PaymentCheckSettled",
            "LoyaltyGuestUpdated",
            "TemperatureDeviceReadingReceived",
            "VendorDeliveryReceived",
            "BrandPolicyChanged",
            "SiteConfigurationChanged",
            "LaborSchedulePublished",
            "SupplierItemUnavailable",
        )
    )
)
_BASE_FIELDS = (
    "tenant_id",
    "brand_id",
    "site_id",
    "daypart_id",
    "service_date",
    "station_id",
    "operator_id",
    "policy_version",
    "evidence_references",
)
_FIELD_ROWS = """
1|menu_lifecycle_id,item_state,effective_window,channel_scope,daypart_scope,site_scope,rollout_status
2|menu_version_set_id,item_group,price_version,modifier_rule_version,preview_diff,rollback_token,deployment_state
3|modifier_group_id,min_selection,max_selection,nesting_depth,default_value,price_delta,kitchen_instruction
4|allergen_label_id,dietary_flag,allergen_declaration,cross_contact_risk,claim_source,approver,label_status
5|recipe_version_id,target_yield,portion_size,unit_conversion,prep_method,store_override,historical_lock
6|recipe_binding_id,bundle_component,plating_only_flag,shared_sauce,seasonal_garnish,dependency_status,activation_block
7|prep_recommendation_id,reservation_covers,historical_mix,channel_weighting,menu_availability,suggested_quantity,approval_state
8|prep_batch_id,production_time,expiration_time,holding_method,station_assignment,remaining_quantity,discard_reason
9|readiness_check_id,required_prep,required_tool,label_status,sanitizer_status,template_version,opening_blocker
10|kds_ticket_id,ticket_state,transition_actor,transition_timestamp,course_context,recall_reason,state_guard
11|course_pacing_id,course_group,fire_offset,hold_instruction,sync_rule,expo_override,timing_variance
12|expo_board_id,plate_completeness,modifier_fulfillment,allergen_marking,handoff_destination,refire_flag,rejection_reason
13|table_map_id,table_status,party_size,service_phase,assigned_server,turn_timer,active_occupancy
14|reservation_pacing_id,table_inventory,combinable_table,accessibility_constraint,turn_assumption,pacing_result,block_reason
15|waitlist_id,quoted_wait,actual_seat_time,party_preference,text_ready_state,missed_quote_count,promotion_audit
16|order_lifecycle_id,channel,state,promise_time,cancel_reason,refund_status,reconciliation_state
17|modifier_propagation_id,guest_label,server_instruction,kds_instruction,expo_instruction,allergen_impact,price_alignment
18|eighty_six_id,outage_scope,item_or_modifier,approved_substitution,guest_message,channel_sync_state,time_window
19|inventory_boundary_id,ingredient_snapshot,source_system,canonical_quantity,decision_quantity,source_timestamp,boundary_mode
20|depletion_event_id,recipe_usage,theoretical_usage,confirmed_usage,correction_event,void_causal_link,inventory_consumer
21|temperature_check_id,prep_batch_id,temperature_zone,reading_value,threshold_breach,corrective_action,manager_review
22|cross_contact_control_id,recipe_risk,station_risk,tool_change,dedicated_zone,manager_confirmation,routing_decision
23|cooling_reheat_id,cooling_start,cooling_end,reheat_attempts,reuse_count,mandatory_discard_state,violation_status
24|waste_reason_id,waste_taxonomy,station,shift_id,linked_menu_item,linked_batch,estimated_cost
25|yield_variance_id,target_yield,approved_prep_quantity,sold_quantity,recorded_waste,variance_reason,investigation_state
26|comp_void_id,void_type,comp_type,reason_code,approval_threshold,kitchen_impact,service_recovery_context
27|loss_ledger_id,discount_amount,comp_amount,void_amount,waste_amount,reporting_destination,misuse_block
28|delivery_publish_id,channel_id,mapped_item_id,mapped_modifier,lead_time,pickup_window,sync_status
29|delivery_intake_id,marketplace_identifier,promised_time,handoff_type,duplicate_key,late_accept_decision,recovery_path
30|labor_boundary_id,staffing_snapshot,source_system,labor_cost_assumption,service_impact,boundary_mode,dependency_exception
31|staffing_pressure_id,reservation_pressure,order_mix_pressure,prep_intensity,channel_mix,station_pressure,pinch_point
32|station_assignment_id,worker_id,station_skill,certification_status,break_overlap,coverage_risk,opening_blocker
33|guest_recovery_id,table_id,seat_id,order_line,server_action,manager_visit,resolution_state
34|seat_order_id,seat_number,shareable_item,split_responsibility,guest_note,kitchen_rendering,expo_rollup
35|server_ui_flow_id,service_step,modifier_validation,seat_assignment,fire_hold,guest_note_review,escalation_required
36|kds_ui_flow_id,station_view,lane_group,urgent_badge,modifier_prominence,allergen_marker,promised_time_countdown
37|manager_cockpit_id,exception_widget,severity,linked_record,remediation_action,open_count,route_snapshot
38|menu_agent_skill_id,manager_prompt,daypart_assignment,modifier_set,rollout_plan,source_citation,human_confirmation
39|prep_waste_agent_skill_id,prep_shortfall,waste_root_cause,eighty_six_recommendation,batch_change_suggestion,accepted_state,rejected_state
40|reservation_agent_skill_id,seating_plan,quote_adjustment,reseating_action,constraint_explanation,simulation_case,accepted_state
41|service_event_catalog_id,event_type,causal_link,idempotency_key,payload_schema,projection_target,replay_status
42|dependency_health_id,dependency_type,last_processed_offset,freshness_state,duplicate_result,handler_status,exception_action
43|permission_control_id,role_name,site_scope,station_scope,monetary_threshold,safety_threshold,denied_action_state
44|degraded_mode_id,offline_action,queued_kitchen_update,deferred_delivery_ack,sync_status,conflict_resolution,review_required
45|concept_governance_id,brand_scope,concept_scope,region_scope,site_override,inheritance_reason,isolation_result
46|release_scenario_id,scenario_name,api_path,ui_flow,event_sequence,edge_case,scenario_result
47|delivery_sla_id,ready_time,packed_time,courier_arrival,courier_handoff,late_reason,delay_owner
48|boundary_contract_id,adjacent_domain,contract_name,local_owned_state,projection_reference,shared_table_check,proof_result
49|kpi_definition_id,kpi_name,calculation_window,exclusion_rule,drillthrough_path,source_event,explanation
50|release_gate_id,operational_surface,schema_evidence,api_evidence,event_evidence,ui_agent_evidence,gate_result
"""
_DOMAIN_FIELDS = {int(line.split("|", 1)[0]): tuple(line.split("|", 1)[1].split(",")) for line in _FIELD_ROWS.strip().splitlines()}
_PRIMARY_PROOF_FIELDS = {number: f"{CAPABILITY_BY_NUMBER[number].slug}_verified" for number in range(1, 51)}
_FEATURE_FIELDS = {number: _BASE_FIELDS + _DOMAIN_FIELDS[number] + (_PRIMARY_PROOF_FIELDS[number],) for number in range(1, 51)}
_FEATURE_DEPENDENCIES = {
    7: ("OperationalKpiChanged",),
    19: ("InventoryPositionChanged",),
    20: ("InventoryPositionChanged",),
    21: ("TemperatureDeviceReadingReceived",),
    28: ("DeliveryMarketplaceStatusChanged",),
    29: ("DeliveryMarketplaceOrderReceived",),
    30: ("LaborSchedulePublished", "StaffingSignalChanged"),
    31: ("StaffingSignalChanged",),
    32: ("LaborSchedulePublished",),
    33: ("LoyaltyGuestUpdated",),
    42: ("PolicyChanged", "AuditEventSealed", "OperationalKpiChanged"),
    45: ("BrandPolicyChanged", "SiteConfigurationChanged"),
    47: ("DeliveryMarketplaceStatusChanged",),
    48: ("InventoryPositionChanged", "StaffingSignalChanged", "PolicyChanged", "AuditEventSealed"),
}
_HUMAN_CONFIRMATION_FEATURES = (1, 2, 4, 8, 9, 12, 18, 21, 22, 23, 26, 28, 29, 33, 38, 39, 40, 43, 44, 45, 46, 50)
_APPROVAL_REQUIRED_FEATURES = (1, 2, 4, 9, 12, 18, 21, 22, 23, 26, 27, 33, 38, 43, 45, 46, 50)
_NON_MUTATING_FEATURES = (1, 2, 3, 4, 5, 6, 7, 9, 11, 14, 15, 17, 18, 19, 20, 25, 27, 28, 30, 31, 32, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 48, 49, 50)
_AI_PREVIEW_FEATURES = (7, 18, 25, 31, 33, 37, 38, 39, 40, 46, 49, 50)
_FOOD_SAFETY_FEATURES = (4, 8, 9, 12, 21, 22, 23, 24, 32, 36, 37, 43, 44, 46, 50)
_SERVICE_CONTROL_FEATURES = (10, 11, 12, 13, 14, 15, 16, 17, 26, 33, 34, 35, 36, 37, 40, 47, 49, 50)
_COMMERCIAL_CONTROL_FEATURES = (1, 2, 5, 6, 7, 18, 20, 24, 25, 26, 27, 28, 29, 31, 38, 39, 46, 49, 50)
_PROJECTION_ONLY_FEATURES = (7, 19, 20, 21, 28, 29, 30, 31, 32, 33, 42, 45, 47, 48)


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
        "tables": (f"restaurant_operations_{capability.slug}_control",),
        "fields": _FEATURE_FIELDS[capability.feature_number],
        "primary_proof": _PRIMARY_PROOF_FIELDS[capability.feature_number],
        "ui": f"RestaurantOperations{_camel(capability.slug)}Panel",
        "route": f"POST /restaurant-operations/improve1/{capability.slug}",
        "dependencies": _FEATURE_DEPENDENCIES.get(capability.feature_number, ()),
    }


CONTROL_SPECS = {capability.feature_number: _spec_for(capability) for capability in RESTAURANT_CAPABILITIES}


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
        "event_topic": RESTAURANT_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependency_access_mode": "api_event_projection",
        "human_confirmation": True,
        "approver_separate_from_initiator": True,
        "agent_preview_only": True,
        "non_mutating_simulation": True,
        "food_safety_evidence_complete": True,
        "service_evidence_complete": True,
        "commercial_evidence_complete": True,
        "side_effects": (),
    })
    return payload


def _domain_findings(capability: Improve1Capability, payload: dict[str, Any]) -> tuple[str, ...]:
    findings: list[str] = []
    number = capability.feature_number
    spec = CONTROL_SPECS[number]
    if payload.get(spec["primary_proof"]) is not True:
        findings.append(f"{capability.title} requires {spec['primary_proof'].replace('_', ' ')}")
        findings.append(f"{capability.title} requires owned restaurant model, UI, service/API, event, agent, test, and release evidence before approval.")
    if number in _FOOD_SAFETY_FEATURES and payload.get("food_safety_evidence_complete") is not True:
        findings.append("allergens, prep batches, readiness, expo, temperature checks, cross-contact, cooling/reheating, waste, station skills, KDS, manager exceptions, permissions, degraded mode, release scenarios, and release gates require food safety evidence")
    if number in _SERVICE_CONTROL_FEATURES and payload.get("service_evidence_complete") is not True:
        findings.append("KDS state, course pacing, expo, table map, reservation pacing, waitlist, order lifecycle, modifier execution, comps, recovery, seat logic, FOH/KDS UIs, manager cockpit, reservation assistant, delivery SLA, KPIs, and release gates require service evidence")
    if number in _COMMERCIAL_CONTROL_FEATURES and payload.get("commercial_evidence_complete") is not True:
        findings.append("menu lifecycle, version sets, recipe binding, prep, 86, depletion, waste/yield, comps, discounts, delivery publishing, order ingestion, staffing pressure, agent recommendations, release scenarios, KPIs, and release gates require commercial evidence")
    if number in _HUMAN_CONFIRMATION_FEATURES and payload.get("human_confirmation") is not True:
        findings.append("menu activation, rollback, allergen labels, prep overrides, opening checks, expo overrides, 86, safety actions, comps, channel publishing, delivery recovery, guest recovery, assistant actions, permissions, degraded reconciliation, concept overrides, release scenarios, and release gates require human confirmation")
    if number in _APPROVAL_REQUIRED_FEATURES and payload.get("approver_separate_from_initiator") is not True:
        findings.append("high-risk restaurant actions require separated approval for menu rollout, allergen labels, service opening, expo, 86, food safety, comps, losses, guest recovery, assistants, permissions, concept overrides, scenarios, and release gates")
    if number in _AI_PREVIEW_FEATURES and payload.get("agent_preview_only") is not True:
        findings.append("restaurant assistant skills must be evidence-cited, permission-checked, and preview-only until confirmed by operations staff")
    if number in _NON_MUTATING_FEATURES and payload.get("non_mutating_simulation") is not True:
        findings.append("menu previews, modifiers, recipes, prep forecasts, readiness, pacing, reservations, boundaries, depletion, analytics, labor pressure, UIs, agents, dependency health, permissions, governance, release evidence, KPIs, and release gates must be side-effect-free")
    if number in _PROJECTION_ONLY_FEATURES and payload.get("dependency_access_mode") != "api_event_projection":
        findings.append("inventory, staffing, delivery, payment, loyalty, temperature, vendor, brand/site policy, labor schedule, supplier, audit, policy, and KPI facts must use declared APIs, events, or projections")
    if payload.get("event_contract") != EVENT_CONTRACT or payload.get("event_topic") != RESTAURANT_REQUIRED_EVENT_TOPIC:
        findings.append("restaurant operations eventing must use the AppGen-X event contract and package topic")
    if payload.get("stream_engine_picker_visible"):
        findings.append("ordinary PBCs must not expose stream-engine pickers")
    if payload.get("database_backend") not in RESTAURANT_ALLOWED_DATABASE_BACKENDS:
        findings.append("ordinary restaurant datastore must be PostgreSQL, MySQL, or MariaDB")
    if payload.get("shared_table_access"):
        findings.append("restaurant controls must use owned tables plus declared APIs/events/projections")
    return tuple(dict.fromkeys(findings))


def evaluate_restaurant_operations_control(capability: Improve1Capability | str | int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    resolved = _resolve(capability)
    if resolved is None:
        return {"ok": False, "reason": "unknown_capability", "side_effects": ()}
    spec = CONTROL_SPECS[resolved.feature_number]
    candidate = sample_payload_for(resolved)
    candidate.update(dict(payload or {}))
    missing_fields = tuple(field for field in spec["fields"] if candidate.get(field) in (None, "", (), []))
    foreign_tables = tuple(table for table in spec["tables"] if table not in RESTAURANT_OWNED_TABLES)
    undeclared_dependencies = tuple(dependency for dependency in spec["dependencies"] if dependency not in RESTAURANT_DECLARED_DEPENDENCIES)
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
        "required_event_topic": RESTAURANT_REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": RESTAURANT_ALLOWED_DATABASE_BACKENDS,
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


def improve1_restaurant_operations_control_contract() -> dict[str, Any]:
    evaluations = tuple(evaluate_restaurant_operations_control(capability) for capability in RESTAURANT_CAPABILITIES)
    blocking = tuple(item for item in evaluations if not item["ok"])
    return {
        "ok": not blocking,
        "pbc": PBC_KEY,
        "format": "appgen.restaurant-operations-improve1-control.v1",
        "capability_count": len(evaluations),
        "capabilities": evaluations,
        "owned_tables": RESTAURANT_OWNED_TABLES,
        "declared_dependencies": RESTAURANT_DECLARED_DEPENDENCIES,
        "allowed_database_backends": RESTAURANT_ALLOWED_DATABASE_BACKENDS,
        "event_contract": EVENT_CONTRACT,
        "required_event_topic": RESTAURANT_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "blocking_gaps": blocking,
        "side_effects": (),
    }


RESTAURANT_OPERATIONS_CONTROL_FUNCTIONS = {
    capability.slug: (lambda payload=None, slug=capability.slug: evaluate_restaurant_operations_control(slug, payload))
    for capability in RESTAURANT_CAPABILITIES
}
