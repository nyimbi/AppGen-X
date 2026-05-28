"""Operational planning helpers for the airline_operations_control PBC."""
from __future__ import annotations

from datetime import datetime

PBC_KEY = "airline_operations_control"
TIMELINE_MILESTONES = (
    "published_at",
    "scheduled_out",
    "actual_off_block",
    "actual_takeoff",
    "actual_landing",
    "actual_on_block",
    "closed_at",
)


def _coalesce(payload: dict, *keys: str):
    for key in keys:
        value = payload.get(key)
        if value not in (None, ""):
            return value
    return None


def _parse_timestamp(value):
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        return None
    candidate = value.strip()
    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(candidate)
    except ValueError:
        return None


def _minutes_between(start, end):
    start_dt = _parse_timestamp(start)
    end_dt = _parse_timestamp(end)
    if start_dt is None or end_dt is None:
        return None
    return round((end_dt - start_dt).total_seconds() / 60)


def _sort_key(leg: dict):
    scheduled_out = _parse_timestamp(leg.get("scheduled_out"))
    return (scheduled_out is None, scheduled_out or leg["id"])


def _derive_branch(payload: dict, timeline_lookup: dict):
    status = str(payload.get("status", "")).strip().lower()
    leg_type = str(payload.get("leg_type", "scheduled")).strip().lower()
    if timeline_lookup.get("cancelled_at") or status == "cancelled":
        return "cancelled"
    if timeline_lookup.get("diversion_decided_at") or payload.get("diverted_to") or status == "diverted":
        return "diverted"
    if timeline_lookup.get("returned_to_gate_at") or status == "returned_to_gate":
        return "returned_to_gate"
    if leg_type in {"ferry", "reposition", "rescue"}:
        return leg_type
    return "standard"


def _derive_authoritative_status(branch: str, timeline_lookup: dict):
    if branch == "cancelled":
        return "cancelled"
    if branch == "diverted":
        return "diverted"
    if branch == "returned_to_gate":
        return "returned_to_gate"
    if timeline_lookup.get("closed_at"):
        return "closed"
    if timeline_lookup.get("actual_on_block"):
        return "arrived"
    if timeline_lookup.get("actual_landing"):
        return "landed"
    if timeline_lookup.get("actual_takeoff"):
        return "airborne"
    if timeline_lookup.get("actual_off_block"):
        return "departed_gate"
    if timeline_lookup.get("scheduled_out"):
        return "scheduled"
    return "draft"


def _turn_components(payload: dict):
    aircraft_type = str(payload.get("aircraft_type", "narrowbody")).strip().lower()
    base_turn = {"regional": 25, "narrowbody": 35, "widebody": 55}.get(aircraft_type, 40)
    components = [
        {"name": "base_turn", "minutes": payload.get("base_turn_minutes", base_turn)},
        {"name": "crew_change", "minutes": 10 if payload.get("crew_change_required") else 0},
        {"name": "cleaning", "minutes": 5 if payload.get("cleaning_required", True) else 0},
        {"name": "catering", "minutes": 5 if payload.get("catering_required") else 0},
        {"name": "fueling", "minutes": 7 if payload.get("fueling_required", True) else 0},
        {"name": "bags", "minutes": 8 if payload.get("bag_transfer_required", True) else 0},
        {"name": "special_assistance", "minutes": 10 if payload.get("special_assistance_passengers", 0) else 0},
        {"name": "outstation_padding", "minutes": 5 if payload.get("station_type") == "outstation" else 0},
    ]
    return tuple(components)


def _required_turn_minutes(payload: dict):
    explicit = payload.get("minimum_turn_minutes")
    if explicit is not None:
        return int(explicit)
    return sum(component["minutes"] for component in _turn_components(payload))


def normalize_flight_leg(payload: dict) -> dict:
    """Build one authoritative leg timeline from varying operational inputs."""
    source = dict(payload)
    timeline_lookup = {
        "published_at": _coalesce(source, "published_at", "schedule_published_at", "created_at"),
        "scheduled_out": _coalesce(source, "scheduled_out", "scheduled_out_at", "scheduled_departure_at", "departure_scheduled_at"),
        "estimated_out": _coalesce(source, "estimated_out", "estimated_out_at", "estimated_departure_at"),
        "actual_off_block": _coalesce(source, "actual_off_block", "actual_off_block_at", "off_block_at"),
        "actual_takeoff": _coalesce(source, "actual_takeoff", "actual_takeoff_at", "takeoff_at"),
        "actual_landing": _coalesce(source, "actual_landing", "actual_landing_at", "landing_at"),
        "scheduled_in": _coalesce(source, "scheduled_in", "scheduled_in_at", "scheduled_arrival_at", "arrival_scheduled_at"),
        "estimated_on_block": _coalesce(source, "estimated_on_block", "estimated_on_block_at", "estimated_arrival_at"),
        "actual_on_block": _coalesce(source, "actual_on_block", "actual_on_block_at", "on_block_at", "actual_arrival_at"),
        "closed_at": _coalesce(source, "closed_at"),
        "cancelled_at": _coalesce(source, "cancelled_at"),
        "returned_to_gate_at": _coalesce(source, "returned_to_gate_at"),
        "diversion_decided_at": _coalesce(source, "diversion_decided_at", "diverted_at"),
    }
    branch = _derive_branch(source, timeline_lookup)
    authoritative_status = _derive_authoritative_status(branch, timeline_lookup)
    actual_or_estimated_out = _coalesce(
        timeline_lookup,
        "actual_off_block",
        "estimated_out",
        "scheduled_out",
    )
    actual_or_estimated_on = _coalesce(
        timeline_lookup,
        "actual_on_block",
        "estimated_on_block",
        "scheduled_in",
    )
    delay_minutes = _minutes_between(timeline_lookup.get("scheduled_out"), actual_or_estimated_out)
    arrival_delay_minutes = _minutes_between(timeline_lookup.get("scheduled_in"), actual_or_estimated_on)
    turnaround_target_minutes = _required_turn_minutes(source)
    timeline = []
    for milestone in TIMELINE_MILESTONES:
        timeline.append(
            {
                "milestone": milestone,
                "timestamp": timeline_lookup.get(milestone),
                "reached": timeline_lookup.get(milestone) is not None,
            }
        )
    for milestone in ("returned_to_gate_at", "diversion_decided_at", "cancelled_at"):
        if timeline_lookup.get(milestone) is not None or branch in milestone:
            timeline.append(
                {
                    "milestone": milestone,
                    "timestamp": timeline_lookup.get(milestone),
                    "reached": timeline_lookup.get(milestone) is not None,
                }
            )
    return {
        "id": str(_coalesce(source, "id", "flight_leg_id", "code", "flight_number") or "flight_leg-1"),
        "tenant": source.get("tenant", "default"),
        "flight_number": _coalesce(source, "flight_number", "code", "id"),
        "tail_number": _coalesce(source, "tail_number", "aircraft_tail", "tail") or "UNASSIGNED",
        "origin": source.get("origin"),
        "destination": source.get("destination"),
        "completion_airport": source.get("diverted_to") or source.get("destination"),
        "leg_type": source.get("leg_type", "scheduled"),
        "branch": branch,
        "authoritative_status": authoritative_status,
        "delay_minutes": delay_minutes,
        "arrival_delay_minutes": arrival_delay_minutes,
        "minimum_turn_minutes": turnaround_target_minutes,
        "station_type": source.get("station_type", "hub"),
        "timeline": tuple(timeline),
        "timeline_lookup": timeline_lookup,
        "scheduled_out": timeline_lookup.get("scheduled_out"),
        "scheduled_in": timeline_lookup.get("scheduled_in"),
        "estimated_out": timeline_lookup.get("estimated_out"),
        "estimated_on_block": timeline_lookup.get("estimated_on_block"),
        "actual_off_block": timeline_lookup.get("actual_off_block"),
        "actual_on_block": timeline_lookup.get("actual_on_block"),
        "diverted_to": source.get("diverted_to"),
        "turn_components": _turn_components(source),
        "notes": tuple(source.get("notes", ()) or ()),
        "raw_payload": source,
    }


def assess_turn_feasibility(inbound_leg: dict, outbound_leg: dict) -> dict:
    """Evaluate whether the outbound can realistically depart after the inbound."""
    inbound = inbound_leg if inbound_leg.get("timeline_lookup") else normalize_flight_leg(inbound_leg)
    outbound = outbound_leg if outbound_leg.get("timeline_lookup") else normalize_flight_leg(outbound_leg)
    available_turn_minutes = _minutes_between(
        _coalesce(inbound["timeline_lookup"], "actual_on_block", "estimated_on_block", "scheduled_in", "actual_landing"),
        _coalesce(outbound["timeline_lookup"], "actual_off_block", "estimated_out", "scheduled_out"),
    )
    required_turn_minutes = outbound["minimum_turn_minutes"]
    buffer_minutes = None if available_turn_minutes is None else available_turn_minutes - required_turn_minutes
    if available_turn_minutes is None:
        status = "unknown"
    elif buffer_minutes < 0:
        status = "impossible"
    elif buffer_minutes < 15:
        status = "marginal"
    else:
        status = "feasible"
    reasons = []
    if inbound.get("delay_minutes") and inbound["delay_minutes"] > 0:
        reasons.append("late_inbound")
    if outbound.get("branch") in {"cancelled", "diverted", "returned_to_gate"}:
        reasons.append(outbound["branch"])
    for component in outbound["turn_components"]:
        if component["minutes"]:
            reasons.append(component["name"])
    return {
        "ok": True,
        "inbound_leg_id": inbound["id"],
        "outbound_leg_id": outbound["id"],
        "tail_number": outbound["tail_number"],
        "available_turn_minutes": available_turn_minutes,
        "required_turn_minutes": required_turn_minutes,
        "buffer_minutes": buffer_minutes,
        "status": status,
        "risk_level": {"impossible": "high", "marginal": "medium", "feasible": "low", "unknown": "medium"}[status],
        "inbound_delay_minutes": inbound.get("delay_minutes"),
        "reasons": tuple(dict.fromkeys(reasons)),
        "protected_departure": status == "feasible",
        "event_contract": "AppGen-X",
    }


def normalize_aircraft_rotation(payload: dict, flight_legs: tuple[dict, ...]) -> dict:
    source = dict(payload)
    legs_by_id = {leg["id"]: leg for leg in flight_legs}
    ordered_leg_ids = tuple(
        source.get("leg_ids")
        or source.get("flight_leg_ids")
        or source.get("sequence")
        or ()
    )
    ordered_legs = [legs_by_id[leg_id] for leg_id in ordered_leg_ids if leg_id in legs_by_id]
    if not ordered_legs:
        tail_number = _coalesce(source, "tail_number", "aircraft_tail", "tail")
        ordered_legs = [leg for leg in flight_legs if leg["tail_number"] == tail_number]
    ordered_legs = sorted(ordered_legs, key=_sort_key)
    return {
        "rotation_id": str(_coalesce(source, "rotation_id", "id", "tail_number", "aircraft_tail") or "rotation-1"),
        "tenant": source.get("tenant", "default"),
        "tail_number": _coalesce(source, "tail_number", "aircraft_tail", "tail") or (ordered_legs[0]["tail_number"] if ordered_legs else "UNASSIGNED"),
        "operating_day": _coalesce(source, "operating_day", "rotation_date"),
        "leg_ids": tuple(leg["id"] for leg in ordered_legs),
        "maintenance_stop_station": source.get("maintenance_stop_station"),
        "spare_tail_candidates": tuple(source.get("spare_tail_candidates", ()) or ()),
        "raw_payload": source,
    }


def build_tail_rotation_graph(flight_legs: list[dict] | tuple[dict, ...], rotation_payload: dict | None = None) -> dict:
    """Build one tail's continuity graph with turn and dependency visibility."""
    normalized_legs = [leg if leg.get("timeline_lookup") else normalize_flight_leg(leg) for leg in flight_legs]
    normalized_legs = sorted(normalized_legs, key=_sort_key)
    rotation = normalize_aircraft_rotation(rotation_payload or {}, tuple(normalized_legs))
    if rotation["leg_ids"]:
        legs_by_id = {leg["id"]: leg for leg in normalized_legs}
        ordered_legs = [legs_by_id[leg_id] for leg_id in rotation["leg_ids"] if leg_id in legs_by_id]
    else:
        ordered_legs = normalized_legs
    nodes = []
    edges = []
    critical_leg_ids = []
    for index, leg in enumerate(ordered_legs):
        previous_leg = ordered_legs[index - 1] if index else None
        next_leg = ordered_legs[index + 1] if index + 1 < len(ordered_legs) else None
        node = {
            "leg_id": leg["id"],
            "flight_number": leg["flight_number"],
            "origin": leg["origin"],
            "destination": leg["destination"],
            "branch": leg["branch"],
            "authoritative_status": leg["authoritative_status"],
            "delay_minutes": leg["delay_minutes"],
            "previous_leg_id": previous_leg["id"] if previous_leg else None,
            "next_leg_id": next_leg["id"] if next_leg else None,
        }
        if leg["branch"] != "standard" or (leg["delay_minutes"] or 0) >= 15:
            critical_leg_ids.append(leg["id"])
        nodes.append(node)
        if previous_leg is not None:
            edge = assess_turn_feasibility(previous_leg, leg)
            edges.append(edge)
            if edge["status"] != "feasible":
                critical_leg_ids.append(leg["id"])
    broken_turns = tuple(edge for edge in edges if edge["status"] in {"impossible", "marginal"})
    return {
        "ok": True,
        "rotation_id": rotation["rotation_id"],
        "tenant": rotation["tenant"],
        "tail_number": rotation["tail_number"],
        "operating_day": rotation["operating_day"],
        "nodes": tuple(nodes),
        "edges": tuple(edges),
        "critical_leg_ids": tuple(dict.fromkeys(critical_leg_ids)),
        "broken_turn_count": len(broken_turns),
        "recovery_outlook": "stable" if not broken_turns else ("degrading" if any(edge["status"] == "impossible" for edge in broken_turns) else "fragile"),
        "maintenance_stop_station": rotation["maintenance_stop_station"],
        "spare_tail_candidates": rotation["spare_tail_candidates"],
        "event_contract": "AppGen-X",
    }


def build_operational_workbench(
    flight_legs: list[dict] | tuple[dict, ...],
    aircraft_rotations: list[dict] | tuple[dict, ...] | None = None,
    tenant: str = "default",
) -> dict:
    """Project a focused OCC workbench with authoritative timelines and tail alerts."""
    normalized_legs = [
        leg if leg.get("timeline_lookup") else normalize_flight_leg(leg)
        for leg in flight_legs
        if leg.get("tenant", tenant) == tenant
    ]
    normalized_legs = sorted(normalized_legs, key=_sort_key)
    rotations = tuple(aircraft_rotations or ())
    if rotations:
        tail_graphs = tuple(
            build_tail_rotation_graph(normalized_legs, rotation)
            for rotation in rotations
            if rotation.get("tenant", tenant) == tenant
        )
    else:
        tails = tuple(dict.fromkeys(leg["tail_number"] for leg in normalized_legs))
        tail_graphs = tuple(
            build_tail_rotation_graph([leg for leg in normalized_legs if leg["tail_number"] == tail_number], {"tail_number": tail_number, "tenant": tenant})
            for tail_number in tails
        )
    turn_watchlist = []
    for graph in tail_graphs:
        for edge in graph["edges"]:
            if edge["status"] in {"impossible", "marginal"}:
                turn_watchlist.append(edge)
    attention_queue = []
    for leg in normalized_legs:
        reason = None
        if leg["branch"] != "standard":
            reason = leg["branch"]
        elif (leg["delay_minutes"] or 0) >= 15:
            reason = "departure_delay"
        outbound_turn = next((edge for edge in turn_watchlist if edge["outbound_leg_id"] == leg["id"]), None)
        if outbound_turn is not None:
            reason = outbound_turn["status"]
        if reason is not None:
            attention_queue.append(
                {
                    "leg_id": leg["id"],
                    "flight_number": leg["flight_number"],
                    "tail_number": leg["tail_number"],
                    "reason": reason,
                    "authoritative_status": leg["authoritative_status"],
                    "delay_minutes": leg["delay_minutes"],
                }
            )
    reason_priority = {
        "impossible": 0,
        "cancelled": 1,
        "diverted": 1,
        "returned_to_gate": 1,
        "marginal": 2,
        "departure_delay": 3,
    }
    attention_queue = sorted(
        attention_queue,
        key=lambda item: (
            reason_priority.get(item["reason"], 99),
            -(item.get("delay_minutes") or 0),
            item["leg_id"],
        ),
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "legs": tuple(normalized_legs),
        "tail_graphs": tail_graphs,
        "turn_watchlist": tuple(turn_watchlist),
        "attention_queue": tuple(attention_queue),
        "metrics": {
            "flight_leg_count": len(normalized_legs),
            "tail_rotation_count": len(tail_graphs),
            "critical_leg_count": len(tuple(dict.fromkeys(item["leg_id"] for item in attention_queue))),
            "broken_turn_count": len(turn_watchlist),
        },
        "event_contract": "AppGen-X",
    }
