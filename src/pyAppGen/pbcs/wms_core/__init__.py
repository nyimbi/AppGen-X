"""Warehouse Management Core PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .release_evidence import build_release_evidence as package_build_release_evidence
from .runtime import WMS_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import WMS_CORE_CONSUMED_EVENT_TYPES
from .runtime import WMS_CORE_EMITTED_EVENT_TYPES
from .runtime import WMS_CORE_OWNED_TABLES
from .runtime import WMS_CORE_REQUIRED_EVENT_TOPIC
from .runtime import WMS_CORE_RUNTIME_CAPABILITY_KEYS
from .runtime import WMS_CORE_STANDARD_FEATURE_KEYS
from .runtime import wms_core_allocate_labor_tasks
from .runtime import wms_core_build_api_contract
from .runtime import wms_core_build_release_evidence
from .runtime import wms_core_build_schema_contract
from .runtime import wms_core_build_service_contract
from .runtime import wms_core_build_workbench_view
from .runtime import wms_core_configure_runtime
from .runtime import wms_core_confirm_pack
from .runtime import wms_core_confirm_putaway
from .runtime import wms_core_confirm_shipment
from .runtime import wms_core_create_pack_task
from .runtime import wms_core_create_pick_wave
from .runtime import wms_core_create_putaway_task
from .runtime import wms_core_detect_warehouse_anomaly
from .runtime import wms_core_empty_state
from .runtime import wms_core_execute_pick
from .runtime import wms_core_generate_shipment_proof
from .runtime import wms_core_receive_event
from .runtime import wms_core_receive_inbound
from .runtime import wms_core_register_bin
from .runtime import wms_core_register_governed_model
from .runtime import wms_core_register_rule
from .runtime import wms_core_register_schema_extension
from .runtime import wms_core_register_warehouse
from .runtime import wms_core_route_edge_command
from .runtime import wms_core_run_control_tests
from .runtime import wms_core_runtime_capabilities
from .runtime import wms_core_runtime_smoke
from .runtime import wms_core_set_parameter
from .runtime import wms_core_verify_owned_table_boundary
from .runtime import wms_core_permissions_contract
from .repository import WmsCoreRepository
from .repository import wms_core_repository_contract
from .standalone import WmsCoreStandaloneApp
from .standalone import standalone_app_manifest
from .ui import WMS_CORE_UI_FRAGMENT_KEYS
from .ui import wms_core_render_standalone_app
from .ui import wms_core_render_workbench
from .ui import wms_core_standalone_app_contract
from .ui import wms_core_ui_contract

PBC_KEY = "wms_core"


def implementation_contract() -> dict:
    runtime = wms_core_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "owned_tables": WMS_CORE_OWNED_TABLES,
        "allowed_database_backends": WMS_CORE_ALLOWED_DATABASE_BACKENDS,
        "api_contract": wms_core_build_api_contract(),
        "schema_contract": wms_core_build_schema_contract(),
        "service_contract": wms_core_build_service_contract(),
        "release_evidence_contract": package_build_release_evidence(),
        "permissions_contract": wms_core_permissions_contract(),
        "required_event_topic": WMS_CORE_REQUIRED_EVENT_TOPIC,
        "consumes": WMS_CORE_CONSUMED_EVENT_TYPES,
        "emits": WMS_CORE_EMITTED_EVENT_TYPES,
        "advanced_runtime": runtime,
        "ui_contract": wms_core_ui_contract(),
        "repository_contract": wms_core_repository_contract(),
        "standalone_app_contract": wms_core_standalone_app_contract(),
        "standalone_app_manifest": standalone_app_manifest(),
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
