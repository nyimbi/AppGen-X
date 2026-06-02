"""Chemical Batch Compliance PBC implementation package."""

from __future__ import annotations

from .manifest import PBC_MANIFEST
from .runtime import CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS
from .runtime import CHEMICAL_BATCH_COMPLIANCE_CONSUMED_EVENT_TYPES
from .runtime import CHEMICAL_BATCH_COMPLIANCE_EMITTED_EVENT_TYPES
from .runtime import CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES
from .runtime import CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC
from .runtime import CHEMICAL_BATCH_COMPLIANCE_RUNTIME_TABLES
from .runtime import chemical_batch_compliance_build_api_contract
from .runtime import chemical_batch_compliance_build_release_evidence
from .runtime import chemical_batch_compliance_build_schema_contract
from .runtime import chemical_batch_compliance_build_service_contract
from .runtime import chemical_batch_compliance_permissions_contract
from .runtime import chemical_batch_compliance_runtime_capabilities
from .runtime import chemical_batch_compliance_runtime_smoke
from .runtime import chemical_batch_compliance_verify_owned_table_boundary
from .ui import chemical_batch_compliance_render_workbench
from .ui import chemical_batch_compliance_ui_contract
from .standalone import ChemicalBatchComplianceStandaloneApp
from .standalone import single_pbc_app_contract
from .standalone import standalone_smoke_test
from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata

PBC_KEY = "chemical_batch_compliance"


def implementation_contract() -> dict:
    runtime = chemical_batch_compliance_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": chemical_batch_compliance_ui_contract(),
        "api_contract": chemical_batch_compliance_build_api_contract(),
        "schema_contract": chemical_batch_compliance_build_schema_contract(),
        "service_contract": chemical_batch_compliance_build_service_contract(),
        "release_evidence_contract": chemical_batch_compliance_build_release_evidence(),
        "permissions_contract": chemical_batch_compliance_permissions_contract(),
        "owned_tables": CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES,
        "runtime_tables": CHEMICAL_BATCH_COMPLIANCE_RUNTIME_TABLES,
        "allowed_database_backends": CHEMICAL_BATCH_COMPLIANCE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": CHEMICAL_BATCH_COMPLIANCE_REQUIRED_EVENT_TOPIC,
        "emits": CHEMICAL_BATCH_COMPLIANCE_EMITTED_EVENT_TYPES,
        "consumes": CHEMICAL_BATCH_COMPLIANCE_CONSUMED_EVENT_TYPES,
        "boundary_contract": chemical_batch_compliance_verify_owned_table_boundary(CHEMICAL_BATCH_COMPLIANCE_OWNED_TABLES),
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
    runtime = chemical_batch_compliance_runtime_smoke()
    return {"ok": discovery["ok"] and runtime["ok"], "discovery": discovery, "runtime": runtime, "side_effects": ()}


__all__ = (
    "PBC_KEY",
    "PBC_MANIFEST",
    "chemical_batch_compliance_runtime_capabilities",
    "chemical_batch_compliance_runtime_smoke",
    "chemical_batch_compliance_ui_contract",
    "chemical_batch_compliance_render_workbench",
    "implementation_contract",
    "package_discovery_plan",
    "package_metadata_manifest",
    "register_pbc",
    "registration_plan",
    "ChemicalBatchComplianceStandaloneApp",
    "single_pbc_app_contract",
    "standalone_smoke_test",
    "smoke_test",
    "validate_package_metadata",
)
