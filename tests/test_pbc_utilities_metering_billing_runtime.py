from pyAppGen.pbcs.utilities_metering_billing import implementation_contract, utilities_metering_billing_runtime_capabilities, utilities_metering_billing_runtime_smoke, utilities_metering_billing_build_schema_contract, utilities_metering_billing_build_service_contract, utilities_metering_billing_build_release_evidence, utilities_metering_billing_receive_event, utilities_metering_billing_verify_owned_table_boundary, utilities_metering_billing_configure_runtime, utilities_metering_billing_set_parameter, utilities_metering_billing_register_rule, utilities_metering_billing_empty_state
from pyAppGen.pbcs.utilities_metering_billing.ui import utilities_metering_billing_ui_contract, utilities_metering_billing_render_workbench


def test_utilities_metering_billing_runtime_capabilities_and_contracts():
    runtime = utilities_metering_billing_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/utilities_metering_billing'
    assert utilities_metering_billing_build_schema_contract()['ok'] is True
    assert utilities_metering_billing_build_service_contract()['ok'] is True
    assert utilities_metering_billing_build_release_evidence()['ok'] is True
    assert utilities_metering_billing_runtime_smoke()['ok'] is True


def test_utilities_metering_billing_events_ui_boundary_and_configuration():
    state = utilities_metering_billing_empty_state()
    assert utilities_metering_billing_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.utilities_metering_billing.events'})['ok'] is True
    assert utilities_metering_billing_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert utilities_metering_billing_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert utilities_metering_billing_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert utilities_metering_billing_ui_contract()['ok'] is True
    assert utilities_metering_billing_render_workbench()['ok'] is True
    assert utilities_metering_billing_verify_owned_table_boundary((f'utilities_metering_billing_owned_table', 'foreign_table'))['ok'] is False
