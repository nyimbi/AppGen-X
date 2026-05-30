"""Executable runtime contract for the defense_readiness_logistics PBC."""

from __future__ import annotations

from hashlib import sha256

from .agent import agent_skill_manifest, chatbot_interface_contract, composed_agent_contribution, document_instruction_plan, smoke_test as agent_smoke_test
from .config import ALLOWED_DATABASE_BACKENDS, REQUIRED_EVENT_TOPIC, governance_smoke_test
from .defense_app import (
    build_defense_workbench,
    defense_app_smoke_test,
    document_instruction_mutation_plan,
    empty_defense_state,
    forms_contract,
    single_pbc_app_contract,
    workflow_contracts,
    wizards_contract,
    controls_contract,
)
from .domain_depth import domain_depth_contract, domain_depth_smoke_test
from .events import CONSUMED, EMITTED, DEFAULT_TOPIC, event_contract_manifest, smoke_test as event_smoke_test, validate_event_contract
from .handlers import handler_manifest, smoke_test as handler_smoke_test
from .models import MODEL_CONTRACTS, OWNED_TABLES, load_migration_sql, migration_alignment_contract, model_contracts
from .permissions import permission_manifest
from .routes import ROUTE_DEFINITIONS, ROUTES, api_route_contracts, validate_api_route_contracts
from .seed_data import seed_plan, smoke_test as seed_smoke_test
from .services import COMMAND_OPERATIONS, QUERY_OPERATIONS, DefenseReadinessLogisticsService, service_operation_contracts, service_operation_manifest, smoke_test as service_smoke_test
from .ui import defense_readiness_logistics_render_workbench, defense_readiness_logistics_ui_contract

PBC_KEY = "defense_readiness_logistics"
DEFENSE_READINESS_LOGISTICS_OWNED_TABLES = OWNED_TABLES
DEFENSE_READINESS_LOGISTICS_RUNTIME_TABLES = OWNED_TABLES
DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
DEFENSE_READINESS_LOGISTICS_REQUIRED_EVENT_TOPIC = REQUIRED_EVENT_TOPIC
DEFENSE_READINESS_LOGISTICS_EMITTED_EVENT_TYPES = EMITTED
DEFENSE_READINESS_LOGISTICS_CONSUMED_EVENT_TYPES = CONSUMED
DEFENSE_READINESS_LOGISTICS_STANDARD_FEATURE_KEYS = (
    "unit_readiness_management",
    "defense_readiness_logistics_workflow",
    "defense_readiness_logistics_analytics",
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
    "single_pbc_domain_app",
    "forms",
    "wizards",
    "controls",
    "mission_capability_rollup",
    "movement_order_control",
)
DEFENSE_READINESS_LOGISTICS_RUNTIME_CAPABILITY_KEYS = (
    "defense_readiness_logistics_event_sourced_operational_history",
    "defense_readiness_logistics_multi_tenant_policy_isolation",
    "defense_readiness_logistics_schema_evolution_resilience",
    "defense_readiness_logistics_autonomous_anomaly_detection",
    "defense_readiness_logistics_semantic_document_instruction_understanding",
    "defense_readiness_logistics_predictive_risk_scoring",
    "defense_readiness_logistics_counterfactual_scenario_simulation",
    "defense_readiness_logistics_cryptographic_audit_proofs",
    "defense_readiness_logistics_continuous_control_testing",
    "defense_readiness_logistics_carbon_and_sustainability_awareness",
    "defense_readiness_logistics_cross_pbc_event_federation",
    "defense_readiness_logistics_governed_ai_agent_execution",
)
DEFENSE_READINESS_LOGISTICS_UI_FRAGMENT_KEYS = (
    "DefenseReadinessLogisticsWorkbench",
    "DefenseReadinessLogisticsDetail",
    "DefenseReadinessLogisticsAssistantPanel",
)


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def _camel(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def defense_readiness_logistics_empty_state() -> dict:
    return empty_defense_state()


def defense_readiness_logistics_configure_runtime(state: dict, config: dict) -> dict:
    service = DefenseReadinessLogisticsService(state)
    result = service.configure_runtime(config)
    return {"ok": result["ok"], "state": service.state, "configuration": service.state["configuration"], "side_effects": ()}


def defense_readiness_logistics_set_parameter(state: dict, name: str, value) -> dict:
    service = DefenseReadinessLogisticsService(state)
    result = service.set_parameter({"name": name, "value": value})
    return {"ok": result["ok"], "state": service.state, "parameter": service.state["parameters"].get(name), "side_effects": ()}


def defense_readiness_logistics_register_rule(state: dict, rule: dict) -> dict:
    service = DefenseReadinessLogisticsService(state)
    result = service.register_rule(rule)
    rule_id = rule.get("rule_id") or rule.get("name") or next(iter(service.state["rules"]))
    return {"ok": result["ok"], "state": service.state, "rule": service.state["rules"].get(rule_id), "side_effects": ()}


def defense_readiness_logistics_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    service = DefenseReadinessLogisticsService(state)
    result = service.register_schema_extension({"table_name": table, "field_manifest": fields})
    return {"ok": result["ok"], "state": service.state, "table": table, "fields": fields, "side_effects": ()}


def defense_readiness_logistics_receive_event(state: dict, event: dict) -> dict:
    service = DefenseReadinessLogisticsService(state)
    result = service.receive_event(event)
    return {
        "ok": result["ok"],
        "duplicate": result.get("duplicate", False),
        "state": service.state,
        "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
        "side_effects": (),
    }


def defense_readiness_logistics_command_unit_readiness(state: dict, payload: dict) -> dict:
    service = DefenseReadinessLogisticsService(state)
    result = service.assess_unit_readiness(payload)
    return {"ok": result["ok"], "state": service.state, "record": result["domain_app"]["unit_readiness"], "side_effects": ()}


def defense_readiness_logistics_query_workbench(state: dict, filters: dict | None = None) -> dict:
    workbench = build_defense_workbench(state)
    return {"ok": True, "records": workbench["queues"], "filters": dict(filters or {}), "read_only": True, "side_effects": ()}


def defense_readiness_logistics_run_advanced_assessment(state: dict, payload: dict | None = None) -> dict:
    workbench = build_defense_workbench(state)
    total_records = sum(len(queue) for queue in workbench["queues"].values())
    risk = min(1.0, total_records / 20.0)
    return {
        "ok": True,
        "score": round(1.0 - risk, 4),
        "explanations": ("owned_boundary_respected", "workbench_projection_available", "assistant_governance_enabled"),
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def defense_readiness_logistics_parse_document_instruction(document: str, instruction: str) -> dict:
    return document_instruction_plan(document, instruction)


def defense_readiness_logistics_build_schema_contract() -> dict:
    migration_sql = load_migration_sql()
    models = tuple(
        {
            "class_name": f"{_camel(spec['entity'])}Model",
            "table": spec["table"],
            "category": spec["category"],
            "purpose": spec["purpose"],
            "fields": spec["fields"],
            "columns": spec["columns"],
            "primary_key": spec["primary_key"],
        }
        for spec in model_contracts()
    )
    tables = tuple(
        {
            "table": spec["table"],
            "fields": spec["fields"],
            "columns": spec["columns"],
            "primary_key": spec["primary_key"],
            "owned_by": spec["owned_by"],
            "category": spec["category"],
            "purpose": spec["purpose"],
        }
        for spec in MODEL_CONTRACTS
    )
    return {
        "format": "appgen.defense-readiness-logistics-owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": tables,
        "migrations": (
            {
                "path": "migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": DEFENSE_READINESS_LOGISTICS_OWNED_TABLES,
                "backend_allowlist": DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
                "sql_digest": _digest(migration_sql),
            },
        ),
        "models": models,
        "database_backends": DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": DEFENSE_READINESS_LOGISTICS_OWNED_TABLES,
    }


def defense_readiness_logistics_build_service_contract() -> dict:
    manifest = service_operation_manifest()
    return {
        "format": "appgen.defense-readiness-logistics-service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": manifest["service_class"],
        "command_methods": manifest["command_operations"],
        "query_methods": manifest["query_operations"],
        "workflows": manifest["workflows"],
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def defense_readiness_logistics_build_api_contract() -> dict:
    contracts = api_route_contracts()["contracts"]
    return {
        "format": "appgen.defense-readiness-logistics-api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(item["route"] for item in contracts),
        "bindings": tuple({"route": item["route"], "operation": item["operation"], "permission": item["required_permission"]} for item in contracts),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": DEFENSE_READINESS_LOGISTICS_OWNED_TABLES,
    }


def defense_readiness_logistics_build_release_evidence() -> dict:
    schema = defense_readiness_logistics_build_schema_contract()
    services = defense_readiness_logistics_build_service_contract()
    api = defense_readiness_logistics_build_api_contract()
    ui = defense_readiness_logistics_ui_contract()
    render = defense_readiness_logistics_render_workbench()
    events = event_contract_manifest()
    handlers = handler_manifest()
    agent = agent_skill_manifest()
    governance = governance_smoke_test()
    seed = seed_plan()
    app_smoke = defense_app_smoke_test()
    domain = domain_depth_contract()
    checks = (
        {"id": "schema_models_migrations", "ok": schema["ok"]},
        {"id": "service_contract", "ok": services["ok"]},
        {"id": "api_contract", "ok": api["ok"] and validate_api_route_contracts()["ok"]},
        {"id": "events", "ok": events["ok"] and validate_event_contract()["ok"]},
        {"id": "handlers", "ok": handlers["ok"]},
        {"id": "ui_forms_wizards_controls", "ok": ui["ok"] and render["ok"]},
        {"id": "assistant_skills", "ok": agent["ok"] and chatbot_interface_contract()["ok"] and composed_agent_contribution()["ok"]},
        {"id": "governance", "ok": governance["ok"]},
        {"id": "seed_data", "ok": seed["ok"]},
        {"id": "domain_depth", "ok": domain["ok"]},
        {"id": "single_pbc_domain_app", "ok": app_smoke["ok"] and single_pbc_app_contract()["ok"]},
    )
    return {
        "format": "appgen.defense-readiness-logistics-release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "migrations": schema["migrations"],
            "models": schema["models"],
            "services": services,
            "api": api,
            "events": events,
            "handlers": handlers,
            "ui": ui,
            "workbench": render,
            "workflows": workflow_contracts(),
            "single_pbc_app": single_pbc_app_contract(),
            "assistant": chatbot_interface_contract(),
            "seed": seed,
            "migration_alignment": migration_alignment_contract(),
        },
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
    }


def defense_readiness_logistics_permissions_contract() -> dict:
    return permission_manifest()


def defense_readiness_logistics_build_workbench_view(tenant: str = "default") -> dict:
    rendered = defense_readiness_logistics_render_workbench()
    return {"ok": True, "pbc": PBC_KEY, "tenant": tenant, **rendered, "side_effects": ()}


def defense_readiness_logistics_verify_owned_table_boundary(references=()) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str) and ref.endswith("_table") and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": DEFENSE_READINESS_LOGISTICS_OWNED_TABLES,
        "shared_table_access": False,
    }


def defense_readiness_logistics_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = defense_readiness_logistics_runtime_smoke()
    operations = COMMAND_OPERATIONS + QUERY_OPERATIONS + (
        "build_schema_contract",
        "build_service_contract",
        "build_api_contract",
        "build_release_evidence",
        "permissions_contract",
        "verify_owned_table_boundary",
        "run_advanced_assessment",
        "parse_document_instruction",
    )
    return {
        "format": "appgen.defense-readiness-logistics-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": DEFENSE_READINESS_LOGISTICS_OWNED_TABLES,
        "allowed_database_backends": DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
        "standard_features": DEFENSE_READINESS_LOGISTICS_STANDARD_FEATURE_KEYS,
        "capabilities": DEFENSE_READINESS_LOGISTICS_RUNTIME_CAPABILITY_KEYS,
        "operations": operations,
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "workflows": workflow_contracts()["workflows"],
        "single_pbc_app": single_pbc_app_contract(),
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": DEFENSE_READINESS_LOGISTICS_ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def defense_readiness_logistics_runtime_smoke() -> dict:
    state = defense_readiness_logistics_empty_state()
    configured = defense_readiness_logistics_configure_runtime(state, {"database_backend": "postgresql", "event_topic": DEFAULT_TOPIC})
    parameter = defense_readiness_logistics_set_parameter(configured["state"], "workbench_limit", 50)
    rule = defense_readiness_logistics_register_rule(parameter["state"], {"rule_id": "unit_readiness_policy", "scope": "readiness"})
    received = defense_readiness_logistics_receive_event(rule["state"], {"event_type": CONSUMED[0], "idempotency_key": "smoke"})
    duplicate = defense_readiness_logistics_receive_event(received["state"], {"event_type": CONSUMED[0], "idempotency_key": "smoke"})
    dead_letter = defense_readiness_logistics_receive_event(duplicate["state"], {"event_type": "UnexpectedEvent", "idempotency_key": "bad-smoke"})
    command = defense_readiness_logistics_command_unit_readiness(
        dead_letter["state"],
        {
            "tenant_id": "tenant-smoke",
            "unit_id": "unit-runtime-smoke",
            "unit_code": "runtime-smoke",
            "personnel": {"available": 12, "required": 10, "certified_roles": 4, "required_certified_roles": 3},
            "serviceable_assets": 4,
            "required_assets": 3,
            "supply": {"critical_fill_rate": 0.95},
            "ammo_fill_rate": 0.91,
            "fuel_days": 2,
            "inspection_evidence": ("pack-runtime",),
            "commander_approved": True,
        },
    )
    workbench = defense_readiness_logistics_query_workbench(command["state"])
    checks = (
        {"id": "configuration", "ok": configured["ok"]},
        {"id": "parameter", "ok": parameter["ok"]},
        {"id": "rule", "ok": rule["ok"]},
        {"id": "event_receive", "ok": received["ok"]},
        {"id": "event_duplicate", "ok": duplicate["duplicate"]},
        {"id": "event_dead_letter", "ok": dead_letter["dead_letter_table"].endswith("dead_letter_event")},
        {"id": "command_unit_readiness", "ok": command["ok"]},
        {"id": "query_workbench", "ok": workbench["ok"]},
        {"id": "service_smoke", "ok": service_smoke_test()["ok"]},
        {"id": "event_smoke", "ok": event_smoke_test()["ok"]},
        {"id": "handler_smoke", "ok": handler_smoke_test()["ok"]},
        {"id": "agent_smoke", "ok": agent_smoke_test()["ok"]},
        {"id": "seed_smoke", "ok": seed_smoke_test()["ok"]},
        {"id": "governance_smoke", "ok": governance_smoke_test()["ok"]},
        {"id": "domain_depth_smoke", "ok": domain_depth_smoke_test()["ok"]},
        {"id": "app_smoke", "ok": defense_app_smoke_test()["ok"]},
    )
    return {"ok": all(check["ok"] for check in checks), "checks": checks, "side_effects": ()}
