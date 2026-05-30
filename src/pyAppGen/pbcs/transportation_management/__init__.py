"""Transportation Management PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS
from .runtime import TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES
from .runtime import TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES
from .runtime import TRANSPORTATION_MANAGEMENT_OWNED_TABLES
from .runtime import TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC
from .runtime import TRANSPORTATION_MANAGEMENT_RUNTIME_CAPABILITY_KEYS
from .runtime import TRANSPORTATION_MANAGEMENT_STANDARD_FEATURE_KEYS
from .runtime import transportation_management_build_api_contract
from .runtime import transportation_management_build_release_evidence
from .runtime import transportation_management_build_schema_contract
from .runtime import transportation_management_build_service_contract
from .runtime import transportation_management_build_workbench_view
from .runtime import transportation_management_calculate_eta
from .runtime import transportation_management_configure_runtime
from .runtime import transportation_management_confirm_delivery
from .runtime import transportation_management_create_shipment
from .runtime import transportation_management_dispatch_shipment
from .runtime import transportation_management_empty_state
from .runtime import transportation_management_plan_route
from .runtime import transportation_management_record_tracking_event
from .runtime import transportation_management_register_carrier
from .runtime import transportation_management_register_rule
from .runtime import transportation_management_register_schema_extension
from .runtime import transportation_management_permissions_contract
from .runtime import transportation_management_receive_event
from .runtime import transportation_management_runtime_capabilities
from .runtime import transportation_management_runtime_smoke
from .runtime import transportation_management_select_carrier
from .runtime import transportation_management_set_parameter
from .runtime import transportation_management_verify_owned_table_boundary
from .ui import TRANSPORTATION_MANAGEMENT_UI_FRAGMENT_KEYS
from .ui import transportation_management_render_workbench
from .ui import transportation_management_ui_contract

PBC_KEY = "transportation_management"


def implementation_contract() -> dict:
    runtime = transportation_management_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": TRANSPORTATION_MANAGEMENT_OWNED_TABLES,
        "allowed_database_backends": TRANSPORTATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "api_contract": transportation_management_build_api_contract(),
        "schema_contract": transportation_management_build_schema_contract(),
        "service_contract": transportation_management_build_service_contract(),
        "release_evidence_contract": transportation_management_build_release_evidence(),
        "permissions_contract": transportation_management_permissions_contract(),
        "required_event_topic": TRANSPORTATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "consumes": TRANSPORTATION_MANAGEMENT_CONSUMED_EVENT_TYPES,
        "emits": TRANSPORTATION_MANAGEMENT_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime,
        "ui_contract": transportation_management_ui_contract(),
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



from .repository import TransportationManagementRepository
from .repository import transportation_management_repository_contract
from .standalone import TransportationManagementStandaloneApp
from .standalone import standalone_app_manifest
from .ui import transportation_management_render_standalone_app
from .ui import transportation_management_standalone_app_contract
