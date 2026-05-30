"""Food Safety Quality Compliance PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .runtime import *
from .ui import food_safety_quality_compliance_render_workbench
from .ui import food_safety_quality_compliance_ui_contract

PBC_KEY = "food_safety_quality_compliance"


def implementation_contract() -> dict:
    runtime = food_safety_quality_compliance_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": food_safety_quality_compliance_ui_contract(),
        "api_contract": food_safety_quality_compliance_build_api_contract(),
        "schema_contract": food_safety_quality_compliance_build_schema_contract(),
        "service_contract": food_safety_quality_compliance_build_service_contract(),
        "release_evidence_contract": food_safety_quality_compliance_build_release_evidence(),
        "permissions_contract": food_safety_quality_compliance_permissions_contract(),
        "owned_tables": FOOD_SAFETY_QUALITY_COMPLIANCE_OWNED_TABLES,
        "runtime_tables": FOOD_SAFETY_QUALITY_COMPLIANCE_RUNTIME_TABLES,
        "allowed_database_backends": FOOD_SAFETY_QUALITY_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": FOOD_SAFETY_QUALITY_COMPLIANCE_REQUIRED_EVENT_TOPIC,
        "emits": FOOD_SAFETY_QUALITY_COMPLIANCE_EMITTED_EVENT_TYPES,
        "consumes": FOOD_SAFETY_QUALITY_COMPLIANCE_CONSUMED_EVENT_TYPES,
        "boundary_contract": food_safety_quality_compliance_verify_owned_table_boundary(FOOD_SAFETY_QUALITY_COMPLIANCE_OWNED_TABLES),
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
    runtime = food_safety_quality_compliance_runtime_smoke()
    return {"ok": discovery["ok"] and runtime["ok"], "discovery": discovery, "runtime": runtime, "side_effects": ()}
