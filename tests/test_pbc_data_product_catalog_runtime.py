from pyAppGen.pbcs.data_product_catalog import implementation_contract, data_product_catalog_runtime_capabilities, data_product_catalog_runtime_smoke, data_product_catalog_build_schema_contract, data_product_catalog_build_service_contract, data_product_catalog_build_release_evidence, data_product_catalog_receive_event, data_product_catalog_ui_contract, data_product_catalog_verify_owned_table_boundary, data_product_catalog_configure_runtime, data_product_catalog_set_parameter, data_product_catalog_register_rule


def test_data_product_catalog_runtime_capabilities_and_smoke():
    runtime = data_product_catalog_runtime_capabilities()
    smoke = data_product_catalog_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'data_product_catalog'


def test_data_product_catalog_contracts_events_workbench_and_boundary():
    assert data_product_catalog_build_schema_contract()['ok'] is True
    assert data_product_catalog_build_service_contract()['ok'] is True
    assert data_product_catalog_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'data_product_catalog'
    assert data_product_catalog_receive_event(data_product_catalog_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.data_product_catalog.events'})['state'], {'event_type': ('SchemaPublished', 'PolicyChanged', 'SearchIndexRefreshed')[0], 'event_id': 'evt'})['ok'] is True
    assert data_product_catalog_ui_contract()['ok'] is True  # workbench ui_contract
    assert data_product_catalog_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert data_product_catalog_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.data_product_catalog.events'})['ok'] is True
    assert data_product_catalog_set_parameter(state, 'threshold', 1)['ok'] is True
    assert data_product_catalog_register_rule(state, {'rule_id':'r1'})['ok'] is True
