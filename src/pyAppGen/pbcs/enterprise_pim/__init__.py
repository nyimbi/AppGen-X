"""Enterprise PIM PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS
from .runtime import ENTERPRISE_PIM_CONSUMED_EVENT_TYPES
from .runtime import ENTERPRISE_PIM_EMITTED_EVENT_TYPES
from .runtime import ENTERPRISE_PIM_OWNED_TABLES
from .runtime import ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC
from .runtime import ENTERPRISE_PIM_RUNTIME_CAPABILITY_KEYS
from .runtime import ENTERPRISE_PIM_STANDARD_FEATURE_KEYS
from .runtime import enterprise_pim_accept_dependency_schema
from .runtime import enterprise_pim_approve_validation_workflow
from .runtime import enterprise_pim_build_api_contract
from .runtime import enterprise_pim_build_release_evidence
from .runtime import enterprise_pim_build_schema_contract
from .runtime import enterprise_pim_build_service_contract
from .runtime import enterprise_pim_build_workbench_view
from .runtime import enterprise_pim_configure_runtime
from .runtime import enterprise_pim_create_taxonomy
from .runtime import enterprise_pim_define_attribute
from .runtime import enterprise_pim_empty_state
from .runtime import enterprise_pim_permissions_contract
from .runtime import enterprise_pim_receive_event
from .runtime import enterprise_pim_register_rule
from .runtime import enterprise_pim_register_schema_extension
from .runtime import enterprise_pim_runtime_capabilities
from .runtime import enterprise_pim_runtime_smoke
from .runtime import enterprise_pim_set_parameter
from .runtime import enterprise_pim_start_validation_workflow
from .runtime import enterprise_pim_upsert_localized_content
from .runtime import enterprise_pim_verify_owned_table_boundary
from .ui import ENTERPRISE_PIM_UI_FRAGMENT_KEYS
from .ui import enterprise_pim_render_workbench
from .ui import enterprise_pim_ui_contract

PBC_KEY = "enterprise_pim"


def implementation_contract() -> dict:
    runtime = enterprise_pim_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": enterprise_pim_ui_contract(),
        "api_contract": enterprise_pim_build_api_contract(),
        "schema_contract": enterprise_pim_build_schema_contract(),
        "service_contract": enterprise_pim_build_service_contract(),
        "release_evidence_contract": enterprise_pim_build_release_evidence(),
        "permissions_contract": enterprise_pim_permissions_contract(),
        "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
        "allowed_database_backends": ENTERPRISE_PIM_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC,
        "consumes": ENTERPRISE_PIM_CONSUMED_EVENT_TYPES,
        "emits": ENTERPRISE_PIM_EMITTED_EVENT_TYPES,
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

