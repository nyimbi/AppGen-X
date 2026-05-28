from pyAppGen.pbcs.capital_projects_delivery import implementation_contract, capital_projects_delivery_runtime_capabilities, capital_projects_delivery_runtime_smoke, capital_projects_delivery_build_schema_contract, capital_projects_delivery_build_service_contract, capital_projects_delivery_build_release_evidence, capital_projects_delivery_receive_event, capital_projects_delivery_verify_owned_table_boundary, capital_projects_delivery_configure_runtime, capital_projects_delivery_set_parameter, capital_projects_delivery_register_rule, capital_projects_delivery_empty_state
from pyAppGen.pbcs.capital_projects_delivery.ui import capital_projects_delivery_ui_contract, capital_projects_delivery_render_workbench


def test_capital_projects_delivery_runtime_capabilities_and_contracts():
    runtime = capital_projects_delivery_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/capital_projects_delivery'
    assert capital_projects_delivery_build_schema_contract()['ok'] is True
    assert capital_projects_delivery_build_service_contract()['ok'] is True
    assert capital_projects_delivery_build_release_evidence()['ok'] is True
    assert capital_projects_delivery_runtime_smoke()['ok'] is True


def test_capital_projects_delivery_events_ui_boundary_and_configuration():
    state = capital_projects_delivery_empty_state()
    assert capital_projects_delivery_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.capital_projects_delivery.events'})['ok'] is True
    assert capital_projects_delivery_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert capital_projects_delivery_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert capital_projects_delivery_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert capital_projects_delivery_ui_contract()['ok'] is True
    assert capital_projects_delivery_render_workbench()['ok'] is True
    assert capital_projects_delivery_verify_owned_table_boundary((f'capital_projects_delivery_owned_table', 'foreign_table'))['ok'] is False
