from pyAppGen.pbcs.enterprise_risk_controls import implementation_contract, enterprise_risk_controls_runtime_capabilities, enterprise_risk_controls_runtime_smoke, enterprise_risk_controls_build_schema_contract, enterprise_risk_controls_build_service_contract, enterprise_risk_controls_build_release_evidence, enterprise_risk_controls_receive_event, enterprise_risk_controls_ui_contract, enterprise_risk_controls_verify_owned_table_boundary, enterprise_risk_controls_configure_runtime, enterprise_risk_controls_set_parameter, enterprise_risk_controls_register_rule


def test_enterprise_risk_controls_runtime_capabilities_and_smoke():
    runtime = enterprise_risk_controls_runtime_capabilities()
    smoke = enterprise_risk_controls_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'enterprise_risk_controls'


def test_enterprise_risk_controls_contracts_events_workbench_and_boundary():
    assert enterprise_risk_controls_build_schema_contract()['ok'] is True
    assert enterprise_risk_controls_build_service_contract()['ok'] is True
    assert enterprise_risk_controls_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'enterprise_risk_controls'
    assert enterprise_risk_controls_receive_event(enterprise_risk_controls_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.enterprise_risk_controls.events'})['state'], {'event_type': ('PolicyChanged', 'AuditProofGenerated', 'AccessPolicyChanged')[0], 'event_id': 'evt'})['ok'] is True
    assert enterprise_risk_controls_ui_contract()['ok'] is True  # workbench ui_contract
    assert enterprise_risk_controls_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert enterprise_risk_controls_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.enterprise_risk_controls.events'})['ok'] is True
    assert enterprise_risk_controls_set_parameter(state, 'threshold', 1)['ok'] is True
    assert enterprise_risk_controls_register_rule(state, {'rule_id':'r1'})['ok'] is True
