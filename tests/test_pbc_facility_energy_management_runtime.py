from pyAppGen.pbcs.facility_energy_management import implementation_contract, facility_energy_management_runtime_capabilities, facility_energy_management_runtime_smoke, facility_energy_management_build_schema_contract, facility_energy_management_build_service_contract, facility_energy_management_build_release_evidence, facility_energy_management_receive_event, facility_energy_management_verify_owned_table_boundary, facility_energy_management_configure_runtime, facility_energy_management_set_parameter, facility_energy_management_register_rule, facility_energy_management_empty_state
from pyAppGen.pbcs.facility_energy_management.ui import facility_energy_management_ui_contract, facility_energy_management_render_workbench


def test_facility_energy_management_runtime_capabilities_and_contracts():
    runtime = facility_energy_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/facility_energy_management'
    assert facility_energy_management_build_schema_contract()['ok'] is True
    assert facility_energy_management_build_service_contract()['ok'] is True
    assert facility_energy_management_build_release_evidence()['ok'] is True
    assert facility_energy_management_runtime_smoke()['ok'] is True


def test_facility_energy_management_events_ui_boundary_and_configuration():
    state = facility_energy_management_empty_state()
    assert facility_energy_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.facility_energy_management.events'})['ok'] is True
    assert facility_energy_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert facility_energy_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert facility_energy_management_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert facility_energy_management_ui_contract()['ok'] is True
    assert facility_energy_management_render_workbench()['ok'] is True
    assert facility_energy_management_verify_owned_table_boundary((f'facility_energy_management_owned_table', 'foreign_table'))['ok'] is False
