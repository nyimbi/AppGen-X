from pyAppGen.pbcs.contract_lifecycle import implementation_contract, contract_lifecycle_runtime_capabilities, contract_lifecycle_runtime_smoke, contract_lifecycle_build_schema_contract, contract_lifecycle_build_service_contract, contract_lifecycle_build_release_evidence, contract_lifecycle_receive_event, contract_lifecycle_ui_contract, contract_lifecycle_verify_owned_table_boundary, contract_lifecycle_configure_runtime, contract_lifecycle_set_parameter, contract_lifecycle_register_rule


def test_contract_lifecycle_runtime_capabilities_and_smoke():
    runtime = contract_lifecycle_runtime_capabilities()
    smoke = contract_lifecycle_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'contract_lifecycle'


def test_contract_lifecycle_contracts_events_workbench_and_boundary():
    assert contract_lifecycle_build_schema_contract()['ok'] is True
    assert contract_lifecycle_build_service_contract()['ok'] is True
    assert contract_lifecycle_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'contract_lifecycle'
    assert contract_lifecycle_receive_event(contract_lifecycle_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.contract_lifecycle.events'})['state'], {'event_type': ('CustomerUpdated', 'SupplierQualified', 'PolicyChanged')[0], 'event_id': 'evt'})['ok'] is True
    assert contract_lifecycle_ui_contract()['ok'] is True  # workbench ui_contract
    assert contract_lifecycle_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert contract_lifecycle_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.contract_lifecycle.events'})['ok'] is True
    assert contract_lifecycle_set_parameter(state, 'threshold', 1)['ok'] is True
    assert contract_lifecycle_register_rule(state, {'rule_id':'r1'})['ok'] is True
