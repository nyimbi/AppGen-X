"""General Ledger Core PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import GL_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import GL_CORE_CONSUMED_EVENT_TYPES
from .runtime import GL_CORE_EMITTED_EVENT_TYPES
from .runtime import GL_CORE_OWNED_TABLES
from .runtime import GL_CORE_REQUIRED_EVENT_TOPIC
from .runtime import GL_CORE_STANDARD_FEATURE_KEYS
from .runtime import gl_core_append_ledger_event
from .runtime import gl_core_build_api_contract
from .runtime import gl_core_build_release_evidence
from .runtime import gl_core_build_federated_view
from .runtime import gl_core_build_projection
from .runtime import gl_core_build_schema_contract
from .runtime import gl_core_build_service_contract
from .runtime import gl_core_build_workbench_view
from .runtime import gl_core_compile_regulatory_rules
from .runtime import gl_core_configure_runtime
from .runtime import gl_core_consolidate_private_balances
from .runtime import gl_core_create_continuous_close_snapshot
from .runtime import gl_core_derive_account_from_semantics
from .runtime import gl_core_empty_state
from .runtime import gl_core_evaluate_policy
from .runtime import gl_core_generate_audit_proof
from .runtime import gl_core_measure_information_auditability
from .runtime import gl_core_predict_posting_validation
from .runtime import gl_core_query_temporal_ledger
from .runtime import gl_core_receive_event
from .runtime import gl_core_register_financial_model
from .runtime import gl_core_permissions_contract
from .runtime import gl_core_register_rule
from .runtime import gl_core_register_schema_extension
from .runtime import gl_core_replicate_consensus
from .runtime import gl_core_resolve_reconciliation_game
from .runtime import gl_core_rotate_crypto_epoch
from .runtime import gl_core_run_causal_scenario
from .runtime import gl_core_run_control_tests
from .runtime import gl_core_run_resilience_drill
from .runtime import gl_core_runtime_capabilities
from .runtime import gl_core_runtime_smoke
from .runtime import gl_core_schedule_carbon_aware_execution
from .runtime import gl_core_set_parameter
from .runtime import gl_core_simulate_probabilistic_posting
from .runtime import gl_core_suggest_reconciliation
from .runtime import gl_core_verify_owned_table_boundary
from .runtime import gl_core_verify_formal_invariants
from .runtime import gl_core_verify_identity_credential
from .ui import GL_CORE_UI_FRAGMENT_KEYS
from .ui import gl_core_render_workbench
from .ui import gl_core_ui_contract

PBC_KEY = "gl_core"


def implementation_contract() -> dict:
    runtime = gl_core_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": gl_core_ui_contract(),
        "api_contract": gl_core_build_api_contract(),
        "schema_contract": gl_core_build_schema_contract(),
        "service_contract": gl_core_build_service_contract(),
        "release_evidence_contract": gl_core_build_release_evidence(),
        "permissions_contract": gl_core_permissions_contract(),
        "owned_tables": GL_CORE_OWNED_TABLES,
        "allowed_database_backends": GL_CORE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
        "emitted_event_types": GL_CORE_EMITTED_EVENT_TYPES,
        "consumed_event_types": GL_CORE_CONSUMED_EVENT_TYPES,
    }


def register_pbc() -> dict:
    """Return this PBC manifest without mutating global catalog state."""
    return dict(PBC_MANIFEST)


def registration_plan(existing_catalog: dict | None = None) -> dict:
    """Return a side-effect-free registration plan for this PBC package."""
    return source_registration_plan(
        PBC_KEY,
        register_pbc(),
        existing_catalog=existing_catalog,
    )


def package_metadata_manifest() -> dict:
    """Return package identity, artifacts, and discovery metadata."""
    return source_package_metadata(PBC_KEY, register_pbc(), implementation_contract())


def validate_package_metadata() -> dict:
    """Validate package metadata without mutating catalog state."""
    return validate_source_package_metadata(package_metadata_manifest())


def package_discovery_plan(existing_catalog: dict | None = None) -> dict:
    """Return side-effect-free package discovery and registration evidence."""
    metadata_validation = validate_package_metadata()
    registration = registration_plan(existing_catalog=existing_catalog)
    return {
        "format": "appgen.pbc-source-package-discovery-plan.v1",
        "ok": metadata_validation["ok"] and registration["ok"],
        "pbc": PBC_KEY,
        "metadata_validation": metadata_validation,
        "registration": registration,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise package metadata validation and discovery planning."""
    discovery = package_discovery_plan()
    return {
        "ok": discovery["ok"],
        "discovery": discovery,
        "side_effects": (),
    }

