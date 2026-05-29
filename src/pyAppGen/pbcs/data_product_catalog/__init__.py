"""Data Product Catalog PBC implementation package."""
from __future__ import annotations

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_package_metadata,
    source_pbc_package_contract,
    source_registration_plan,
    validate_source_package_metadata,
)
from .release_evidence import (
    pbc_generation_smoke_audit,
    pbc_implementation_release_audit,
    pbc_source_artifact_contract,
)
from .runtime import *  # noqa: F401,F403
from .ui import data_product_catalog_render_workbench, data_product_catalog_ui_contract

PBC_KEY = "data_product_catalog"


def implementation_contract() -> dict:
    runtime = data_product_catalog_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": data_product_catalog_ui_contract(),
        "api_contract": data_product_catalog_build_api_contract(),
        "schema_contract": data_product_catalog_build_schema_contract(),
        "service_contract": data_product_catalog_build_service_contract(),
        "release_evidence_contract": data_product_catalog_build_release_evidence(),
        "permissions_contract": data_product_catalog_permissions_contract(),
        "owned_tables": DATA_PRODUCT_CATALOG_OWNED_TABLES,
        "runtime_tables": DATA_PRODUCT_CATALOG_RUNTIME_TABLES,
        "allowed_database_backends": DATA_PRODUCT_CATALOG_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": DATA_PRODUCT_CATALOG_REQUIRED_EVENT_TOPIC,
        "emits": DATA_PRODUCT_CATALOG_EMITTED_EVENT_TYPES,
        "consumes": DATA_PRODUCT_CATALOG_CONSUMED_EVENT_TYPES,
        "release_gates": {
            "pbc_source_artifact_contract": pbc_source_artifact_contract(),
            "pbc_implementation_release_audit": pbc_implementation_release_audit(),
            "pbc_generation_smoke_audit": pbc_generation_smoke_audit(),
        },
        "boundary_contract": data_product_catalog_verify_owned_table_boundary(
            DATA_PRODUCT_CATALOG_OWNED_TABLES + ("api_dependency",)
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
    runtime = data_product_catalog_runtime_smoke()
    return {
        "ok": discovery["ok"] and runtime["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "side_effects": (),
    }
