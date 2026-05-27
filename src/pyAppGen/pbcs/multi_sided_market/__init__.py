"""Multi-sided market PBC implementation package."""

from .manifest import PBC_MANIFEST
from ..source_contract import source_pbc_package_contract, source_package_metadata, validate_source_package_metadata, source_registration_plan
from .runtime import MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC, MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS, MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES, MULTI_SIDED_MARKET_EMITTED_EVENT_TYPES, MULTI_SIDED_MARKET_OWNED_TABLES, MULTI_SIDED_MARKET_RUNTIME_TABLES, MULTI_SIDED_MARKET_RUNTIME_CAPABILITY_KEYS, MULTI_SIDED_MARKET_STANDARD_FEATURE_KEYS, multi_sided_market_empty_state, multi_sided_market_configure_runtime, multi_sided_market_set_parameter, multi_sided_market_register_rule, multi_sided_market_register_schema_extension, multi_sided_market_receive_event, multi_sided_market_verify_participant, multi_sided_market_publish_listing, multi_sided_market_create_service_offer, multi_sided_market_place_trade_order, multi_sided_market_match_barter_offer, multi_sided_market_execute_sale, multi_sided_market_reserve_booking, multi_sided_market_start_rental, multi_sided_market_issue_loan, multi_sided_market_open_escrow, multi_sided_market_prepare_settlement, multi_sided_market_open_dispute, multi_sided_market_score_reputation, multi_sided_market_optimize_exchange_match, multi_sided_market_build_schema_contract, multi_sided_market_build_service_contract, multi_sided_market_build_api_contract, multi_sided_market_build_release_evidence, multi_sided_market_permissions_contract, multi_sided_market_build_workbench_view, multi_sided_market_verify_owned_table_boundary, multi_sided_market_runtime_capabilities, multi_sided_market_runtime_smoke
from .ui import multi_sided_market_ui_contract, multi_sided_market_render_workbench

PBC_KEY = 'multi_sided_market'


def implementation_contract() -> dict:
    runtime = multi_sided_market_runtime_capabilities()
    contract = source_pbc_package_contract(PBC_KEY, tuple(runtime['capabilities']))
    return {
        **contract,
        'standard_features': runtime['standard_features'],
        'advanced_runtime': runtime,
        'ui_contract': multi_sided_market_ui_contract(),
        'api_contract': multi_sided_market_build_api_contract(),
        'schema_contract': multi_sided_market_build_schema_contract(),
        'service_contract': multi_sided_market_build_service_contract(),
        'release_evidence_contract': multi_sided_market_build_release_evidence(),
        'permissions_contract': multi_sided_market_permissions_contract(),
        'owned_tables': MULTI_SIDED_MARKET_OWNED_TABLES,
        'runtime_tables': MULTI_SIDED_MARKET_RUNTIME_TABLES,
        'allowed_database_backends': MULTI_SIDED_MARKET_ALLOWED_DATABASE_BACKENDS,
        'required_event_topic': MULTI_SIDED_MARKET_REQUIRED_EVENT_TOPIC,
        'emits': MULTI_SIDED_MARKET_EMITTED_EVENT_TYPES,
        'consumes': MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES,
        'boundary_contract': multi_sided_market_verify_owned_table_boundary(MULTI_SIDED_MARKET_OWNED_TABLES + MULTI_SIDED_MARKET_CONSUMED_EVENT_TYPES + ('payment_orchestration.api', 'tax_localization.api', 'inventory_positioning.api')),
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
    return {'format': 'appgen.pbc-source-package-discovery-plan.v1', 'ok': metadata_validation['ok'] and registration['ok'], 'pbc': PBC_KEY, 'metadata_validation': metadata_validation, 'registration': registration, 'side_effects': ()}


def smoke_test() -> dict:
    discovery = package_discovery_plan()
    runtime = multi_sided_market_runtime_smoke()
    return {'ok': discovery['ok'] and runtime['ok'], 'discovery': discovery, 'runtime': runtime, 'side_effects': ()}
