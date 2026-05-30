"""Insurance Policy Administration PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_package_metadata,
    source_pbc_package_contract,
    source_registration_plan,
    validate_source_package_metadata,
)
from .runtime import *
from .ui import (
    policy_administration_insurance_render_standalone_workbench,
    policy_administration_insurance_render_workbench,
    policy_administration_insurance_standalone_workbench_blueprint,
    policy_administration_insurance_ui_contract,
)
from .standalone import (
    PolicyAdministrationInsuranceStandaloneApplication,
    bootstrap_policy_administration_insurance_standalone_app,
    policy_administration_insurance_standalone_app_contract,
    policy_administration_insurance_standalone_smoke,
)
from .release_evidence import build_release_evidence as package_build_release_evidence

PBC_KEY = "policy_administration_insurance"


def implementation_contract() -> dict:
    runtime = policy_administration_insurance_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": policy_administration_insurance_ui_contract(),
        "api_contract": policy_administration_insurance_build_api_contract(),
        "schema_contract": policy_administration_insurance_build_schema_contract(),
        "service_contract": policy_administration_insurance_build_service_contract(),
        "release_evidence_contract": package_build_release_evidence(),
        "permissions_contract": policy_administration_insurance_permissions_contract(),
        "owned_tables": POLICY_ADMINISTRATION_INSURANCE_OWNED_TABLES,
        "runtime_tables": POLICY_ADMINISTRATION_INSURANCE_RUNTIME_TABLES,
        "allowed_database_backends": POLICY_ADMINISTRATION_INSURANCE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": POLICY_ADMINISTRATION_INSURANCE_REQUIRED_EVENT_TOPIC,
        "emits": POLICY_ADMINISTRATION_INSURANCE_EMITTED_EVENT_TYPES,
        "consumes": POLICY_ADMINISTRATION_INSURANCE_CONSUMED_EVENT_TYPES,
        "standalone_app": policy_administration_insurance_standalone_app_contract(),
        "boundary_contract": policy_administration_insurance_verify_owned_table_boundary(
            POLICY_ADMINISTRATION_INSURANCE_OWNED_TABLES + ("api_dependency",)
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
    runtime = policy_administration_insurance_runtime_smoke()
    standalone = policy_administration_insurance_standalone_smoke()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
