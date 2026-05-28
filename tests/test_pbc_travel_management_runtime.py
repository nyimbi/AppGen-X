from pyAppGen.pbcs.travel_management import implementation_contract, travel_management_runtime_capabilities, travel_management_runtime_smoke, travel_management_build_schema_contract, travel_management_build_service_contract, travel_management_build_release_evidence, travel_management_receive_event, travel_management_ui_contract, travel_management_verify_owned_table_boundary, travel_management_configure_runtime, travel_management_set_parameter, travel_management_register_rule


def test_travel_management_runtime_capabilities_and_smoke():
    runtime = travel_management_runtime_capabilities()
    smoke = travel_management_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'travel_management'


def test_travel_management_contracts_events_workbench_and_boundary():
    assert travel_management_build_schema_contract()['ok'] is True
    assert travel_management_build_service_contract()['ok'] is True
    assert travel_management_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'travel_management'
    assert travel_management_receive_event(travel_management_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.travel_management.events'})['state'], {'event_type': ('EmployeeProvisioned', 'ExpenseApproved', 'SupplierQualified')[0], 'event_id': 'evt'})['ok'] is True
    assert travel_management_ui_contract()['ok'] is True  # workbench ui_contract
    assert travel_management_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert travel_management_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.travel_management.events'})['ok'] is True
    assert travel_management_set_parameter(state, 'threshold', 1)['ok'] is True
    assert travel_management_register_rule(state, {'rule_id':'r1'})['ok'] is True
