"""Generated contract smoke tests for wms_core."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    assert SCHEMA_CONTRACT['pbc'] == 'wms_core'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    assert SERVICE_CONTRACT['pbc'] == 'wms_core'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'wms_core'
    assert RELEASE_EVIDENCE['ok'] is True


def test_manifest_and_event_contract():
    assert PBC_MANIFEST['pbc'] == 'wms_core'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('wms_core_')
    assert EVENT_CONTRACT['inbox_table'].startswith('wms_core_')


def test_registration_plan_is_side_effect_free():
    from .. import register_pbc, registration_plan

    assert register_pbc()['pbc'] == 'wms_core'
    plan = registration_plan()
    assert plan['ok'] is True
    assert plan['catalog_patch']


def test_service_and_route_surface_are_executable():
    from .. import routes, services

    service_smoke = services.smoke_test()
    route_smoke = routes.smoke_test()
    assert service_smoke['ok'] is True
    assert route_smoke['ok'] is True
    assert not service_smoke['side_effects']
    assert not route_smoke['side_effects']


def test_configuration_permissions_and_seed_hooks_are_executable():
    from .. import config, permissions, seed_data

    config_smoke = config.smoke_test()
    permission_smoke = permissions.smoke_test()
    seed_smoke = seed_data.smoke_test()
    assert config_smoke['ok'] is True
    assert permission_smoke['ok'] is True
    assert seed_smoke['ok'] is True
    assert not config_smoke['side_effects']
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
    assert smoke['first_result']['dead_letter_table'].startswith('wms_core_')
    assert smoke['duplicate_result']['duplicate'] is True
    assert smoke['unknown_result']['handled'] is False
    assert not smoke['side_effects']
