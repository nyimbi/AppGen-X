"""Package-local standalone store and model contracts for smart city mobility."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib

from .domain_depth import (
    BUSINESS_TABLES,
    DOMAIN_CONSUMED_EVENTS,
    DOMAIN_QUERY_SPECS,
    DOMAIN_RECORD_SPECS,
    DOMAIN_OWNED_TABLES,
    PBC_KEY,
    record_spec,
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def standalone_model_contract() -> dict:
    return {
        "format": "appgen.smart-city-mobility-operations-standalone-model.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "table_keys": DOMAIN_OWNED_TABLES,
        "business_tables": BUSINESS_TABLES,
        "record_types": tuple(spec["record_type"] for spec in DOMAIN_RECORD_SPECS),
        "query_types": tuple(spec["query"] for spec in DOMAIN_QUERY_SPECS),
        "database_backends": ("postgresql", "mysql", "mariadb"),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def model_contracts():
    return tuple(
        {
            "class_name": "".join(part.capitalize() for part in spec["record_type"].split("_")),
            "table": spec["table"],
            "fields": spec["required_fields"] + ("status", "created_at", "updated_at", "payload"),
        }
        for spec in DOMAIN_RECORD_SPECS
    )


class SmartCityMobilityOperationsStandaloneStore:
    """In-memory owned-table store for the standalone one-PBC mobility slice."""

    def __init__(self) -> None:
        self.records = {spec["record_type"]: {} for spec in DOMAIN_RECORD_SPECS}
        self.outbox = []
        self.inbox = []
        self.dead_letter = []
        self.idempotency_keys = set()

    def close(self) -> None:
        return None

    def _emit(self, event_type: str, payload: dict) -> dict:
        event = {
            "event_type": event_type,
            "topic": f"pbc.{PBC_KEY}.events",
            "payload": deepcopy(payload),
            "idempotency_key": _digest((event_type, payload)),
            "event_contract": "AppGen-X",
        }
        self.outbox.append(event)
        return event

    def _validate_payload(self, spec: dict, payload: dict) -> tuple[str, ...]:
        missing = tuple(field for field in spec["required_fields"] if payload.get(field) in (None, "", ()))
        if missing:
            return missing
        broken_refs = []
        for field, target_type in spec.get("references", ()):
            value = payload.get(field)
            if value not in self.records[target_type]:
                broken_refs.append(field)
        if broken_refs:
            return tuple(broken_refs)
        if spec["record_type"] == "signal_plan":
            accessibility = payload.get("accessibility_profile") or {}
            if not accessibility.get("walk_interval_seconds") or not accessibility.get(
                "flashing_clearance_seconds"
            ):
                return ("accessibility_profile",)
        if spec["record_type"] == "transit_priority_rule_pack":
            if not payload.get("blackout_conditions") or not payload.get("eligible_routes"):
                return ("transit_priority_thresholds",)
        if spec["record_type"] == "emergency_preemption_policy":
            priority_order = tuple(payload.get("priority_order") or ())
            if not priority_order or priority_order[0] != "emergency":
                return ("priority_order",)
        if spec["record_type"] == "accessibility_disruption":
            if not payload.get("replacement_guidance") and not payload.get("exemption_reason"):
                return ("replacement_guidance",)
        if spec["record_type"] == "multimodal_trip" and len(tuple(payload.get("modes") or ())) < 2:
            return ("modes",)
        if spec["record_type"] == "mobility_sensor_feed":
            quality = float(payload.get("quality_score", 0.0))
            if quality < 0:
                return ("quality_score",)
        return ()

    def record_domain_item(self, record_type: str, payload: dict | None = None) -> dict:
        spec = record_spec(record_type)
        if spec is None:
            return {
                "ok": False,
                "reason": "unknown_record_type",
                "record_type": record_type,
                "side_effects": (),
            }
        payload = deepcopy(dict(payload or {}))
        missing = self._validate_payload(spec, payload)
        if missing:
            return {
                "ok": False,
                "reason": "validation_failed",
                "record_type": record_type,
                "missing_fields": missing,
                "side_effects": (),
            }
        record_id = payload.get(spec["id_field"]) or payload.get("id") or _digest(payload)[:12]
        timestamp = _now()
        quality_state = "healthy"
        emitted_event = spec["event"]
        if record_type == "mobility_sensor_feed" and float(payload.get("quality_score", 0.0)) < 0.8:
            quality_state = "quarantined"
            payload.setdefault("quarantine_reason", "quality_score_below_floor")
            emitted_event = "SensorFeedQuarantined"
        record = {
            spec["id_field"]: record_id,
            "record_type": record_type,
            "table": spec["table"],
            "tenant": payload.get("tenant", "default"),
            "status": payload.get("status", "active"),
            "quality_state": quality_state,
            "references": {field: payload.get(field) for field, _ in spec.get("references", ())},
            "payload": payload,
            "created_at": timestamp,
            "updated_at": timestamp,
        }
        self.records[record_type][record_id] = record
        event = self._emit(emitted_event, {"record_type": record_type, "record_id": record_id, **record["references"]})
        return {
            "ok": True,
            "record_type": record_type,
            "record": deepcopy(record),
            "table": spec["table"],
            "event": deepcopy(event),
            "side_effects": (),
        }

    def receive_event(self, event: dict | None = None) -> dict:
        event = deepcopy(dict(event or {}))
        idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
        if idem in self.idempotency_keys:
            return {"ok": True, "duplicate": True, "idempotency_key": idem, "side_effects": ()}
        self.idempotency_keys.add(idem)
        if event.get("event_type") not in DOMAIN_CONSUMED_EVENTS:
            dead_letter = {
                "event": event,
                "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
                "retry_policy": {"max_attempts": 5},
            }
            self.dead_letter.append(dead_letter)
            return {
                "ok": False,
                "duplicate": False,
                "dead_letter_table": dead_letter["dead_letter_table"],
                "retry_policy": dead_letter["retry_policy"],
                "side_effects": (),
            }
        inbox_event = {
            "event": event,
            "idempotency_key": idem,
            "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        }
        self.inbox.append(inbox_event)
        return {"ok": True, "duplicate": False, "event": inbox_event, "side_effects": ()}

    def build_corridor_snapshot(self, corridor_id: str) -> dict:
        corridor = self.records["corridor_registry"].get(corridor_id)
        related = {
            spec["record_type"]: tuple(
                record
                for record in self.records[spec["record_type"]].values()
                if record["references"].get("corridor_id") == corridor_id
            )
            for spec in DOMAIN_RECORD_SPECS
            if any(field == "corridor_id" for field, _ in spec.get("references", ()))
        }
        incident_count = len(related.get("traffic_incident", ()))
        closure_count = len(related.get("planned_disruption", ()))
        parking_assets = related.get("parking_asset", ())
        return {
            "ok": corridor is not None,
            "corridor": deepcopy(corridor),
            "related": deepcopy(related),
            "corridor_id": corridor_id,
            "incident_count": incident_count,
            "closure_count": closure_count,
            "parking_asset_count": len(parking_assets),
            "notification_count": len(related.get("public_notification", ())),
            "side_effects": (),
        }

    def build_intersection_detail(self, intersection_id: str) -> dict:
        intersection = self.records["intersection_registry"].get(intersection_id)
        signal_plans = tuple(
            record
            for record in self.records["signal_plan"].values()
            if record["references"].get("intersection_id") == intersection_id
        )
        corridor_id = intersection["references"].get("corridor_id") if intersection else None
        sensor_feeds = tuple(
            record
            for record in self.records["mobility_sensor_feed"].values()
            if record["references"].get("corridor_id") == corridor_id
        )
        incidents = tuple(
            record
            for record in self.records["traffic_incident"].values()
            if record["references"].get("corridor_id") == corridor_id
        )
        degraded = not signal_plans or any(feed["quality_state"] == "quarantined" for feed in sensor_feeds)
        return {
            "ok": intersection is not None,
            "intersection": deepcopy(intersection),
            "signal_plans": deepcopy(signal_plans),
            "sensor_feeds": deepcopy(sensor_feeds),
            "incidents": deepcopy(incidents),
            "degraded": degraded,
            "fallback_message": "detector data degraded" if degraded else "",
            "side_effects": (),
        }

    def build_readiness_scorecard(self, tenant: str = "default") -> dict:
        dimensions = (
            ("corridors", bool(self.records["corridor_registry"])),
            ("intersections", bool(self.records["intersection_registry"])),
            ("signal_plans", bool(self.records["signal_plan"])),
            ("feed_quality", any(self.records["mobility_sensor_feed"].values())),
            ("accessibility", bool(self.records["accessibility_disruption"])),
            ("notifications", bool(self.records["public_notification"])),
            ("reliability", bool(self.records["service_reliability_snapshot"])),
            ("governed_previews", bool(self.records["governed_instruction_preview"])),
        )
        failed = tuple(name for name, ok in dimensions if not ok)
        return {
            "ok": not failed,
            "tenant": tenant,
            "dimensions": tuple({"key": name, "ok": ok} for name, ok in dimensions),
            "failed_dimensions": failed,
            "green": not failed,
            "side_effects": (),
        }

    def build_workbench(self, tenant: str = "default") -> dict:
        corridors = tuple(self.records["corridor_registry"].values())
        corridor_cards = []
        for corridor in corridors:
            corridor_id = corridor["payload"]["corridor_id"]
            snapshot = self.build_corridor_snapshot(corridor_id)
            corridor_cards.append(
                {
                    "corridor_id": corridor_id,
                    "name": corridor["payload"]["name"],
                    "functional_class": corridor["payload"]["functional_class"],
                    "operating_objective": corridor["payload"]["operating_objective"],
                    "incident_count": snapshot["incident_count"],
                    "closure_count": snapshot["closure_count"],
                    "parking_asset_count": snapshot["parking_asset_count"],
                    "notification_count": snapshot["notification_count"],
                }
            )
        readiness = self.build_readiness_scorecard(tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "corridor_cards": tuple(corridor_cards),
            "quarantined_feed_count": sum(
                1
                for feed in self.records["mobility_sensor_feed"].values()
                if feed["quality_state"] == "quarantined"
            ),
            "incident_count": len(self.records["traffic_incident"]),
            "planned_disruption_count": len(self.records["planned_disruption"]),
            "notification_count": len(self.records["public_notification"]),
            "readiness": readiness,
            "views": (
                "corridor_command",
                "intersection_detail",
                "signal_timing_review",
                "public_notification_preview",
            ),
            "side_effects": (),
        }

    def preview_governed_instruction(self, document: str, instruction: str, tenant: str = "default") -> dict:
        combined = f"{document} {instruction}".lower()
        matched_specs = tuple(
            spec
            for spec in DOMAIN_RECORD_SPECS
            if any(keyword in combined for keyword in spec["keywords"])
        )
        candidate_tables = tuple(dict.fromkeys(spec["table"] for spec in matched_specs)) or (
            f"{PBC_KEY}_governed_instruction_preview",
        )
        route_candidates = tuple(f"POST {spec['path']}" for spec in matched_specs) or (
            "POST /app/smart-city-mobility-operations/governed-previews",
        )
        preview = {
            "preview_id": _digest((tenant, document, instruction))[:12],
            "tenant": tenant,
            "document": document,
            "instruction": instruction,
            "candidate_tables": candidate_tables,
            "route_candidates": route_candidates,
            "control_checks": (
                "owned_table_boundary_check",
                "human_confirmation_required",
                "appgen_x_event_only",
            ),
            "requires_human_confirmation": True,
        }
        stored = self.record_domain_item("governed_instruction_preview", preview)
        return {
            "ok": stored["ok"],
            "preview": stored.get("record"),
            "candidate_tables": candidate_tables,
            "route_candidates": route_candidates,
            "requires_human_confirmation": True,
            "side_effects": (),
        }


def standalone_store_smoke_test() -> dict:
    store = SmartCityMobilityOperationsStandaloneStore()
    try:
        corridor = store.record_domain_item(
            "corridor_registry",
            {
                "corridor_id": "c_smoke",
                "tenant": "tenant_smoke",
                "name": "Central Corridor",
                "functional_class": "arterial",
                "operating_objective": "bus reliability",
            },
        )
        intersection = store.record_domain_item(
            "intersection_registry",
            {
                "intersection_id": "i_smoke",
                "tenant": "tenant_smoke",
                "corridor_id": "c_smoke",
                "name": "5th & Main",
                "control_mode": "adaptive",
                "movements": ("nb_through", "sb_through", "ped_crossing"),
            },
        )
        signal = store.record_domain_item(
            "signal_plan",
            {
                "signal_plan_id": "sp_smoke",
                "tenant": "tenant_smoke",
                "corridor_id": "c_smoke",
                "intersection_id": "i_smoke",
                "plan_name": "AM Peak",
                "cycle_length_seconds": 90,
                "phase_splits": {"p2": 35, "p4": 20},
                "accessibility_profile": {
                    "walk_interval_seconds": 7,
                    "flashing_clearance_seconds": 18,
                },
            },
        )
        preview = store.preview_governed_instruction(
            "closure permit for Main St",
            "prepare a governed incident and notification preview",
            tenant="tenant_smoke",
        )
        workbench = store.build_workbench("tenant_smoke")
        return {
            "ok": corridor["ok"] and intersection["ok"] and signal["ok"] and preview["ok"] and workbench["ok"],
            "corridor": corridor,
            "intersection": intersection,
            "signal": signal,
            "preview": preview,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        store.close()
