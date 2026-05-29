"""Standalone one-PBC application surface for donor_grant_fundraising."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from . import agent
from . import runtime
from . import ui
from .fundraising_app import (
    advance_prospect_stage,
    build_fundraising_workbench,
    compose_proposal_workspace,
    create_campaign,
    create_pledge,
    create_restriction,
    empty_fundraising_state,
    generate_briefing_packet,
    manage_grant_application,
    manage_review_chain,
    map_donor_relationship,
    post_gift,
    record_stewardship_touchpoint,
    register_donor_profile,
    score_fundraising_opportunity,
    track_acknowledgement,
    validate_grant_budget,
)

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_policy": "fundraising-default",
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.8,
    "materiality_threshold": 1000,
    "approval_sla_hours": 48,
    "risk_threshold": 0.65,
    "forecast_horizon_days": 180,
    "workbench_limit": 100,
}
DEFAULT_RULES = (
    {
        "rule_id": "donor_grant_fundraising.donor.default",
        "scope": "donor",
        "status": "active",
        "requires_recognition_preference": True,
        "requires_owner_before_conversion": True,
    },
    {
        "rule_id": "donor_grant_fundraising.grant_submission.default",
        "scope": "grant_submission",
        "status": "active",
        "required_review_roles": ("program", "finance"),
        "requires_budget_validation": True,
    },
)
DEFAULT_SEED_PACK = {
    "donor": {
        "donor_id": "seed-foundation",
        "name": "Evergreen Foundation",
        "donor_type": "foundation",
        "recognition_preference": "named_report",
        "funding_interests": ("health", "education"),
        "next_action_date": "2026-06-15",
    },
    "campaign": {
        "campaign_id": "seed-campaign",
        "name": "2026 Leadership Giving",
        "objective_category": "leadership_giving",
        "goal_amount": 250000,
        "target_segments": ("major_donor", "foundation"),
    },
    "restriction": {
        "restriction_id": "seed-restriction",
        "restriction_type": "purpose",
        "purpose_code": "education",
        "required_approvals": ("finance",),
        "time_window": "fy26",
    },
}


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": runtime.PBC_KEY,
        "app_class": "DonorGrantFundraisingStandaloneApplication",
        "implementation_directory": "src/pyAppGen/pbcs/donor_grant_fundraising",
        "service_methods": (
            "configure",
            "register_defaults",
            "seed_demo_data",
            "register_donor_profile",
            "advance_prospect_stage",
            "create_campaign",
            "create_pledge",
            "create_restriction",
            "post_gift",
            "manage_grant_application",
            "record_stewardship_touchpoint",
            "map_donor_relationship",
            "compose_proposal_workspace",
            "track_acknowledgement",
            "generate_briefing_packet",
            "score_fundraising_opportunity",
            "manage_review_chain",
            "validate_grant_budget",
            "receive_event",
            "document_intake",
            "crud_mutation_plan",
            "workbench",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench"),
        "docs": ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md"),
        "event_contract": "AppGen-X",
        "event_topic": runtime.DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_backends": runtime.DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS,
    }


class DonorGrantFundraisingStandaloneApplication:
    """Mutable, package-local fundraising shell for one-PBC usage."""

    def __init__(self, *, tenant: str = "default", state: dict[str, Any] | None = None) -> None:
        self.tenant = tenant
        self.state = deepcopy(state or empty_fundraising_state())
        self.runtime_state = runtime.donor_grant_fundraising_empty_state()

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.state)

    def configure(self, configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        candidate = {**DEFAULT_CONFIGURATION, **_copy_payload(configuration)}
        result = runtime.donor_grant_fundraising_configure_runtime(self.runtime_state, candidate)
        self.runtime_state = result["state"]
        return {**result, "state": self.snapshot()}

    def register_defaults(self) -> dict[str, Any]:
        if not self.runtime_state.get("configuration", {}).get("ok"):
            self.configure()
        parameter_results = []
        for key, value in DEFAULT_PARAMETERS.items():
            parameter_results.append(runtime.donor_grant_fundraising_set_parameter(self.runtime_state, key, value))
            self.runtime_state = parameter_results[-1]["state"]
        rule_results = []
        for rule in DEFAULT_RULES:
            rule_results.append(runtime.donor_grant_fundraising_register_rule(self.runtime_state, rule))
            self.runtime_state = rule_results[-1]["state"]
        return {
            "ok": all(item["ok"] for item in parameter_results + rule_results),
            "state": self.snapshot(),
            "parameters": tuple(item["parameter"] for item in parameter_results),
            "rules": tuple(item["rule"] for item in rule_results),
        }

    def seed_demo_data(self) -> dict[str, Any]:
        donor = self.register_donor_profile(DEFAULT_SEED_PACK["donor"])
        campaign = self.create_campaign(DEFAULT_SEED_PACK["campaign"])
        restriction = self.create_restriction(DEFAULT_SEED_PACK["restriction"])
        return {
            "ok": donor["ok"] and campaign["ok"] and restriction["ok"],
            "state": self.snapshot(),
            "donor": donor.get("donor"),
            "campaign": campaign.get("campaign"),
            "restriction": restriction.get("restriction"),
        }

    def _apply(self, handler, payload: dict[str, Any]) -> dict[str, Any]:
        result = handler(self.state, payload)
        self.state = result["state"]
        return {**result, "state": self.snapshot()}

    def register_donor_profile(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(register_donor_profile, {"tenant": self.tenant, **_copy_payload(payload)})

    def advance_prospect_stage(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(advance_prospect_stage, {"tenant": self.tenant, **_copy_payload(payload)})

    def create_campaign(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(create_campaign, {"tenant": self.tenant, **_copy_payload(payload)})

    def create_pledge(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(create_pledge, {"tenant": self.tenant, **_copy_payload(payload)})

    def create_restriction(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(create_restriction, {"tenant": self.tenant, **_copy_payload(payload)})

    def post_gift(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(post_gift, {"tenant": self.tenant, **_copy_payload(payload)})

    def manage_grant_application(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(manage_grant_application, {"tenant": self.tenant, **_copy_payload(payload)})

    def record_stewardship_touchpoint(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(record_stewardship_touchpoint, {"tenant": self.tenant, **_copy_payload(payload)})

    def map_donor_relationship(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(map_donor_relationship, {"tenant": self.tenant, **_copy_payload(payload)})

    def compose_proposal_workspace(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(compose_proposal_workspace, {"tenant": self.tenant, **_copy_payload(payload)})

    def track_acknowledgement(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(track_acknowledgement, {"tenant": self.tenant, **_copy_payload(payload)})

    def generate_briefing_packet(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(generate_briefing_packet, {"tenant": self.tenant, **_copy_payload(payload)})

    def score_fundraising_opportunity(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(score_fundraising_opportunity, {"tenant": self.tenant, **_copy_payload(payload)})

    def manage_review_chain(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(manage_review_chain, {"tenant": self.tenant, **_copy_payload(payload)})

    def validate_grant_budget(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._apply(validate_grant_budget, {"tenant": self.tenant, **_copy_payload(payload)})

    def receive_event(self, event: dict[str, Any]) -> dict[str, Any]:
        result = runtime.donor_grant_fundraising_receive_event(self.runtime_state, {"tenant": self.tenant, **_copy_payload(event)})
        self.runtime_state = result["state"]
        return {**result, "state": self.snapshot()}

    def document_intake(self, document: str, instruction: str) -> dict[str, Any]:
        plan = agent.document_instruction_plan(document, instruction)
        return {"ok": plan["ok"], "plan": plan, "state": self.snapshot()}

    def crud_mutation_plan(self, *, action_name: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return agent.datastore_crud_plan(action_name, table=table, payload=payload)

    def workbench(self, *, tenant: str | None = None) -> dict[str, Any]:
        rendered = build_fundraising_workbench(self.state)
        rendered["ui_contract"] = ui.donor_grant_fundraising_render_workbench()
        rendered["tenant"] = tenant or self.tenant
        rendered["standalone"] = {
            "proposal_workspaces": tuple(self.state.get("proposal_workspaces", {}).values()),
            "acknowledgements": tuple(self.state.get("acknowledgements", {}).values()),
            "briefing_packets": tuple(self.state.get("briefing_packets", {}).values()),
            "opportunity_scores": tuple(self.state.get("opportunity_scores", {}).values()),
            "review_chains": tuple(self.state.get("review_chains", {}).values()),
            "budget_validations": tuple(self.state.get("budget_validations", {}).values()),
        }
        return rendered


def standalone_smoke_test() -> dict[str, Any]:
    app = DonorGrantFundraisingStandaloneApplication(tenant="tenant_alpha")
    configuration = app.configure()
    defaults = app.register_defaults()
    seeds = app.seed_demo_data()
    app.advance_prospect_stage({"donor_id": "seed-foundation", "target_stage": "researched", "qualification_evidence": ("research-complete",)})
    pledge = app.create_pledge(
        {
            "pledge_id": "pledge-100",
            "donor_id": "seed-foundation",
            "campaign_id": "seed-campaign",
            "amount": 10000,
            "installments": ({"amount": 5000}, {"amount": 5000}),
        }
    )
    gift = app.post_gift(
        {
            "gift_id": "gift-100",
            "donor_id": "seed-foundation",
            "campaign_id": "seed-campaign",
            "pledge_id": "pledge-100",
            "restriction_id": "seed-restriction",
            "purpose_code": "education",
            "amount": 5000,
        }
    )
    grant = app.manage_grant_application(
        {
            "grant_application_id": "grant-100",
            "funder_id": "seed-foundation",
            "stage": "submitted",
            "proposal_complete": True,
            "review_signoffs": ("program", "finance"),
            "budget": {"purpose_code": "education", "line_items": ({"amount": 7000}, {"amount": 3000})},
            "deadline_confidence": 0.9,
        }
    )
    workspace = app.compose_proposal_workspace(
        {
            "grant_application_id": "grant-100",
            "attachment_checklist": ({"name": "budget", "complete": True}, {"name": "narrative", "complete": True}),
            "final_signoff": True,
        }
    )
    review = app.manage_review_chain(
        {
            "entity_type": "grant_application",
            "entity_id": "grant-100",
            "required_roles": ("program", "finance"),
            "completed_roles": ("program", "finance"),
            "status": "approved",
        }
    )
    validation = app.validate_grant_budget(
        {
            "grant_application_id": "grant-100",
            "restriction_id": "seed-restriction",
            "approvals": ("finance",),
            "period": "fy26",
        }
    )
    acknowledgement = app.track_acknowledgement({"donor_id": "seed-foundation", "gift_id": "gift-100", "channel": "email", "status": "sent"})
    stewardship = app.record_stewardship_touchpoint({"donor_id": "seed-foundation", "playbook_type": "foundation", "acknowledgement_status": "complete", "requires_acknowledgement": True})
    relationship = app.map_donor_relationship({"donor_id": "seed-foundation", "related_donor_id": "seed-foundation", "relationship_type": "household_anchor"})
    score = app.score_fundraising_opportunity({"donor_id": "seed-foundation", "grant_application_id": "grant-100", "potential_value": 250000, "likelihood": 0.7, "urgency": 0.4, "delivery_risk": 0.2})
    packet = app.generate_briefing_packet({"generated_for_date": "2026-06-15"})
    document = app.document_intake("grant proposal for education", "prepare review checklist")
    crud = app.crud_mutation_plan(action_name="create", table="donor_grant_fundraising_acknowledgement", payload={"gift_id": "gift-100"})
    workbench = app.workbench(tenant="tenant_alpha")
    return {
        "ok": configuration["ok"] and defaults["ok"] and seeds["ok"] and pledge["ok"] and gift["ok"] and grant["ok"] and workspace["ok"] and review["ok"] and validation["ok"] and acknowledgement["ok"] and stewardship["ok"] and relationship["ok"] and score["ok"] and packet["ok"] and document["ok"] and crud["ok"] and workbench["ok"],
        "manifest": standalone_manifest(),
        "state": app.snapshot(),
        "workbench": workbench,
        "document": document["plan"],
    }
