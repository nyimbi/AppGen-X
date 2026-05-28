from pyAppGen.pbcs.environment_health_safety import implementation_contract, environment_health_safety_runtime_capabilities, environment_health_safety_runtime_smoke, environment_health_safety_build_schema_contract, environment_health_safety_build_service_contract, environment_health_safety_build_release_evidence, environment_health_safety_receive_event, environment_health_safety_verify_owned_table_boundary, environment_health_safety_configure_runtime, environment_health_safety_set_parameter, environment_health_safety_register_rule, environment_health_safety_empty_state
from pyAppGen.pbcs.environment_health_safety.ui import environment_health_safety_ui_contract, environment_health_safety_render_workbench


def test_environment_health_safety_runtime_capabilities_and_contracts():
    runtime = environment_health_safety_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/environment_health_safety'
    assert environment_health_safety_build_schema_contract()['ok'] is True
    assert environment_health_safety_build_service_contract()['ok'] is True
    assert environment_health_safety_build_release_evidence()['ok'] is True
    assert environment_health_safety_runtime_smoke()['ok'] is True


def test_environment_health_safety_events_ui_boundary_and_configuration():
    state = environment_health_safety_empty_state()
    assert environment_health_safety_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.environment_health_safety.events'})['ok'] is True
    assert environment_health_safety_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert environment_health_safety_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert environment_health_safety_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert environment_health_safety_ui_contract()['ok'] is True
    assert environment_health_safety_render_workbench()['ok'] is True
    assert environment_health_safety_verify_owned_table_boundary((f'environment_health_safety_owned_table', 'foreign_table'))['ok'] is False
