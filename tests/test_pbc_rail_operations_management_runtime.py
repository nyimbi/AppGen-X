from pyAppGen.pbcs.rail_operations_management import implementation_contract, rail_operations_management_runtime_capabilities, rail_operations_management_runtime_smoke, rail_operations_management_build_schema_contract, rail_operations_management_build_service_contract, rail_operations_management_build_release_evidence, rail_operations_management_receive_event, rail_operations_management_verify_owned_table_boundary, rail_operations_management_configure_runtime, rail_operations_management_set_parameter, rail_operations_management_register_rule, rail_operations_management_empty_state
from pyAppGen.pbcs.rail_operations_management.ui import rail_operations_management_ui_contract, rail_operations_management_render_workbench


def test_rail_operations_management_runtime_capabilities_and_contracts():
    runtime = rail_operations_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/rail_operations_management'
    assert rail_operations_management_build_schema_contract()['ok'] is True
    assert rail_operations_management_build_service_contract()['ok'] is True
    assert rail_operations_management_build_release_evidence()['ok'] is True
    assert rail_operations_management_runtime_smoke()['ok'] is True


def test_rail_operations_management_events_ui_boundary_and_configuration():
    state = rail_operations_management_empty_state()
    assert rail_operations_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.rail_operations_management.events'})['ok'] is True
    assert rail_operations_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert rail_operations_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert rail_operations_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert rail_operations_management_ui_contract()['ok'] is True
    assert rail_operations_management_render_workbench()['ok'] is True
    assert rail_operations_management_verify_owned_table_boundary((f'rail_operations_management_owned_table', 'foreign_table'))['ok'] is False
