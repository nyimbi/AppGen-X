from pyAppGen.pbcs.water_wastewater_operations import implementation_contract, water_wastewater_operations_runtime_capabilities, water_wastewater_operations_runtime_smoke, water_wastewater_operations_build_schema_contract, water_wastewater_operations_build_service_contract, water_wastewater_operations_build_release_evidence, water_wastewater_operations_receive_event, water_wastewater_operations_verify_owned_table_boundary, water_wastewater_operations_configure_runtime, water_wastewater_operations_set_parameter, water_wastewater_operations_register_rule, water_wastewater_operations_empty_state
from pyAppGen.pbcs.water_wastewater_operations.ui import water_wastewater_operations_ui_contract, water_wastewater_operations_render_workbench


def test_water_wastewater_operations_runtime_capabilities_and_contracts():
    runtime = water_wastewater_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/water_wastewater_operations'
    assert water_wastewater_operations_build_schema_contract()['ok'] is True
    assert water_wastewater_operations_build_service_contract()['ok'] is True
    assert water_wastewater_operations_build_release_evidence()['ok'] is True
    assert water_wastewater_operations_runtime_smoke()['ok'] is True


def test_water_wastewater_operations_events_ui_boundary_and_configuration():
    state = water_wastewater_operations_empty_state()
    assert water_wastewater_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.water_wastewater_operations.events'})['ok'] is True
    assert water_wastewater_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert water_wastewater_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert water_wastewater_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert water_wastewater_operations_ui_contract()['ok'] is True
    assert water_wastewater_operations_render_workbench()['ok'] is True
    assert water_wastewater_operations_verify_owned_table_boundary((f'water_wastewater_operations_owned_table', 'foreign_table'))['ok'] is False
