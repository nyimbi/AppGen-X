"""Material Requirements Planning Engine PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import MRP_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import MRP_ENGINE_CONSUMED_EVENT_TYPES
from .runtime import MRP_ENGINE_EMITTED_EVENT_TYPES
from .runtime import MRP_ENGINE_OWNED_TABLES
from .runtime import MRP_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import MRP_ENGINE_RUNTIME_CAPABILITY_KEYS
from .runtime import MRP_ENGINE_STANDARD_FEATURE_KEYS
from .runtime import mrp_engine_build_api_contract
from .runtime import mrp_engine_build_release_evidence
from .runtime import mrp_engine_build_schema_contract
from .runtime import mrp_engine_build_service_contract
from .runtime import mrp_engine_build_workbench_view
from .runtime import mrp_engine_calculate_material_plan
from .runtime import mrp_engine_configure_runtime
from .runtime import mrp_engine_create_mrp_run
from .runtime import mrp_engine_empty_state
from .runtime import mrp_engine_explode_bom
from .runtime import mrp_engine_ingest_demand_projection
from .runtime import mrp_engine_ingest_inventory_projection
from .runtime import mrp_engine_permissions_contract
from .runtime import mrp_engine_register_bom
from .runtime import mrp_engine_register_rule
from .runtime import mrp_engine_register_schema_extension
from .runtime import mrp_engine_release_planned_order
from .runtime import mrp_engine_receive_event
from .runtime import mrp_engine_runtime_capabilities
from .runtime import mrp_engine_runtime_smoke
from .runtime import mrp_engine_set_parameter
from .runtime import mrp_engine_verify_owned_table_boundary
from .ui import MRP_ENGINE_UI_FRAGMENT_KEYS
from .ui import mrp_engine_render_workbench
from .ui import mrp_engine_ui_contract

PBC_KEY = "mrp_engine"


def implementation_contract() -> dict:
    runtime = mrp_engine_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": mrp_engine_ui_contract(),
        "api_contract": mrp_engine_build_api_contract(),
        "schema_contract": mrp_engine_build_schema_contract(),
        "service_contract": mrp_engine_build_service_contract(),
        "release_evidence_contract": mrp_engine_build_release_evidence(),
        "permissions_contract": mrp_engine_permissions_contract(),
        "owned_tables": MRP_ENGINE_OWNED_TABLES,
        "allowed_database_backends": MRP_ENGINE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": MRP_ENGINE_REQUIRED_EVENT_TOPIC,
        "consumes": MRP_ENGINE_CONSUMED_EVENT_TYPES,
        "emits": MRP_ENGINE_EMITTED_EVENT_TYPES,
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

