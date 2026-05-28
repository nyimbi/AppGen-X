"""Bank Payments Clearing PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import bank_payments_clearing_ui_contract, bank_payments_clearing_render_workbench

PBC_KEY = 'bank_payments_clearing'


def implementation_contract() -> dict:
    runtime = bank_payments_clearing_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': bank_payments_clearing_ui_contract(), 'api_contract': bank_payments_clearing_build_api_contract(), 'schema_contract': bank_payments_clearing_build_schema_contract(), 'service_contract': bank_payments_clearing_build_service_contract(), 'release_evidence_contract': bank_payments_clearing_build_release_evidence(), 'permissions_contract': bank_payments_clearing_permissions_contract(), 'owned_tables': BANK_PAYMENTS_CLEARING_OWNED_TABLES, 'runtime_tables': BANK_PAYMENTS_CLEARING_RUNTIME_TABLES, 'allowed_database_backends': BANK_PAYMENTS_CLEARING_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': BANK_PAYMENTS_CLEARING_REQUIRED_EVENT_TOPIC, 'emits': BANK_PAYMENTS_CLEARING_EMITTED_EVENT_TYPES, 'consumes': BANK_PAYMENTS_CLEARING_CONSUMED_EVENT_TYPES, 'boundary_contract': bank_payments_clearing_verify_owned_table_boundary(BANK_PAYMENTS_CLEARING_OWNED_TABLES + ('api_dependency',))}


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
    runtime = bank_payments_clearing_runtime_smoke()
    return {'ok': discovery['ok'] and runtime['ok'], 'discovery': discovery, 'runtime': runtime, 'side_effects': ()}
