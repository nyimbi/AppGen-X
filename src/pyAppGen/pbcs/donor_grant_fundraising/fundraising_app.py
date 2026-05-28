"""Standalone donor, grant, and fundraising app surface."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256

PBC_KEY = "donor_grant_fundraising"
OWNED_TABLES = (
    "donor_grant_fundraising_donor",
    "donor_grant_fundraising_campaign",
    "donor_grant_fundraising_pledge",
    "donor_grant_fundraising_gift",
    "donor_grant_fundraising_restriction",
    "donor_grant_fundraising_grant_application",
    "donor_grant_fundraising_stewardship_touchpoint",
    "donor_grant_fundraising_donor_relationship",
    "donor_grant_fundraising_proposal_workspace",
    "donor_grant_fundraising_acknowledgement",
    "donor_grant_fundraising_briefing_packet",
    "donor_grant_fundraising_opportunity_score",
    "donor_grant_fundraising_review_chain",
    "donor_grant_fundraising_budget_validation",
)
PROSPECT_STAGES = (
    "identified",
    "researched",
    "qualified",
    "assigned",
    "cultivated",
    "solicitation_ready",
    "converted",
)
PLEDGE_STATES = (
    "draft",
    "pending_confirmation",
    "active",
    "partially_paid",
    "fulfilled",
    "overdue",
    "amended",
    "cancelled",
    "written_off",
)
GRANT_STAGES = (
    "identified",
    "researching",
    "qualified",
    "drafting",
    "internal_review",
    "submitted",
    "declined",
    "awarded",
    "closed",
)


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def empty_fundraising_state() -> dict:
    return {
        "donors": {},
        "campaigns": {},
        "pledges": {},
        "gifts": {},
        "restrictions": {},
        "grant_applications": {},
        "stewardship": {},
        "exceptions": {},
        "outbox": [],
    }


def _copy_state(state: dict) -> dict:
    return deepcopy(state)


def _emit(state: dict, event_type: str, payload: dict) -> None:
    state["outbox"].append(
        {
            "event_type": event_type,
            "event_contract": "AppGen-X",
            "topic": "pbc.donor_grant_fundraising.events",
            "payload": dict(payload),
            "idempotency_key": _digest((event_type, payload)),
        }
    )


def register_donor_profile(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    donor_id = payload.get("donor_id") or f"donor-{_digest((payload.get('name'), payload.get('donor_type')))[:8]}"
    donor_type = payload.get("donor_type", "individual")
    blockers = []
    if donor_type not in {"individual", "household", "corporate", "foundation"}:
        blockers.append("unsupported_donor_type")
    if not payload.get("recognition_preference"):
        blockers.append("recognition_preference_missing")
    donor = {
        "id": donor_id,
        "table": "donor_grant_fundraising_donor",
        "name": payload.get("name", donor_id),
        "donor_type": donor_type,
        "relationship_stage": payload.get("relationship_stage", "identified"),
        "preferred_channels": tuple(payload.get("preferred_channels", ())),
        "funding_interests": tuple(payload.get("funding_interests", ())),
        "recognition_preference": payload.get("recognition_preference"),
        "restriction_preferences": tuple(payload.get("restriction_preferences", ())),
        "compliance_requirements": tuple(payload.get("compliance_requirements", ())),
        "household_or_org_links": tuple(payload.get("household_or_org_links", ())),
        "owner": payload.get("owner"),
        "next_action_date": payload.get("next_action_date"),
        "blockers": tuple(blockers),
    }
    next_state["donors"][donor_id] = donor
    _emit(next_state, "DonorGrantFundraisingExceptionOpened" if blockers else "DonorGrantFundraisingCreated", {"entity": "donor", "id": donor_id, "blockers": tuple(blockers)})
    return {"ok": not blockers, "state": next_state, "donor": donor, "side_effects": ()}


def advance_prospect_stage(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    donor = next_state["donors"].get(payload.get("donor_id"))
    if donor is None:
        return {"ok": False, "state": next_state, "reason": "donor_missing", "side_effects": ()}
    current = donor.get("relationship_stage", "identified")
    target = payload.get("target_stage")
    blockers = []
    if target not in PROSPECT_STAGES:
        blockers.append("unknown_stage")
    elif PROSPECT_STAGES.index(target) > PROSPECT_STAGES.index(current) + 1 and not payload.get("override_approved"):
        blockers.append("stage_skip_requires_approval")
    if target in {"qualified", "solicitation_ready", "converted"} and not payload.get("qualification_evidence"):
        blockers.append("qualification_evidence_missing")
    if not blockers:
        donor["relationship_stage"] = target
        donor["qualification_evidence"] = tuple(payload.get("qualification_evidence", ()))
    _emit(next_state, "DonorGrantFundraisingExceptionOpened" if blockers else "DonorGrantFundraisingUpdated", {"entity": "donor", "id": donor["id"], "target_stage": target, "blockers": tuple(blockers)})
    return {"ok": not blockers, "state": next_state, "donor": donor, "blockers": tuple(blockers), "side_effects": ()}


def create_campaign(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    campaign_id = payload.get("campaign_id") or f"camp-{_digest((payload.get('name'), payload.get('start_date')))[:8]}"
    campaign = {
        "id": campaign_id,
        "table": "donor_grant_fundraising_campaign",
        "name": payload.get("name", campaign_id),
        "parent_campaign_id": payload.get("parent_campaign_id"),
        "objective_category": payload.get("objective_category", "annual_fund"),
        "goal_amount": float(payload.get("goal_amount", 0.0)),
        "target_segments": tuple(payload.get("target_segments", ())),
        "start_date": payload.get("start_date"),
        "end_date": payload.get("end_date"),
        "gift_counting_rules": tuple(payload.get("gift_counting_rules", ("posted_gifts",))),
        "linked_grant_themes": tuple(payload.get("linked_grant_themes", ())),
        "current_amount": 0.0,
    }
    next_state["campaigns"][campaign_id] = campaign
    _emit(next_state, "DonorGrantFundraisingCreated", {"entity": "campaign", "id": campaign_id})
    return {"ok": True, "state": next_state, "campaign": campaign, "side_effects": ()}


def create_pledge(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    pledge_id = payload.get("pledge_id") or f"pledge-{_digest((payload.get('donor_id'), payload.get('amount')))[:8]}"
    amount = float(payload.get("amount", 0.0))
    paid = float(payload.get("paid_amount", 0.0))
    status = payload.get("status", "active")
    blockers = []
    if status not in PLEDGE_STATES:
        blockers.append("unknown_pledge_state")
    if amount <= 0:
        blockers.append("pledge_amount_required")
    if payload.get("installments") and round(sum(float(item.get("amount", 0.0)) for item in payload["installments"]), 2) != round(amount, 2):
        blockers.append("installments_do_not_match_pledge_amount")
    pledge = {
        "id": pledge_id,
        "table": "donor_grant_fundraising_pledge",
        "donor_id": payload.get("donor_id"),
        "campaign_id": payload.get("campaign_id"),
        "amount": amount,
        "paid_amount": paid,
        "remaining_balance": max(0.0, amount - paid),
        "status": status if not blockers else "draft",
        "installments": tuple(payload.get("installments", ())),
        "reminder_dates": tuple(payload.get("reminder_dates", ())),
        "amendment_reason": payload.get("amendment_reason"),
        "blockers": tuple(blockers),
    }
    next_state["pledges"][pledge_id] = pledge
    _emit(next_state, "DonorGrantFundraisingExceptionOpened" if blockers else "DonorGrantFundraisingCreated", {"entity": "pledge", "id": pledge_id, "blockers": tuple(blockers)})
    return {"ok": not blockers, "state": next_state, "pledge": pledge, "side_effects": ()}


def create_restriction(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    restriction_id = payload.get("restriction_id") or f"restr-{_digest((payload.get('purpose_code'), payload.get('time_window')))[:8]}"
    required = ("restriction_type", "purpose_code")
    blockers = tuple(f"{field}_missing" for field in required if not payload.get(field))
    restriction = {
        "id": restriction_id,
        "table": "donor_grant_fundraising_restriction",
        "restriction_type": payload.get("restriction_type"),
        "purpose_code": payload.get("purpose_code"),
        "geography": payload.get("geography"),
        "time_window": payload.get("time_window"),
        "beneficiary_class": payload.get("beneficiary_class"),
        "required_approvals": tuple(payload.get("required_approvals", ())),
        "release_conditions": tuple(payload.get("release_conditions", ())),
        "sunset_date": payload.get("sunset_date"),
        "blockers": blockers,
    }
    next_state["restrictions"][restriction_id] = restriction
    _emit(next_state, "DonorGrantFundraisingExceptionOpened" if blockers else "DonorGrantFundraisingCreated", {"entity": "restriction", "id": restriction_id, "blockers": blockers})
    return {"ok": not blockers, "state": next_state, "restriction": restriction, "side_effects": ()}


def post_gift(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    gift_id = payload.get("gift_id") or f"gift-{_digest((payload.get('donor_id'), payload.get('amount'), payload.get('posting_date')))[:8]}"
    amount = float(payload.get("amount", 0.0))
    pledge = next_state["pledges"].get(payload.get("pledge_id"))
    campaign = next_state["campaigns"].get(payload.get("campaign_id"))
    restriction = next_state["restrictions"].get(payload.get("restriction_id"))
    blockers = []
    if amount <= 0:
        blockers.append("gift_amount_required")
    if payload.get("pledge_id") and pledge is None:
        blockers.append("pledge_not_found")
    if payload.get("campaign_id") and campaign is None:
        blockers.append("campaign_not_found")
    if payload.get("restriction_id") and restriction is None:
        blockers.append("restriction_not_found")
    if restriction and payload.get("purpose_code") and payload["purpose_code"] != restriction.get("purpose_code"):
        blockers.append("restriction_purpose_mismatch")
    if pledge:
        pledge["paid_amount"] = round(float(pledge.get("paid_amount", 0.0)) + amount, 2)
        pledge["remaining_balance"] = max(0.0, round(float(pledge["amount"]) - pledge["paid_amount"], 2))
        pledge["status"] = "fulfilled" if pledge["remaining_balance"] == 0 else "partially_paid"
    if campaign:
        campaign["current_amount"] = round(float(campaign.get("current_amount", 0.0)) + amount, 2)
    gift = {
        "id": gift_id,
        "table": "donor_grant_fundraising_gift",
        "donor_id": payload.get("donor_id"),
        "campaign_id": payload.get("campaign_id"),
        "pledge_id": payload.get("pledge_id"),
        "restriction_id": payload.get("restriction_id"),
        "amount": amount,
        "appeal_source": payload.get("appeal_source"),
        "receipt_status": "blocked" if blockers else payload.get("receipt_status", "receipt_due"),
        "posting_date": payload.get("posting_date"),
        "blockers": tuple(blockers),
    }
    next_state["gifts"][gift_id] = gift
    _emit(next_state, "DonorGrantFundraisingExceptionOpened" if blockers else "DonorGrantFundraisingApproved", {"entity": "gift", "id": gift_id, "blockers": tuple(blockers)})
    return {"ok": not blockers, "state": next_state, "gift": gift, "pledge": pledge, "campaign": campaign, "side_effects": ()}


def manage_grant_application(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    grant_id = payload.get("grant_application_id") or f"grant-{_digest((payload.get('funder_id'), payload.get('deadline')))[:8]}"
    stage = payload.get("stage", "identified")
    blockers = []
    if stage not in GRANT_STAGES:
        blockers.append("unknown_grant_stage")
    if stage in {"submitted", "awarded"} and not payload.get("proposal_complete"):
        blockers.append("proposal_incomplete")
    if stage == "submitted" and not payload.get("review_signoffs"):
        blockers.append("internal_review_missing")
    if stage == "awarded" and not payload.get("post_award_setup"):
        blockers.append("post_award_setup_missing")
    grant = {
        "id": grant_id,
        "table": "donor_grant_fundraising_grant_application",
        "funder_id": payload.get("funder_id"),
        "stage": stage if not blockers else "internal_review",
        "fit_score": float(payload.get("fit_score", 0.0)),
        "strategic_priority": payload.get("strategic_priority"),
        "deadline": payload.get("deadline"),
        "deadline_confidence": float(payload.get("deadline_confidence", 0.0)),
        "proposal_workspace": dict(payload.get("proposal_workspace", {})),
        "budget": dict(payload.get("budget", {})),
        "review_signoffs": tuple(payload.get("review_signoffs", ())),
        "post_award_setup": tuple(payload.get("post_award_setup", ())),
        "blockers": tuple(blockers),
    }
    next_state["grant_applications"][grant_id] = grant
    _emit(next_state, "DonorGrantFundraisingExceptionOpened" if blockers else "DonorGrantFundraisingUpdated", {"entity": "grant_application", "id": grant_id, "stage": grant["stage"], "blockers": tuple(blockers)})
    return {"ok": not blockers, "state": next_state, "grant_application": grant, "side_effects": ()}


def record_stewardship_touchpoint(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    touchpoint_id = payload.get("touchpoint_id") or f"stew-{_digest((payload.get('donor_id'), payload.get('date'), payload.get('playbook_type')))[:8]}"
    blockers = []
    if payload.get("requires_acknowledgement") and not payload.get("acknowledgement_status"):
        blockers.append("acknowledgement_status_missing")
    if payload.get("cadence_overdue"):
        blockers.append("stewardship_cadence_missed")
    touchpoint = {
        "id": touchpoint_id,
        "table": "donor_grant_fundraising_stewardship_touchpoint",
        "donor_id": payload.get("donor_id"),
        "playbook_type": payload.get("playbook_type", "general"),
        "expected_cadence": payload.get("expected_cadence"),
        "outcome": payload.get("outcome"),
        "next_ask_readiness": payload.get("next_ask_readiness", "unknown"),
        "segment": payload.get("segment"),
        "acknowledgement_status": payload.get("acknowledgement_status"),
        "blockers": tuple(blockers),
    }
    next_state["stewardship"][touchpoint_id] = touchpoint
    _emit(next_state, "DonorGrantFundraisingExceptionOpened" if blockers else "DonorGrantFundraisingUpdated", {"entity": "stewardship_touchpoint", "id": touchpoint_id, "blockers": tuple(blockers)})
    return {"ok": not blockers, "state": next_state, "stewardship_touchpoint": touchpoint, "side_effects": ()}


def build_fundraising_workbench(state: dict) -> dict:
    donors = tuple(state.get("donors", {}).values())
    pledges = tuple(state.get("pledges", {}).values())
    gifts = tuple(state.get("gifts", {}).values())
    grants = tuple(state.get("grant_applications", {}).values())
    stewardship = tuple(state.get("stewardship", {}).values())
    campaigns = tuple(state.get("campaigns", {}).values())
    queues = {
        "portfolio_next_actions": tuple(donor for donor in donors if donor.get("next_action_date")),
        "pledge_exposure": tuple(pledge for pledge in pledges if pledge.get("remaining_balance", 0.0) > 0),
        "acknowledgement_backlog": tuple(gift for gift in gifts if gift.get("receipt_status") in {"receipt_due", "blocked"}),
        "grant_deadline_risk": tuple(grant for grant in grants if grant.get("deadline_confidence", 1.0) < 0.75 or grant.get("blockers")),
        "stewardship_gaps": tuple(item for item in stewardship if item.get("blockers")),
        "campaign_performance": tuple({"campaign_id": campaign["id"], "goal_amount": campaign["goal_amount"], "current_amount": campaign["current_amount"]} for campaign in campaigns),
        "exception_backlog": tuple(item for item in donors + pledges + gifts + grants + stewardship if item.get("blockers")),
    }
    return {"ok": True, "pbc": PBC_KEY, "queues": queues, "queue_counts": {key: len(value) for key, value in queues.items()}, "side_effects": ()}


def forms_contract() -> dict:
    forms = (
        {"form_id": "donor_profile_form", "writes_table": "donor_grant_fundraising_donor", "command": "register_donor_profile"},
        {"form_id": "prospect_stage_form", "writes_table": "donor_grant_fundraising_donor", "command": "advance_prospect_stage"},
        {"form_id": "campaign_hierarchy_form", "writes_table": "donor_grant_fundraising_campaign", "command": "create_campaign"},
        {"form_id": "pledge_installment_form", "writes_table": "donor_grant_fundraising_pledge", "command": "create_pledge"},
        {"form_id": "gift_posting_form", "writes_table": "donor_grant_fundraising_gift", "command": "post_gift"},
        {"form_id": "restriction_rule_form", "writes_table": "donor_grant_fundraising_restriction", "command": "create_restriction"},
        {"form_id": "grant_application_form", "writes_table": "donor_grant_fundraising_grant_application", "command": "manage_grant_application"},
        {"form_id": "stewardship_touchpoint_form", "writes_table": "donor_grant_fundraising_stewardship_touchpoint", "command": "record_stewardship_touchpoint"},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def wizards_contract() -> dict:
    wizards = (
        {"wizard_id": "donor_conversion_wizard", "steps": ("register_profile", "research", "qualify", "assign_owner", "convert")},
        {"wizard_id": "major_gift_wizard", "steps": ("select_campaign", "create_pledge", "schedule_installments", "record_gift", "acknowledge")},
        {"wizard_id": "restriction_setup_wizard", "steps": ("capture_intent", "code_restriction", "validate_use", "approve_release_rules")},
        {"wizard_id": "grant_submission_wizard", "steps": ("qualify_opportunity", "complete_proposal", "collect_reviews", "validate_budget", "submit")},
        {"wizard_id": "post_award_setup_wizard", "steps": ("review_award", "create_restrictions", "assign_reporting", "schedule_stewardship")},
        {"wizard_id": "single_pbc_launch_wizard", "steps": ("configure_database", "seed_campaigns", "open_workbench", "invite_roles")},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def controls_contract() -> dict:
    controls = (
        {"control_id": "prospect_stage_gate", "blocks_on_failure": True, "table_scope": ("donor_grant_fundraising_donor",)},
        {"control_id": "pledge_installment_reconciliation_gate", "blocks_on_failure": True, "table_scope": ("donor_grant_fundraising_pledge",)},
        {"control_id": "gift_pledge_campaign_matching_gate", "blocks_on_failure": True, "table_scope": ("donor_grant_fundraising_gift", "donor_grant_fundraising_pledge", "donor_grant_fundraising_campaign")},
        {"control_id": "restriction_purpose_time_approval_gate", "blocks_on_failure": True, "table_scope": ("donor_grant_fundraising_restriction", "donor_grant_fundraising_gift")},
        {"control_id": "grant_submission_review_gate", "blocks_on_failure": True, "table_scope": ("donor_grant_fundraising_grant_application",)},
        {"control_id": "acknowledgement_sla_gate", "blocks_on_failure": True, "table_scope": ("donor_grant_fundraising_gift", "donor_grant_fundraising_stewardship_touchpoint")},
        {"control_id": "assistant_mutation_confirmation_gate", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "database_backed": True,
        "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
        "owned_tables": OWNED_TABLES,
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "workbench": "DonorGrantFundraisingWorkbench",
        "assistant_panel": "DonorGrantFundraisingAssistantPanel",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def document_instruction_mutation_plan(document: str, instruction: str) -> dict:
    text = f"{document} {instruction}".lower()
    if "grant" in text or "proposal" in text or "award" in text:
        operation = "manage_grant_application"
        table = "donor_grant_fundraising_grant_application"
    elif "pledge" in text or "installment" in text:
        operation = "create_pledge"
        table = "donor_grant_fundraising_pledge"
    elif "gift" in text or "donation" in text or "receipt" in text:
        operation = "post_gift"
        table = "donor_grant_fundraising_gift"
    elif "restriction" in text or "restricted" in text or "purpose" in text:
        operation = "create_restriction"
        table = "donor_grant_fundraising_restriction"
    elif "stewardship" in text or "thank" in text or "acknowledgement" in text:
        operation = "record_stewardship_touchpoint"
        table = "donor_grant_fundraising_stewardship_touchpoint"
    elif "campaign" in text or "appeal" in text:
        operation = "create_campaign"
        table = "donor_grant_fundraising_campaign"
    else:
        operation = "register_donor_profile"
        table = "donor_grant_fundraising_donor"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "proposed_operation": operation,
        "target_table": table,
        "requires_human_confirmation": True,
        "requires_citations": True,
        "crud_datastore_mutation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def fundraising_app_smoke_test() -> dict:
    state = empty_fundraising_state()
    donor = register_donor_profile(
        state,
        {
            "donor_id": "donor-1",
            "name": "Evergreen Foundation",
            "donor_type": "foundation",
            "recognition_preference": "named_report",
            "funding_interests": ("health", "education"),
            "next_action_date": "2026-06-01",
        },
    )
    stage = advance_prospect_stage(donor["state"], {"donor_id": "donor-1", "target_stage": "researched"})
    campaign = create_campaign(stage["state"], {"campaign_id": "camp-1", "name": "Annual Impact", "goal_amount": 100000})
    pledge = create_pledge(campaign["state"], {"pledge_id": "pledge-1", "donor_id": "donor-1", "campaign_id": "camp-1", "amount": 1000, "installments": ({"amount": 500}, {"amount": 500})})
    restriction = create_restriction(pledge["state"], {"restriction_id": "rest-1", "restriction_type": "purpose", "purpose_code": "health"})
    gift = post_gift(restriction["state"], {"gift_id": "gift-1", "donor_id": "donor-1", "campaign_id": "camp-1", "pledge_id": "pledge-1", "restriction_id": "rest-1", "purpose_code": "health", "amount": 500})
    grant = manage_grant_application(gift["state"], {"grant_application_id": "grant-1", "funder_id": "donor-1", "stage": "submitted", "proposal_complete": True, "review_signoffs": ("program", "finance"), "deadline_confidence": 0.9})
    stewardship = record_stewardship_touchpoint(grant["state"], {"donor_id": "donor-1", "playbook_type": "foundation", "requires_acknowledgement": True, "acknowledgement_status": "complete"})
    workbench = build_fundraising_workbench(stewardship["state"])
    checks = (
        donor["ok"],
        stage["ok"],
        campaign["ok"],
        pledge["ok"],
        restriction["ok"],
        gift["ok"],
        grant["ok"],
        stewardship["ok"],
        workbench["ok"],
        single_pbc_app_contract()["ok"],
        document_instruction_mutation_plan("grant proposal guideline", "prepare submission")["target_table"] == "donor_grant_fundraising_grant_application",
    )
    return {"ok": all(checks), "state": stewardship["state"], "workbench": workbench, "single_pbc_app": single_pbc_app_contract(), "side_effects": ()}
