"""Actuarial Pricing and Reserving PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import actuarial_pricing_reserving_ui_contract, actuarial_pricing_reserving_render_workbench

PBC_KEY = 'actuarial_pricing_reserving'


def implementation_contract() -> dict:
    runtime = actuarial_pricing_reserving_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': actuarial_pricing_reserving_ui_contract(), 'api_contract': actuarial_pricing_reserving_build_api_contract(), 'schema_contract': actuarial_pricing_reserving_build_schema_contract(), 'service_contract': actuarial_pricing_reserving_build_service_contract(), 'release_evidence_contract': actuarial_pricing_reserving_build_release_evidence(), 'permissions_contract': actuarial_pricing_reserving_permissions_contract(), 'owned_tables': ACTUARIAL_PRICING_RESERVING_OWNED_TABLES, 'runtime_tables': ACTUARIAL_PRICING_RESERVING_RUNTIME_TABLES, 'allowed_database_backends': ACTUARIAL_PRICING_RESERVING_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': ACTUARIAL_PRICING_RESERVING_REQUIRED_EVENT_TOPIC, 'emits': ACTUARIAL_PRICING_RESERVING_EMITTED_EVENT_TYPES, 'consumes': ACTUARIAL_PRICING_RESERVING_CONSUMED_EVENT_TYPES, 'boundary_contract': actuarial_pricing_reserving_verify_owned_table_boundary(ACTUARIAL_PRICING_RESERVING_OWNED_TABLES + ('api_dependency',))}


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
    runtime = actuarial_pricing_reserving_runtime_smoke()
    return {'ok': discovery['ok'] and runtime['ok'], 'discovery': discovery, 'runtime': runtime, 'side_effects': ()}
