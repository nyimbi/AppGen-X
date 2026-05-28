from pyAppGen.pbcs.aviation_maintenance_repair import implementation_contract, aviation_maintenance_repair_runtime_capabilities, aviation_maintenance_repair_runtime_smoke, aviation_maintenance_repair_build_schema_contract, aviation_maintenance_repair_build_service_contract, aviation_maintenance_repair_build_release_evidence, aviation_maintenance_repair_receive_event, aviation_maintenance_repair_verify_owned_table_boundary, aviation_maintenance_repair_configure_runtime, aviation_maintenance_repair_set_parameter, aviation_maintenance_repair_register_rule, aviation_maintenance_repair_empty_state
from pyAppGen.pbcs.aviation_maintenance_repair.ui import aviation_maintenance_repair_ui_contract, aviation_maintenance_repair_render_workbench


def test_aviation_maintenance_repair_runtime_capabilities_and_contracts():
    runtime = aviation_maintenance_repair_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/aviation_maintenance_repair'
    assert aviation_maintenance_repair_build_schema_contract()['ok'] is True
    assert aviation_maintenance_repair_build_service_contract()['ok'] is True
    assert aviation_maintenance_repair_build_release_evidence()['ok'] is True
    assert aviation_maintenance_repair_runtime_smoke()['ok'] is True


def test_aviation_maintenance_repair_events_ui_boundary_and_configuration():
    state = aviation_maintenance_repair_empty_state()
    assert aviation_maintenance_repair_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.aviation_maintenance_repair.events'})['ok'] is True
    assert aviation_maintenance_repair_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert aviation_maintenance_repair_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert aviation_maintenance_repair_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert aviation_maintenance_repair_ui_contract()['ok'] is True
    assert aviation_maintenance_repair_render_workbench()['ok'] is True
    assert aviation_maintenance_repair_verify_owned_table_boundary((f'aviation_maintenance_repair_owned_table', 'foreign_table'))['ok'] is False
