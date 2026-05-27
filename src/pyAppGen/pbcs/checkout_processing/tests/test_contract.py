"""Generated contract smoke tests for checkout_processing."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    from .. import models, release_evidence, schema_contract

    assert SCHEMA_CONTRACT['pbc'] == 'checkout_processing'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    schema_smoke = schema_contract.smoke_test()
    model_smoke = models.smoke_test()
    assert schema_smoke['ok'] is True
    assert model_smoke['ok'] is True
    assert not schema_smoke['side_effects']
    assert not model_smoke['side_effects']
    assert SERVICE_CONTRACT['pbc'] == 'checkout_processing'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert 'confirm_inventory_reservation' in SERVICE_CONTRACT['command_methods']
    assert 'authorize_payment_intent' in SERVICE_CONTRACT['command_methods']
    assert 'capture_payment_intent' in SERVICE_CONTRACT['command_methods']
    assert RELEASE_EVIDENCE['pbc'] == 'checkout_processing'
    assert RELEASE_EVIDENCE['ok'] is True


    release_manifest = release_evidence.release_readiness_manifest()
    release_validation = release_evidence.validate_release_evidence()
    release_smoke = release_evidence.smoke_test()
    assert release_manifest['ok'] is True
    assert release_validation['ok'] is True
    assert release_smoke['ok'] is True
    assert not release_manifest['blocking_gaps']
    assert not release_validation['missing_sections']
    assert not release_validation['failed_checks']
    assert not release_validation['boundary_gaps']
    assert not release_manifest['side_effects']
    assert not release_validation['side_effects']
    assert not release_smoke['side_effects']


def test_runtime_owned_tables_have_schema_models_and_migrations():
    from pathlib import Path

    from .. import models, schema_contract
    from ..runtime import checkout_processing_runtime_capabilities

    runtime_owned = tuple(checkout_processing_runtime_capabilities()["owned_tables"])
    expected_owned = tuple(
        table if table.startswith("checkout_processing_") else f"checkout_processing_{table}"
        for table in runtime_owned
    )
    schema = schema_contract.build_schema_contract()
    model_manifest = models.model_manifest()
    migration_sql = Path(__file__).parents[1].joinpath("migrations/001_initial.sql").read_text()

    assert set(expected_owned) <= set(schema["owned_tables"])
    assert set(expected_owned) <= set(model_manifest["model_tables"])
    assert all(f"CREATE TABLE {table}" in migration_sql for table in expected_owned)
    assert schema["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert not schema_contract.validate_schema_contract()["missing_models"]
    assert not model_manifest["cross_pbc_relationships"]


def test_checkout_handoff_rule_config_and_event_tables_are_first_class():
    from .. import events, handlers, schema_contract

    schema = schema_contract.build_schema_contract()
    required_tables = {
        "checkout_processing_checkout_pricing_handoff",
        "checkout_processing_checkout_tax_handoff",
        "checkout_processing_checkout_inventory_reservation_handoff",
        "checkout_processing_checkout_payment_intent_handoff",
        "checkout_processing_checkout_risk_screen",
        "checkout_processing_checkout_address_validation",
        "checkout_processing_checkout_rule",
        "checkout_processing_checkout_parameter",
        "checkout_processing_checkout_configuration",
        "checkout_processing_appgen_outbox_event",
        "checkout_processing_appgen_inbox_event",
        "checkout_processing_dead_letter_event",
    }

    assert required_tables <= set(schema["owned_tables"])
    assert events.EVENT_CONTRACT["dead_letter_table"] == "checkout_processing_dead_letter_event"
    assert set(handlers.handler_manifest()["dead_letter_tables"]) == {"checkout_processing_dead_letter_event"}


def test_manifest_and_event_contract():
    from .. import events

    assert PBC_MANIFEST['pbc'] == 'checkout_processing'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('checkout_processing_')
    assert EVENT_CONTRACT['inbox_table'].startswith('checkout_processing_')
    manifest = events.event_contract_manifest()
    validation = events.validate_event_contract()
    smoke = events.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['stream_engine_picker_visible'] is False
    assert not validation['invalid_tables']
    assert not validation['invalid_emitted']
    assert not validation['invalid_consumed']
    assert smoke['emitted']['table'] == EVENT_CONTRACT['outbox_table']
    assert smoke['consumed']['table'] == EVENT_CONTRACT['inbox_table']
    assert smoke['emitted']['retry_policy']['max_attempts'] >= 3
    assert smoke['consumed']['dead_letter_table'].startswith(PBC_MANIFEST['pbc'] + '_')
    assert not manifest['side_effects']
    assert not validation['side_effects']
    assert not smoke['side_effects']


def test_registration_plan_is_side_effect_free():
    from .. import package_discovery_plan, package_metadata_manifest, register_pbc, registration_plan, validate_package_metadata

    assert register_pbc()['pbc'] == 'checkout_processing'
    plan = registration_plan()
    assert plan['ok'] is True
    assert plan['catalog_patch']
    metadata = package_metadata_manifest()
    metadata_validation = validate_package_metadata()
    discovery = package_discovery_plan()
    assert metadata['ok'] is True
    assert metadata_validation['ok'] is True
    assert discovery['ok'] is True
    assert metadata['stream_engine_picker_visible'] is False
    assert metadata['event_contract'] == 'AppGen-X'
    assert not metadata_validation['missing_entrypoints']
    assert not metadata_validation['missing_publish_artifacts']
    assert not metadata_validation['missing_capability_evidence']
    assert not metadata_validation['invalid']
    assert not discovery['side_effects']


def test_service_and_route_surface_are_executable():
    from .. import routes, services

    service_smoke = services.smoke_test()
    operation_contracts = services.service_operation_contracts()
    route_contracts = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    route_smoke = routes.smoke_test()
    assert service_smoke['ok'] is True
    assert operation_contracts['ok'] is True
    assert route_contracts['ok'] is True
    assert route_validation['ok'] is True
    assert route_contracts['contracts']
    assert 'command_inventory_confirmations' in operation_contracts['command_operations']
    assert 'command_payment_authorizations' in operation_contracts['command_operations']
    assert 'command_payment_captures' in operation_contracts['command_operations']
    assert all(item['permission'] for item in route_contracts['contracts'])
    assert all(item['event_contract'] == 'AppGen-X' for item in route_contracts['contracts'])
    assert all(item['stream_engine_picker_visible'] is False for item in route_contracts['contracts'])
    assert all(item['shared_table_access'] is False for item in route_contracts['contracts'])
    assert not route_validation['service_mismatches']
    assert not route_validation['missing_idempotency']
    assert not route_validation['invalid_table_scope']
    assert service_smoke['result']['operation_contract']['route']['path']
    assert service_smoke['result']['operation_contract']['permission']
    assert service_smoke['result']['operation_contract']['event_contract'] == 'AppGen-X'
    assert service_smoke['result']['operation_contract']['owned_tables'] or service_smoke['result']['operation_contract']['read_tables']
    assert route_smoke['ok'] is True
    assert not service_smoke['side_effects']
    assert not operation_contracts['side_effects']
    assert not route_contracts['side_effects']
    assert not route_validation['side_effects']
    assert not route_smoke['side_effects']


def test_runtime_requires_confirmed_inventory_and_captured_payment():
    from ..runtime import checkout_processing_build_workbench_view
    from ..runtime import checkout_processing_runtime_smoke

    smoke = checkout_processing_runtime_smoke()
    assert smoke['ok'] is True
    state = smoke['state']
    session = state['checkout_sessions']['chk_100']
    reservation = state['inventory_reservations'][session['inventory_reservation_id']]
    payment = state['payment_intents'][session['payment_intent_id']]
    workbench = checkout_processing_build_workbench_view(state, tenant='tenant_alpha')
    assert reservation['status'] == 'confirmed'
    assert payment['status'] == 'captured'
    assert session['status'] == 'completed'
    assert workbench['confirmed_inventory_count'] == 1
    assert workbench['captured_payment_count'] == 1


def test_configuration_permissions_and_seed_hooks_are_executable():
    from .. import config, permissions, seed_data

    config_smoke = config.smoke_test()
    governance_smoke = config.governance_smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()
    assert config_smoke['ok'] is True
    assert governance_smoke['ok'] is True
    assert governance_smoke['parameter']['accepted'] is True
    assert governance_smoke['compiled_rule']['compiled'] is True
    assert governance_smoke['rule_decision']['allowed'] is True
    assert permission_smoke['ok'] is True
    assert seed_smoke['ok'] is True
    assert not config_smoke['side_effects']
    assert not governance_smoke['side_effects']
    assert not permission_smoke['side_effects']
    assert not seed_smoke['side_effects']


def test_ui_workbench_surface_is_executable():
    from .. import ui

    if hasattr(ui, 'smoke_test'):
        smoke = ui.smoke_test()
    else:
        contract = getattr(ui, f"{PBC_MANIFEST['pbc']}_ui_contract")()
        rendered = {
            'ok': contract['ok'],
            'cards': contract.get('panels') or contract.get('fragments'),
            'route': (contract.get('routes') or (None,))[0],
        }
        smoke = {
            'ok': contract['ok'] and bool(contract.get('fragments')) and bool(rendered['cards']),
            'manifest': {'fragments': contract.get('fragments', ())},
            'rendered': rendered,
            'side_effects': (),
        }
    assert smoke['ok'] is True
    assert smoke['manifest']['fragments']
    assert smoke['rendered']['cards']
    assert not smoke['side_effects']


def test_event_handlers_are_idempotent_and_retryable():
    from .. import handlers

    smoke = handlers.smoke_test()
    assert smoke['ok'] is True
    assert smoke['manifest']['handlers']
    assert smoke['first_result']['retry_policy']
    assert smoke['first_result']['dead_letter_table'].startswith('checkout_processing_')
    assert smoke['duplicate_result']['duplicate'] is True
    assert smoke['unknown_result']['handled'] is False
    assert not smoke['side_effects']

def test_table_stakes_and_advanced_capability_assurance_is_executable():
    from .. import capability_assurance

    manifest = capability_assurance.table_stakes_capability_manifest()
    validation = capability_assurance.validate_table_stakes_capability_coverage()
    smoke = capability_assurance.smoke_test()
    assert manifest['ok'] is True
    assert validation['ok'] is True
    assert smoke['ok'] is True
    assert manifest['standard_features']
    assert manifest['advanced_capabilities']
    assert not validation['missing_standard']
    assert not validation['missing_advanced']
    assert not validation['missing_operations']
    assert not validation['uncovered_features']
    assert not validation['invalid_tables']
    assert not validation['invalid_backends']
    assert validation['stream_picker_visible'] is False
    assert validation['event_contract'] == 'AppGen-X'
    assert validation['owned_boundary_rejection']['ok'] is False
    assert validation['owned_boundary_rejection']['violations']
    assert not smoke['side_effects']
