"""Telecom Network Operations PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import telecom_network_operations_ui_contract, telecom_network_operations_render_workbench
from .standalone import single_pbc_app_contract, standalone_smoke_test

PBC_KEY = 'telecom_network_operations'


def implementation_contract() -> dict:
    runtime = telecom_network_operations_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': telecom_network_operations_ui_contract(), 'api_contract': telecom_network_operations_build_api_contract(), 'schema_contract': telecom_network_operations_build_schema_contract(), 'service_contract': telecom_network_operations_build_service_contract(), 'release_evidence_contract': telecom_network_operations_build_release_evidence(), 'permissions_contract': telecom_network_operations_permissions_contract(), 'owned_tables': TELECOM_NETWORK_OPERATIONS_OWNED_TABLES, 'runtime_tables': TELECOM_NETWORK_OPERATIONS_RUNTIME_TABLES, 'allowed_database_backends': TELECOM_NETWORK_OPERATIONS_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': TELECOM_NETWORK_OPERATIONS_REQUIRED_EVENT_TOPIC, 'emits': TELECOM_NETWORK_OPERATIONS_EMITTED_EVENT_TYPES, 'consumes': TELECOM_NETWORK_OPERATIONS_CONSUMED_EVENT_TYPES, 'boundary_contract': telecom_network_operations_verify_owned_table_boundary(TELECOM_NETWORK_OPERATIONS_OWNED_TABLES + ('api_dependency',)), 'standalone_app_contract': single_pbc_app_contract()}


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
    runtime = telecom_network_operations_runtime_smoke()
    standalone = standalone_smoke_test()
    return {'ok': discovery['ok'] and runtime['ok'] and standalone['ok'], 'discovery': discovery, 'runtime': runtime, 'standalone': standalone, 'side_effects': ()}
