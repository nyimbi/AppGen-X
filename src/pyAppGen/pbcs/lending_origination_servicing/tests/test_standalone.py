from pyAppGen.pbcs.lending_origination_servicing.controls import evaluate_control
from pyAppGen.pbcs.lending_origination_servicing.forms import form_catalog
from pyAppGen.pbcs.lending_origination_servicing.release_evidence import validate_release_evidence
from pyAppGen.pbcs.lending_origination_servicing.standalone import LendingOriginationServicingStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.lending_origination_servicing.ui import lending_origination_servicing_standalone_ui_contract
from pyAppGen.pbcs.lending_origination_servicing.wizards import wizard_catalog


def test_standalone_app_runs_origination_to_servicing_flow():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    demo = smoke['demo']
    assert demo['bad_app']['ok'] is False
    assert demo['fraud']['ok'] is False
    assert demo['blocked_funding']['ok'] is False
    assert demo['bad_board']['ok'] is False
    assert demo['promise_broken']['ok'] is False
    assert demo['mod_bad']['ok'] is False
    assert demo['payoff']['payoff_quote']['total'] >= 0


def test_forms_wizards_controls_surface_lending_domain():
    assert len(form_catalog()['forms']) >= 9
    assert len(wizard_catalog()['wizards']) >= 7
    assert lending_origination_servicing_standalone_ui_contract()['ok'] is True
    blocked = evaluate_control('funding_boarding_control', {'closing_conditions': True})
    assert blocked['ok'] is False
    assert 'post_disbursement' in blocked['blocked_actions']


def test_underwriting_and_funding_blockers_are_executable():
    app = LendingOriginationServicingStandaloneApp()
    assert app.configure()['ok'] is True
    app.create_application('APP-X', 'BOR-X', ('applicant',), 'home_improvement', 100000, ('credit_pull', 'privacy'))
    app.verify_borrower('BOR-X', 80000, 70000, 5000, True, (), 650)
    decline = app.underwrite('DEC-X', 'APP-X', 'consumer', '2026.05')
    assert decline['ok'] is False
    assert 'dti_exceeds_policy' in decline['decision']['reason_codes']


def test_agent_lending_file_preview_is_owned_and_confirmation_gated():
    app = LendingOriginationServicingStandaloneApp()
    preview = app.assistant_lending_file_preview('paystub and note', 'draft application update')
    assert preview['ok'] is True
    assert preview['crud_preview']['table'] == 'lending_origination_servicing_loan_application'
    assert preview['requires_confirmation'] is True
    assert preview['extraction']['citation_spans_required'] is True
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['stream_engine_picker_visible'] is False
    assert all(table.startswith('lending_origination_servicing_') for table in contract['owned_tables'])


def test_release_evidence_includes_standalone_sections():
    evidence = validate_release_evidence()
    assert evidence['ok'] is True
    assert evidence['failed_checks'] == ()
