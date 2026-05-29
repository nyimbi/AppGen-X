"""Standalone one-PBC application composition for loyalty_rewards."""

from __future__ import annotations

from . import agent
from . import events
from . import permissions
from . import routes
from . import seed_data
from . import services
from . import ui
from .manifest import PBC_MANIFEST
from .runtime import loyalty_rewards_adjust_points
from .runtime import loyalty_rewards_build_release_evidence
from .runtime import loyalty_rewards_build_workbench_view
from .runtime import loyalty_rewards_create_redemption
from .runtime import loyalty_rewards_empty_state
from .runtime import loyalty_rewards_evaluate_offer_eligibility
from .runtime import loyalty_rewards_forecast_breakage
from .runtime import loyalty_rewards_generate_balance_proof
from .runtime import loyalty_rewards_issue_points
from .runtime import loyalty_rewards_qualify_tier
from .runtime import loyalty_rewards_reconcile_balance
from .runtime import loyalty_rewards_register_earning_rule
from .runtime import loyalty_rewards_register_governed_model
from .runtime import loyalty_rewards_register_rule
from .runtime import loyalty_rewards_review_fraud_risk
from .runtime import loyalty_rewards_run_liability_controls
from .runtime import loyalty_rewards_schedule_expiration
from .runtime import loyalty_rewards_screen_rewards_policy
from .runtime import loyalty_rewards_set_parameter
from .runtime import loyalty_rewards_simulate_offer
from .runtime import loyalty_rewards_snapshot_liability
from .runtime import loyalty_rewards_configure_runtime
from .runtime import loyalty_rewards_enroll_member
from .runtime import loyalty_rewards_record_partner_accrual
from .runtime import loyalty_rewards_receive_event


PBC_KEY = "loyalty_rewards"


def standalone_workflow_catalog() -> tuple[dict, ...]:
    """Return executable standalone workflow definitions for this PBC app."""
    return (
        {
            "workflow_id": "bootstrap_loyalty_app",
            "label": "Bootstrap Loyalty App",
            "steps": ("configure_runtime", "set_parameter", "register_rule", "register_earning_rule"),
            "outcome": "runtime_ready",
        },
        {
            "workflow_id": "member_rewards_lifecycle",
            "label": "Member Rewards Lifecycle",
            "steps": (
                "enroll_member",
                "issue_points",
                "qualify_tier",
                "evaluate_offer_eligibility",
                "create_redemption",
            ),
            "outcome": "member_wallet_governed",
        },
        {
            "workflow_id": "partner_and_offer_growth",
            "label": "Partner and Offer Growth",
            "steps": (
                "record_partner_accrual",
                "simulate_offer",
                "review_fraud_risk",
                "screen_rewards_policy",
            ),
            "outcome": "campaign_decision_trace",
        },
        {
            "workflow_id": "liability_and_audit_review",
            "label": "Liability and Audit Review",
            "steps": (
                "schedule_expiration",
                "snapshot_liability",
                "forecast_breakage",
                "run_liability_controls",
                "reconcile_balance",
                "generate_balance_proof",
            ),
            "outcome": "audit_ready_release_evidence",
        },
    )


def bootstrap_standalone_state() -> dict:
    """Build a deterministic standalone app state using package-local seeds."""
    state = loyalty_rewards_empty_state()
    bundle = seed_data.seed_plan()["standalone_bundle"]
    state = loyalty_rewards_configure_runtime(state, bundle["configuration"])["state"]
    for key, value in bundle["parameters"].items():
        state = loyalty_rewards_set_parameter(state, key, value)["state"]
    for rule in bundle["rules"]:
        state = loyalty_rewards_register_rule(state, rule)["state"]
    for earning_rule in bundle["earning_rules"]:
        state = loyalty_rewards_register_earning_rule(state, earning_rule)["state"]
    for member in bundle["members"]:
        state = loyalty_rewards_enroll_member(state, member)["state"]
    for point_command in bundle["point_commands"]:
        state = loyalty_rewards_issue_points(state, point_command)["state"]
    state = loyalty_rewards_adjust_points(
        state,
        {
            "ledger_id": "ledger_alpha_adjustment",
            "account_id": "acct_alpha",
            "tenant": "tenant_alpha",
            "points": 60,
            "reason": "service_recovery_bonus",
        },
    )["state"]
    state = loyalty_rewards_qualify_tier(state, "acct_alpha")["state"]
    for accrual in bundle["partner_accruals"]:
        state = loyalty_rewards_record_partner_accrual(state, accrual)["state"]
    for offer in bundle["offer_evaluations"]:
        state = loyalty_rewards_evaluate_offer_eligibility(state, offer)["state"]
    state = loyalty_rewards_simulate_offer(
        state,
        {
            "simulation_id": "offer_sim_alpha",
            "tenant": "tenant_alpha",
            "account_id": "acct_alpha",
            "offer_id": "offer_bonus_alpha",
            "bonus_multiplier": 1.35,
        },
    )["state"]
    for review in bundle["fraud_reviews"]:
        state = loyalty_rewards_review_fraud_risk(state, review)["state"]
    state = loyalty_rewards_screen_rewards_policy(
        state,
        {
            "screening_id": "screen_alpha",
            "tenant": "tenant_alpha",
            "account_id": "acct_alpha",
            "activity_type": "consent_reward",
            "points": 90,
        },
    )["state"]
    state = loyalty_rewards_schedule_expiration(
        state,
        {
            "schedule_id": "expiry_alpha",
            "tenant": "tenant_alpha",
            "account_id": "acct_alpha",
            "points": 75,
            "expires_in_days": 45,
        },
    )["state"]
    state = loyalty_rewards_snapshot_liability(state, "tenant_alpha")["state"]
    state = loyalty_rewards_forecast_breakage(
        state,
        {"forecast_id": "forecast_alpha", "tenant": "tenant_alpha", "horizon_days": 90},
    )["state"]
    for event in bundle["events"]:
        state = loyalty_rewards_receive_event(state, event)["state"]
    state = loyalty_rewards_create_redemption(state, bundle["redemptions"][0])["state"]
    state = loyalty_rewards_run_liability_controls(state, "tenant_alpha")["state"]
    state = loyalty_rewards_reconcile_balance(state, "acct_alpha")["state"]
    state = loyalty_rewards_generate_balance_proof(
        state,
        {"proof_id": "proof_alpha", "tenant": "tenant_alpha", "account_id": "acct_alpha"},
    )["state"]
    for model in bundle["governed_models"]:
        state = loyalty_rewards_register_governed_model(state, model)["state"]
    return state


def standalone_application_manifest() -> dict:
    """Return the standalone one-PBC app composition contract."""
    state = bootstrap_standalone_state()
    workbench = loyalty_rewards_build_workbench_view(state, tenant="tenant_alpha")
    return {
        "format": "appgen.loyalty-rewards-standalone-app.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "mode": "standalone_one_pbc_app",
        "manifest": PBC_MANIFEST,
        "routes": routes.api_route_contracts(),
        "services": services.service_operation_manifest(),
        "permissions": permissions.permission_manifest(),
        "events": events.event_contract_manifest(),
        "ui": ui.loyalty_rewards_ui_contract(),
        "agent": agent.composed_agent_contribution(),
        "release": loyalty_rewards_build_release_evidence(),
        "seed": seed_data.seed_plan(),
        "workflows": standalone_workflow_catalog(),
        "bootstrap": {
            "state_digest": workbench["binding_evidence"]["outbox_table"],
            "account_count": workbench["account_count"],
            "liability_amount": workbench["liability_amount"],
            "workbench": workbench,
        },
        "side_effects": (),
    }


def validate_standalone_application() -> dict:
    """Validate standalone app completeness and bootstrap evidence."""
    app = standalone_application_manifest()
    workflow_ids = tuple(item["workflow_id"] for item in app["workflows"])
    missing_workflows = tuple(
        workflow
        for workflow in (
            "bootstrap_loyalty_app",
            "member_rewards_lifecycle",
            "partner_and_offer_growth",
            "liability_and_audit_review",
        )
        if workflow not in workflow_ids
    )
    missing_sections = tuple(
        section
        for section in ("routes", "services", "permissions", "events", "ui", "agent", "release", "seed")
        if not app.get(section)
    )
    return {
        "ok": app["ok"]
        and not missing_workflows
        and not missing_sections
        and app["bootstrap"]["account_count"] >= 1
        and app["bootstrap"]["liability_amount"] >= 0
        and app["bootstrap"]["workbench"]["configuration_bound"] is True,
        "pbc": PBC_KEY,
        "missing_workflows": missing_workflows,
        "missing_sections": missing_sections,
        "app": app,
        "side_effects": (),
    }


class LoyaltyRewardsStandaloneApp:
    """Package-local standalone app that owns the loyalty runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or bootstrap_standalone_state()
        self.service = services.LoyaltyRewardsService(state=self.state)

    def dispatch(self, method: str, path: str, payload: dict | None = None) -> dict:
        result = routes.dispatch_route(method, path, payload, service=self.service)
        self.state = self.service.state
        return result

    def render_workbench(self, *, tenant: str, principal_permissions: tuple[str, ...] | None = None) -> dict:
        permissions_tuple = principal_permissions or tuple(sorted(set(permissions.permission_manifest()["permissions"])))
        rendered = ui.loyalty_rewards_render_standalone_app(
            self.state,
            tenant=tenant,
            principal_permissions=permissions_tuple,
        )
        return rendered

    def release_snapshot(self) -> dict:
        from . import release_evidence

        return release_evidence.build_release_evidence()


def workbench_smoke_test() -> dict:
    """Exercise bootstrap and rendering without release recursion."""
    app = LoyaltyRewardsStandaloneApp()
    rendered = app.render_workbench(tenant="tenant_alpha")
    service_contract = app.dispatch("GET", "/loyalty-rewards/service-contract", {})
    return {
        "ok": rendered["ok"] and service_contract["ok"] and bool(rendered["workbench"]["cards"]),
        "rendered": rendered,
        "service_contract": service_contract,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the standalone app composition contract."""
    validation = validate_standalone_application()
    app = validation["app"]
    return {
        "ok": validation["ok"]
        and app["agent"]["ok"]
        and bool(app["ui"]["forms"])
        and bool(app["ui"]["wizards"])
        and bool(app["ui"]["controls"])
        and bool(app["bootstrap"]["workbench"]["binding_evidence"]["owned_tables"]),
        "validation": validation,
        "side_effects": (),
    }
