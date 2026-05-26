"""Checkout Processing PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC
from .runtime import CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS
from .runtime import CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES
from .runtime import CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES
from .runtime import CHECKOUT_PROCESSING_OWNED_TABLES
from .runtime import CHECKOUT_PROCESSING_RUNTIME_TABLES
from .runtime import CHECKOUT_PROCESSING_RUNTIME_CAPABILITY_KEYS
from .runtime import CHECKOUT_PROCESSING_STANDARD_FEATURE_KEYS
from .runtime import checkout_processing_allocate_promotion_value
from .runtime import checkout_processing_add_cart_line
from .runtime import checkout_processing_apply_coupon
from .runtime import checkout_processing_apply_pricing_handoff
from .runtime import checkout_processing_apply_tax_handoff
from .runtime import checkout_processing_build_api_contract
from .runtime import checkout_processing_build_release_evidence
from .runtime import checkout_processing_build_schema_contract
from .runtime import checkout_processing_build_service_contract
from .runtime import checkout_processing_build_workbench_view
from .runtime import checkout_processing_complete_checkout
from .runtime import checkout_processing_configure_runtime
from .runtime import checkout_processing_create_cart
from .runtime import checkout_processing_create_payment_intent
from .runtime import checkout_processing_detect_checkout_anomaly
from .runtime import checkout_processing_empty_state
from .runtime import checkout_processing_federate_checkout_view
from .runtime import checkout_processing_forecast_abandonment
from .runtime import checkout_processing_generate_checkout_proof
from .runtime import checkout_processing_model_stochastic_checkout_exposure
from .runtime import checkout_processing_open_checkout_session
from .runtime import checkout_processing_optimize_checkout_path
from .runtime import checkout_processing_parse_instruction
from .runtime import checkout_processing_permissions_contract
from .runtime import checkout_processing_predictive_risk_score
from .runtime import checkout_processing_receive_event
from .runtime import checkout_processing_register_governed_model
from .runtime import checkout_processing_register_rule
from .runtime import checkout_processing_register_schema_extension
from .runtime import checkout_processing_reserve_inventory_handoff
from .runtime import checkout_processing_resolve_checkout_exception
from .runtime import checkout_processing_rotate_crypto_epoch
from .runtime import checkout_processing_route_checkout
from .runtime import checkout_processing_run_control_tests
from .runtime import checkout_processing_run_resilience_drill
from .runtime import checkout_processing_runtime_capabilities
from .runtime import checkout_processing_runtime_smoke
from .runtime import checkout_processing_score_conversion_probability
from .runtime import checkout_processing_screen_checkout_policy
from .runtime import checkout_processing_screen_risk
from .runtime import checkout_processing_select_carbon_aware_fulfillment
from .runtime import checkout_processing_set_parameter
from .runtime import checkout_processing_simulate_counterfactual_checkout
from .runtime import checkout_processing_validate_shipping_address
from .runtime import checkout_processing_verify_owned_table_boundary
from .runtime import checkout_processing_verify_formal_invariants
from .ui import CHECKOUT_PROCESSING_UI_FRAGMENT_KEYS
from .ui import checkout_processing_render_workbench
from .ui import checkout_processing_ui_contract

PBC_KEY = "checkout_processing"


def implementation_contract() -> dict:
    runtime = checkout_processing_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": checkout_processing_ui_contract(),
        "api_contract": checkout_processing_build_api_contract(),
        "schema_contract": checkout_processing_build_schema_contract(),
        "service_contract": checkout_processing_build_service_contract(),
        "release_evidence_contract": checkout_processing_build_release_evidence(),
        "permissions_contract": checkout_processing_permissions_contract(),
        "owned_tables": CHECKOUT_PROCESSING_OWNED_TABLES,
        "runtime_tables": CHECKOUT_PROCESSING_RUNTIME_TABLES,
        "allowed_database_backends": CHECKOUT_PROCESSING_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": CHECKOUT_PROCESSING_REQUIRED_EVENT_TOPIC,
        "emits": CHECKOUT_PROCESSING_EMITTED_EVENT_TYPES,
        "consumes": CHECKOUT_PROCESSING_CONSUMED_EVENT_TYPES,
        "boundary_contract": checkout_processing_verify_owned_table_boundary(
            CHECKOUT_PROCESSING_OWNED_TABLES
            + (
                "ProductPublished",
                "product_projection",
                "POST /payment-intents",
            )
        ),
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

