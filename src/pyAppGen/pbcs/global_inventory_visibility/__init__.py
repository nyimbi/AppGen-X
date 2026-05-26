"""Global Inventory Visibility PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from .runtime import GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS
from .runtime import GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC
from .runtime import GLOBAL_INVENTORY_VISIBILITY_RUNTIME_CAPABILITY_KEYS
from .runtime import GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES
from .runtime import GLOBAL_INVENTORY_VISIBILITY_STANDARD_FEATURE_KEYS
from .runtime import global_inventory_visibility_allocate_competing_pools
from .runtime import global_inventory_visibility_build_api_contract
from .runtime import global_inventory_visibility_build_release_evidence
from .runtime import global_inventory_visibility_build_schema_contract
from .runtime import global_inventory_visibility_build_service_contract
from .runtime import global_inventory_visibility_build_workbench_view
from .runtime import global_inventory_visibility_configure_runtime
from .runtime import global_inventory_visibility_detect_inventory_anomaly
from .runtime import global_inventory_visibility_empty_state
from .runtime import global_inventory_visibility_federate_inventory_view
from .runtime import global_inventory_visibility_forecast_temporal_availability
from .runtime import global_inventory_visibility_generate_availability_proof
from .runtime import global_inventory_visibility_get_global_availability
from .runtime import global_inventory_visibility_ingest_event
from .runtime import global_inventory_visibility_optimize_allocation
from .runtime import global_inventory_visibility_parse_semantic_query
from .runtime import global_inventory_visibility_permissions_contract
from .runtime import global_inventory_visibility_project_availability
from .runtime import global_inventory_visibility_record_availability_snapshot
from .runtime import global_inventory_visibility_register_governed_model
from .runtime import global_inventory_visibility_register_inventory_pool
from .runtime import global_inventory_visibility_register_rule
from .runtime import global_inventory_visibility_register_schema_extension
from .runtime import global_inventory_visibility_register_supply_node
from .runtime import global_inventory_visibility_reserve_inventory
from .runtime import global_inventory_visibility_resolve_exception
from .runtime import global_inventory_visibility_rotate_crypto_epoch
from .runtime import global_inventory_visibility_route_projection
from .runtime import global_inventory_visibility_run_control_tests
from .runtime import global_inventory_visibility_run_resilience_drill
from .runtime import global_inventory_visibility_runtime_capabilities
from .runtime import global_inventory_visibility_runtime_smoke
from .runtime import global_inventory_visibility_schedule_carbon_aware_sourcing
from .runtime import global_inventory_visibility_score_stockout_risk
from .runtime import global_inventory_visibility_screen_allocation_policy
from .runtime import global_inventory_visibility_set_parameter
from .runtime import global_inventory_visibility_simulate_counterfactual_allocation
from .runtime import global_inventory_visibility_verify_formal_invariants
from .runtime import global_inventory_visibility_verify_owned_table_boundary
from .runtime import global_inventory_visibility_verify_supply_identity
from .ui import GLOBAL_INVENTORY_VISIBILITY_UI_FRAGMENT_KEYS
from .ui import global_inventory_visibility_render_workbench
from .ui import global_inventory_visibility_ui_contract

PBC_KEY = "global_inventory_visibility"


def implementation_contract() -> dict:
    runtime = global_inventory_visibility_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": global_inventory_visibility_ui_contract(),
        "api_contract": global_inventory_visibility_build_api_contract(),
        "schema_contract": global_inventory_visibility_build_schema_contract(),
        "service_contract": global_inventory_visibility_build_service_contract(),
        "release_evidence_contract": global_inventory_visibility_build_release_evidence(),
        "permissions_contract": global_inventory_visibility_permissions_contract(),
        "owned_tables": GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES,
        "runtime_tables": GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES,
        "allowed_database_backends": GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
        "consumes": GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES,
        "emits": GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES,
    }


__all__ = (
    "GLOBAL_INVENTORY_VISIBILITY_RUNTIME_CAPABILITY_KEYS",
    "GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS",
    "GLOBAL_INVENTORY_VISIBILITY_CONSUMED_EVENT_TYPES",
    "GLOBAL_INVENTORY_VISIBILITY_EMITTED_EVENT_TYPES",
    "GLOBAL_INVENTORY_VISIBILITY_OWNED_TABLES",
    "GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC",
    "GLOBAL_INVENTORY_VISIBILITY_STANDARD_FEATURE_KEYS",
    "GLOBAL_INVENTORY_VISIBILITY_RUNTIME_TABLES",
    "GLOBAL_INVENTORY_VISIBILITY_UI_FRAGMENT_KEYS",
    "PBC_KEY",
    "global_inventory_visibility_allocate_competing_pools",
    "global_inventory_visibility_build_api_contract",
    "global_inventory_visibility_build_release_evidence",
    "global_inventory_visibility_build_schema_contract",
    "global_inventory_visibility_build_service_contract",
    "global_inventory_visibility_build_workbench_view",
    "global_inventory_visibility_configure_runtime",
    "global_inventory_visibility_detect_inventory_anomaly",
    "global_inventory_visibility_empty_state",
    "global_inventory_visibility_federate_inventory_view",
    "global_inventory_visibility_forecast_temporal_availability",
    "global_inventory_visibility_generate_availability_proof",
    "global_inventory_visibility_get_global_availability",
    "global_inventory_visibility_ingest_event",
    "global_inventory_visibility_optimize_allocation",
    "global_inventory_visibility_parse_semantic_query",
    "global_inventory_visibility_permissions_contract",
    "global_inventory_visibility_project_availability",
    "global_inventory_visibility_record_availability_snapshot",
    "global_inventory_visibility_register_governed_model",
    "global_inventory_visibility_register_inventory_pool",
    "global_inventory_visibility_register_rule",
    "global_inventory_visibility_register_schema_extension",
    "global_inventory_visibility_register_supply_node",
    "global_inventory_visibility_render_workbench",
    "global_inventory_visibility_reserve_inventory",
    "global_inventory_visibility_resolve_exception",
    "global_inventory_visibility_rotate_crypto_epoch",
    "global_inventory_visibility_route_projection",
    "global_inventory_visibility_run_control_tests",
    "global_inventory_visibility_run_resilience_drill",
    "global_inventory_visibility_runtime_capabilities",
    "global_inventory_visibility_runtime_smoke",
    "global_inventory_visibility_schedule_carbon_aware_sourcing",
    "global_inventory_visibility_score_stockout_risk",
    "global_inventory_visibility_screen_allocation_policy",
    "global_inventory_visibility_set_parameter",
    "global_inventory_visibility_simulate_counterfactual_allocation",
    "global_inventory_visibility_ui_contract",
    "global_inventory_visibility_verify_formal_invariants",
    "global_inventory_visibility_verify_owned_table_boundary",
    "global_inventory_visibility_verify_supply_identity",
    "implementation_contract",
)


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
