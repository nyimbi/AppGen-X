from pyAppGen.pbcs.permitting_licensing_inspections import implementation_contract, permitting_licensing_inspections_runtime_capabilities, permitting_licensing_inspections_runtime_smoke, permitting_licensing_inspections_build_schema_contract, permitting_licensing_inspections_build_service_contract, permitting_licensing_inspections_build_release_evidence, permitting_licensing_inspections_receive_event, permitting_licensing_inspections_verify_owned_table_boundary, permitting_licensing_inspections_configure_runtime, permitting_licensing_inspections_set_parameter, permitting_licensing_inspections_register_rule, permitting_licensing_inspections_empty_state
from pyAppGen.pbcs.permitting_licensing_inspections.ui import permitting_licensing_inspections_ui_contract, permitting_licensing_inspections_render_workbench


def test_permitting_licensing_inspections_runtime_capabilities_and_contracts():
    runtime = permitting_licensing_inspections_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/permitting_licensing_inspections'
    assert permitting_licensing_inspections_build_schema_contract()['ok'] is True
    assert permitting_licensing_inspections_build_service_contract()['ok'] is True
    assert permitting_licensing_inspections_build_release_evidence()['ok'] is True
    assert permitting_licensing_inspections_runtime_smoke()['ok'] is True


def test_permitting_licensing_inspections_events_ui_boundary_and_configuration():
    state = permitting_licensing_inspections_empty_state()
    assert permitting_licensing_inspections_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.permitting_licensing_inspections.events'})['ok'] is True
    assert permitting_licensing_inspections_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert permitting_licensing_inspections_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert permitting_licensing_inspections_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert permitting_licensing_inspections_ui_contract()['ok'] is True
    assert permitting_licensing_inspections_render_workbench()['ok'] is True
    assert permitting_licensing_inspections_verify_owned_table_boundary((f'permitting_licensing_inspections_owned_table', 'foreign_table'))['ok'] is False
