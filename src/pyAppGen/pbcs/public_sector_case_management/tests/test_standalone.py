from pyAppGen.pbcs.public_sector_case_management.controls import evaluate_control
from pyAppGen.pbcs.public_sector_case_management.forms import form_catalog, form_for
from pyAppGen.pbcs.public_sector_case_management.standalone import (
    PublicSectorCaseManagementStandaloneApp,
    single_pbc_app_contract,
    standalone_smoke_test,
)
from pyAppGen.pbcs.public_sector_case_management.wizards import wizard_catalog, wizard_for


def test_single_pbc_app_contract_exposes_operable_surface():
    contract = single_pbc_app_contract()

    assert contract["ok"] is True
    assert contract["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["stream_engine_picker_visible"] is False
    assert contract["dsl"]["skills_namespace"] == "public_sector_case_management_skills"
    assert len(contract["forms"]["forms"]) >= 12
    assert len(contract["wizards"]["wizards"]) >= 9
    assert len(contract["controls"]["controls"]) >= 15
    assert contract["agent"]["ok"] is True


def test_forms_and_wizards_cover_public_sector_specialist_domain():
    assert form_catalog()["ok"] is True
    assert form_for("evidence_intake_and_sufficiency")["form"]["owned_table"] == "public_sector_case_management_eligibility_determination"
    assert form_for("appeal_hearing")["ok"] is True
    assert form_for("sla_override_fraud_handoff")["ok"] is True
    assert wizard_catalog()["ok"] is True
    assert wizard_for("appeal_hearing_management")["ok"] is True
    assert wizard_for("privacy_override_and_fraud_handoff")["ok"] is True


def test_controls_block_due_process_privacy_and_governance_failures():
    assert evaluate_control("intake_envelope_complete", {"channel": "portal", "language": "en"})["ok"] is False
    assert evaluate_control("evidence_sufficient_for_rule", {"sufficiency": "satisfied"})["ok"] is True
    assert evaluate_control("notice_has_rule_citation", {"citation": None, "fact_snapshot": {}})["ok"] is False
    assert evaluate_control("purpose_based_access_declared", {"sensitive": True, "purpose": None})["ok"] is False
    assert evaluate_control("fraud_handoff_boundary", {"investigative_notes_visible": True})["ok"] is False
    assert evaluate_control("agent_mutations_require_confirmation", {"confirmed": False})["ok"] is False


def test_standalone_case_lifecycle_is_executable_and_guarded():
    app = PublicSectorCaseManagementStandaloneApp()

    assert app.configure()["ok"] is True
    assert app.capture_intake("IN0", "portal", "en", "housing", "")["ok"] is False
    assert app.capture_intake("IN1", "portal", "en", "housing", "reachable")["ok"] is True
    assert app.open_case("C0", "IN1", "Amina", None)["ok"] is False
    assert app.open_case("C1", "IN1", "Amina", "north", confidential=True)["ok"] is True
    assert app.record_household("H0", "C1", ("Amina",), "Legal Aid", False)["ok"] is False
    assert app.record_household("H1", "C1", ("Amina", "Child"), "Legal Aid", True)["ok"] is True
    assert app.screen_programs("S1", "C1", ("housing", "food"))["ok"] is True
    assert app.ingest_evidence("E0", "C1", "pay_stub", (), 0.4, "income")["ok"] is False
    assert app.ingest_evidence("E1", "C1", "lease", ("residency",), 0.9, "residency")["ok"] is True
    assert app.generate_checklist("CL0", "C1", ("id",), expired=True, tolled=False)["ok"] is False
    assert app.generate_checklist("CL1", "C1", ("id",), expired=True, tolled=True)["ok"] is True
    assert app.determine_eligibility("D0", "C1", "manual_review", "2026-01-01")["ok"] is False
    assert app.determine_eligibility("D1", "C1", "satisfied", "2026-01-01", "2025-12-01")["ok"] is True
    assert app.render_notice("N0", "C1", "denial", None, {}, "mail")["ok"] is False
    assert app.render_notice("N1", "C1", "approval", "housing-101", {"eligible": True}, "mail")["ok"] is True
    assert app.create_referral("R0", "C1", "housing", "Partner", includes_restricted=True)["ok"] is False
    assert app.create_referral("R1", "C1", "housing", "Partner")["ok"] is True
    assert app.intake_appeal("A0", "C1", True, False, "approve")["ok"] is False
    assert app.intake_appeal("A1", "C1", True, True, "approve")["ok"] is True
    assert app.assemble_hearing_packet("HP0", "A1", None, (), (), (), None)["ok"] is False
    assert app.assemble_hearing_packet("HP1", "A1", "denial", ("intake",), ("E1",), ("N1",), "housing-101")["ok"] is True
    assert app.manage_sla("SLA0", "C1", expired=True)["ok"] is False
    assert app.manage_sla("SLA1", "C1", expired=True, pause_reason="citizen response")["ok"] is True
    assert app.declare_purpose_access("P0", "C1", sensitive=True, purpose=None)["ok"] is False
    assert app.declare_purpose_access("P1", "C1", sensitive=True, purpose="eligibility", marker="protected_address", masked=True)["ok"] is True
    assert app.approve_override("O0", "C1", "hardship", None, "supervisor", "2026-12-31")["ok"] is False
    assert app.approve_override("O1", "C1", "hardship", "emergency", "supervisor", "2026-12-31")["ok"] is True
    assert app.prepare_fraud_handoff("F0", "C1", "identity_conflict", ("E1",), investigative_notes_visible=True)["ok"] is False
    assert app.prepare_fraud_handoff("F1", "C1", "identity_conflict", ("E1",))["ok"] is True
    assert app.assistant_case_action_preview("packet", "update case", confirmed=False)["ok"] is False
    assert app.assistant_case_action_preview("packet", "update case", confirmed=True)["ok"] is True


def test_standalone_smoke_proves_single_pbc_readiness():
    smoke = standalone_smoke_test()

    assert smoke["ok"] is True
    assert smoke["contract"]["routes"]["stream_engine_picker_visible"] is False
