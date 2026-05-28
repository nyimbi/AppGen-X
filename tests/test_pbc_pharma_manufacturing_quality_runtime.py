from pyAppGen.pbcs.pharma_manufacturing_quality import implementation_contract, pharma_manufacturing_quality_runtime_capabilities, pharma_manufacturing_quality_runtime_smoke, pharma_manufacturing_quality_build_schema_contract, pharma_manufacturing_quality_build_service_contract, pharma_manufacturing_quality_build_release_evidence, pharma_manufacturing_quality_receive_event, pharma_manufacturing_quality_verify_owned_table_boundary, pharma_manufacturing_quality_configure_runtime, pharma_manufacturing_quality_set_parameter, pharma_manufacturing_quality_register_rule, pharma_manufacturing_quality_empty_state
from pyAppGen.pbcs.pharma_manufacturing_quality.ui import pharma_manufacturing_quality_ui_contract, pharma_manufacturing_quality_render_workbench


def test_pharma_manufacturing_quality_runtime_capabilities_and_contracts():
    runtime = pharma_manufacturing_quality_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/pharma_manufacturing_quality'
    assert pharma_manufacturing_quality_build_schema_contract()['ok'] is True
    assert pharma_manufacturing_quality_build_service_contract()['ok'] is True
    assert pharma_manufacturing_quality_build_release_evidence()['ok'] is True
    assert pharma_manufacturing_quality_runtime_smoke()['ok'] is True


def test_pharma_manufacturing_quality_events_ui_boundary_and_configuration():
    state = pharma_manufacturing_quality_empty_state()
    assert pharma_manufacturing_quality_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.pharma_manufacturing_quality.events'})['ok'] is True
    assert pharma_manufacturing_quality_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert pharma_manufacturing_quality_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert pharma_manufacturing_quality_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert pharma_manufacturing_quality_ui_contract()['ok'] is True
    assert pharma_manufacturing_quality_render_workbench()['ok'] is True
    assert pharma_manufacturing_quality_verify_owned_table_boundary((f'pharma_manufacturing_quality_owned_table', 'foreign_table'))['ok'] is False
