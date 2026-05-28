"""Energy Trading and Risk PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import *
from .ui import energy_trading_risk_ui_contract, energy_trading_risk_render_workbench

PBC_KEY = 'energy_trading_risk'


def implementation_contract() -> dict:
    runtime = energy_trading_risk_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': energy_trading_risk_ui_contract(), 'api_contract': energy_trading_risk_build_api_contract(), 'schema_contract': energy_trading_risk_build_schema_contract(), 'service_contract': energy_trading_risk_build_service_contract(), 'release_evidence_contract': energy_trading_risk_build_release_evidence(), 'permissions_contract': energy_trading_risk_permissions_contract(), 'owned_tables': ENERGY_TRADING_RISK_OWNED_TABLES, 'runtime_tables': ENERGY_TRADING_RISK_RUNTIME_TABLES, 'allowed_database_backends': ENERGY_TRADING_RISK_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': ENERGY_TRADING_RISK_REQUIRED_EVENT_TOPIC, 'emits': ENERGY_TRADING_RISK_EMITTED_EVENT_TYPES, 'consumes': ENERGY_TRADING_RISK_CONSUMED_EVENT_TYPES, 'boundary_contract': energy_trading_risk_verify_owned_table_boundary(ENERGY_TRADING_RISK_OWNED_TABLES + ('api_dependency',))}


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
    runtime = energy_trading_risk_runtime_smoke()
    return {'ok': discovery['ok'] and runtime['ok'], 'discovery': discovery, 'runtime': runtime, 'side_effects': ()}
