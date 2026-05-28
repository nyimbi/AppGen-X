from pyAppGen.pbcs.policy_administration_insurance import implementation_contract, policy_administration_insurance_runtime_capabilities, policy_administration_insurance_runtime_smoke, policy_administration_insurance_build_schema_contract, policy_administration_insurance_build_service_contract, policy_administration_insurance_build_release_evidence, policy_administration_insurance_receive_event, policy_administration_insurance_verify_owned_table_boundary, policy_administration_insurance_configure_runtime, policy_administration_insurance_set_parameter, policy_administration_insurance_register_rule, policy_administration_insurance_empty_state
from pyAppGen.pbcs.policy_administration_insurance.ui import policy_administration_insurance_ui_contract, policy_administration_insurance_render_workbench


def test_policy_administration_insurance_runtime_capabilities_and_contracts():
    runtime = policy_administration_insurance_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/policy_administration_insurance'
    assert policy_administration_insurance_build_schema_contract()['ok'] is True
    assert policy_administration_insurance_build_service_contract()['ok'] is True
    assert policy_administration_insurance_build_release_evidence()['ok'] is True
    assert policy_administration_insurance_runtime_smoke()['ok'] is True


def test_policy_administration_insurance_events_ui_boundary_and_configuration():
    state = policy_administration_insurance_empty_state()
    assert policy_administration_insurance_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.policy_administration_insurance.events'})['ok'] is True
    assert policy_administration_insurance_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert policy_administration_insurance_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert policy_administration_insurance_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert policy_administration_insurance_ui_contract()['ok'] is True
    assert policy_administration_insurance_render_workbench()['ok'] is True
    assert policy_administration_insurance_verify_owned_table_boundary((f'policy_administration_insurance_owned_table', 'foreign_table'))['ok'] is False
