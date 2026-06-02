"""Sports Venue Event Operations PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_pbc_package_contract,
    source_package_metadata,
    source_registration_plan,
    validate_source_package_metadata,
)
from .release_evidence import build_release_evidence
from .runtime import *  # noqa: F401,F403
from .standalone import documentation_presence, standalone_manifest, standalone_smoke_test
from .ui import (
    sports_venue_event_operations_render_standalone_workbench,
    sports_venue_event_operations_render_workbench,
    sports_venue_event_operations_standalone_workbench_blueprint,
    sports_venue_event_operations_ui_contract,
)

PBC_KEY = "sports_venue_event_operations"


def implementation_contract() -> dict:
    runtime = sports_venue_event_operations_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime["capabilities"]))
    return {
        **contract,
        "standard_features": runtime["standard_features"],
        "advanced_runtime": runtime,
        "ui_contract": sports_venue_event_operations_ui_contract(),
        "api_contract": sports_venue_event_operations_build_api_contract(),
        "schema_contract": sports_venue_event_operations_build_schema_contract(),
        "service_contract": sports_venue_event_operations_build_service_contract(),
        "release_evidence_contract": build_release_evidence(),
        "permissions_contract": sports_venue_event_operations_permissions_contract(),
        "owned_tables": SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES,
        "runtime_tables": SPORTS_VENUE_EVENT_OPERATIONS_RUNTIME_TABLES,
        "allowed_database_backends": SPORTS_VENUE_EVENT_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
        "required_event_topic": SPORTS_VENUE_EVENT_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "emits": SPORTS_VENUE_EVENT_OPERATIONS_EMITTED_EVENT_TYPES,
        "consumes": SPORTS_VENUE_EVENT_OPERATIONS_CONSUMED_EVENT_TYPES,
        "boundary_contract": sports_venue_event_operations_verify_owned_table_boundary(
            SPORTS_VENUE_EVENT_OPERATIONS_OWNED_TABLES + ("api_dependency",)
        ),
        "standalone_manifest": standalone_manifest(),
        "documentation_presence": documentation_presence(),
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
    runtime = sports_venue_event_operations_runtime_smoke()
    standalone = standalone_smoke_test()
    return {
        "ok": discovery["ok"] and runtime["ok"] and standalone["ok"],
        "discovery": discovery,
        "runtime": runtime,
        "standalone": standalone,
        "side_effects": (),
    }
