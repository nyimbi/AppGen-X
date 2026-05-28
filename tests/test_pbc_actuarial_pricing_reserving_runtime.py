from pyAppGen.pbcs.actuarial_pricing_reserving import implementation_contract, actuarial_pricing_reserving_runtime_capabilities, actuarial_pricing_reserving_runtime_smoke, actuarial_pricing_reserving_build_schema_contract, actuarial_pricing_reserving_build_service_contract, actuarial_pricing_reserving_build_release_evidence, actuarial_pricing_reserving_receive_event, actuarial_pricing_reserving_verify_owned_table_boundary, actuarial_pricing_reserving_configure_runtime, actuarial_pricing_reserving_set_parameter, actuarial_pricing_reserving_register_rule, actuarial_pricing_reserving_empty_state
from pyAppGen.pbcs.actuarial_pricing_reserving.ui import actuarial_pricing_reserving_ui_contract, actuarial_pricing_reserving_render_workbench


def test_actuarial_pricing_reserving_runtime_capabilities_and_contracts():
    runtime = actuarial_pricing_reserving_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/actuarial_pricing_reserving'
    assert actuarial_pricing_reserving_build_schema_contract()['ok'] is True
    assert actuarial_pricing_reserving_build_service_contract()['ok'] is True
    assert actuarial_pricing_reserving_build_release_evidence()['ok'] is True
    assert actuarial_pricing_reserving_runtime_smoke()['ok'] is True


def test_actuarial_pricing_reserving_events_ui_boundary_and_configuration():
    state = actuarial_pricing_reserving_empty_state()
    assert actuarial_pricing_reserving_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.actuarial_pricing_reserving.events'})['ok'] is True
    assert actuarial_pricing_reserving_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert actuarial_pricing_reserving_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert actuarial_pricing_reserving_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert actuarial_pricing_reserving_ui_contract()['ok'] is True
    assert actuarial_pricing_reserving_render_workbench()['ok'] is True
    assert actuarial_pricing_reserving_verify_owned_table_boundary((f'actuarial_pricing_reserving_owned_table', 'foreign_table'))['ok'] is False
