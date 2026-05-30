"""Identity KYC / AML compliance PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_package_metadata,
    source_pbc_package_contract,
    source_registration_plan,
    validate_source_package_metadata,
)
from .runtime import *
from .ui import (
    identity_kyc_aml_compliance_render_workbench,
    identity_kyc_aml_compliance_ui_contract,
)

PBC_KEY = "identity_kyc_aml_compliance"


def implementation_contract() -> dict:
    runtime = identity_kyc_aml_compliance_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": identity_kyc_aml_compliance_ui_contract(),
        "api_contract": identity_kyc_aml_compliance_build_api_contract(),
        "schema_contract": identity_kyc_aml_compliance_build_schema_contract(),
        "service_contract": identity_kyc_aml_compliance_build_service_contract(),
        "release_evidence_contract": identity_kyc_aml_compliance_build_release_evidence(),
        "permissions_contract": identity_kyc_aml_compliance_permissions_contract(),
        "owned_tables": IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES,
        "runtime_tables": IDENTITY_KYC_AML_COMPLIANCE_RUNTIME_TABLES,
        "allowed_database_backends": IDENTITY_KYC_AML_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": IDENTITY_KYC_AML_COMPLIANCE_REQUIRED_EVENT_TOPIC,
        "emits": IDENTITY_KYC_AML_COMPLIANCE_EMITTED_EVENT_TYPES,
        "consumes": IDENTITY_KYC_AML_COMPLIANCE_CONSUMED_EVENT_TYPES,
        "boundary_contract": identity_kyc_aml_compliance_verify_owned_table_boundary(IDENTITY_KYC_AML_COMPLIANCE_OWNED_TABLES),
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
    runtime = identity_kyc_aml_compliance_runtime_smoke()
    return {"ok": discovery["ok"] and runtime["ok"], "discovery": discovery, "runtime": runtime, "side_effects": ()}
