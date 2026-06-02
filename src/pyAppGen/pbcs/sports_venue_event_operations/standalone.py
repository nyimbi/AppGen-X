"""Standalone one-PBC application logic for sports venue event operations."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from .runtime import (
    SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC,
)


DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_policy": "standard_event_day",
    "workbench_limit": 100,
    "stream_engine_picker_visible": False,
}

DEFAULT_PARAMETERS = {
    "changeover_buffer_minutes": 180,
    "gate_scan_rate_threshold": 550,
    "staffing_relief_minutes": 30,
    "weather_lightning_radius_miles": 8,
    "crowd_density_alert_threshold": 0.82,
    "ticket_hold_release_deadline_minutes": 45,
    "workbench_limit": 100,
}

DEFAULT_RULES = (
    {
        "rule_id": "sports.calendar.default",
        "scope": "event_calendar",
        "allow_doubleheader": True,
        "minimum_turnover_minutes": 180,
        "status": "active",
    },
    {
        "rule_id": "sports.accessibility.default",
        "scope": "seat_inventory",
        "accessible_inventory_floor": 0.98,
        "requires_supervisor_acknowledgement": True,
        "status": "active",
    },
    {
        "rule_id": "sports.weather.default",
        "scope": "weather_delay",
        "lightning_radius_miles": 8,
        "heat_index_alert": 103,
        "status": "active",
    },
)

DOCS = ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md")
PBC_KEY = "sports_venue_event_operations"


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))


def _ensure_state(state: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(state)
    defaults: dict[str, Any] = {
        "configuration": deepcopy(DEFAULT_CONFIGURATION),
        "parameters": deepcopy(DEFAULT_PARAMETERS),
        "rules": {rule["rule_id"]: deepcopy(rule) for rule in DEFAULT_RULES},
        "venues": {},
        "zones": {},
        "seats": {},
        "events": {},
        "ingress_plans": {},
        "egress_plans": {},
        "staffing_plans": {},
        "concession_plans": {},
        "ticketing": {},
        "credentials": {},
        "security_plans": {},
        "crowd_observations": {},
        "incidents": {},
        "weather_delays": {},
        "production_readiness": {},
        "sponsor_activations": {},
        "cleaning_turnovers": {},
        "accessibility_cases": {},
        "lost_found": {},
        "emergency_operations": {},
        "revenue_attendance": {},
        "documents": {},
        "instructions": {},
        "outbox": (),
        "audit_log": (),
    }
    for key, default in defaults.items():
        if key not in enriched:
            enriched[key] = deepcopy(default)
    return enriched


def _next_id(prefix: str, bucket: dict[str, Any]) -> str:
    return f"{prefix}_{len(bucket) + 1:05d}"


def _append_audit(state: dict[str, Any], action: str, data: dict[str, Any]) -> dict[str, Any]:
    audit_log = tuple(state.get("audit_log", ()))
    entry = {
        "audit_id": f"audit_{len(audit_log) + 1:05d}",
        "action": action,
        "data": deepcopy(data),
    }
    return {**state, "audit_log": (*audit_log, entry)}


def _append_outbox(state: dict[str, Any], event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    outbox = tuple(state.get("outbox", ()))
    envelope = {
        "event_type": event_type,
        "topic": SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "payload": deepcopy(payload),
        "event_contract": "AppGen-X",
    }
    return {**state, "outbox": (*outbox, envelope)}


def _upsert(state: dict[str, Any], bucket_name: str, record_id: str, record: dict[str, Any], event_type: str) -> dict[str, Any]:
    bucket = {**state.get(bucket_name, {})}
    bucket[record_id] = deepcopy(record)
    next_state = {**state, bucket_name: bucket}
    next_state = _append_audit(next_state, f"upsert_{bucket_name}", {"record_id": record_id})
    return _append_outbox(next_state, event_type, record)


def _status_from_density(density: float) -> str:
    if density >= 0.9:
        return "critical"
    if density >= 0.8:
        return "warning"
    return "normal"


def _normalize_event(state: dict[str, Any], event_id: str) -> dict[str, Any]:
    event = deepcopy(state["events"][event_id])
    event["incident_count"] = sum(1 for item in state["incidents"].values() if item["event_id"] == event_id)
    event["weather_state"] = next(
        (
            item["state"]
            for item in reversed(tuple(state["weather_delays"].values()))
            if item["event_id"] == event_id
        ),
        "clear",
    )
    event["credential_count"] = sum(
        1 for item in state["credentials"].values() if item["event_id"] == event_id
    )
    return event


class SportsVenueEventOperationsStandaloneApp:
    def __init__(self, tenant: str = "default") -> None:
        self.tenant = tenant
        self.state = _ensure_state({})

    def configure(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        merged = {**self.state["configuration"], **_copy_payload(config)}
        merged["database_backend"] = merged.get("database_backend", "postgresql")
        merged["event_topic"] = SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC
        ok = merged["database_backend"] in SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS
        merged["event_contract"] = "AppGen-X"
        merged["stream_engine_picker_visible"] = False
        self.state = {**self.state, "configuration": merged}
        return {"ok": ok, "configuration": deepcopy(merged), "side_effects": ()}

    def register_defaults(self) -> dict[str, Any]:
        self.state = {
            **self.state,
            "parameters": deepcopy(DEFAULT_PARAMETERS),
            "rules": {rule["rule_id"]: deepcopy(rule) for rule in DEFAULT_RULES},
        }
        self.state = _append_audit(self.state, "register_defaults", {"rules": len(DEFAULT_RULES)})
        return {
            "ok": True,
            "parameters": deepcopy(self.state["parameters"]),
            "rules": tuple(self.state["rules"].values()),
            "side_effects": (),
        }

    def upsert_venue_layout(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        venue_id = data.get("venue_id", _next_id("venue", self.state["venues"]))
        zones = tuple(data.get("zones", ()))
        seats = tuple(data.get("seats", ()))
        record = {
            "venue_id": venue_id,
            "tenant": data.get("tenant", self.tenant),
            "venue_name": data.get("venue_name", venue_id.replace("_", " ").title()),
            "venue_type": data.get("venue_type", "arena"),
            "zones": zones,
            "accessible_routes": tuple(data.get("accessible_routes", ())),
        }
        self.state = _upsert(self.state, "venues", venue_id, record, "SportsVenueEventOperationsCreated")
        zone_records = {**self.state["zones"]}
        for index, zone in enumerate(zones, start=1):
            zone_id = zone.get("zone_id", f"{venue_id}_zone_{index}")
            zone_records[zone_id] = {
                "zone_id": zone_id,
                "venue_id": venue_id,
                "name": zone.get("name", zone_id),
                "gate_count": zone.get("gate_count", 0),
                "capacity": zone.get("capacity", 0),
            }
        seat_records = {**self.state["seats"]}
        for index, seat in enumerate(seats, start=1):
            seat_id = seat.get("seat_id", f"{venue_id}_seat_{index}")
            seat_records[seat_id] = {
                "seat_id": seat_id,
                "venue_id": venue_id,
                "zone_id": seat.get("zone_id"),
                "seat_class": seat.get("seat_class", "general"),
                "accessible": bool(seat.get("accessible", False)),
                "status": seat.get("status", "available"),
            }
        self.state = {**self.state, "zones": zone_records, "seats": seat_records}
        return {
            "ok": True,
            "venue": deepcopy(record),
            "zone_count": len(zones),
            "seat_count": len(seats),
            "side_effects": (),
        }

    def plan_zone_seating(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        coordination = {
            "ticketing_id": data.get("ticketing_id", f"ticketing_{event_id}"),
            "event_id": event_id,
            "hold_groups": tuple(data.get("hold_groups", ())),
            "camera_kills": tuple(data.get("camera_kills", ())),
            "accessible_seat_relocations": tuple(data.get("accessible_seat_relocations", ())),
            "status": data.get("status", "planned"),
        }
        self.state = _upsert(
            self.state,
            "ticketing",
            coordination["ticketing_id"],
            coordination,
            "SportsVenueEventOperationsUpdated",
        )
        return {"ok": True, "ticketing": deepcopy(coordination), "side_effects": ()}

    def schedule_event(self, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        event_id = data.get("event_id", _next_id("event", self.state["events"]))
        record = {
            "event_id": event_id,
            "tenant": data.get("tenant", self.tenant),
            "venue_id": data.get("venue_id"),
            "event_name": data.get("event_name", event_id.replace("_", " ").title()),
            "event_type": data.get("event_type", "game"),
            "event_date": data.get("event_date", "2026-01-01"),
            "status": data.get("status", "scheduled"),
            "hold_type": data.get("hold_type", "hard_hold"),
            "gates_open_at": data.get("gates_open_at", "18:00"),
            "start_at": data.get("start_at", "19:00"),
            "changeover_buffer_minutes": data.get(
                "changeover_buffer_minutes", self.state["parameters"]["changeover_buffer_minutes"]
            ),
            "curfew_at": data.get("curfew_at", "23:00"),
        }
        self.state = _upsert(self.state, "events", event_id, record, "SportsVenueEventOperationsCreated")
        return {"ok": True, "event": deepcopy(record), "side_effects": ()}

    def plan_ingress_egress(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        ingress_id = data.get("ingress_id", f"ingress_{event_id}")
        egress_id = data.get("egress_id", f"egress_{event_id}")
        ingress = {
            "ingress_id": ingress_id,
            "event_id": event_id,
            "gate_plan": tuple(data.get("gate_plan", ())),
            "queue_capacity": data.get("queue_capacity", 0),
            "fallback_routes": tuple(data.get("fallback_routes", ())),
            "status": data.get("status", "ready"),
        }
        egress = {
            "egress_id": egress_id,
            "event_id": event_id,
            "routes": tuple(data.get("egress_routes", ())),
            "phased_release": tuple(data.get("phased_release", ())),
            "transit_windows": tuple(data.get("transit_windows", ())),
            "status": data.get("status", "ready"),
        }
        self.state = _upsert(self.state, "ingress_plans", ingress_id, ingress, "SportsVenueEventOperationsUpdated")
        self.state = _upsert(self.state, "egress_plans", egress_id, egress, "SportsVenueEventOperationsUpdated")
        return {"ok": True, "ingress": deepcopy(ingress), "egress": deepcopy(egress), "side_effects": ()}

    def assign_staffing(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        staffing_id = data.get("staffing_id", f"staffing_{event_id}")
        shifts = tuple(data.get("shifts", ()))
        planned = sum(shift.get("planned", 0) for shift in shifts)
        assigned = sum(shift.get("assigned", 0) for shift in shifts)
        record = {
            "staffing_id": staffing_id,
            "event_id": event_id,
            "roles": tuple(data.get("roles", ())),
            "shifts": shifts,
            "coverage_gap": max(planned - assigned, 0),
            "status": "gap" if planned > assigned else data.get("status", "ready"),
        }
        self.state = _upsert(self.state, "staffing_plans", staffing_id, record, "SportsVenueEventOperationsUpdated")
        return {"ok": True, "staffing": deepcopy(record), "side_effects": ()}

    def plan_concessions(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        concession_id = data.get("concession_id", f"concession_{event_id}")
        record = {
            "concession_id": concession_id,
            "event_id": event_id,
            "stand_count": data.get("stand_count", 0),
            "menu_focus": tuple(data.get("menu_focus", ())),
            "alcohol_cutoff": data.get("alcohol_cutoff", "third_quarter"),
            "mobile_ordering": bool(data.get("mobile_ordering", True)),
            "status": data.get("status", "ready"),
        }
        self.state = _upsert(self.state, "concession_plans", concession_id, record, "SportsVenueEventOperationsUpdated")
        return {"ok": True, "concession_plan": deepcopy(record), "side_effects": ()}

    def coordinate_ticketing(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self.plan_zone_seating(event_id, payload)

    def issue_credential(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        credential_id = data.get("credential_id", _next_id("credential", self.state["credentials"]))
        record = {
            "credential_id": credential_id,
            "event_id": event_id,
            "holder_name": data.get("holder_name", credential_id),
            "credential_type": data.get("credential_type", "staff"),
            "zone_access": tuple(data.get("zone_access", ())),
            "access_windows": tuple(data.get("access_windows", ())),
            "escort_required": bool(data.get("escort_required", False)),
            "status": data.get("status", "issued"),
        }
        self.state = _upsert(self.state, "credentials", credential_id, record, "SportsVenueEventOperationsApproved")
        return {"ok": True, "credential": deepcopy(record), "side_effects": ()}

    def update_security_posture(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        plan_id = data.get("security_plan_id", f"security_{event_id}")
        record = {
            "security_plan_id": plan_id,
            "event_id": event_id,
            "security_level": data.get("security_level", "heightened"),
            "screening_lanes": tuple(data.get("screening_lanes", ())),
            "magnetometers": data.get("magnetometers", 0),
            "credential_exceptions": tuple(data.get("credential_exceptions", ())),
            "status": data.get("status", "ready"),
        }
        self.state = _upsert(self.state, "security_plans", plan_id, record, "SportsVenueEventOperationsApproved")
        return {"ok": True, "security_plan": deepcopy(record), "side_effects": ()}

    def record_crowd_snapshot(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        snapshot_id = data.get("snapshot_id", _next_id("crowd", self.state["crowd_observations"]))
        density = float(data.get("density", 0.0))
        record = {
            "snapshot_id": snapshot_id,
            "event_id": event_id,
            "zone_id": data.get("zone_id", "unknown"),
            "density": density,
            "status": _status_from_density(density),
            "queue_minutes": data.get("queue_minutes", 0),
            "note": data.get("note", ""),
        }
        event_type = "SportsVenueEventOperationsExceptionOpened" if record["status"] != "normal" else "SportsVenueEventOperationsUpdated"
        self.state = _upsert(self.state, "crowd_observations", snapshot_id, record, event_type)
        return {"ok": True, "crowd_observation": deepcopy(record), "side_effects": ()}

    def open_incident(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        incident_id = data.get("incident_id", _next_id("incident", self.state["incidents"]))
        record = {
            "incident_id": incident_id,
            "event_id": event_id,
            "category": data.get("category", "crowd"),
            "severity": data.get("severity", "medium"),
            "location": data.get("location", "unknown"),
            "owner_team": data.get("owner_team", "guest_services"),
            "status": data.get("status", "open"),
        }
        self.state = _upsert(self.state, "incidents", incident_id, record, "SportsVenueEventOperationsExceptionOpened")
        return {"ok": True, "incident": deepcopy(record), "side_effects": ()}

    def manage_weather_delay(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        weather_id = data.get("weather_id", _next_id("weather", self.state["weather_delays"]))
        record = {
            "weather_id": weather_id,
            "event_id": event_id,
            "hazard": data.get("hazard", "lightning"),
            "state": data.get("state", "watch"),
            "restart_target": data.get("restart_target", "pending"),
            "public_message": data.get("public_message", "Weather monitoring active"),
            "status": data.get("status", "active"),
        }
        self.state = _upsert(self.state, "weather_delays", weather_id, record, "SportsVenueEventOperationsExceptionOpened")
        event = {**self.state["events"].get(event_id, {}), "status": record["state"]}
        if event:
            self.state = {**self.state, "events": {**self.state["events"], event_id: event}}
        return {"ok": True, "weather_delay": deepcopy(record), "side_effects": ()}

    def confirm_production_ready(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        production_id = data.get("production_id", f"production_{event_id}")
        ready_checks = {
            "scoreboard": bool(data.get("scoreboard", True)),
            "public_address": bool(data.get("public_address", True)),
            "compound": bool(data.get("compound", True)),
            "camera_positions": bool(data.get("camera_positions", True)),
        }
        record = {
            "production_id": production_id,
            "event_id": event_id,
            "checks": ready_checks,
            "run_of_show": tuple(data.get("run_of_show", ())),
            "status": "ready" if all(ready_checks.values()) else "degraded",
        }
        self.state = _upsert(self.state, "production_readiness", production_id, record, "SportsVenueEventOperationsApproved")
        return {"ok": True, "production_readiness": deepcopy(record), "side_effects": ()}

    def activate_sponsor(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        activation_id = data.get("activation_id", _next_id("activation", self.state["sponsor_activations"]))
        record = {
            "activation_id": activation_id,
            "event_id": event_id,
            "sponsor_name": data.get("sponsor_name", "title_partner"),
            "activation_type": data.get("activation_type", "concourse"),
            "window": data.get("window", "pregame"),
            "status": data.get("status", "scheduled"),
        }
        self.state = _upsert(self.state, "sponsor_activations", activation_id, record, "SportsVenueEventOperationsUpdated")
        return {"ok": True, "sponsor_activation": deepcopy(record), "side_effects": ()}

    def complete_turnover(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        turnover_id = data.get("turnover_id", _next_id("turnover", self.state["cleaning_turnovers"]))
        record = {
            "turnover_id": turnover_id,
            "event_id": event_id,
            "phase": data.get("phase", "post_event_clean"),
            "crew_status": data.get("crew_status", "complete"),
            "inspection_owner": data.get("inspection_owner", "operations"),
            "status": data.get("status", "complete"),
        }
        self.state = _upsert(self.state, "cleaning_turnovers", turnover_id, record, "SportsVenueEventOperationsApproved")
        return {"ok": True, "cleaning_turnover": deepcopy(record), "side_effects": ()}

    def log_accessibility_request(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        case_id = data.get("case_id", _next_id("access", self.state["accessibility_cases"]))
        record = {
            "case_id": case_id,
            "event_id": event_id,
            "request_type": data.get("request_type", "relocation"),
            "location": data.get("location", "section_101"),
            "status": data.get("status", "open"),
            "resolution": data.get("resolution", "pending"),
        }
        self.state = _upsert(self.state, "accessibility_cases", case_id, record, "SportsVenueEventOperationsUpdated")
        return {"ok": True, "accessibility_case": deepcopy(record), "side_effects": ()}

    def register_lost_and_found(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        item_id = data.get("item_id", _next_id("lost_found", self.state["lost_found"]))
        record = {
            "item_id": item_id,
            "event_id": event_id,
            "description": data.get("description", "lost_item"),
            "found_location": data.get("found_location", "guest_services"),
            "status": data.get("status", "logged"),
        }
        self.state = _upsert(self.state, "lost_found", item_id, record, "SportsVenueEventOperationsUpdated")
        return {"ok": True, "lost_found_item": deepcopy(record), "side_effects": ()}

    def start_emergency_operation(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        operation_id = data.get("operation_id", _next_id("emergency", self.state["emergency_operations"]))
        record = {
            "operation_id": operation_id,
            "event_id": event_id,
            "playbook": data.get("playbook", "shelter_in_place"),
            "incident_level": data.get("incident_level", "level_2"),
            "commander": data.get("commander", "event_commander"),
            "status": data.get("status", "active"),
        }
        self.state = _upsert(self.state, "emergency_operations", operation_id, record, "SportsVenueEventOperationsExceptionOpened")
        return {"ok": True, "emergency_operation": deepcopy(record), "side_effects": ()}

    def record_attendance_and_revenue(self, event_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = _copy_payload(payload)
        snapshot_id = data.get("snapshot_id", _next_id("revenue", self.state["revenue_attendance"]))
        record = {
            "snapshot_id": snapshot_id,
            "event_id": event_id,
            "attendance": int(data.get("attendance", 0)),
            "paid_attendance": int(data.get("paid_attendance", 0)),
            "gross_revenue": float(data.get("gross_revenue", 0.0)),
            "net_revenue": float(data.get("net_revenue", 0.0)),
            "status": data.get("status", "captured"),
        }
        self.state = _upsert(self.state, "revenue_attendance", snapshot_id, record, "SportsVenueEventOperationsApproved")
        return {"ok": True, "revenue_attendance_snapshot": deepcopy(record), "side_effects": ()}

    def document_intake(self, document: str | None = None, instruction: str | None = None) -> dict[str, Any]:
        document_text = str(document or "")
        instruction_text = str(instruction or "")
        combined = f"{document_text} {instruction_text}".lower()
        action = "update" if "update" in combined or "delay" in combined else "create"
        table_map = (
            ("weather", f"{PBC_KEY}_weather_delay"),
            ("incident", f"{PBC_KEY}_incident"),
            ("credential", f"{PBC_KEY}_credential"),
            ("seat", f"{PBC_KEY}_ticketing_coordination"),
            ("broadcast", f"{PBC_KEY}_production_readiness"),
            ("sponsor", f"{PBC_KEY}_sponsor_activation"),
            ("access", f"{PBC_KEY}_accessibility_case"),
        )
        candidate_tables = tuple(table for word, table in table_map if word in combined) or (
            f"{PBC_KEY}_event_calendar",
            f"{PBC_KEY}_ingress_plan",
            f"{PBC_KEY}_security_plan",
        )
        preview = {
            "action": action,
            "table": candidate_tables[0],
            "requires_confirmation": True,
            "event_contract": "AppGen-X",
        }
        intake_id = _next_id("doc", self.state["documents"])
        record = {
            "intake_id": intake_id,
            "document": document_text,
            "instruction": instruction_text,
            "candidate_tables": candidate_tables,
            "crud_preview": preview,
        }
        self.state = {**self.state, "documents": {**self.state["documents"], intake_id: record}}
        return {"ok": True, **deepcopy(record), "side_effects": ()}

    def crud_mutation_plan(self, action: str = "read", table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        selected = table or f"{PBC_KEY}_event_calendar"
        allowed_tables = (
            f"{PBC_KEY}_venue",
            f"{PBC_KEY}_venue_zone",
            f"{PBC_KEY}_seat_inventory",
            f"{PBC_KEY}_event_calendar",
            f"{PBC_KEY}_ingress_plan",
            f"{PBC_KEY}_egress_plan",
            f"{PBC_KEY}_staffing_plan",
            f"{PBC_KEY}_concession_plan",
            f"{PBC_KEY}_ticketing_coordination",
            f"{PBC_KEY}_credential",
            f"{PBC_KEY}_security_plan",
            f"{PBC_KEY}_crowd_observation",
            f"{PBC_KEY}_incident",
            f"{PBC_KEY}_weather_delay",
            f"{PBC_KEY}_production_readiness",
            f"{PBC_KEY}_sponsor_activation",
            f"{PBC_KEY}_cleaning_turnover",
            f"{PBC_KEY}_accessibility_case",
            f"{PBC_KEY}_lost_found_item",
            f"{PBC_KEY}_emergency_operation",
            f"{PBC_KEY}_revenue_attendance_snapshot",
        )
        return {
            "ok": selected in allowed_tables,
            "action": action,
            "table": selected,
            "payload_keys": tuple(sorted(dict(payload or {}))),
            "requires_confirmation": action != "read",
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "side_effects": (),
        }

    def build_workbench(self, tenant: str | None = None, event_id: str | None = None, role: str = "operator") -> dict[str, Any]:
        scoped_events = [
            _normalize_event(self.state, current_event_id)
            for current_event_id in self.state["events"]
            if event_id is None or current_event_id == event_id
        ]
        metrics = {
            "event_count": len(scoped_events),
            "incident_count": len(self.state["incidents"]),
            "weather_delay_count": len(self.state["weather_delays"]),
            "credential_count": len(self.state["credentials"]),
            "staffing_gap_count": sum(
                1 for plan in self.state["staffing_plans"].values() if plan["coverage_gap"] > 0
            ),
            "crowd_alert_count": sum(
                1
                for snapshot in self.state["crowd_observations"].values()
                if snapshot["status"] != "normal"
            ),
            "gross_revenue": round(
                sum(item["gross_revenue"] for item in self.state["revenue_attendance"].values()), 2
            ),
            "attendance_total": sum(item["attendance"] for item in self.state["revenue_attendance"].values()),
        }
        return {
            "ok": True,
            "tenant": tenant or self.tenant,
            "role": role,
            "events": tuple(scoped_events),
            "metrics": metrics,
            "alerts": {
                "staffing": tuple(
                    plan["staffing_id"]
                    for plan in self.state["staffing_plans"].values()
                    if plan["coverage_gap"] > 0
                ),
                "crowd": tuple(
                    snapshot["snapshot_id"]
                    for snapshot in self.state["crowd_observations"].values()
                    if snapshot["status"] != "normal"
                ),
                "weather": tuple(delay["weather_id"] for delay in self.state["weather_delays"].values()),
            },
            "side_effects": (),
        }

    def get_event_snapshot(self, event_id: str) -> dict[str, Any]:
        if event_id not in self.state["events"]:
            return {"ok": False, "reason": "event_not_found", "event_id": event_id, "side_effects": ()}
        related = {
            "event": _normalize_event(self.state, event_id),
            "ingress": next((item for item in self.state["ingress_plans"].values() if item["event_id"] == event_id), None),
            "egress": next((item for item in self.state["egress_plans"].values() if item["event_id"] == event_id), None),
            "staffing": next((item for item in self.state["staffing_plans"].values() if item["event_id"] == event_id), None),
            "concessions": next((item for item in self.state["concession_plans"].values() if item["event_id"] == event_id), None),
            "ticketing": next((item for item in self.state["ticketing"].values() if item["event_id"] == event_id), None),
            "security": next((item for item in self.state["security_plans"].values() if item["event_id"] == event_id), None),
            "production": next((item for item in self.state["production_readiness"].values() if item["event_id"] == event_id), None),
            "incidents": tuple(item for item in self.state["incidents"].values() if item["event_id"] == event_id),
            "weather_delays": tuple(item for item in self.state["weather_delays"].values() if item["event_id"] == event_id),
            "analytics": tuple(item for item in self.state["revenue_attendance"].values() if item["event_id"] == event_id),
        }
        return {"ok": True, "snapshot": deepcopy(related), "side_effects": ()}

    def close(self) -> None:
        return None


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_class": "SportsVenueEventOperationsStandaloneApp",
        "implementation_directory": "src/pyAppGen/pbcs/sports_venue_event_operations",
        "service_methods": (
            "configure",
            "register_defaults",
            "upsert_venue_layout",
            "plan_zone_seating",
            "schedule_event",
            "plan_ingress_egress",
            "assign_staffing",
            "plan_concessions",
            "coordinate_ticketing",
            "issue_credential",
            "update_security_posture",
            "record_crowd_snapshot",
            "open_incident",
            "manage_weather_delay",
            "confirm_production_ready",
            "activate_sponsor",
            "complete_turnover",
            "log_accessibility_request",
            "register_lost_and_found",
            "start_emergency_operation",
            "record_attendance_and_revenue",
            "document_intake",
            "crud_mutation_plan",
            "build_workbench",
            "get_event_snapshot",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench"),
        "docs": DOCS,
        "event_contract": "AppGen-X",
        "event_topic": SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_backends": SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    }


def documentation_presence() -> dict[str, Any]:
    base = Path(__file__).resolve().parent
    missing = tuple(name for name in DOCS if not (base / name).exists())
    return {"ok": not missing, "missing": missing, "docs": DOCS, "side_effects": ()}


def standalone_smoke_test() -> dict[str, Any]:
    app = SportsVenueEventOperationsStandaloneApp(tenant="tenant_smoke")
    configured = app.configure({"database_backend": "postgresql"})
    defaults = app.register_defaults()
    venue = app.upsert_venue_layout(
        {
            "venue_id": "venue_alpha",
            "venue_name": "Alpha Arena",
            "zones": (
                {"zone_id": "gate_north", "name": "North Gate", "gate_count": 6, "capacity": 12000},
                {"zone_id": "club_west", "name": "West Club", "gate_count": 2, "capacity": 1500},
            ),
            "seats": (
                {"seat_id": "A-1", "zone_id": "gate_north", "accessible": False},
                {"seat_id": "A-2", "zone_id": "gate_north", "accessible": True},
            ),
        }
    )
    event = app.schedule_event(
        {
            "event_id": "event_alpha",
            "venue_id": "venue_alpha",
            "event_name": "Alpha FC vs Harbor City",
            "event_date": "2026-08-12",
        }
    )
    gates = app.plan_ingress_egress(
        "event_alpha",
        {
            "gate_plan": ({"gate": "N1", "population": "general"}, {"gate": "VIP", "population": "premium"}),
            "egress_routes": ({"route": "north_plaza"}, {"route": "south_bus"}),
            "queue_capacity": 18000,
        }
    )
    staffing = app.assign_staffing(
        "event_alpha",
        {
            "roles": ("ushers", "security", "guest_services"),
            "shifts": (
                {"role": "ushers", "planned": 120, "assigned": 118},
                {"role": "security", "planned": 80, "assigned": 80},
            ),
        }
    )
    concessions = app.plan_concessions(
        "event_alpha",
        {"stand_count": 24, "menu_focus": ("beer", "family_combo"), "mobile_ordering": True},
    )
    ticketing = app.coordinate_ticketing(
        "event_alpha",
        {
            "hold_groups": ({"reason": "camera_kill", "seats": 48},),
            "accessible_seat_relocations": ({"from": "101-A", "to": "102-A"},),
        },
    )
    credential = app.issue_credential(
        "event_alpha",
        {"holder_name": "Broadcast Truck A", "credential_type": "broadcast", "zone_access": ("compound", "dock")},
    )
    security = app.update_security_posture(
        "event_alpha",
        {"security_level": "high", "screening_lanes": ("N1", "N2", "VIP"), "magnetometers": 12},
    )
    crowd = app.record_crowd_snapshot(
        "event_alpha",
        {"zone_id": "north_concourse", "density": 0.87, "queue_minutes": 19},
    )
    incident = app.open_incident(
        "event_alpha",
        {"category": "medical", "severity": "high", "location": "Section 109"},
    )
    weather = app.manage_weather_delay(
        "event_alpha",
        {"hazard": "lightning", "state": "delay", "public_message": "Seek shelter"},
    )
    production = app.confirm_production_ready(
        "event_alpha",
        {"run_of_show": ({"segment": "anthem", "duration": 4}, {"segment": "halftime", "duration": 17})},
    )
    sponsor = app.activate_sponsor(
        "event_alpha",
        {"sponsor_name": "NorthBank", "activation_type": "plaza", "window": "pregame"},
    )
    turnover = app.complete_turnover(
        "event_alpha",
        {"phase": "concert_to_match", "crew_status": "complete"},
    )
    accessibility = app.log_accessibility_request(
        "event_alpha",
        {"request_type": "relocation", "location": "Section 102", "resolution": "resolved"},
    )
    lost_found = app.register_lost_and_found(
        "event_alpha",
        {"description": "wallet", "found_location": "guest_services"},
    )
    emergency = app.start_emergency_operation(
        "event_alpha",
        {"playbook": "weather_shelter", "incident_level": "level_2"},
    )
    revenue = app.record_attendance_and_revenue(
        "event_alpha",
        {"attendance": 18250, "paid_attendance": 17910, "gross_revenue": 985000.0, "net_revenue": 812300.0},
    )
    intake = app.document_intake(
        "Weather deck for matchday and accessible gate notes",
        "update the weather delay runbook and prepare accessibility routing preview",
    )
    mutation = app.crud_mutation_plan("update", f"{PBC_KEY}_weather_delay", {"state": "delay"})
    workbench = app.build_workbench(event_id="event_alpha", role="event_commander")
    snapshot = app.get_event_snapshot("event_alpha")
    docs = documentation_presence()
    return {
        "ok": all(
            item["ok"]
            for item in (
                configured,
                defaults,
                venue,
                event,
                gates,
                staffing,
                concessions,
                ticketing,
                credential,
                security,
                crowd,
                incident,
                weather,
                production,
                sponsor,
                turnover,
                accessibility,
                lost_found,
                emergency,
                revenue,
                intake,
                mutation,
                workbench,
                snapshot,
            )
        )
        and docs["ok"],
        "configured": configured,
        "event": event,
        "workbench": workbench,
        "snapshot": snapshot,
        "docs": docs,
        "side_effects": (),
    }
