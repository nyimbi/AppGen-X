"""Rail Operations Management PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import (
    source_pbc_package_contract,
    source_package_metadata,
    source_registration_plan,
    validate_source_package_metadata,
)
from .runtime import *
from .standalone import RailOperationsManagementStandaloneApp, standalone_app_manifest
from .ui import (
    rail_operations_management_render_standalone_app,
    rail_operations_management_render_workbench,
    rail_operations_management_standalone_app_contract,
    rail_operations_management_ui_contract,
)

PBC_KEY = 'rail_operations_management'


def implementation_contract() -> dict:
    runtime = rail_operations_management_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {
        **contract,
        'standard_features': runtime['standard_features'],
        'advanced_runtime': runtime,
        'ui_contract': rail_operations_management_ui_contract(),
        'api_contract': rail_operations_management_build_api_contract(),
        'schema_contract': rail_operations_management_build_schema_contract(),
        'service_contract': rail_operations_management_build_service_contract(),
        'release_evidence_contract': rail_operations_management_build_release_evidence(),
        'permissions_contract': rail_operations_management_permissions_contract(),
        'owned_tables': RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES,
        'runtime_tables': RAIL_OPERATIONS_MANAGEMENT_RUNTIME_TABLES,
        'allowed_database_backends': RAIL_OPERATIONS_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        'required_event_topic': RAIL_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        'emits': RAIL_OPERATIONS_MANAGEMENT_EMITTED_EVENT_TYPES,
        'consumes': RAIL_OPERATIONS_MANAGEMENT_CONSUMED_EVENT_TYPES,
        'standalone_app': rail_operations_management_standalone_app_contract(),
        'boundary_contract': rail_operations_management_verify_owned_table_boundary(
            RAIL_OPERATIONS_MANAGEMENT_OWNED_TABLES + ('api_dependency',),
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
        'format': 'appgen.pbc-source-package-discovery-plan.v1',
        'ok': metadata_validation['ok'] and registration['ok'],
        'pbc': PBC_KEY,
        'metadata_validation': metadata_validation,
        'registration': registration,
        'side_effects': (),
    }


def smoke_test() -> dict:
    discovery = package_discovery_plan()
    runtime = rail_operations_management_runtime_smoke()
    standalone = RailOperationsManagementStandaloneApp().load_demo_workspace()
    return {
        'ok': discovery['ok'] and runtime['ok'] and standalone['ok'],
        'discovery': discovery,
        'runtime': runtime,
        'standalone': standalone,
        'side_effects': (),
    }
