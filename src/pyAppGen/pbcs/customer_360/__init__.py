"""Customer 360 PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import CUSTOMER_360_ALLOWED_DATABASE_BACKENDS
from .runtime import CUSTOMER_360_CONSUMED_EVENT_TYPES
from .runtime import CUSTOMER_360_EMITTED_EVENT_TYPES
from .runtime import CUSTOMER_360_OWNED_TABLES
from .runtime import CUSTOMER_360_REQUIRED_EVENT_TOPIC
from .runtime import CUSTOMER_360_RUNTIME_CAPABILITY_KEYS
from .runtime import CUSTOMER_360_STANDARD_FEATURE_KEYS
from .runtime import customer_360_build_api_contract
from .runtime import customer_360_build_release_evidence
from .runtime import customer_360_build_schema_contract
from .runtime import customer_360_build_service_contract
from .runtime import customer_360_build_timeline
from .runtime import customer_360_build_workbench_view
from .runtime import customer_360_capture_touchpoint
from .runtime import customer_360_configure_runtime
from .runtime import customer_360_create_profile
from .runtime import customer_360_empty_state
from .runtime import customer_360_ingest_engagement_event
from .runtime import customer_360_link_identity
from .runtime import customer_360_open_merge_case
from .runtime import customer_360_permissions_contract
from .runtime import customer_360_receive_event
from .runtime import customer_360_record_consent
from .runtime import customer_360_register_rule
from .runtime import customer_360_register_schema_extension
from .runtime import customer_360_resolve_merge_case
from .runtime import customer_360_runtime_capabilities
from .runtime import customer_360_runtime_smoke
from .runtime import customer_360_set_parameter
from .runtime import customer_360_set_preference
from .runtime import customer_360_verify_owned_table_boundary
from .ui import CUSTOMER_360_UI_FRAGMENT_KEYS
from .ui import customer_360_render_workbench
from .ui import customer_360_ui_contract

PBC_KEY = "customer_360"


def implementation_contract() -> dict:
    runtime = customer_360_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": customer_360_ui_contract(),
        "owned_tables": CUSTOMER_360_OWNED_TABLES,
        "allowed_database_backends": CUSTOMER_360_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": CUSTOMER_360_REQUIRED_EVENT_TOPIC,
        "emitted_events": CUSTOMER_360_EMITTED_EVENT_TYPES,
        "consumed_events": CUSTOMER_360_CONSUMED_EVENT_TYPES,
        "api_contract": customer_360_build_api_contract(),
        "schema_contract": customer_360_build_schema_contract(),
        "service_contract": customer_360_build_service_contract(),
        "release_evidence_contract": customer_360_build_release_evidence(),
        "permissions_contract": customer_360_permissions_contract(),
        "boundary_contract": customer_360_verify_owned_table_boundary(CUSTOMER_360_OWNED_TABLES),
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

