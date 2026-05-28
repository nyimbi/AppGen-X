from pyAppGen.pbcs.advertising_campaign_operations import implementation_contract, advertising_campaign_operations_runtime_capabilities, advertising_campaign_operations_runtime_smoke, advertising_campaign_operations_build_schema_contract, advertising_campaign_operations_build_service_contract, advertising_campaign_operations_build_release_evidence, advertising_campaign_operations_receive_event, advertising_campaign_operations_verify_owned_table_boundary, advertising_campaign_operations_configure_runtime, advertising_campaign_operations_set_parameter, advertising_campaign_operations_register_rule, advertising_campaign_operations_empty_state
from pyAppGen.pbcs.advertising_campaign_operations.ui import advertising_campaign_operations_ui_contract, advertising_campaign_operations_render_workbench


def test_advertising_campaign_operations_runtime_capabilities_and_contracts():
    runtime = advertising_campaign_operations_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/advertising_campaign_operations'
    assert advertising_campaign_operations_build_schema_contract()['ok'] is True
    assert advertising_campaign_operations_build_service_contract()['ok'] is True
    assert advertising_campaign_operations_build_release_evidence()['ok'] is True
    assert advertising_campaign_operations_runtime_smoke()['ok'] is True


def test_advertising_campaign_operations_events_ui_boundary_and_configuration():
    state = advertising_campaign_operations_empty_state()
    assert advertising_campaign_operations_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.advertising_campaign_operations.events'})['ok'] is True
    assert advertising_campaign_operations_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert advertising_campaign_operations_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert advertising_campaign_operations_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert advertising_campaign_operations_ui_contract()['ok'] is True
    assert advertising_campaign_operations_render_workbench()['ok'] is True
    assert advertising_campaign_operations_verify_owned_table_boundary((f'advertising_campaign_operations_owned_table', 'foreign_table'))['ok'] is False
