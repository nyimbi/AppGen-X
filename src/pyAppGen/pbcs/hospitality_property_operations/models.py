"""Owned schema metadata and standalone persistence for hospitality operations."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from .domain_depth import (
    DOMAIN_CONSUMED_EVENTS,
    DOMAIN_EMITTED_EVENTS,
    assess_room_sellable_state,
    assignment_compatibility,
    calculate_overbooking_risk,
    recommend_request_escalation,
)

PBC_KEY = "hospitality_property_operations"
TABLE_PREFIX = f"{PBC_KEY}_"
EVENT_TOPIC = "pbc.hospitality_property_operations.events"


def _field(
    name: str,
    field_type: str,
    *,
    required: bool = True,
    primary_key: bool = False,
    nullable: bool | None = None,
) -> dict:
    return {
        "name": name,
        "type": field_type,
        "required": required,
        "primary_key": primary_key,
        "nullable": nullable if nullable is not None else not required,
    }


def _table(logical_table: str, fields: tuple[dict, ...], relationships: tuple[dict, ...] = ()) -> dict:
    return {
        "logical_table": logical_table,
        "owned_table": f"{TABLE_PREFIX}{logical_table}",
        "fields": fields,
        "relationships": relationships,
    }


AUDIT_FIELDS = (
    _field("version", "integer"),
    _field("created_at", "datetime"),
    _field("updated_at", "datetime"),
)

OWNED_SCHEMA = {
    "schema": PBC_KEY,
    "table_prefix": TABLE_PREFIX,
    "tables": (
        _table(
            "room_inventory",
            (
                _field("room_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("room_number", "string"),
                _field("room_class", "string"),
                _field("bed_configuration", "string"),
                _field("zone", "string"),
                _field("floor", "string"),
                _field("accessibility_features_json", "json"),
                _field("amenity_state_json", "json"),
                _field("operational_status", "string"),
                _field("housekeeping_status", "string"),
                _field("inspection_status", "string"),
                _field("maintenance_status", "string"),
                _field("sellable_status", "string"),
                _field("connected_room_id", "string", required=False),
                _field("current_stay_id", "string", required=False),
                _field("last_cleaned_at", "datetime", required=False),
                _field("last_inspected_at", "datetime", required=False),
                _field("return_to_service_at", "datetime", required=False),
                _field("priority_score", "decimal"),
                _field("notes_json", "json"),
            )
            + AUDIT_FIELDS,
        ),
        _table(
            "reservation",
            (
                _field("reservation_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("reservation_code", "string"),
                _field("guest_name", "string"),
                _field("status", "string"),
                _field("guarantee_status", "string"),
                _field("arrival_date", "date"),
                _field("departure_date", "date"),
                _field("arrival_window", "string"),
                _field("room_class", "string"),
                _field("accessible_required", "boolean"),
                _field("adults", "integer"),
                _field("children", "integer"),
                _field("source_channel", "string"),
                _field("assigned_room_id", "string", required=False),
                _field("overbooking_priority", "decimal"),
                _field("cancellation_deadline", "datetime"),
                _field("special_requests_json", "json"),
            )
            + AUDIT_FIELDS,
            relationships=(
                {"target_table": f"{TABLE_PREFIX}room_inventory", "field": "assigned_room_id"},
            ),
        ),
        _table(
            "guest_stay",
            (
                _field("stay_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("reservation_id", "string"),
                _field("guest_name", "string"),
                _field("lifecycle_state", "string"),
                _field("room_id", "string"),
                _field("check_in_at", "datetime"),
                _field("check_out_due_at", "datetime"),
                _field("actual_check_out_at", "datetime", required=False),
                _field("late_checkout_until", "datetime", required=False),
                _field("service_flags_json", "json"),
                _field("notes_json", "json"),
            )
            + AUDIT_FIELDS,
            relationships=(
                {"target_table": f"{TABLE_PREFIX}reservation", "field": "reservation_id"},
                {"target_table": f"{TABLE_PREFIX}room_inventory", "field": "room_id"},
            ),
        ),
        _table(
            "housekeeping_task",
            (
                _field("task_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("room_id", "string"),
                _field("task_type", "string"),
                _field("status", "string"),
                _field("zone", "string"),
                _field("shift_code", "string"),
                _field("priority", "integer"),
                _field("due_at", "datetime"),
                _field("attendant", "string", required=False),
                _field("inspector", "string", required=False),
                _field("arrival_dependency", "boolean"),
                _field("expedite", "boolean"),
                _field("defect_count", "integer"),
                _field("blocker_reason", "string", required=False),
                _field("evidence_json", "json"),
            )
            + AUDIT_FIELDS,
            relationships=(
                {"target_table": f"{TABLE_PREFIX}room_inventory", "field": "room_id"},
            ),
        ),
        _table(
            "guest_request",
            (
                _field("request_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("stay_id", "string", required=False),
                _field("room_id", "string", required=False),
                _field("category", "string"),
                _field("urgency", "string"),
                _field("status", "string"),
                _field("promised_by", "datetime"),
                _field("fulfillment_team", "string"),
                _field("service_recovery", "boolean"),
                _field("guest_confirmed", "boolean"),
                _field("wait_reason", "string", required=False),
                _field("evidence_json", "json"),
            )
            + AUDIT_FIELDS,
            relationships=(
                {"target_table": f"{TABLE_PREFIX}guest_stay", "field": "stay_id"},
                {"target_table": f"{TABLE_PREFIX}room_inventory", "field": "room_id"},
            ),
        ),
        _table(
            "occupancy_snapshot",
            (
                _field("snapshot_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("stay_date", "date"),
                _field("time_bucket", "string"),
                _field("occupied_rooms", "integer"),
                _field("vacant_clean_rooms", "integer"),
                _field("vacant_dirty_rooms", "integer"),
                _field("blocked_rooms", "integer"),
                _field("arrivals_pending", "integer"),
                _field("departures_pending", "integer"),
                _field("stayovers", "integer"),
                _field("same_day_turns", "integer"),
                _field("oversell_risk", "decimal"),
                _field("notes_json", "json"),
            )
            + AUDIT_FIELDS,
        ),
        _table(
            "rate_plan",
            (
                _field("rate_plan_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("plan_code", "string"),
                _field("room_class", "string"),
                _field("status", "string"),
                _field("closed_to_arrival", "boolean"),
                _field("minimum_stay", "integer"),
                _field("maximum_stay", "integer"),
                _field("sell_threshold", "integer"),
                _field("price_delta", "decimal"),
                _field("package_inclusions_json", "json"),
                _field("effective_from", "date"),
                _field("effective_to", "date"),
            )
            + AUDIT_FIELDS,
        ),
        _table(
            "hospitality_property_operations_policy_rule",
            (
                _field("rule_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("rule_type", "string"),
                _field("status", "string"),
                _field("scope", "string"),
                _field("condition_json", "json"),
                _field("action_json", "json"),
                _field("override_requires_reason", "boolean"),
            )
            + AUDIT_FIELDS,
        ),
        _table(
            "hospitality_property_operations_runtime_parameter",
            (
                _field("parameter_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("parameter_name", "string"),
                _field("parameter_value", "string"),
                _field("min_value", "decimal"),
                _field("max_value", "decimal"),
                _field("status", "string"),
                _field("effective_from", "datetime"),
            )
            + AUDIT_FIELDS,
        ),
        _table(
            "hospitality_property_operations_schema_extension",
            (
                _field("extension_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("table_name", "string"),
                _field("field_name", "string"),
                _field("field_type", "string"),
                _field("status", "string"),
            )
            + AUDIT_FIELDS,
        ),
        _table(
            "hospitality_property_operations_control_assertion",
            (
                _field("assertion_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("assertion_name", "string"),
                _field("subject_ref", "string"),
                _field("status", "string"),
                _field("checked_at", "datetime"),
                _field("evidence_json", "json"),
            )
            + AUDIT_FIELDS,
        ),
        _table(
            "hospitality_property_operations_governed_model",
            (
                _field("model_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("model_name", "string"),
                _field("status", "string"),
                _field("use_case", "string"),
                _field("approval_state", "string"),
                _field("metadata_json", "json"),
            )
            + AUDIT_FIELDS,
        ),
        _table(
            "appgen_outbox_event",
            (
                _field("event_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("event_type", "string"),
                _field("topic", "string"),
                _field("payload_json", "json"),
                _field("status", "string"),
                _field("occurred_at", "datetime"),
                _field("idempotency_key", "string"),
            ),
        ),
        _table(
            "appgen_inbox_event",
            (
                _field("event_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("event_type", "string"),
                _field("source_pbc", "string"),
                _field("payload_json", "json"),
                _field("status", "string"),
                _field("occurred_at", "datetime"),
                _field("idempotency_key", "string"),
            ),
        ),
        _table(
            "appgen_dead_letter_event",
            (
                _field("dead_letter_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("event_type", "string"),
                _field("payload_json", "json"),
                _field("status", "string"),
                _field("occurred_at", "datetime"),
                _field("reason", "string"),
                _field("idempotency_key", "string"),
            ),
        ),
    ),
}
OWNED_TABLES = tuple(table["owned_table"] for table in OWNED_SCHEMA["tables"])
BUSINESS_TABLES = OWNED_TABLES[:-3]
MODEL_NAMES = tuple(
    "".join(part.capitalize() for part in table["owned_table"].split("_"))
    for table in OWNED_SCHEMA["tables"]
)


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _json(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def _loads(value: str | None) -> object:
    return json.loads(value) if value else {}


def _digest(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def standalone_model_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "owned_schema": OWNED_SCHEMA,
        "owned_tables": OWNED_TABLES,
        "models": tuple(
            {
                "class_name": model_name,
                "table": table["owned_table"],
                "fields": tuple(field["name"] for field in table["fields"]),
            }
            for model_name, table in zip(MODEL_NAMES, OWNED_SCHEMA["tables"], strict=True)
        ),
        "sqlite_local_harness": True,
        "event_topic": EVENT_TOPIC,
        "side_effects": (),
    }


def model_contracts() -> tuple[dict, ...]:
    return standalone_model_contract()["models"]


class HospitalityPropertyOperationsStandaloneStore:
    """sqlite-backed local execution harness for the standalone hospitality slice."""

    def __init__(self, database_path: str = ":memory:") -> None:
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = OFF")
        self._create_schema()

    def close(self) -> None:
        self.connection.close()

    def _create_schema(self) -> None:
        statements = (
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_room_inventory (
                room_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                room_number TEXT NOT NULL,
                room_class TEXT NOT NULL,
                bed_configuration TEXT NOT NULL,
                zone TEXT NOT NULL,
                floor TEXT NOT NULL,
                accessibility_features_json TEXT NOT NULL,
                amenity_state_json TEXT NOT NULL,
                operational_status TEXT NOT NULL,
                housekeeping_status TEXT NOT NULL,
                inspection_status TEXT NOT NULL,
                maintenance_status TEXT NOT NULL,
                sellable_status TEXT NOT NULL,
                connected_room_id TEXT,
                current_stay_id TEXT,
                last_cleaned_at TEXT,
                last_inspected_at TEXT,
                return_to_service_at TEXT,
                priority_score REAL NOT NULL,
                notes_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_reservation (
                reservation_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                reservation_code TEXT NOT NULL,
                guest_name TEXT NOT NULL,
                status TEXT NOT NULL,
                guarantee_status TEXT NOT NULL,
                arrival_date TEXT NOT NULL,
                departure_date TEXT NOT NULL,
                arrival_window TEXT NOT NULL,
                room_class TEXT NOT NULL,
                accessible_required INTEGER NOT NULL,
                adults INTEGER NOT NULL,
                children INTEGER NOT NULL,
                source_channel TEXT NOT NULL,
                assigned_room_id TEXT,
                overbooking_priority REAL NOT NULL,
                cancellation_deadline TEXT NOT NULL,
                special_requests_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_guest_stay (
                stay_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                reservation_id TEXT NOT NULL,
                guest_name TEXT NOT NULL,
                lifecycle_state TEXT NOT NULL,
                room_id TEXT NOT NULL,
                check_in_at TEXT NOT NULL,
                check_out_due_at TEXT NOT NULL,
                actual_check_out_at TEXT,
                late_checkout_until TEXT,
                service_flags_json TEXT NOT NULL,
                notes_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_housekeeping_task (
                task_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                room_id TEXT NOT NULL,
                task_type TEXT NOT NULL,
                status TEXT NOT NULL,
                zone TEXT NOT NULL,
                shift_code TEXT NOT NULL,
                priority INTEGER NOT NULL,
                due_at TEXT NOT NULL,
                attendant TEXT,
                inspector TEXT,
                arrival_dependency INTEGER NOT NULL,
                expedite INTEGER NOT NULL,
                defect_count INTEGER NOT NULL,
                blocker_reason TEXT,
                evidence_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_guest_request (
                request_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                stay_id TEXT,
                room_id TEXT,
                category TEXT NOT NULL,
                urgency TEXT NOT NULL,
                status TEXT NOT NULL,
                promised_by TEXT NOT NULL,
                fulfillment_team TEXT NOT NULL,
                service_recovery INTEGER NOT NULL,
                guest_confirmed INTEGER NOT NULL,
                wait_reason TEXT,
                evidence_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_occupancy_snapshot (
                snapshot_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                stay_date TEXT NOT NULL,
                time_bucket TEXT NOT NULL,
                occupied_rooms INTEGER NOT NULL,
                vacant_clean_rooms INTEGER NOT NULL,
                vacant_dirty_rooms INTEGER NOT NULL,
                blocked_rooms INTEGER NOT NULL,
                arrivals_pending INTEGER NOT NULL,
                departures_pending INTEGER NOT NULL,
                stayovers INTEGER NOT NULL,
                same_day_turns INTEGER NOT NULL,
                oversell_risk REAL NOT NULL,
                notes_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_rate_plan (
                rate_plan_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                plan_code TEXT NOT NULL,
                room_class TEXT NOT NULL,
                status TEXT NOT NULL,
                closed_to_arrival INTEGER NOT NULL,
                minimum_stay INTEGER NOT NULL,
                maximum_stay INTEGER NOT NULL,
                sell_threshold INTEGER NOT NULL,
                price_delta REAL NOT NULL,
                package_inclusions_json TEXT NOT NULL,
                effective_from TEXT NOT NULL,
                effective_to TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_hospitality_property_operations_policy_rule (
                rule_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                rule_type TEXT NOT NULL,
                status TEXT NOT NULL,
                scope TEXT NOT NULL,
                condition_json TEXT NOT NULL,
                action_json TEXT NOT NULL,
                override_requires_reason INTEGER NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_hospitality_property_operations_runtime_parameter (
                parameter_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                parameter_name TEXT NOT NULL,
                parameter_value TEXT NOT NULL,
                min_value REAL NOT NULL,
                max_value REAL NOT NULL,
                status TEXT NOT NULL,
                effective_from TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_hospitality_property_operations_schema_extension (
                extension_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                table_name TEXT NOT NULL,
                field_name TEXT NOT NULL,
                field_type TEXT NOT NULL,
                status TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_hospitality_property_operations_control_assertion (
                assertion_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                assertion_name TEXT NOT NULL,
                subject_ref TEXT NOT NULL,
                status TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                evidence_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_hospitality_property_operations_governed_model (
                model_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                model_name TEXT NOT NULL,
                status TEXT NOT NULL,
                use_case TEXT NOT NULL,
                approval_state TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_appgen_outbox_event (
                event_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                event_type TEXT NOT NULL,
                topic TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                status TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                idempotency_key TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_appgen_inbox_event (
                event_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                event_type TEXT NOT NULL,
                source_pbc TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                status TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                idempotency_key TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS hospitality_property_operations_appgen_dead_letter_event (
                dead_letter_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                status TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                reason TEXT NOT NULL,
                idempotency_key TEXT NOT NULL
            )
            """,
        )
        for statement in statements:
            self.connection.execute(statement)
        self.connection.commit()

    def _row(self, query: str, params: tuple = ()) -> dict | None:
        record = self.connection.execute(query, params).fetchone()
        return dict(record) if record else None

    def _rows(self, query: str, params: tuple = ()) -> tuple[dict, ...]:
        return tuple(dict(row) for row in self.connection.execute(query, params).fetchall())

    def _emit(self, tenant: str, event_type: str, payload: dict, *, idem_seed: object) -> dict:
        occurred_at = _now()
        event_id = f"evt_{_digest((event_type, payload, occurred_at))[:16]}"
        idempotency_key = f"{PBC_KEY}:{_digest(idem_seed)[:16]}"
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_appgen_outbox_event
            (event_id, tenant, event_type, topic, payload_json, status, occurred_at, idempotency_key)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_id,
                tenant,
                event_type,
                EVENT_TOPIC,
                _json(payload),
                "pending",
                occurred_at,
                idempotency_key,
            ),
        )
        self.connection.commit()
        return {
            "event_id": event_id,
            "event_type": event_type,
            "topic": EVENT_TOPIC,
            "payload": payload,
            "idempotency_key": idempotency_key,
        }

    def _upsert_room(self, room: dict) -> None:
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_room_inventory
            (room_id, tenant, room_number, room_class, bed_configuration, zone, floor,
             accessibility_features_json, amenity_state_json, operational_status,
             housekeeping_status, inspection_status, maintenance_status, sellable_status,
             connected_room_id, current_stay_id, last_cleaned_at, last_inspected_at,
             return_to_service_at, priority_score, notes_json, version, created_at, updated_at)
            VALUES (:room_id, :tenant, :room_number, :room_class, :bed_configuration, :zone, :floor,
                    :accessibility_features_json, :amenity_state_json, :operational_status,
                    :housekeeping_status, :inspection_status, :maintenance_status, :sellable_status,
                    :connected_room_id, :current_stay_id, :last_cleaned_at, :last_inspected_at,
                    :return_to_service_at, :priority_score, :notes_json, :version, :created_at, :updated_at)
            ON CONFLICT(room_id) DO UPDATE SET
                room_number=excluded.room_number,
                room_class=excluded.room_class,
                bed_configuration=excluded.bed_configuration,
                zone=excluded.zone,
                floor=excluded.floor,
                accessibility_features_json=excluded.accessibility_features_json,
                amenity_state_json=excluded.amenity_state_json,
                operational_status=excluded.operational_status,
                housekeeping_status=excluded.housekeeping_status,
                inspection_status=excluded.inspection_status,
                maintenance_status=excluded.maintenance_status,
                sellable_status=excluded.sellable_status,
                connected_room_id=excluded.connected_room_id,
                current_stay_id=excluded.current_stay_id,
                last_cleaned_at=excluded.last_cleaned_at,
                last_inspected_at=excluded.last_inspected_at,
                return_to_service_at=excluded.return_to_service_at,
                priority_score=excluded.priority_score,
                notes_json=excluded.notes_json,
                version=excluded.version,
                updated_at=excluded.updated_at
            """,
            room,
        )

    def upsert_room_inventory(self, payload: dict) -> dict:
        now = _now()
        room = {
            "room_id": payload.get("room_id") or payload.get("id") or payload.get("room_number"),
            "tenant": payload.get("tenant", "default"),
            "room_number": payload.get("room_number") or payload.get("code") or payload.get("room_id"),
            "room_class": payload.get("room_class", "standard"),
            "bed_configuration": payload.get("bed_configuration", "king"),
            "zone": payload.get("zone", "main"),
            "floor": payload.get("floor", "1"),
            "accessibility_features_json": _json(payload.get("accessibility_features", [])),
            "amenity_state_json": _json(payload.get("amenity_state", {"minibar": "ready"})),
            "operational_status": payload.get("operational_status", "vacant"),
            "housekeeping_status": payload.get("housekeeping_status", "clean"),
            "inspection_status": payload.get("inspection_status", "passed"),
            "maintenance_status": payload.get("maintenance_status", "clear"),
            "sellable_status": payload.get("sellable_status", "sellable"),
            "connected_room_id": payload.get("connected_room_id"),
            "current_stay_id": payload.get("current_stay_id"),
            "last_cleaned_at": payload.get("last_cleaned_at", now),
            "last_inspected_at": payload.get("last_inspected_at", now),
            "return_to_service_at": payload.get("return_to_service_at"),
            "priority_score": float(payload.get("priority_score", 50.0)),
            "notes_json": _json(payload.get("notes", {})),
            "version": int(payload.get("version", 1)),
            "created_at": payload.get("created_at", now),
            "updated_at": now,
        }
        assessment = assess_room_sellable_state(
            {
                "operational_status": room["operational_status"],
                "housekeeping_status": room["housekeeping_status"],
                "inspection_status": room["inspection_status"],
                "maintenance_status": room["maintenance_status"],
                "sellable_status": room["sellable_status"],
            }
        )
        if not room["room_id"] or assessment["ok"] is False:
            return {"ok": False, "reason": "invalid_room_state", "assessment": assessment, "side_effects": ()}
        self._upsert_room(room)
        event = self._emit(
            room["tenant"],
            DOMAIN_EMITTED_EVENTS[0],
            {
                "room_id": room["room_id"],
                "room_number": room["room_number"],
                "sellable_status": room["sellable_status"],
                "assessment": assessment,
            },
            idem_seed=("room", room["room_id"], room["version"]),
        )
        self.connection.commit()
        return {"ok": True, "room": room, "assessment": assessment, "event": event, "side_effects": ()}

    def create_reservation(self, payload: dict) -> dict:
        now = _now()
        reservation = {
            "reservation_id": payload.get("reservation_id") or payload.get("id") or payload.get("reservation_code"),
            "tenant": payload.get("tenant", "default"),
            "reservation_code": payload.get("reservation_code") or payload.get("reservation_id"),
            "guest_name": payload.get("guest_name", "Guest"),
            "status": payload.get("status", "booked"),
            "guarantee_status": payload.get("guarantee_status", "guaranteed"),
            "arrival_date": payload.get("arrival_date", now[:10]),
            "departure_date": payload.get("departure_date", now[:10]),
            "arrival_window": payload.get("arrival_window", "15:00-18:00"),
            "room_class": payload.get("room_class", "standard"),
            "accessible_required": 1 if payload.get("accessible_required") else 0,
            "adults": int(payload.get("adults", 1)),
            "children": int(payload.get("children", 0)),
            "source_channel": payload.get("source_channel", "direct"),
            "assigned_room_id": payload.get("assigned_room_id"),
            "overbooking_priority": float(payload.get("overbooking_priority", 0.5)),
            "cancellation_deadline": payload.get("cancellation_deadline", now),
            "special_requests_json": _json(payload.get("special_requests", [])),
            "version": int(payload.get("version", 1)),
            "created_at": payload.get("created_at", now),
            "updated_at": now,
        }
        if reservation["arrival_date"] >= reservation["departure_date"]:
            return {"ok": False, "reason": "invalid_stay_window", "reservation": reservation, "side_effects": ()}
        assigned_room = None
        compatibility = {"ok": True, "reasons": ()}
        if reservation["assigned_room_id"]:
            assigned_room = self._row(
                """
                SELECT * FROM hospitality_property_operations_room_inventory
                WHERE room_id = ?
                """,
                (reservation["assigned_room_id"],),
            )
            if not assigned_room:
                return {"ok": False, "reason": "assigned_room_missing", "reservation": reservation, "side_effects": ()}
            compatibility = assignment_compatibility(
                {
                    "room_class": reservation["room_class"],
                    "accessible_required": bool(reservation["accessible_required"]),
                },
                {
                    "room_class": assigned_room["room_class"],
                    "accessibility_features": _loads(assigned_room["accessibility_features_json"]),
                    "sellable_status": assigned_room["sellable_status"],
                },
            )
            if compatibility["ok"] is False:
                return {"ok": False, "reason": "room_assignment_rejected", "compatibility": compatibility, "side_effects": ()}
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_reservation
            (reservation_id, tenant, reservation_code, guest_name, status, guarantee_status,
             arrival_date, departure_date, arrival_window, room_class, accessible_required,
             adults, children, source_channel, assigned_room_id, overbooking_priority,
             cancellation_deadline, special_requests_json, version, created_at, updated_at)
            VALUES (:reservation_id, :tenant, :reservation_code, :guest_name, :status, :guarantee_status,
                    :arrival_date, :departure_date, :arrival_window, :room_class, :accessible_required,
                    :adults, :children, :source_channel, :assigned_room_id, :overbooking_priority,
                    :cancellation_deadline, :special_requests_json, :version, :created_at, :updated_at)
            """,
            reservation,
        )
        event = self._emit(
            reservation["tenant"],
            DOMAIN_EMITTED_EVENTS[1],
            {
                "reservation_id": reservation["reservation_id"],
                "guest_name": reservation["guest_name"],
                "assigned_room_id": reservation["assigned_room_id"],
                "guarantee_status": reservation["guarantee_status"],
            },
            idem_seed=("reservation", reservation["reservation_id"]),
        )
        self.connection.commit()
        return {
            "ok": True,
            "reservation": reservation,
            "compatibility": compatibility,
            "assigned_room": assigned_room,
            "event": event,
            "side_effects": (),
        }

    def check_in_guest(self, payload: dict) -> dict:
        reservation_id = payload.get("reservation_id")
        reservation = self._row(
            """
            SELECT * FROM hospitality_property_operations_reservation WHERE reservation_id = ?
            """,
            (reservation_id,),
        )
        if not reservation:
            return {"ok": False, "reason": "reservation_missing", "side_effects": ()}
        room_id = payload.get("room_id") or reservation["assigned_room_id"]
        room = self._row(
            "SELECT * FROM hospitality_property_operations_room_inventory WHERE room_id = ?",
            (room_id,),
        )
        if not room:
            return {"ok": False, "reason": "room_missing", "side_effects": ()}
        room_assessment = assess_room_sellable_state(room)
        if room_assessment["sellable"] is False:
            return {"ok": False, "reason": "room_not_ready", "assessment": room_assessment, "side_effects": ()}
        now = _now()
        stay = {
            "stay_id": payload.get("stay_id") or f"stay_{reservation_id}",
            "tenant": reservation["tenant"],
            "reservation_id": reservation_id,
            "guest_name": reservation["guest_name"],
            "lifecycle_state": payload.get("lifecycle_state", "checked_in"),
            "room_id": room_id,
            "check_in_at": payload.get("check_in_at", now),
            "check_out_due_at": payload.get("check_out_due_at", f"{reservation['departure_date']}T11:00:00+00:00"),
            "actual_check_out_at": None,
            "late_checkout_until": payload.get("late_checkout_until"),
            "service_flags_json": _json(payload.get("service_flags", {"vip": False})),
            "notes_json": _json(payload.get("notes", {})),
            "version": 1,
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_guest_stay
            (stay_id, tenant, reservation_id, guest_name, lifecycle_state, room_id, check_in_at,
             check_out_due_at, actual_check_out_at, late_checkout_until, service_flags_json,
             notes_json, version, created_at, updated_at)
            VALUES (:stay_id, :tenant, :reservation_id, :guest_name, :lifecycle_state, :room_id, :check_in_at,
                    :check_out_due_at, :actual_check_out_at, :late_checkout_until, :service_flags_json,
                    :notes_json, :version, :created_at, :updated_at)
            """,
            stay,
        )
        room["operational_status"] = "occupied"
        room["housekeeping_status"] = "stayover"
        room["sellable_status"] = "withhold"
        room["current_stay_id"] = stay["stay_id"]
        room["version"] = int(room["version"]) + 1
        room["updated_at"] = now
        self._upsert_room(room)
        self.connection.execute(
            """
            UPDATE hospitality_property_operations_reservation
            SET status = ?, updated_at = ?
            WHERE reservation_id = ?
            """,
            ("checked_in", now, reservation_id),
        )
        event = self._emit(
            reservation["tenant"],
            DOMAIN_EMITTED_EVENTS[2],
            {"stay_id": stay["stay_id"], "reservation_id": reservation_id, "room_id": room_id},
            idem_seed=("stay", stay["stay_id"]),
        )
        self.connection.commit()
        return {"ok": True, "stay": stay, "room": room, "event": event, "side_effects": ()}

    def move_guest_stay(self, payload: dict) -> dict:
        stay_id = payload.get("stay_id")
        stay = self._row(
            "SELECT * FROM hospitality_property_operations_guest_stay WHERE stay_id = ?",
            (stay_id,),
        )
        if not stay:
            return {"ok": False, "reason": "stay_missing", "side_effects": ()}
        new_room = self._row(
            "SELECT * FROM hospitality_property_operations_room_inventory WHERE room_id = ?",
            (payload.get("new_room_id"),),
        )
        if not new_room:
            return {"ok": False, "reason": "new_room_missing", "side_effects": ()}
        compatibility = assignment_compatibility(
            {"room_class": payload.get("room_class", new_room["room_class"]), "accessible_required": False},
            {
                "room_class": new_room["room_class"],
                "accessibility_features": _loads(new_room["accessibility_features_json"]),
                "sellable_status": new_room["sellable_status"],
            },
        )
        if compatibility["ok"] is False:
            return {"ok": False, "reason": "move_rejected", "compatibility": compatibility, "side_effects": ()}
        old_room = self._row(
            "SELECT * FROM hospitality_property_operations_room_inventory WHERE room_id = ?",
            (stay["room_id"],),
        )
        now = _now()
        if old_room:
            old_room["operational_status"] = "vacant"
            old_room["housekeeping_status"] = "dirty"
            old_room["sellable_status"] = "withhold"
            old_room["current_stay_id"] = None
            old_room["version"] = int(old_room["version"]) + 1
            old_room["updated_at"] = now
            self._upsert_room(old_room)
        new_room["operational_status"] = "occupied"
        new_room["housekeeping_status"] = "stayover"
        new_room["sellable_status"] = "withhold"
        new_room["current_stay_id"] = stay_id
        new_room["version"] = int(new_room["version"]) + 1
        new_room["updated_at"] = now
        self._upsert_room(new_room)
        self.connection.execute(
            """
            UPDATE hospitality_property_operations_guest_stay
            SET room_id = ?, lifecycle_state = ?, updated_at = ?
            WHERE stay_id = ?
            """,
            (new_room["room_id"], "room_moved", now, stay_id),
        )
        self.connection.commit()
        return {
            "ok": True,
            "stay_id": stay_id,
            "from_room_id": stay["room_id"],
            "to_room_id": new_room["room_id"],
            "compatibility": compatibility,
            "side_effects": (),
        }

    def check_out_guest(self, payload: dict) -> dict:
        stay_id = payload.get("stay_id")
        stay = self._row("SELECT * FROM hospitality_property_operations_guest_stay WHERE stay_id = ?", (stay_id,))
        if not stay:
            return {"ok": False, "reason": "stay_missing", "side_effects": ()}
        now = _now()
        self.connection.execute(
            """
            UPDATE hospitality_property_operations_guest_stay
            SET lifecycle_state = ?, actual_check_out_at = ?, updated_at = ?
            WHERE stay_id = ?
            """,
            ("checked_out", now, now, stay_id),
        )
        room = self._row(
            "SELECT * FROM hospitality_property_operations_room_inventory WHERE room_id = ?",
            (stay["room_id"],),
        )
        if room:
            room["operational_status"] = "vacant"
            room["housekeeping_status"] = "dirty"
            room["inspection_status"] = "pending"
            room["sellable_status"] = "withhold"
            room["current_stay_id"] = None
            room["version"] = int(room["version"]) + 1
            room["updated_at"] = now
            self._upsert_room(room)
        self.connection.commit()
        return {"ok": True, "stay_id": stay_id, "room_id": stay["room_id"], "side_effects": ()}

    def schedule_housekeeping_task(self, payload: dict) -> dict:
        room = self._row(
            "SELECT * FROM hospitality_property_operations_room_inventory WHERE room_id = ?",
            (payload.get("room_id"),),
        )
        if not room:
            return {"ok": False, "reason": "room_missing", "side_effects": ()}
        now = _now()
        task = {
            "task_id": payload.get("task_id") or payload.get("room_id") + "_hk",
            "tenant": payload.get("tenant", room["tenant"]),
            "room_id": payload["room_id"],
            "task_type": payload.get("task_type", "checkout_clean"),
            "status": payload.get("status", "scheduled"),
            "zone": payload.get("zone", room["zone"]),
            "shift_code": payload.get("shift_code", "day"),
            "priority": int(payload.get("priority", 50)),
            "due_at": payload.get("due_at", now),
            "attendant": payload.get("attendant"),
            "inspector": payload.get("inspector"),
            "arrival_dependency": 1 if payload.get("arrival_dependency") else 0,
            "expedite": 1 if payload.get("expedite") else 0,
            "defect_count": int(payload.get("defect_count", 0)),
            "blocker_reason": payload.get("blocker_reason"),
            "evidence_json": _json(payload.get("evidence", {})),
            "version": int(payload.get("version", 1)),
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_housekeeping_task
            (task_id, tenant, room_id, task_type, status, zone, shift_code, priority, due_at,
             attendant, inspector, arrival_dependency, expedite, defect_count, blocker_reason,
             evidence_json, version, created_at, updated_at)
            VALUES (:task_id, :tenant, :room_id, :task_type, :status, :zone, :shift_code, :priority, :due_at,
                    :attendant, :inspector, :arrival_dependency, :expedite, :defect_count, :blocker_reason,
                    :evidence_json, :version, :created_at, :updated_at)
            """,
            task,
        )
        self.connection.commit()
        return {"ok": True, "task": task, "side_effects": ()}

    def complete_housekeeping_task(self, payload: dict) -> dict:
        task = self._row(
            "SELECT * FROM hospitality_property_operations_housekeeping_task WHERE task_id = ?",
            (payload.get("task_id"),),
        )
        if not task:
            return {"ok": False, "reason": "task_missing", "side_effects": ()}
        defects = int(payload.get("defect_count", task["defect_count"]))
        status = "blocked" if defects else payload.get("status", "completed")
        now = _now()
        evidence = payload.get("evidence", {"inspection_result": "passed" if defects == 0 else "failed"})
        self.connection.execute(
            """
            UPDATE hospitality_property_operations_housekeeping_task
            SET status = ?, inspector = ?, defect_count = ?, evidence_json = ?, updated_at = ?
            WHERE task_id = ?
            """,
            (status, payload.get("inspector"), defects, _json(evidence), now, task["task_id"]),
        )
        room = self._row(
            "SELECT * FROM hospitality_property_operations_room_inventory WHERE room_id = ?",
            (task["room_id"],),
        )
        if room:
            room["housekeeping_status"] = "clean" if defects == 0 else "dirty"
            room["inspection_status"] = "passed" if defects == 0 else "failed"
            room["sellable_status"] = (
                "sellable"
                if defects == 0 and room["maintenance_status"] == "clear" and room["operational_status"] == "vacant"
                else "withhold"
            )
            room["last_cleaned_at"] = now
            room["last_inspected_at"] = now
            room["version"] = int(room["version"]) + 1
            room["updated_at"] = now
            self._upsert_room(room)
        event = self._emit(
            task["tenant"],
            DOMAIN_EMITTED_EVENTS[3],
            {"task_id": task["task_id"], "room_id": task["room_id"], "defect_count": defects},
            idem_seed=("housekeeping", task["task_id"], defects),
        )
        self.connection.commit()
        return {"ok": True, "task_id": task["task_id"], "room": room, "event": event, "side_effects": ()}

    def record_guest_request(self, payload: dict) -> dict:
        now = _now()
        request = {
            "request_id": payload.get("request_id") or payload.get("id"),
            "tenant": payload.get("tenant", "default"),
            "stay_id": payload.get("stay_id"),
            "room_id": payload.get("room_id"),
            "category": payload.get("category", "amenity"),
            "urgency": payload.get("urgency", "routine"),
            "status": payload.get("status", "open"),
            "promised_by": payload.get("promised_by", now),
            "fulfillment_team": payload.get("fulfillment_team", "guest_services"),
            "service_recovery": 1 if payload.get("service_recovery") else 0,
            "guest_confirmed": 1 if payload.get("guest_confirmed") else 0,
            "wait_reason": payload.get("wait_reason"),
            "evidence_json": _json(payload.get("evidence", {})),
            "version": int(payload.get("version", 1)),
            "created_at": now,
            "updated_at": now,
        }
        if not request["request_id"]:
            return {"ok": False, "reason": "request_id_required", "side_effects": ()}
        escalation = recommend_request_escalation(
            {
                "urgency": request["urgency"],
                "service_recovery": bool(request["service_recovery"]),
                "category": request["category"],
            }
        )
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_guest_request
            (request_id, tenant, stay_id, room_id, category, urgency, status, promised_by,
             fulfillment_team, service_recovery, guest_confirmed, wait_reason, evidence_json,
             version, created_at, updated_at)
            VALUES (:request_id, :tenant, :stay_id, :room_id, :category, :urgency, :status, :promised_by,
                    :fulfillment_team, :service_recovery, :guest_confirmed, :wait_reason, :evidence_json,
                    :version, :created_at, :updated_at)
            """,
            request,
        )
        self.connection.commit()
        return {"ok": True, "request": request, "escalation": escalation, "side_effects": ()}

    def resolve_guest_request(self, payload: dict) -> dict:
        request = self._row(
            "SELECT * FROM hospitality_property_operations_guest_request WHERE request_id = ?",
            (payload.get("request_id"),),
        )
        if not request:
            return {"ok": False, "reason": "request_missing", "side_effects": ()}
        now = _now()
        guest_confirmed = 1 if payload.get("guest_confirmed", True) else 0
        status = "resolved" if guest_confirmed else "follow_up_required"
        self.connection.execute(
            """
            UPDATE hospitality_property_operations_guest_request
            SET status = ?, guest_confirmed = ?, evidence_json = ?, updated_at = ?
            WHERE request_id = ?
            """,
            (
                status,
                guest_confirmed,
                _json(payload.get("evidence", {"resolution": "completed"})),
                now,
                request["request_id"],
            ),
        )
        event = self._emit(
            request["tenant"],
            DOMAIN_EMITTED_EVENTS[4],
            {"request_id": request["request_id"], "status": status},
            idem_seed=("request", request["request_id"], status),
        )
        self.connection.commit()
        return {"ok": True, "request_id": request["request_id"], "status": status, "event": event, "side_effects": ()}

    def capture_occupancy_snapshot(self, payload: dict) -> dict:
        tenant = payload.get("tenant", "default")
        stay_date = payload.get("stay_date", _now()[:10])
        rooms = self._rows(
            "SELECT * FROM hospitality_property_operations_room_inventory WHERE tenant = ?",
            (tenant,),
        )
        stays = self._rows(
            """
            SELECT * FROM hospitality_property_operations_guest_stay
            WHERE tenant = ? AND lifecycle_state != 'checked_out'
            """,
            (tenant,),
        )
        reservations = self._rows(
            """
            SELECT * FROM hospitality_property_operations_reservation
            WHERE tenant = ? AND arrival_date = ? AND status IN ('booked', 'guaranteed')
            """,
            (tenant, stay_date),
        )
        occupied = sum(1 for room in rooms if room["operational_status"] == "occupied")
        vacant_clean = sum(
            1
            for room in rooms
            if room["operational_status"] == "vacant" and room["sellable_status"] == "sellable"
        )
        vacant_dirty = sum(1 for room in rooms if room["housekeeping_status"] in {"dirty", "turnover"})
        blocked = sum(
            1
            for room in rooms
            if room["sellable_status"] != "sellable" and room["operational_status"] != "occupied"
        )
        arrivals_pending = len(reservations)
        departures_pending = sum(
            1 for stay in stays if stay["check_out_due_at"][:10] == stay_date and not stay["actual_check_out_at"]
        )
        snapshot = {
            "snapshot_id": payload.get("snapshot_id") or f"snapshot_{tenant}_{stay_date}_{payload.get('time_bucket', 'am')}",
            "tenant": tenant,
            "stay_date": stay_date,
            "time_bucket": payload.get("time_bucket", "am"),
            "occupied_rooms": occupied,
            "vacant_clean_rooms": vacant_clean,
            "vacant_dirty_rooms": vacant_dirty,
            "blocked_rooms": blocked,
            "arrivals_pending": arrivals_pending,
            "departures_pending": departures_pending,
            "stayovers": max(len(stays) - departures_pending, 0),
            "same_day_turns": min(arrivals_pending, departures_pending),
            "oversell_risk": calculate_overbooking_risk(
                {
                    "available_rooms": vacant_clean,
                    "arrivals_pending": arrivals_pending,
                    "blocked_rooms": blocked,
                }
            )["risk_score"],
            "notes_json": _json(payload.get("notes", {})),
            "version": int(payload.get("version", 1)),
            "created_at": _now(),
            "updated_at": _now(),
        }
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_occupancy_snapshot
            (snapshot_id, tenant, stay_date, time_bucket, occupied_rooms, vacant_clean_rooms,
             vacant_dirty_rooms, blocked_rooms, arrivals_pending, departures_pending, stayovers,
             same_day_turns, oversell_risk, notes_json, version, created_at, updated_at)
            VALUES (:snapshot_id, :tenant, :stay_date, :time_bucket, :occupied_rooms, :vacant_clean_rooms,
                    :vacant_dirty_rooms, :blocked_rooms, :arrivals_pending, :departures_pending, :stayovers,
                    :same_day_turns, :oversell_risk, :notes_json, :version, :created_at, :updated_at)
            """,
            snapshot,
        )
        event = self._emit(
            tenant,
            DOMAIN_EMITTED_EVENTS[5],
            {
                "snapshot_id": snapshot["snapshot_id"],
                "oversell_risk": snapshot["oversell_risk"],
                "same_day_turns": snapshot["same_day_turns"],
            },
            idem_seed=("snapshot", snapshot["snapshot_id"]),
        )
        self.connection.commit()
        return {"ok": True, "snapshot": snapshot, "event": event, "side_effects": ()}

    def publish_rate_plan(self, payload: dict) -> dict:
        minimum_stay = int(payload.get("minimum_stay", 1))
        maximum_stay = int(payload.get("maximum_stay", 5))
        if minimum_stay > maximum_stay:
            return {"ok": False, "reason": "invalid_length_of_stay_window", "side_effects": ()}
        now = _now()
        rate_plan = {
            "rate_plan_id": payload.get("rate_plan_id") or payload.get("plan_code"),
            "tenant": payload.get("tenant", "default"),
            "plan_code": payload.get("plan_code", "BAR"),
            "room_class": payload.get("room_class", "standard"),
            "status": payload.get("status", "published"),
            "closed_to_arrival": 1 if payload.get("closed_to_arrival") else 0,
            "minimum_stay": minimum_stay,
            "maximum_stay": maximum_stay,
            "sell_threshold": int(payload.get("sell_threshold", 2)),
            "price_delta": float(payload.get("price_delta", 0.0)),
            "package_inclusions_json": _json(payload.get("package_inclusions", [])),
            "effective_from": payload.get("effective_from", now[:10]),
            "effective_to": payload.get("effective_to", now[:10]),
            "version": int(payload.get("version", 1)),
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_rate_plan
            (rate_plan_id, tenant, plan_code, room_class, status, closed_to_arrival, minimum_stay,
             maximum_stay, sell_threshold, price_delta, package_inclusions_json, effective_from,
             effective_to, version, created_at, updated_at)
            VALUES (:rate_plan_id, :tenant, :plan_code, :room_class, :status, :closed_to_arrival, :minimum_stay,
                    :maximum_stay, :sell_threshold, :price_delta, :package_inclusions_json, :effective_from,
                    :effective_to, :version, :created_at, :updated_at)
            """,
            rate_plan,
        )
        event = self._emit(
            rate_plan["tenant"],
            DOMAIN_EMITTED_EVENTS[6],
            {"rate_plan_id": rate_plan["rate_plan_id"], "sell_threshold": rate_plan["sell_threshold"]},
            idem_seed=("rate_plan", rate_plan["rate_plan_id"]),
        )
        self.connection.commit()
        return {"ok": True, "rate_plan": rate_plan, "event": event, "side_effects": ()}

    def set_policy_rule(self, payload: dict) -> dict:
        now = _now()
        record = {
            "rule_id": payload.get("rule_id"),
            "tenant": payload.get("tenant", "default"),
            "rule_type": payload.get("rule_type", "room_sellable_state"),
            "status": payload.get("status", "active"),
            "scope": payload.get("scope", "property"),
            "condition_json": _json(payload.get("condition", {})),
            "action_json": _json(payload.get("action", {})),
            "override_requires_reason": 1 if payload.get("override_requires_reason", True) else 0,
            "version": int(payload.get("version", 1)),
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_hospitality_property_operations_policy_rule
            (rule_id, tenant, rule_type, status, scope, condition_json, action_json,
             override_requires_reason, version, created_at, updated_at)
            VALUES (:rule_id, :tenant, :rule_type, :status, :scope, :condition_json, :action_json,
                    :override_requires_reason, :version, :created_at, :updated_at)
            """,
            record,
        )
        self.connection.commit()
        return {"ok": True, "rule": record, "side_effects": ()}

    def set_runtime_parameter(self, payload: dict) -> dict:
        now = _now()
        value = float(payload.get("parameter_value", payload.get("value", 0)))
        min_value = float(payload.get("min_value", 0))
        max_value = float(payload.get("max_value", value if value > 0 else 1))
        if value < min_value or value > max_value:
            return {"ok": False, "reason": "parameter_out_of_bounds", "side_effects": ()}
        record = {
            "parameter_id": payload.get("parameter_id") or payload.get("parameter_name"),
            "tenant": payload.get("tenant", "default"),
            "parameter_name": payload.get("parameter_name"),
            "parameter_value": str(value),
            "min_value": min_value,
            "max_value": max_value,
            "status": payload.get("status", "active"),
            "effective_from": payload.get("effective_from", now),
            "version": int(payload.get("version", 1)),
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_hospitality_property_operations_runtime_parameter
            (parameter_id, tenant, parameter_name, parameter_value, min_value, max_value, status,
             effective_from, version, created_at, updated_at)
            VALUES (:parameter_id, :tenant, :parameter_name, :parameter_value, :min_value, :max_value, :status,
                    :effective_from, :version, :created_at, :updated_at)
            """,
            record,
        )
        self.connection.commit()
        return {"ok": True, "parameter": record, "side_effects": ()}

    def receive_event(self, event: dict) -> dict:
        idempotency_key = event.get("idempotency_key") or f"{PBC_KEY}:{_digest(event)[:16]}"
        existing = self._row(
            """
            SELECT * FROM hospitality_property_operations_appgen_inbox_event
            WHERE idempotency_key = ?
            """,
            (idempotency_key,),
        )
        if existing:
            return {"ok": True, "duplicate": True, "event": existing, "side_effects": ()}
        occurred_at = event.get("occurred_at", _now())
        tenant = event.get("payload", {}).get("tenant", "default")
        if event.get("event_type") not in DOMAIN_CONSUMED_EVENTS:
            dead_letter_id = f"dlq_{_digest((idempotency_key, occurred_at))[:16]}"
            self.connection.execute(
                """
                INSERT INTO hospitality_property_operations_appgen_dead_letter_event
                (dead_letter_id, tenant, event_type, payload_json, status, occurred_at, reason, idempotency_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    dead_letter_id,
                    tenant,
                    event.get("event_type", "unknown"),
                    _json(event.get("payload", {})),
                    "pending_retry",
                    occurred_at,
                    "unsupported_event_type",
                    idempotency_key,
                ),
            )
            self.connection.commit()
            return {"ok": False, "dead_letter_id": dead_letter_id, "idempotency_key": idempotency_key, "side_effects": ()}
        event_id = event.get("event_id") or f"inbox_{_digest((event, occurred_at))[:16]}"
        self.connection.execute(
            """
            INSERT INTO hospitality_property_operations_appgen_inbox_event
            (event_id, tenant, event_type, source_pbc, payload_json, status, occurred_at, idempotency_key)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_id,
                tenant,
                event["event_type"],
                event.get("source_pbc", "external"),
                _json(event.get("payload", {})),
                "received",
                occurred_at,
                idempotency_key,
            ),
        )
        self.connection.commit()
        return {"ok": True, "duplicate": False, "event_id": event_id, "idempotency_key": idempotency_key, "side_effects": ()}

    def build_workbench(self, tenant: str, shift_code: str = "day") -> dict:
        rooms = self._rows(
            "SELECT * FROM hospitality_property_operations_room_inventory WHERE tenant = ?",
            (tenant,),
        )
        reservations = self._rows(
            "SELECT * FROM hospitality_property_operations_reservation WHERE tenant = ?",
            (tenant,),
        )
        stays = self._rows(
            """
            SELECT * FROM hospitality_property_operations_guest_stay
            WHERE tenant = ? AND lifecycle_state != 'checked_out'
            """,
            (tenant,),
        )
        tasks = self._rows(
            """
            SELECT * FROM hospitality_property_operations_housekeeping_task
            WHERE tenant = ? AND status NOT IN ('completed', 'cancelled')
            """,
            (tenant,),
        )
        requests = self._rows(
            """
            SELECT * FROM hospitality_property_operations_guest_request
            WHERE tenant = ? AND status NOT IN ('resolved', 'cancelled')
            """,
            (tenant,),
        )
        latest_snapshot = self._row(
            """
            SELECT * FROM hospitality_property_operations_occupancy_snapshot
            WHERE tenant = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (tenant,),
        )
        room_ready_gaps = tuple(
            room["room_id"]
            for room in rooms
            if assess_room_sellable_state(room)["sellable"] is False and room["operational_status"] == "vacant"
        )
        urgent_requests = tuple(
            request["request_id"]
            for request in requests
            if request["urgency"] in {"urgent", "vip"} or request["service_recovery"]
        )
        blocked_rooms = tuple(
            room["room_id"] for room in rooms if room["sellable_status"] != "sellable" and room["operational_status"] != "occupied"
        )
        lane_summary = {
            "arrivals": sum(1 for reservation in reservations if reservation["status"] in {"booked", "guaranteed"}),
            "in_house": len(stays),
            "departures": sum(1 for stay in stays if not stay["actual_check_out_at"]),
            "room_ready_gaps": len(room_ready_gaps),
            "exceptions": len(blocked_rooms) + sum(1 for task in tasks if task["status"] == "blocked"),
            "service_recovery": len(urgent_requests),
        }
        return {
            "ok": True,
            "tenant": tenant,
            "shift_code": shift_code,
            "lane_summary": lane_summary,
            "blocked_rooms": blocked_rooms,
            "room_ready_gaps": room_ready_gaps,
            "urgent_requests": urgent_requests,
            "open_housekeeping_tasks": tuple(task["task_id"] for task in tasks),
            "latest_snapshot": latest_snapshot,
            "room_count": len(rooms),
            "reservation_count": len(reservations),
            "stay_count": len(stays),
            "side_effects": (),
        }

    def get_room_detail(self, room_id: str) -> dict:
        room = self._row(
            "SELECT * FROM hospitality_property_operations_room_inventory WHERE room_id = ?",
            (room_id,),
        )
        if not room:
            return {"ok": False, "reason": "room_missing", "side_effects": ()}
        tasks = self._rows(
            """
            SELECT * FROM hospitality_property_operations_housekeeping_task
            WHERE room_id = ?
            ORDER BY updated_at DESC
            """,
            (room_id,),
        )
        requests = self._rows(
            """
            SELECT * FROM hospitality_property_operations_guest_request
            WHERE room_id = ?
            ORDER BY updated_at DESC
            """,
            (room_id,),
        )
        stay = None
        if room.get("current_stay_id"):
            stay = self._row(
                "SELECT * FROM hospitality_property_operations_guest_stay WHERE stay_id = ?",
                (room["current_stay_id"],),
            )
        events = tuple(
            dict(row)
            for row in self.connection.execute(
                """
                SELECT * FROM hospitality_property_operations_appgen_outbox_event
                ORDER BY occurred_at DESC
                """
            ).fetchall()
        )
        related_events = tuple(
            event
            for event in events
            if room_id in event["payload_json"] or (stay and stay["stay_id"] in event["payload_json"])
        )
        return {
            "ok": True,
            "room": room,
            "sellable_assessment": assess_room_sellable_state(room),
            "active_stay": stay,
            "housekeeping_tasks": tasks,
            "guest_requests": requests,
            "recent_events": related_events[:10],
            "side_effects": (),
        }

    def build_shift_handover(self, tenant: str, shift_code: str) -> dict:
        workbench = self.build_workbench(tenant, shift_code)
        arrivals = self._rows(
            """
            SELECT reservation_id, guest_name, assigned_room_id, guarantee_status
            FROM hospitality_property_operations_reservation
            WHERE tenant = ? AND status IN ('booked', 'guaranteed')
            ORDER BY arrival_date, reservation_code
            """,
            (tenant,),
        )
        requests = self._rows(
            """
            SELECT request_id, category, urgency, room_id
            FROM hospitality_property_operations_guest_request
            WHERE tenant = ? AND status NOT IN ('resolved', 'cancelled')
            ORDER BY promised_by
            """,
            (tenant,),
        )
        packet = {
            "arrivals_pending": arrivals[:10],
            "blocked_rooms": workbench["blocked_rooms"],
            "service_recovery": requests[:10],
            "room_ready_gaps": workbench["room_ready_gaps"],
        }
        event = self._emit(
            tenant,
            DOMAIN_EMITTED_EVENTS[7],
            {"shift_code": shift_code, "packet": packet},
            idem_seed=("handover", tenant, shift_code, packet),
        )
        self.connection.commit()
        return {"ok": True, "tenant": tenant, "shift_code": shift_code, "packet": packet, "event": event, "side_effects": ()}


def standalone_store_smoke_test() -> dict:
    store = HospitalityPropertyOperationsStandaloneStore()
    try:
        room = store.upsert_room_inventory(
            {
                "room_id": "rm_101",
                "tenant": "tenant_smoke",
                "room_number": "101",
                "room_class": "deluxe_king",
                "accessibility_features": ["roll_in_shower"],
                "amenity_state": {"minibar": "ready", "crib": "available"},
            }
        )
        reservation = store.create_reservation(
            {
                "reservation_id": "res_101",
                "tenant": "tenant_smoke",
                "reservation_code": "RSV-101",
                "guest_name": "Ada Guest",
                "arrival_date": "2026-05-30",
                "departure_date": "2026-05-31",
                "room_class": "deluxe_king",
                "assigned_room_id": "rm_101",
            }
        )
        stay = store.check_in_guest({"reservation_id": "res_101", "room_id": "rm_101"})
        checkout = store.check_out_guest({"stay_id": stay["stay"]["stay_id"]})
        task = store.schedule_housekeeping_task(
            {
                "task_id": "hk_101",
                "tenant": "tenant_smoke",
                "room_id": "rm_101",
                "arrival_dependency": True,
                "expedite": True,
            }
        )
        task_done = store.complete_housekeeping_task({"task_id": "hk_101", "inspector": "supervisor"})
        request = store.record_guest_request(
            {
                "request_id": "req_101",
                "tenant": "tenant_smoke",
                "room_id": "rm_101",
                "category": "late_checkout",
                "urgency": "urgent",
                "service_recovery": True,
            }
        )
        request_done = store.resolve_guest_request({"request_id": "req_101"})
        snapshot = store.capture_occupancy_snapshot({"tenant": "tenant_smoke", "stay_date": "2026-05-30"})
        rate_plan = store.publish_rate_plan(
            {
                "rate_plan_id": "rate_101",
                "tenant": "tenant_smoke",
                "plan_code": "BAR",
                "room_class": "deluxe_king",
                "effective_from": "2026-05-30",
                "effective_to": "2026-05-31",
            }
        )
        handover = store.build_shift_handover("tenant_smoke", "day")
        workbench = store.build_workbench("tenant_smoke")
        detail = store.get_room_detail("rm_101")
        consumed = store.receive_event(
            {
                "event_id": "evt_policy",
                "event_type": DOMAIN_CONSUMED_EVENTS[0],
                "source_pbc": "policy_management",
                "payload": {"tenant": "tenant_smoke", "rule_id": "arrival"},
            }
        )
        duplicate = store.receive_event(
            {
                "event_id": "evt_policy",
                "event_type": DOMAIN_CONSUMED_EVENTS[0],
                "idempotency_key": consumed["idempotency_key"],
                "payload": {"tenant": "tenant_smoke"},
            }
        )
        dead = store.receive_event({"event_type": "Unexpected", "payload": {"tenant": "tenant_smoke"}})
        return {
            "ok": all(
                item["ok"] is True
                for item in (
                    room,
                    reservation,
                    stay,
                    checkout,
                    task,
                    task_done,
                    request,
                    request_done,
                    snapshot,
                    rate_plan,
                    handover,
                    workbench,
                    detail,
                    consumed,
                )
            )
            and duplicate["duplicate"] is True
            and dead["ok"] is False,
            "room": room,
            "reservation": reservation,
            "stay": stay,
            "task_done": task_done,
            "request_done": request_done,
            "snapshot": snapshot,
            "rate_plan": rate_plan,
            "handover": handover,
            "workbench": workbench,
            "detail": detail,
            "consumed": consumed,
            "duplicate": duplicate,
            "dead": dead,
            "side_effects": (),
        }
    finally:
        store.close()


def migration_artifact_path() -> str:
    return str(Path("src") / "pyAppGen" / "pbcs" / PBC_KEY / "migrations" / "001_initial.sql")
