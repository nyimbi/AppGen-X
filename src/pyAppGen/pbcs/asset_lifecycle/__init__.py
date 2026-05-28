"""Asset Lifecycle PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS
from .runtime import ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES
from .runtime import ASSET_LIFECYCLE_EMITTED_EVENT_TYPES
from .runtime import ASSET_LIFECYCLE_OWNED_TABLES
from .runtime import ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC
from .runtime import ASSET_LIFECYCLE_RUNTIME_CAPABILITY_KEYS
from .runtime import ASSET_LIFECYCLE_STANDARD_FEATURE_KEYS
from .runtime import asset_lifecycle_build_api_contract
from .runtime import asset_lifecycle_build_depreciation_schedule
from .runtime import asset_lifecycle_build_release_evidence
from .runtime import asset_lifecycle_build_schema_contract
from .runtime import asset_lifecycle_build_service_contract
from .runtime import asset_lifecycle_build_workbench_view
from .runtime import asset_lifecycle_configure_runtime
from .runtime import asset_lifecycle_empty_state
from .runtime import asset_lifecycle_place_asset_in_service
from .runtime import asset_lifecycle_permissions_contract
from .runtime import asset_lifecycle_receive_event
from .runtime import asset_lifecycle_register_asset
from .runtime import asset_lifecycle_review_depreciation_plan
from .runtime import asset_lifecycle_register_rule
from .runtime import asset_lifecycle_register_schema_extension
from .runtime import asset_lifecycle_retire_asset
from .runtime import asset_lifecycle_run_depreciation
from .runtime import asset_lifecycle_runtime_capabilities
from .runtime import asset_lifecycle_runtime_smoke
from .runtime import asset_lifecycle_set_parameter
from .runtime import asset_lifecycle_transfer_asset
from .runtime import asset_lifecycle_verify_owned_table_boundary
from .ui import ASSET_LIFECYCLE_UI_FRAGMENT_KEYS
from .ui import asset_lifecycle_render_workbench
from .ui import asset_lifecycle_ui_contract

PBC_KEY = "asset_lifecycle"


def implementation_contract() -> dict:
    runtime = asset_lifecycle_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": ASSET_LIFECYCLE_OWNED_TABLES,
        "allowed_database_backends": ASSET_LIFECYCLE_ALLOWED_DATABASE_BACKENDS,
        "api_contract": asset_lifecycle_build_api_contract(),
        "schema_contract": asset_lifecycle_build_schema_contract(),
        "service_contract": asset_lifecycle_build_service_contract(),
        "release_evidence_contract": asset_lifecycle_build_release_evidence(),
        "permissions_contract": asset_lifecycle_permissions_contract(),
        "required_event_topic": ASSET_LIFECYCLE_REQUIRED_EVENT_TOPIC,
        "consumes": ASSET_LIFECYCLE_CONSUMED_EVENT_TYPES,
        "emits": ASSET_LIFECYCLE_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime,
        "ui_contract": asset_lifecycle_ui_contract(),
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
