from pyAppGen.pbcs.renewables_asset_operations import implementation_contract, renewables_asset_operations_runtime_capabilities, renewables_asset_operations_runtime_smoke, renewables_asset_operations_build_schema_contract, renewables_asset_operations_build_service_contract, renewables_asset_operations_build_release_evidence, renewables_asset_operations_receive_event, renewables_asset_operations_verify_owned_table_boundary, renewables_asset_operations_configure_runtime, renewables_asset_operations_set_parameter, renewables_asset_operations_register_rule, renewables_asset_operations_empty_state
from pyAppGen.pbcs.renewables_asset_operations.ui import renewables_asset_operations_ui_contract, renewables_asset_operations_render_workbench


def test_renewables_asset_operations_runtime_capabilities_and_contracts():
    runtime = renewables_asset_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/renewables_asset_operations'
    assert renewables_asset_operations_build_schema_contract()['ok'] is True
    assert renewables_asset_operations_build_service_contract()['ok'] is True
    assert renewables_asset_operations_build_release_evidence()['ok'] is True
    assert renewables_asset_operations_runtime_smoke()['ok'] is True


def test_renewables_asset_operations_events_ui_boundary_and_configuration():
    state = renewables_asset_operations_empty_state()
    assert renewables_asset_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.renewables_asset_operations.events'})['ok'] is True
    assert renewables_asset_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert renewables_asset_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert renewables_asset_operations_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert renewables_asset_operations_ui_contract()['ok'] is True
    assert renewables_asset_operations_render_workbench()['ok'] is True
    assert renewables_asset_operations_verify_owned_table_boundary((f'renewables_asset_operations_owned_table', 'foreign_table'))['ok'] is False
