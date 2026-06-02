"""Standalone executable application for the public_safety_dispatch PBC."""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
import hashlib
import json
import re
from typing import Any

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
    domain_depth_contract,
    domain_depth_smoke_test,
)
from .manifest import PBC_MANIFEST

PBC_KEY = "public_safety_dispatch"
APPGEN_X_TOPIC = f"pbc.{PBC_KEY}.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
LEGACY_EMITTED_EVENTS = tuple(PBC_MANIFEST["emits"])
LEGACY_CONSUMED_EVENTS = tuple(PBC_MANIFEST["consumes"])
EMITTED_EVENTS = tuple(
    dict.fromkeys(
        (
            "CallIntakeAccepted",
            "IncidentClassified",
            "DispatchRecommendationPrepared",
            "UnitsDispatched",
            "MutualAidRequested",
            "ResponderSafetyAlertRaised",
            "CadLifecycleUpdated",
            "CaseDispositionRecorded",
            "AiPreviewPrepared",
        )
        + LEGACY_EMITTED_EVENTS
    )
)
CONSUMED_EVENTS = LEGACY_CONSUMED_EVENTS
BUSINESS_TABLES = tuple(DOMAIN_OWNED_TABLES[:-3])
EVENT_TABLES = tuple(DOMAIN_OWNED_TABLES[-3:])
RUNTIME_TABLES = BUSINESS_TABLES + EVENT_TABLES
STANDARD_FEATURES = tuple(PBC_MANIFEST["standard_features"])
ADVANCED_CAPABILITIES = tuple(PBC_MANIFEST["advanced_capabilities"])
PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
    f"{PBC_KEY}.operate",
    f"{PBC_KEY}.dispatch",
    f"{PBC_KEY}.audit",
)
PUBLIC_ROUTES = (
    {"method": "POST", "path": "/emergency-calls", "operation": "create_emergency_call", "permission": f"{PBC_KEY}.create"},
    {"method": "POST", "path": "/response-units", "operation": "record_response_unit", "permission": f"{PBC_KEY}.update"},
    {"method": "POST", "path": "/incidents", "operation": "review_incident", "permission": f"{PBC_KEY}.update"},
    {"method": "POST", "path": "/dispatch-assignments", "operation": "approve_dispatch_assignment", "permission": f"{PBC_KEY}.dispatch"},
    {"method": "POST", "path": "/mutual-aids", "operation": "simulate_mutual_aid", "permission": f"{PBC_KEY}.dispatch"},
    {"method": "POST", "path": "/response-milestones", "operation": "create_response_milestone", "permission": f"{PBC_KEY}.update"},
    {"method": "POST", "path": "/case-dispositions", "operation": "record_case_disposition", "permission": f"{PBC_KEY}.approve"},
    {"method": "POST", "path": "/assistant/document-plan", "operation": "document_instruction_plan", "permission": f"{PBC_KEY}.read"},
    {"method": "POST", "path": "/assistant/crud-plan", "operation": "datastore_crud_plan", "permission": f"{PBC_KEY}.read"},
    {"method": "GET", "path": "/public-safety-dispatch-workbench", "operation": "query_workbench", "permission": f"{PBC_KEY}.audit"},
)
UI_FRAGMENTS = (
    "PublicSafetyDispatchWorkbench",
    "PublicSafetyDispatchDetail",
    "PublicSafetyDispatchAssistantPanel",
    "PublicSafetyDispatchMapPanel",
    "PublicSafetyDispatchRadioConsole",
)
FORMS = (
    {
        "form_id": "call_intake",
        "title": "Emergency Call Intake",
        "action": "create_emergency_call",
        "permission": f"{PBC_KEY}.create",
        "fields": (
            "tenant",
            "call_source",
            "caller_name",
            "callback_number",
            "chief_complaint",
            "narrative",
            "address",
            "jurisdiction",
            "beat",
            "agency",
            "conference_parties",
            "attachments",
        ),
    },
    {
        "form_id": "response_unit_status",
        "title": "Response Unit Status",
        "action": "record_response_unit",
        "permission": f"{PBC_KEY}.update",
        "fields": (
            "tenant",
            "unit_code",
            "discipline",
            "status",
            "agency",
            "jurisdiction",
            "beat",
            "capabilities",
            "radio_profile",
            "eta_minutes",
        ),
    },
    {
        "form_id": "dispatch_assignment",
        "title": "Dispatch Assignment",
        "action": "approve_dispatch_assignment",
        "permission": f"{PBC_KEY}.dispatch",
        "fields": (
            "tenant",
            "incident_id",
            "required_units",
            "required_capabilities",
            "allow_mutual_aid",
            "requested_agency",
            "requested_channel_family",
        ),
    },
    {
        "form_id": "scene_milestone",
        "title": "CAD Scene Milestone",
        "action": "create_response_milestone",
        "permission": f"{PBC_KEY}.update",
        "fields": (
            "tenant",
            "incident_id",
            "milestone_type",
            "status",
            "scene_notes",
            "radio_channel",
            "attachments",
            "safety_alerts",
        ),
    },
    {
        "form_id": "case_disposition",
        "title": "Case Disposition",
        "action": "record_case_disposition",
        "permission": f"{PBC_KEY}.approve",
        "fields": (
            "tenant",
            "incident_id",
            "discipline",
            "disposition_code",
            "outcome_summary",
            "after_action_review",
            "evidence_attachments",
        ),
    },
)
WIZARDS = (
    {
        "wizard_id": "dispatch_call_to_closeout",
        "title": "Call To Closeout",
        "permission": f"{PBC_KEY}.dispatch",
        "steps": (
            "create_emergency_call",
            "review_incident",
            "approve_dispatch_assignment",
            "create_response_milestone",
            "record_case_disposition",
        ),
        "outcome": "closed_incident_with_audit_trail",
    },
    {
        "wizard_id": "mutual_aid_activation",
        "title": "Mutual Aid Activation",
        "permission": f"{PBC_KEY}.dispatch",
        "steps": (
            "create_emergency_call",
            "approve_dispatch_assignment",
            "simulate_mutual_aid",
            "create_response_milestone",
        ),
        "outcome": "partner_agency_routed_with_sla_tracking",
    },
    {
        "wizard_id": "ai_dispatch_assistant_review",
        "title": "AI Assistant Review",
        "permission": f"{PBC_KEY}.audit",
        "steps": (
            "document_instruction_plan",
            "datastore_crud_plan",
            "review_incident",
            "record_case_disposition",
        ),
        "outcome": "governed_mutation_preview",
    },
)
CONTROLS = (
    {
        "control_id": "priority_escalation_panel",
        "label": "Priority Escalation",
        "type": "panel",
        "action": "review_incident",
        "permission": f"{PBC_KEY}.dispatch",
    },
    {
        "control_id": "beat_jurisdiction_filter",
        "label": "Beat/Jurisdiction Filter",
        "type": "filter",
        "action": "query_workbench",
        "permission": f"{PBC_KEY}.read",
    },
    {
        "control_id": "radio_channel_selector",
        "label": "Radio Channel Selector",
        "type": "selector",
        "action": "approve_dispatch_assignment",
        "permission": f"{PBC_KEY}.dispatch",
    },
    {
        "control_id": "dead_letter_replay",
        "label": "Dead Letter Replay",
        "type": "action",
        "action": "receive_event",
        "permission": f"{PBC_KEY}.audit",
    },
    {
        "control_id": "assistant_preview_console",
        "label": "Assistant Preview",
        "type": "preview",
        "action": "document_instruction_plan",
        "permission": f"{PBC_KEY}.audit",
    },
)
QUEUES = (
    "waiting_intake",
    "active_incidents",
    "units_awaiting_assignment",
    "mutual_aid_pending_ack",
    "priority_escalations",
    "safety_alerts",
    "sla_watch",
    "dead_letter",
)
WORKFLOWS = (
    "public_safety_dispatch_create_emergency_call_workflow",
    "public_safety_dispatch_record_response_unit_workflow",
    "public_safety_dispatch_dispatch_to_closeout_workflow",
    "public_safety_dispatch_mutual_aid_escalation_workflow",
)
INCIDENT_CLASSIFIERS = (
    {
        "keywords": ("cardiac", "not breathing", "overdose", "unresponsive", "seizure"),
        "discipline": "ems",
        "incident_type": "medical_emergency",
        "priority": 1,
        "determinant_code": "ECHO-MED-1",
        "required_capabilities": ("als", "cpr", "medical"),
        "channel_family": "ems",
    },
    {
        "keywords": ("fire", "smoke", "alarm", "hazmat", "structure fire"),
        "discipline": "fire",
        "incident_type": "fire_response",
        "priority": 1,
        "determinant_code": "DELTA-FIRE-2",
        "required_capabilities": ("engine", "ladder", "fire"),
        "channel_family": "fire",
    },
    {
        "keywords": ("shooting", "assault", "weapon", "violent", "burglary", "robbery"),
        "discipline": "law",
        "incident_type": "law_enforcement_response",
        "priority": 1,
        "determinant_code": "DELTA-LAW-7",
        "required_capabilities": ("law", "de_escalation", "scene_security"),
        "channel_family": "law",
    },
    {
        "keywords": ("crash", "collision", "accident", "vehicle", "rollover"),
        "discipline": "multi",
        "incident_type": "traffic_collision",
        "priority": 2,
        "determinant_code": "CHARLIE-TRF-4",
        "required_capabilities": ("traffic_control", "medical", "extrication"),
        "channel_family": "interop",
    },
)
DISCIPLINE_DISPOSITIONS = {
    "law": ("arrest", "citation", "gone_on_arrival", "unable_to_locate", "cancelled_en_route"),
    "fire": ("fire_contained", "false_alarm", "cancelled_en_route", "hazmat_stabilized"),
    "ems": ("transport", "refusal", "treated_and_released", "unable_to_locate", "cancelled_en_route"),
    "multi": ("resolved_on_scene", "transport", "fire_contained", "arrest"),
}
CHANNEL_FAMILIES = {
    "law": {"dispatch": "LAW-DISP-1", "tactical": "LAW-TAC-2"},
    "fire": {"dispatch": "FIRE-DISP-1", "tactical": "FIRE-TAC-3"},
    "ems": {"dispatch": "EMS-DISP-1", "tactical": "EMS-TAC-2"},
    "interop": {"dispatch": "INT-DISP-1", "tactical": "INT-TAC-1"},
}
TABLE_FIELDS = {
    f"{PBC_KEY}_emergency_call": (
        "id",
        "tenant",
        "call_source",
        "caller_name",
        "callback_number",
        "chief_complaint",
        "location_text",
        "location_confidence",
        "status",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_response_unit": (
        "id",
        "tenant",
        "unit_code",
        "discipline",
        "status",
        "agency",
        "jurisdiction",
        "beat",
        "capabilities",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_incident": (
        "id",
        "tenant",
        "incident_number",
        "discipline",
        "priority",
        "cad_status",
        "jurisdiction",
        "beat",
        "response_sla_due_at",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_dispatch_assignment": (
        "id",
        "tenant",
        "incident_id",
        "assignment_code",
        "status",
        "selected_units",
        "radio_channel",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_mutual_aid": (
        "id",
        "tenant",
        "incident_id",
        "partner_agencies",
        "status",
        "requested_capabilities",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_response_milestone": (
        "id",
        "tenant",
        "incident_id",
        "milestone_type",
        "status",
        "radio_channel",
        "scene_notes",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_case_disposition": (
        "id",
        "tenant",
        "incident_id",
        "discipline",
        "disposition_code",
        "status",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_public_safety_dispatch_policy_rule": (
        "id",
        "tenant",
        "rule_id",
        "scope",
        "status",
        "compiled_hash",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_public_safety_dispatch_runtime_parameter": (
        "id",
        "tenant",
        "parameter_name",
        "value",
        "bounded",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_public_safety_dispatch_schema_extension": (
        "id",
        "tenant",
        "table_name",
        "field_names",
        "status",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_public_safety_dispatch_control_assertion": (
        "id",
        "tenant",
        "assertion_name",
        "status",
        "evidence_hash",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_public_safety_dispatch_governed_model": (
        "id",
        "tenant",
        "model_name",
        "model_version",
        "governance_status",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_appgen_outbox_event": (
        "id",
        "tenant",
        "event_type",
        "topic",
        "status",
        "idempotency_key",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_appgen_inbox_event": (
        "id",
        "tenant",
        "event_type",
        "status",
        "idempotency_key",
        "payload",
        "created_at",
        "updated_at",
    ),
    f"{PBC_KEY}_appgen_dead_letter_event": (
        "id",
        "tenant",
        "event_type",
        "status",
        "idempotency_key",
        "payload",
        "created_at",
        "updated_at",
    ),
}


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()



def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()



def _normalize_phone(number: str | None) -> str:
    digits = "".join(ch for ch in str(number or "") if ch.isdigit())
    return digits[-10:] if digits else ""



def _normalize_text(value: str | None) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())



def _copy_record(record: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(record)



def _sla_minutes(priority: int) -> int:
    return {1: 4, 2: 8, 3: 12, 4: 18, 5: 30}.get(priority, 18)



def default_configuration() -> dict[str, Any]:
    return {
        "database_backend": "postgresql",
        "event_topic": APPGEN_X_TOPIC,
        "retry_limit": 5,
        "default_policy": "standard_dispatch",
        "workbench_limit": 25,
        "confirmation_required_for_agent_writes": True,
        "stream_engine_picker_visible": False,
    }



def default_parameter_values() -> dict[str, Any]:
    return {
        "quality_score_floor": 0.8,
        "materiality_threshold": 0.6,
        "approval_sla_hours": 2,
        "risk_threshold": 0.7,
        "forecast_horizon_days": 7,
        "workbench_limit": 25,
    }



def default_rules() -> tuple[dict[str, Any], ...]:
    return (
        {
            "rule_id": "emergency_call_policy",
            "scope": "call_intake",
            "status": "active",
            "requires_callback_validation": True,
            "requires_location_confirmation_below": 0.65,
        },
        {
            "rule_id": "dispatch_assignment_policy",
            "scope": "dispatch",
            "status": "active",
            "prefer_same_jurisdiction": True,
            "mutual_aid_when_units_below": 1,
        },
        {
            "rule_id": "response_milestone_policy",
            "scope": "cad_lifecycle",
            "status": "active",
            "allowed_statuses": (
                "call_received",
                "triaged",
                "pending_dispatch",
                "dispatched",
                "enroute",
                "on_scene",
                "transport",
                "clear",
                "closed",
            ),
        },
    )



def default_units(tenant: str = "tenant_alpha") -> tuple[dict[str, Any], ...]:
    return (
        {
            "tenant": tenant,
            "unit_code": "LAW-12",
            "discipline": "law",
            "status": "available",
            "agency": "metro_police",
            "jurisdiction": "central_city",
            "beat": "beat-1",
            "capabilities": ("law", "de_escalation", "scene_security"),
            "radio_profile": {"preferred_family": "law", "portable": "LAW-TAC-2"},
            "eta_minutes": 3,
        },
        {
            "tenant": tenant,
            "unit_code": "ENG-7",
            "discipline": "fire",
            "status": "available",
            "agency": "metro_fire",
            "jurisdiction": "central_city",
            "beat": "beat-1",
            "capabilities": ("engine", "fire", "extrication"),
            "radio_profile": {"preferred_family": "fire", "portable": "FIRE-TAC-3"},
            "eta_minutes": 4,
        },
        {
            "tenant": tenant,
            "unit_code": "MED-4",
            "discipline": "ems",
            "status": "available",
            "agency": "metro_ems",
            "jurisdiction": "central_city",
            "beat": "beat-1",
            "capabilities": ("medical", "als", "cpr"),
            "radio_profile": {"preferred_family": "ems", "portable": "EMS-TAC-2"},
            "eta_minutes": 5,
        },
        {
            "tenant": tenant,
            "unit_code": "COUNTY-RESCUE-2",
            "discipline": "fire",
            "status": "available",
            "agency": "county_fire",
            "jurisdiction": "north_county",
            "beat": "beat-8",
            "capabilities": ("ladder", "fire", "hazmat"),
            "radio_profile": {"preferred_family": "fire", "portable": "FIRE-TAC-5"},
            "eta_minutes": 11,
        },
    )



def default_governed_models() -> tuple[dict[str, Any], ...]:
    return (
        {
            "tenant": "system",
            "model_name": "dispatch_recommendation_ranker",
            "model_version": "2026.05",
            "governance_status": "approved",
            "features": ("eta_minutes", "capability_match", "jurisdiction_fit", "coverage_gap"),
            "drift_score": 0.03,
            "auc": 0.91,
        },
    )



def seed_plan() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "configuration": default_configuration(),
        "parameters": default_parameter_values(),
        "rules": default_rules(),
        "units": default_units(),
        "governed_models": default_governed_models(),
        "side_effects": (),
    }


class PublicSafetyDispatchStandaloneApp:
    """Standalone one-PBC dispatch application with an owned in-memory datastore."""

    def __init__(self) -> None:
        self.configuration = default_configuration()
        self.parameters = dict(default_parameter_values())
        self.rules = {rule["rule_id"]: dict(rule) for rule in default_rules()}
        self.schema_extensions: dict[str, dict[str, Any]] = {}
        self.records = {table: {} for table in BUSINESS_TABLES}
        self.outbox: list[dict[str, Any]] = []
        self.inbox: list[dict[str, Any]] = []
        self.dead_letter: list[dict[str, Any]] = []
        self.audit_log: list[dict[str, Any]] = []
        self.handled_idempotency: set[str] = set()
        self._sequences: dict[str, int] = {}
        self._demo_tenants: set[str] = set()

    def configure_runtime(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        config = dict(config or {})
        backend = config.get("database_backend", self.configuration["database_backend"])
        topic = config.get("event_topic", APPGEN_X_TOPIC)
        ok = backend in ALLOWED_DATABASE_BACKENDS and topic == APPGEN_X_TOPIC
        if ok:
            self.configuration.update(config)
            self.configuration["event_contract"] = "AppGen-X"
            self.configuration["stream_engine_picker_visible"] = False
        return {"ok": ok, "configuration": dict(self.configuration), "side_effects": ()}

    def set_parameter(self, name: str, value: Any) -> dict[str, Any]:
        bounded = name in DOMAIN_PARAMETERS
        if bounded:
            self.parameters[name] = value
        record = self._store(
            f"{PBC_KEY}_public_safety_dispatch_runtime_parameter",
            tenant="system",
            code=name,
            title=name.replace("_", " ").title(),
            status="active" if bounded else "rejected",
            payload={"name": name, "value": value, "bounded": bounded},
            parameter_name=name,
            value=value,
            bounded=bounded,
        )
        return {"ok": bounded, "parameter": record, "side_effects": ()}

    def register_rule(self, rule: dict[str, Any]) -> dict[str, Any]:
        compiled = dict(rule)
        compiled.setdefault("rule_id", "unnamed_rule")
        compiled.setdefault("scope", "dispatch")
        compiled["compiled_hash"] = _digest(compiled)
        compiled["event_contract"] = "AppGen-X"
        self.rules[compiled["rule_id"]] = compiled
        record = self._store(
            f"{PBC_KEY}_public_safety_dispatch_policy_rule",
            tenant=compiled.get("tenant", "system"),
            code=compiled["rule_id"],
            title=compiled["rule_id"].replace("_", " ").title(),
            status=compiled.get("status", "compiled"),
            payload=compiled,
            rule_id=compiled["rule_id"],
            scope=compiled["scope"],
            compiled_hash=compiled["compiled_hash"],
        )
        self._audit("register_rule", record["table"], record["id"], record["payload"])
        return {"ok": True, "rule": record, "side_effects": ()}

    def register_schema_extension(self, table: str, fields: dict[str, Any]) -> dict[str, Any]:
        owned_table = table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        if owned_table not in RUNTIME_TABLES:
            return {"ok": False, "reason": "unknown_owned_table", "table": owned_table, "side_effects": ()}
        self.schema_extensions[owned_table] = dict(fields)
        record = self._store(
            f"{PBC_KEY}_public_safety_dispatch_schema_extension",
            tenant="system",
            code=owned_table,
            title=f"Extension for {owned_table}",
            status="proposed",
            payload={"table": owned_table, "fields": dict(fields)},
            table_name=owned_table,
            field_names=tuple(sorted(fields)),
        )
        self._audit("register_schema_extension", record["table"], record["id"], record["payload"])
        return {"ok": True, "table": owned_table, "extension": record, "side_effects": ()}

    def create_emergency_call(self, payload: dict[str, Any]) -> dict[str, Any]:
        required = ("tenant", "caller_name", "chief_complaint", "address")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "missing_fields": missing, "side_effects": ()}
        tenant = payload["tenant"]
        caller = self._validate_caller(payload)
        location = self._validate_location(payload)
        classification = self._classify_incident(payload)
        protocol_trace = self._triage_protocol(classification, payload, location)
        safety_alerts = self._derive_safety_alerts(payload, classification, location)
        duplicate_review = self._find_duplicate_incidents(tenant, payload, classification, location)
        incident, incident_resolution = self._materialize_incident(
            tenant,
            payload,
            classification,
            location,
            protocol_trace,
            safety_alerts,
            duplicate_review,
        )
        call_payload = {
            **dict(payload),
            "caller_validation": caller,
            "location_validation": location,
            "classification": classification,
            "protocol_trace": protocol_trace,
            "safety_alerts": safety_alerts,
            "conference_parties": tuple(payload.get("conference_parties", ())),
            "transfer_chain": tuple(payload.get("transfer_chain", ())),
            "attachments": tuple(payload.get("attachments", ())),
            "linked_incident_id": incident["id"],
            "duplicate_review": duplicate_review,
            "incident_resolution": incident_resolution,
        }
        call_record = self._store(
            f"{PBC_KEY}_emergency_call",
            tenant=tenant,
            code=payload.get("call_number", self._next_code("CALL")),
            title=payload["chief_complaint"],
            status="validated" if caller["callback_verified"] else "pending_callback_validation",
            payload=call_payload,
            call_source=payload.get("call_source", "voice"),
            caller_name=payload["caller_name"],
            callback_number=caller["normalized_callback_number"],
            chief_complaint=payload["chief_complaint"],
            location_text=payload["address"],
            location_confidence=location["confidence"],
        )
        self._emit_event("CallIntakeAccepted", tenant, {"call_id": call_record["id"], "incident_id": incident["id"], "priority": incident["priority"]})
        self._emit_event(LEGACY_EMITTED_EVENTS[0], tenant, {"call_id": call_record["id"], "incident_id": incident["id"]})
        milestone = self.create_response_milestone(
            {
                "tenant": tenant,
                "incident_id": incident["id"],
                "milestone_type": "triaged",
                "status": "triaged",
                "scene_notes": payload.get("narrative", "Call triaged."),
                "radio_channel": CHANNEL_FAMILIES[classification["channel_family"]]["dispatch"],
                "attachments": tuple(payload.get("attachments", ())),
                "safety_alerts": safety_alerts,
                "suppress_event": True,
            }
        )
        return {
            "ok": True,
            "call": call_record,
            "incident": incident,
            "incident_resolution": incident_resolution,
            "protocol_trace": protocol_trace,
            "duplicate_review": duplicate_review,
            "safety_alerts": safety_alerts,
            "milestone": milestone["milestone"],
            "side_effects": (),
        }

    def record_response_unit(self, payload: dict[str, Any]) -> dict[str, Any]:
        required = ("tenant", "unit_code", "discipline", "status", "agency", "jurisdiction", "beat")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "missing_fields": missing, "side_effects": ()}
        normalized = {
            **dict(payload),
            "capabilities": tuple(dict.fromkeys(tuple(payload.get("capabilities", (payload["discipline"],))))),
            "radio_profile": {
                "preferred_family": payload.get("radio_profile", {}).get("preferred_family", payload.get("discipline", "interop")),
                "portable": payload.get("radio_profile", {}).get("portable", CHANNEL_FAMILIES.get(payload.get("discipline", "interop"), CHANNEL_FAMILIES["interop"])["tactical"]),
            },
            "eta_minutes": int(payload.get("eta_minutes", 6)),
            "availability": payload.get("status") in {"available", "staged"},
        }
        record = self._store(
            f"{PBC_KEY}_response_unit",
            tenant=normalized["tenant"],
            code=normalized["unit_code"],
            title=normalized["unit_code"],
            status=normalized["status"],
            payload=normalized,
            unit_code=normalized["unit_code"],
            discipline=normalized["discipline"],
            agency=normalized["agency"],
            jurisdiction=normalized["jurisdiction"],
            beat=normalized["beat"],
            capabilities=normalized["capabilities"],
        )
        self._audit("record_response_unit", record["table"], record["id"], record["payload"])
        return {"ok": True, "record": record, "side_effects": ()}

    def review_incident(self, payload: dict[str, Any]) -> dict[str, Any]:
        incident = self._lookup(f"{PBC_KEY}_incident", payload.get("incident_id"))
        if incident is None:
            return {"ok": False, "reason": "incident_not_found", "side_effects": ()}
        snapshot = _copy_record(incident)
        merged_payload = deepcopy(snapshot["payload"])
        if payload.get("scene_notes"):
            merged_payload.setdefault("scene_notes", []).append(payload["scene_notes"])
        if payload.get("attachments"):
            merged_payload.setdefault("attachments", []).extend(tuple(payload["attachments"]))
        if payload.get("transfer_to_agency"):
            merged_payload.setdefault("transfer_chain", []).append(payload["transfer_to_agency"])
        if payload.get("conference_parties"):
            merged_payload.setdefault("conference_parties", []).extend(tuple(payload["conference_parties"]))
        if payload.get("priority_override"):
            snapshot["priority"] = int(payload["priority_override"])
            merged_payload.setdefault("priority_overrides", []).append(
                {
                    "new_priority": snapshot["priority"],
                    "reason": payload.get("override_reason", "dispatcher_review"),
                    "approved_by": payload.get("approved_by", "dispatcher"),
                }
            )
        if payload.get("cad_status"):
            snapshot["cad_status"] = payload["cad_status"]
        if payload.get("safety_alerts"):
            merged_payload["safety_alerts"] = list(dict.fromkeys(tuple(merged_payload.get("safety_alerts", ())) + tuple(payload["safety_alerts"])))
        snapshot["payload"] = merged_payload
        snapshot["updated_at"] = _utcnow()
        snapshot["audit_hash"] = _digest(snapshot)
        self.records[f"{PBC_KEY}_incident"][snapshot["id"]] = snapshot
        self._audit("review_incident", snapshot["table"], snapshot["id"], merged_payload)
        self._emit_event("IncidentClassified", snapshot["tenant"], {"incident_id": snapshot["id"], "priority": snapshot["priority"], "cad_status": snapshot["cad_status"]})
        return {"ok": True, "incident": snapshot, "before": incident, "side_effects": ()}

    def approve_dispatch_assignment(self, payload: dict[str, Any]) -> dict[str, Any]:
        incident = self._lookup(f"{PBC_KEY}_incident", payload.get("incident_id"))
        if incident is None:
            return {"ok": False, "reason": "incident_not_found", "side_effects": ()}
        requested_units = max(1, int(payload.get("required_units", 1 if incident["priority"] >= 3 else 2)))
        required_capabilities = tuple(dict.fromkeys(tuple(payload.get("required_capabilities", ()) or tuple(incident["payload"]["classification"]["required_capabilities"]))))
        requested_agency = payload.get("requested_agency") or incident["payload"].get("agency")
        candidates = self._rank_units(incident, required_capabilities, requested_agency)
        selected = tuple(candidate for candidate in candidates if candidate["eligible"])[:requested_units]
        mutual_aid = None
        if len(selected) < requested_units and payload.get("allow_mutual_aid", True):
            mutual_aid = self.simulate_mutual_aid(
                {
                    "tenant": incident["tenant"],
                    "incident_id": incident["id"],
                    "partner_agencies": ("county_fire", "regional_ems", "state_patrol"),
                    "requested_capabilities": required_capabilities,
                    "reason": "insufficient_local_coverage",
                    "requested_units": requested_units - len(selected),
                    "suppress_event": True,
                }
            )
        channel_family = payload.get("requested_channel_family") or incident["payload"]["classification"]["channel_family"]
        channel_plan = CHANNEL_FAMILIES.get(channel_family, CHANNEL_FAMILIES["interop"])
        assignment_payload = {
            "incident_id": incident["id"],
            "required_capabilities": required_capabilities,
            "candidate_units": candidates,
            "selected_units": tuple(item["unit"]["id"] for item in selected),
            "selected_unit_codes": tuple(item["unit"]["unit_code"] for item in selected),
            "jurisdiction": incident["jurisdiction"],
            "beat": incident["beat"],
            "agency": requested_agency,
            "radio_plan": channel_plan,
            "safety_alerts": incident["payload"].get("safety_alerts", ()),
            "response_sla_due_at": incident["response_sla_due_at"],
            "priority_escalated": len(selected) < requested_units or bool(incident["payload"].get("safety_alerts")),
            "mutual_aid_request_id": mutual_aid and mutual_aid["mutual_aid"]["id"],
        }
        assignment = self._store(
            f"{PBC_KEY}_dispatch_assignment",
            tenant=incident["tenant"],
            code=self._next_code("ASGN"),
            title=f"Dispatch for {incident['incident_number']}",
            status="dispatched" if selected else "pending_mutual_aid",
            payload=assignment_payload,
            incident_id=incident["id"],
            assignment_code=self._next_code("DSP"),
            selected_units=assignment_payload["selected_unit_codes"],
            radio_channel=channel_plan["dispatch"],
        )
        for candidate in selected:
            unit = _copy_record(candidate["unit"])
            unit["status"] = "dispatched"
            unit_payload = deepcopy(unit["payload"])
            unit_payload["assigned_incident_id"] = incident["id"]
            unit_payload["dispatch_score"] = candidate["score"]
            unit_payload["dispatch_reason"] = candidate["reasons"]
            unit["payload"] = unit_payload
            unit["updated_at"] = _utcnow()
            unit["audit_hash"] = _digest(unit)
            self.records[f"{PBC_KEY}_response_unit"][unit["id"]] = unit
        incident_update = self.review_incident(
            {
                "incident_id": incident["id"],
                "cad_status": "dispatched" if selected else "awaiting_mutual_aid",
                "scene_notes": f"Dispatch assignment {assignment['code']} prepared.",
                "safety_alerts": incident["payload"].get("safety_alerts", ()),
            }
        )
        milestone = self.create_response_milestone(
            {
                "tenant": incident["tenant"],
                "incident_id": incident["id"],
                "milestone_type": "dispatched",
                "status": "dispatched" if selected else "awaiting_mutual_aid",
                "scene_notes": f"Units dispatched: {', '.join(assignment_payload['selected_unit_codes']) or 'none'}",
                "radio_channel": channel_plan["dispatch"],
                "attachments": (),
                "safety_alerts": incident["payload"].get("safety_alerts", ()),
                "suppress_event": True,
            }
        )
        self._audit("approve_dispatch_assignment", assignment["table"], assignment["id"], assignment_payload)
        self._emit_event("DispatchRecommendationPrepared", incident["tenant"], {"incident_id": incident["id"], "assignment_id": assignment["id"], "selected_unit_count": len(selected)})
        self._emit_event("UnitsDispatched", incident["tenant"], {"incident_id": incident["id"], "assignment_id": assignment["id"], "radio_channel": channel_plan["dispatch"]})
        self._emit_event(LEGACY_EMITTED_EVENTS[1], incident["tenant"], {"incident_id": incident["id"], "assignment_id": assignment["id"]})
        return {
            "ok": True,
            "assignment": assignment,
            "recommendations": candidates,
            "selected": selected,
            "mutual_aid": mutual_aid and mutual_aid["mutual_aid"],
            "incident": incident_update["incident"],
            "milestone": milestone["milestone"],
            "side_effects": (),
        }

    def simulate_mutual_aid(self, payload: dict[str, Any]) -> dict[str, Any]:
        required = ("tenant", "incident_id", "partner_agencies", "requested_capabilities")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "missing_fields": missing, "side_effects": ()}
        record = self._store(
            f"{PBC_KEY}_mutual_aid",
            tenant=payload["tenant"],
            code=self._next_code("MA"),
            title=f"Mutual aid for {payload['incident_id']}",
            status=payload.get("status", "pending_ack"),
            payload={
                **dict(payload),
                "requested_units": int(payload.get("requested_units", 1)),
                "partner_agencies": tuple(payload["partner_agencies"]),
                "requested_capabilities": tuple(payload["requested_capabilities"]),
            },
            incident_id=payload["incident_id"],
            partner_agencies=tuple(payload["partner_agencies"]),
            requested_capabilities=tuple(payload["requested_capabilities"]),
        )
        self._audit("simulate_mutual_aid", record["table"], record["id"], record["payload"])
        if not payload.get("suppress_event"):
            self._emit_event("MutualAidRequested", payload["tenant"], {"incident_id": payload["incident_id"], "mutual_aid_id": record["id"]})
        return {"ok": True, "mutual_aid": record, "side_effects": ()}

    def create_response_milestone(self, payload: dict[str, Any]) -> dict[str, Any]:
        incident = self._lookup(f"{PBC_KEY}_incident", payload.get("incident_id"))
        if incident is None:
            return {"ok": False, "reason": "incident_not_found", "side_effects": ()}
        milestone_type = payload.get("milestone_type", "note")
        status = payload.get("status", milestone_type)
        record = self._store(
            f"{PBC_KEY}_response_milestone",
            tenant=payload.get("tenant", incident["tenant"]),
            code=self._next_code("MS"),
            title=milestone_type.replace("_", " ").title(),
            status=status,
            payload={
                **dict(payload),
                "attachments": tuple(payload.get("attachments", ())),
                "safety_alerts": tuple(payload.get("safety_alerts", ())),
            },
            incident_id=incident["id"],
            milestone_type=milestone_type,
            radio_channel=payload.get("radio_channel", CHANNEL_FAMILIES[incident["payload"]["classification"]["channel_family"]]["dispatch"]),
            scene_notes=payload.get("scene_notes", ""),
        )
        incident_payload = deepcopy(incident["payload"])
        incident_payload.setdefault("milestones", []).append({"milestone_id": record["id"], "type": milestone_type, "status": status})
        incident["cad_status"] = status
        incident["payload"] = incident_payload
        incident["updated_at"] = _utcnow()
        incident["audit_hash"] = _digest(incident)
        self.records[f"{PBC_KEY}_incident"][incident["id"]] = incident
        self._audit("create_response_milestone", record["table"], record["id"], record["payload"])
        if not payload.get("suppress_event"):
            self._emit_event("CadLifecycleUpdated", incident["tenant"], {"incident_id": incident["id"], "milestone_id": record["id"], "status": status})
        return {"ok": True, "milestone": record, "incident": incident, "side_effects": ()}

    def record_case_disposition(self, payload: dict[str, Any]) -> dict[str, Any]:
        incident = self._lookup(f"{PBC_KEY}_incident", payload.get("incident_id"))
        if incident is None:
            return {"ok": False, "reason": "incident_not_found", "side_effects": ()}
        discipline = payload.get("discipline") or incident["payload"]["classification"]["discipline"]
        allowed = DISCIPLINE_DISPOSITIONS.get(discipline, DISCIPLINE_DISPOSITIONS["multi"])
        disposition_code = payload.get("disposition_code")
        if disposition_code not in allowed:
            return {"ok": False, "reason": "invalid_disposition", "allowed": allowed, "side_effects": ()}
        disposition_payload = {
            **dict(payload),
            "after_action_review": {
                "response_sla_met": incident["payload"]["response_sla"]["status"] != "breached",
                "requires_supervisor_review": incident["priority"] <= 2 or bool(incident["payload"].get("safety_alerts")),
                "open_questions": tuple(payload.get("after_action_review", {}).get("open_questions", ())),
                "summary": payload.get("after_action_review", {}).get("summary", "Review completed."),
            },
            "evidence_attachments": tuple(payload.get("evidence_attachments", ())),
        }
        record = self._store(
            f"{PBC_KEY}_case_disposition",
            tenant=incident["tenant"],
            code=self._next_code("DSP"),
            title=f"Disposition for {incident['incident_number']}",
            status="closed",
            payload=disposition_payload,
            incident_id=incident["id"],
            discipline=discipline,
            disposition_code=disposition_code,
        )
        self.create_response_milestone(
            {
                "tenant": incident["tenant"],
                "incident_id": incident["id"],
                "milestone_type": "closed",
                "status": "closed",
                "scene_notes": payload.get("outcome_summary", "Incident closed."),
                "radio_channel": CHANNEL_FAMILIES[incident["payload"]["classification"]["channel_family"]]["dispatch"],
                "attachments": tuple(payload.get("evidence_attachments", ())),
                "safety_alerts": incident["payload"].get("safety_alerts", ()),
                "suppress_event": True,
            }
        )
        incident_payload = deepcopy(incident["payload"])
        incident_payload["disposition_id"] = record["id"]
        incident_payload["after_action_review"] = disposition_payload["after_action_review"]
        incident["status"] = "closed"
        incident["cad_status"] = "closed"
        incident["payload"] = incident_payload
        incident["updated_at"] = _utcnow()
        incident["audit_hash"] = _digest(incident)
        self.records[f"{PBC_KEY}_incident"][incident["id"]] = incident
        self._audit("record_case_disposition", record["table"], record["id"], record["payload"])
        self._emit_event("CaseDispositionRecorded", incident["tenant"], {"incident_id": incident["id"], "disposition_id": record["id"]})
        self._emit_event(LEGACY_EMITTED_EVENTS[2], incident["tenant"], {"incident_id": incident["id"], "disposition_id": record["id"]})
        return {"ok": True, "disposition": record, "incident": incident, "side_effects": ()}

    def receive_event(self, event: dict[str, Any]) -> dict[str, Any]:
        event_type = event.get("event_type", "Unknown")
        idempotency_key = event.get("idempotency_key") or event.get("event_id") or _digest(event)
        if idempotency_key in self.handled_idempotency:
            return {"ok": True, "duplicate": True, "idempotency_key": idempotency_key, "side_effects": ()}
        self.handled_idempotency.add(idempotency_key)
        if event_type not in CONSUMED_EVENTS:
            record = self._store_event(
                f"{PBC_KEY}_appgen_dead_letter_event",
                tenant=event.get("tenant", "system"),
                event_type=event_type,
                idempotency_key=idempotency_key,
                status="dead_letter",
                payload={**dict(event), "retry_policy": {"max_attempts": self.configuration.get("retry_limit", 5)}},
            )
            self.dead_letter.append(record)
            self._emit_event(LEGACY_EMITTED_EVENTS[3], record["tenant"], {"event_type": event_type, "dead_letter_id": record["id"]})
            return {
                "ok": False,
                "duplicate": False,
                "dead_letter_table": record["table"],
                "retry_policy": {"max_attempts": self.configuration.get("retry_limit", 5)},
                "record": record,
                "side_effects": (),
            }
        record = self._store_event(
            f"{PBC_KEY}_appgen_inbox_event",
            tenant=event.get("tenant", "system"),
            event_type=event_type,
            idempotency_key=idempotency_key,
            status="accepted",
            payload=dict(event),
        )
        self.inbox.append(record)
        self._audit("receive_event", record["table"], record["id"], record["payload"])
        return {"ok": True, "duplicate": False, "record": record, "side_effects": ()}

    def document_instruction_plan(self, document: str, instruction: str) -> dict[str, Any]:
        document_text = _normalize_text(document)
        inferred_operation = "review_incident"
        if any(keyword in document_text for keyword in ("dispatch", "assign", "unit")):
            inferred_operation = "approve_dispatch_assignment"
        elif any(keyword in document_text for keyword in ("mutual aid", "partner agency")):
            inferred_operation = "simulate_mutual_aid"
        elif any(keyword in document_text for keyword in ("after action", "disposition", "close")):
            inferred_operation = "record_case_disposition"
        entities = {
            "incident": bool(re.search(r"incident|call|cad", document_text)),
            "unit": bool(re.search(r"unit|engine|med|law", document_text)),
            "safety": bool(re.search(r"weapon|hazmat|unsafe|violent", document_text)),
        }
        preview = {
            "operation": inferred_operation,
            "target_tables": self._preview_tables_for_operation(inferred_operation),
            "fields_to_change": tuple(sorted(field for field, present in entities.items() if present)),
            "requires_human_confirmation": True,
            "crud_preview": {
                "instruction": instruction,
                "operation": "update" if entities["incident"] else "create",
                "event_contract": "AppGen-X",
            },
        }
        self._emit_event("AiPreviewPrepared", "system", {"operation": inferred_operation, "instruction": instruction})
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "document_digest": _digest({"document": document, "instruction": instruction}),
            "instruction": instruction,
            "inferred_operation": inferred_operation,
            "candidate_tables": preview["target_tables"],
            "requires_human_confirmation": True,
            "preview": preview,
            "side_effects": (),
        }

    def datastore_crud_plan(self, action: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        target = table or f"{PBC_KEY}_incident"
        owned_table = target if target.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{target}"
        if owned_table not in RUNTIME_TABLES:
            return {"ok": False, "reason": "foreign_table_rejected", "table": owned_table, "side_effects": ()}
        preview = {
            "operation": action,
            "table": owned_table,
            "fields": tuple(sorted((payload or {}).keys())),
            "requires_confirmation": action in {"create", "update", "delete"},
            "event_contract": "AppGen-X",
        }
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "action": action,
            "table": owned_table,
            "payload": dict(payload or {}),
            "requires_confirmation": preview["requires_confirmation"],
            "preview": preview,
            "side_effects": (),
        }

    def query_workbench(self, tenant: str = "default") -> dict[str, Any]:
        incidents = self._records_for_tenant(f"{PBC_KEY}_incident", tenant)
        calls = self._records_for_tenant(f"{PBC_KEY}_emergency_call", tenant)
        assignments = self._records_for_tenant(f"{PBC_KEY}_dispatch_assignment", tenant)
        units = self._records_for_tenant(f"{PBC_KEY}_response_unit", tenant)
        mutual_aids = self._records_for_tenant(f"{PBC_KEY}_mutual_aid", tenant)
        dispositions = self._records_for_tenant(f"{PBC_KEY}_case_disposition", tenant)
        workbench = self.build_workbench_view(tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "records": {
                "calls": calls,
                "incidents": incidents,
                "assignments": assignments,
                "units": units,
                "mutual_aids": mutual_aids,
                "dispositions": dispositions,
            },
            "summary": workbench["summary"],
            "queues": workbench["queues"],
            "read_only": True,
            "side_effects": (),
        }

    def build_workbench_view(self, tenant: str = "default") -> dict[str, Any]:
        incidents = self._records_for_tenant(f"{PBC_KEY}_incident", tenant)
        calls = self._records_for_tenant(f"{PBC_KEY}_emergency_call", tenant)
        units = self._records_for_tenant(f"{PBC_KEY}_response_unit", tenant)
        assignments = self._records_for_tenant(f"{PBC_KEY}_dispatch_assignment", tenant)
        mutual_aids = self._records_for_tenant(f"{PBC_KEY}_mutual_aid", tenant)
        dead_letters = tuple(record for record in self.dead_letter if record["tenant"] in {tenant, "system"})
        summary = {
            "call_count": len(calls),
            "active_incident_count": len(tuple(item for item in incidents if item["status"] != "closed")),
            "available_unit_count": len(tuple(item for item in units if item["status"] in {"available", "staged"})),
            "dispatch_assignment_count": len(assignments),
            "mutual_aid_pending_count": len(tuple(item for item in mutual_aids if item["status"] == "pending_ack")),
            "dead_letter_count": len(dead_letters),
            "audit_entry_count": len(self.audit_log),
            "configuration_bound": self.configuration.get("event_topic") == APPGEN_X_TOPIC,
        }
        queues = {
            "waiting_intake": tuple(call["id"] for call in calls if call["status"] != "validated"),
            "active_incidents": tuple(incident["id"] for incident in incidents if incident["status"] != "closed"),
            "units_awaiting_assignment": tuple(
                incident["id"]
                for incident in incidents
                if incident["status"] != "closed" and not any(assignment["incident_id"] == incident["id"] for assignment in assignments)
            ),
            "mutual_aid_pending_ack": tuple(item["id"] for item in mutual_aids if item["status"] == "pending_ack"),
            "priority_escalations": tuple(
                incident["id"]
                for incident in incidents
                if incident["priority"] <= 2 or incident["payload"]["response_sla"]["status"] == "watch"
            ),
            "safety_alerts": tuple(
                incident["id"] for incident in incidents if incident["payload"].get("safety_alerts")
            ),
            "sla_watch": tuple(
                incident["id"]
                for incident in incidents
                if incident["payload"]["response_sla"]["status"] in {"watch", "breached"}
            ),
            "dead_letter": tuple(record["id"] for record in dead_letters),
        }
        return {
            "ok": True,
            "tenant": tenant,
            "fragments": UI_FRAGMENTS,
            "forms": FORMS,
            "wizards": WIZARDS,
            "controls": CONTROLS,
            "queues": queues,
            "summary": summary,
            "binding_evidence": {
                "owned_tables": BUSINESS_TABLES,
                "runtime_tables": RUNTIME_TABLES,
                "event_contract": "AppGen-X",
                "required_event_topic": APPGEN_X_TOPIC,
                "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
                "permissions": PERMISSIONS,
                "stream_engine_picker_visible": False,
            },
            "queue_order": QUEUES,
            "side_effects": (),
        }

    def standalone_workflows(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            {
                "workflow_id": workflow,
                "label": workflow.replace("public_safety_dispatch_", "").replace("_", " ").title(),
                "steps": wizard["steps"],
                "outcome": wizard["outcome"],
            }
            for workflow, wizard in zip(WORKFLOWS, WIZARDS + (WIZARDS[-1],))
        )

    def standalone_manifest(self) -> dict[str, Any]:
        self.load_demo_workspace("tenant_alpha")
        workbench = self.build_workbench_view("tenant_alpha")
        return {
            "format": "appgen.public-safety-dispatch-standalone-app.v1",
            "ok": True,
            "pbc": PBC_KEY,
            "mode": "standalone_one_pbc_app",
            "manifest": PBC_MANIFEST,
            "routes": build_api_contract(),
            "services": build_service_contract(),
            "permissions": build_permissions_contract(),
            "events": build_event_contract(),
            "ui": build_ui_contract(),
            "agent": build_agent_contract(),
            "seed": seed_plan(),
            "workflows": self.standalone_workflows(),
            "bootstrap": {
                "query_result_count": workbench["summary"]["active_incident_count"],
                "workbench": workbench,
                "audit_chain_length": len(self.audit_log),
            },
            "side_effects": (),
        }

    def validate_standalone(self) -> dict[str, Any]:
        manifest = self.standalone_manifest()
        missing_sections = tuple(
            section
            for section in ("routes", "services", "permissions", "events", "ui", "agent", "seed", "workflows")
            if not manifest.get(section)
        )
        required_workflows = {
            "public_safety_dispatch_create_emergency_call_workflow",
            "public_safety_dispatch_record_response_unit_workflow",
            "public_safety_dispatch_dispatch_to_closeout_workflow",
            "public_safety_dispatch_mutual_aid_escalation_workflow",
        }
        workflow_ids = {item["workflow_id"] for item in manifest["workflows"]}
        return {
            "ok": not missing_sections and required_workflows <= workflow_ids and manifest["bootstrap"]["query_result_count"] >= 1,
            "missing_sections": missing_sections,
            "missing_workflows": tuple(sorted(required_workflows - workflow_ids)),
            "manifest": manifest,
            "side_effects": (),
        }

    def smoke_test(self) -> dict[str, Any]:
        validation = self.validate_standalone()
        workbench = validation["manifest"]["bootstrap"]["workbench"]
        return {
            "ok": validation["ok"] and bool(workbench["forms"]) and bool(workbench["wizards"]) and bool(workbench["controls"]),
            "validation": validation,
            "side_effects": (),
        }

    def load_demo_workspace(self, tenant: str = "tenant_alpha") -> None:
        if tenant in self._demo_tenants:
            return
        self.configure_runtime(default_configuration())
        for name, value in default_parameter_values().items():
            self.set_parameter(name, value)
        for rule in default_rules():
            self.register_rule(rule)
        for model in default_governed_models():
            self.register_governed_model(model)
        for unit in default_units(tenant):
            self.record_response_unit(unit)
        seeded_call = self.create_emergency_call(
            {
                "tenant": tenant,
                "call_source": "wireless",
                "caller_name": "Jordan Kim",
                "callback_number": "+1 (555) 010-4444",
                "chief_complaint": "Vehicle crash with smoke and trapped occupant",
                "narrative": "Two-car crash near the bridge, smoke from one engine compartment, occupant trapped.",
                "address": "410 Riverfront Ave",
                "jurisdiction": "central_city",
                "beat": "beat-1",
                "agency": "metro_dispatch",
                "lat": 40.7123,
                "lon": -74.0052,
                "attachments": ({"filename": "dashcam.jpg", "kind": "image"},),
            }
        )
        self.approve_dispatch_assignment(
            {
                "tenant": tenant,
                "incident_id": seeded_call["incident"]["id"],
                "required_units": 2,
                "allow_mutual_aid": True,
            }
        )
        self._demo_tenants.add(tenant)

    def register_governed_model(self, payload: dict[str, Any]) -> dict[str, Any]:
        governance_status = "approved" if payload.get("auc", 0.0) >= 0.85 and payload.get("drift_score", 1.0) <= 0.1 else "review_required"
        record = self._store(
            f"{PBC_KEY}_public_safety_dispatch_governed_model",
            tenant=payload.get("tenant", "system"),
            code=payload.get("model_name", self._next_code("MODEL")),
            title=payload.get("model_name", "Dispatch Model"),
            status=governance_status,
            payload=dict(payload),
            model_name=payload.get("model_name", "dispatch_model"),
            model_version=payload.get("model_version", "1.0"),
            governance_status=governance_status,
        )
        self._audit("register_governed_model", record["table"], record["id"], record["payload"])
        return {"ok": True, "model": record, "side_effects": ()}

    def run_advanced_assessment(self, tenant: str = "tenant_alpha") -> dict[str, Any]:
        self.load_demo_workspace(tenant)
        workbench = self.build_workbench_view(tenant)
        score = round(
            0.7
            + min(workbench["summary"]["available_unit_count"], 5) * 0.02
            + min(workbench["summary"]["dispatch_assignment_count"], 3) * 0.03,
            4,
        )
        return {
            "ok": True,
            "tenant": tenant,
            "score": score,
            "explanations": (
                "call intake validation available",
                "capability-based dispatch and mutual aid routing available",
                "dead-letter, audit trail, and AI previews available",
            ),
            "workbench": workbench,
            "side_effects": (),
        }

    def verify_owned_table_boundary(self, references: tuple[str, ...] | list[str]) -> dict[str, Any]:
        allowed = set(RUNTIME_TABLES) | set(CONSUMED_EVENTS)
        violations = tuple(sorted(reference for reference in references if reference not in allowed and not str(reference).startswith(f"{PBC_KEY}_")))
        return {
            "ok": not violations,
            "pbc": PBC_KEY,
            "owned_tables": RUNTIME_TABLES,
            "violations": violations,
            "shared_table_access": False,
            "side_effects": (),
        }

    def dispatch_route(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        route = next((item for item in PUBLIC_ROUTES if item["method"] == method and item["path"] == path), None)
        if route is None:
            return {"ok": False, "reason": "route_not_found", "route": f"{method} {path}", "side_effects": ()}
        operation = route["operation"]
        handler = getattr(self, operation)
        if operation == "query_workbench":
            return handler(payload.get("tenant", "default"))
        if operation == "document_instruction_plan":
            return handler(payload.get("document", ""), payload.get("instruction", "preview"))
        if operation == "datastore_crud_plan":
            return handler(payload.get("action", "create"), payload.get("table"), payload.get("payload"))
        return handler(payload)

    def _next_code(self, prefix: str) -> str:
        self._sequences[prefix] = self._sequences.get(prefix, 0) + 1
        return f"{prefix}-{self._sequences[prefix]:05d}"

    def _store(
        self,
        table: str,
        *,
        tenant: str,
        code: str,
        title: str,
        status: str,
        payload: dict[str, Any],
        **extra: Any,
    ) -> dict[str, Any]:
        record_id = self._next_code(table.rsplit("_", 1)[-1].upper())
        now = _utcnow()
        record = {
            "id": record_id,
            "table": table,
            "tenant": tenant,
            "code": code,
            "title": title,
            "status": status,
            "version": 1,
            "payload": deepcopy(payload),
            "created_at": now,
            "updated_at": now,
            **extra,
        }
        record["audit_hash"] = _digest(record)
        self.records[table][record_id] = record
        return _copy_record(record)

    def _store_event(
        self,
        table: str,
        *,
        tenant: str,
        event_type: str,
        idempotency_key: str,
        status: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        now = _utcnow()
        record = {
            "id": self._next_code("EVT"),
            "table": table,
            "tenant": tenant,
            "event_type": event_type,
            "topic": APPGEN_X_TOPIC,
            "status": status,
            "idempotency_key": idempotency_key,
            "payload": deepcopy(payload),
            "created_at": now,
            "updated_at": now,
        }
        record["audit_hash"] = _digest(record)
        if table == f"{PBC_KEY}_appgen_outbox_event":
            self.outbox.append(record)
        return _copy_record(record)

    def _lookup(self, table: str, record_id: str | None) -> dict[str, Any] | None:
        if not record_id:
            return None
        record = self.records.get(table, {}).get(record_id)
        return _copy_record(record) if record else None

    def _records_for_tenant(self, table: str, tenant: str) -> tuple[dict[str, Any], ...]:
        return tuple(_copy_record(record) for record in self.records[table].values() if record["tenant"] == tenant)

    def _emit_event(self, event_type: str, tenant: str, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._store_event(
            f"{PBC_KEY}_appgen_outbox_event",
            tenant=tenant,
            event_type=event_type,
            idempotency_key=f"{PBC_KEY}:{event_type}:{_digest(payload)}",
            status="queued",
            payload=payload,
        )
        self._audit("emit_event", record["table"], record["id"], payload)
        return record

    def _audit(self, action: str, table: str, record_id: str, payload: dict[str, Any]) -> None:
        previous_hash = self.audit_log[-1]["hash"] if self.audit_log else "GENESIS"
        entry = {
            "id": self._next_code("AUD"),
            "action": action,
            "table": table,
            "record_id": record_id,
            "payload": deepcopy(payload),
            "timestamp": _utcnow(),
            "previous_hash": previous_hash,
        }
        entry["hash"] = _digest(entry)
        self.audit_log.append(entry)

    def _validate_caller(self, payload: dict[str, Any]) -> dict[str, Any]:
        normalized = _normalize_phone(payload.get("callback_number"))
        source = payload.get("call_source", "voice")
        callback_verified = len(normalized) >= 10 or source in {"silent_text", "text_to_911", "alarm_company"}
        return {
            "normalized_callback_number": normalized,
            "callback_verified": callback_verified,
            "source": source,
            "requires_interpreter": bool(payload.get("language") and payload.get("language") != "english"),
            "tty_tdd": bool(payload.get("tty_tdd")),
            "callback_failure_reason": None if callback_verified else "insufficient_digits",
        }

    def _validate_location(self, payload: dict[str, Any]) -> dict[str, Any]:
        normalized_address = _normalize_text(payload.get("address"))
        confidence = 0.25 if payload.get("address") else 0.0
        confidence += 0.1 if re.search(r"\d", normalized_address) else 0.0
        confidence += 0.3 if payload.get("lat") is not None and payload.get("lon") is not None else 0.0
        confidence += 0.15 if payload.get("jurisdiction") else 0.0
        confidence += 0.15 if payload.get("beat") else 0.0
        if payload.get("call_source") in {"text_to_911", "silent_text"}:
            confidence -= 0.1
        if "mile marker" in _normalize_text(payload.get("address")) or "unknown" in _normalize_text(payload.get("address")):
            confidence -= 0.1
        confidence = round(max(0.05, min(confidence, 0.99)), 2)
        validation = "verified" if confidence >= 0.65 else "needs_confirmation"
        return {
            "address": payload.get("address"),
            "confidence": confidence,
            "validation_status": validation,
            "premise_type": payload.get("premise_type", "unknown"),
            "address_source": payload.get("call_source", "voice"),
            "fallback_geocode": payload.get("fallback_geocode") or payload.get("address"),
        }

    def _classify_incident(self, payload: dict[str, Any]) -> dict[str, Any]:
        text = " ".join(
            filter(
                None,
                (
                    str(payload.get("chief_complaint", "")),
                    str(payload.get("narrative", "")),
                ),
            )
        ).lower()
        classifier = INCIDENT_CLASSIFIERS[-1]
        for candidate in INCIDENT_CLASSIFIERS:
            if any(keyword in text for keyword in candidate["keywords"]):
                classifier = candidate
                break
        return {
            "discipline": classifier["discipline"],
            "incident_type": classifier["incident_type"],
            "priority": classifier["priority"],
            "determinant_code": classifier["determinant_code"],
            "required_capabilities": classifier["required_capabilities"],
            "channel_family": classifier["channel_family"],
            "caller_wording": payload.get("chief_complaint"),
        }

    def _triage_protocol(self, classification: dict[str, Any], payload: dict[str, Any], location: dict[str, Any]) -> dict[str, Any]:
        questions = [
            {"question": "Is anyone in immediate danger?", "answer": payload.get("caller_answers", {}).get("immediate_danger", "unknown")},
            {"question": "Are there weapons, fire, smoke, or hazardous materials?", "answer": payload.get("caller_answers", {}).get("hazards", "unknown")},
            {"question": "Is the location verified enough for dispatch?", "answer": "yes" if location["confidence"] >= 0.65 else "needs confirmation"},
        ]
        upgrade_reasons = []
        if payload.get("weapons") or payload.get("hazmat") or payload.get("active_violence"):
            upgrade_reasons.append("scene_hazard_present")
        if classification["discipline"] == "ems" and any(term in _normalize_text(payload.get("narrative")) for term in ("not breathing", "unresponsive", "cardiac")):
            upgrade_reasons.append("life_threatening_medical_signal")
        if location["confidence"] < 0.65:
            upgrade_reasons.append("low_location_confidence")
        final_priority = 1 if upgrade_reasons and classification["priority"] > 1 else classification["priority"]
        return {
            "discipline": classification["discipline"],
            "determinant_code": classification["determinant_code"],
            "questions": tuple(questions),
            "upgrade_reasons": tuple(upgrade_reasons),
            "downgrade_reasons": (),
            "final_priority": final_priority,
            "supervisor_override": payload.get("supervisor_override"),
        }

    def _derive_safety_alerts(self, payload: dict[str, Any], classification: dict[str, Any], location: dict[str, Any]) -> tuple[str, ...]:
        alerts = []
        text = _normalize_text(payload.get("narrative"))
        if payload.get("weapons") or "weapon" in text or "gun" in text:
            alerts.append("weapon_reported")
        if payload.get("hazmat") or "hazmat" in text or "chemical" in text:
            alerts.append("hazmat_risk")
        if payload.get("active_violence") or "violent" in text or "assault" in text:
            alerts.append("violence_risk")
        if payload.get("contagious_exposure"):
            alerts.append("contagious_exposure")
        if location["confidence"] < 0.65:
            alerts.append("location_unverified")
        if classification["discipline"] == "fire" and any(term in text for term in ("smoke", "collapse", "explosion")):
            alerts.append("fireground_hazard")
        return tuple(dict.fromkeys(alerts))

    def _find_duplicate_incidents(
        self,
        tenant: str,
        payload: dict[str, Any],
        classification: dict[str, Any],
        location: dict[str, Any],
    ) -> dict[str, Any]:
        matches = []
        target_address = _normalize_text(payload.get("address"))
        target_phone = _normalize_phone(payload.get("callback_number"))
        for incident in self._records_for_tenant(f"{PBC_KEY}_incident", tenant):
            if incident["status"] == "closed":
                continue
            score = 0.0
            if _normalize_text(incident["payload"].get("location", {}).get("address")) == target_address:
                score += 0.45
            if incident["payload"].get("classification", {}).get("incident_type") == classification["incident_type"]:
                score += 0.25
            if incident["payload"].get("caller_validation", {}).get("normalized_callback_number") == target_phone and target_phone:
                score += 0.15
            if incident["jurisdiction"] == payload.get("jurisdiction"):
                score += 0.1
            if location["confidence"] >= 0.8 and incident["beat"] == payload.get("beat"):
                score += 0.05
            if score >= 0.5:
                matches.append({"incident_id": incident["id"], "score": round(score, 2), "incident_number": incident["incident_number"]})
        matches = tuple(sorted(matches, key=lambda item: item["score"], reverse=True))
        return {
            "matched_incidents": matches,
            "requires_review": bool(matches),
            "recommended_incident_id": matches[0]["incident_id"] if matches and matches[0]["score"] >= 0.8 else None,
        }

    def _materialize_incident(
        self,
        tenant: str,
        payload: dict[str, Any],
        classification: dict[str, Any],
        location: dict[str, Any],
        protocol_trace: dict[str, Any],
        safety_alerts: tuple[str, ...],
        duplicate_review: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        existing_id = payload.get("merge_existing_incident_id") or (
            duplicate_review["recommended_incident_id"] if not payload.get("force_new_incident") else None
        )
        if existing_id:
            incident = self._lookup(f"{PBC_KEY}_incident", existing_id)
            if incident is not None:
                updated = self.review_incident(
                    {
                        "incident_id": existing_id,
                        "scene_notes": payload.get("narrative", "Additional caller report linked."),
                        "attachments": payload.get("attachments", ()),
                        "conference_parties": payload.get("conference_parties", ()),
                        "safety_alerts": safety_alerts,
                    }
                )
                return updated["incident"], "linked_existing_incident"
        priority = protocol_trace["final_priority"]
        sla_due_at = (datetime.now(timezone.utc) + timedelta(minutes=_sla_minutes(priority))).replace(microsecond=0).isoformat()
        incident_payload = {
            "classification": {**classification, "priority": priority},
            "location": location,
            "protocol_trace": protocol_trace,
            "caller_validation": self._validate_caller(payload),
            "safety_alerts": safety_alerts,
            "response_sla": {"minutes": _sla_minutes(priority), "due_by": sla_due_at, "status": "watch" if priority <= 2 else "tracking"},
            "transfer_chain": tuple(payload.get("transfer_chain", ())),
            "conference_parties": tuple(payload.get("conference_parties", ())),
            "attachments": tuple(payload.get("attachments", ())),
            "agency": payload.get("agency"),
        }
        incident = self._store(
            f"{PBC_KEY}_incident",
            tenant=tenant,
            code=self._next_code("INC"),
            title=classification["incident_type"].replace("_", " ").title(),
            status="open",
            payload=incident_payload,
            incident_number=self._next_code("CAD"),
            discipline=classification["discipline"],
            priority=priority,
            cad_status="pending_dispatch",
            jurisdiction=payload.get("jurisdiction", "unassigned"),
            beat=payload.get("beat", "unassigned"),
            response_sla_due_at=sla_due_at,
        )
        self._audit("create_incident", incident["table"], incident["id"], incident_payload)
        self._emit_event("IncidentClassified", tenant, {"incident_id": incident["id"], "priority": priority, "discipline": classification["discipline"]})
        return incident, "created_new_incident"

    def _rank_units(
        self,
        incident: dict[str, Any],
        required_capabilities: tuple[str, ...],
        requested_agency: str | None,
    ) -> tuple[dict[str, Any], ...]:
        ranked = []
        required = set(required_capabilities)
        incident_discipline = incident["payload"]["classification"]["discipline"]
        for unit in self._records_for_tenant(f"{PBC_KEY}_response_unit", incident["tenant"]):
            payload = unit["payload"]
            unit_capabilities = set(payload.get("capabilities", ()))
            capability_matches = len(required & unit_capabilities)
            discipline_match = incident_discipline == "multi" or payload.get("discipline") == incident_discipline or capability_matches > 0
            eligible = unit["status"] in {"available", "staged"} and discipline_match
            reasons = []
            score = capability_matches * 20
            if payload.get("jurisdiction") == incident["jurisdiction"]:
                score += 8
                reasons.append("same_jurisdiction")
            if payload.get("beat") == incident["beat"]:
                score += 5
                reasons.append("same_beat")
            if requested_agency and payload.get("agency") == requested_agency:
                score += 4
                reasons.append("agency_match")
            if unit["status"] == "available":
                score += 3
                reasons.append("available")
            score -= int(payload.get("eta_minutes", 10))
            if capability_matches:
                reasons.append("capability_match")
            if not eligible:
                reasons.append("not_eligible")
            ranked.append(
                {
                    "unit": unit,
                    "eligible": eligible,
                    "score": score,
                    "reasons": tuple(reasons),
                    "capability_matches": capability_matches,
                }
            )
        return tuple(sorted(ranked, key=lambda item: (item["eligible"], item["score"]), reverse=True))

    def _preview_tables_for_operation(self, operation: str) -> tuple[str, ...]:
        mapping = {
            "create_emergency_call": (f"{PBC_KEY}_emergency_call", f"{PBC_KEY}_incident"),
            "approve_dispatch_assignment": (f"{PBC_KEY}_dispatch_assignment", f"{PBC_KEY}_response_unit"),
            "simulate_mutual_aid": (f"{PBC_KEY}_mutual_aid",),
            "record_case_disposition": (f"{PBC_KEY}_case_disposition", f"{PBC_KEY}_incident"),
            "review_incident": (f"{PBC_KEY}_incident", f"{PBC_KEY}_response_milestone"),
        }
        return mapping.get(operation, (f"{PBC_KEY}_incident",))



def build_standalone_app() -> PublicSafetyDispatchStandaloneApp:
    return PublicSafetyDispatchStandaloneApp()



def build_permissions_contract() -> dict[str, Any]:
    return {
        "format": "appgen.public-safety-dispatch-permissions.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": PERMISSIONS,
        "roles": ("call_taker", "dispatcher", "supervisor", "auditor", "admin"),
        "action_permissions": {
            "configure_runtime": f"{PBC_KEY}.admin",
            "set_parameter": f"{PBC_KEY}.admin",
            "register_rule": f"{PBC_KEY}.admin",
            "register_schema_extension": f"{PBC_KEY}.admin",
            "create_emergency_call": f"{PBC_KEY}.create",
            "record_response_unit": f"{PBC_KEY}.update",
            "review_incident": f"{PBC_KEY}.update",
            "approve_dispatch_assignment": f"{PBC_KEY}.dispatch",
            "simulate_mutual_aid": f"{PBC_KEY}.dispatch",
            "create_response_milestone": f"{PBC_KEY}.update",
            "record_case_disposition": f"{PBC_KEY}.approve",
            "receive_event": f"{PBC_KEY}.audit",
            "query_workbench": f"{PBC_KEY}.audit",
            "document_instruction_plan": f"{PBC_KEY}.audit",
            "datastore_crud_plan": f"{PBC_KEY}.audit",
        },
        "side_effects": (),
    }



def build_event_contract() -> dict[str, Any]:
    return {
        "format": "appgen.public-safety-dispatch-event-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "emitted": EMITTED_EVENTS,
        "consumed": CONSUMED_EVENTS,
        "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
        "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "event_contract": "AppGen-X",
        "topic": APPGEN_X_TOPIC,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }



def build_schema_contract() -> dict[str, Any]:
    tables = tuple(
        {
            "table": table,
            "fields": TABLE_FIELDS[table],
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table in RUNTIME_TABLES
    )
    relationships = (
        {"from": f"{PBC_KEY}_dispatch_assignment.incident_id", "to": f"{PBC_KEY}_incident.id", "type": "owned_child"},
        {"from": f"{PBC_KEY}_mutual_aid.incident_id", "to": f"{PBC_KEY}_incident.id", "type": "owned_child"},
        {"from": f"{PBC_KEY}_response_milestone.incident_id", "to": f"{PBC_KEY}_incident.id", "type": "owned_timeline"},
        {"from": f"{PBC_KEY}_case_disposition.incident_id", "to": f"{PBC_KEY}_incident.id", "type": "owned_closeout"},
    )
    return {
        "format": "appgen.public-safety-dispatch-owned-schema-contract.v1",
        "ok": len(tables) == len(RUNTIME_TABLES),
        "pbc": PBC_KEY,
        "tables": tables,
        "relationships": relationships,
        "migrations": tuple(
            {
                "path": f"pbcs/{PBC_KEY}/migrations/001_initial.sql",
                "operation": "create_owned_table_bundle",
                "table": table,
                "backend_allowlist": ALLOWED_DATABASE_BACKENDS,
            }
            for table in RUNTIME_TABLES
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table.split("_")),
                "table": table,
                "fields": TABLE_FIELDS[table],
            }
            for table in RUNTIME_TABLES
        ),
        "datastore_backends": ALLOWED_DATABASE_BACKENDS,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "side_effects": (),
    }



def build_service_contract() -> dict[str, Any]:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "create_emergency_call",
        "record_response_unit",
        "review_incident",
        "approve_dispatch_assignment",
        "simulate_mutual_aid",
        "create_response_milestone",
        "record_case_disposition",
        "document_instruction_plan",
        "datastore_crud_plan",
        "register_governed_model",
        "run_advanced_assessment",
    )
    query_methods = (
        "query_workbench",
        "build_workbench_view",
        "verify_owned_table_boundary",
    )
    return {
        "format": "appgen.public-safety-dispatch-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": command_methods,
        "query_methods": query_methods,
        "transaction_boundary": "public_safety_dispatch_owned_datastore_plus_outbox",
        "mutates_only": RUNTIME_TABLES,
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "side_effects": (),
    }



def build_api_contract() -> dict[str, Any]:
    return {
        "format": "appgen.public-safety-dispatch-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(
            {
                "route": f"{item['method']} {item['path']}",
                "method": item["method"],
                "path": item["path"],
                "operation": item["operation"],
                "requires_permission": item["permission"],
                "owned_tables": RUNTIME_TABLES,
                "idempotency_key": f"{PBC_KEY}:{item['operation']}",
            }
            for item in PUBLIC_ROUTES
        ),
        "declared_catalog_routes": tuple(f"{item['method']} {item['path']}" for item in PUBLIC_ROUTES),
        "events": {"emits": EMITTED_EVENTS, "consumes": CONSUMED_EVENTS},
        "emits": EMITTED_EVENTS,
        "consumes": CONSUMED_EVENTS,
        "permissions": tuple(sorted(PERMISSIONS)),
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "owned_tables": RUNTIME_TABLES,
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "required_event_topic": APPGEN_X_TOPIC,
        "stream_engine_picker_visible": False,
        "configuration": tuple(default_configuration().keys()),
        "side_effects": (),
    }



def build_ui_contract() -> dict[str, Any]:
    return {
        "format": "appgen.public-safety-dispatch-ui-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": UI_FRAGMENTS,
        "forms": FORMS,
        "wizards": WIZARDS,
        "controls": CONTROLS,
        "queues": QUEUES,
        "configuration_editor": True,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "keyboard_shortcuts": {
            "new_call": "Ctrl+Shift+C",
            "dispatch_recommendation": "Ctrl+Shift+D",
            "unit_status": "Ctrl+Shift+U",
            "radio_log": "Ctrl+Shift+R",
            "incident_search": "Ctrl+K",
        },
        "panels": {
            "map": {"overlays": ("jurisdiction", "beat", "hydrants", "hospitals", "staging_points")},
            "radio": {"channels": CHANNEL_FAMILIES},
            "assistant": {"skills": ("intake_draft", "dispatch_explanation", "radio_log_summary", "crud_preview")},
        },
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }



def build_agent_contract() -> dict[str, Any]:
    skills = (
        {
            "name": f"{PBC_KEY}_intake_draft",
            "description": "Turn transcripts and notes into structured intake drafts with missing-question prompts.",
            "requires_confirmation_for_mutation": True,
        },
        {
            "name": f"{PBC_KEY}_dispatch_explanation",
            "description": "Explain unit recommendations using ETA, capability fit, jurisdiction, beat, and agency coverage.",
            "requires_confirmation_for_mutation": True,
        },
        {
            "name": f"{PBC_KEY}_radio_log_summary",
            "description": "Summarize radio and milestone evidence into after-action and records handoff drafts.",
            "requires_confirmation_for_mutation": True,
        },
        {
            "name": f"{PBC_KEY}_crud_preview",
            "description": "Preview safe CRUD mutations against owned dispatch tables only.",
            "requires_confirmation_for_mutation": True,
        },
    )
    return {
        "format": "appgen.public-safety-dispatch-agent-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "skills": skills,
        "entrypoint": f"/assistant/pbc/{PBC_KEY}",
        "capabilities": (
            "task_guidance",
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "dispatch_explanation",
            "records_handoff_summary",
        ),
        "side_effects": (),
    }



def standalone_application_manifest() -> dict[str, Any]:
    return build_standalone_app().standalone_manifest()



def validate_standalone_application() -> dict[str, Any]:
    return build_standalone_app().validate_standalone()



def standalone_smoke_test() -> dict[str, Any]:
    return build_standalone_app().smoke_test()



def build_runtime_capabilities() -> dict[str, Any]:
    app = build_standalone_app()
    smoke = standalone_smoke_test()
    return {
        "format": "appgen.public-safety-dispatch-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain_depth_contract()["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": RUNTIME_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "standard_features": STANDARD_FEATURES,
        "capabilities": ADVANCED_CAPABILITIES,
        "operations": tuple(build_service_contract()["command_methods"] + build_service_contract()["query_methods"] + ("build_schema_contract", "build_service_contract", "build_api_contract", "build_release_evidence")),
        "smoke": smoke,
        "world_class_domain_depth": domain_depth_contract(),
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "ui_fragments": UI_FRAGMENTS,
        "application_mode": "standalone_one_pbc_app",
        "side_effects": (),
    }



def build_release_evidence() -> dict[str, Any]:
    app = build_standalone_app()
    app.load_demo_workspace("tenant_release")
    call = app.create_emergency_call(
        {
            "tenant": "tenant_release",
            "call_source": "text_to_911",
            "caller_name": "Avery Singh",
            "callback_number": "555-010-9000",
            "chief_complaint": "Possible overdose in parking lot",
            "narrative": "Caller reports unconscious person by a blue sedan, no weapons seen.",
            "address": "1100 Harbor Blvd",
            "jurisdiction": "central_city",
            "beat": "beat-2",
            "agency": "metro_dispatch",
            "lat": 40.7001,
            "lon": -74.0021,
            "conference_parties": ({"role": "witness", "name": "Store clerk"},),
        }
    )
    assignment = app.approve_dispatch_assignment(
        {
            "tenant": "tenant_release",
            "incident_id": call["incident"]["id"],
            "required_units": 1,
            "allow_mutual_aid": True,
        }
    )
    milestone = app.create_response_milestone(
        {
            "tenant": "tenant_release",
            "incident_id": call["incident"]["id"],
            "milestone_type": "on_scene",
            "status": "on_scene",
            "scene_notes": "EMS unit on scene, naloxone prepared.",
            "radio_channel": "EMS-TAC-2",
            "attachments": ({"filename": "patient_care_note.txt", "kind": "text"},),
            "safety_alerts": (),
        }
    )
    disposition = app.record_case_disposition(
        {
            "tenant": "tenant_release",
            "incident_id": call["incident"]["id"],
            "discipline": "ems",
            "disposition_code": "transport",
            "outcome_summary": "Patient transported to trauma center.",
            "after_action_review": {"summary": "Dispatch questions captured overdose indicators early."},
            "evidence_attachments": ({"filename": "handoff.pdf", "kind": "pdf"},),
        }
    )
    unknown = app.receive_event({"tenant": "tenant_release", "event_type": "UnexpectedEvent", "event_id": "evt-bad-1"})
    assistant = app.document_instruction_plan("Dispatch notes require mutual aid review and scene safety summary.", "Prepare supervisor brief")
    crud = app.datastore_crud_plan("update", f"{PBC_KEY}_incident", {"status": "review"})
    workbench = app.build_workbench_view("tenant_release")
    schema = build_schema_contract()
    service = build_service_contract()
    api = build_api_contract()
    checks = (
        {"id": "standalone_application", "ok": app.smoke_test()["ok"]},
        {"id": "call_intake_and_classification", "ok": call["ok"] and call["incident"]["priority"] <= 2},
        {"id": "dispatch_and_channel_coordination", "ok": assignment["ok"] and bool(assignment["assignment"]["radio_channel"])},
        {"id": "cad_lifecycle_and_scene_notes", "ok": milestone["ok"] and milestone["incident"]["cad_status"] == "on_scene"},
        {"id": "after_action_review", "ok": disposition["ok"] and disposition["incident"]["cad_status"] == "closed"},
        {"id": "dead_letter_retry_evidence", "ok": unknown["ok"] is False and bool(unknown.get("dead_letter_table"))},
        {"id": "assistant_crud_preview", "ok": assistant["ok"] and crud["ok"]},
        {"id": "workbench_forms_wizards_controls", "ok": bool(workbench["forms"]) and bool(workbench["wizards"]) and bool(workbench["controls"])},
        {"id": "schema_service_api_contracts", "ok": schema["ok"] and service["ok"] and api["ok"]},
        {"id": "ordinary_backends_only", "ok": schema["database_backends"] == ALLOWED_DATABASE_BACKENDS},
    )
    return {
        "format": "appgen.public-safety-dispatch-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": build_permissions_contract(),
        "ui": build_ui_contract(),
        "agent": build_agent_contract(),
        "workbench": workbench,
        "assistant_preview": assistant,
        "crud_preview": crud,
        "dead_letter": unknown,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }



def pbc_generation_smoke_audit() -> dict[str, Any]:
    app = build_standalone_app()
    app.load_demo_workspace("tenant_smoke")
    workbench = app.query_workbench("tenant_smoke")
    route = app.dispatch_route("GET", "/public-safety-dispatch-workbench", {"tenant": "tenant_smoke"})
    boundary = app.verify_owned_table_boundary(RUNTIME_TABLES + ("foreign_table",))
    checks = (
        {"id": "standalone_smoke", "ok": app.smoke_test()["ok"]},
        {"id": "workbench_non_empty", "ok": workbench["summary"]["active_incident_count"] >= 1},
        {"id": "route_dispatch", "ok": route["ok"]},
        {"id": "boundary_rejects_foreign", "ok": boundary["ok"] is False},
    )
    return {
        "format": "appgen.public-safety-dispatch-generation-smoke-audit.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "workbench": workbench,
        "route": route,
        "boundary": boundary,
        "side_effects": (),
    }
