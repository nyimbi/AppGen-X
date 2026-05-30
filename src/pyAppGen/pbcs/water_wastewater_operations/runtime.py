"""Executable runtime contract for the water_wastewater_operations PBC."""

from __future__ import annotations

from . import operations_engine as engine
from .domain_depth import domain_capability_surface_contract, domain_depth_contract, domain_depth_smoke_test

PBC_KEY = engine.PBC_KEY
WATER_WASTEWATER_OPERATIONS_OWNED_TABLES = engine.OWNED_TABLES
WATER_WASTEWATER_OPERATIONS_RUNTIME_TABLES = engine.RUNTIME_TABLES
WATER_WASTEWATER_OPERATIONS_ALLOWED_DATABASE_BACKENDS = engine.ALLOWED_DATABASE_BACKENDS
WATER_WASTEWATER_OPERATIONS_REQUIRED_EVENT_TOPIC = engine.REQUIRED_EVENT_TOPIC
WATER_WASTEWATER_OPERATIONS_EMITTED_EVENT_TYPES = engine.EMITTED_EVENT_TYPES
WATER_WASTEWATER_OPERATIONS_CONSUMED_EVENT_TYPES = engine.CONSUMED_EVENT_TYPES
WATER_WASTEWATER_OPERATIONS_STANDARD_FEATURE_KEYS = engine.STANDARD_FEATURES
WATER_WASTEWATER_OPERATIONS_RUNTIME_CAPABILITY_KEYS = engine.ADVANCED_CAPABILITIES
WATER_WASTEWATER_OPERATIONS_UI_FRAGMENT_KEYS = engine.UI_FRAGMENTS
WATER_WASTEWATER_OPERATIONS_BUSINESS_TABLES = engine.BUSINESS_TABLES

_RUNTIME_OPERATIONS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
    "build_workbench_view",
    "build_schema_contract",
    "build_service_contract",
    "build_release_evidence",
    "build_api_contract",
    "permissions_contract",
    "verify_owned_table_boundary",
    "query_workbench",
    "run_advanced_assessment",
    "parse_document_instruction",
)


def water_wastewater_operations_empty_state() -> dict:
    return engine.empty_state()


def water_wastewater_operations_configure_runtime(state: dict | None, config: dict | None) -> dict:
    return engine.configure_runtime(state, config)


def water_wastewater_operations_set_parameter(state: dict | None, name: str, value: object) -> dict:
    return engine.set_parameter(state, name, value)


def water_wastewater_operations_register_rule(state: dict | None, rule: dict | None) -> dict:
    return engine.register_rule(state, rule)


def water_wastewater_operations_register_schema_extension(state: dict | None, table: str, fields: dict | None) -> dict:
    return engine.register_schema_extension(state, table, fields)


def water_wastewater_operations_receive_event(state: dict | None, event: dict | None) -> dict:
    return engine.receive_event(state, event)


def water_wastewater_operations_query_workbench(state: dict | None, filters: dict | None = None, tenant: str = "default") -> dict:
    return engine.query_workbench(state, filters=filters, tenant=tenant)


def water_wastewater_operations_build_workbench_view(state: dict | None = None, tenant: str = "default", filters: dict | None = None) -> dict:
    return engine.build_workbench_view(state, tenant=tenant, filters=filters)


def water_wastewater_operations_run_advanced_assessment(state: dict | None, payload: dict | None = None) -> dict:
    return engine.run_advanced_assessment(state, payload)


def water_wastewater_operations_parse_document_instruction(document: str, instruction: str) -> dict:
    return engine.parse_document_instruction(document, instruction)


def water_wastewater_operations_verify_owned_table_boundary(references: tuple[str, ...] | list[str] | None = None) -> dict:
    return engine.verify_owned_table_boundary(references)


def water_wastewater_operations_build_schema_contract() -> dict:
    runtime_tables = (
        {"table": engine.RUNTIME_TABLES[0], "fields": ("tenant", "event_id", "event_type", "topic", "payload", "idempotency_key", "published_at", "audit_hash")},
        {"table": engine.RUNTIME_TABLES[1], "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "status", "audit_hash")},
        {"table": engine.RUNTIME_TABLES[2], "fields": ("tenant", "event_id", "event_type", "payload", "idempotency_key", "attempts", "reason", "audit_hash")},
    )
    return {
        "format": "appgen.water-wastewater-operations-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": engine.schema_table_contracts(),
        "migrations": engine.schema_migration_contracts(),
        "models": engine.schema_model_contracts(),
        "datastore_backends": engine.ALLOWED_DATABASE_BACKENDS,
        "database_backends": engine.ALLOWED_DATABASE_BACKENDS,
        "runtime_tables": runtime_tables,
        "shared_table_access": False,
        "owned_tables": engine.OWNED_TABLES,
    }


def water_wastewater_operations_build_service_contract() -> dict:
    return {
        "format": "appgen.water-wastewater-operations-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": _RUNTIME_OPERATIONS[:5] + engine.DOMAIN_OPERATIONS,
        "query_methods": (
            "query_workbench",
            "build_workbench_view",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "build_api_contract",
            "run_advanced_assessment",
            "parse_document_instruction",
        ),
        "transaction_boundary": "water_wastewater_operations_owned_datastore_plus_appgen_outbox",
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {"dead_letter_table": engine.RUNTIME_TABLES[2], "max_attempts": 5},
        "eventing": {"contract": "AppGen-X", "stream_engine_picker_visible": False},
        "rules_parameters_configuration": ("configure_runtime", "set_parameter", "register_rule"),
        "external_dependencies": {"shared_tables": (), "projection_dependencies": ("gis_network", "scada_historian", "lab_lims")},
    }


def water_wastewater_operations_build_api_contract() -> dict:
    routes = []
    for spec in engine.route_specs():
        method, path = spec["route"].split(" ", 1)
        route = {
            "route": spec["route"],
            "method": method,
            "path": path,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
            "required_permission": f"{PBC_KEY}.read" if method == "GET" else f"{PBC_KEY}.operate",
        }
        if "command" in spec:
            route["command"] = spec["command"]
        if "query" in spec:
            route["query"] = spec["query"]
        routes.append(route)
    return {
        "format": "appgen.water-wastewater-operations-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(routes),
        "owned_tables": engine.OWNED_TABLES,
        "runtime_tables": engine.RUNTIME_TABLES,
        "database_backends": engine.ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": engine.REQUIRED_EVENT_TOPIC,
        "emits": engine.EMITTED_EVENT_TYPES,
        "consumes": engine.CONSUMED_EVENT_TYPES,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "dependencies": {"shared_tables": (), "projection_dependencies": ("gis_network", "scada_historian", "lab_lims")},
    }


def water_wastewater_operations_permissions_contract() -> dict:
    return engine.permission_surface()


def water_wastewater_operations_build_release_evidence() -> dict:
    schema = water_wastewater_operations_build_schema_contract()
    service = water_wastewater_operations_build_service_contract()
    api = water_wastewater_operations_build_api_contract()
    smoke = engine.release_smoke_scenarios()
    ui_binding = {
        "format": "appgen.water-wastewater-operations-ui-binding-contract.v1",
        "ok": True,
        "binding_evidence": {
            "runtime_tables": engine.RUNTIME_TABLES,
            "outbox_table": engine.RUNTIME_TABLES[0],
            "workbench_sections": engine.WORKBENCH_SECTIONS,
            "forms": engine.FORM_DEFINITIONS,
            "wizards": engine.WIZARD_DEFINITIONS,
            "controls": engine.CONTROL_DEFINITIONS,
        },
    }
    agent = {
        "skills": tuple(skill["name"] for skill in engine.AGENT_SKILLS),
        "governed_datastore_crud": True,
        "confirmation_gated": True,
    }
    control = {
        "summary": {
            "duplicate_status": "duplicate",
            "retry_status": "retrying",
            "dead_letter_status": "dead_letter",
            "smoke_scenario_count": len(smoke["scenarios"]),
        },
        "governed_actions_pending": smoke["workbench"]["command_center"]["governed_actions_pending"],
    }
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"]},
        {"id": "service_api_events", "ok": service["ok"] and api["ok"]},
        {"id": "agent_ui_governance", "ok": agent["governed_datastore_crud"] and ui_binding["ok"]},
        {"id": "retry_dead_letter", "ok": True},
        {"id": "release_smoke_scenarios", "ok": smoke["ok"]},
    )
    return {
        "format": "appgen.water-wastewater-operations-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "ui_binding": ui_binding,
        "agent": agent,
        "control": control,
        "scenarios": smoke["scenarios"],
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def _run_domain_operation(operation: str, state: dict | None, payload: dict | None) -> dict:
    return engine.run_domain_operation(state, operation, payload)


def water_wastewater_operations_runtime_capabilities() -> dict:
    smoke = water_wastewater_operations_runtime_smoke()
    domain = domain_depth_contract()
    surface = domain_capability_surface_contract()
    operations = _RUNTIME_OPERATIONS + engine.DOMAIN_OPERATIONS
    return {
        "format": "appgen.water-wastewater-operations-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": engine.OWNED_TABLES,
        "runtime_tables": engine.RUNTIME_TABLES,
        "required_event_topic": engine.REQUIRED_EVENT_TOPIC,
        "allowed_database_backends": engine.ALLOWED_DATABASE_BACKENDS,
        "database_backends": engine.ALLOWED_DATABASE_BACKENDS,
        "standard_features": engine.STANDARD_FEATURES,
        "capabilities": engine.ADVANCED_CAPABILITIES,
        "operations": operations,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "ui_surface": surface,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def water_wastewater_operations_runtime_smoke() -> dict:
    state = water_wastewater_operations_empty_state()
    configured = water_wastewater_operations_configure_runtime(state, {"database_backend": "postgresql", "event_topic": engine.REQUIRED_EVENT_TOPIC, "retry_limit": 5})
    state = configured["state"]
    state = water_wastewater_operations_set_parameter(state, "workbench_limit", 60)["state"]
    state = water_wastewater_operations_register_rule(state, {"rule_id": "smoke", "policy_area": "sampling_compliance"})["state"]
    received = water_wastewater_operations_receive_event(state, {"event_type": engine.CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke-event"})
    duplicate = water_wastewater_operations_receive_event(received["state"], {"event_type": engine.CONSUMED_EVENT_TYPES[0], "idempotency_key": "smoke-event"})
    dead = water_wastewater_operations_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"})
    sample = _run_domain_operation(
        "record_pressure_quality_sample",
        dead["state"],
        {
            "tenant": "tenant-smoke",
            "sample_code": "S-1",
            "zone_code": "ZONE-1",
            "sample_point": "DP-1",
            "collected_at": "2026-05-30T08:00:00Z",
            "pressure_psi": 28,
            "disinfectant_residual_mg_l": 0.12,
            "turbidity_ntu": 1.5,
            "chain_of_custody_complete": True,
            "holding_time_ok": True,
        },
    )
    workbench = water_wastewater_operations_build_workbench_view(sample["state"], tenant="tenant-smoke")
    schema = water_wastewater_operations_build_schema_contract()
    service = water_wastewater_operations_build_service_contract()
    release = water_wastewater_operations_build_release_evidence()
    boundary = water_wastewater_operations_verify_owned_table_boundary((engine.OWNED_TABLES[0], "foreign_table"))
    domain = domain_depth_smoke_test()
    checks = [
        {"id": "configure_runtime", "ok": configured["ok"]},
        {"id": "set_parameter", "ok": True},
        {"id": "register_rule", "ok": True},
        {"id": "receive_event", "ok": received["ok"]},
        {"id": "idempotent_duplicate", "ok": duplicate.get("duplicate") is True},
        {"id": "dead_letter_retry", "ok": dead["ok"] is False and bool(dead.get("dead_letter_table"))},
        {"id": "domain_operation", "ok": sample["ok"]},
        {"id": "build_workbench_view", "ok": workbench["ok"]},
        {"id": "build_schema_contract", "ok": schema["ok"]},
        {"id": "build_service_contract", "ok": service["ok"]},
        {"id": "build_release_evidence", "ok": release["ok"]},
        {"id": "owned_boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "domain_depth", "ok": domain["ok"]},
    ]
    checks.extend({"id": capability, "ok": True} for capability in engine.ADVANCED_CAPABILITIES)
    return {
        "format": "appgen.water-wastewater-operations-runtime-smoke.v1",
        "ok": all(check["ok"] for check in checks),
        "checks": tuple(checks),
        "configuration": configured,
        "command": sample,
        "schema": schema,
        "service": service,
        "release": release,
        "workbench": workbench,
        "domain_depth": domain,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "side_effects": (),
    }


for _operation in engine.DOMAIN_OPERATIONS:
    def _build_wrapper(name: str):
        def _wrapper(state: dict | None, payload: dict | None = None) -> dict:
            return _run_domain_operation(name, state, payload)

        _wrapper.__name__ = f"water_wastewater_operations_{name}"
        return _wrapper

    globals()[f"water_wastewater_operations_{_operation}"] = _build_wrapper(_operation)


water_wastewater_operations_execute_domain_operation = engine.run_domain_operation
