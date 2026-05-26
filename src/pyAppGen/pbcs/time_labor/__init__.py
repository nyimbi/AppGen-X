"""Time and Labor PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import TIME_LABOR_ALLOWED_DATABASE_BACKENDS
from .runtime import TIME_LABOR_CONSUMED_EVENT_TYPES
from .runtime import TIME_LABOR_EMITTED_EVENT_TYPES
from .runtime import TIME_LABOR_OWNED_TABLES
from .runtime import TIME_LABOR_REQUIRED_EVENT_TOPIC
from .runtime import TIME_LABOR_RUNTIME_CAPABILITY_KEYS
from .runtime import TIME_LABOR_STANDARD_FEATURE_KEYS
from .runtime import time_labor_approve_labor_summary
from .runtime import time_labor_build_api_contract
from .runtime import time_labor_build_release_evidence
from .runtime import time_labor_build_schema_contract
from .runtime import time_labor_build_service_contract
from .runtime import time_labor_build_workbench_view
from .runtime import time_labor_calculate_time_entry
from .runtime import time_labor_configure_runtime
from .runtime import time_labor_create_shift
from .runtime import time_labor_empty_state
from .runtime import time_labor_permissions_contract
from .runtime import time_labor_record_absence
from .runtime import time_labor_record_clock_event
from .runtime import time_labor_receive_event
from .runtime import time_labor_register_rule
from .runtime import time_labor_register_schema_extension
from .runtime import time_labor_runtime_capabilities
from .runtime import time_labor_runtime_smoke
from .runtime import time_labor_set_parameter
from .runtime import time_labor_upsert_employee_projection
from .runtime import time_labor_verify_owned_table_boundary
from .ui import TIME_LABOR_UI_FRAGMENT_KEYS
from .ui import time_labor_render_workbench
from .ui import time_labor_ui_contract

PBC_KEY = "time_labor"


def implementation_contract() -> dict:
    runtime = time_labor_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": time_labor_ui_contract(),
        "api_contract": time_labor_build_api_contract(),
        "schema_contract": time_labor_build_schema_contract(),
        "service_contract": time_labor_build_service_contract(),
        "release_evidence_contract": time_labor_build_release_evidence(),
        "permissions_contract": time_labor_permissions_contract(),
        "owned_tables": TIME_LABOR_OWNED_TABLES,
        "allowed_database_backends": TIME_LABOR_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": TIME_LABOR_REQUIRED_EVENT_TOPIC,
        "consumes": TIME_LABOR_CONSUMED_EVENT_TYPES,
        "emits": TIME_LABOR_EMITTED_EVENT_TYPES,
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

