from pyAppGen.pbcs.identity_kyc_aml_compliance import implementation_contract, identity_kyc_aml_compliance_runtime_capabilities, identity_kyc_aml_compliance_runtime_smoke, identity_kyc_aml_compliance_build_schema_contract, identity_kyc_aml_compliance_build_service_contract, identity_kyc_aml_compliance_build_release_evidence, identity_kyc_aml_compliance_receive_event, identity_kyc_aml_compliance_verify_owned_table_boundary, identity_kyc_aml_compliance_configure_runtime, identity_kyc_aml_compliance_set_parameter, identity_kyc_aml_compliance_register_rule, identity_kyc_aml_compliance_empty_state
from pyAppGen.pbcs.identity_kyc_aml_compliance.ui import identity_kyc_aml_compliance_ui_contract, identity_kyc_aml_compliance_render_workbench


def test_identity_kyc_aml_compliance_runtime_capabilities_and_contracts():
    runtime = identity_kyc_aml_compliance_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/identity_kyc_aml_compliance'
    assert identity_kyc_aml_compliance_build_schema_contract()['ok'] is True
    assert identity_kyc_aml_compliance_build_service_contract()['ok'] is True
    assert identity_kyc_aml_compliance_build_release_evidence()['ok'] is True
    assert identity_kyc_aml_compliance_runtime_smoke()['ok'] is True


def test_identity_kyc_aml_compliance_events_ui_boundary_and_configuration():
    state = identity_kyc_aml_compliance_empty_state()
    assert identity_kyc_aml_compliance_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.identity_kyc_aml_compliance.events'})['ok'] is True
    assert identity_kyc_aml_compliance_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert identity_kyc_aml_compliance_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert identity_kyc_aml_compliance_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert identity_kyc_aml_compliance_ui_contract()['ok'] is True
    assert identity_kyc_aml_compliance_render_workbench()['ok'] is True
    assert identity_kyc_aml_compliance_verify_owned_table_boundary((f'identity_kyc_aml_compliance_owned_table', 'foreign_table'))['ok'] is False
