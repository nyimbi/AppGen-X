from pyAppGen.pbcs.clinical_care_coordination import implementation_contract, clinical_care_coordination_runtime_capabilities, clinical_care_coordination_runtime_smoke, clinical_care_coordination_build_schema_contract, clinical_care_coordination_build_service_contract, clinical_care_coordination_build_release_evidence, clinical_care_coordination_receive_event, clinical_care_coordination_verify_owned_table_boundary, clinical_care_coordination_configure_runtime, clinical_care_coordination_set_parameter, clinical_care_coordination_register_rule, clinical_care_coordination_empty_state
from pyAppGen.pbcs.clinical_care_coordination.ui import clinical_care_coordination_ui_contract, clinical_care_coordination_render_workbench


def test_clinical_care_coordination_runtime_capabilities_and_contracts():
    runtime = clinical_care_coordination_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/clinical_care_coordination'
    assert clinical_care_coordination_build_schema_contract()['ok'] is True
    assert clinical_care_coordination_build_service_contract()['ok'] is True
    assert clinical_care_coordination_build_release_evidence()['ok'] is True
    assert clinical_care_coordination_runtime_smoke()['ok'] is True


def test_clinical_care_coordination_events_ui_boundary_and_configuration():
    state = clinical_care_coordination_empty_state()
    assert clinical_care_coordination_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.clinical_care_coordination.events'})['ok'] is True
    assert clinical_care_coordination_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert clinical_care_coordination_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert clinical_care_coordination_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert clinical_care_coordination_ui_contract()['ok'] is True
    assert clinical_care_coordination_render_workbench()['ok'] is True
    assert clinical_care_coordination_verify_owned_table_boundary((f'clinical_care_coordination_owned_table', 'foreign_table'))['ok'] is False
