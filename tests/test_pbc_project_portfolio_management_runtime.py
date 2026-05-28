from pyAppGen.pbcs.project_portfolio_management import implementation_contract, project_portfolio_management_runtime_capabilities, project_portfolio_management_runtime_smoke, project_portfolio_management_build_schema_contract, project_portfolio_management_build_service_contract, project_portfolio_management_build_release_evidence, project_portfolio_management_receive_event, project_portfolio_management_ui_contract, project_portfolio_management_verify_owned_table_boundary, project_portfolio_management_configure_runtime, project_portfolio_management_set_parameter, project_portfolio_management_register_rule


def test_project_portfolio_management_runtime_capabilities_and_smoke():
    runtime = project_portfolio_management_runtime_capabilities()
    smoke = project_portfolio_management_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'project_portfolio_management'


def test_project_portfolio_management_contracts_events_workbench_and_boundary():
    assert project_portfolio_management_build_schema_contract()['ok'] is True
    assert project_portfolio_management_build_service_contract()['ok'] is True
    assert project_portfolio_management_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'project_portfolio_management'
    assert project_portfolio_management_receive_event(project_portfolio_management_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.project_portfolio_management.events'})['state'], {'event_type': ('BudgetApproved', 'EmployeeProvisioned', 'ProcurementApproved')[0], 'event_id': 'evt'})['ok'] is True
    assert project_portfolio_management_ui_contract()['ok'] is True  # workbench ui_contract
    assert project_portfolio_management_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert project_portfolio_management_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.project_portfolio_management.events'})['ok'] is True
    assert project_portfolio_management_set_parameter(state, 'threshold', 1)['ok'] is True
    assert project_portfolio_management_register_rule(state, {'rule_id':'r1'})['ok'] is True
