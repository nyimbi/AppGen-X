"""Package-local capability assurance for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import (
    ADVANCED_CAPABILITIES,
    ALLOWED_DATABASE_BACKENDS,
    OWNED_TABLES,
    PBC_KEY,
    RUNTIME_CAPABILITIES,
    STANDARD_FEATURES,
)
from .service_contract import build_service_contract

STANDARD_FEATURE_OPERATION_COVERAGE = {
    "data_product_management": ("create_data_product", "assign_data_owner", "query_workbench"),
    "data_product_catalog_workflow": ("publish_data_contract", "register_schema_version", "publish_product_change"),
    "data_product_catalog_analytics": ("record_usage", "run_advanced_assessment"),
    "configuration_schema": ("configure_runtime", "build_workbench_view"),
    "rule_engine": ("register_rule", "compile_data_product_rule"),
    "parameter_engine": ("set_parameter", "list_controls"),
    "owned_schema_migrations_models": ("register_schema_extension", "build_workbench_view"),
    "appgen_x_outbox_inbox_eventing": ("receive_event", "grant_data_access"),
    "idempotent_handlers": ("receive_event",),
    "retry_dead_letter_evidence": ("receive_event",),
    "permissions": ("grant_data_access", "certify_data_product"),
    "seed_data": ("query_workbench",),
    "workbench": ("query_workbench", "build_workbench_view", "list_forms", "list_wizards", "list_controls"),
    "agentic_document_instruction_intake": ("document_instruction_plan",),
    "governed_datastore_crud": ("create_data_product", "grant_data_access"),
    "ai_agent_task_assistance": ("document_instruction_plan", "run_advanced_assessment"),
    "configuration_workbench": ("build_workbench_view", "list_controls"),
    "continuous_release_assurance": ("run_advanced_assessment", "query_workbench"),
}
ADVANCED_CAPABILITY_OPERATION_COVERAGE = {
    "contract-aware data discovery": ("query_workbench", "publish_data_contract"),
    "lineage impact simulation": ("map_lineage_edge", "simulate_contract_change_impact"),
    "quality drift detection": ("record_quality_signal", "run_advanced_assessment"),
    "AI data product steward": ("document_instruction_plan", "run_advanced_assessment"),
    "policy-aware access recommendation": ("request_data_access", "grant_data_access"),
    "cryptographic contract evidence": ("publish_data_contract", "certify_data_product"),
}


def _missing_coverage(features: tuple[str, ...], coverage: dict, operations: set[str]) -> tuple[dict, ...]:
    gaps = []
    for feature in features:
        required_operations = coverage.get(feature, ())
        missing_operations = tuple(operation for operation in required_operations if operation not in operations)
        if missing_operations:
            gaps.append(
                {
                    "feature": feature,
                    "required_operations": required_operations,
                    "missing_operations": missing_operations,
                }
            )
    return tuple(gaps)


def table_stakes_capability_manifest() -> dict:
    service = build_service_contract()
    runtime_operations = tuple(service["command_methods"]) + tuple(service["query_methods"])
    return {
        "ok": service["ok"],
        "pbc": PBC_KEY,
        "standard_features": STANDARD_FEATURES,
        "advanced_capabilities": ADVANCED_CAPABILITIES,
        "runtime_capability_keys": RUNTIME_CAPABILITIES,
        "runtime_operations": runtime_operations,
        "owned_tables": OWNED_TABLES,
        "event_contract": "AppGen-X",
        "stream_picker_visible": False,
        "stream_engine_picker_visible": False,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    operations = set(manifest["runtime_operations"])
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{PBC_KEY}_"))
    invalid_backends = tuple(
        backend for backend in manifest["allowed_database_backends"] if backend not in ("postgresql", "mysql", "mariadb")
    )
    missing_standard = _missing_coverage(manifest["standard_features"], STANDARD_FEATURE_OPERATION_COVERAGE, operations)
    missing_advanced = _missing_coverage(manifest["advanced_capabilities"], ADVANCED_CAPABILITY_OPERATION_COVERAGE, operations)
    return {
        "ok": manifest["ok"] and not invalid_tables and not invalid_backends and not missing_standard and not missing_advanced,
        "manifest": manifest,
        "missing_standard": missing_standard,
        "missing_advanced": missing_advanced,
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "side_effects": (),
    }


def smoke_test() -> dict:
    coverage = validate_table_stakes_capability_coverage()
    return {"ok": coverage["ok"], "coverage": coverage, "side_effects": ()}
