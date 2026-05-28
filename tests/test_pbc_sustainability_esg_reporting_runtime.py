from pyAppGen.pbcs.sustainability_esg_reporting import implementation_contract, sustainability_esg_reporting_runtime_capabilities, sustainability_esg_reporting_runtime_smoke, sustainability_esg_reporting_build_schema_contract, sustainability_esg_reporting_build_service_contract, sustainability_esg_reporting_build_release_evidence, sustainability_esg_reporting_receive_event, sustainability_esg_reporting_ui_contract, sustainability_esg_reporting_verify_owned_table_boundary, sustainability_esg_reporting_configure_runtime, sustainability_esg_reporting_set_parameter, sustainability_esg_reporting_register_rule


def test_sustainability_esg_reporting_runtime_capabilities_and_smoke():
    runtime = sustainability_esg_reporting_runtime_capabilities()
    smoke = sustainability_esg_reporting_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'sustainability_esg_reporting'


def test_sustainability_esg_reporting_contracts_events_workbench_and_boundary():
    assert sustainability_esg_reporting_build_schema_contract()['ok'] is True
    assert sustainability_esg_reporting_build_service_contract()['ok'] is True
    assert sustainability_esg_reporting_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'sustainability_esg_reporting'
    assert sustainability_esg_reporting_receive_event(sustainability_esg_reporting_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.sustainability_esg_reporting.events'})['state'], {'event_type': ('SupplierQualified', 'TravelBooked', 'AssetPlacedInService')[0], 'event_id': 'evt'})['ok'] is True
    assert sustainability_esg_reporting_ui_contract()['ok'] is True  # workbench ui_contract
    assert sustainability_esg_reporting_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert sustainability_esg_reporting_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.sustainability_esg_reporting.events'})['ok'] is True
    assert sustainability_esg_reporting_set_parameter(state, 'threshold', 1)['ok'] is True
    assert sustainability_esg_reporting_register_rule(state, {'rule_id':'r1'})['ok'] is True
