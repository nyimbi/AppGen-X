from pyAppGen.pbcs.donor_grant_fundraising.agent import document_instruction_plan
from pyAppGen.pbcs.donor_grant_fundraising.fundraising_app import (
    advance_prospect_stage,
    build_fundraising_workbench,
    compose_proposal_workspace,
    controls_contract,
    create_campaign,
    create_pledge,
    create_restriction,
    empty_fundraising_state,
    forms_contract,
    fundraising_app_smoke_test,
    generate_briefing_packet,
    manage_grant_application,
    manage_review_chain,
    map_donor_relationship,
    post_gift,
    record_stewardship_touchpoint,
    register_donor_profile,
    score_fundraising_opportunity,
    single_pbc_app_contract,
    track_acknowledgement,
    validate_grant_budget,
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
        "compose_proposal_workspace",
        "manage_review_chain",
        "validate_grant_budget",
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
    qualified = advance_prospect_stage(
        donor["state"],
        {"donor_id": "donor-a", "target_stage": "researched", "qualification_evidence": ("profile-reviewed",)},
    )

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


def test_proposal_review_budget_and_briefing_flow_are_executable():
    state = empty_fundraising_state()
    donor = register_donor_profile(state, {"donor_id": "donor-a", "donor_type": "foundation", "recognition_preference": "named"})
    restriction = create_restriction(
        donor["state"],
        {"restriction_id": "rest-a", "restriction_type": "purpose", "purpose_code": "health", "required_approvals": ("finance",), "time_window": "fy26"},
    )
    grant = manage_grant_application(
        restriction["state"],
        {
            "grant_application_id": "grant-a",
            "funder_id": "donor-a",
            "stage": "submitted",
            "proposal_complete": True,
            "review_signoffs": ("program", "finance"),
            "budget": {"purpose_code": "health", "line_items": ({"amount": 600}, {"amount": 400})},
        },
    )
    workspace = compose_proposal_workspace(
        grant["state"],
        {
            "grant_application_id": "grant-a",
            "attachment_checklist": ({"name": "budget", "complete": True}, {"name": "narrative", "complete": True}),
            "final_signoff": True,
        },
    )
    review = manage_review_chain(
        workspace["state"],
        {
            "entity_type": "grant_application",
            "entity_id": "grant-a",
            "required_roles": ("program", "finance"),
            "completed_roles": ("program", "finance"),
            "status": "approved",
        },
    )
    validation = validate_grant_budget(
        review["state"],
        {
            "grant_application_id": "grant-a",
            "restriction_id": "rest-a",
            "approvals": ("finance",),
            "period": "fy26",
        },
    )
    score = score_fundraising_opportunity(
        validation["state"],
        {"donor_id": "donor-a", "grant_application_id": "grant-a", "potential_value": 100000, "likelihood": 0.6, "urgency": 0.5, "delivery_risk": 0.2},
    )
    packet = generate_briefing_packet(score["state"], {"generated_for_date": "2026-06-15"})

    assert workspace["ok"] is True
    assert review["ok"] is True
    assert validation["ok"] is True
    assert score["opportunity_score"]["priority_score"] > 0
    assert len(packet["briefing_packet"]["grant_pipeline_summary"]) == 1


def test_relationship_acknowledgement_and_workbench_queues_surface_operating_backlog():
    state = empty_fundraising_state()
    donor = register_donor_profile(state, {"donor_id": "donor-a", "donor_type": "individual", "recognition_preference": "public", "next_action_date": "2026-06-01"})
    related = register_donor_profile(donor["state"], {"donor_id": "donor-b", "donor_type": "household", "recognition_preference": "public"})
    relationship = map_donor_relationship(related["state"], {"donor_id": "donor-a", "related_donor_id": "donor-b", "relationship_type": "household"})
    gift = post_gift(relationship["state"], {"gift_id": "gift-a", "donor_id": "donor-a", "amount": 100})
    acknowledgement = track_acknowledgement(gift["state"], {"donor_id": "donor-a", "gift_id": "gift-a", "channel": "email", "status": "queued"})
    stewardship = record_stewardship_touchpoint(acknowledgement["state"], {"donor_id": "donor-a", "requires_acknowledgement": True, "cadence_overdue": True})
    workbench = build_fundraising_workbench(stewardship["state"])

    assert relationship["ok"] is True
    assert acknowledgement["ok"] is True
    assert stewardship["ok"] is False
    assert workbench["queue_counts"]["portfolio_next_actions"] == 1
    assert workbench["queue_counts"]["acknowledgement_backlog"] >= 1
    assert workbench["queue_counts"]["stewardship_gaps"] == 1
    assert workbench["queue_counts"]["exception_backlog"] >= 1


def test_agent_document_plan_is_stable_and_domain_routed():
    first = document_instruction_plan("grant guidelines", "prepare proposal")
    second = document_instruction_plan("grant guidelines", "prepare proposal")
    gift = document_instruction_plan("donation receipt letter", "post gift")
    briefing = document_instruction_plan("leadership board packet", "prepare the board briefing")

    assert first["document_digest"] == second["document_digest"]
    assert first["domain_plan"]["target_table"] == "donor_grant_fundraising_grant_application"
    assert gift["domain_plan"]["proposed_operation"] == "post_gift"
    assert briefing["domain_plan"]["target_table"] == "donor_grant_fundraising_briefing_packet"
    assert first["requires_human_confirmation"] is True


def test_stateful_service_executes_domain_app_commands_and_queries():
    service = DonorGrantFundraisingService()
    donor = service.register_donor_profile({"donor_id": "donor-svc", "donor_type": "foundation", "recognition_preference": "named"})
    campaign = service.create_campaign({"campaign_id": "camp-svc", "goal_amount": 500})
    workbench = service.build_fundraising_workbench({})
    view = service.build_workbench_view({"tenant": "tenant-svc"})

    assert donor["ok"] is True
    assert campaign["ok"] is True
    assert workbench["ok"] is True
    assert view["ok"] is True
    assert "donor-svc" in service.state["donors"]
    assert "camp-svc" in service.state["campaigns"]


def test_fundraising_app_smoke_covers_end_to_end_flow():
    assert fundraising_app_smoke_test()["ok"] is True
