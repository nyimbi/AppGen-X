"""Capital Markets Trading Operations PBC implementation package."""
from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .application import CapitalMarketsTradingOpsApp
from .standalone import CapitalMarketsTradingOpsStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from .runtime import *
from .ui import capital_markets_trading_ops_ui_contract, capital_markets_trading_ops_render_workbench

PBC_KEY = 'capital_markets_trading_ops'


def implementation_contract() -> dict:
    runtime = capital_markets_trading_ops_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {**contract, 'standard_features': runtime['standard_features'], 'advanced_runtime': runtime, 'ui_contract': capital_markets_trading_ops_ui_contract(), 'api_contract': capital_markets_trading_ops_build_api_contract(), 'schema_contract': capital_markets_trading_ops_build_schema_contract(), 'service_contract': capital_markets_trading_ops_build_service_contract(), 'release_evidence_contract': capital_markets_trading_ops_build_release_evidence(), 'permissions_contract': capital_markets_trading_ops_permissions_contract(), 'owned_tables': CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES, 'runtime_tables': CAPITAL_MARKETS_TRADING_OPS_RUNTIME_TABLES, 'allowed_database_backends': CAPITAL_MARKETS_TRADING_OPS_ALLOWED_DATABASE_BACKENDS, 'required_event_topic': CAPITAL_MARKETS_TRADING_OPS_REQUIRED_EVENT_TOPIC, 'emits': CAPITAL_MARKETS_TRADING_OPS_EMITTED_EVENT_TYPES, 'consumes': CAPITAL_MARKETS_TRADING_OPS_CONSUMED_EVENT_TYPES, 'boundary_contract': capital_markets_trading_ops_verify_owned_table_boundary(CAPITAL_MARKETS_TRADING_OPS_OWNED_TABLES + ('api_dependency',))}


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
    runtime = capital_markets_trading_ops_runtime_smoke()
    app = CapitalMarketsTradingOpsApp()
    app_contract = app.app_contract()
    app.close()
    return {'ok': discovery['ok'] and runtime['ok'] and app_contract['ok'], 'discovery': discovery, 'runtime': runtime, 'app_contract': app_contract, 'side_effects': ()}
