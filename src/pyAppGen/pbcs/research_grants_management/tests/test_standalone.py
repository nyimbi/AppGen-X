from pyAppGen.pbcs.research_grants_management.controls import evaluate_control
from pyAppGen.pbcs.research_grants_management.forms import form_catalog, form_for
from pyAppGen.pbcs.research_grants_management.standalone import (
    ResearchGrantsManagementStandaloneApp,
    single_pbc_app_contract,
    standalone_smoke_test,
)
from pyAppGen.pbcs.research_grants_management.wizards import wizard_catalog, wizard_for


def test_single_pbc_app_contract_exposes_research_grants_surface():
    contract = single_pbc_app_contract()
    assert contract["ok"] is True
    assert contract["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["stream_engine_picker_visible"] is False
    assert contract["dsl"]["skills_namespace"] == "research_grants_management_skills"
    assert len(contract["forms"]["forms"]) >= 14
    assert len(contract["wizards"]["wizards"]) >= 11
    assert len(contract["controls"]["controls"]) >= 16


def test_forms_and_wizards_cover_sponsored_research_specialties():
    assert form_catalog()["ok"] is True
    assert form_for("funding_opportunity")["form"]["owned_table"] == "research_grants_management_grant_proposal"
    assert form_for("award_notice_extraction")["ok"] is True
    assert form_for("effort_certification")["ok"] is True
    assert wizard_catalog()["ok"] is True
    assert wizard_for("opportunity_to_proposal")["ok"] is True
    assert wizard_for("subaward_issue_monitor")["ok"] is True
    assert wizard_for("assistant_document_to_action")["ok"] is True


def test_controls_block_research_admin_edge_cases():
    assert evaluate_control("opportunity_has_traceable_notice", {"sponsor": "NIH"})["ok"] is False
    assert evaluate_control("limited_submission_slot_available", {"selected_count": 2, "slot_count": 1})["ok"] is False
    assert evaluate_control("proposal_sections_submission_ready", {"sections": {"abstract": "approved", "aims": "draft"}})["ok"] is False
    assert evaluate_control("budget_line_allowable_or_justified", {"allowability": "restricted"})["ok"] is False
    assert evaluate_control("award_readiness_gates_clear", {"gates": {"account_setup": True, "budget": False}})["ok"] is False
    assert evaluate_control("effort_boundary_respected", {"mutates_payroll": True})["ok"] is False
    assert evaluate_control("agent_mutations_require_confirmation", {"confirmed": False})["ok"] is False


def test_standalone_research_grants_workflow_is_executable_and_guarded():
    app = ResearchGrantsManagementStandaloneApp()
    assert app.configure()["ok"] is True
    assert app.register_opportunity("O0", "NIH", None, "2026-07-01", None)["ok"] is False
    assert app.register_opportunity("O1", "NIH", "R01", "2026-07-01", "notice-hash")["ok"] is True
    assert app.evaluate_eligibility("P0", "O1", "blocked")["ok"] is False
    assert app.evaluate_eligibility("P1", "O1", "pass")["ok"] is True
    assert app.allocate_limited_submission_slot("P1", 2, 1, "minutes")["ok"] is False
    assert app.allocate_limited_submission_slot("P1", 1, 1, "minutes")["ok"] is True
    assert app.build_deadline_calendar("P1", sponsor_submission="2026-07-01")["ok"] is False
    assert app.build_deadline_calendar("P1", sponsor_submission="2026-07-01", institutional_routing="2026-06-20", compliance_review="2026-06-15", budget_final="2026-06-18", collaborator_packet="2026-06-12", narrative_freeze="2026-06-22")["ok"] is True
    assert app.assemble_proposal_sections("P1", {"abstract": "approved", "aims": "draft"})["ok"] is False
    assert app.assemble_proposal_sections("P1", {"abstract": "approved", "aims": "approved", "narrative": "approved"})["ok"] is True
    assert app.validate_budget_line("B0", "P1", "participant_support", 5000, allowability="restricted")["ok"] is False
    assert app.validate_budget_line("B1", "P1", "participant_support", 5000, allowability="restricted", justification="ok", prior_approval_reference="PA")["ok"] is True
    assert app.approve_cost_share("CS0", "P1", "mandatory", source_account="A")["ok"] is False
    assert app.approve_cost_share("CS1", "P1", "mandatory", source_account="A", responsible_unit="School", approval_chain=("dean",))["ok"] is True
    assert app.calculate_indirect_cost("I0", 100000, .55, .2)["ok"] is False
    assert app.calculate_indirect_cost("I1", 100000, .55, .2, waiver_approver="vp", waiver_reason="cap", sponsor_citation="rfa")["ok"] is True
    assert app.classify_compliance_dependency("C0", "P1", required=True, status="pending")["ok"] is False
    assert app.classify_compliance_dependency("C1", "P1", required=True, status="approved")["ok"] is True
    assert app.extract_award_notice("A1", total_amount=100000, obligated_amount=50000, project_start="2026-09-01", project_end="2027-08-31", reporting_schedule="annual")["ok"] is True
    assert app.activate_award("A1", {"account_setup": True, "budget_activation": False})["ok"] is False
    assert app.activate_award("A1", {"account_setup": True, "budget_activation": True})["ok"] is True
    assert app.issue_subaward("S0", "A1", True, False, True, "high")["ok"] is False
    assert app.issue_subaward("S1", "A1", True, True, True, "high")["ok"] is True
    assert app.generate_report_pack("R0", "A1", 90, 100)["ok"] is False
    assert app.generate_report_pack("R1", "A1", 100, 100)["ok"] is True
    assert app.certify_effort("E0", "A1", .2, .3)["ok"] is False
    assert app.certify_effort("E1", "A1", .2, .3, exception_reason="approved")["ok"] is True
    assert app.simulate_no_cost_extension("A1", "2027-08-31", "2028-02-28", 12000, "delay")["mutates_live_records"] is False
    assert app.assistant_document_action_preview("notice", "create", False)["ok"] is False
    assert app.assistant_document_action_preview("notice", "create", True)["ok"] is True


def test_standalone_smoke_proves_single_pbc_readiness():
    smoke = standalone_smoke_test()
    assert smoke["ok"] is True
    assert smoke["contract"]["routes"]["stream_engine_picker_visible"] is False
