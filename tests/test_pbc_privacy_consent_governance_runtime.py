from pyAppGen.pbcs.privacy_consent_governance import implementation_contract, privacy_consent_governance_runtime_capabilities, privacy_consent_governance_runtime_smoke, privacy_consent_governance_build_schema_contract, privacy_consent_governance_build_service_contract, privacy_consent_governance_build_release_evidence, privacy_consent_governance_receive_event, privacy_consent_governance_ui_contract, privacy_consent_governance_verify_owned_table_boundary, privacy_consent_governance_configure_runtime, privacy_consent_governance_set_parameter, privacy_consent_governance_register_rule


def test_privacy_consent_governance_runtime_capabilities_and_smoke():
    runtime = privacy_consent_governance_runtime_capabilities()
    smoke = privacy_consent_governance_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'privacy_consent_governance'


def test_privacy_consent_governance_contracts_events_workbench_and_boundary():
    assert privacy_consent_governance_build_schema_contract()['ok'] is True
    assert privacy_consent_governance_build_service_contract()['ok'] is True
    assert privacy_consent_governance_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'privacy_consent_governance'
    assert privacy_consent_governance_receive_event(privacy_consent_governance_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.privacy_consent_governance.events'})['state'], {'event_type': ('CustomerUpdated', 'AccessPolicyChanged', 'AuditProofGenerated')[0], 'event_id': 'evt'})['ok'] is True
    assert privacy_consent_governance_ui_contract()['ok'] is True  # workbench ui_contract
    assert privacy_consent_governance_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert privacy_consent_governance_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.privacy_consent_governance.events'})['ok'] is True
    assert privacy_consent_governance_set_parameter(state, 'threshold', 1)['ok'] is True
    assert privacy_consent_governance_register_rule(state, {'rule_id':'r1'})['ok'] is True
