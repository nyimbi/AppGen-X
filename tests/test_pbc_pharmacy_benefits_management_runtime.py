from pyAppGen.pbcs.pharmacy_benefits_management import implementation_contract, pharmacy_benefits_management_runtime_capabilities, pharmacy_benefits_management_runtime_smoke, pharmacy_benefits_management_build_schema_contract, pharmacy_benefits_management_build_service_contract, pharmacy_benefits_management_build_release_evidence, pharmacy_benefits_management_receive_event, pharmacy_benefits_management_verify_owned_table_boundary, pharmacy_benefits_management_configure_runtime, pharmacy_benefits_management_set_parameter, pharmacy_benefits_management_register_rule, pharmacy_benefits_management_empty_state
from pyAppGen.pbcs.pharmacy_benefits_management.ui import pharmacy_benefits_management_ui_contract, pharmacy_benefits_management_render_workbench


def test_pharmacy_benefits_management_runtime_capabilities_and_contracts():
    runtime = pharmacy_benefits_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/pharmacy_benefits_management'
    assert pharmacy_benefits_management_build_schema_contract()['ok'] is True
    assert pharmacy_benefits_management_build_service_contract()['ok'] is True
    assert pharmacy_benefits_management_build_release_evidence()['ok'] is True
    assert pharmacy_benefits_management_runtime_smoke()['ok'] is True


def test_pharmacy_benefits_management_events_ui_boundary_and_configuration():
    state = pharmacy_benefits_management_empty_state()
    assert pharmacy_benefits_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.pharmacy_benefits_management.events'})['ok'] is True
    assert pharmacy_benefits_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert pharmacy_benefits_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert pharmacy_benefits_management_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert pharmacy_benefits_management_ui_contract()['ok'] is True
    assert pharmacy_benefits_management_render_workbench()['ok'] is True
    assert pharmacy_benefits_management_verify_owned_table_boundary((f'pharmacy_benefits_management_owned_table', 'foreign_table'))['ok'] is False
