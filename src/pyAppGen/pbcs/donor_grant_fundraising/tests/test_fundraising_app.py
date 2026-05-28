from pyAppGen.pbcs.donor_grant_fundraising.agent import document_instruction_plan
from pyAppGen.pbcs.donor_grant_fundraising.fundraising_app import (
    advance_prospect_stage,
    build_fundraising_workbench,
    controls_contract,
    create_campaign,
    create_pledge,
    create_restriction,
    empty_fundraising_state,
    forms_contract,
    fundraising_app_smoke_test,
    manage_grant_application,
    post_gift,
    record_stewardship_touchpoint,
    register_donor_profile,
    single_pbc_app_contract,
    wizards_contract,
)
from pyAppGen.pbcs.donor_grant_fundraising.services import DonorGrantFundraisingService


def test_single_pbc_app_has_forms_wizards_controls_and_database_contract():
    app = single_pbc_app_contract()

    assert app["ok"] is True
    assert app["single_pbc_app"] is True
    assert app["allowed_database_backends"] == ("postgresql", "mysql", "mariadb")
    assert {form["command"] for form in forms_contract()["forms"]} >= {
        "register_donor_profile",
        "advance_prospect_stage",
        "create_campaign",
        "create_pledge",
        "post_gift",
        "manage_grant_application",
        "record_stewardship_touchpoint",
    }
    assert any(wizard["wizard_id"] == "grant_submission_wizard" for wizard in wizards_contract()["wizards"])
    assert all(control["blocks_on_failure"] for control in controls_contract()["controls"])


def test_donor_profile_and_prospect_pipeline_enforce_stage_evidence():
    state = empty_fundraising_state()
    donor = register_donor_profile(
        state,
        {
            "donor_id": "donor-a",
            "name": "Amina Rao",
            "donor_type": "individual",
            "recognition_preference": "anonymous",
            "next_action_date": "2026-06-01",
        },
    )
    blocked = advance_prospect_stage(donor["state"], {"donor_id": "donor-a", "target_stage": "solicitation_ready"})
    qualified = advance_prospect_stage(donor["state"], {"donor_id": "donor-a", "target_stage": "researched"})

    assert donor["ok"] is True
    assert blocked["ok"] is False
    assert "stage_skip_requires_approval" in blocked["blockers"]
    assert qualified["ok"] is True
    assert qualified["donor"]["relationship_stage"] == "researched"


def test_campaign_pledge_restriction_gift_flow_updates_balances_and_progress():
    state = empty_fundraising_state()
    donor = register_donor_profile(state, {"donor_id": "donor-a", "donor_type": "foundation", "recognition_preference": "named"})
    campaign = create_campaign(donor["state"], {"campaign_id": "camp-a", "goal_amount": 1000})
    pledge = create_pledge(
        campaign["state"],
        {
            "pledge_id": "pledge-a",
            "donor_id": "donor-a",
            "campaign_id": "camp-a",
            "amount": 1000,
            "installments": ({"amount": 500}, {"amount": 500}),
        },
    )
    restriction = create_restriction(pledge["state"], {"restriction_id": "rest-a", "restriction_type": "purpose", "purpose_code": "education"})
    gift = post_gift(
        restriction["state"],
        {
            "gift_id": "gift-a",
            "donor_id": "donor-a",
            "campaign_id": "camp-a",
            "pledge_id": "pledge-a",
            "restriction_id": "rest-a",
            "purpose_code": "education",
            "amount": 400,
        },
    )

    assert gift["ok"] is True
    assert gift["pledge"]["remaining_balance"] == 600
    assert gift["campaign"]["current_amount"] == 400
    assert gift["gift"]["receipt_status"] == "receipt_due"
    assert gift["state"]["outbox"][-1]["event_contract"] == "AppGen-X"


def test_restriction_mismatch_and_grant_submission_controls_block_bad_actions():
    state = empty_fundraising_state()
    restriction = create_restriction(state, {"restriction_id": "rest-a", "restriction_type": "purpose", "purpose_code": "health"})
    bad_gift = post_gift(restriction["state"], {"gift_id": "gift-b", "amount": 50, "restriction_id": "rest-a", "purpose_code": "education"})
    bad_grant = manage_grant_application(restriction["state"], {"grant_application_id": "grant-b", "stage": "submitted", "proposal_complete": True})

    assert bad_gift["ok"] is False
    assert "restriction_purpose_mismatch" in bad_gift["gift"]["blockers"]
    assert bad_grant["ok"] is False
    assert "internal_review_missing" in bad_grant["grant_application"]["blockers"]


def test_stewardship_and_workbench_queues_surface_operating_backlog():
    state = empty_fundraising_state()
    donor = register_donor_profile(state, {"donor_id": "donor-a", "donor_type": "individual", "recognition_preference": "public", "next_action_date": "2026-06-01"})
    gift = post_gift(donor["state"], {"gift_id": "gift-a", "donor_id": "donor-a", "amount": 100})
    stewardship = record_stewardship_touchpoint(gift["state"], {"donor_id": "donor-a", "requires_acknowledgement": True, "cadence_overdue": True})
    workbench = build_fundraising_workbench(stewardship["state"])

    assert stewardship["ok"] is False
    assert workbench["queue_counts"]["portfolio_next_actions"] == 1
    assert workbench["queue_counts"]["acknowledgement_backlog"] == 1
    assert workbench["queue_counts"]["stewardship_gaps"] == 1
    assert workbench["queue_counts"]["exception_backlog"] >= 1


def test_agent_document_plan_is_stable_and_domain_routed():
    first = document_instruction_plan("grant guidelines", "prepare proposal")
    second = document_instruction_plan("grant guidelines", "prepare proposal")
    gift = document_instruction_plan("donation receipt letter", "post gift")

    assert first["document_digest"] == second["document_digest"]
    assert first["domain_plan"]["target_table"] == "donor_grant_fundraising_grant_application"
    assert gift["domain_plan"]["proposed_operation"] == "post_gift"
    assert first["requires_human_confirmation"] is True


def test_stateful_service_executes_domain_app_commands_and_queries():
    service = DonorGrantFundraisingService()
    donor = service.register_donor_profile({"donor_id": "donor-svc", "donor_type": "foundation", "recognition_preference": "named"})
    campaign = service.create_campaign({"campaign_id": "camp-svc", "goal_amount": 500})
    workbench = service.build_fundraising_workbench({})

    assert donor["ok"] is True
    assert campaign["ok"] is True
    assert workbench["ok"] is True
    assert "donor-svc" in service.state["donors"]
    assert "camp-svc" in service.state["campaigns"]


def test_fundraising_app_smoke_covers_end_to_end_flow():
    assert fundraising_app_smoke_test()["ok"] is True
