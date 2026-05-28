from pyAppGen.pbcs.claims_adjudication_healthcare import implementation_contract, claims_adjudication_healthcare_runtime_capabilities, claims_adjudication_healthcare_runtime_smoke, claims_adjudication_healthcare_build_schema_contract, claims_adjudication_healthcare_build_service_contract, claims_adjudication_healthcare_build_release_evidence, claims_adjudication_healthcare_receive_event, claims_adjudication_healthcare_verify_owned_table_boundary, claims_adjudication_healthcare_configure_runtime, claims_adjudication_healthcare_set_parameter, claims_adjudication_healthcare_register_rule, claims_adjudication_healthcare_empty_state
from pyAppGen.pbcs.claims_adjudication_healthcare.ui import claims_adjudication_healthcare_ui_contract, claims_adjudication_healthcare_render_workbench


def test_claims_adjudication_healthcare_runtime_capabilities_and_contracts():
    runtime = claims_adjudication_healthcare_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/claims_adjudication_healthcare'
    assert claims_adjudication_healthcare_build_schema_contract()['ok'] is True
    assert claims_adjudication_healthcare_build_service_contract()['ok'] is True
    assert claims_adjudication_healthcare_build_release_evidence()['ok'] is True
    assert claims_adjudication_healthcare_runtime_smoke()['ok'] is True


def test_claims_adjudication_healthcare_events_ui_boundary_and_configuration():
    state = claims_adjudication_healthcare_empty_state()
    assert claims_adjudication_healthcare_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.claims_adjudication_healthcare.events'})['ok'] is True
    assert claims_adjudication_healthcare_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert claims_adjudication_healthcare_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert claims_adjudication_healthcare_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert claims_adjudication_healthcare_ui_contract()['ok'] is True
    assert claims_adjudication_healthcare_render_workbench()['ok'] is True
    assert claims_adjudication_healthcare_verify_owned_table_boundary((f'claims_adjudication_healthcare_owned_table', 'foreign_table'))['ok'] is False
