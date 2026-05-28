from pyAppGen.pbcs.master_data_governance import implementation_contract, master_data_governance_runtime_capabilities, master_data_governance_runtime_smoke, master_data_governance_build_schema_contract, master_data_governance_build_service_contract, master_data_governance_build_release_evidence, master_data_governance_receive_event, master_data_governance_ui_contract, master_data_governance_verify_owned_table_boundary, master_data_governance_configure_runtime, master_data_governance_set_parameter, master_data_governance_register_rule


def test_master_data_governance_runtime_capabilities_and_smoke():
    runtime = master_data_governance_runtime_capabilities()
    smoke = master_data_governance_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'master_data_governance'


def test_master_data_governance_contracts_events_workbench_and_boundary():
    assert master_data_governance_build_schema_contract()['ok'] is True
    assert master_data_governance_build_service_contract()['ok'] is True
    assert master_data_governance_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'master_data_governance'
    assert master_data_governance_receive_event(master_data_governance_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.master_data_governance.events'})['state'], {'event_type': ('CustomerUpdated', 'SupplierQualified', 'ProductPublished')[0], 'event_id': 'evt'})['ok'] is True
    assert master_data_governance_ui_contract()['ok'] is True  # workbench ui_contract
    assert master_data_governance_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert master_data_governance_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.master_data_governance.events'})['ok'] is True
    assert master_data_governance_set_parameter(state, 'threshold', 1)['ok'] is True
    assert master_data_governance_register_rule(state, {'rule_id':'r1'})['ok'] is True
