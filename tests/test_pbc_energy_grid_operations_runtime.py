from pyAppGen.pbcs.energy_grid_operations import implementation_contract, energy_grid_operations_runtime_capabilities, energy_grid_operations_runtime_smoke, energy_grid_operations_build_schema_contract, energy_grid_operations_build_service_contract, energy_grid_operations_build_release_evidence, energy_grid_operations_receive_event, energy_grid_operations_verify_owned_table_boundary, energy_grid_operations_configure_runtime, energy_grid_operations_set_parameter, energy_grid_operations_register_rule, energy_grid_operations_empty_state
from pyAppGen.pbcs.energy_grid_operations.ui import energy_grid_operations_ui_contract, energy_grid_operations_render_workbench


def test_energy_grid_operations_runtime_capabilities_and_contracts():
    runtime = energy_grid_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/energy_grid_operations'
    assert energy_grid_operations_build_schema_contract()['ok'] is True
    assert energy_grid_operations_build_service_contract()['ok'] is True
    assert energy_grid_operations_build_release_evidence()['ok'] is True
    assert energy_grid_operations_runtime_smoke()['ok'] is True


def test_energy_grid_operations_events_ui_boundary_and_configuration():
    state = energy_grid_operations_empty_state()
    assert energy_grid_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.energy_grid_operations.events'})['ok'] is True
    assert energy_grid_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert energy_grid_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert energy_grid_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert energy_grid_operations_ui_contract()['ok'] is True
    assert energy_grid_operations_render_workbench()['ok'] is True
    assert energy_grid_operations_verify_owned_table_boundary((f'energy_grid_operations_owned_table', 'foreign_table'))['ok'] is False
