from pyAppGen.pbcs.revenue_recognition import implementation_contract, revenue_recognition_runtime_capabilities, revenue_recognition_runtime_smoke, revenue_recognition_build_schema_contract, revenue_recognition_build_service_contract, revenue_recognition_build_release_evidence, revenue_recognition_receive_event, revenue_recognition_ui_contract, revenue_recognition_verify_owned_table_boundary, revenue_recognition_configure_runtime, revenue_recognition_set_parameter, revenue_recognition_register_rule


def test_revenue_recognition_runtime_capabilities_and_smoke():
    runtime = revenue_recognition_runtime_capabilities()
    smoke = revenue_recognition_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'revenue_recognition'


def test_revenue_recognition_contracts_events_workbench_and_boundary():
    assert revenue_recognition_build_schema_contract()['ok'] is True
    assert revenue_recognition_build_service_contract()['ok'] is True
    assert revenue_recognition_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'revenue_recognition'
    assert revenue_recognition_receive_event(revenue_recognition_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.revenue_recognition.events'})['state'], {'event_type': ('ContractApproved', 'InvoiceIssued', 'PaymentCaptured')[0], 'event_id': 'evt'})['ok'] is True
    assert revenue_recognition_ui_contract()['ok'] is True  # workbench ui_contract
    assert revenue_recognition_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert revenue_recognition_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.revenue_recognition.events'})['ok'] is True
    assert revenue_recognition_set_parameter(state, 'threshold', 1)['ok'] is True
    assert revenue_recognition_register_rule(state, {'rule_id':'r1'})['ok'] is True
