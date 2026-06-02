from pyAppGen.pbcs.legal_matter_management.controls import evaluate_control
from pyAppGen.pbcs.legal_matter_management.forms import form_catalog
from pyAppGen.pbcs.legal_matter_management.release_evidence import validate_release_evidence
from pyAppGen.pbcs.legal_matter_management.standalone import LegalMatterManagementStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.legal_matter_management.ui import legal_matter_management_standalone_ui_contract
from pyAppGen.pbcs.legal_matter_management.wizards import wizard_catalog


def test_standalone_app_runs_intake_to_close_flow():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    demo = smoke['demo']
    assert demo['duplicate']['ok'] is False
    assert demo['conflict_block']['ok'] is False
    assert demo['deadline_bad']['ok'] is False
    assert demo['invoice_bad']['ok'] is False
    assert demo['settlement_bad']['ok'] is False
    assert demo['closed']['matter']['status'] == 'closed'


def test_forms_wizards_controls_surface_legal_domain():
    assert len(form_catalog()['forms']) >= 8
    assert len(wizard_catalog()['wizards']) >= 7
    assert legal_matter_management_standalone_ui_contract()['ok'] is True
    blocked = evaluate_control('conflict_clearance_control', {'adverse_party_screening': True})
    assert blocked['ok'] is False
    assert 'assign_counsel' in blocked['blocked_actions']


def test_critical_legal_controls_are_executable():
    app = LegalMatterManagementStandaloneApp()
    assert app.configure()['ok'] is True
    app.open_matter('MAT-X', 'regulatory', 'US-NY', 'critical', True, ('regulator',))
    bad_deadline = app.compute_deadline('DL-X', 'MAT-X', 1, 20, 'US-NY', True, ('lawyer-1',))
    assert bad_deadline['ok'] is False
    good_deadline = app.compute_deadline('DL-Y', 'MAT-X', 1, 20, 'US-NY', True, ('lawyer-1', 'lawyer-2'))
    assert good_deadline['ok'] is True
    bad_settlement = app.record_settlement_offer('OUT-X', 'MAT-X', 800000, 900000, ('gc',), ('release',))
    assert bad_settlement['ok'] is False


def test_agent_legal_work_preview_is_owned_and_confirmation_gated():
    app = LegalMatterManagementStandaloneApp()
    preview = app.assistant_legal_work_preview('hold memo', 'draft hold scope')
    assert preview['ok'] is True
    assert preview['crud_preview']['table'] == 'legal_matter_management_legal_matter'
    assert preview['requires_confirmation'] is True
    assert preview['legal_notice'] == 'draft_not_legal_advice_until_approved'
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['stream_engine_picker_visible'] is False
    assert all(table.startswith('legal_matter_management_') for table in contract['owned_tables'])


def test_release_evidence_includes_standalone_sections():
    evidence = validate_release_evidence()
    assert evidence['ok'] is True
    assert evidence['failed_checks'] == ()
