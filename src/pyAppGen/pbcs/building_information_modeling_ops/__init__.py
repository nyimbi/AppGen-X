"""Building Information Modeling Operations PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_package_metadata,
    source_pbc_package_contract,
    source_registration_plan,
    validate_source_package_metadata,
)
from .runtime import *
from .standalone import (
    BuildingInformationModelingOpsStandaloneApp,
    standalone_app_manifest,
)
from .ui import (
    building_information_modeling_ops_render_workbench,
    building_information_modeling_ops_ui_contract,
)

PBC_KEY = "building_information_modeling_ops"


def implementation_contract() -> dict:
    runtime = building_information_modeling_ops_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": building_information_modeling_ops_ui_contract(),
        "api_contract": building_information_modeling_ops_build_api_contract(),
        "schema_contract": building_information_modeling_ops_build_schema_contract(),
        "service_contract": building_information_modeling_ops_build_service_contract(),
        "release_evidence_contract": building_information_modeling_ops_build_release_evidence(),
        "permissions_contract": building_information_modeling_ops_permissions_contract(),
        "standalone_app": standalone_app_manifest(),
        "owned_tables": BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES,
        "runtime_tables": BUILDING_INFORMATION_MODELING_OPS_RUNTIME_TABLES,
        "allowed_database_backends": BUILDING_INFORMATION_MODELING_OPS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": BUILDING_INFORMATION_MODELING_OPS_REQUIRED_EVENT_TOPIC,
        "emits": BUILDING_INFORMATION_MODELING_OPS_EMITTED_EVENT_TYPES,
        "consumes": BUILDING_INFORMATION_MODELING_OPS_CONSUMED_EVENT_TYPES,
        "boundary_contract": building_information_modeling_ops_verify_owned_table_boundary(
            BUILDING_INFORMATION_MODELING_OPS_OWNED_TABLES + ("api_dependency",)
        ),
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
    runtime = building_information_modeling_ops_runtime_smoke()
    standalone = standalone_app_manifest()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
