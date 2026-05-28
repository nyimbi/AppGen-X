from pyAppGen.pbcs.defense_readiness_logistics import implementation_contract, defense_readiness_logistics_runtime_capabilities, defense_readiness_logistics_runtime_smoke, defense_readiness_logistics_build_schema_contract, defense_readiness_logistics_build_service_contract, defense_readiness_logistics_build_release_evidence, defense_readiness_logistics_receive_event, defense_readiness_logistics_verify_owned_table_boundary, defense_readiness_logistics_configure_runtime, defense_readiness_logistics_set_parameter, defense_readiness_logistics_register_rule, defense_readiness_logistics_empty_state
from pyAppGen.pbcs.defense_readiness_logistics.ui import defense_readiness_logistics_ui_contract, defense_readiness_logistics_render_workbench


def test_defense_readiness_logistics_runtime_capabilities_and_contracts():
    runtime = defense_readiness_logistics_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/defense_readiness_logistics'
    assert defense_readiness_logistics_build_schema_contract()['ok'] is True
    assert defense_readiness_logistics_build_service_contract()['ok'] is True
    assert defense_readiness_logistics_build_release_evidence()['ok'] is True
    assert defense_readiness_logistics_runtime_smoke()['ok'] is True


def test_defense_readiness_logistics_events_ui_boundary_and_configuration():
    state = defense_readiness_logistics_empty_state()
    assert defense_readiness_logistics_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.defense_readiness_logistics.events'})['ok'] is True
    assert defense_readiness_logistics_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert defense_readiness_logistics_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert defense_readiness_logistics_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert defense_readiness_logistics_ui_contract()['ok'] is True
    assert defense_readiness_logistics_render_workbench()['ok'] is True
    assert defense_readiness_logistics_verify_owned_table_boundary((f'defense_readiness_logistics_owned_table', 'foreign_table'))['ok'] is False
