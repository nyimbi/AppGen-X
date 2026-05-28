from pyAppGen.pbcs.legal_matter_management import implementation_contract, legal_matter_management_runtime_capabilities, legal_matter_management_runtime_smoke, legal_matter_management_build_schema_contract, legal_matter_management_build_service_contract, legal_matter_management_build_release_evidence, legal_matter_management_receive_event, legal_matter_management_ui_contract, legal_matter_management_verify_owned_table_boundary, legal_matter_management_configure_runtime, legal_matter_management_set_parameter, legal_matter_management_register_rule


def test_legal_matter_management_runtime_capabilities_and_smoke():
    runtime = legal_matter_management_runtime_capabilities()
    smoke = legal_matter_management_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'legal_matter_management'


def test_legal_matter_management_contracts_events_workbench_and_boundary():
    assert legal_matter_management_build_schema_contract()['ok'] is True
    assert legal_matter_management_build_service_contract()['ok'] is True
    assert legal_matter_management_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'legal_matter_management'
    assert legal_matter_management_receive_event(legal_matter_management_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.legal_matter_management.events'})['state'], {'event_type': ('ContractApproved', 'InvoiceApproved', 'RiskAssessed')[0], 'event_id': 'evt'})['ok'] is True
    assert legal_matter_management_ui_contract()['ok'] is True  # workbench ui_contract
    assert legal_matter_management_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert legal_matter_management_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.legal_matter_management.events'})['ok'] is True
    assert legal_matter_management_set_parameter(state, 'threshold', 1)['ok'] is True
    assert legal_matter_management_register_rule(state, {'rule_id':'r1'})['ok'] is True
