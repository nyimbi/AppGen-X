"""Package-local capability assurance for the insurance_claims_policy PBC."""

from __future__ import annotations

from .manifest import PBC_MANIFEST
from .runtime import INSURANCE_CLAIMS_POLICY_ALLOWED_DATABASE_BACKENDS
from .runtime import insurance_claims_policy_runtime_capabilities

PBC_KEY = "insurance_claims_policy"
CORE_OPERATIONS = {
    "insurance_policy_management": "create_insurance_policy",
    "insurance_claims_policy_workflow": "open_claim",
    "insurance_claims_policy_analytics": "simulate_loss_exposure",
    "configuration_schema": "configure_runtime",
    "rule_engine": "register_rule",
    "parameter_engine": "set_parameter",
    "owned_schema_migrations_models": "build_schema_contract",
    "appgen_x_outbox_inbox_eventing": "receive_event",
    "idempotent_handlers": "receive_event",
    "retry_dead_letter_evidence": "receive_event",
    "permissions": "permissions_contract",
    "seed_data": "create_insurance_policy",
    "workbench": "build_workbench_view",
    "agentic_document_instruction_intake": "parse_document_instruction",
    "governed_datastore_crud": "register_schema_extension",
}
ADVANCED_OPERATIONS = {
    "insurance_claims_policy_event_sourced_operational_history": "query_workbench",
    "insurance_claims_policy_multi_tenant_policy_isolation": "build_workbench_view",
    "insurance_claims_policy_schema_evolution_resilience": "register_schema_extension",
    "insurance_claims_policy_autonomous_anomaly_detection": "run_advanced_assessment",
    "insurance_claims_policy_semantic_document_instruction_understanding": "parse_document_instruction",
    "insurance_claims_policy_predictive_risk_scoring": "run_advanced_assessment",
    "insurance_claims_policy_counterfactual_scenario_simulation": "run_advanced_assessment",
    "insurance_claims_policy_cryptographic_audit_proofs": "build_release_evidence",
    "insurance_claims_policy_continuous_control_testing": "build_release_evidence",
    "insurance_claims_policy_carbon_and_sustainability_awareness": "run_advanced_assessment",
    "insurance_claims_policy_cross_pbc_event_federation": "receive_event",
    "insurance_claims_policy_governed_ai_agent_execution": "parse_document_instruction",
}


def table_stakes_capability_manifest() -> dict:
    runtime = insurance_claims_policy_runtime_capabilities()
    return {
        "ok": runtime["ok"],
        "pbc": PBC_KEY,
        "standard_features": PBC_MANIFEST["standard_features"],
        "advanced_capabilities": PBC_MANIFEST["advanced_capabilities"],
        "runtime_operations": tuple(runtime["operations"]),
        "owned_tables": tuple(runtime["owned_tables"]),
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "allowed_database_backends": INSURANCE_CLAIMS_POLICY_ALLOWED_DATABASE_BACKENDS,
        "side_effects": (),
    }


def validate_table_stakes_capability_coverage() -> dict:
    manifest = table_stakes_capability_manifest()
    operations = set(manifest["runtime_operations"])
    invalid_tables = tuple(table for table in manifest["owned_tables"] if not table.startswith(f"{PBC_KEY}_"))
    invalid_backends = tuple(backend for backend in (PBC_MANIFEST["datastore_backend"],) if backend not in manifest["allowed_database_backends"])
    missing_standard = tuple(feature for feature, operation in CORE_OPERATIONS.items() if operation not in operations)
    missing_advanced = tuple(feature for feature, operation in ADVANCED_OPERATIONS.items() if operation not in operations)
    return {
        "ok": manifest["ok"] and not invalid_tables and not invalid_backends and not missing_standard and not missing_advanced,
        "manifest": manifest,
        "covered_standard": tuple(feature for feature in manifest["standard_features"] if feature not in missing_standard),
        "covered_advanced": tuple(feature for feature in manifest["advanced_capabilities"] if feature not in missing_advanced),
        "missing_standard": missing_standard,
        "missing_advanced": missing_advanced,
        "missing_operations": tuple(sorted({CORE_OPERATIONS[feature] for feature in CORE_OPERATIONS if feature in missing_standard} | {ADVANCED_OPERATIONS[feature] for feature in ADVANCED_OPERATIONS if feature in missing_advanced})),
        "invalid_tables": invalid_tables,
        "invalid_backends": invalid_backends,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def smoke_test() -> dict:
    coverage = validate_table_stakes_capability_coverage()
    runtime = insurance_claims_policy_runtime_capabilities()
    return {"ok": coverage["ok"] and runtime["ok"], "coverage": coverage, "runtime": runtime, "side_effects": ()}
