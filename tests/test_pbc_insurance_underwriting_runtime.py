from pyAppGen.pbcs.insurance_underwriting import implementation_contract, insurance_underwriting_runtime_capabilities, insurance_underwriting_runtime_smoke, insurance_underwriting_build_schema_contract, insurance_underwriting_build_service_contract, insurance_underwriting_build_release_evidence, insurance_underwriting_receive_event, insurance_underwriting_verify_owned_table_boundary, insurance_underwriting_configure_runtime, insurance_underwriting_set_parameter, insurance_underwriting_register_rule, insurance_underwriting_empty_state
from pyAppGen.pbcs.insurance_underwriting.ui import insurance_underwriting_ui_contract, insurance_underwriting_render_workbench


def test_insurance_underwriting_runtime_capabilities_and_contracts():
    runtime = insurance_underwriting_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/insurance_underwriting'
    assert insurance_underwriting_build_schema_contract()['ok'] is True
    assert insurance_underwriting_build_service_contract()['ok'] is True
    assert insurance_underwriting_build_release_evidence()['ok'] is True
    assert insurance_underwriting_runtime_smoke()['ok'] is True


def test_insurance_underwriting_events_ui_boundary_and_configuration():
    state = insurance_underwriting_empty_state()
    assert insurance_underwriting_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.insurance_underwriting.events'})['ok'] is True
    assert insurance_underwriting_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert insurance_underwriting_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert insurance_underwriting_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert insurance_underwriting_ui_contract()['ok'] is True
    assert insurance_underwriting_render_workbench()['ok'] is True
    assert insurance_underwriting_verify_owned_table_boundary((f'insurance_underwriting_owned_table', 'foreign_table'))['ok'] is False
