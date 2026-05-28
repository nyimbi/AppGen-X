"""Advanced field operations for the field_service_management PBC."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import math

PBC_KEY = "field_service_management"

FIELD_WORKFORCE_TABLES = (
    "field_service_management_technician_live_location",
    "field_service_management_technician_location_breadcrumb",
    "field_service_management_technician_availability",
    "field_service_management_technician_home_base",
    "field_service_management_service_route_plan",
    "field_service_management_service_route_stop",
    "field_service_management_service_route_leg",
    "field_service_management_route_reoptimization",
    "field_service_management_mobile_task_dependency",
    "field_service_management_task_safety_gate",
    "field_service_management_job_tool_requirement",
    "field_service_management_tool_inventory",
    "field_service_management_tool_calibration",
    "field_service_management_van_stock_position",
    "field_service_management_skill_assignment_score",
    "field_service_management_assignment_constraint",
    "field_service_management_geofence_event",
    "field_service_management_location_privacy_consent",
)

FIELD_WORKFORCE_OPERATIONS = (
    "track_technician_location",
    "update_technician_availability",
    "optimize_service_route",
    "reoptimize_route_for_disruption",
    "plan_mobile_task_dependencies",
    "validate_job_tool_requirements",
    "reserve_job_tools",
    "assign_by_skill_location_and_tools",
)

FIELD_WORKFORCE_UI_SURFACES = (
    "live_workforce_map",
    "route_optimizer",
    "technician_availability_board",
    "skill_assignment_console",
    "job_tool_requirement_planner",
    "tool_calibration_and_custody",
    "task_dependency_board",
    "offline_mobile_conflict_queue",
)

FIELD_WORKFORCE_RULES = (
    "location_privacy_policy",
    "route_optimization_policy",
    "skill_certification_policy",
    "tool_calibration_policy",
    "task_dependency_policy",
    "van_stock_policy",
)

FIELD_WORKFORCE_PARAMETERS = (
    "location_staleness_minutes",
    "maximum_route_detour_minutes",
    "minimum_assignment_score",
    "tool_calibration_warning_days",
    "offline_conflict_grace_minutes",
    "geofence_radius_meters",
)

FIELD_WORKFORCE_EVENTS = (
    "TechnicianLocationUpdated",
    "TechnicianAvailabilityChanged",
    "ServiceRouteOptimized",
    "RouteReoptimizationRequested",
    "MobileTaskDependenciesPlanned",
    "JobToolRequirementsValidated",
    "JobToolsReserved",
    "SkillBasedAssignmentRecommended",
)


def _copy(state: dict | None) -> dict:
    base = deepcopy(state or {})
    base.setdefault("records", {})
    base.setdefault("outbox", [])
    base.setdefault("technician_locations", {})
    base.setdefault("technician_availability", {})
    base.setdefault("route_plans", {})
    base.setdefault("task_plans", {})
    base.setdefault("tool_plans", {})
    base.setdefault("assignments", {})
    base.setdefault("idempotency_keys", set())
    base["idempotency_keys"] = set(base.get("idempotency_keys", set()))
    return base


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _event(state: dict, event_type: str, payload: dict) -> None:
    state["outbox"].append(
        {
            "event_type": event_type,
            "topic": "pbc.field_service_management.events",
            "payload": dict(payload),
            "event_contract": "AppGen-X",
            "idempotency_key": _digest((event_type, payload)),
        }
    )


def _distance_km(a: dict, b: dict) -> float:
    lat1 = float(a.get("lat", 0.0))
    lon1 = float(a.get("lon", 0.0))
    lat2 = float(b.get("lat", 0.0))
    lon2 = float(b.get("lon", 0.0))
    return round(math.hypot(lat1 - lat2, lon1 - lon2) * 111.0, 3)


def field_service_management_workforce_capability_contract() -> dict:
    return {
        "format": "appgen.field-service-management.workforce-capability.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "owned_tables": FIELD_WORKFORCE_TABLES,
        "operations": FIELD_WORKFORCE_OPERATIONS,
        "ui_surfaces": FIELD_WORKFORCE_UI_SURFACES,
        "rules": FIELD_WORKFORCE_RULES,
        "parameters": FIELD_WORKFORCE_PARAMETERS,
        "emitted_events": FIELD_WORKFORCE_EVENTS,
        "tracks_live_technician_location": True,
        "supports_route_optimization": True,
        "supports_task_dependency_planning": True,
        "supports_job_tool_requirements": True,
        "supports_skill_based_assignment": True,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def field_service_management_track_technician_location(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    if payload.get("privacy_consent") is not True:
        return {
            "ok": False,
            "reason": "location_privacy_consent_required",
            "owned_table": "field_service_management_location_privacy_consent",
            "state": next_state,
            "side_effects": (),
        }
    technician_id = payload["technician_id"]
    location = {
        "technician_id": technician_id,
        "tenant": payload.get("tenant", "default"),
        "lat": float(payload["lat"]),
        "lon": float(payload["lon"]),
        "accuracy_meters": payload.get("accuracy_meters"),
        "captured_at": payload.get("captured_at", "now"),
        "source": payload.get("source", "mobile"),
        "privacy_consent": True,
        "owned_tables": (
            "field_service_management_technician_live_location",
            "field_service_management_technician_location_breadcrumb",
        ),
    }
    next_state["technician_locations"][technician_id] = location
    _event(next_state, "TechnicianLocationUpdated", location)
    return {"ok": True, "state": next_state, "location": location, "side_effects": ()}


def field_service_management_update_technician_availability(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    availability = {
        "technician_id": payload["technician_id"],
        "tenant": payload.get("tenant", "default"),
        "status": payload.get("status", "available"),
        "capacity_minutes": int(payload.get("capacity_minutes", 480)),
        "home_base": dict(payload.get("home_base", {})),
        "shift_window": tuple(payload.get("shift_window", ())),
        "owned_tables": (
            "field_service_management_technician_availability",
            "field_service_management_technician_home_base",
        ),
    }
    next_state["technician_availability"][availability["technician_id"]] = availability
    _event(next_state, "TechnicianAvailabilityChanged", availability)
    return {"ok": True, "state": next_state, "availability": availability, "side_effects": ()}


def field_service_management_optimize_service_route(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    route_id = payload.get("route_id") or _digest(payload)[:12]
    stops = tuple(dict(stop) for stop in payload.get("stops", ()))
    start = dict(payload.get("start_location") or (stops[0] if stops else {"lat": 0.0, "lon": 0.0}))
    ordered_stops = tuple(
        sorted(
            stops,
            key=lambda stop: (
                int(stop.get("priority", 5)),
                _distance_km(start, stop.get("location", stop)),
                stop.get("window_start", ""),
            ),
        )
    )
    legs = []
    current = start
    total_km = 0.0
    for sequence, stop in enumerate(ordered_stops, start=1):
        target = stop.get("location", stop)
        km = _distance_km(current, target)
        total_km += km
        legs.append(
            {
                "sequence": sequence,
                "from": dict(current),
                "to_stop_id": stop.get("stop_id", f"stop-{sequence}"),
                "distance_km": km,
                "eta_minutes": int(round(km / max(float(payload.get("average_speed_kph", 36.0)), 1.0) * 60))
                + int(payload.get("travel_buffer_minutes", 0)),
            }
        )
        current = target
    route = {
        "route_id": route_id,
        "technician_id": payload.get("technician_id"),
        "ordered_stops": ordered_stops,
        "route_legs": tuple(legs),
        "total_distance_km": round(total_km, 3),
        "constraint_summary": {
            "traffic": payload.get("traffic", "normal"),
            "time_windows_respected": all(stop.get("window_start") and stop.get("window_end") for stop in ordered_stops),
            "skill_constraints_checked": bool(payload.get("required_skills")),
            "tool_constraints_checked": bool(payload.get("required_tools")),
        },
        "owned_tables": (
            "field_service_management_service_route_plan",
            "field_service_management_service_route_stop",
            "field_service_management_service_route_leg",
        ),
    }
    next_state["route_plans"][route_id] = route
    _event(next_state, "ServiceRouteOptimized", route)
    return {"ok": True, "state": next_state, "route": route, "side_effects": ()}


def field_service_management_reoptimize_route_for_disruption(state: dict, payload: dict) -> dict:
    disruption = {
        "route_id": payload["route_id"],
        "reason": payload.get("reason", "field_disruption"),
        "blocked_stop_ids": tuple(payload.get("blocked_stop_ids", ())),
        "new_constraints": dict(payload.get("new_constraints", {})),
        "owned_table": "field_service_management_route_reoptimization",
    }
    route_payload = dict(payload.get("route_payload", {}))
    route_payload.setdefault("route_id", payload["route_id"])
    optimized = field_service_management_optimize_service_route(state, route_payload)
    optimized["route"]["reoptimization"] = disruption
    _event(optimized["state"], "RouteReoptimizationRequested", disruption)
    return {"ok": optimized["ok"], "state": optimized["state"], "route": optimized["route"], "disruption": disruption, "side_effects": ()}


def field_service_management_plan_mobile_task_dependencies(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    work_order_id = payload["work_order_id"]
    tasks = tuple(dict(task) for task in payload.get("tasks", ()))
    dependencies = tuple(
        {
            "task_id": task["task_id"],
            "depends_on": tuple(task.get("depends_on", ())),
            "safety_gate": task.get("safety_gate"),
            "offline_allowed": bool(task.get("offline_allowed", True)),
        }
        for task in tasks
    )
    blocked = tuple(item["task_id"] for item in dependencies if item["depends_on"] and not set(item["depends_on"]).issubset({task["task_id"] for task in tasks}))
    plan = {
        "work_order_id": work_order_id,
        "tasks": tasks,
        "dependencies": dependencies,
        "blocked_tasks": blocked,
        "offline_conflict_policy": payload.get("offline_conflict_policy", "last_writer_requires_review"),
        "owned_tables": (
            "field_service_management_mobile_task",
            "field_service_management_mobile_task_dependency",
            "field_service_management_task_safety_gate",
        ),
    }
    next_state["task_plans"][work_order_id] = plan
    _event(next_state, "MobileTaskDependenciesPlanned", plan)
    return {"ok": not blocked, "state": next_state, "task_plan": plan, "side_effects": ()}


def field_service_management_validate_job_tool_requirements(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    required_tools = tuple(dict(tool) for tool in payload.get("required_tools", ()))
    available_tools = {tool["tool_type"]: dict(tool) for tool in payload.get("available_tools", ())}
    missing = []
    calibration_risks = []
    for required in required_tools:
        available = available_tools.get(required["tool_type"])
        if not available:
            missing.append(required["tool_type"])
            continue
        if required.get("calibrated") and not available.get("calibrated"):
            calibration_risks.append(required["tool_type"])
    plan = {
        "work_order_id": payload["work_order_id"],
        "required_tools": required_tools,
        "available_tools": tuple(available_tools.values()),
        "missing_tools": tuple(missing),
        "calibration_risks": tuple(calibration_risks),
        "van_stock_checked": bool(payload.get("van_stock_checked", False)),
        "owned_tables": (
            "field_service_management_job_tool_requirement",
            "field_service_management_tool_inventory",
            "field_service_management_tool_calibration",
            "field_service_management_van_stock_position",
        ),
    }
    next_state["tool_plans"][payload["work_order_id"]] = plan
    _event(next_state, "JobToolRequirementsValidated", plan)
    return {"ok": not missing and not calibration_risks, "state": next_state, "tool_plan": plan, "side_effects": ()}


def field_service_management_reserve_job_tools(state: dict, payload: dict) -> dict:
    validation = field_service_management_validate_job_tool_requirements(state, payload)
    reservation = {
        "reservation_id": payload.get("reservation_id") or _digest(payload)[:12],
        "work_order_id": payload["work_order_id"],
        "reserved_tools": tuple(tool["tool_type"] for tool in payload.get("required_tools", ())),
        "status": "reserved" if validation["ok"] else "blocked",
        "owned_tables": (
            "field_service_management_tool_inventory",
            "field_service_management_job_tool_requirement",
        ),
    }
    validation["state"]["tool_plans"][payload["work_order_id"]]["reservation"] = reservation
    _event(validation["state"], "JobToolsReserved", reservation)
    return {"ok": validation["ok"], "state": validation["state"], "reservation": reservation, "tool_plan": validation["tool_plan"], "side_effects": ()}


def field_service_management_assign_by_skill_location_and_tools(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    required_skills = set(payload.get("required_skills", ()))
    required_tools = set(payload.get("required_tools", ()))
    job_location = dict(payload.get("job_location", {}))
    candidates = []
    for candidate in payload.get("candidates", ()):
        candidate = dict(candidate)
        skills = set(candidate.get("skills", ()))
        tools = set(candidate.get("tools", ()))
        missing_skills = tuple(sorted(required_skills - skills))
        missing_tools = tuple(sorted(required_tools - tools))
        distance = _distance_km(job_location, candidate.get("location", {})) if job_location else 0.0
        score = 100.0
        score -= 25.0 * len(missing_skills)
        score -= 20.0 * len(missing_tools)
        score -= min(distance, 100.0) * 0.25
        if candidate.get("availability") != "available":
            score -= 35.0
        scored = {
            "technician_id": candidate["technician_id"],
            "score": round(max(score, 0.0), 2),
            "distance_km": distance,
            "missing_skills": missing_skills,
            "missing_tools": missing_tools,
            "availability": candidate.get("availability", "unknown"),
            "explanation": (
                "skills_match" if not missing_skills else "skill_gap",
                "tools_ready" if not missing_tools else "tool_gap",
                "available" if candidate.get("availability") == "available" else "availability_risk",
            ),
        }
        candidates.append(scored)
    ranked = tuple(sorted(candidates, key=lambda item: item["score"], reverse=True))
    recommended = ranked[0] if ranked else None
    threshold = float(payload.get("minimum_assignment_score", 70.0))
    assignment = {
        "work_order_id": payload["work_order_id"],
        "required_skills": tuple(sorted(required_skills)),
        "required_tools": tuple(sorted(required_tools)),
        "ranked_candidates": ranked,
        "recommended_assignment": recommended,
        "meets_threshold": bool(recommended and recommended["score"] >= threshold),
        "owned_tables": (
            "field_service_management_skill_assignment_score",
            "field_service_management_assignment_constraint",
            "field_service_management_dispatch_assignment",
        ),
    }
    next_state["assignments"][payload["work_order_id"]] = assignment
    _event(next_state, "SkillBasedAssignmentRecommended", assignment)
    return {"ok": assignment["meets_threshold"], "state": next_state, "assignment": assignment, "side_effects": ()}


def field_service_management_advanced_field_operations_smoke() -> dict:
    state = {}
    location = field_service_management_track_technician_location(
        state,
        {"technician_id": "tech-1", "lat": -1.2921, "lon": 36.8219, "privacy_consent": True, "tenant": "tenant-smoke"},
    )
    state = location["state"]
    availability = field_service_management_update_technician_availability(
        state,
        {"technician_id": "tech-1", "status": "available", "capacity_minutes": 420, "home_base": {"lat": -1.29, "lon": 36.82}},
    )
    state = availability["state"]
    route = field_service_management_optimize_service_route(
        state,
        {
            "route_id": "route-1",
            "technician_id": "tech-1",
            "start_location": {"lat": -1.29, "lon": 36.82},
            "stops": (
                {"stop_id": "wo-1", "priority": 1, "lat": -1.30, "lon": 36.83, "window_start": "09:00", "window_end": "10:00"},
                {"stop_id": "wo-2", "priority": 2, "lat": -1.31, "lon": 36.84, "window_start": "10:30", "window_end": "12:00"},
            ),
            "required_skills": ("hvac",),
            "required_tools": ("multimeter",),
        },
    )
    state = route["state"]
    tasks = field_service_management_plan_mobile_task_dependencies(
        state,
        {
            "work_order_id": "wo-1",
            "tasks": (
                {"task_id": "isolate-power", "safety_gate": "lockout", "offline_allowed": False},
                {"task_id": "replace-part", "depends_on": ("isolate-power",), "offline_allowed": True},
            ),
        },
    )
    state = tasks["state"]
    tools = field_service_management_reserve_job_tools(
        state,
        {
            "work_order_id": "wo-1",
            "required_tools": ({"tool_type": "multimeter", "calibrated": True},),
            "available_tools": ({"tool_type": "multimeter", "calibrated": True, "location": "van"},),
            "van_stock_checked": True,
        },
    )
    state = tools["state"]
    assignment = field_service_management_assign_by_skill_location_and_tools(
        state,
        {
            "work_order_id": "wo-1",
            "job_location": {"lat": -1.30, "lon": 36.83},
            "required_skills": ("hvac",),
            "required_tools": ("multimeter",),
            "candidates": (
                {
                    "technician_id": "tech-1",
                    "skills": ("hvac", "electrical"),
                    "tools": ("multimeter",),
                    "availability": "available",
                    "location": {"lat": -1.2921, "lon": 36.8219},
                },
                {
                    "technician_id": "tech-2",
                    "skills": ("plumbing",),
                    "tools": (),
                    "availability": "busy",
                    "location": {"lat": -1.40, "lon": 36.70},
                },
            ),
            "minimum_assignment_score": 70,
        },
    )
    contract = field_service_management_workforce_capability_contract()
    return {
        "ok": all(
            item["ok"]
            for item in (
                contract,
                location,
                availability,
                route,
                tasks,
                tools,
                assignment,
            )
        )
        and assignment["assignment"]["recommended_assignment"]["technician_id"] == "tech-1"
        and len(assignment["state"]["outbox"]) >= len(FIELD_WORKFORCE_EVENTS) - 1,
        "contract": contract,
        "location": location,
        "availability": availability,
        "route": route,
        "task_plan": tasks,
        "tool_plan": tools,
        "assignment": assignment,
        "side_effects": (),
    }
