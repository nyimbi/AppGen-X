from pyAppGen.pbcs.hospitality_property_operations import implementation_contract, hospitality_property_operations_runtime_capabilities, hospitality_property_operations_runtime_smoke, hospitality_property_operations_build_schema_contract, hospitality_property_operations_build_service_contract, hospitality_property_operations_build_release_evidence, hospitality_property_operations_receive_event, hospitality_property_operations_verify_owned_table_boundary, hospitality_property_operations_configure_runtime, hospitality_property_operations_set_parameter, hospitality_property_operations_register_rule, hospitality_property_operations_empty_state
from pyAppGen.pbcs.hospitality_property_operations.ui import hospitality_property_operations_ui_contract, hospitality_property_operations_render_workbench


def test_hospitality_property_operations_runtime_capabilities_and_contracts():
    runtime = hospitality_property_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/hospitality_property_operations'
    assert hospitality_property_operations_build_schema_contract()['ok'] is True
    assert hospitality_property_operations_build_service_contract()['ok'] is True
    assert hospitality_property_operations_build_release_evidence()['ok'] is True
    assert hospitality_property_operations_runtime_smoke()['ok'] is True


def test_hospitality_property_operations_events_ui_boundary_and_configuration():
    state = hospitality_property_operations_empty_state()
    assert hospitality_property_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.hospitality_property_operations.events'})['ok'] is True
    assert hospitality_property_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert hospitality_property_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert hospitality_property_operations_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert hospitality_property_operations_ui_contract()['ok'] is True
    assert hospitality_property_operations_render_workbench()['ok'] is True
    assert hospitality_property_operations_verify_owned_table_boundary((f'hospitality_property_operations_owned_table', 'foreign_table'))['ok'] is False
