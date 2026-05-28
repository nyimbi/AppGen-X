from pyAppGen.pbcs.insurance_claims_policy import implementation_contract, insurance_claims_policy_runtime_capabilities, insurance_claims_policy_runtime_smoke, insurance_claims_policy_build_schema_contract, insurance_claims_policy_build_service_contract, insurance_claims_policy_build_release_evidence, insurance_claims_policy_receive_event, insurance_claims_policy_ui_contract, insurance_claims_policy_verify_owned_table_boundary, insurance_claims_policy_configure_runtime, insurance_claims_policy_set_parameter, insurance_claims_policy_register_rule


def test_insurance_claims_policy_runtime_capabilities_and_smoke():
    runtime = insurance_claims_policy_runtime_capabilities()
    smoke = insurance_claims_policy_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'insurance_claims_policy'


def test_insurance_claims_policy_contracts_events_workbench_and_boundary():
    assert insurance_claims_policy_build_schema_contract()['ok'] is True
    assert insurance_claims_policy_build_service_contract()['ok'] is True
    assert insurance_claims_policy_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'insurance_claims_policy'
    assert insurance_claims_policy_receive_event(insurance_claims_policy_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.insurance_claims_policy.events'})['state'], {'event_type': ('CustomerUpdated', 'PaymentCaptured', 'FraudRiskScored')[0], 'event_id': 'evt'})['ok'] is True
    assert insurance_claims_policy_ui_contract()['ok'] is True  # workbench ui_contract
    assert insurance_claims_policy_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert insurance_claims_policy_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.insurance_claims_policy.events'})['ok'] is True
    assert insurance_claims_policy_set_parameter(state, 'threshold', 1)['ok'] is True
    assert insurance_claims_policy_register_rule(state, {'rule_id':'r1'})['ok'] is True
