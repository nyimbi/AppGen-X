"""Quality Assurance PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS
from .runtime import QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES
from .runtime import QUALITY_ASSURANCE_EMITTED_EVENT_TYPES
from .runtime import QUALITY_ASSURANCE_OWNED_TABLES
from .runtime import QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC
from .runtime import QUALITY_ASSURANCE_RUNTIME_CAPABILITY_KEYS
from .runtime import QUALITY_ASSURANCE_RUNTIME_TABLES
from .runtime import QUALITY_ASSURANCE_SCHEMA_TABLES
from .runtime import QUALITY_ASSURANCE_STANDARD_FEATURE_KEYS
from .runtime import quality_assurance_build_api_contract
from .runtime import quality_assurance_build_release_evidence
from .runtime import quality_assurance_build_schema_contract
from .runtime import quality_assurance_build_service_contract
from .runtime import quality_assurance_build_workbench_view
from .runtime import quality_assurance_configure_runtime
from .runtime import quality_assurance_create_inspection_plan
from .runtime import quality_assurance_create_quality_hold
from .runtime import quality_assurance_disposition_nonconformance
from .runtime import quality_assurance_empty_state
from .runtime import quality_assurance_permissions_contract
from .runtime import quality_assurance_raise_nonconformance
from .runtime import quality_assurance_receive_event
from .runtime import quality_assurance_record_inspection_result
from .runtime import quality_assurance_register_rule
from .runtime import quality_assurance_register_schema_extension
from .runtime import quality_assurance_release_quality_hold
from .runtime import quality_assurance_runtime_capabilities
from .runtime import quality_assurance_runtime_smoke
from .runtime import quality_assurance_set_parameter
from .runtime import quality_assurance_ui_binding_contract
from .runtime import quality_assurance_verify_owned_table_boundary
from .ui import QUALITY_ASSURANCE_UI_FRAGMENT_KEYS
from .ui import quality_assurance_render_workbench
from .ui import quality_assurance_ui_contract

PBC_KEY = "quality_assurance"


def implementation_contract() -> dict:
    runtime = quality_assurance_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": quality_assurance_ui_contract(),
        "owned_tables": QUALITY_ASSURANCE_OWNED_TABLES,
        "runtime_tables": QUALITY_ASSURANCE_RUNTIME_TABLES,
        "schema_tables": QUALITY_ASSURANCE_SCHEMA_TABLES,
        "allowed_database_backends": QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": QUALITY_ASSURANCE_REQUIRED_EVENT_TOPIC,
        "emitted_events": QUALITY_ASSURANCE_EMITTED_EVENT_TYPES,
        "consumed_events": QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES,
        "emits": QUALITY_ASSURANCE_EMITTED_EVENT_TYPES,
        "consumes": QUALITY_ASSURANCE_CONSUMED_EVENT_TYPES,
        "api_contract": quality_assurance_build_api_contract(),
        "schema_contract": quality_assurance_build_schema_contract(),
        "service_contract": quality_assurance_build_service_contract(),
        "release_evidence_contract": quality_assurance_build_release_evidence(),
        "ui_binding_contract": quality_assurance_ui_binding_contract(),
        "permissions_contract": quality_assurance_permissions_contract(),
        "boundary_contract": quality_assurance_verify_owned_table_boundary(QUALITY_ASSURANCE_OWNED_TABLES),
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

