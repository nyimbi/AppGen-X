from pyAppGen.pbcs.grant_fund_accounting.controls import evaluate_control
from pyAppGen.pbcs.grant_fund_accounting.forms import form_catalog
from pyAppGen.pbcs.grant_fund_accounting.release_evidence import validate_release_evidence
from pyAppGen.pbcs.grant_fund_accounting.standalone import GrantFundAccountingStandaloneApp, single_pbc_app_contract, standalone_smoke_test
from pyAppGen.pbcs.grant_fund_accounting.ui import grant_fund_accounting_standalone_ui_contract
from pyAppGen.pbcs.grant_fund_accounting.wizards import wizard_catalog


def test_standalone_app_runs_award_to_closeout_flow():
    smoke = standalone_smoke_test()
    assert smoke['ok'] is True
    assert smoke['demo']['blocked_cost']['ok'] is False
    assert smoke['demo']['drawdown']['drawdown']['status'] == 'ready'
    assert smoke['demo']['report']['report']['status'] == 'ready_for_submission'
    assert smoke['demo']['closeout']['closeout']['status'] == 'closed'


def test_forms_wizards_controls_surface_grant_domain():
    assert len(form_catalog()['forms']) >= 10
    assert len(wizard_catalog()['wizards']) >= 6
    assert grant_fund_accounting_standalone_ui_contract()['ok'] is True
    blocked = evaluate_control('restriction_allowability_control', {'failures': ('draw_submission',)})
    assert blocked['ok'] is False
    assert 'draw_submission' in blocked['blocked_actions']


def test_agent_award_preview_stays_owned_and_confirmation_gated():
    app = GrantFundAccountingStandaloneApp()
    preview = app.assistant_award_preview('award notice', 'create award and restrictions')
    assert preview['ok'] is True
    assert preview['crud_preview']['table'] == 'grant_fund_accounting_grant_award'
    assert preview['requires_confirmation'] is True
    contract = single_pbc_app_contract()
    assert contract['ok'] is True
    assert contract['stream_engine_picker_visible'] is False
    assert all(table.startswith('grant_fund_accounting_') for table in contract['owned_tables'])


def test_release_evidence_includes_standalone_sections():
    assert validate_release_evidence()['ok'] is True
