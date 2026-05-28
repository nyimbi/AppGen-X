"""Utility Outage Restoration PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import utility_outage_restoration_ui_contract, utility_outage_restoration_render_workbench

PBC_KEY = 'utility_outage_restoration'


def implementation_contract() -> dict:
    runtime = utility_outage_restoration_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': utility_outage_restoration_ui_contract(), 'api_contract': utility_outage_restoration_build_api_contract(), 'schema_contract': utility_outage_restoration_build_schema_contract(), 'service_contract': utility_outage_restoration_build_service_contract(), 'release_evidence_contract': utility_outage_restoration_build_release_evidence(), 'permissions_contract': utility_outage_restoration_permissions_contract(), 'owned_tables': UTILITY_OUTAGE_RESTORATION_OWNED_TABLES, 'runtime_tables': UTILITY_OUTAGE_RESTORATION_RUNTIME_TABLES, 'allowed_database_backends': UTILITY_OUTAGE_RESTORATION_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': UTILITY_OUTAGE_RESTORATION_REQUIRED_EVENT_TOPIC, 'emits': UTILITY_OUTAGE_RESTORATION_EMITTED_EVENT_TYPES, 'consumes': UTILITY_OUTAGE_RESTORATION_CONSUMED_EVENT_TYPES, 'boundary_contract': utility_outage_restoration_verify_owned_table_boundary(UTILITY_OUTAGE_RESTORATION_OWNED_TABLES + ('api_dependency',))}


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
    return {'format': 'appgen.pbc-source-package-discovery-plan.v1', 'ok': metadata_validation['ok'] and registration['ok'], 'pbc': PBC_KEY, 'metadata_validation': metadata_validation, 'registration': registration, 'side_effects': ()}


def smoke_test() -> dict:
    discovery = package_discovery_plan()
    runtime = utility_outage_restoration_runtime_smoke()
    return {'ok': discovery['ok'] and runtime['ok'], 'discovery': discovery, 'runtime': runtime, 'side_effects': ()}
