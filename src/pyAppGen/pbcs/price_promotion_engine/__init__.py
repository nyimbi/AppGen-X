"""Price Promotion Engine PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES
from .runtime import PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES
from .runtime import PRICE_PROMOTION_ENGINE_EVENT_CONTRACT
from .runtime import PRICE_PROMOTION_ENGINE_OWNED_TABLES
from .runtime import PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import PRICE_PROMOTION_ENGINE_RUNTIME_CAPABILITY_KEYS
from .runtime import PRICE_PROMOTION_ENGINE_RUNTIME_TABLES
from .runtime import PRICE_PROMOTION_ENGINE_STANDARD_FEATURE_KEYS
from .runtime import price_promotion_engine_apply_promotion
from .runtime import price_promotion_engine_build_api_contract
from .runtime import price_promotion_engine_build_release_evidence
from .runtime import price_promotion_engine_build_schema_contract
from .runtime import price_promotion_engine_build_service_contract
from .runtime import price_promotion_engine_build_workbench_view
from .runtime import price_promotion_engine_binding_evidence
from .runtime import price_promotion_engine_configure_runtime
from .runtime import price_promotion_engine_empty_state
from .runtime import price_promotion_engine_permissions_contract
from .runtime import price_promotion_engine_quote_price
from .runtime import price_promotion_engine_receive_event
from .runtime import price_promotion_engine_register_loyalty_tier
from .runtime import price_promotion_engine_register_price_rule
from .runtime import price_promotion_engine_register_promotion
from .runtime import price_promotion_engine_register_rule
from .runtime import price_promotion_engine_register_schema_extension
from .runtime import price_promotion_engine_runtime_capabilities
from .runtime import price_promotion_engine_runtime_smoke
from .runtime import price_promotion_engine_set_parameter
from .runtime import price_promotion_engine_verify_owned_table_boundary
from .ui import PRICE_PROMOTION_ENGINE_UI_FRAGMENT_KEYS
from .ui import price_promotion_engine_render_workbench
from .ui import price_promotion_engine_ui_contract

PBC_KEY = "price_promotion_engine"


def implementation_contract() -> dict:
    runtime = price_promotion_engine_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": price_promotion_engine_ui_contract(),
        "api_contract": price_promotion_engine_build_api_contract(),
        "schema_contract": price_promotion_engine_build_schema_contract(),
        "service_contract": price_promotion_engine_build_service_contract(),
        "release_evidence_contract": price_promotion_engine_build_release_evidence(),
        "permissions_contract": price_promotion_engine_permissions_contract(),
        "owned_tables": PRICE_PROMOTION_ENGINE_OWNED_TABLES,
        "allowed_database_backends": PRICE_PROMOTION_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "runtime_tables": PRICE_PROMOTION_ENGINE_RUNTIME_TABLES,
        "required_event_topic": PRICE_PROMOTION_ENGINE_REQUIRED_EVENT_TOPIC,
        "event_contract": PRICE_PROMOTION_ENGINE_EVENT_CONTRACT,
        "consumes": PRICE_PROMOTION_ENGINE_CONSUMED_EVENT_TYPES,
        "emits": PRICE_PROMOTION_ENGINE_EMITTED_EVENT_TYPES,
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

