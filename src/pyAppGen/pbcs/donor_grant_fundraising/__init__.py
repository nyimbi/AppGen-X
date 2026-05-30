"""Donor Grant and Fundraising PBC implementation package."""

from .manifest import PBC_MANIFEST
from .runtime import *
from .standalone import DonorGrantFundraisingStandaloneApplication, standalone_manifest, standalone_smoke_test
from .ui import donor_grant_fundraising_render_workbench, donor_grant_fundraising_ui_contract
from ..source_contract import source_package_metadata, source_pbc_package_contract, source_registration_plan, validate_source_package_metadata

PBC_KEY = "donor_grant_fundraising"


def implementation_contract() -> dict:
    runtime = donor_grant_fundraising_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": donor_grant_fundraising_ui_contract(),
        "api_contract": donor_grant_fundraising_build_api_contract(),
        "schema_contract": donor_grant_fundraising_build_schema_contract(),
        "service_contract": donor_grant_fundraising_build_service_contract(),
        "release_evidence_contract": donor_grant_fundraising_build_release_evidence(),
        "permissions_contract": donor_grant_fundraising_permissions_contract(),
        "owned_tables": DONOR_GRANT_FUNDRAISING_OWNED_TABLES,
        "runtime_tables": DONOR_GRANT_FUNDRAISING_RUNTIME_TABLES,
        "allowed_database_backends": DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC,
        "emits": DONOR_GRANT_FUNDRAISING_EMITTED_EVENT_TYPES,
        "consumes": DONOR_GRANT_FUNDRAISING_CONSUMED_EVENT_TYPES,
        "boundary_contract": donor_grant_fundraising_verify_owned_table_boundary(DONOR_GRANT_FUNDRAISING_OWNED_TABLES + ("api_dependency",)),
        "standalone": standalone_manifest(),
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
    runtime = donor_grant_fundraising_runtime_smoke()
    standalone = standalone_smoke_test()
    return {"ok": discovery["ok"] and runtime["ok"] and standalone["ok"], "discovery": discovery, "runtime": runtime, "standalone": standalone, "side_effects": ()}
