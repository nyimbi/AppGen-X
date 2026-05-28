from pyAppGen.pbcs.nonprofit_program_impact import implementation_contract, nonprofit_program_impact_runtime_capabilities, nonprofit_program_impact_runtime_smoke, nonprofit_program_impact_build_schema_contract, nonprofit_program_impact_build_service_contract, nonprofit_program_impact_build_release_evidence, nonprofit_program_impact_receive_event, nonprofit_program_impact_verify_owned_table_boundary, nonprofit_program_impact_configure_runtime, nonprofit_program_impact_set_parameter, nonprofit_program_impact_register_rule, nonprofit_program_impact_empty_state
from pyAppGen.pbcs.nonprofit_program_impact.ui import nonprofit_program_impact_ui_contract, nonprofit_program_impact_render_workbench


def test_nonprofit_program_impact_runtime_capabilities_and_contracts():
    runtime = nonprofit_program_impact_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/nonprofit_program_impact'
    assert nonprofit_program_impact_build_schema_contract()['ok'] is True
    assert nonprofit_program_impact_build_service_contract()['ok'] is True
    assert nonprofit_program_impact_build_release_evidence()['ok'] is True
    assert nonprofit_program_impact_runtime_smoke()['ok'] is True


def test_nonprofit_program_impact_events_ui_boundary_and_configuration():
    state = nonprofit_program_impact_empty_state()
    assert nonprofit_program_impact_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.nonprofit_program_impact.events'})['ok'] is True
    assert nonprofit_program_impact_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert nonprofit_program_impact_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert nonprofit_program_impact_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert nonprofit_program_impact_ui_contract()['ok'] is True
    assert nonprofit_program_impact_render_workbench()['ok'] is True
    assert nonprofit_program_impact_verify_owned_table_boundary((f'nonprofit_program_impact_owned_table', 'foreign_table'))['ok'] is False
