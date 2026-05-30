"""Master Data Governance PBC implementation package."""
from __future__ import annotations

from .agent import composed_agent_contribution
from .manifest import PBC_MANIFEST
from .release_evidence import build_release_evidence
from .release_evidence import generation_smoke_audit
from .runtime import *  # noqa: F401,F403
from .schema_contract import build_schema_contract
from .service_contract import build_service_contract
from .standalone import build_standalone_app
from .standalone import master_data_governance_standalone_app_contract
from .standalone import master_data_governance_standalone_app_smoke
from .ui import master_data_governance_render_workbench
from .ui import master_data_governance_ui_contract
from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata

PBC_KEY = "master_data_governance"



def implementation_contract() -> dict:
    runtime = master_data_governance_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": master_data_governance_ui_contract(),
        "api_contract": master_data_governance_build_api_contract(),
        "schema_contract": build_schema_contract(),
        "service_contract": build_service_contract(),
        "release_evidence_contract": build_release_evidence(),
        "permissions_contract": master_data_governance_permissions_contract(),
        "owned_tables": MASTER_DATA_GOVERNANCE_OWNED_TABLES,
        "runtime_tables": MASTER_DATA_GOVERNANCE_RUNTIME_TABLES,
        "allowed_database_backends": MASTER_DATA_GOVERNANCE_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": MASTER_DATA_GOVERNANCE_REQUIRED_EVENT_TOPIC,
        "emits": MASTER_DATA_GOVERNANCE_EMITTED_EVENT_TYPES,
        "consumes": MASTER_DATA_GOVERNANCE_CONSUMED_EVENT_TYPES,
        "boundary_contract": master_data_governance_verify_owned_table_boundary(MASTER_DATA_GOVERNANCE_OWNED_TABLES + ("api_dependency",)),
        "standalone_app_contract": master_data_governance_standalone_app_contract(),
        "agent_contribution": composed_agent_contribution(),
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
    runtime = master_data_governance_runtime_smoke()
    standalone = master_data_governance_standalone_app_smoke()
    release = generation_smoke_audit()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"] and release["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "release": release,
        "side_effects": (),
    }
