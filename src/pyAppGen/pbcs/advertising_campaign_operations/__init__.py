"""Advertising Campaign Operations PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import source_package_metadata
from ..source_contract import source_pbc_package_contract
from ..source_contract import source_registration_plan
from ..source_contract import validate_source_package_metadata
from .release_evidence import build_release_evidence
from .routes import api_route_contracts
from .runtime import *
from .schema_contract import build_schema_contract
from .service_contract import build_service_contract
from .standalone import smoke_test as standalone_smoke_test
from .standalone import standalone_app_manifest
from .ui import advertising_campaign_operations_render_workbench
from .ui import advertising_campaign_operations_ui_contract

PBC_KEY = "advertising_campaign_operations"


def implementation_contract() -> dict:
    runtime = advertising_campaign_operations_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": advertising_campaign_operations_ui_contract(),
        "api_contract": api_route_contracts(),
        "schema_contract": build_schema_contract(),
        "service_contract": build_service_contract(),
        "release_evidence_contract": build_release_evidence(),
        "permissions_contract": advertising_campaign_operations_permissions_contract(),
        "standalone_app": standalone_app_manifest(),
        "owned_tables": ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES,
        "runtime_tables": ADVERTISING_CAMPAIGN_OPERATIONS_RUNTIME_TABLES,
        "allowed_database_backends": ADVERTISING_CAMPAIGN_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": ADVERTISING_CAMPAIGN_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "emits": ADVERTISING_CAMPAIGN_OPERATIONS_EMITTED_EVENT_TYPES,
        "consumes": ADVERTISING_CAMPAIGN_OPERATIONS_CONSUMED_EVENT_TYPES,
        "boundary_contract": advertising_campaign_operations_verify_owned_table_boundary(
            ADVERTISING_CAMPAIGN_OPERATIONS_OWNED_TABLES + ("api_dependency",)
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
    runtime = advertising_campaign_operations_runtime_smoke()
    standalone = standalone_smoke_test()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
