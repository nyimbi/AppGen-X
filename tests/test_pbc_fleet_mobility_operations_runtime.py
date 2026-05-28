from pyAppGen.pbcs.fleet_mobility_operations import implementation_contract, fleet_mobility_operations_runtime_capabilities, fleet_mobility_operations_runtime_smoke, fleet_mobility_operations_build_schema_contract, fleet_mobility_operations_build_service_contract, fleet_mobility_operations_build_release_evidence, fleet_mobility_operations_receive_event, fleet_mobility_operations_verify_owned_table_boundary, fleet_mobility_operations_configure_runtime, fleet_mobility_operations_set_parameter, fleet_mobility_operations_register_rule, fleet_mobility_operations_empty_state
from pyAppGen.pbcs.fleet_mobility_operations.ui import fleet_mobility_operations_ui_contract, fleet_mobility_operations_render_workbench


def test_fleet_mobility_operations_runtime_capabilities_and_contracts():
    runtime = fleet_mobility_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/fleet_mobility_operations'
    assert fleet_mobility_operations_build_schema_contract()['ok'] is True
    assert fleet_mobility_operations_build_service_contract()['ok'] is True
    assert fleet_mobility_operations_build_release_evidence()['ok'] is True
    assert fleet_mobility_operations_runtime_smoke()['ok'] is True


def test_fleet_mobility_operations_events_ui_boundary_and_configuration():
    state = fleet_mobility_operations_empty_state()
    assert fleet_mobility_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.fleet_mobility_operations.events'})['ok'] is True
    assert fleet_mobility_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert fleet_mobility_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert fleet_mobility_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert fleet_mobility_operations_ui_contract()['ok'] is True
    assert fleet_mobility_operations_render_workbench()['ok'] is True
    assert fleet_mobility_operations_verify_owned_table_boundary((f'fleet_mobility_operations_owned_table', 'foreign_table'))['ok'] is False
