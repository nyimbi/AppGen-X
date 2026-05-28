from pyAppGen.pbcs.lending_origination_servicing import implementation_contract, lending_origination_servicing_runtime_capabilities, lending_origination_servicing_runtime_smoke, lending_origination_servicing_build_schema_contract, lending_origination_servicing_build_service_contract, lending_origination_servicing_build_release_evidence, lending_origination_servicing_receive_event, lending_origination_servicing_verify_owned_table_boundary, lending_origination_servicing_configure_runtime, lending_origination_servicing_set_parameter, lending_origination_servicing_register_rule, lending_origination_servicing_empty_state
from pyAppGen.pbcs.lending_origination_servicing.ui import lending_origination_servicing_ui_contract, lending_origination_servicing_render_workbench


def test_lending_origination_servicing_runtime_capabilities_and_contracts():
    runtime = lending_origination_servicing_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/lending_origination_servicing'
    assert lending_origination_servicing_build_schema_contract()['ok'] is True
    assert lending_origination_servicing_build_service_contract()['ok'] is True
    assert lending_origination_servicing_build_release_evidence()['ok'] is True
    assert lending_origination_servicing_runtime_smoke()['ok'] is True


def test_lending_origination_servicing_events_ui_boundary_and_configuration():
    state = lending_origination_servicing_empty_state()
    assert lending_origination_servicing_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.lending_origination_servicing.events'})['ok'] is True
    assert lending_origination_servicing_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert lending_origination_servicing_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert lending_origination_servicing_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert lending_origination_servicing_ui_contract()['ok'] is True
    assert lending_origination_servicing_render_workbench()['ok'] is True
    assert lending_origination_servicing_verify_owned_table_boundary((f'lending_origination_servicing_owned_table', 'foreign_table'))['ok'] is False
