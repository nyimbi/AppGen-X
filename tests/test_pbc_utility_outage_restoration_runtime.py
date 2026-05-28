from pyAppGen.pbcs.utility_outage_restoration import implementation_contract, utility_outage_restoration_runtime_capabilities, utility_outage_restoration_runtime_smoke, utility_outage_restoration_build_schema_contract, utility_outage_restoration_build_service_contract, utility_outage_restoration_build_release_evidence, utility_outage_restoration_receive_event, utility_outage_restoration_verify_owned_table_boundary, utility_outage_restoration_configure_runtime, utility_outage_restoration_set_parameter, utility_outage_restoration_register_rule, utility_outage_restoration_empty_state
from pyAppGen.pbcs.utility_outage_restoration.ui import utility_outage_restoration_ui_contract, utility_outage_restoration_render_workbench


def test_utility_outage_restoration_runtime_capabilities_and_contracts():
    runtime = utility_outage_restoration_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/utility_outage_restoration'
    assert utility_outage_restoration_build_schema_contract()['ok'] is True
    assert utility_outage_restoration_build_service_contract()['ok'] is True
    assert utility_outage_restoration_build_release_evidence()['ok'] is True
    assert utility_outage_restoration_runtime_smoke()['ok'] is True


def test_utility_outage_restoration_events_ui_boundary_and_configuration():
    state = utility_outage_restoration_empty_state()
    assert utility_outage_restoration_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.utility_outage_restoration.events'})['ok'] is True
    assert utility_outage_restoration_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert utility_outage_restoration_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert utility_outage_restoration_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert utility_outage_restoration_ui_contract()['ok'] is True
    assert utility_outage_restoration_render_workbench()['ok'] is True
    assert utility_outage_restoration_verify_owned_table_boundary((f'utility_outage_restoration_owned_table', 'foreign_table'))['ok'] is False
