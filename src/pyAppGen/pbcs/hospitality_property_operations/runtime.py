"""Executable runtime contract for the hospitality_property_operations PBC."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from . import agent as agent_module
from . import config as config_module
from . import events as events_module
from . import handlers as handlers_module
from . import routes as routes_module
from . import services as services_module
from . import ui as ui_module
from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_CONSUMED_EVENTS,
    DOMAIN_EMITTED_EVENTS,
    DOMAIN_OPERATIONS,
    calculate_overbooking_risk,
    domain_depth_contract,
    domain_depth_smoke_test,
    execute_domain_operation,
)
from .models import OWNED_SCHEMA, OWNED_TABLES, BUSINESS_TABLES, standalone_model_contract, standalone_store_smoke_test
from .permissions import permission_manifest
from .seed_data import seed_plan
from .standalone import hospitality_property_operations_standalone_app_contract, hospitality_property_operations_standalone_app_smoke

PBC_KEY = "hospitality_property_operations"
HOSPITALITY_PROPERTY_OPERATIONS_OWNED_TABLES = OWNED_TABLES
HOSPITALITY_PROPERTY_OPERATIONS_RUNTIME_TABLES = OWNED_TABLES
HOSPITALITY_PROPERTY_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
HOSPITALITY_PROPERTY_OPERATIONS_REQUIRED_EVENT_TOPIC = "pbc.hospitality_property_operations.events"
HOSPITALITY_PROPERTY_OPERATIONS_EMITTED_EVENT_TYPES = DOMAIN_EMITTED_EVENTS
HOSPITALITY_PROPERTY_OPERATIONS_CONSUMED_EVENT_TYPES = DOMAIN_CONSUMED_EVENTS
HOSPITALITY_PROPERTY_OPERATIONS_STANDARD_FEATURE_KEYS = (
    "room_inventory_management",
    "reservation_lifecycle",
    "guest_stay_lifecycle",
    "housekeeping_dispatch",
    "guest_request_sla",
    "occupancy_snapshotting",
    "rate_fence_controls",
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
    "standalone_one_pbc_app",
)
HOSPITALITY_PROPERTY_OPERATIONS_RUNTIME_CAPABILITY_KEYS = tuple(DOMAIN_ADVANCED_CAPABILITIES)
HOSPITALITY_PROPERTY_OPERATIONS_UI_FRAGMENT_KEYS = (
    "HospitalityPropertyOperationsWorkbench",
    "HospitalityPropertyOperationsDetail",
    "HospitalityPropertyOperationsAssistantPanel",
)
HOSPITALITY_PROPERTY_OPERATIONS_BUSINESS_TABLES = BUSINESS_TABLES


def hospitality_property_operations_empty_state():
    return {"configuration": {}, "parameters": {}, "rules": {}, "schema_extensions": {}, "events": [], "idempotency_keys": set()}


def _copy(state):
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def hospitality_property_operations_configure_runtime(state, config):
    next_state = _copy(state)
    validation = config_module.validate_configuration(config)
    next_state["configuration"] = dict(validation["configuration"])
    next_state["configuration"]["event_contract"] = "AppGen-X"
    next_state["configuration"]["stream_engine_picker_visible"] = False
    return {"ok": validation["ok"], "state": next_state, "configuration": next_state["configuration"], "side_effects": ()}


def hospitality_property_operations_set_parameter(state, name, value):
    next_state = _copy(state)
    parameter = config_module.set_parameter(name, value)
    if parameter["ok"]:
        next_state["parameters"][name] = {"name": name, "value": value, "bounded": True}
    return {"ok": parameter["ok"], "state": next_state, "parameter": parameter, "side_effects": ()}


def hospitality_property_operations_register_rule(state, rule):
    next_state = _copy(state)
    compiled = config_module.compile_rule(rule)
    if compiled["ok"]:
        next_state["rules"][rule["rule_id"]] = compiled
    return {"ok": compiled["ok"], "state": next_state, "rule": compiled, "side_effects": ()}


def hospitality_property_operations_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in HOSPITALITY_PROPERTY_OPERATIONS_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {"ok": True, "state": next_state, "table": owned_name, "fields": dict(fields), "side_effects": ()}


def hospitality_property_operations_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or repr(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in HOSPITALITY_PROPERTY_OPERATIONS_CONSUMED_EVENT_TYPES:
        next_state["events"].append({"event": dict(event), "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event"})
        return {"ok": False, "duplicate": False, "state": next_state, "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event", "side_effects": ()}
    next_state["events"].append(dict(event))
    return {"ok": True, "duplicate": False, "state": next_state, "side_effects": ()}


def hospitality_property_operations_command_room_inventory(state, payload):
    next_state = _copy(state)
    next_state["last_room_command"] = dict(payload)
    return {
        "ok": True,
        "state": next_state,
        "record": {"id": payload.get("room_id") or payload.get("room_number"), "payload": dict(payload)},
        "side_effects": (),
    }


def hospitality_property_operations_query_workbench(state, filters=None):
    return {"ok": True, "filters": dict(filters or {}), "read_only": True, "records": tuple(state.get("events", ())), "side_effects": ()}


def hospitality_property_operations_run_advanced_assessment(state, payload=None):
    payload = dict(payload or {})
    score = calculate_overbooking_risk(
        {
            "available_rooms": payload.get("available_rooms", 10),
            "arrivals_pending": payload.get("arrivals_pending", 8),
            "blocked_rooms": payload.get("blocked_rooms", 1),
        }
    )
    return {"ok": True, "score": score["risk_score"], "risk_band": score["risk_band"], "payload": payload, "side_effects": ()}


def hospitality_property_operations_parse_document_instruction(document, instruction):
    return agent_module.document_instruction_plan(document, instruction)


def hospitality_property_operations_build_schema_contract():
    model_contract = standalone_model_contract()
    return {
        "format": "appgen.hospitality-property-operations-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": OWNED_SCHEMA["tables"],
        "relationships": tuple(
            relationship
            for table in OWNED_SCHEMA["tables"]
            for relationship in table.get("relationships", ())
        ),
        "migrations": (
            {
                "path": "pbcs/hospitality_property_operations/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": HOSPITALITY_PROPERTY_OPERATIONS_OWNED_TABLES,
                "backend_allowlist": HOSPITALITY_PROPERTY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": model_contract["models"],
        "datastore_backends": HOSPITALITY_PROPERTY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": HOSPITALITY_PROPERTY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": HOSPITALITY_PROPERTY_OPERATIONS_OWNED_TABLES,
    }


def hospitality_property_operations_build_service_contract():
    contracts = services_module.service_operation_contracts()
    standalone = services_module.standalone_service_operation_contracts()
    return {
        "format": "appgen.hospitality-property-operations-service-contract.v1",
        "ok": contracts["ok"] and standalone["ok"],
        "pbc": PBC_KEY,
        "command_methods": contracts["command_operations"],
        "query_methods": contracts["query_operations"],
        "workflow_methods": tuple(item["name"] for item in ui_module.hospitality_property_operations_standalone_workbench_blueprint()["wizards"]),
        "standalone_operations": standalone["operations"],
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def hospitality_property_operations_build_api_contract():
    route_contracts = routes_module.api_route_contracts()
    return {
        "format": "appgen.hospitality-property-operations-api-contract.v1",
        "ok": route_contracts["ok"],
        "pbc": PBC_KEY,
        "routes": route_contracts["routes"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": HOSPITALITY_PROPERTY_OPERATIONS_OWNED_TABLES,
    }


def hospitality_property_operations_build_release_evidence():
    docs = {
        "README.md": Path(__file__).with_name("README.md").exists(),
        "SPECIFICATION.md": Path(__file__).with_name("SPECIFICATION.md").exists(),
        "RELEASE_EVIDENCE.md": Path(__file__).with_name("RELEASE_EVIDENCE.md").exists(),
        "implementation-status.md": Path(__file__).with_name("implementation-status.md").exists(),
    }
    standalone_contract = hospitality_property_operations_standalone_app_contract()
    standalone_smoke = hospitality_property_operations_standalone_app_smoke()
    checks = (
        {"id": "schema_models_migrations", "ok": hospitality_property_operations_build_schema_contract()["ok"]},
        {"id": "service_api_events", "ok": hospitality_property_operations_build_service_contract()["ok"] and hospitality_property_operations_build_api_contract()["ok"] and events_module.event_contract_manifest()["ok"]},
        {"id": "handlers_ui_agent", "ok": handlers_module.handler_manifest()["ok"] and ui_module.hospitality_property_operations_ui_contract()["ok"] and agent_module.agent_skill_manifest()["ok"]},
        {"id": "governance", "ok": config_module.governance_smoke_test()["ok"] and permission_manifest()["ok"] and seed_plan()["ok"]},
        {"id": "documentation", "ok": all(docs.values())},
        {"id": "standalone_app", "ok": standalone_contract["ok"] and standalone_smoke["ok"]},
    )
    blocking_gaps = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.hospitality-property-operations-release-evidence.v1",
        "ok": not blocking_gaps,
        "pbc": PBC_KEY,
        "checks": checks,
        "documentation": {"ok": all(docs.values()), "artifacts": docs},
        "standalone_app": standalone_smoke,
        "generated_artifacts": {
            "migrations": hospitality_property_operations_build_schema_contract()["migrations"],
            "models": hospitality_property_operations_build_schema_contract()["models"],
            "events": events_module.event_contract_manifest(),
            "handlers": ("dispatch_event",),
            "ui": HOSPITALITY_PROPERTY_OPERATIONS_UI_FRAGMENT_KEYS,
        },
        "blocking_gaps": blocking_gaps,
    }


def hospitality_property_operations_permissions_contract():
    return permission_manifest()


def hospitality_property_operations_build_workbench_view(tenant="default"):
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": HOSPITALITY_PROPERTY_OPERATIONS_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "ui_fragments": HOSPITALITY_PROPERTY_OPERATIONS_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def hospitality_property_operations_verify_owned_table_boundary(references=()):
    invalid = tuple(ref for ref in references if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_"))
    return {"ok": not invalid, "pbc": PBC_KEY, "invalid_references": invalid, "allowed_tables": HOSPITALITY_PROPERTY_OPERATIONS_OWNED_TABLES, "shared_table_access": False}


def hospitality_property_operations_runtime_capabilities():
    smoke = hospitality_property_operations_runtime_smoke()
    domain = domain_depth_contract()
    return {
        "format": "appgen.hospitality-property-operations-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": HOSPITALITY_PROPERTY_OPERATIONS_OWNED_TABLES,
        "allowed_database_backends": HOSPITALITY_PROPERTY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": HOSPITALITY_PROPERTY_OPERATIONS_STANDARD_FEATURE_KEYS,
        "capabilities": HOSPITALITY_PROPERTY_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        "operations": (
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
            "command_room_inventory",
            "query_workbench",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + DOMAIN_OPERATIONS,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": HOSPITALITY_PROPERTY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def hospitality_property_operations_runtime_smoke():
    state = hospitality_property_operations_empty_state()
    cfg = hospitality_property_operations_configure_runtime(state, {"database_backend": "postgresql", "event_topic": HOSPITALITY_PROPERTY_OPERATIONS_REQUIRED_EVENT_TOPIC, "workbench_limit": 50})
    parameter = hospitality_property_operations_set_parameter(cfg["state"], "workbench_limit", 50)
    rule = hospitality_property_operations_register_rule(parameter["state"], {"rule_id": "room_sellable_state", "scope": "property"})
    event = hospitality_property_operations_receive_event(rule["state"], {"event_type": HOSPITALITY_PROPERTY_OPERATIONS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke"})
    duplicate = hospitality_property_operations_receive_event(event["state"], {"event_type": HOSPITALITY_PROPERTY_OPERATIONS_CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke"})
    dead = hospitality_property_operations_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"})
    command = hospitality_property_operations_command_room_inventory(dead["state"], {"tenant": "tenant-smoke", "room_id": "rm_smoke"})
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": parameter["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": event["ok"]},
        {"id": "duplicate_event", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "command_room_inventory", "ok": command["ok"]},
        {"id": "schema_contract", "ok": hospitality_property_operations_build_schema_contract()["ok"]},
        {"id": "service_contract", "ok": hospitality_property_operations_build_service_contract()["ok"]},
        {"id": "api_contract", "ok": hospitality_property_operations_build_api_contract()["ok"]},
        {"id": "release_evidence", "ok": hospitality_property_operations_build_release_evidence()["ok"]},
        {"id": "route_smoke", "ok": routes_module.smoke_test()["ok"]},
        {"id": "service_smoke", "ok": services_module.smoke_test()["ok"]},
        {"id": "event_smoke", "ok": events_module.smoke_test()["ok"]},
        {"id": "handler_smoke", "ok": handlers_module.smoke_test()["ok"]},
        {"id": "governance_smoke", "ok": config_module.smoke_test()["ok"]},
        {"id": "ui_smoke", "ok": ui_module.smoke_test()["ok"]},
        {"id": "agent_smoke", "ok": agent_module.smoke_test()["ok"]},
        {"id": "model_smoke", "ok": standalone_store_smoke_test()["ok"]},
        {"id": "standalone_app_smoke", "ok": hospitality_property_operations_standalone_app_smoke()["ok"]},
        {"id": "domain_depth_smoke", "ok": domain_depth_smoke_test()["ok"]},
    )
    return {"format": "appgen.hospitality-property-operations-runtime-smoke.v1", "ok": all(check["ok"] for check in checks), "checks": checks, "configuration": cfg, "command": command, "schema": hospitality_property_operations_build_schema_contract(), "side_effects": ()}


hospitality_property_operations_execute_domain_operation = execute_domain_operation


# Improve1 hospitality hotel control extension.
from .hospitality_control import improve1_hospitality_control_contract as hospitality_property_operations_improve1_hospitality_control_contract

_HOSPITALITY_PROPERTY_OPERATIONS_BASE_RUNTIME_CAPABILITIES = hospitality_property_operations_runtime_capabilities
_HOSPITALITY_PROPERTY_OPERATIONS_BASE_RELEASE_EVIDENCE = hospitality_property_operations_build_release_evidence


def hospitality_property_operations_build_release_evidence():
    evidence = dict(_HOSPITALITY_PROPERTY_OPERATIONS_BASE_RELEASE_EVIDENCE())
    hospitality_control = hospitality_property_operations_improve1_hospitality_control_contract()
    checks = tuple(evidence.get('checks', ())) + (
        {'id': 'improve1_hospitality_control', 'ok': hospitality_control['ok']},
        {'id': 'arrival_to_room_ready_release', 'ok': hospitality_control['capability_count'] == 50 and hospitality_control['event_contract'] == 'AppGen-X'},
    )
    return {**evidence, 'ok': evidence.get('ok') is True and all(check['ok'] for check in checks), 'checks': checks, 'hospitality_control': hospitality_control, 'blocking_gaps': tuple(check for check in checks if not check['ok'])}


def hospitality_property_operations_runtime_capabilities():
    runtime = dict(_HOSPITALITY_PROPERTY_OPERATIONS_BASE_RUNTIME_CAPABILITIES())
    hospitality_control = hospitality_property_operations_improve1_hospitality_control_contract()
    return {
        **runtime,
        'ok': runtime.get('ok') is True and hospitality_control['ok'],
        'hospitality_control': hospitality_control,
        'improve1_capabilities': hospitality_control['capabilities'],
        'operations': tuple(dict.fromkeys(tuple(runtime.get('operations', ())) + ('improve1_hospitality_control_contract', 'evaluate_hospitality_control'))),
        'owned_tables': tuple(dict.fromkeys(tuple(runtime.get('owned_tables', ())) + tuple(hospitality_control['owned_tables']))),
        'allowed_database_backends': hospitality_control['allowed_database_backends'],
        'event_contract': hospitality_control['event_contract'],
        'required_event_topic': hospitality_control['required_event_topic'],
        'stream_engine_picker_visible': False,
        'side_effects': (),
    }
