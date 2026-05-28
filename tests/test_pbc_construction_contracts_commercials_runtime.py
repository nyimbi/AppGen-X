from pyAppGen.pbcs.construction_contracts_commercials import implementation_contract, construction_contracts_commercials_runtime_capabilities, construction_contracts_commercials_runtime_smoke, construction_contracts_commercials_build_schema_contract, construction_contracts_commercials_build_service_contract, construction_contracts_commercials_build_release_evidence, construction_contracts_commercials_receive_event, construction_contracts_commercials_verify_owned_table_boundary, construction_contracts_commercials_configure_runtime, construction_contracts_commercials_set_parameter, construction_contracts_commercials_register_rule, construction_contracts_commercials_empty_state
from pyAppGen.pbcs.construction_contracts_commercials.ui import construction_contracts_commercials_ui_contract, construction_contracts_commercials_render_workbench


def test_construction_contracts_commercials_runtime_capabilities_and_contracts():
    runtime = construction_contracts_commercials_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/construction_contracts_commercials'
    assert construction_contracts_commercials_build_schema_contract()['ok'] is True
    assert construction_contracts_commercials_build_service_contract()['ok'] is True
    assert construction_contracts_commercials_build_release_evidence()['ok'] is True
    assert construction_contracts_commercials_runtime_smoke()['ok'] is True


def test_construction_contracts_commercials_events_ui_boundary_and_configuration():
    state = construction_contracts_commercials_empty_state()
    assert construction_contracts_commercials_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.construction_contracts_commercials.events'})['ok'] is True
    assert construction_contracts_commercials_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert construction_contracts_commercials_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert construction_contracts_commercials_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert construction_contracts_commercials_ui_contract()['ok'] is True
    assert construction_contracts_commercials_render_workbench()['ok'] is True
    assert construction_contracts_commercials_verify_owned_table_boundary((f'construction_contracts_commercials_owned_table', 'foreign_table'))['ok'] is False
