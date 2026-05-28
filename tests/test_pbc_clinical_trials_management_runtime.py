from pyAppGen.pbcs.clinical_trials_management import implementation_contract, clinical_trials_management_runtime_capabilities, clinical_trials_management_runtime_smoke, clinical_trials_management_build_schema_contract, clinical_trials_management_build_service_contract, clinical_trials_management_build_release_evidence, clinical_trials_management_receive_event, clinical_trials_management_verify_owned_table_boundary, clinical_trials_management_configure_runtime, clinical_trials_management_set_parameter, clinical_trials_management_register_rule, clinical_trials_management_empty_state
from pyAppGen.pbcs.clinical_trials_management.ui import clinical_trials_management_ui_contract, clinical_trials_management_render_workbench


def test_clinical_trials_management_runtime_capabilities_and_contracts():
    runtime = clinical_trials_management_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/clinical_trials_management'
    assert clinical_trials_management_build_schema_contract()['ok'] is True
    assert clinical_trials_management_build_service_contract()['ok'] is True
    assert clinical_trials_management_build_release_evidence()['ok'] is True
    assert clinical_trials_management_runtime_smoke()['ok'] is True


def test_clinical_trials_management_events_ui_boundary_and_configuration():
    state = clinical_trials_management_empty_state()
    assert clinical_trials_management_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.clinical_trials_management.events'})['ok'] is True
    assert clinical_trials_management_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert clinical_trials_management_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert clinical_trials_management_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert clinical_trials_management_ui_contract()['ok'] is True
    assert clinical_trials_management_render_workbench()['ok'] is True
    assert clinical_trials_management_verify_owned_table_boundary((f'clinical_trials_management_owned_table', 'foreign_table'))['ok'] is False
