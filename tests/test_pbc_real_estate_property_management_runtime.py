from pyAppGen.pbcs.real_estate_property_management import implementation_contract, real_estate_property_management_runtime_capabilities, real_estate_property_management_runtime_smoke, real_estate_property_management_build_schema_contract, real_estate_property_management_build_service_contract, real_estate_property_management_build_release_evidence, real_estate_property_management_receive_event, real_estate_property_management_verify_owned_table_boundary, real_estate_property_management_configure_runtime, real_estate_property_management_set_parameter, real_estate_property_management_register_rule, real_estate_property_management_empty_state
from pyAppGen.pbcs.real_estate_property_management.ui import real_estate_property_management_ui_contract, real_estate_property_management_render_workbench


def test_real_estate_property_management_runtime_capabilities_and_contracts():
    runtime = real_estate_property_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/real_estate_property_management'
    assert real_estate_property_management_build_schema_contract()['ok'] is True
    assert real_estate_property_management_build_service_contract()['ok'] is True
    assert real_estate_property_management_build_release_evidence()['ok'] is True
    assert real_estate_property_management_runtime_smoke()['ok'] is True


def test_real_estate_property_management_events_ui_boundary_and_configuration():
    state = real_estate_property_management_empty_state()
    assert real_estate_property_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.real_estate_property_management.events'})['ok'] is True
    assert real_estate_property_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert real_estate_property_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert real_estate_property_management_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert real_estate_property_management_ui_contract()['ok'] is True
    assert real_estate_property_management_render_workbench()['ok'] is True
    assert real_estate_property_management_verify_owned_table_boundary((f'real_estate_property_management_owned_table', 'foreign_table'))['ok'] is False
