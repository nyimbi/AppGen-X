from pyAppGen.pbcs.vendor_supplier_360 import implementation_contract, vendor_supplier_360_runtime_capabilities, vendor_supplier_360_runtime_smoke, vendor_supplier_360_build_schema_contract, vendor_supplier_360_build_service_contract, vendor_supplier_360_build_release_evidence, vendor_supplier_360_receive_event, vendor_supplier_360_ui_contract, vendor_supplier_360_verify_owned_table_boundary, vendor_supplier_360_configure_runtime, vendor_supplier_360_set_parameter, vendor_supplier_360_register_rule


def test_vendor_supplier_360_runtime_capabilities_and_smoke():
    runtime = vendor_supplier_360_runtime_capabilities()
    smoke = vendor_supplier_360_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'vendor_supplier_360'


def test_vendor_supplier_360_contracts_events_workbench_and_boundary():
    assert vendor_supplier_360_build_schema_contract()['ok'] is True
    assert vendor_supplier_360_build_service_contract()['ok'] is True
    assert vendor_supplier_360_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'vendor_supplier_360'
    assert vendor_supplier_360_receive_event(vendor_supplier_360_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.vendor_supplier_360.events'})['state'], {'event_type': ('PurchaseOrderCreated', 'PaymentRejected', 'CompliancePolicyChanged')[0], 'event_id': 'evt'})['ok'] is True
    assert vendor_supplier_360_ui_contract()['ok'] is True  # workbench ui_contract
    assert vendor_supplier_360_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert vendor_supplier_360_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.vendor_supplier_360.events'})['ok'] is True
    assert vendor_supplier_360_set_parameter(state, 'threshold', 1)['ok'] is True
    assert vendor_supplier_360_register_rule(state, {'rule_id':'r1'})['ok'] is True
