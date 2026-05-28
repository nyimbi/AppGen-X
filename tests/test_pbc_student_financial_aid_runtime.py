from pyAppGen.pbcs.student_financial_aid import implementation_contract, student_financial_aid_runtime_capabilities, student_financial_aid_runtime_smoke, student_financial_aid_build_schema_contract, student_financial_aid_build_service_contract, student_financial_aid_build_release_evidence, student_financial_aid_receive_event, student_financial_aid_verify_owned_table_boundary, student_financial_aid_configure_runtime, student_financial_aid_set_parameter, student_financial_aid_register_rule, student_financial_aid_empty_state
from pyAppGen.pbcs.student_financial_aid.ui import student_financial_aid_ui_contract, student_financial_aid_render_workbench


def test_student_financial_aid_runtime_capabilities_and_contracts():
    runtime = student_financial_aid_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/student_financial_aid'
    assert student_financial_aid_build_schema_contract()['ok'] is True
    assert student_financial_aid_build_service_contract()['ok'] is True
    assert student_financial_aid_build_release_evidence()['ok'] is True
    assert student_financial_aid_runtime_smoke()['ok'] is True


def test_student_financial_aid_events_ui_boundary_and_configuration():
    state = student_financial_aid_empty_state()
    assert student_financial_aid_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.student_financial_aid.events'})['ok'] is True
    assert student_financial_aid_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert student_financial_aid_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert student_financial_aid_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert student_financial_aid_ui_contract()['ok'] is True
    assert student_financial_aid_render_workbench()['ok'] is True
    assert student_financial_aid_verify_owned_table_boundary((f'student_financial_aid_owned_table', 'foreign_table'))['ok'] is False
