"""Predictive Demand PBC implementation package."""

from .manifest import PBC_MANIFEST

from ..source_contract import source_pbc_package_contract
from ..source_contract import source_package_metadata
from ..source_contract import validate_source_package_metadata
from ..source_contract import source_registration_plan
from .runtime import PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS
from .runtime import PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES
from .runtime import PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES
from .runtime import PREDICTIVE_DEMAND_EVENT_CONTRACT
from .runtime import PREDICTIVE_DEMAND_OWNED_TABLES
from .runtime import PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC
from .runtime import PREDICTIVE_DEMAND_RUNTIME_TABLES
from .runtime import PREDICTIVE_DEMAND_RUNTIME_CAPABILITY_KEYS
from .runtime import PREDICTIVE_DEMAND_STANDARD_FEATURE_KEYS
from .runtime import predictive_demand_build_api_contract
from .runtime import predictive_demand_build_release_evidence
from .runtime import predictive_demand_build_schema_contract
from .runtime import predictive_demand_build_service_contract
from .runtime import predictive_demand_build_workbench_view
from .runtime import predictive_demand_configure_runtime
from .runtime import predictive_demand_create_forecast_run
from .runtime import predictive_demand_empty_state
from .runtime import predictive_demand_ingest_demand_signal
from .runtime import predictive_demand_permissions_contract
from .runtime import predictive_demand_publish_forecast_result
from .runtime import predictive_demand_receive_event
from .runtime import predictive_demand_register_forecast_model
from .runtime import predictive_demand_register_rule
from .runtime import predictive_demand_register_schema_extension
from .runtime import predictive_demand_runtime_capabilities
from .runtime import predictive_demand_runtime_smoke
from .runtime import predictive_demand_set_parameter
from .runtime import predictive_demand_verify_owned_table_boundary
from .ui import PREDICTIVE_DEMAND_UI_FRAGMENT_KEYS
from .ui import predictive_demand_render_workbench
from .ui import predictive_demand_ui_contract

PBC_KEY = "predictive_demand"


def implementation_contract() -> dict:
    runtime = predictive_demand_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": predictive_demand_ui_contract(),
        "api_contract": predictive_demand_build_api_contract(),
        "schema_contract": predictive_demand_build_schema_contract(),
        "service_contract": predictive_demand_build_service_contract(),
        "release_evidence_contract": predictive_demand_build_release_evidence(),
        "permissions_contract": predictive_demand_permissions_contract(),
        "owned_tables": PREDICTIVE_DEMAND_OWNED_TABLES,
        "runtime_tables": PREDICTIVE_DEMAND_RUNTIME_TABLES,
        "allowed_database_backends": PREDICTIVE_DEMAND_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PREDICTIVE_DEMAND_REQUIRED_EVENT_TOPIC,
        "event_contract": PREDICTIVE_DEMAND_EVENT_CONTRACT,
        "emits": PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES,
        "consumes": PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES,
        "emitted_events": PREDICTIVE_DEMAND_EMITTED_EVENT_TYPES,
        "consumed_events": PREDICTIVE_DEMAND_CONSUMED_EVENT_TYPES,
        "boundary_contract": predictive_demand_verify_owned_table_boundary(
            PREDICTIVE_DEMAND_OWNED_TABLES
        ),
        "shared_table_access": False,
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

