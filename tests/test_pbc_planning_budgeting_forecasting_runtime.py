from pyAppGen.pbcs.planning_budgeting_forecasting import implementation_contract, planning_budgeting_forecasting_runtime_capabilities, planning_budgeting_forecasting_runtime_smoke, planning_budgeting_forecasting_build_schema_contract, planning_budgeting_forecasting_build_service_contract, planning_budgeting_forecasting_build_release_evidence, planning_budgeting_forecasting_receive_event, planning_budgeting_forecasting_ui_contract, planning_budgeting_forecasting_verify_owned_table_boundary, planning_budgeting_forecasting_configure_runtime, planning_budgeting_forecasting_set_parameter, planning_budgeting_forecasting_register_rule


def test_planning_budgeting_forecasting_runtime_capabilities_and_smoke():
    runtime = planning_budgeting_forecasting_runtime_capabilities()
    smoke = planning_budgeting_forecasting_runtime_smoke()
    assert runtime['ok'] is True
    assert smoke['ok'] is True
    assert runtime['pbc'] == 'planning_budgeting_forecasting'


def test_planning_budgeting_forecasting_contracts_events_workbench_and_boundary():
    assert planning_budgeting_forecasting_build_schema_contract()['ok'] is True
    assert planning_budgeting_forecasting_build_service_contract()['ok'] is True
    assert planning_budgeting_forecasting_build_release_evidence()['ok'] is True
    assert implementation_contract()['pbc'] == 'planning_budgeting_forecasting'
    assert planning_budgeting_forecasting_receive_event(planning_budgeting_forecasting_configure_runtime({'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}, {'database_backend':'postgresql','event_topic':'pbc.planning_budgeting_forecasting.events'})['state'], {'event_type': ('TrialBalanceCalculated', 'RevenueRecognized', 'DemandForecastPublished')[0], 'event_id': 'evt'})['ok'] is True
    assert planning_budgeting_forecasting_ui_contract()['ok'] is True  # workbench ui_contract
    assert planning_budgeting_forecasting_verify_owned_table_boundary(('foreign_table',))['ok'] is False  # foreign boundary
    state = {'records': {}, 'parameters': {}, 'rules': {}, 'schema_extensions': {}, 'configuration': {}, 'inbox': [], 'outbox': [], 'dead_letter': [], 'idempotency_keys': set()}
    assert planning_budgeting_forecasting_configure_runtime(state, {'database_backend':'postgresql','event_topic':'pbc.planning_budgeting_forecasting.events'})['ok'] is True
    assert planning_budgeting_forecasting_set_parameter(state, 'threshold', 1)['ok'] is True
    assert planning_budgeting_forecasting_register_rule(state, {'rule_id':'r1'})['ok'] is True
