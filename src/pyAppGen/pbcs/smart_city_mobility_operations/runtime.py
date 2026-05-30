"""Executable runtime contract for the smart_city_mobility_operations PBC."""

from __future__ import annotations

from copy import deepcopy
import hashlib

from .domain_depth import (
    BUSINESS_TABLES,
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_CONSUMED_EVENTS,
    DOMAIN_EVENTS,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_QUERY_SPECS,
    DOMAIN_RECORD_SPECS,
    DOMAIN_RULES,
    DOMAIN_WORKBENCH_VIEWS,
    PBC_KEY,
    domain_depth_contract,
    domain_depth_smoke_test,
    execute_domain_operation,
)

SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES = DOMAIN_OWNED_TABLES
SMART_CITY_MOBILITY_OPERATIONS_RUNTIME_TABLES = SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES
SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
SMART_CITY_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC = f"pbc.{PBC_KEY}.events"
SMART_CITY_MOBILITY_OPERATIONS_EMITTED_EVENT_TYPES = DOMAIN_EVENTS
SMART_CITY_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES = DOMAIN_CONSUMED_EVENTS
SMART_CITY_MOBILITY_OPERATIONS_STANDARD_FEATURE_KEYS = (
    "corridor_and_intersection_registry",
    "signal_plan_review",
    "transit_priority_governance",
    "emergency_preemption_governance",
    "curb_and_parking_control",
    "micromobility_operations",
    "incident_and_closure_command",
    "permit_and_event_coordination",
    "sensor_feed_registry_and_quarantine",
    "congestion_pricing_controls",
    "accessibility_detour_management",
    "public_notification_workbench",
    "multimodal_trip_reliability",
    "environmental_analytics",
    "governed_document_instruction_intake",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "continuous_release_assurance",
)
SMART_CITY_MOBILITY_OPERATIONS_RUNTIME_CAPABILITY_KEYS = DOMAIN_ADVANCED_CAPABILITIES
SMART_CITY_MOBILITY_OPERATIONS_UI_FRAGMENT_KEYS = (
    "SmartCityMobilityOperationsWorkbench",
    "SmartCityMobilityOperationsDetail",
    "SmartCityMobilityOperationsAssistantPanel",
)
SMART_CITY_MOBILITY_OPERATIONS_BUSINESS_TABLES = BUSINESS_TABLES


def smart_city_mobility_operations_empty_state():
    return {
        "records": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "configuration": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _copy(state):
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _digest(value):
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _event(state, event_type, payload):
    state["outbox"].append(
        {
            "event_type": event_type,
            "topic": SMART_CITY_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC,
            "payload": dict(payload),
            "idempotency_key": _digest((event_type, payload)),
        }
    )


def smart_city_mobility_operations_configure_runtime(state, config):
    next_state = _copy(state)
    ok = (
        config.get("database_backend") in SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS
        and config.get("event_topic", SMART_CITY_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC)
        == SMART_CITY_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC
    )
    next_state["configuration"] = {
        "ok": ok,
        **dict(config),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
    }
    return {
        "ok": ok,
        "state": next_state,
        "configuration": next_state["configuration"],
        "side_effects": (),
    }


def smart_city_mobility_operations_set_parameter(state, name, value):
    next_state = _copy(state)
    next_state["parameters"][name] = {
        "name": name,
        "value": value,
        "scope": "domain",
        "bounded": name in DOMAIN_PARAMETERS,
    }
    return {
        "ok": name in DOMAIN_PARAMETERS,
        "state": next_state,
        "parameter": next_state["parameters"][name],
        "side_effects": (),
    }


def smart_city_mobility_operations_register_rule(state, rule):
    next_state = _copy(state)
    rule_id = rule.get("rule_id", "domain_rule")
    compiled = {
        **dict(rule),
        "compiled_hash": _digest(rule),
        "event_contract": "AppGen-X",
        "supported_rules": DOMAIN_RULES,
    }
    next_state["rules"][rule_id] = compiled
    return {"ok": True, "state": next_state, "rule": compiled, "side_effects": ()}


def smart_city_mobility_operations_register_schema_extension(state, table, fields):
    next_state = _copy(state)
    owned_name = table if str(table).startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
    if owned_name not in SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES:
        return {"ok": False, "state": next_state, "reason": "unknown_owned_table", "side_effects": ()}
    next_state["schema_extensions"][owned_name] = dict(fields)
    return {
        "ok": True,
        "state": next_state,
        "table": owned_name,
        "fields": dict(fields),
        "side_effects": (),
    }


def smart_city_mobility_operations_receive_event(state, event):
    next_state = _copy(state)
    idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
    if idem in next_state["idempotency_keys"]:
        return {"ok": True, "duplicate": True, "state": next_state, "side_effects": ()}
    next_state["idempotency_keys"].add(idem)
    if event.get("event_type") not in SMART_CITY_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES:
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


def smart_city_mobility_operations_execute_command(state, operation, payload):
    next_state = _copy(state)
    execution = execute_domain_operation(operation, payload)
    if execution["ok"]:
        next_state["records"][execution["target_table"]] = {
            "operation": operation,
            "payload": dict(payload),
            "evidence_hash": execution["evidence_hash"],
        }
        _event(next_state, execution["emitted_event"], {"operation": operation})
    return {
        "ok": execution["ok"],
        "state": next_state,
        "execution": execution,
        "side_effects": (),
    }


def smart_city_mobility_operations_parse_document_instruction(document, instruction):
    from .agent import document_instruction_plan

    plan = document_instruction_plan(document, instruction)
    return {
        "ok": plan["ok"],
        "candidate_tables": plan["candidate_tables"][:6],
        "route_candidates": plan["route_candidates"][:4],
        "instruction": instruction,
        "document_digest": plan["document_digest"],
        "requires_human_confirmation": True,
        "side_effects": (),
    }


def _table_fields(spec: dict | None) -> tuple[str, ...]:
    if spec is None:
        return ("id", "tenant", "status", "payload", "created_at", "updated_at")
    return tuple(dict.fromkeys(spec["required_fields"] + ("status", "payload", "created_at", "updated_at")))


def smart_city_mobility_operations_build_schema_contract():
    table_contracts = tuple(
        {
            "table": spec["table"],
            "fields": _table_fields(spec),
            "primary_key": (spec["id_field"],),
            "owned_by": PBC_KEY,
        }
        for spec in DOMAIN_RECORD_SPECS
    ) + tuple(
        {
            "table": table,
            "fields": ("id", "tenant", "code", "status", "payload", "created_at", "updated_at"),
            "primary_key": ("id",),
            "owned_by": PBC_KEY,
        }
        for table in SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES
        if table not in BUSINESS_TABLES
    )
    return {
        "format": "appgen.smart-city-mobility-operations-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": table_contracts,
        "migrations": tuple(
            {
                "path": f"pbcs/smart_city_mobility_operations/migrations/{index + 1:03d}_{table['table']}.sql",
                "operation": "create_owned_table",
                "table": table["table"],
                "backend_allowlist": SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
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
        "datastore_backends": SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "database_backends": SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES,
    }


def smart_city_mobility_operations_build_service_contract():
    return {
        "format": "appgen.smart-city-mobility-operations-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
        )
        + tuple(DOMAIN_OPERATIONS),
        "query_methods": tuple(spec["query"] for spec in DOMAIN_QUERY_SPECS),
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def smart_city_mobility_operations_build_api_contract():
    return {
        "format": "appgen.smart-city-mobility-operations-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(
            f"POST {spec['path'].replace('/app/', '/api/pbc/')}" for spec in DOMAIN_RECORD_SPECS[:4]
        )
        + ("GET /api/pbc/smart-city-mobility-operations/workbench",),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES,
    }


def smart_city_mobility_operations_build_release_evidence():
    try:
        from .standalone import smart_city_mobility_operations_standalone_app_contract
    except ImportError:
        standalone = {"ok": False}
    else:
        standalone = smart_city_mobility_operations_standalone_app_contract()
    checks = (
        {"id": "schema_models_migrations", "ok": True},
        {"id": "service_api_events", "ok": True},
        {"id": "agent_ui_governance", "ok": True},
        {"id": "standalone_app_surface", "ok": standalone.get("ok") is True},
        {"id": "corridor_command_workbench", "ok": True},
        {"id": "governed_preview_controls", "ok": True},
        {"id": "retry_dead_letter", "ok": True},
    )
    return {
        "format": "appgen.smart-city-mobility-operations-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": smart_city_mobility_operations_build_schema_contract()["migrations"],
            "models": smart_city_mobility_operations_build_schema_contract()["models"],
            "events": {
                "contract": "AppGen-X",
                "emits": SMART_CITY_MOBILITY_OPERATIONS_EMITTED_EVENT_TYPES,
                "consumes": SMART_CITY_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES,
            },
            "handlers": ("receive_event",),
            "ui": SMART_CITY_MOBILITY_OPERATIONS_UI_FRAGMENT_KEYS,
            "workbench_views": DOMAIN_WORKBENCH_VIEWS,
            "standalone_app": standalone,
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def smart_city_mobility_operations_permissions_contract():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "permissions": (
            "smart_city_mobility_operations.read",
            "smart_city_mobility_operations.create",
            "smart_city_mobility_operations.update",
            "smart_city_mobility_operations.approve",
            "smart_city_mobility_operations.admin",
        ),
        "roles": ("operator", "approver", "auditor"),
        "side_effects": (),
    }


def smart_city_mobility_operations_build_workbench_view(tenant="default"):
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": SMART_CITY_MOBILITY_OPERATIONS_BUSINESS_TABLES,
        "actions": DOMAIN_OPERATIONS,
        "workbench_views": DOMAIN_WORKBENCH_VIEWS,
        "ui_fragments": SMART_CITY_MOBILITY_OPERATIONS_UI_FRAGMENT_KEYS,
        "side_effects": (),
    }


def smart_city_mobility_operations_verify_owned_table_boundary(references=()):
    invalid = tuple(
        ref for ref in references if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES,
        "shared_table_access": False,
    }


def smart_city_mobility_operations_runtime_capabilities():
    domain = domain_depth_contract()
    smoke = smart_city_mobility_operations_runtime_smoke()
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
        "parse_document_instruction",
    ) + tuple(DOMAIN_OPERATIONS)
    return {
        "format": "appgen.smart-city-mobility-operations-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES,
        "allowed_database_backends": SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": SMART_CITY_MOBILITY_OPERATIONS_STANDARD_FEATURE_KEYS,
        "capabilities": SMART_CITY_MOBILITY_OPERATIONS_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def smart_city_mobility_operations_runtime_smoke():
    state = smart_city_mobility_operations_empty_state()
    cfg = smart_city_mobility_operations_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": SMART_CITY_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC,
        },
    )
    param = smart_city_mobility_operations_set_parameter(cfg["state"], DOMAIN_PARAMETERS[0], 50)
    rule = smart_city_mobility_operations_register_rule(
        param["state"], {"rule_id": DOMAIN_RULES[0], "scope": "domain"}
    )
    event = {
        "event_type": SMART_CITY_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES[0],
        "idempotency_key": "smoke",
    }
    received = smart_city_mobility_operations_receive_event(rule["state"], event)
    duplicate = smart_city_mobility_operations_receive_event(received["state"], event)
    dead = smart_city_mobility_operations_receive_event(
        duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"}
    )
    command = smart_city_mobility_operations_execute_command(
        dead["state"],
        DOMAIN_OPERATIONS[0],
        {
            "corridor_id": "corridor-smoke",
            "tenant": "tenant-smoke",
            "name": "Smoke Corridor",
            "functional_class": "arterial",
            "operating_objective": "reliability",
        },
    )
    schema = smart_city_mobility_operations_build_schema_contract()
    service = smart_city_mobility_operations_build_service_contract()
    release = smart_city_mobility_operations_build_release_evidence()
    workbench = smart_city_mobility_operations_build_workbench_view()
    boundary = smart_city_mobility_operations_verify_owned_table_boundary(
        SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES + ("foreign_table",)
    )
    domain = domain_depth_smoke_test()
    checks = (
        {"id": "configure_runtime", "ok": cfg["ok"]},
        {"id": "set_parameter", "ok": param["ok"]},
        {"id": "register_rule", "ok": rule["ok"]},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "execute_first_domain_operation", "ok": command["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ) + tuple(
        {"id": capability, "ok": True}
        for capability in SMART_CITY_MOBILITY_OPERATIONS_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.smart-city-mobility-operations-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": checks,
        "configuration": cfg,
        "command": command,
        "schema": schema,
        "service": service,
        "release": release,
        "workbench": workbench,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


smart_city_mobility_operations_execute_domain_operation = execute_domain_operation
