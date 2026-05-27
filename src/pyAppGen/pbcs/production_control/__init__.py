"""Production Control PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS
from .runtime import PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES
from .runtime import PRODUCTION_CONTROL_EMITTED_EVENT_TYPES
from .runtime import PRODUCTION_CONTROL_OWNED_TABLES
from .runtime import PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC
from .runtime import PRODUCTION_CONTROL_RUNTIME_CAPABILITY_KEYS
from .runtime import PRODUCTION_CONTROL_STANDARD_FEATURE_KEYS
from .runtime import production_control_build_api_contract
from .runtime import production_control_build_release_evidence
from .runtime import production_control_build_schema_contract
from .runtime import production_control_build_service_contract
from .runtime import production_control_build_workbench_view
from .runtime import production_control_allocate_capacity_plan
from .runtime import production_control_append_audit_entry
from .runtime import production_control_book_labor_time
from .runtime import production_control_book_machine_time
from .runtime import production_control_capture_oee_snapshot
from .runtime import production_control_complete_production_order
from .runtime import production_control_configure_runtime
from .runtime import production_control_confirm_operation
from .runtime import production_control_create_production_order
from .runtime import production_control_define_routing_step
from .runtime import production_control_empty_state
from .runtime import production_control_open_exception_case
from .runtime import production_control_permissions_contract
from .runtime import production_control_record_downtime
from .runtime import production_control_record_completion_proof
from .runtime import production_control_record_material_consumption
from .runtime import production_control_record_quality_gate_result
from .runtime import production_control_record_scrap_rework
from .runtime import production_control_receive_event
from .runtime import production_control_register_rule
from .runtime import production_control_register_schema_extension
from .runtime import production_control_register_work_center
from .runtime import production_control_runtime_capabilities
from .runtime import production_control_runtime_smoke
from .runtime import production_control_schedule_order
from .runtime import production_control_set_parameter
from .runtime import production_control_start_operation
from .runtime import production_control_verify_owned_table_boundary
from .ui import PRODUCTION_CONTROL_UI_FRAGMENT_KEYS
from .ui import production_control_render_workbench
from .ui import production_control_ui_contract

PBC_KEY = "production_control"


def implementation_contract() -> dict:
    runtime = production_control_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": production_control_ui_contract(),
        "api_contract": production_control_build_api_contract(),
        "schema_contract": production_control_build_schema_contract(),
        "service_contract": production_control_build_service_contract(),
        "release_evidence_contract": production_control_build_release_evidence(),
        "permissions_contract": production_control_permissions_contract(),
        "owned_tables": PRODUCTION_CONTROL_OWNED_TABLES,
        "allowed_database_backends": PRODUCTION_CONTROL_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PRODUCTION_CONTROL_REQUIRED_EVENT_TOPIC,
        "emitted_events": PRODUCTION_CONTROL_EMITTED_EVENT_TYPES,
        "consumed_events": PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES,
        "emits": PRODUCTION_CONTROL_EMITTED_EVENT_TYPES,
        "consumes": PRODUCTION_CONTROL_CONSUMED_EVENT_TYPES,
        "boundary_contract": production_control_verify_owned_table_boundary(PRODUCTION_CONTROL_OWNED_TABLES),
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
