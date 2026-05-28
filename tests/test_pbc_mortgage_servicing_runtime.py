from pyAppGen.pbcs.mortgage_servicing import implementation_contract, mortgage_servicing_runtime_capabilities, mortgage_servicing_runtime_smoke, mortgage_servicing_build_schema_contract, mortgage_servicing_build_service_contract, mortgage_servicing_build_release_evidence, mortgage_servicing_receive_event, mortgage_servicing_verify_owned_table_boundary, mortgage_servicing_configure_runtime, mortgage_servicing_set_parameter, mortgage_servicing_register_rule, mortgage_servicing_empty_state
from pyAppGen.pbcs.mortgage_servicing.ui import mortgage_servicing_ui_contract, mortgage_servicing_render_workbench


def test_mortgage_servicing_runtime_capabilities_and_contracts():
    runtime = mortgage_servicing_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/mortgage_servicing'
    assert mortgage_servicing_build_schema_contract()['ok'] is True
    assert mortgage_servicing_build_service_contract()['ok'] is True
    assert mortgage_servicing_build_release_evidence()['ok'] is True
    assert mortgage_servicing_runtime_smoke()['ok'] is True


def test_mortgage_servicing_events_ui_boundary_and_configuration():
    state = mortgage_servicing_empty_state()
    assert mortgage_servicing_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.mortgage_servicing.events'})['ok'] is True
    assert mortgage_servicing_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert mortgage_servicing_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert mortgage_servicing_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert mortgage_servicing_ui_contract()['ok'] is True
    assert mortgage_servicing_render_workbench()['ok'] is True
    assert mortgage_servicing_verify_owned_table_boundary((f'mortgage_servicing_owned_table', 'foreign_table'))['ok'] is False
