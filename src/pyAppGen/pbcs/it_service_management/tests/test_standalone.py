from pyAppGen.pbcs.it_service_management.controls import evaluate_control
from pyAppGen.pbcs.it_service_management.forms import form_catalog
from pyAppGen.pbcs.it_service_management.release_evidence import validate_release_evidence
from pyAppGen.pbcs.it_service_management.standalone import ItServiceManagementStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.it_service_management.ui import it_service_management_standalone_ui_contract
from pyAppGen.pbcs.it_service_management.wizards import wizard_catalog


def test_standalone_app_runs_full_itsm_operating_model():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    demo = smoke['demo']
    assert demo['major_incident']['incident']['major'] is True
    assert demo['duplicate_rollup']['child']['status'] == 'child_symptom'
    assert demo['stale_ci']['ok'] is False
    assert demo['blocked_access']['ok'] is False
    assert demo['blocked_change']['ok'] is False
    assert demo['problem']['problem']['status'] == 'investigating'
    assert demo['known_error']['article']['visibility'] == 'both'


def test_forms_wizards_controls_surface_full_domain():
    assert len(form_catalog()['forms']) >= 9
    assert len(wizard_catalog()['wizards']) >= 6
    assert it_service_management_standalone_ui_contract()['ok'] is True
    blocked = evaluate_control('backout_plan_control', {'validation_steps': ('smoke',)})
    assert blocked['ok'] is False
    assert 'approve_change' in blocked['blocked_actions']


def test_incident_sla_change_problem_edge_cases_are_executable():
    app = ItServiceManagementStandaloneApp()
    assert app.configure()['ok'] is True
    app.register_configuration_item('CI-1', relationships=(('provides', 'payroll'),), technical_owner='sre', service_owner='hr', support_group='ops', criticality='tier-1')
    opened = app.open_incident('INC-100', impact='enterprise', urgency='high', regulated=True)
    assert opened['priority']['priority'] == 'P1'
    bad_major = app.declare_major_incident('INC-100', '', ('payroll',), ('stable',))
    assert bad_major['ok'] is False
    paused = app.pause_sla_clock('SLA-INC-100', 'cab_review_pending', 'manager')
    assert paused['ok'] is True
    blocked_change = app.submit_change('CHG-100', 'normal', ('CI-1',), False, {'validation_steps': ('x',), 'success_criteria': 'ok', 'rollback_owner': 'ops', 'backout_triggers': ('fail',)}, approvals=2)
    assert blocked_change['ok'] is False


def test_agent_preview_stays_owned_and_confirmation_gated():
    app = ItServiceManagementStandaloneApp()
    preview = app.assistant_instruction_preview('incident memo', 'update workaround')
    assert preview['ok'] is True
    assert preview['crud_preview']['table'] == 'it_service_management_it_incident'
    assert preview['requires_confirmation'] is True
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['stream_engine_picker_visible'] is False
    assert all(table.startswith('it_service_management_') for table in contract['owned_tables'])


def test_release_evidence_includes_standalone_sections():
    evidence = validate_release_evidence()
    assert evidence['ok'] is True
    assert evidence['failed_checks'] == ()
