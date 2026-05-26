"""Distributed Order Management PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import DOM_RUNTIME_CAPABILITY_KEYS
from .runtime import DOM_STANDARD_FEATURE_KEYS
from .runtime import DOM_ALLOWED_DATABASE_BACKENDS
from .runtime import DOM_CONSUMED_EVENT_TYPES
from .runtime import DOM_EMITTED_EVENT_TYPES
from .runtime import DOM_OWNED_TABLES
from .runtime import DOM_REQUIRED_EVENT_TOPIC
from .runtime import dom_apply_inventory_allocation
from .runtime import dom_apply_tax_projection
from .runtime import dom_build_api_contract
from .runtime import dom_build_release_evidence
from .runtime import dom_build_schema_contract
from .runtime import dom_build_service_contract
from .runtime import dom_build_workbench_view
from .runtime import dom_capture_order
from .runtime import dom_configure_runtime
from .runtime import dom_confirm_order_shipped
from .runtime import dom_create_fulfillment_plan
from .runtime import dom_empty_state
from .runtime import dom_permissions_contract
from .runtime import dom_price_order
from .runtime import dom_register_rule
from .runtime import dom_register_schema_extension
from .runtime import dom_receive_event
from .runtime import dom_runtime_capabilities
from .runtime import dom_runtime_smoke
from .runtime import dom_screen_fraud
from .runtime import dom_set_parameter
from .runtime import dom_upsert_customer_projection
from .runtime import dom_verify_order
from .runtime import dom_verify_owned_table_boundary
from .ui import DOM_UI_FRAGMENT_KEYS
from .ui import dom_render_workbench
from .ui import dom_ui_contract

PBC_KEY = "dom"


def implementation_contract() -> dict:
    runtime = dom_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": DOM_OWNED_TABLES,
        "allowed_database_backends": DOM_ALLOWED_DATABASE_BACKENDS,
        "api_contract": dom_build_api_contract(),
        "schema_contract": dom_build_schema_contract(),
        "service_contract": dom_build_service_contract(),
        "release_evidence_contract": dom_build_release_evidence(),
        "permissions_contract": dom_permissions_contract(),
        "required_event_topic": DOM_REQUIRED_EVENT_TOPIC,
        "consumes": DOM_CONSUMED_EVENT_TYPES,
        "emits": DOM_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime,
        "ui_contract": dom_ui_contract(),
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

