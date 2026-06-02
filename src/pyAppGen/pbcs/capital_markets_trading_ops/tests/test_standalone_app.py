from pyAppGen.pbcs.capital_markets_trading_ops.post_trade import allocation_contract
from pyAppGen.pbcs.capital_markets_trading_ops.post_trade import confirmation_contract
from pyAppGen.pbcs.capital_markets_trading_ops.post_trade import execution_capture_contract
from pyAppGen.pbcs.capital_markets_trading_ops.post_trade import post_trade_smoke_test
from pyAppGen.pbcs.capital_markets_trading_ops.standalone import CapitalMarketsTradingOpsStandaloneApp
from pyAppGen.pbcs.capital_markets_trading_ops.standalone import single_pbc_app_contract
from pyAppGen.pbcs.capital_markets_trading_ops.standalone import standalone_smoke_test
from pyAppGen.pbcs.capital_markets_trading_ops.ui import capital_markets_trading_ops_standalone_app_contract


def test_post_trade_contracts_cover_execution_allocation_confirmation():
    assert execution_capture_contract()["ok"] is True
    assert allocation_contract()["ok"] is True
    assert confirmation_contract()["ok"] is True
    assert post_trade_smoke_test()["ok"] is True


def test_standalone_app_runs_order_to_settlement_flow():
    app = CapitalMarketsTradingOpsStandaloneApp()
    try:
        loaded = app.load_demo_workspace()
        workbench = app.workbench()
        assert loaded["ok"] is True
        assert loaded["trade_break"]["record"]["category"] == "settlement"
        assert workbench["summary"]["settlement_fails"] == 1
        assert workbench["summary"]["open_breaks"] == 1
    finally:
        app.close()


def test_single_pbc_app_surfaces_forms_wizards_controls_and_agent_namespace():
    ui = capital_markets_trading_ops_standalone_app_contract()
    contract = single_pbc_app_contract()
    assert ui["ok"] is True
    assert len(contract["forms"]) >= 8
    assert len(contract["wizards"]) >= 6
    assert len(contract["controls"]) >= 8
    assert contract["dsl_exposure"]["agent_skill_namespace"] == "capital_markets_trading_ops_skills"
    assert standalone_smoke_test()["ok"] is True
