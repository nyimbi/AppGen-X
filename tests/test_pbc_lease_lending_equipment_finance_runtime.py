from pyAppGen.pbcs.lease_lending_equipment_finance import implementation_contract, lease_lending_equipment_finance_runtime_capabilities, lease_lending_equipment_finance_runtime_smoke, lease_lending_equipment_finance_build_schema_contract, lease_lending_equipment_finance_build_service_contract, lease_lending_equipment_finance_build_release_evidence, lease_lending_equipment_finance_receive_event, lease_lending_equipment_finance_verify_owned_table_boundary, lease_lending_equipment_finance_configure_runtime, lease_lending_equipment_finance_set_parameter, lease_lending_equipment_finance_register_rule, lease_lending_equipment_finance_empty_state
from pyAppGen.pbcs.lease_lending_equipment_finance.ui import lease_lending_equipment_finance_ui_contract, lease_lending_equipment_finance_render_workbench


def test_lease_lending_equipment_finance_runtime_capabilities_and_contracts():
    runtime = lease_lending_equipment_finance_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/lease_lending_equipment_finance'
    assert lease_lending_equipment_finance_build_schema_contract()['ok'] is True
    assert lease_lending_equipment_finance_build_service_contract()['ok'] is True
    assert lease_lending_equipment_finance_build_release_evidence()['ok'] is True
    assert lease_lending_equipment_finance_runtime_smoke()['ok'] is True


def test_lease_lending_equipment_finance_events_ui_boundary_and_configuration():
    state = lease_lending_equipment_finance_empty_state()
    assert lease_lending_equipment_finance_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.lease_lending_equipment_finance.events'})['ok'] is True
    assert lease_lending_equipment_finance_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert lease_lending_equipment_finance_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert lease_lending_equipment_finance_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert lease_lending_equipment_finance_ui_contract()['ok'] is True
    assert lease_lending_equipment_finance_render_workbench()['ok'] is True
    assert lease_lending_equipment_finance_verify_owned_table_boundary((f'lease_lending_equipment_finance_owned_table', 'foreign_table'))['ok'] is False
