"""Domain behavior checks for wealth portfolio management improve1 controls."""
from ..release_evidence import build_release_evidence, validate_release_evidence
from ..runtime import wealth_portfolio_management_runtime_capabilities
from ..ui import wealth_portfolio_management_render_workbench, wealth_portfolio_management_ui_contract
from ..wealth_portfolio_management_control import CONTROL_SPECS, WEALTH_ALLOWED_DATABASE_BACKENDS, WEALTH_CONTROL_OWNED_TABLES, WEALTH_DECLARED_DEPENDENCIES, WEALTH_REQUIRED_EVENT_TOPIC, evaluate_wealth_portfolio_management_control, improve1_wealth_portfolio_management_control_contract, sample_payload_for

def test_all_50_wealth_controls_are_executable_and_owned():
    contract=improve1_wealth_portfolio_management_control_contract(); assert contract["ok"] is True; assert contract["capability_count"]==50; assert contract["allowed_database_backends"]==("postgresql","mysql","mariadb"); assert contract["event_contract"]=="AppGen-X"; assert contract["required_event_topic"]==WEALTH_REQUIRED_EVENT_TOPIC; assert contract["stream_engine_picker_visible"] is False
    for item in contract["capabilities"]:
        assert item["ok"] is True, item["findings"]; assert item["side_effects"]==(); assert item["evidence"]["service_api"].startswith("POST /wealth-portfolio-management/improve1/"); assert item["evidence"]["ui_surface"].startswith("WealthPortfolioManagement"); assert item["evidence"]["allowed_database_backends"]==WEALTH_ALLOWED_DATABASE_BACKENDS
        for table in item["evidence"]["owned_tables"]: assert table in WEALTH_CONTROL_OWNED_TABLES and table.startswith("wealth_portfolio_management_")
        for dependency in item["evidence"]["declared_dependencies"]: assert dependency in WEALTH_DECLARED_DEPENDENCIES

def test_runtime_ui_and_release_surfaces_expose_wealth_control_contract():
    runtime=wealth_portfolio_management_runtime_capabilities(); ui=wealth_portfolio_management_ui_contract(); workbench=wealth_portfolio_management_render_workbench(); release=build_release_evidence(); validation=validate_release_evidence()
    assert runtime["ok"] is True; assert runtime["wealth_portfolio_management_control"]["capability_count"]==50; assert "evaluate_wealth_portfolio_management_control" in runtime["operations"]
    assert ui["ok"] is True and ui["stream_engine_picker_visible"] is False and len(ui["wealth_portfolio_management_control_panels"])==50
    assert workbench["ok"] is True and len(workbench["wealth_portfolio_management_control_agent_tools"])==50
    assert release["ok"] is True and release["wealth_portfolio_management_control"]["ok"] is True
    assert validation["ok"] is True and validation["wealth_portfolio_management_control"]["ok"] is True

def test_wealth_domains_fail_closed_without_evidence():
    for feature in (1,2,3,4,5,6,7,8,19,20,21,29,30,42,43,44,49,50):
        result=evaluate_wealth_portfolio_management_control(feature,{"client_mandate_evidence_complete":False}); assert result["ok"] is False; assert any("client portfolio lifecycle" in f for f in result["findings"])
    for feature in (9,10,11,12,13,14,22,23,24,25,26,27,28,31,32,46,50):
        result=evaluate_wealth_portfolio_management_control(feature,{"portfolio_trading_evidence_complete":False}); assert result["ok"] is False; assert any("holdings boundaries" in f for f in result["findings"])
    for feature in (15,16,17,18,24,30,40,45,47,48,50):
        result=evaluate_wealth_portfolio_management_control(feature,{"fees_performance_evidence_complete":False}); assert result["ok"] is False; assert any("performance snapshots" in f for f in result["findings"])
    for feature in (33,34,35,36,37,38,39,40,41,42,43,44,47,48,49,50):
        result=evaluate_wealth_portfolio_management_control(feature,{"governance_agent_evidence_complete":False}); assert result["ok"] is False; assert any("exception taxonomy" in f for f in result["findings"])

def test_agent_judgment_and_approval_controls_are_gated():
    for feature in (4,6,7,11,12,14,19,20,21,26,27,28,29,31,36,37,38,41,43,44,49,50):
        result=evaluate_wealth_portfolio_management_control(feature,{"human_confirmation":False}); assert result["ok"] is False; assert any("human confirmation" in f for f in result["findings"])
    for feature in (4,7,11,12,14,21,26,29,31,37,38,41,43,44,49,50):
        result=evaluate_wealth_portfolio_management_control(feature,{"approver_separate_from_initiator":False}); assert result["ok"] is False; assert any("separated approval" in f for f in result["findings"])
    for feature in (36,37,38,49,50):
        result=evaluate_wealth_portfolio_management_control(feature,{"agent_preview_only":False}); assert result["ok"] is False; assert any("reversible CRUD previews" in f for f in result["findings"])

def test_database_eventing_owned_boundary_and_projection_constraints():
    assert evaluate_wealth_portfolio_management_control(1,{"database_backend":"sqlite"})["ok"] is False
    assert evaluate_wealth_portfolio_management_control(50,{"event_topic":"custom.stream"})["ok"] is False
    assert evaluate_wealth_portfolio_management_control(50,{"stream_engine_picker_visible":True})["ok"] is False
    assert evaluate_wealth_portfolio_management_control(48,{"shared_table_access":True})["ok"] is False
    assert evaluate_wealth_portfolio_management_control(9,{"dependency_access_mode":"shared_table"})["ok"] is False

def test_sample_payloads_are_domain_specific_and_side_effect_free():
    portfolio=sample_payload_for(1); assert portfolio["portfolio_lifecycle_id"].startswith("client_portfolio_lifecycle_model"); assert portfolio["client_portfolio_lifecycle_model_verified"] is True; assert portfolio["side_effects"]==()
    rebalance=evaluate_wealth_portfolio_management_control("rebalance_order_lifecycle"); assert rebalance["ok"] is True; assert "tax_check_status" in rebalance["evidence"]["required_fields"]; assert "restriction_check_status" in rebalance["evidence"]["required_fields"]
    boundary=CONTROL_SPECS[48]; assert boundary["route"].endswith("/cross_pbc_boundary_proof"); assert "no_foreign_mutation" in boundary["fields"]
