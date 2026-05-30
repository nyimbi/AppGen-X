"""Gaming and Casino Operations PBC implementation package."""

from __future__ import annotations

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_package_metadata,
    source_pbc_package_contract,
    source_registration_plan,
    validate_source_package_metadata,
)
from .runtime import *  # noqa: F401,F403
from .runtime import (
    GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    GAMING_CASINO_OPERATIONS_CONSUMED_EVENT_TYPES,
    GAMING_CASINO_OPERATIONS_EMITTED_EVENT_TYPES,
    GAMING_CASINO_OPERATIONS_OWNED_TABLES,
    GAMING_CASINO_OPERATIONS_REQUIRED_EVENT_TOPIC,
    GAMING_CASINO_OPERATIONS_RUNTIME_TABLES,
    gaming_casino_operations_build_api_contract,
    gaming_casino_operations_build_release_evidence,
    gaming_casino_operations_build_schema_contract,
    gaming_casino_operations_build_service_contract,
    gaming_casino_operations_permissions_contract,
    gaming_casino_operations_runtime_capabilities,
    gaming_casino_operations_runtime_smoke,
    gaming_casino_operations_verify_owned_table_boundary,
)
from .standalone import (
    GamingCasinoOperationsStandaloneApplication,
    gaming_casino_operations_bootstrap_standalone_app,
    gaming_casino_operations_standalone_app_contract,
    gaming_casino_operations_standalone_app_smoke,
)
from .ui import gaming_casino_operations_render_workbench, gaming_casino_operations_ui_contract


PBC_KEY = "gaming_casino_operations"


def implementation_contract() -> dict:
    runtime = gaming_casino_operations_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": gaming_casino_operations_ui_contract(),
        "api_contract": gaming_casino_operations_build_api_contract(),
        "schema_contract": gaming_casino_operations_build_schema_contract(),
        "service_contract": gaming_casino_operations_build_service_contract(),
        "release_evidence_contract": gaming_casino_operations_build_release_evidence(),
        "permissions_contract": gaming_casino_operations_permissions_contract(),
        "standalone_app_contract": gaming_casino_operations_standalone_app_contract(),
        "owned_tables": GAMING_CASINO_OPERATIONS_OWNED_TABLES,
        "runtime_tables": GAMING_CASINO_OPERATIONS_RUNTIME_TABLES,
        "allowed_database_backends": GAMING_CASINO_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": GAMING_CASINO_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "emits": GAMING_CASINO_OPERATIONS_EMITTED_EVENT_TYPES,
        "consumes": GAMING_CASINO_OPERATIONS_CONSUMED_EVENT_TYPES,
        "boundary_contract": gaming_casino_operations_verify_owned_table_boundary(GAMING_CASINO_OPERATIONS_OWNED_TABLES),
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
    runtime = gaming_casino_operations_runtime_smoke()
    standalone = gaming_casino_operations_standalone_app_smoke()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
