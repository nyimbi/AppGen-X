"""Laboratory Information Management PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .runtime import *
from .standalone import bootstrap_standalone_app
from .standalone import standalone_manifest
from .standalone import standalone_smoke_test
from .ui import laboratory_information_management_render_standalone_workbench
from .ui import laboratory_information_management_render_workbench
from .ui import laboratory_information_management_standalone_workbench_blueprint
from .ui import laboratory_information_management_ui_contract

PBC_KEY = "laboratory_information_management"


def implementation_contract() -> dict:
    runtime = laboratory_information_management_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": laboratory_information_management_ui_contract(),
        "api_contract": laboratory_information_management_build_api_contract(),
        "schema_contract": laboratory_information_management_build_schema_contract(),
        "service_contract": laboratory_information_management_build_service_contract(),
        "release_evidence_contract": laboratory_information_management_build_release_evidence(),
        "permissions_contract": laboratory_information_management_permissions_contract(),
        "owned_tables": LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES,
        "runtime_tables": LABORATORY_INFORMATION_MANAGEMENT_RUNTIME_TABLES,
        "allowed_database_backends": LABORATORY_INFORMATION_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": LABORATORY_INFORMATION_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "emits": LABORATORY_INFORMATION_MANAGEMENT_EMITTED_EVENT_TYPES,
        "consumes": LABORATORY_INFORMATION_MANAGEMENT_CONSUMED_EVENT_TYPES,
        "boundary_contract": laboratory_information_management_verify_owned_table_boundary(LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES + ("api_dependency",)),
        "standalone_app_contract": standalone_manifest(),
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
    runtime = laboratory_information_management_runtime_smoke()
    standalone = standalone_smoke_test()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
