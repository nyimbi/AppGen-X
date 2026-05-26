"""Service Ticketing PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS
from .runtime import SERVICE_TICKETING_CONSUMED_EVENT_TYPES
from .runtime import SERVICE_TICKETING_EMITTED_EVENT_TYPES
from .runtime import SERVICE_TICKETING_OWNED_TABLES
from .runtime import SERVICE_TICKETING_REQUIRED_EVENT_TOPIC
from .runtime import SERVICE_TICKETING_RUNTIME_CAPABILITY_KEYS
from .runtime import SERVICE_TICKETING_RUNTIME_TABLES
from .runtime import SERVICE_TICKETING_STANDARD_FEATURE_KEYS
from .runtime import service_ticketing_assign_ticket
from .runtime import service_ticketing_build_api_contract
from .runtime import service_ticketing_build_release_evidence
from .runtime import service_ticketing_build_schema_contract
from .runtime import service_ticketing_build_service_contract
from .runtime import service_ticketing_build_workbench_view
from .runtime import service_ticketing_configure_runtime
from .runtime import service_ticketing_create_sla_policy
from .runtime import service_ticketing_empty_state
from .runtime import service_ticketing_open_ticket
from .runtime import service_ticketing_permissions_contract
from .runtime import service_ticketing_receive_event
from .runtime import service_ticketing_record_escalation
from .runtime import service_ticketing_register_rule
from .runtime import service_ticketing_register_schema_extension
from .runtime import service_ticketing_resolve_ticket
from .runtime import service_ticketing_run_control_tests
from .runtime import service_ticketing_runtime_capabilities
from .runtime import service_ticketing_runtime_smoke
from .runtime import service_ticketing_set_parameter
from .runtime import service_ticketing_ui_binding_contract
from .runtime import service_ticketing_verify_owned_table_boundary
from .ui import SERVICE_TICKETING_UI_FRAGMENT_KEYS
from .ui import service_ticketing_render_workbench
from .ui import service_ticketing_ui_contract

PBC_KEY = "service_ticketing"


def implementation_contract() -> dict:
    runtime = service_ticketing_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": service_ticketing_ui_contract(),
        "owned_tables": SERVICE_TICKETING_OWNED_TABLES,
        "runtime_tables": SERVICE_TICKETING_RUNTIME_TABLES,
        "allowed_database_backends": SERVICE_TICKETING_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": SERVICE_TICKETING_REQUIRED_EVENT_TOPIC,
        "emitted_events": SERVICE_TICKETING_EMITTED_EVENT_TYPES,
        "consumed_events": SERVICE_TICKETING_CONSUMED_EVENT_TYPES,
        "api_contract": service_ticketing_build_api_contract(),
        "schema_contract": service_ticketing_build_schema_contract(),
        "service_contract": service_ticketing_build_service_contract(),
        "release_evidence_contract": service_ticketing_build_release_evidence(),
        "permissions_contract": service_ticketing_permissions_contract(),
        "ui_binding_contract": service_ticketing_ui_binding_contract(),
        "boundary_contract": service_ticketing_verify_owned_table_boundary(SERVICE_TICKETING_OWNED_TABLES),
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

