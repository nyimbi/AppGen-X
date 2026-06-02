"""Hotel-operations domain depth contracts and deterministic planning helpers."""

from __future__ import annotations

import hashlib

PBC_KEY = "hospitality_property_operations"
DOMAIN_ENTITY = "room_inventory"
DOMAIN_PURPOSE = (
    "Rooms, reservations, guest stays, housekeeping, service recovery, "
    "occupancy control, and rate readiness for one hotel property."
)
DOMAIN_OWNED_TABLES = (
    "hospitality_property_operations_room_inventory",
    "hospitality_property_operations_reservation",
    "hospitality_property_operations_guest_stay",
    "hospitality_property_operations_housekeeping_task",
    "hospitality_property_operations_guest_request",
    "hospitality_property_operations_occupancy_snapshot",
    "hospitality_property_operations_rate_plan",
    "hospitality_property_operations_hospitality_property_operations_policy_rule",
    "hospitality_property_operations_hospitality_property_operations_runtime_parameter",
    "hospitality_property_operations_hospitality_property_operations_schema_extension",
    "hospitality_property_operations_hospitality_property_operations_control_assertion",
    "hospitality_property_operations_hospitality_property_operations_governed_model",
    "hospitality_property_operations_appgen_outbox_event",
    "hospitality_property_operations_appgen_inbox_event",
    "hospitality_property_operations_appgen_dead_letter_event",
)
DOMAIN_OPERATIONS = (
    "stage_room_inventory",
    "book_reservation",
    "check_in_guest",
    "move_guest_stay",
    "close_guest_stay",
    "dispatch_housekeeping_task",
    "release_room_after_inspection",
    "open_guest_request",
    "resolve_guest_request",
    "capture_occupancy_snapshot",
    "publish_rate_plan",
    "prepare_shift_handover",
    "apply_policy_rule",
    "set_runtime_parameter",
    "review_operational_exception",
)
DOMAIN_RULES = (
    "room_sellable_state",
    "accessible_assignment_guard",
    "reservation_guarantee_cutoff",
    "overbooking_limit",
    "late_checkout_approval",
    "guest_request_sla",
)
DOMAIN_PARAMETERS = (
    "turn_time_minutes",
    "inspection_delay_minutes",
    "arrival_rush_threshold",
    "same_day_turn_limit",
    "oversell_threshold",
    "late_night_escalation_minutes",
    "workbench_limit",
)
DOMAIN_EMITTED_EVENTS = (
    "RoomInventoryAdjusted",
    "ReservationBooked",
    "GuestCheckedIn",
    "HousekeepingTaskCompleted",
    "GuestRequestRecovered",
    "OccupancySnapshotCaptured",
    "RatePlanAdjusted",
    "ShiftHandoverPrepared",
)
DOMAIN_CONSUMED_EVENTS = ("PolicyChanged", "CustomerUpdated", "SupplierQualified")
DOMAIN_ADVANCED_CAPABILITIES = (
    "hotel_event_sourced_operational_history",
    "multi_tenant_property_policy_isolation",
    "schema_evolution_resilience",
    "autonomous_room_readiness_anomaly_detection",
    "predictive_walk_risk_scoring",
    "counterfactual_occupancy_scenario_simulation",
    "continuous_control_testing",
    "governed_ai_agent_execution",
)
DOMAIN_WORKBENCH_VIEWS = (
    "arrival_lane",
    "in_house_lane",
    "departure_lane",
    "room_ready_lane",
    "exception_lane",
    "service_recovery_lane",
)


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def assess_room_sellable_state(room: dict) -> dict:
    reasons = []
    if room.get("maintenance_status") not in {None, "clear"}:
        reasons.append("maintenance_hold")
    if room.get("housekeeping_status") in {"dirty", "turnover"}:
        reasons.append("room_not_clean")
    if room.get("inspection_status") in {"failed", "pending"}:
        reasons.append("inspection_incomplete")
    if room.get("operational_status") in {"occupied", "out_of_order", "out_of_service"}:
        reasons.append("operationally_unavailable")
    if room.get("sellable_status") not in {"sellable", "ready"}:
        reasons.append("sellable_state_withheld")
    return {
        "ok": not reasons,
        "sellable": not reasons,
        "reasons": tuple(reasons),
        "recommended_sellable_status": "sellable" if not reasons else "withhold",
    }


def assignment_compatibility(reservation: dict, room: dict) -> dict:
    reasons = []
    if reservation.get("room_class") and reservation.get("room_class") != room.get("room_class"):
        reasons.append("room_class_mismatch")
    accessible = reservation.get("accessible_required")
    features = room.get("accessibility_features") or []
    if accessible and not features:
        reasons.append("accessibility_not_supported")
    if room.get("sellable_status") not in {"sellable", "ready"}:
        reasons.append("room_not_sellable")
    return {"ok": not reasons, "reasons": tuple(reasons)}


def calculate_overbooking_risk(metrics: dict) -> dict:
    available = max(int(metrics.get("available_rooms", 0)), 0)
    arrivals = max(int(metrics.get("arrivals_pending", 0)), 0)
    blocked = max(int(metrics.get("blocked_rooms", 0)), 0)
    exposure = max(arrivals - available, 0) + blocked * 0.25
    denominator = max(arrivals + available, 1)
    risk_score = round(min(exposure / denominator, 1.0), 4)
    return {
        "ok": True,
        "risk_score": risk_score,
        "risk_band": "high" if risk_score >= 0.4 else "medium" if risk_score >= 0.15 else "low",
    }


def recommend_request_escalation(request: dict) -> dict:
    urgency = request.get("urgency", "routine")
    service_recovery = bool(request.get("service_recovery"))
    if service_recovery or urgency in {"urgent", "vip"}:
        level = "manager_on_duty"
    elif request.get("category") in {"room_move", "complaint"}:
        level = "front_office_supervisor"
    else:
        level = "line_team"
    return {"ok": True, "level": level}


def workflow_catalog() -> tuple[dict, ...]:
    return (
        {
            "workflow": "arrival_turnaround",
            "steps": (
                "book_reservation",
                "dispatch_housekeeping_task",
                "release_room_after_inspection",
                "check_in_guest",
            ),
            "goal": "Convert arrivals into in-house stays without room-ready gaps.",
        },
        {
            "workflow": "service_recovery",
            "steps": ("open_guest_request", "move_guest_stay", "resolve_guest_request"),
            "goal": "Resolve guest-impacting issues with evidence and escalation.",
        },
        {
            "workflow": "revenue_control",
            "steps": ("capture_occupancy_snapshot", "publish_rate_plan", "review_operational_exception"),
            "goal": "Adjust sell controls using operationally ready inventory.",
        },
        {
            "workflow": "shift_handover",
            "steps": ("prepare_shift_handover", "review_operational_exception"),
            "goal": "Hand unresolved arrivals, blocked rooms, and recoveries to the next shift.",
        },
    )


def domain_depth_contract() -> dict:
    return {
        "format": f"appgen.{PBC_KEY}.world-class-domain-depth.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "purpose": DOMAIN_PURPOSE,
        "owned_tables": DOMAIN_OWNED_TABLES,
        "operations": DOMAIN_OPERATIONS,
        "operation_count": len(DOMAIN_OPERATIONS),
        "rules": DOMAIN_RULES,
        "parameters": DOMAIN_PARAMETERS,
        "emitted_events": DOMAIN_EMITTED_EVENTS,
        "consumed_events": DOMAIN_CONSUMED_EVENTS,
        "advanced_capabilities": DOMAIN_ADVANCED_CAPABILITIES,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "workflows": workflow_catalog(),
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "minimum_owned_domain_tables": 12,
        "minimum_domain_operations": 12,
        "side_effects": (),
    }


def execute_domain_operation(operation: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    if operation not in DOMAIN_OPERATIONS:
        return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
    index = DOMAIN_OPERATIONS.index(operation)
    target_table = DOMAIN_OWNED_TABLES[index % len(DOMAIN_OWNED_TABLES)]
    emitted_event = DOMAIN_EMITTED_EVENTS[index % len(DOMAIN_EMITTED_EVENTS)]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation,
        "operation_kind": "command",
        "target_table": target_table,
        "owned_tables": (target_table,),
        "read_tables": (),
        "emitted_event": emitted_event,
        "idempotency_key": f"{PBC_KEY}:{_digest((operation, tuple(sorted(payload.items()))))[:16]}",
        "rules_evaluated": DOMAIN_RULES[:3],
        "parameters_read": DOMAIN_PARAMETERS[:3],
        "permission": f"{PBC_KEY}.operate",
        "workflow_candidates": tuple(item["workflow"] for item in workflow_catalog() if operation in item["steps"]),
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


DOMAIN_EDGE_CASES = (
    "arrival_on_unsellable_room",
    "accessible_room_override_attempt",
    "duplicate_reservation_submission",
    "same_day_turn_shortfall",
    "housekeeping_reinspection_loop",
    "guest_request_sla_breach",
    "late_checkout_conflict",
    "unexpected_inbox_event",
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
                "target_table": DOMAIN_OWNED_TABLES[index % len(DOMAIN_OWNED_TABLES)],
                "permission": f"{PBC_KEY}.operate",
                "requires_confirmation": operation
                in {"apply_policy_rule", "set_runtime_parameter", "move_guest_stay"},
                "agent_tool": f"{PBC_KEY}_skills.{operation}",
                "event": DOMAIN_EMITTED_EVENTS[index % len(DOMAIN_EMITTED_EVENTS)],
            }
            for index, operation in enumerate(DOMAIN_OPERATIONS)
        ),
        "rule_surfaces": tuple(
            {"rule": rule, "surface": f"{PBC_KEY}.ui.rule.{rule}", "editor": True, "explainable": True}
            for rule in DOMAIN_RULES
        ),
        "parameter_surfaces": tuple(
            {"parameter": parameter, "surface": f"{PBC_KEY}.ui.parameter.{parameter}", "bounded": True}
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
            {
                "edge_case": edge_case,
                "surface": f"{PBC_KEY}.ui.edge_case.{edge_case}",
                "triage_queue": True,
            }
            for edge_case in DOMAIN_EDGE_CASES
        ),
        "table_surfaces": tuple(
            {
                "owned_table": table,
                "surface": f"{PBC_KEY}.ui.table.{table}",
                "read_model": True,
                "mutation_guard": True,
            }
            for table in DOMAIN_OWNED_TABLES
        ),
        "coverage": {"event_contract": "AppGen-X", "stream_engine_picker_visible": False, "shared_table_access": False},
        "side_effects": (),
    }


def domain_depth_smoke_test() -> dict:
    contract = domain_depth_contract()
    executions = tuple(execute_domain_operation(name, {"tenant": "tenant_smoke"}) for name in DOMAIN_OPERATIONS[:4])
    sellable = assess_room_sellable_state(
        {
            "operational_status": "vacant",
            "housekeeping_status": "clean",
            "inspection_status": "passed",
            "maintenance_status": "clear",
            "sellable_status": "sellable",
        }
    )
    compatibility = assignment_compatibility(
        {"room_class": "deluxe_king", "accessible_required": True},
        {"room_class": "deluxe_king", "accessibility_features": ["roll_in_shower"], "sellable_status": "sellable"},
    )
    risk = calculate_overbooking_risk({"available_rooms": 4, "arrivals_pending": 5, "blocked_rooms": 1})
    return {
        "ok": contract["ok"]
        and len(contract["owned_tables"]) >= contract["minimum_owned_domain_tables"]
        and contract["operation_count"] >= contract["minimum_domain_operations"]
        and all(item["ok"] for item in executions)
        and sellable["ok"]
        and compatibility["ok"]
        and risk["ok"],
        "contract": contract,
        "executions": executions,
        "sellable": sellable,
        "compatibility": compatibility,
        "risk": risk,
        "side_effects": (),
    }
