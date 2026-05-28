from pyAppGen.pbcs.public_sector_case_management import implementation_contract, public_sector_case_management_runtime_capabilities, public_sector_case_management_runtime_smoke, public_sector_case_management_build_schema_contract, public_sector_case_management_build_service_contract, public_sector_case_management_build_release_evidence, public_sector_case_management_receive_event, public_sector_case_management_verify_owned_table_boundary, public_sector_case_management_configure_runtime, public_sector_case_management_set_parameter, public_sector_case_management_register_rule, public_sector_case_management_empty_state
from pyAppGen.pbcs.public_sector_case_management.ui import public_sector_case_management_ui_contract, public_sector_case_management_render_workbench


def test_public_sector_case_management_runtime_capabilities_and_contracts():
    runtime = public_sector_case_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/public_sector_case_management'
    assert public_sector_case_management_build_schema_contract()['ok'] is True
    assert public_sector_case_management_build_service_contract()['ok'] is True
    assert public_sector_case_management_build_release_evidence()['ok'] is True
    assert public_sector_case_management_runtime_smoke()['ok'] is True


def test_public_sector_case_management_events_ui_boundary_and_configuration():
    state = public_sector_case_management_empty_state()
    assert public_sector_case_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.public_sector_case_management.events'})['ok'] is True
    assert public_sector_case_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert public_sector_case_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert public_sector_case_management_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert public_sector_case_management_ui_contract()['ok'] is True
    assert public_sector_case_management_render_workbench()['ok'] is True
    assert public_sector_case_management_verify_owned_table_boundary((f'public_sector_case_management_owned_table', 'foreign_table'))['ok'] is False
