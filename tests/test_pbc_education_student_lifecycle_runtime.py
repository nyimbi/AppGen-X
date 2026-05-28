from pyAppGen.pbcs.education_student_lifecycle import implementation_contract, education_student_lifecycle_runtime_capabilities, education_student_lifecycle_runtime_smoke, education_student_lifecycle_build_schema_contract, education_student_lifecycle_build_service_contract, education_student_lifecycle_build_release_evidence, education_student_lifecycle_receive_event, education_student_lifecycle_verify_owned_table_boundary, education_student_lifecycle_configure_runtime, education_student_lifecycle_set_parameter, education_student_lifecycle_register_rule, education_student_lifecycle_empty_state
from pyAppGen.pbcs.education_student_lifecycle.ui import education_student_lifecycle_ui_contract, education_student_lifecycle_render_workbench


def test_education_student_lifecycle_runtime_capabilities_and_contracts():
    runtime = education_student_lifecycle_runtime_capabilities()
    assert runtime['ok'] is True
    assert implementation_contract()['implementation_directory'] == 'src/pyAppGen/pbcs/education_student_lifecycle'
    assert education_student_lifecycle_build_schema_contract()['ok'] is True
    assert education_student_lifecycle_build_service_contract()['ok'] is True
    assert education_student_lifecycle_build_release_evidence()['ok'] is True
    assert education_student_lifecycle_runtime_smoke()['ok'] is True


def test_education_student_lifecycle_events_ui_boundary_and_configuration():
    state = education_student_lifecycle_empty_state()
    assert education_student_lifecycle_configure_runtime(state, {'database_backend': 'postgresql', 'event_topic': 'pbc.education_student_lifecycle.events'})['ok'] is True
    assert education_student_lifecycle_set_parameter(state, 'workbench_limit', 10)['ok'] is True
    assert education_student_lifecycle_register_rule(state, {'rule_id': 'smoke'})['ok'] is True
    assert education_student_lifecycle_receive_event(state, {'event_type': ('PolicyChanged', 'CustomerUpdated', 'SupplierQualified')[0], 'idempotency_key': 'evt'})['ok'] is True
    assert education_student_lifecycle_ui_contract()['ok'] is True
    assert education_student_lifecycle_render_workbench()['ok'] is True
    assert education_student_lifecycle_verify_owned_table_boundary((f'education_student_lifecycle_owned_table', 'foreign_table'))['ok'] is False
