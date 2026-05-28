from pyAppGen.pbcs.field_service_management import implementation_contract, field_service_management_runtime_capabilities, field_service_management_runtime_smoke, field_service_management_build_schema_contract, field_service_management_build_service_contract, field_service_management_build_release_evidence, field_service_management_receive_event, field_service_management_ui_contract, field_service_management_verify_owned_table_boundary, field_service_management_configure_runtime, field_service_management_set_parameter, field_service_management_register_rule


def test_field_service_management_runtime_capabilities_and_smoke():
    runtime = field_service_management_runtime_capabilities()
    smoke = field_service_management_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'field_service_management'


def test_field_service_management_contracts_events_workbench_and_boundary():
    assert field_service_management_build_schema_contract()['ok'] is True
    assert field_service_management_build_service_contract()['ok'] is True
    assert field_service_management_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'field_service_management'
    assert field_service_management_receive_event(field_service_management_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.field_service_management.events'})['state'], {'event_type': ('ServiceTicketOpened', 'InventoryPositionUpdated', 'CustomerUpdated')[0], 'event_id': 'evt'})['ok'] is True
    assert field_service_management_ui_contract()['ok'] is True  # workbench ui_contract
    assert field_service_management_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert field_service_management_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.field_service_management.events'})['ok'] is True
    assert field_service_management_set_parameter(state, 'threshold', 1)['ok'] is True
    assert field_service_management_register_rule(state, {'rule_id':'r1'})['ok'] is True
