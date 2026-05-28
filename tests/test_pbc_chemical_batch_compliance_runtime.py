from pyAppGen.pbcs.chemical_batch_compliance import implementation_contract, chemical_batch_compliance_runtime_capabilities, chemical_batch_compliance_runtime_smoke, chemical_batch_compliance_build_schema_contract, chemical_batch_compliance_build_service_contract, chemical_batch_compliance_build_release_evidence, chemical_batch_compliance_receive_event, chemical_batch_compliance_verify_owned_table_boundary, chemical_batch_compliance_configure_runtime, chemical_batch_compliance_set_parameter, chemical_batch_compliance_register_rule, chemical_batch_compliance_empty_state
from pyAppGen.pbcs.chemical_batch_compliance.ui import chemical_batch_compliance_ui_contract, chemical_batch_compliance_render_workbench


def test_chemical_batch_compliance_runtime_capabilities_and_contracts():
    runtime = chemical_batch_compliance_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/chemical_batch_compliance'
    assert chemical_batch_compliance_build_schema_contract()['ok'] is True
    assert chemical_batch_compliance_build_service_contract()['ok'] is True
    assert chemical_batch_compliance_build_release_evidence()['ok'] is True
    assert chemical_batch_compliance_runtime_smoke()['ok'] is True


def test_chemical_batch_compliance_events_ui_boundary_and_configuration():
    state = chemical_batch_compliance_empty_state()
    assert chemical_batch_compliance_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.chemical_batch_compliance.events'})['ok'] is True
    assert chemical_batch_compliance_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert chemical_batch_compliance_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert chemical_batch_compliance_receive_event(state, {'event_type': ('PolicyChanged', 'AuditEventSealed', 'OperationalKpiChanged')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert chemical_batch_compliance_ui_contract()['ok'] is True
    assert chemical_batch_compliance_render_workbench()['ok'] is True
    assert chemical_batch_compliance_verify_owned_table_boundary((f'chemical_batch_compliance_owned_table', 'foreign_table'))['ok'] is False
