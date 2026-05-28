from pyAppGen.pbcs.hotel_revenue_management import implementation_contract, hotel_revenue_management_runtime_capabilities, hotel_revenue_management_runtime_smoke, hotel_revenue_management_build_schema_contract, hotel_revenue_management_build_service_contract, hotel_revenue_management_build_release_evidence, hotel_revenue_management_receive_event, hotel_revenue_management_verify_owned_table_boundary, hotel_revenue_management_configure_runtime, hotel_revenue_management_set_parameter, hotel_revenue_management_register_rule, hotel_revenue_management_empty_state
from pyAppGen.pbcs.hotel_revenue_management.ui import hotel_revenue_management_ui_contract, hotel_revenue_management_render_workbench


def test_hotel_revenue_management_runtime_capabilities_and_contracts():
    runtime = hotel_revenue_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/hotel_revenue_management'
    assert hotel_revenue_management_build_schema_contract()['ok'] is True
    assert hotel_revenue_management_build_service_contract()['ok'] is True
    assert hotel_revenue_management_build_release_evidence()['ok'] is True
    assert hotel_revenue_management_runtime_smoke()['ok'] is True


def test_hotel_revenue_management_events_ui_boundary_and_configuration():
    state = hotel_revenue_management_empty_state()
    assert hotel_revenue_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.hotel_revenue_management.events'})['ok'] is True
    assert hotel_revenue_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert hotel_revenue_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert hotel_revenue_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert hotel_revenue_management_ui_contract()['ok'] is True
    assert hotel_revenue_management_render_workbench()['ok'] is True
    assert hotel_revenue_management_verify_owned_table_boundary((f'hotel_revenue_management_owned_table', 'foreign_table'))['ok'] is False
