"""Insurance underwriting standalone PBC package."""

from __future__ import annotations

from ..source_contract import (
    source_package_metadata,
    source_pbc_package_contract,
    source_registration_plan,
    validate_source_package_metadata,
)
from .manifest import PBC_MANIFEST
from .release_evidence import build_release_evidence
from .runtime import *
from .standalone import insurance_underwriting_standalone_app_contract, insurance_underwriting_standalone_app_smoke
from .ui import insurance_underwriting_ui_contract


PBC_KEY = "insurance_underwriting"


def implementation_contract() -> dict:
    runtime = insurance_underwriting_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": insurance_underwriting_ui_contract(),
        "api_contract": insurance_underwriting_build_api_contract(),
        "schema_contract": insurance_underwriting_build_schema_contract(),
        "service_contract": insurance_underwriting_build_service_contract(),
        "release_evidence_contract": build_release_evidence(),
        "permissions_contract": insurance_underwriting_permissions_contract(),
        "standalone_app": insurance_underwriting_standalone_app_contract(),
        "owned_tables": INSURANCE_UNDERWRITING_OWNED_TABLES,
        "runtime_tables": INSURANCE_UNDERWRITING_RUNTIME_TABLES,
        "allowed_database_backends": INSURANCE_UNDERWRITING_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": INSURANCE_UNDERWRITING_REQUIRED_EVENT_TOPIC,
        "emits": INSURANCE_UNDERWRITING_EMITTED_EVENT_TYPES,
        "consumes": INSURANCE_UNDERWRITING_CONSUMED_EVENT_TYPES,
        "boundary_contract": insurance_underwriting_verify_owned_table_boundary(INSURANCE_UNDERWRITING_OWNED_TABLES + ("api_dependency",)),
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
    runtime = insurance_underwriting_runtime_smoke()
    standalone = insurance_underwriting_standalone_app_smoke()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
