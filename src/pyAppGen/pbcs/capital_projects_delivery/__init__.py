"""Capital Projects Delivery PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_package_metadata,
    source_pbc_package_contract,
    source_registration_plan,
    validate_source_package_metadata,
)
from .runtime import *
from .ui import (
    capital_projects_delivery_render_workbench,
    capital_projects_delivery_ui_contract,
)

PBC_KEY = "capital_projects_delivery"


def implementation_contract() -> dict:
    runtime = capital_projects_delivery_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": capital_projects_delivery_ui_contract(),
        "api_contract": capital_projects_delivery_build_api_contract(),
        "schema_contract": capital_projects_delivery_build_schema_contract(),
        "service_contract": capital_projects_delivery_build_service_contract(),
        "release_evidence_contract": capital_projects_delivery_build_release_evidence(),
        "permissions_contract": capital_projects_delivery_permissions_contract(),
        "forms_contract": capital_projects_delivery_build_forms_contract(),
        "wizards_contract": capital_projects_delivery_build_wizards_contract(),
        "controls_contract": capital_projects_delivery_build_controls_contract(),
        "agent_help_contract": capital_projects_delivery_build_agent_help_contract(),
        "single_pbc_app_contract": capital_projects_delivery_build_single_pbc_app_contract(),
        "owned_tables": CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES,
        "runtime_tables": CAPITAL_PROJECTS_DELIVERY_RUNTIME_TABLES,
        "allowed_database_backends": CAPITAL_PROJECTS_DELIVERY_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": CAPITAL_PROJECTS_DELIVERY_REQUIRED_EVENT_TOPIC,
        "emits": CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES,
        "consumes": CAPITAL_PROJECTS_DELIVERY_CONSUMED_EVENT_TYPES,
        "boundary_contract": capital_projects_delivery_verify_owned_table_boundary(
            CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES + ("api_dependency",)
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
    runtime = capital_projects_delivery_runtime_smoke()
    return {"ok": discovery["ok"] and runtime["ok"], "discovery": discovery, "runtime": runtime, "side_effects": ()}
