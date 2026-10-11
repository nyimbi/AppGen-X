from pyAppGen.pbcs.case_knowledge_management import implementation_contract, case_knowledge_management_runtime_capabilities, case_knowledge_management_runtime_smoke, case_knowledge_management_build_schema_contract, case_knowledge_management_build_service_contract, case_knowledge_management_build_release_evidence, case_knowledge_management_receive_event, case_knowledge_management_ui_contract, case_knowledge_management_verify_owned_table_boundary, case_knowledge_management_configure_runtime, case_knowledge_management_set_parameter, case_knowledge_management_register_rule
from pyAppGen.pbcs.case_knowledge_management.config import DOMAIN_PARAMETER_SCHEMA, DOMAIN_RULE_SCHEMA


def test_case_knowledge_management_runtime_capabilities_and_smoke():
    runtime = case_knowledge_management_runtime_capabilities()
    smoke = case_knowledge_management_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'case_knowledge_management'


def test_case_knowledge_management_contracts_events_workbench_and_boundary():
    assert case_knowledge_management_build_schema_contract()['ok'] is True
    assert case_knowledge_management_build_service_contract()['ok'] is True
    assert case_knowledge_management_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'case_knowledge_management'
    assert case_knowledge_management_receive_event(case_knowledge_management_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.case_knowledge_management.events'})['state'], {'event_type': ('ServiceTicketOpened', 'CustomerUpdated', 'SearchIndexRefreshed')[0], 'event_id': 'evt'})['ok'] is True
    assert case_knowledge_management_ui_contract()['ok'] is True  # workbench ui_contract
    assert case_knowledge_management_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert case_knowledge_management_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.case_knowledge_management.events'})['ok'] is True
    assert case_knowledge_management_set_parameter(state, DOMAIN_PARAMETER_SCHEMA[0]['key'], DOMAIN_PARAMETER_SCHEMA[0]['default'])['ok'] is True
    assert case_knowledge_management_register_rule(state, dict(DOMAIN_RULE_SCHEMA[0]))['ok'] is True
