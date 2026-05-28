from pyAppGen.pbcs.medical_device_lifecycle import implementation_contract, medical_device_lifecycle_runtime_capabilities, medical_device_lifecycle_runtime_smoke, medical_device_lifecycle_build_schema_contract, medical_device_lifecycle_build_service_contract, medical_device_lifecycle_build_release_evidence, medical_device_lifecycle_receive_event, medical_device_lifecycle_verify_owned_table_boundary, medical_device_lifecycle_configure_runtime, medical_device_lifecycle_set_parameter, medical_device_lifecycle_register_rule, medical_device_lifecycle_empty_state
from pyAppGen.pbcs.medical_device_lifecycle.ui import medical_device_lifecycle_ui_contract, medical_device_lifecycle_render_workbench


def test_medical_device_lifecycle_runtime_capabilities_and_contracts():
    runtime = medical_device_lifecycle_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/medical_device_lifecycle'
    assert medical_device_lifecycle_build_schema_contract()['ok'] is True
    assert medical_device_lifecycle_build_service_contract()['ok'] is True
    assert medical_device_lifecycle_build_release_evidence()['ok'] is True
    assert medical_device_lifecycle_runtime_smoke()['ok'] is True


def test_medical_device_lifecycle_events_ui_boundary_and_configuration():
    state = medical_device_lifecycle_empty_state()
    assert medical_device_lifecycle_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.medical_device_lifecycle.events'})['ok'] is True
    assert medical_device_lifecycle_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert medical_device_lifecycle_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert medical_device_lifecycle_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert medical_device_lifecycle_ui_contract()['ok'] is True
    assert medical_device_lifecycle_render_workbench()['ok'] is True
    assert medical_device_lifecycle_verify_owned_table_boundary((f'medical_device_lifecycle_owned_table', 'foreign_table'))['ok'] is False
