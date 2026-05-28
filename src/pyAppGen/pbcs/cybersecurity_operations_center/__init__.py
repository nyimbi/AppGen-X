"""Cybersecurity Operations Center PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import cybersecurity_operations_center_ui_contract, cybersecurity_operations_center_render_workbench

PBC_KEY = 'cybersecurity_operations_center'


def implementation_contract() -> dict:
    runtime = cybersecurity_operations_center_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': cybersecurity_operations_center_ui_contract(), 'api_contract': cybersecurity_operations_center_build_api_contract(), 'schema_contract': cybersecurity_operations_center_build_schema_contract(), 'service_contract': cybersecurity_operations_center_build_service_contract(), 'release_evidence_contract': cybersecurity_operations_center_build_release_evidence(), 'permissions_contract': cybersecurity_operations_center_permissions_contract(), 'owned_tables': CYBERSECURITY_OPERATIONS_CENTER_OWNED_TABLES, 'runtime_tables': CYBERSECURITY_OPERATIONS_CENTER_RUNTIME_TABLES, 'allowed_database_backends': CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC, 'emits': CYBERSECURITY_OPERATIONS_CENTER_EMITTED_EVENT_TYPES, 'consumes': CYBERSECURITY_OPERATIONS_CENTER_CONSUMED_EVENT_TYPES, 'boundary_contract': cybersecurity_operations_center_verify_owned_table_boundary(CYBERSECURITY_OPERATIONS_CENTER_OWNED_TABLES + ('api_dependency',))}


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
    runtime = cybersecurity_operations_center_runtime_smoke()
    return {'ok': discovery['ok'] and runtime['ok'], 'discovery': discovery, 'runtime': runtime, 'side_effects': ()}
