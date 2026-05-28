from pyAppGen.pbcs.agri_supply_chain_traceability import implementation_contract, agri_supply_chain_traceability_runtime_capabilities, agri_supply_chain_traceability_runtime_smoke, agri_supply_chain_traceability_build_schema_contract, agri_supply_chain_traceability_build_service_contract, agri_supply_chain_traceability_build_release_evidence, agri_supply_chain_traceability_receive_event, agri_supply_chain_traceability_verify_owned_table_boundary, agri_supply_chain_traceability_configure_runtime, agri_supply_chain_traceability_set_parameter, agri_supply_chain_traceability_register_rule, agri_supply_chain_traceability_empty_state
from pyAppGen.pbcs.agri_supply_chain_traceability.ui import agri_supply_chain_traceability_ui_contract, agri_supply_chain_traceability_render_workbench


def test_agri_supply_chain_traceability_runtime_capabilities_and_contracts():
    runtime = agri_supply_chain_traceability_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/agri_supply_chain_traceability'
    assert agri_supply_chain_traceability_build_schema_contract()['ok'] is True
    assert agri_supply_chain_traceability_build_service_contract()['ok'] is True
    assert agri_supply_chain_traceability_build_release_evidence()['ok'] is True
    assert agri_supply_chain_traceability_runtime_smoke()['ok'] is True


def test_agri_supply_chain_traceability_events_ui_boundary_and_configuration():
    state = agri_supply_chain_traceability_empty_state()
    assert agri_supply_chain_traceability_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.agri_supply_chain_traceability.events'})['ok'] is True
    assert agri_supply_chain_traceability_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert agri_supply_chain_traceability_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert agri_supply_chain_traceability_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert agri_supply_chain_traceability_ui_contract()['ok'] is True
    assert agri_supply_chain_traceability_render_workbench()['ok'] is True
    assert agri_supply_chain_traceability_verify_owned_table_boundary((f'agri_supply_chain_traceability_owned_table', 'foreign_table'))['ok'] is False
