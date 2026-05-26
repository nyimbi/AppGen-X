"""Generated contract smoke tests for ap_automation."""

from ..manifest import PBC_MANIFEST
from ..events import EVENT_CONTRACT
from ..schema_contract import SCHEMA_CONTRACT
from ..service_contract import SERVICE_CONTRACT
from ..release_evidence import RELEASE_EVIDENCE


def test_generated_schema_service_and_release_evidence():
    assert SCHEMA_CONTRACT['pbc'] == 'ap_automation'
    assert SCHEMA_CONTRACT['ok'] is True
    assert SCHEMA_CONTRACT['owned_tables']
    assert SERVICE_CONTRACT['pbc'] == 'ap_automation'
    assert SERVICE_CONTRACT['ok'] is True
    assert SERVICE_CONTRACT.get('shared_table_access') is False
    assert RELEASE_EVIDENCE['pbc'] == 'ap_automation'
    assert RELEASE_EVIDENCE['ok'] is True


def test_manifest_and_event_contract():
    assert PBC_MANIFEST['pbc'] == 'ap_automation'
    assert PBC_MANIFEST['standard_features']
    assert PBC_MANIFEST['advanced_capabilities']
    assert EVENT_CONTRACT['contract'] == 'appgen_event_contract'
    assert EVENT_CONTRACT['outbox_table'].startswith('ap_automation_')
    assert EVENT_CONTRACT['inbox_table'].startswith('ap_automation_')


def test_registration_plan_is_side_effect_free():
    from .. import register_pbc, registration_plan

    assert register_pbc()['pbc'] == 'ap_automation'
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
