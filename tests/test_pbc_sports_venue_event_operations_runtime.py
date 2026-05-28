from pyAppGen.pbcs.sports_venue_event_operations import implementation_contract, sports_venue_event_operations_runtime_capabilities, sports_venue_event_operations_runtime_smoke, sports_venue_event_operations_build_schema_contract, sports_venue_event_operations_build_service_contract, sports_venue_event_operations_build_release_evidence, sports_venue_event_operations_receive_event, sports_venue_event_operations_verify_owned_table_boundary, sports_venue_event_operations_configure_runtime, sports_venue_event_operations_set_parameter, sports_venue_event_operations_register_rule, sports_venue_event_operations_empty_state
from pyAppGen.pbcs.sports_venue_event_operations.ui import sports_venue_event_operations_ui_contract, sports_venue_event_operations_render_workbench


def test_sports_venue_event_operations_runtime_capabilities_and_contracts():
    runtime = sports_venue_event_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/sports_venue_event_operations'
    assert sports_venue_event_operations_build_schema_contract()['ok'] is True
    assert sports_venue_event_operations_build_service_contract()['ok'] is True
    assert sports_venue_event_operations_build_release_evidence()['ok'] is True
    assert sports_venue_event_operations_runtime_smoke()['ok'] is True


def test_sports_venue_event_operations_events_ui_boundary_and_configuration():
    state = sports_venue_event_operations_empty_state()
    assert sports_venue_event_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.sports_venue_event_operations.events'})['ok'] is True
    assert sports_venue_event_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert sports_venue_event_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert sports_venue_event_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert sports_venue_event_operations_ui_contract()['ok'] is True
    assert sports_venue_event_operations_render_workbench()['ok'] is True
    assert sports_venue_event_operations_verify_owned_table_boundary((f'sports_venue_event_operations_owned_table', 'foreign_table'))['ok'] is False
