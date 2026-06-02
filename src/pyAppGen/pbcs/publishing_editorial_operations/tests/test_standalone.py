from pyAppGen.pbcs.publishing_editorial_operations.controls import evaluate_control
from pyAppGen.pbcs.publishing_editorial_operations.forms import form_catalog, form_for
from pyAppGen.pbcs.publishing_editorial_operations.standalone import (
    PublishingEditorialOperationsStandaloneApp,
    single_pbc_app_contract,
    standalone_smoke_test,
)
from pyAppGen.pbcs.publishing_editorial_operations.wizards import wizard_catalog, wizard_for


def test_single_pbc_app_contract_exposes_editorial_surface():
    contract = single_pbc_app_contract()

    assert contract["ok"] is True
    assert contract["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert contract["event_contract"] == "AppGen-X"
    assert contract["stream_engine_picker_visible"] is False
    assert contract["dsl"]["skills_namespace"] == "publishing_editorial_operations_skills"
    assert len(contract["forms"]["forms"]) >= 12
    assert len(contract["wizards"]["wizards"]) >= 10
    assert len(contract["controls"]["controls"]) >= 15


def test_forms_and_wizards_cover_publishing_specialties():
    assert form_catalog()["ok"] is True
    assert form_for("rights_and_permissions")["form"]["owned_table"] == "publishing_editorial_operations_rights_grant"
    assert form_for("distribution_release_binder")["ok"] is True
    assert wizard_catalog()["ok"] is True
    assert wizard_for("peer_review_decision")["ok"] is True
    assert wizard_for("release_evidence_binder")["ok"] is True


def test_controls_block_editorial_operational_failures():
    assert evaluate_control("acquisition_packet_complete", {"packet": "p"})["ok"] is False
    assert evaluate_control("rights_collision_absent", {"collisions": ()})["ok"] is True
    assert evaluate_control("release_binder_complete", {"missing_sections": ("proof",)})["ok"] is False
    assert evaluate_control("blind_review_privacy_enforced", {"blind": True, "redacted": False})["ok"] is False
    assert evaluate_control("agent_mutations_require_confirmation", {"confirmed": False})["ok"] is False


def test_standalone_editorial_workflow_is_executable_and_guarded():
    app = PublishingEditorialOperationsStandaloneApp()

    assert app.configure()["ok"] is True
    assert app.capture_acquisition("A0", "packet", None, (), "Fall")["ok"] is False
    assert app.capture_acquisition("A1", "packet", "editor", ("Comp A",), "Fall")["ok"] is True
    assert app.record_board_decision("BD0", "A1", "conditional", True, ())["ok"] is False
    assert app.record_board_decision("BD1", "A1", "conditional", True, ("revise",))["ok"] is True
    assert app.create_manuscript("M0", "A1", ("bio",), None)["ok"] is False
    assert app.create_manuscript("M1", "A1", (), None)["ok"] is True
    assert app.freeze_version("M1", None, None)["ok"] is False
    assert app.freeze_version("M1", "proof-v1", "ready")["ok"] is True
    assert app.invite_reviewer("R0", "M1", "double_blind", True, "double_blind")["ok"] is False
    assert app.invite_reviewer("R1", "M1", "double_blind", False, "double_blind")["ok"] is True
    assert app.approve_decision_bundle("DB0", "M1", "accept", None, ("revise",), "risk")["ok"] is False
    assert app.approve_decision_bundle("DB1", "M1", "accept", "reviews", ("revise",), "risk")["ok"] is True
    assert app.manage_copyedit("CE0", "M1", "house-v1", 1, True)["ok"] is False
    assert app.manage_copyedit("CE1", "M1", "house-v1", 0, True)["ok"] is True
    assert app.clear_rights("RG0", "M1", "US", "en", "ebook", ("collision",))["ok"] is False
    assert app.clear_rights("RG1", "M1", "US", "en", "ebook", ())["ok"] is True
    assert app.approve_edition("E0", "M1", (), ("alt-text",))["ok"] is False
    assert app.approve_edition("E1", "M1", ("ISBN-1",), ("alt-text",))["ok"] is True
    assert app.assemble_handoff("S0", "E1", "proof-v1", (), "RG1", "trim", "meta")["ok"] is False
    assert app.assemble_handoff("S1", "E1", "proof-v1", ("cover",), "RG1", "trim", "meta")["ok"] is True
    assert app.approve_proof("P0", "E1", 1)["ok"] is False
    assert app.approve_proof("P1", "E1", 0, blind=True, redacted=True)["ok"] is True
    assert app.publish_release_binder("B0", "E1", ("rights",))["ok"] is False
    assert app.publish_release_binder("B1", "E1", ())["ok"] is True
    assert app.open_exception("X1", "rights_collision", "rights-editor", "resolved")["ok"] is True
    assert app.simulate_schedule("late", 14, 1)["mutates_live_records"] is False
    assert app.assistant_editorial_action_preview("pitch", "create", confirmed=False)["ok"] is False
    assert app.assistant_editorial_action_preview("pitch", "create", confirmed=True)["ok"] is True


def test_standalone_smoke_proves_single_pbc_readiness():
    smoke = standalone_smoke_test()

    assert smoke["ok"] is True
    assert smoke["contract"]["routes"]["stream_engine_picker_visible"] is False
