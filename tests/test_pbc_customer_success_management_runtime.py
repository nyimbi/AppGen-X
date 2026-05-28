from pyAppGen.pbcs.customer_success_management import implementation_contract, customer_success_management_runtime_capabilities, customer_success_management_runtime_smoke, customer_success_management_build_schema_contract, customer_success_management_build_service_contract, customer_success_management_build_release_evidence, customer_success_management_receive_event, customer_success_management_ui_contract, customer_success_management_verify_owned_table_boundary, customer_success_management_configure_runtime, customer_success_management_set_parameter, customer_success_management_register_rule


def test_customer_success_management_runtime_capabilities_and_smoke():
    runtime = customer_success_management_runtime_capabilities()
    smoke = customer_success_management_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'customer_success_management'


def test_customer_success_management_contracts_events_workbench_and_boundary():
    assert customer_success_management_build_schema_contract()['ok'] is True
    assert customer_success_management_build_service_contract()['ok'] is True
    assert customer_success_management_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'customer_success_management'
    assert customer_success_management_receive_event(customer_success_management_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.customer_success_management.events'})['state'], {'event_type': ('CustomerUpdated', 'SubscriptionRenewed', 'ServiceTicketResolved')[0], 'event_id': 'evt'})['ok'] is True
    assert customer_success_management_ui_contract()['ok'] is True  # workbench ui_contract
    assert customer_success_management_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert customer_success_management_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.customer_success_management.events'})['ok'] is True
    assert customer_success_management_set_parameter(state, 'threshold', 1)['ok'] is True
    assert customer_success_management_register_rule(state, {'rule_id':'r1'})['ok'] is True
