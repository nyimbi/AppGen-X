from pyAppGen.pbcs.electronic_health_records_core import implementation_contract, electronic_health_records_core_runtime_capabilities, electronic_health_records_core_runtime_smoke, electronic_health_records_core_build_schema_contract, electronic_health_records_core_build_service_contract, electronic_health_records_core_build_release_evidence, electronic_health_records_core_receive_event, electronic_health_records_core_verify_owned_table_boundary, electronic_health_records_core_configure_runtime, electronic_health_records_core_set_parameter, electronic_health_records_core_register_rule, electronic_health_records_core_empty_state
from pyAppGen.pbcs.electronic_health_records_core.ui import electronic_health_records_core_ui_contract, electronic_health_records_core_render_workbench


def test_electronic_health_records_core_runtime_capabilities_and_contracts():
    runtime = electronic_health_records_core_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/electronic_health_records_core'
    assert electronic_health_records_core_build_schema_contract()['ok'] is True
    assert electronic_health_records_core_build_service_contract()['ok'] is True
    assert electronic_health_records_core_build_release_evidence()['ok'] is True
    assert electronic_health_records_core_runtime_smoke()['ok'] is True


def test_electronic_health_records_core_events_ui_boundary_and_configuration():
    state = electronic_health_records_core_empty_state()
    assert electronic_health_records_core_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.electronic_health_records_core.events'})['ok'] is True
    assert electronic_health_records_core_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert electronic_health_records_core_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert electronic_health_records_core_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert electronic_health_records_core_ui_contract()['ok'] is True
    assert electronic_health_records_core_render_workbench()['ok'] is True
    assert electronic_health_records_core_verify_owned_table_boundary((f'electronic_health_records_core_owned_table', 'foreign_table'))['ok'] is False
