from pyAppGen.pbcs.food_safety_quality_compliance import implementation_contract, food_safety_quality_compliance_runtime_capabilities, food_safety_quality_compliance_runtime_smoke, food_safety_quality_compliance_build_schema_contract, food_safety_quality_compliance_build_service_contract, food_safety_quality_compliance_build_release_evidence, food_safety_quality_compliance_receive_event, food_safety_quality_compliance_verify_owned_table_boundary, food_safety_quality_compliance_configure_runtime, food_safety_quality_compliance_set_parameter, food_safety_quality_compliance_register_rule, food_safety_quality_compliance_empty_state
from pyAppGen.pbcs.food_safety_quality_compliance.ui import food_safety_quality_compliance_ui_contract, food_safety_quality_compliance_render_workbench


def test_food_safety_quality_compliance_runtime_capabilities_and_contracts():
    runtime = food_safety_quality_compliance_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/food_safety_quality_compliance'
    assert food_safety_quality_compliance_build_schema_contract()['ok'] is True
    assert food_safety_quality_compliance_build_service_contract()['ok'] is True
    assert food_safety_quality_compliance_build_release_evidence()['ok'] is True
    assert food_safety_quality_compliance_runtime_smoke()['ok'] is True


def test_food_safety_quality_compliance_events_ui_boundary_and_configuration():
    state = food_safety_quality_compliance_empty_state()
    assert food_safety_quality_compliance_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.food_safety_quality_compliance.events'})['ok'] is True
    assert food_safety_quality_compliance_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert food_safety_quality_compliance_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert food_safety_quality_compliance_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert food_safety_quality_compliance_ui_contract()['ok'] is True
    assert food_safety_quality_compliance_render_workbench()['ok'] is True
    assert food_safety_quality_compliance_verify_owned_table_boundary((f'food_safety_quality_compliance_owned_table', 'foreign_table'))['ok'] is False
