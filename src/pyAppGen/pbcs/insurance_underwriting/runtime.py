"""Executable runtime contract for the insurance_underwriting PBC."""

from __future__ import annotations

from pathlib import Path

from .agent import composed_agent_contribution
from .config import (
    ALLOWED_DATABASE_BACKENDS,
    DEFAULT_RUNTIME_PARAMETERS,
    SUPPORTED_CONFIGURATION_FIELDS,
    configuration_manifest,
    governance_smoke_test,
    parameter_manifest,
    rule_manifest,
)
from .domain_depth import DOMAIN_OPERATIONS, domain_depth_contract, domain_depth_smoke_test
from .events import CONSUMED, EMITTED, TOPIC, event_contract_manifest
from .handlers import handler_manifest
from .models import (
    BUSINESS_TABLES,
    EVENT_TABLES,
    OWNED_SCHEMA,
    OWNED_TABLES,
    migration_alignment_report,
    standalone_model_contract,
    standalone_store_smoke_test,
)
from .permissions import ACTION_PERMISSIONS, permission_manifest
from .routes import api_route_contracts, standalone_route_contracts, validate_api_route_contracts
from .services import service_operation_contracts, standalone_service_operation_contracts
from .ui import insurance_underwriting_standalone_workbench_blueprint, insurance_underwriting_ui_contract
from .workflows import underwriting_workflow_catalog


PBC_KEY = "insurance_underwriting"
INSURANCE_UNDERWRITING_OWNED_TABLES = OWNED_TABLES
INSURANCE_UNDERWRITING_RUNTIME_TABLES = OWNED_TABLES
INSURANCE_UNDERWRITING_ALLOWED_DATABASE_BACKENDS = ALLOWED_DATABASE_BACKENDS
INSURANCE_UNDERWRITING_REQUIRED_EVENT_TOPIC = TOPIC
INSURANCE_UNDERWRITING_EMITTED_EVENT_TYPES = EMITTED
INSURANCE_UNDERWRITING_CONSUMED_EVENT_TYPES = CONSUMED
INSURANCE_UNDERWRITING_STANDARD_FEATURE_KEYS = (
    "underwriting_submission_management",
    "insurance_underwriting_workflow",
    "insurance_underwriting_analytics",
    "risk_appetite_screening",
    "rating_traceability",
    "quote_scenarioing",
    "authority_governed_decisions",
    "bind_readiness_tracking",
    "workbench",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "owned_schema_migrations_models",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "seed_data",
    "agentic_document_instruction_intake",
    "governed_datastore_crud",
    "ai_agent_task_assistance",
    "configuration_workbench",
    "standalone_package_local_app",
    "continuous_release_assurance",
)
INSURANCE_UNDERWRITING_RUNTIME_CAPABILITY_KEYS = (
    "insurance_underwriting_event_sourced_operational_history",
    "insurance_underwriting_multi_tenant_policy_isolation",
    "insurance_underwriting_schema_evolution_resilience",
    "insurance_underwriting_autonomous_anomaly_detection",
    "insurance_underwriting_semantic_document_instruction_understanding",
    "insurance_underwriting_predictive_risk_scoring",
    "insurance_underwriting_counterfactual_scenario_simulation",
    "insurance_underwriting_cryptographic_audit_proofs",
    "insurance_underwriting_continuous_control_testing",
    "insurance_underwriting_carbon_and_sustainability_awareness",
    "insurance_underwriting_cross_pbc_event_federation",
    "insurance_underwriting_governed_ai_agent_execution",
    "insurance_underwriting_counterfactual_quote_scenarioing",
)
INSURANCE_UNDERWRITING_UI_FRAGMENT_KEYS = insurance_underwriting_ui_contract()["fragments"]
INSURANCE_UNDERWRITING_BUSINESS_TABLES = BUSINESS_TABLES
INSURANCE_UNDERWRITING_SUPPORTED_CONFIGURATION_FIELDS = SUPPORTED_CONFIGURATION_FIELDS
INSURANCE_UNDERWRITING_SUPPORTED_PARAMETER_KEYS = tuple(DEFAULT_RUNTIME_PARAMETERS)
INSURANCE_UNDERWRITING_REQUIRED_RULE_FIELDS = ("rule_id", "rule_type", "description")
BASE_DIR = Path(__file__).parent


def insurance_underwriting_build_schema_contract() -> dict:
    alignment = migration_alignment_report()
    return {
        "format": "appgen.insurance-underwriting-owned-schema-contract.v1",
        "ok": alignment["ok"],
        "pbc": PBC_KEY,
        "tables": OWNED_SCHEMA["tables"],
        "models": tuple(
            {
                "class_name": "".join(part.capitalize() for part in table["logical_table"].split("_")),
                "table": table["owned_table"],
                "fields": table["fields"],
            }
            for table in OWNED_SCHEMA["tables"]
        ),
        "migrations": (
            {
                "path": "pbcs/insurance_underwriting/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": OWNED_TABLES,
                "backend_allowlist": ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "datastore_backends": ALLOWED_DATABASE_BACKENDS,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": OWNED_TABLES,
        "migration_alignment": alignment,
        "side_effects": (),
    }


def insurance_underwriting_build_service_contract() -> dict:
    source = service_operation_contracts()
    standalone = standalone_service_operation_contracts()
    return {
        "format": "appgen.insurance-underwriting-service-contract.v1",
        "ok": source["ok"] and standalone["ok"],
        "pbc": PBC_KEY,
        "command_methods": source["command_operations"] + standalone["command_operations"],
        "query_methods": source["query_operations"] + standalone["query_operations"],
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "standalone": standalone,
        "side_effects": (),
    }


def insurance_underwriting_build_api_contract() -> dict:
    source = api_route_contracts()
    standalone = standalone_route_contracts()
    return {
        "format": "appgen.insurance-underwriting-api-contract.v1",
        "ok": source["ok"] and standalone["ok"],
        "pbc": PBC_KEY,
        "routes": source["routes"],
        "standalone_routes": standalone["routes"],
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "owned_tables": OWNED_TABLES,
        "side_effects": (),
    }


def insurance_underwriting_permissions_contract() -> dict:
    manifest = permission_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "permissions": manifest["permissions"],
        "roles": manifest["roles"],
        "action_permissions": ACTION_PERMISSIONS,
        "side_effects": (),
    }


def insurance_underwriting_build_workbench_view(tenant: str = "default") -> dict:
    blueprint = insurance_underwriting_standalone_workbench_blueprint()
    return {
        "ok": blueprint["ok"],
        "pbc": PBC_KEY,
        "tenant": tenant,
        "route": f"/workbench/pbcs/{PBC_KEY}",
        "tables": INSURANCE_UNDERWRITING_BUSINESS_TABLES,
        "actions": tuple(ACTION_PERMISSIONS),
        "ui_fragments": INSURANCE_UNDERWRITING_UI_FRAGMENT_KEYS,
        "forms": blueprint["forms"],
        "wizards": blueprint["wizards"],
        "controls": blueprint["controls"],
        "side_effects": (),
    }


def insurance_underwriting_verify_owned_table_boundary(references=()) -> dict:
    invalid = tuple(
        ref
        for ref in references
        if isinstance(ref, str)
        and ref.endswith("_table")
        and not ref.startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not invalid,
        "pbc": PBC_KEY,
        "invalid_references": invalid,
        "allowed_tables": OWNED_TABLES,
        "shared_table_access": False,
    }


def insurance_underwriting_build_release_evidence() -> dict:
    from .standalone import insurance_underwriting_standalone_app_contract, insurance_underwriting_standalone_app_smoke

    docs = {
        name: (BASE_DIR / name).exists()
        for name in (
            "README.md",
            "implementation-plan.md",
            "implementation-status.md",
            "RELEASE_EVIDENCE.md",
        )
    }
    checks = (
        {"id": "schema_alignment", "ok": insurance_underwriting_build_schema_contract()["ok"]},
        {"id": "service_and_routes", "ok": insurance_underwriting_build_service_contract()["ok"] and validate_api_route_contracts()["ok"]},
        {"id": "event_and_handler_contracts", "ok": event_contract_manifest()["ok"] and handler_manifest()["ok"]},
        {"id": "governance", "ok": governance_smoke_test()["ok"] and permission_manifest()["ok"]},
        {"id": "agent_and_ui", "ok": composed_agent_contribution()["ok"] and insurance_underwriting_ui_contract()["ok"]},
        {"id": "standalone_app", "ok": insurance_underwriting_standalone_app_contract()["ok"] and insurance_underwriting_standalone_app_smoke()["ok"]},
        {"id": "documentation", "ok": all(docs.values())},
    )
    return {
        "format": "appgen.insurance-underwriting-release-evidence.v1",
        "ok": all(item["ok"] for item in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "generated_artifacts": {
            "schema": insurance_underwriting_build_schema_contract(),
            "service": insurance_underwriting_build_service_contract(),
            "api": insurance_underwriting_build_api_contract(),
            "events": event_contract_manifest(),
            "handlers": handler_manifest(),
            "workflows": underwriting_workflow_catalog(),
            "ui": insurance_underwriting_ui_contract(),
            "agent": composed_agent_contribution(),
        },
        "documentation": {"ok": all(docs.values()), "files": docs},
        "blocking_gaps": tuple(item["id"] for item in checks if not item["ok"]),
        "side_effects": (),
    }


def insurance_underwriting_runtime_capabilities() -> dict:
    domain = domain_depth_contract()
    smoke = insurance_underwriting_runtime_smoke()
    return {
        "format": "appgen.insurance-underwriting-runtime-capabilities.v1",
        "ok": smoke["ok"] and domain["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": OWNED_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "standard_features": INSURANCE_UNDERWRITING_STANDARD_FEATURE_KEYS,
        "capabilities": INSURANCE_UNDERWRITING_RUNTIME_CAPABILITY_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "receive_event",
            "build_workbench_view",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
        ) + DOMAIN_OPERATIONS,
        "smoke": smoke,
        "world_class_domain_depth": domain,
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def insurance_underwriting_runtime_smoke() -> dict:
    schema = insurance_underwriting_build_schema_contract()
    service = insurance_underwriting_build_service_contract()
    api = insurance_underwriting_build_api_contract()
    workbench = insurance_underwriting_build_workbench_view()
    boundary = insurance_underwriting_verify_owned_table_boundary(OWNED_TABLES + ("foreign_table",))
    release = insurance_underwriting_build_release_evidence()
    checks = (
        {"id": "schema", "ok": schema["ok"]},
        {"id": "service", "ok": service["ok"]},
        {"id": "api", "ok": api["ok"]},
        {"id": "governance", "ok": governance_smoke_test()["ok"]},
        {"id": "permissions", "ok": permission_manifest()["ok"]},
        {"id": "ui", "ok": insurance_underwriting_ui_contract()["ok"]},
        {"id": "agent", "ok": composed_agent_contribution()["ok"]},
        {"id": "workbench", "ok": workbench["ok"]},
        {"id": "store_smoke", "ok": standalone_store_smoke_test()["ok"]},
        {"id": "domain_depth", "ok": domain_depth_smoke_test()["ok"]},
        {"id": "boundary_rejects_foreign_table", "ok": boundary["ok"] is False},
        {"id": "release", "ok": release["ok"]},
    )
    return {
        "format": "appgen.insurance-underwriting-runtime-smoke.v1",
        "ok": all(item["ok"] for item in checks),
        "checks": checks,
        "schema": schema,
        "service": service,
        "api": api,
        "release": release,
        "side_effects": (),
    }
