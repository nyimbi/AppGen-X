"""Provider Revenue Cycle PBC implementation package."""

from __future__ import annotations

from .manifest import PBC_MANIFEST
from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .audit import run_provider_revenue_cycle_pbc_audit
from .release_evidence import build_release_evidence
from .runtime import *
from .standalone import standalone_manifest
from .ui import provider_revenue_cycle_render_workbench
from .ui import provider_revenue_cycle_ui_contract

PBC_KEY = "provider_revenue_cycle"


def implementation_contract() -> dict:
    runtime = provider_revenue_cycle_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": provider_revenue_cycle_ui_contract(),
        "api_contract": provider_revenue_cycle_build_api_contract(),
        "schema_contract": provider_revenue_cycle_build_schema_contract(),
        "service_contract": provider_revenue_cycle_build_service_contract(),
        "release_evidence_contract": build_release_evidence(),
        "permissions_contract": provider_revenue_cycle_permissions_contract(),
        "owned_tables": PROVIDER_REVENUE_CYCLE_OWNED_TABLES,
        "runtime_tables": PROVIDER_REVENUE_CYCLE_RUNTIME_TABLES,
        "allowed_database_backends": PROVIDER_REVENUE_CYCLE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": PROVIDER_REVENUE_CYCLE_REQUIRED_EVENT_TOPIC,
        "emits": PROVIDER_REVENUE_CYCLE_EMITTED_EVENT_TYPES,
        "consumes": PROVIDER_REVENUE_CYCLE_CONSUMED_EVENT_TYPES,
        "boundary_contract": provider_revenue_cycle_verify_owned_table_boundary(("provider_revenue_cycle_patient_account_table",)),
        "standalone_contract": standalone_manifest(),
        "package_audit": run_provider_revenue_cycle_pbc_audit(),
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
    runtime = provider_revenue_cycle_runtime_smoke()
    audit = run_provider_revenue_cycle_pbc_audit()
    return {
        "ok": discovery["ok"] and runtime["ok"] and audit["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "audit": audit,
        "side_effects": (),
    }
