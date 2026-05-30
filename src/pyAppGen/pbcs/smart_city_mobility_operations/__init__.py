"""Smart City Mobility Operations PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_pbc_package_contract,
    source_package_metadata,
    source_registration_plan,
    validate_source_package_metadata,
)
from .runtime import *
from .standalone import (
    smart_city_mobility_operations_bootstrap_standalone_app,
    smart_city_mobility_operations_standalone_app_contract,
    smart_city_mobility_operations_standalone_app_smoke,
)
from .ui import (
    smart_city_mobility_operations_render_workbench,
    smart_city_mobility_operations_ui_contract,
)

PBC_KEY = "smart_city_mobility_operations"


def implementation_contract() -> dict:
    runtime = smart_city_mobility_operations_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": smart_city_mobility_operations_ui_contract(),
        "api_contract": smart_city_mobility_operations_build_api_contract(),
        "schema_contract": smart_city_mobility_operations_build_schema_contract(),
        "service_contract": smart_city_mobility_operations_build_service_contract(),
        "release_evidence_contract": smart_city_mobility_operations_build_release_evidence(),
        "permissions_contract": smart_city_mobility_operations_permissions_contract(),
        "owned_tables": SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES,
        "runtime_tables": SMART_CITY_MOBILITY_OPERATIONS_RUNTIME_TABLES,
        "allowed_database_backends": SMART_CITY_MOBILITY_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": SMART_CITY_MOBILITY_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "emits": SMART_CITY_MOBILITY_OPERATIONS_EMITTED_EVENT_TYPES,
        "consumes": SMART_CITY_MOBILITY_OPERATIONS_CONSUMED_EVENT_TYPES,
        "boundary_contract": smart_city_mobility_operations_verify_owned_table_boundary(
            SMART_CITY_MOBILITY_OPERATIONS_OWNED_TABLES + ("api_dependency",)
        ),
        "standalone_app_contract": smart_city_mobility_operations_standalone_app_contract(),
    }


def register_pbc() -> dict:
    return dict(PBC_MANIFEST)


def registration_plan(existing_catalog: dict | None = None) -> dict:
    return source_registration_plan(PBC_KEY, register_pbc(), existing_catalog=existing_catalog)


def package_metadata_manifest() -> dict:
    return source_package_metadata(PBC_KEY, register_pbc(), implementation_contract())


def validate_package_metadata() -> dict:
    return validate_source_package_metadata(package_metadata_manifest())


def package_discovery_plan(existing_catalog: dict | None = None) -> dict:
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
    discovery = package_discovery_plan()
    runtime = smart_city_mobility_operations_runtime_smoke()
    standalone = smart_city_mobility_operations_standalone_app_smoke()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
