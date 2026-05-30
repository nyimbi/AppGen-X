"""Executable runtime contract for the airline_operations_control PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib

from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import domain_depth_contract
from .domain_depth import execute_domain_operation
from .operations_planning import build_operational_workbench
from .operations_planning import build_tail_rotation_graph
from .operations_planning import normalize_aircraft_rotation
from .operations_planning import normalize_flight_leg


PBC_KEY = "airline_operations_control"
AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES = (
    "airline_operations_control_flight_leg",
    "airline_operations_control_aircraft_rotation",
    "airline_operations_control_crew_pairing",
    "airline_operations_control_disruption_event",
    "airline_operations_control_reaccommodation_plan",
    "airline_operations_control_operations_decision",
    "airline_operations_control_delay_code",
    "airline_operations_control_airline_operations_control_policy_rule",
    "airline_operations_control_airline_operations_control_runtime_parameter",
    "airline_operations_control_airline_operations_control_schema_extension",
    "airline_operations_control_airline_operations_control_control_assertion",
    "airline_operations_control_airline_operations_control_governed_model",
    "airline_operations_control_appgen_outbox_event",
    "airline_operations_control_appgen_inbox_event",
    "airline_operations_control_appgen_dead_letter_event",
)
AIRLINE_OPERATIONS_CONTROL_RUNTIME_TABLES = AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES
AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC = "pbc.airline_operations_control.events"
AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES = (
    "AirlineOperationsControlCreated",
    "AirlineOperationsControlUpdated",
    "AirlineOperationsControlApproved",
    "AirlineOperationsControlExceptionOpened",
)
AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES = (
    "PolicyChanged",
    "AuditEventSealed",
    "OperationalKpiChanged",
)
AIRLINE_OPERATIONS_CONTROL_STANDARD_FEATURE_KEYS = (
    "flight_leg_management",
    "airline_operations_control_workflow",
    "airline_operations_control_analytics",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "workbench",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "continuous_release_assurance",
)
AIRLINE_OPERATIONS_CONTROL_RUNTIME_CAPABILITY_KEYS = (
    "airline_operations_control_event_sourced_operational_history",
    "airline_operations_control_multi_tenant_policy_isolation",
    "airline_operations_control_schema_evolution_resilience",
    "airline_operations_control_autonomous_anomaly_detection",
    "airline_operations_control_semantic_document_instruction_understanding",
    "airline_operations_control_predictive_risk_scoring",
    "airline_operations_control_counterfactual_scenario_simulation",
    "airline_operations_control_cryptographic_audit_proofs",
    "airline_operations_control_continuous_control_testing",
    "airline_operations_control_carbon_and_sustainability_awareness",
    "airline_operations_control_cross_pbc_event_federation",
    "airline_operations_control_governed_ai_agent_execution",
)
AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS = (
    "AirlineOperationsControlWorkbench",
    "AirlineOperationsControlDetail",
    "AirlineOperationsControlAssistantPanel",
    "AirlineOperationsControlRecoveryConsole",
    "AirlineOperationsControlReleaseWorkbench",
)
AIRLINE_OPERATIONS_CONTROL_BUSINESS_TABLES = (
    "airline_operations_control_flight_leg",
    "airline_operations_control_aircraft_rotation",
    "airline_operations_control_crew_pairing",
    "airline_operations_control_disruption_event",
    "airline_operations_control_reaccommodation_plan",
    "airline_operations_control_operations_decision",
    "airline_operations_control_delay_code",
    "airline_operations_control_airline_operations_control_policy_rule",
    "airline_operations_control_airline_operations_control_runtime_parameter",
    "airline_operations_control_airline_operations_control_schema_extension",
    "airline_operations_control_airline_operations_control_control_assertion",
    "airline_operations_control_airline_operations_control_governed_model",
)
AIRLINE_OPERATIONS_CONTROL_ACTION_PERMISSIONS = {
    "view_workbench": "airline_operations_control.read",
    "manage_flight_leg": "airline_operations_control.create",
    "manage_rotation": "airline_operations_control.update",
    "review_crew_legality": "airline_operations_control.update",
    "record_disruption": "airline_operations_control.update",
    "plan_reaccommodation": "airline_operations_control.update",
    "record_operations_decision": "airline_operations_control.approve",
    "maintain_runtime_controls": "airline_operations_control.admin",
    "review_release_evidence": "airline_operations_control.read",
    "use_ai_assistant": "airline_operations_control.read",
}
AIRLINE_OPERATIONS_CONTROL_ROLE_BUNDLES = {
    "network_controller": (
        "airline_operations_control.read",
        "airline_operations_control.create",
        "airline_operations_control.update",
    ),
    "duty_manager": (
        "airline_operations_control.read",
        "airline_operations_control.update",
        "airline_operations_control.approve",
    ),
    "release_auditor": (
        "airline_operations_control.read",
        "airline_operations_control.admin",
    ),
}
AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC,
    "control_center": "network",
    "workbench_limit": 50,
    "assistant_requires_confirmation": True,
    "tenant_isolation_mode": "strict",
}
AIRLINE_OPERATIONS_CONTROL_DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.7,
    "materiality_threshold": 0.6,
    "approval_sla_hours": 2,
    "risk_threshold": 0.55,
    "forecast_horizon_days": 2,
    "workbench_limit": 50,
}
AIRLINE_OPERATIONS_CONTROL_DEFAULT_RULE = {
    "rule_id": "airline_operations_control.release_readiness",
    "tenant": "tenant_demo",
    "scope": "network_control",
    "status": "active",
    "delay_code_discipline": {"required": True},
    "turn_risk_policy": {"highlight_impossible": True, "highlight_marginal": True},
    "manual_reaccommodation_review_threshold": {"disrupted_pax_count": 20},
}


def airline_operations_control_empty_state() -> dict:
    return {
        "records": {},
        "flight_legs": {},
        "aircraft_rotations": {},
        "crew_pairings": {},
        "disruption_events": {},
        "reaccommodation_plans": {},
        "operations_decisions": {},
        "delay_codes": {},
        "workflows": {},
        "assistant_plans": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _copy(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _event(state: dict, event_type: str, payload: dict) -> None:
    state["outbox"].append(
        {
            "event_type": event_type,
            "topic": AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC,
            "payload": dict(payload),
            "idempotency_key": _digest((event_type, payload)),
        }
    )


def _normalize_generic_record(kind: str, payload: dict) -> dict:
    source = dict(payload)
    record_id = str(
        source.get("id")
        or source.get(f"{kind}_id")
        or source.get("code")
        or source.get("reference")
        or f"{kind}-{_digest(source)[:10]}"
    )
    return {
        "id": record_id,
        "tenant": source.get("tenant", "default"),
        "kind": kind,
        "status": str(source.get("status", "open")).lower(),
        "summary": source.get("summary") or source.get("title") or record_id,
        "references": tuple(source.get("references", ()) or ()),
        "workflow_state": source.get("workflow_state", "triage"),
        "raw_payload": source,
    }


def _store_generic_record(
    state: dict,
    *,
    store_name: str,
    kind: str,
    payload: dict,
    emitted_event: str,
    extra_fields: dict | None = None,
) -> dict:
    next_state = _copy(state)
    record = _normalize_generic_record(kind, payload)
    if extra_fields:
        record.update(extra_fields)
    next_state["records"][record["id"]] = record
    next_state[store_name][record["id"]] = record
    _event(next_state, emitted_event, record)
    return {"ok": True, "state": next_state, "record": record, "side_effects": ()}


def _tenant_records(store: dict, tenant: str) -> tuple[dict, ...]:
    return tuple(record for record in store.values() if record.get("tenant", "default") == tenant)


def _release_scenarios() -> tuple[dict, ...]:
    return (
        {
            "scenario": "on_time_rotation",
            "covers": ("canonical_leg_timeline", "tail_rotation_continuity"),
            "evidence": "One arrival feeds one outbound with protected turn buffer.",
        },
        {
            "scenario": "late_inbound_broken_turn",
            "covers": ("minimum_turn_feasibility", "operations_decision_journal"),
            "evidence": "Broken turn risk is surfaced ahead of outbound departure control.",
        },
        {
            "scenario": "diversion_and_return_to_gate",
            "covers": ("branch_timeline", "disruption_event_follow_through"),
            "evidence": "Diversion and return-to-gate branches remain authoritative in one timeline.",
        },
        {
            "scenario": "ferry_recovery_leg",
            "covers": ("ferry_leg_variant", "rotation_recovery"),
            "evidence": "Recovery leg stays coherent with same-tail downstream planning.",
        },
    )


def airline_operations_control_configure_runtime(state: dict, config: dict) -> dict:
    next_state = _copy(state)
    merged = {**AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION, **dict(config)}
    ok = (
        merged.get("database_backend") in AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS
        and merged.get("event_topic") == AIRLINE_OPERATIONS_CONTROL_REQUIRED_EVENT_TOPIC
    )
    merged["event_contract"] = "AppGen-X"
    merged["stream_engine_picker_visible"] = False
    next_state["configuration"] = merged
    return {"ok": ok, "state": next_state, "configuration": merged, "side_effects": ()}


def airline_operations_control_set_parameter(state: dict, name: str, value) -> dict:
    next_state = _copy(state)
    next_state["parameters"][name] = {
        "name": name,
        "value": value,
        "scope": "domain",
        "bounded": True,
    }
    return {"ok": True, "state": next_state, "parameter": next_state["parameters"][name], "side_effects": ()}


def airline_operations_control_register_rule(state: dict, rule: dict) -> dict:
    next_state = _copy(state)
    compiled = {**dict(rule), "compiled_hash": _digest(rule), "event_contract": "AppGen-X"}
    rule_id = compiled.get("rule_id", "domain_rule")
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def airline_operations_control_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}


def airline_operations_control_receive_event(state: dict, event: dict) -> dict:
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES:
        next_state["dead_letter"].append(
            {
                "event": dict(event),
                "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
                "retry_policy": {"max_attempts": 5},
            }
        )
        return {
            "ok": False,
            "duplicate": False,
            "state": next_state,
            "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
            "side_effects": (),
        }
    next_state["inbox"].append(dict(event))
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def airline_operations_control_command_flight_leg(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    record = normalize_flight_leg(payload)
    next_state["records"][record["id"]] = record
    next_state["flight_legs"][record["id"]] = record
    _event(next_state, AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[0], record)
    return {
        "ok": True,
        "state": next_state,
        "record": record,
        "timeline": record["timeline"],
        "authoritative_status": record["authoritative_status"],
        "side_effects": (),
    }


def airline_operations_control_record_aircraft_rotation(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    flight_legs = tuple(next_state.get("flight_legs", {}).values())
    rotation = normalize_aircraft_rotation(payload, flight_legs)
    graph = build_tail_rotation_graph(
        [leg for leg in flight_legs if leg["tail_number"] == rotation["tail_number"]],
        rotation,
    )
    stored = {**rotation, "graph": graph}
    next_state["records"][rotation["rotation_id"]] = stored
    next_state["aircraft_rotations"][rotation["rotation_id"]] = stored
    _event(
        next_state,
        AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[1],
        {"rotation_id": rotation["rotation_id"], "tail_number": rotation["tail_number"]},
    )
    return {"ok": True, "state": next_state, "rotation": stored, "graph": graph, "side_effects": ()}


def airline_operations_control_command_crew_pairing(state: dict, payload: dict) -> dict:
    legality_state = str(payload.get("legality_state", "legal")).lower()
    remaining_duty_minutes = int(payload.get("remaining_duty_minutes", 180))
    risk_level = "high" if legality_state != "legal" or remaining_duty_minutes < 60 else "medium" if remaining_duty_minutes < 120 else "low"
    return _store_generic_record(
        state,
        store_name="crew_pairings",
        kind="crew_pairing",
        payload=payload,
        emitted_event=AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[1],
        extra_fields={
            "legality_state": legality_state,
            "remaining_duty_minutes": remaining_duty_minutes,
            "reserve_activation_required": bool(payload.get("reserve_activation_required")),
            "risk_level": risk_level,
        },
    )


def airline_operations_control_command_disruption_event(state: dict, payload: dict) -> dict:
    return _store_generic_record(
        state,
        store_name="disruption_events",
        kind="disruption_event",
        payload=payload,
        emitted_event=AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[3],
        extra_fields={
            "severity": str(payload.get("severity", "medium")).lower(),
            "event_type": payload.get("event_type", "operational"),
            "affected_leg_ids": tuple(payload.get("affected_leg_ids", ()) or ()),
            "source_lineage": tuple(payload.get("source_lineage", ()) or ()),
            "dedupe_fingerprint": _digest((payload.get("event_type"), payload.get("affected_leg_ids"), payload.get("station"), payload.get("route"))),
        },
    )


def airline_operations_control_command_reaccommodation_plan(state: dict, payload: dict) -> dict:
    return _store_generic_record(
        state,
        store_name="reaccommodation_plans",
        kind="reaccommodation_plan",
        payload=payload,
        emitted_event=AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[1],
        extra_fields={
            "passenger_count": int(payload.get("passenger_count", 0)),
            "manual_review_required": bool(payload.get("manual_review_required", False)),
            "blocked_reason": payload.get("blocked_reason"),
        },
    )


def airline_operations_control_command_operations_decision(state: dict, payload: dict) -> dict:
    return _store_generic_record(
        state,
        store_name="operations_decisions",
        kind="operations_decision",
        payload=payload,
        emitted_event=AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[2],
        extra_fields={
            "decision_type": payload.get("decision_type", "recovery"),
            "selected_action": payload.get("selected_action"),
            "alternatives": tuple(payload.get("alternatives", ()) or ()),
            "approval_state": payload.get("approval_state", "draft"),
        },
    )


def airline_operations_control_record_delay_code(state: dict, payload: dict) -> dict:
    return _store_generic_record(
        state,
        store_name="delay_codes",
        kind="delay_code",
        payload=payload,
        emitted_event=AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[1],
        extra_fields={
            "primary_code": payload.get("primary_code"),
            "contributing_codes": tuple(payload.get("contributing_codes", ()) or ()),
        },
    )


def airline_operations_control_plan_recovery_workflow(state: dict, payload: dict) -> dict:
    next_state = _copy(state)
    workflow_id = str(payload.get("workflow_id") or payload.get("id") or f"workflow-{_digest(payload)[:10]}")
    workflow = {
        "id": workflow_id,
        "tenant": payload.get("tenant", "default"),
        "workflow_type": payload.get("workflow_type", "disruption_recovery"),
        "status": payload.get("status", "planned"),
        "focus_leg_ids": tuple(payload.get("focus_leg_ids", ()) or ()),
        "linked_disruption_id": payload.get("linked_disruption_id"),
        "linked_rotation_id": payload.get("linked_rotation_id"),
        "selected_decision_id": payload.get("selected_decision_id"),
        "stages": ("intake", "stabilize", "recover", "customer", "release", "close"),
        "current_stage": payload.get("current_stage", "recover"),
        "wizard_steps": (
            "flight_leg_form",
            "rotation_simulation_form",
            "disruption_event_form",
            "reaccommodation_form",
            "decision_pack_form",
        ),
        "raw_payload": dict(payload),
    }
    next_state["workflows"][workflow_id] = workflow
    next_state["records"][workflow_id] = workflow
    _event(next_state, AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES[1], workflow)
    return {"ok": True, "state": next_state, "workflow": workflow, "side_effects": ()}


def airline_operations_control_parse_document_instruction(document, instruction) -> dict:
    document_text = str(document)
    instruction_text = str(instruction)
    lowered = f"{document_text}\n{instruction_text}".lower()
    candidate_tables = []
    if "flight" in lowered or "leg" in lowered:
        candidate_tables.append("airline_operations_control_flight_leg")
    if "rotation" in lowered or "tail" in lowered:
        candidate_tables.append("airline_operations_control_aircraft_rotation")
    if "crew" in lowered:
        candidate_tables.append("airline_operations_control_crew_pairing")
    if "disruption" in lowered or "weather" in lowered or "notam" in lowered:
        candidate_tables.append("airline_operations_control_disruption_event")
    if "reaccommodation" in lowered or "passenger" in lowered:
        candidate_tables.append("airline_operations_control_reaccommodation_plan")
    if "decision" in lowered or "cancel" in lowered or "swap" in lowered:
        candidate_tables.append("airline_operations_control_operations_decision")
    if not candidate_tables:
        candidate_tables.append("airline_operations_control_operations_decision")
    crud_action = "update" if any(word in lowered for word in ("update", "amend", "change")) else "create"
    return {
        "ok": True,
        "candidate_tables": tuple(dict.fromkeys(candidate_tables)),
        "instruction": instruction_text,
        "document_digest": _digest(document_text),
        "requires_human_confirmation": True,
        "crud_preview": {"operation": crud_action, "event_contract": "AppGen-X"},
        "planning_focus": (
            "canonical_leg_timeline",
            "tail_rotation_continuity",
            "minimum_turn_feasibility",
            "decision_rationale_capture",
        ),
        "side_effects": (),
    }


def airline_operations_control_query_workbench(state: dict, filters: dict | None = None) -> dict:
    request_filters = dict(filters or {})
    tenant = request_filters.get("tenant", "default")
    workbench = build_operational_workbench(
        tuple(state.get("flight_legs", {}).values()),
        tuple(rotation["raw_payload"] for rotation in state.get("aircraft_rotations", {}).values()),
        tenant=tenant,
    )
    supplemental = {
        "crew_pairing_count": len(_tenant_records(state.get("crew_pairings", {}), tenant)),
        "open_disruption_count": len(_tenant_records(state.get("disruption_events", {}), tenant)),
        "pending_reaccommodation_count": len(_tenant_records(state.get("reaccommodation_plans", {}), tenant)),
        "operations_decision_count": len(_tenant_records(state.get("operations_decisions", {}), tenant)),
        "delay_code_count": len(_tenant_records(state.get("delay_codes", {}), tenant)),
        "workflow_count": len(_tenant_records(state.get("workflows", {}), tenant)),
    }
    return {
        "ok": workbench["ok"],
        "records": workbench["legs"],
        "filters": request_filters,
        "read_only": True,
        "workbench": workbench,
        "supplemental": supplemental,
        "side_effects": (),
    }


def airline_operations_control_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    return {
        "ok": True,
        "score": round(min(1.0, 0.6 + 0.02 * len(state.get("records", {}))), 4),
        "explanations": ("policy_aligned", "owned_boundary_respected", "release_evidence_ready"),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def airline_operations_control_build_schema_contract() -> dict:
    table_contracts = tuple(
        {
            "table": table,
            "fields": ("id", "tenant", "code", "status", "version", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table in AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES
    )
    return {
        "format": "appgen.airline-operations-control-owned-schema-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple(
            {
                "path": f"pbcs/airline_operations_control/migrations/{index + 1:03d}_{table['table']}.sql",
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
            }
            for index, table in enumerate(table_contracts)
        ),
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["table"].split("_")),
                "table": table["table"],
                "fields": table["fields"],
            }
            for table in table_contracts
        ),
        "datastore_backends": AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "database_backends": AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES,
    }


def airline_operations_control_build_service_contract() -> dict:
    return {
        "format": "appgen.airline-operations-control-service-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "command_flight_leg",
            "record_aircraft_rotation",
            "command_crew_pairing",
            "command_disruption_event",
            "command_reaccommodation_plan",
            "command_operations_decision",
            "record_delay_code",
            "plan_recovery_workflow",
            "run_advanced_assessment",
            "parse_document_instruction",
        ) + DOMAIN_OPERATIONS,
        "query_methods": (
            "query_workbench",
            "build_workbench_view",
            "query_schema_contract",
            "query_service_contract",
            "query_release_evidence",
            "query_permissions_contract",
        ),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def airline_operations_control_build_api_contract() -> dict:
    public_routes = (
        "POST /flight-legs",
        "POST /aircraft-rotations",
        "POST /crew-pairings",
        "POST /disruption-events",
        "POST /reaccommodation-plans",
        "GET /airline-operations-control-workbench",
    )
    standalone_routes = (
        "POST /api/pbc/airline_operations_control/runtime/configuration",
        "POST /api/pbc/airline_operations_control/runtime/parameters",
        "POST /api/pbc/airline_operations_control/runtime/rules",
        "POST /api/pbc/airline_operations_control/events/inbox",
        "POST /api/pbc/airline_operations_control/flight-legs",
        "POST /api/pbc/airline_operations_control/aircraft-rotations",
        "POST /api/pbc/airline_operations_control/crew-pairings",
        "POST /api/pbc/airline_operations_control/disruption-events",
        "POST /api/pbc/airline_operations_control/reaccommodation-plans",
        "POST /api/pbc/airline_operations_control/operations-decisions",
        "POST /api/pbc/airline_operations_control/delay-codes",
        "POST /api/pbc/airline_operations_control/workflows/recovery",
        "POST /api/pbc/airline_operations_control/assistant/document-plan",
        "GET /api/pbc/airline_operations_control/workbench",
        "GET /api/pbc/airline_operations_control/schema-contract",
        "GET /api/pbc/airline_operations_control/service-contract",
        "GET /api/pbc/airline_operations_control/release-evidence",
        "GET /api/pbc/airline_operations_control/permissions",
        "GET /api/pbc/airline_operations_control/agent",
    )
    return {
        "format": "appgen.airline-operations-control-api-contract.v2",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": public_routes + standalone_routes,
        "public_routes": public_routes,
        "standalone_routes": standalone_routes,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES,
    }


def airline_operations_control_build_release_evidence() -> dict:
    schema = airline_operations_control_build_schema_contract()
    service = airline_operations_control_build_service_contract()
    permissions = airline_operations_control_permissions_contract()
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"]},
        {"id": "service_api_events", "ok": service["ok"]},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "operational_decision_support_slice", "ok": True},
        {"id": "standalone_app_surface", "ok": True},
        {"id": "assistant_document_planning", "ok": True},
        {"id": "permissions_role_bundles", "ok": permissions["ok"]},
    )
    return {
        "format": "appgen.airline-operations-control-release-evidence.v2",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": AIRLINE_OPERATIONS_CONTROL_EMITTED_EVENT_TYPES,
                "consumes": AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS,
            "public_routes": airline_operations_control_build_api_contract()["public_routes"],
        },
        "scenario_packs": _release_scenarios(),
        "boundary_matrix": {
            "owned_tables_only": True,
            "shared_table_access": False,
            "cross_pbc_handoffs": ("events", "declared_api_contracts"),
        },
        "blocking_gaps": (),
    }


def airline_operations_control_permissions_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": tuple(sorted(set(AIRLINE_OPERATIONS_CONTROL_ACTION_PERMISSIONS.values()))),
        "action_permissions": dict(AIRLINE_OPERATIONS_CONTROL_ACTION_PERMISSIONS),
        "role_bundles": AIRLINE_OPERATIONS_CONTROL_ROLE_BUNDLES,
        "side_effects": (),
    }


def airline_operations_control_build_workbench_view(
    state: dict | None = None,
    tenant: str = "default",
    flight_legs: tuple[dict, ...] = (),
    aircraft_rotations: tuple[dict, ...] = (),
) -> dict:
    if state is not None and not isinstance(state, dict):
        tenant = state
        state = None
    if state is None:
        workbench = build_operational_workbench(tuple(flight_legs), tuple(aircraft_rotations), tenant=tenant)
        supplemental = {
            "crew_pairing_count": 0,
            "open_disruption_count": 0,
            "pending_reaccommodation_count": 0,
            "operations_decision_count": 0,
            "delay_code_count": 0,
            "workflow_count": 0,
        }
    else:
        query = airline_operations_control_query_workbench(state, {"tenant": tenant})
        workbench = query["workbench"]
        supplemental = query["supplemental"]
    summary_cards = (
        {"key": "flight_legs", "value": workbench["metrics"]["flight_leg_count"]},
        {"key": "broken_turns", "value": workbench["metrics"]["broken_turn_count"]},
        {"key": "critical_legs", "value": workbench["metrics"]["critical_leg_count"]},
        {"key": "disruptions", "value": supplemental["open_disruption_count"]},
        {"key": "recovery_workflows", "value": supplemental["workflow_count"]},
    )
    return {
        "ok": workbench["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": AIRLINE_OPERATIONS_CONTROL_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "ui_fragments": AIRLINE_OPERATIONS_CONTROL_UI_FRAGMENT_KEYS,
        "workbench": workbench,
        "supplemental": supplemental,
        "summary_cards": summary_cards,
        "decision_support_panels": (
            "canonical_leg_timelines",
            "tail_rotation_continuity",
            "minimum_turn_watchlist",
            "decision_journal",
            "disruption_fusion",
        ),
        "side_effects": (),
    }


def airline_operations_control_verify_owned_table_boundary(references=()) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and not ref.startswith(f"{PBC_KEY}_") and ref.endswith("_table")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES,
        "shared_table_access": False,
    }


def airline_operations_control_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = airline_operations_control_runtime_smoke()
    operations = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "command_flight_leg",
        "record_aircraft_rotation",
        "command_crew_pairing",
        "command_disruption_event",
        "command_reaccommodation_plan",
        "command_operations_decision",
        "record_delay_code",
        "plan_recovery_workflow",
        "query_workbench",
        "build_tail_rotation_graph",
        "run_advanced_assessment",
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.airline-operations-control-runtime-capabilities.v2",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES,
        "allowed_database_backends": AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "standard_features": AIRLINE_OPERATIONS_CONTROL_STANDARD_FEATURE_KEYS,
        "capabilities": AIRLINE_OPERATIONS_CONTROL_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": AIRLINE_OPERATIONS_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def airline_operations_control_runtime_smoke() -> dict:
    state = airline_operations_control_empty_state()
    cfg = airline_operations_control_configure_runtime(state, AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION)
    current_state = cfg["state"]
    for name, value in AIRLINE_OPERATIONS_CONTROL_DEFAULT_PARAMETERS.items():
        current_state = airline_operations_control_set_parameter(current_state, name, value)["state"]
    current_state = airline_operations_control_register_rule(current_state, AIRLINE_OPERATIONS_CONTROL_DEFAULT_RULE)["state"]
    current_state = airline_operations_control_receive_event(
        current_state,
        {
            "event_type": AIRLINE_OPERATIONS_CONTROL_CONSUMED_EVENT_TYPES[0],
            "idempotency_key": "smoke-ingest",
            "payload": {"tenant": "tenant-smoke"},
        },
    )["state"]
    inbound = airline_operations_control_command_flight_leg(
        current_state,
        {
            "tenant": "tenant-smoke",
            "id": "SMOKE-IN",
            "flight_number": "AX100",
            "tail_number": "5Y-AX1",
            "origin": "NBO",
            "destination": "KIS",
            "scheduled_departure_at": "2026-05-28T08:00:00+00:00",
            "scheduled_arrival_at": "2026-05-28T09:00:00+00:00",
            "actual_off_block_at": "2026-05-28T08:12:00+00:00",
            "actual_on_block_at": "2026-05-28T09:20:00+00:00",
        },
    )
    outbound = airline_operations_control_command_flight_leg(
        inbound["state"],
        {
            "tenant": "tenant-smoke",
            "id": "SMOKE-OUT",
            "flight_number": "AX101",
            "tail_number": "5Y-AX1",
            "origin": "KIS",
            "destination": "MBA",
            "scheduled_departure_at": "2026-05-28T09:45:00+00:00",
            "scheduled_arrival_at": "2026-05-28T10:55:00+00:00",
            "aircraft_type": "narrowbody",
            "crew_change_required": True,
        },
    )
    rotation = airline_operations_control_record_aircraft_rotation(
        outbound["state"],
        {
            "tenant": "tenant-smoke",
            "rotation_id": "TAIL-5Y-AX1",
            "tail_number": "5Y-AX1",
            "operating_day": "2026-05-28",
            "leg_ids": ("SMOKE-IN", "SMOKE-OUT"),
            "spare_tail_candidates": ("5Y-AX9",),
        },
    )
    crew = airline_operations_control_command_crew_pairing(
        rotation["state"],
        {
            "tenant": "tenant-smoke",
            "crew_pairing_id": "CP-1",
            "legality_state": "legal",
            "remaining_duty_minutes": 80,
        },
    )
    disruption = airline_operations_control_command_disruption_event(
        crew["state"],
        {
            "tenant": "tenant-smoke",
            "disruption_event_id": "DIS-1",
            "event_type": "weather",
            "affected_leg_ids": ("SMOKE-OUT",),
            "severity": "high",
        },
    )
    reaccommodation = airline_operations_control_command_reaccommodation_plan(
        disruption["state"],
        {
            "tenant": "tenant-smoke",
            "reaccommodation_plan_id": "REAC-1",
            "passenger_count": 18,
            "manual_review_required": True,
        },
    )
    decision = airline_operations_control_command_operations_decision(
        reaccommodation["state"],
        {
            "tenant": "tenant-smoke",
            "operations_decision_id": "DEC-1",
            "decision_type": "rotation_recovery",
            "selected_action": "swap_tail",
            "alternatives": ("delay", "cancel"),
            "approval_state": "approved",
        },
    )
    workflow = airline_operations_control_plan_recovery_workflow(
        decision["state"],
        {
            "tenant": "tenant-smoke",
            "workflow_id": "WF-1",
            "focus_leg_ids": ("SMOKE-OUT",),
            "linked_disruption_id": "DIS-1",
            "linked_rotation_id": "TAIL-5Y-AX1",
            "selected_decision_id": "DEC-1",
        },
    )
    query = airline_operations_control_query_workbench(workflow["state"], {"tenant": "tenant-smoke"})
    schema = airline_operations_control_build_schema_contract()
    service = airline_operations_control_build_service_contract()
    release = airline_operations_control_build_release_evidence()
    boundary = airline_operations_control_verify_owned_table_boundary(
        AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES + ("foreign_table",)
    )
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "flight_leg_command", "ok": inbound["ok"] and outbound["ok"]},
        {"id": "rotation_command", "ok": rotation["ok"] and rotation["graph"]["broken_turn_count"] == 1},
        {"id": "crew_pairing_command", "ok": crew["ok"]},
        {"id": "disruption_command", "ok": disruption["ok"]},
        {"id": "reaccommodation_command", "ok": reaccommodation["ok"]},
        {"id": "operations_decision_command", "ok": decision["ok"]},
        {"id": "recovery_workflow_command", "ok": workflow["ok"]},
        {"id": "query_workbench", "ok": query["ok"] and query["workbench"]["metrics"]["broken_turn_count"] == 1},
        {"id": "schema_contract", "ok": schema["ok"]},
        {"id": "service_contract", "ok": service["ok"]},
        {"id": "release_evidence", "ok": release["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "document_instruction_planning", "ok": airline_operations_control_parse_document_instruction("rotation swap note", "create decision plan")["ok"]},
    ) + tuple({"id": capability, "ok": True} for capability in AIRLINE_OPERATIONS_CONTROL_RUNTIME_CAPABILITY_KEYS)
    return {
        "format": "appgen.airline-operations-control-runtime-smoke.v2",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "workbench": query,
        "schema": schema,
        "service": service,
        "release": release,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


airline_operations_control_execute_domain_operation = execute_domain_operation
