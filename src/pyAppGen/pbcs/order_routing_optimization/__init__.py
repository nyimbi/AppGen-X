"""Order Routing Optimization PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS
from .runtime import ORDER_ROUTING_OPTIMIZATION_CONSUMED_EVENT_TYPES
from .runtime import ORDER_ROUTING_OPTIMIZATION_EMITTED_EVENT_TYPES
from .runtime import ORDER_ROUTING_OPTIMIZATION_OWNED_TABLES
from .runtime import ORDER_ROUTING_OPTIMIZATION_REQUIRED_EVENT_TOPIC
from .runtime import ORDER_ROUTING_OPTIMIZATION_RUNTIME_CAPABILITY_KEYS
from .runtime import ORDER_ROUTING_OPTIMIZATION_STANDARD_FEATURE_KEYS
from .runtime import order_routing_optimization_build_api_contract
from .runtime import order_routing_optimization_build_release_evidence
from .runtime import order_routing_optimization_build_schema_contract
from .runtime import order_routing_optimization_build_service_contract
from .runtime import order_routing_optimization_build_workbench_view
from .runtime import order_routing_optimization_clear_capacity_auction
from .runtime import order_routing_optimization_configure_runtime
from .runtime import order_routing_optimization_detect_routing_anomaly
from .runtime import order_routing_optimization_empty_state
from .runtime import order_routing_optimization_federate_routing_view
from .runtime import order_routing_optimization_forecast_capacity
from .runtime import order_routing_optimization_generate_routing_proof
from .runtime import order_routing_optimization_handle_event
from .runtime import order_routing_optimization_ingest_capacity_snapshot
from .runtime import order_routing_optimization_optimize_route_network
from .runtime import order_routing_optimization_parse_route_request
from .runtime import order_routing_optimization_permissions_contract
from .runtime import order_routing_optimization_recommend_exception_resolution
from .runtime import order_routing_optimization_register_governed_model
from .runtime import order_routing_optimization_register_rule
from .runtime import order_routing_optimization_register_schema_extension
from .runtime import order_routing_optimization_reserve_node_capacity
from .runtime import order_routing_optimization_rotate_crypto_epoch
from .runtime import order_routing_optimization_route_orders
from .runtime import order_routing_optimization_run_control_tests
from .runtime import order_routing_optimization_run_resilience_drill
from .runtime import order_routing_optimization_runtime_capabilities
from .runtime import order_routing_optimization_runtime_smoke
from .runtime import order_routing_optimization_schedule_carbon_aware_route
from .runtime import order_routing_optimization_score_fulfillment_risk
from .runtime import order_routing_optimization_screen_policy
from .runtime import order_routing_optimization_self_heal_route_selection
from .runtime import order_routing_optimization_set_parameter
from .runtime import order_routing_optimization_simulate_counterfactual
from .runtime import order_routing_optimization_model_stochastic_exposure
from .runtime import order_routing_optimization_upsert_route_candidate
from .runtime import order_routing_optimization_verify_owned_table_boundary
from .ui import ORDER_ROUTING_OPTIMIZATION_UI_FRAGMENT_KEYS
from .ui import order_routing_optimization_render_workbench
from .ui import order_routing_optimization_ui_contract

PBC_KEY = "order_routing_optimization"


def implementation_contract() -> dict:
    runtime = order_routing_optimization_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": ORDER_ROUTING_OPTIMIZATION_OWNED_TABLES,
        "allowed_database_backends": ORDER_ROUTING_OPTIMIZATION_ALLOWED_DATABASE_BACKENDS,
        "api_contract": order_routing_optimization_build_api_contract(),
        "schema_contract": order_routing_optimization_build_schema_contract(),
        "service_contract": order_routing_optimization_build_service_contract(),
        "release_evidence_contract": order_routing_optimization_build_release_evidence(),
        "permissions_contract": order_routing_optimization_permissions_contract(),
        "required_event_topic": ORDER_ROUTING_OPTIMIZATION_REQUIRED_EVENT_TOPIC,
        "consumes": ORDER_ROUTING_OPTIMIZATION_CONSUMED_EVENT_TYPES,
        "emits": ORDER_ROUTING_OPTIMIZATION_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime,
        "ui_contract": order_routing_optimization_ui_contract(),
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

