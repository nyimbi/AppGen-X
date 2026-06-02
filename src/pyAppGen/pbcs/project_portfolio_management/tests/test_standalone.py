from pyAppGen.pbcs.project_portfolio_management.controls import evaluate_control
from pyAppGen.pbcs.project_portfolio_management.forms import form_catalog, form_for
from pyAppGen.pbcs.project_portfolio_management.standalone import (
    ProjectPortfolioManagementStandaloneApp,
    single_pbc_app_contract,
    standalone_smoke_test,
)
from pyAppGen.pbcs.project_portfolio_management.wizards import wizard_catalog, wizard_for


def test_standalone_app_exposes_forms_wizards_controls_and_agent():
    contract = single_pbc_app_contract()

    assert contract["ok"] is True
    assert contract["event_contract"] == "AppGen-X"
    assert contract["stream_engine_picker_visible"] is False
    assert contract["dsl"]["skills_namespace"] == "project_portfolio_management_skills"
    assert len(contract["forms"]["forms"]) >= 9
    assert len(contract["wizards"]["wizards"]) >= 7
    assert len(contract["controls"]["controls"]) >= 10
    assert contract["agent"]["ok"] is True


def test_domain_forms_and_wizards_cover_deep_project_portfolio_work():
    assert form_catalog()["ok"] is True
    assert form_for("business_case_assumptions")["form"]["owned_table"] == "project_portfolio_management_business_case"
    assert form_for("financial_snapshot")["ok"] is True
    assert wizard_catalog()["ok"] is True
    assert wizard_for("dependency_and_risk_review")["ok"] is True
    assert wizard_for("executive_scenario_planning")["ok"] is True


def test_controls_block_table_stakes_edge_cases():
    assert evaluate_control("intake_readiness_required", {"score": 69})["ok"] is False
    assert evaluate_control("scoring_weights_balanced", {"weights": (0.4, 0.25, 0.2, 0.15)})["ok"] is True
    assert evaluate_control("prioritization_must_fit_constraints", {"cost": 200, "budget": 100, "demand": 1, "capacity": 2})["ok"] is False
    assert evaluate_control("agent_mutations_require_confirmation", {"confirmed": False})["ok"] is False


def test_standalone_portfolio_workflow_is_executable_and_governed():
    app = ProjectPortfolioManagementStandaloneApp()

    assert app.configure()["ok"] is True
    assert app.intake_item("I0", "Weak", None, "innovation", (), (), 10)["ok"] is False
    assert app.intake_item("I1", "Modernize", "CFO", "platform", ("growth",), ("brief",), 85)["ok"] is True
    assert app.intake_item("I2", "Resilience", "COO", "risk", ("resilience",), ("memo",), 82)["ok"] is True
    assert app.create_business_case("BC1", "I1", 100000, 250000, ("adoption",))["ok"] is True
    assert app.score_item("S1", "I1", 0.9, 0.8, 0.2, 0.8)["ok"] is True
    assert app.prioritize("P0", ("I1", "I2"), 50000, 1)["ok"] is False
    assert app.prioritize("P1", ("I1",), 200000, 1)["ok"] is True
    assert app.record_gate("G0", "I1", "funding", (), True, "approved")["ok"] is False
    assert app.record_gate("G1", "I1", "funding", ("case",), True, "approved")["ok"] is True
    assert app.map_dependency("D1", "I1", "I2", 0.3)["ok"] is True
    assert app.assign_resources("R0", "I1", "architect", 2, 1)["ok"] is False
    assert app.assign_resources("R1", "I1", "architect", 1, 1)["ok"] is True
    assert app.measure_benefit("B0", "I1", 0, 100, 80, None, 0.8)["ok"] is False
    assert app.measure_benefit("B1", "I1", 0, 100, 90, "metric", 0.8)["ok"] is True
    assert app.record_risk("RK0", "I1", 0.9, False)["ok"] is False
    assert app.record_risk("RK1", "I1", 0.9, True)["ok"] is True
    assert app.open_issue("ISS1", "I1", "high", "owner")["ok"] is True
    assert app.process_change_request("CR1", "I1", 1000, 5000, True)["ok"] is True
    assert app.snapshot_financials("F0", "I1", 100000, 250000, 90000, materiality=100000)["ok"] is False
    assert app.snapshot_financials("F1", "I1", 100000, 250000, 90000, "scope", materiality=100000)["ok"] is True
    assert app.resolve_exception("EX1", "I1", "strategic", "cfo")["ok"] is True
    assert app.simulate_scenario("cut", -10000, 0)["mutates_live_records"] is False
    assert app.assistant_portfolio_action_preview("doc", "update", confirmed=False)["ok"] is False
    assert app.assistant_portfolio_action_preview("doc", "update", confirmed=True)["ok"] is True


def test_standalone_smoke_test_proves_single_pbc_app():
    smoke = standalone_smoke_test()

    assert smoke["ok"] is True
    assert smoke["contract"]["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert smoke["contract"]["routes"]["stream_engine_picker_visible"] is False
