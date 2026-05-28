from pyAppGen.pbcs.telecom_subscription_lifecycle import implementation_contract, telecom_subscription_lifecycle_runtime_capabilities, telecom_subscription_lifecycle_runtime_smoke, telecom_subscription_lifecycle_build_schema_contract, telecom_subscription_lifecycle_build_service_contract, telecom_subscription_lifecycle_build_release_evidence, telecom_subscription_lifecycle_receive_event, telecom_subscription_lifecycle_verify_owned_table_boundary, telecom_subscription_lifecycle_configure_runtime, telecom_subscription_lifecycle_set_parameter, telecom_subscription_lifecycle_register_rule, telecom_subscription_lifecycle_empty_state
from pyAppGen.pbcs.telecom_subscription_lifecycle.ui import telecom_subscription_lifecycle_ui_contract, telecom_subscription_lifecycle_render_workbench


def test_telecom_subscription_lifecycle_runtime_capabilities_and_contracts():
    runtime = telecom_subscription_lifecycle_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/telecom_subscription_lifecycle'
    assert telecom_subscription_lifecycle_build_schema_contract()['ok'] is True
    assert telecom_subscription_lifecycle_build_service_contract()['ok'] is True
    assert telecom_subscription_lifecycle_build_release_evidence()['ok'] is True
    assert telecom_subscription_lifecycle_runtime_smoke()['ok'] is True


def test_telecom_subscription_lifecycle_events_ui_boundary_and_configuration():
    state = telecom_subscription_lifecycle_empty_state()
    assert telecom_subscription_lifecycle_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.telecom_subscription_lifecycle.events'})['ok'] is True
    assert telecom_subscription_lifecycle_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert telecom_subscription_lifecycle_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert telecom_subscription_lifecycle_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert telecom_subscription_lifecycle_ui_contract()['ok'] is True
    assert telecom_subscription_lifecycle_render_workbench()['ok'] is True
    assert telecom_subscription_lifecycle_verify_owned_table_boundary((f'telecom_subscription_lifecycle_owned_table', 'foreign_table'))['ok'] is False
