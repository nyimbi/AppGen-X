from pyAppGen.pbcs.professional_services_automation import implementation_contract, professional_services_automation_runtime_capabilities, professional_services_automation_runtime_smoke, professional_services_automation_build_schema_contract, professional_services_automation_build_service_contract, professional_services_automation_build_release_evidence, professional_services_automation_receive_event, professional_services_automation_ui_contract, professional_services_automation_verify_owned_table_boundary, professional_services_automation_configure_runtime, professional_services_automation_set_parameter, professional_services_automation_register_rule


def test_professional_services_automation_runtime_capabilities_and_smoke():
    runtime = professional_services_automation_runtime_capabilities()
    smoke = professional_services_automation_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'professional_services_automation'


def test_professional_services_automation_contracts_events_workbench_and_boundary():
    assert professional_services_automation_build_schema_contract()['ok'] is True
    assert professional_services_automation_build_service_contract()['ok'] is True
    assert professional_services_automation_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'professional_services_automation'
    assert professional_services_automation_receive_event(professional_services_automation_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.professional_services_automation.events'})['state'], {'event_type': ('ContractApproved', 'TimeSubmitted', 'InvoiceIssued')[0], 'event_id': 'evt'})['ok'] is True
    assert professional_services_automation_ui_contract()['ok'] is True  # workbench ui_contract
    assert professional_services_automation_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert professional_services_automation_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.professional_services_automation.events'})['ok'] is True
    assert professional_services_automation_set_parameter(state, 'threshold', 1)['ok'] is True
    assert professional_services_automation_register_rule(state, {'rule_id':'r1'})['ok'] is True
