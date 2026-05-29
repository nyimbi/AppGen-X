"""UI contract and standalone workbench surface for the loyalty_rewards PBC."""

from __future__ import annotations

from .runtime import LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
from .runtime import LOYALTY_REWARDS_CONSUMED_EVENT_TYPES
from .runtime import LOYALTY_REWARDS_EMITTED_EVENT_TYPES
from .runtime import LOYALTY_REWARDS_OWNED_TABLES
from .runtime import LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC
from .runtime import LOYALTY_REWARDS_RUNTIME_TABLES
from .runtime import loyalty_rewards_build_workbench_view
from .runtime import loyalty_rewards_empty_state
from .runtime import loyalty_rewards_permissions_contract


LOYALTY_REWARDS_UI_FRAGMENT_KEYS = (
    "LoyaltyRewardsWorkbench",
    "RewardAccountRegistry",
    "PointsLedgerPanel",
    "EarningRuleStudio",
    "RedemptionConsole",
    "TierQualificationBoard",
    "ReferralAndPartnerPanel",
    "ExpirationLiabilityPanel",
    "RewardsFraudReviewQueue",
    "RewardsRuleStudio",
    "RewardsParameterConsole",
    "RewardsConfigurationPanel",
    "RewardsEventOutbox",
    "RewardsDeadLetterQueue",
)
LOYALTY_REWARDS_FORM_KEYS = (
    "runtime_bootstrap_form",
    "member_enrollment_form",
    "earn_burn_adjustment_form",
    "partner_accrual_form",
    "offer_and_consent_intake_form",
    "reconciliation_proof_form",
)
LOYALTY_REWARDS_WIZARD_KEYS = (
    "launch_loyalty_program_wizard",
    "member_lifecycle_wizard",
    "risk_and_liability_wizard",
)
LOYALTY_REWARDS_CONTROL_KEYS = (
    "tier_progress_ladder",
    "liability_forecast_panel",
    "promotion_eligibility_preview",
    "consent_document_dropzone",
    "fraud_threshold_slider",
    "audit_evidence_drawer",
)


def loyalty_rewards_ui_blueprint() -> dict:
    """Return forms, wizards, and controls for the standalone loyalty workbench."""
    forms = (
        {
            "form_id": "runtime_bootstrap_form",
            "title": "Bootstrap Loyalty Runtime",
            "action": "configure_runtime",
            "permission": "loyalty_rewards.configure",
            "fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "supported_currencies",
                "supported_regions",
                "tier_calendar",
                "default_timezone",
                "liability_mode",
                "workbench_limit",
            ),
        },
        {
            "form_id": "member_enrollment_form",
            "title": "Enroll Loyalty Member",
            "action": "enroll_member",
            "permission": "loyalty_rewards.account.write",
            "fields": ("account_id", "tenant", "customer_id", "currency", "region", "tier", "status"),
        },
        {
            "form_id": "earn_burn_adjustment_form",
            "title": "Earn, Burn, or Adjust Points",
            "action": "issue_points",
            "permission": "loyalty_rewards.points.write",
            "fields": ("ledger_id", "account_id", "tenant", "points", "source", "source_ref"),
            "secondary_actions": ("adjust_points", "create_redemption", "expire_points"),
        },
        {
            "form_id": "partner_accrual_form",
            "title": "Partner Accrual and Referral Credit",
            "action": "record_partner_accrual",
            "permission": "loyalty_rewards.operations.write",
            "fields": ("partner_accrual_id", "tenant", "account_id", "partner_id", "activity_ref", "points", "status"),
            "secondary_actions": ("grant_referral_reward", "qualify_tier"),
        },
        {
            "form_id": "offer_and_consent_intake_form",
            "title": "Offer and Consent Intake",
            "action": "document_instruction_plan",
            "permission": "loyalty_rewards.audit",
            "fields": ("document", "instructions"),
            "handoff_actions": ("evaluate_offer_eligibility", "screen_rewards_policy"),
        },
        {
            "form_id": "reconciliation_proof_form",
            "title": "Reconcile and Prove Balance",
            "action": "reconcile_balance",
            "permission": "loyalty_rewards.operations.write",
            "fields": ("account_id",),
            "secondary_actions": ("generate_balance_proof", "run_liability_controls"),
        },
    )
    wizards = (
        {
            "wizard_id": "launch_loyalty_program_wizard",
            "title": "Launch Standalone Loyalty Program",
            "permission": "loyalty_rewards.configure",
            "steps": ("configure_runtime", "set_parameter", "register_rule", "register_earning_rule"),
            "outcome": "standalone_runtime_ready",
        },
        {
            "wizard_id": "member_lifecycle_wizard",
            "title": "Member Earn and Burn Lifecycle",
            "permission": "loyalty_rewards.operations.write",
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
            "wizard_id": "risk_and_liability_wizard",
            "title": "Risk, Expiration, and Liability Review",
            "permission": "loyalty_rewards.liability.write",
            "steps": (
                "schedule_expiration",
                "snapshot_liability",
                "review_fraud_risk",
                "screen_rewards_policy",
                "run_liability_controls",
                "generate_balance_proof",
            ),
            "outcome": "liability_audit_ready",
        },
    )
    controls = (
        {
            "control_id": "tier_progress_ladder",
            "label": "Tier Progress Ladder",
            "type": "board",
            "action": "qualify_tier",
            "permission": "loyalty_rewards.operations.write",
            "bounds": (),
        },
        {
            "control_id": "liability_forecast_panel",
            "label": "Liability Forecast",
            "type": "panel",
            "action": "forecast_breakage",
            "permission": "loyalty_rewards.intelligence.write",
            "bounds": (1, 365),
        },
        {
            "control_id": "promotion_eligibility_preview",
            "label": "Promotion and Offer Preview",
            "type": "preview",
            "action": "evaluate_offer_eligibility",
            "permission": "loyalty_rewards.operations.write",
            "bounds": (),
        },
        {
            "control_id": "consent_document_dropzone",
            "label": "Consent and Instruction Intake",
            "type": "upload",
            "action": "document_instruction_plan",
            "permission": "loyalty_rewards.audit",
            "bounds": (),
        },
        {
            "control_id": "fraud_threshold_slider",
            "label": "Fraud Threshold",
            "type": "slider",
            "action": "set_parameter",
            "permission": "loyalty_rewards.configure",
            "bounds": (0.0, 1.0),
        },
        {
            "control_id": "audit_evidence_drawer",
            "label": "Audit Evidence",
            "type": "drawer",
            "action": "generate_balance_proof",
            "permission": "loyalty_rewards.audit",
            "bounds": (),
        },
    )
    return {
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "workflow_board": (
            {
                "lane": "program_governance",
                "fragments": ("RewardsConfigurationPanel", "RewardsParameterConsole", "RewardsRuleStudio"),
            },
            {
                "lane": "member_operations",
                "fragments": ("RewardAccountRegistry", "PointsLedgerPanel", "RedemptionConsole"),
            },
            {
                "lane": "risk_and_liability",
                "fragments": ("TierQualificationBoard", "ExpirationLiabilityPanel", "RewardsFraudReviewQueue"),
            },
        ),
    }


def loyalty_rewards_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "loyalty_rewards",
        "app_id": "loyalty_rewards_one_pbc_app",
        "workbench_route": "/workbench/pbcs/loyalty_rewards",
        "navigation": (
            {"key": "members", "route": "/workbench/pbcs/loyalty_rewards/members"},
            {"key": "earn-burn", "route": "/workbench/pbcs/loyalty_rewards/earn-burn"},
            {"key": "tiers", "route": "/workbench/pbcs/loyalty_rewards/tiers"},
            {"key": "promotions", "route": "/workbench/pbcs/loyalty_rewards/promotions"},
            {"key": "liability", "route": "/workbench/pbcs/loyalty_rewards/liability"},
            {"key": "risk", "route": "/workbench/pbcs/loyalty_rewards/risk"},
            {"key": "audit", "route": "/workbench/pbcs/loyalty_rewards/audit"},
            {"key": "configuration", "route": "/workbench/pbcs/loyalty_rewards/configuration"},
        ),
        "forms": LOYALTY_REWARDS_FORM_KEYS,
        "wizards": LOYALTY_REWARDS_WIZARD_KEYS,
        "controls": LOYALTY_REWARDS_CONTROL_KEYS,
        "single_agent_namespace": "loyalty_rewards_skills",
        "side_effects": (),
    }


def loyalty_rewards_ui_contract() -> dict:
    blueprint = loyalty_rewards_ui_blueprint()
    permissions = loyalty_rewards_permissions_contract()
    shell = loyalty_rewards_standalone_app_contract()
    return {
        "format": "appgen.loyalty-rewards-ui-contract.v2",
        "ok": True,
        "pbc": "loyalty_rewards",
        "implementation_directory": "src/pyAppGen/pbcs/loyalty_rewards",
        "fragments": LOYALTY_REWARDS_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in shell["navigation"]) + (shell["workbench_route"],),
        "panels": (
            {
                "key": "members",
                "fragment": "RewardAccountRegistry",
                "binds_to": ("reward_account", "points_ledger", "reward_tier"),
                "commands": ("enroll_member", "issue_points", "adjust_points", "create_redemption"),
            },
            {
                "key": "promotions",
                "fragment": "ReferralAndPartnerPanel",
                "binds_to": ("referral_reward", "partner_accrual", "offer_eligibility", "offer_simulation"),
                "commands": ("grant_referral_reward", "record_partner_accrual", "evaluate_offer_eligibility", "simulate_offer"),
            },
            {
                "key": "liability",
                "fragment": "ExpirationLiabilityPanel",
                "binds_to": ("expiration_schedule", "liability_snapshot", "breakage_forecast", "liability_control_assertion"),
                "commands": ("schedule_expiration", "snapshot_liability", "forecast_breakage", "run_liability_controls"),
            },
            {
                "key": "risk",
                "fragment": "RewardsFraudReviewQueue",
                "binds_to": ("fraud_review", "churn_risk_score", "rewards_policy_screening", "loyalty_exception"),
                "commands": ("review_fraud_risk", "score_churn_risk", "screen_rewards_policy", "resolve_loyalty_exception"),
            },
            {
                "key": "audit",
                "fragment": "RewardsEventOutbox",
                "binds_to": LOYALTY_REWARDS_RUNTIME_TABLES,
                "commands": ("generate_balance_proof", "reconcile_balance", "federate_rewards_view", "build_release_evidence"),
            },
        ),
        "forms": blueprint["forms"],
        "wizards": blueprint["wizards"],
        "controls": blueprint["controls"],
        "workflow_board": blueprint["workflow_board"],
        "standalone_app": shell,
        "action_permissions": permissions["action_permissions"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "supported_currencies",
                "supported_regions",
                "tier_calendar",
                "default_timezone",
                "liability_mode",
                "workbench_limit",
            ),
            "allowed_database_backends": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_eventing_choice": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "base_points_per_currency_unit",
                "tier_multiplier_silver",
                "tier_multiplier_gold",
                "tier_multiplier_platinum",
                "redemption_value_per_point",
                "fraud_review_threshold",
                "liability_reserve_percent",
                "expiration_days",
                "max_daily_earn_points",
                "workbench_limit",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("loyalty_policy", "offer_policy", "promotion_policy", "liability_gate"),
            "required_fields": (
                "rule_id",
                "tenant",
                "scope",
                "status",
                "allowed_currencies",
                "allowed_regions",
                "earning_policy",
                "redemption_policy",
                "tier_policy",
            ),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": LOYALTY_REWARDS_EMITTED_EVENT_TYPES,
            "consumes": LOYALTY_REWARDS_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
            "runtime_tables": LOYALTY_REWARDS_RUNTIME_TABLES,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
            "required_event_topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
        },
    }


def _tenant_records(state: dict, key: str, tenant: str) -> tuple[dict, ...]:
    return tuple(item for item in state.get(key, {}).values() if item.get("tenant") == tenant)


def loyalty_rewards_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = loyalty_rewards_ui_contract()
    shell = loyalty_rewards_standalone_app_contract()
    snapshot = loyalty_rewards_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    tiers = _tenant_records(state, "reward_tiers", tenant)
    partner_accruals = _tenant_records(state, "partner_accruals", tenant)
    offer_eligibilities = _tenant_records(state, "offer_eligibilities", tenant)
    liability_controls = _tenant_records(state, "liability_control_assertions", tenant)
    fraud_reviews = _tenant_records(state, "fraud_reviews", tenant)
    balance_proofs = _tenant_records(state, "reward_balance_proofs", tenant)
    reconciliations = _tenant_records(state, "balance_reconciliations", tenant)
    return {
        "format": "appgen.loyalty-rewards-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": (
            {"key": "members", "value": snapshot["account_count"], "fragment": "RewardAccountRegistry"},
            {"key": "ledger", "value": snapshot["ledger_entry_count"], "fragment": "PointsLedgerPanel"},
            {"key": "redemptions", "value": snapshot["redemption_count"], "fragment": "RedemptionConsole"},
            {"key": "tiers", "value": len(tiers), "fragment": "TierQualificationBoard"},
            {"key": "partner_accruals", "value": len(partner_accruals), "fragment": "ReferralAndPartnerPanel"},
            {"key": "offers", "value": len(offer_eligibilities), "fragment": "ReferralAndPartnerPanel"},
            {"key": "liability", "value": snapshot["liability_amount"], "fragment": "ExpirationLiabilityPanel"},
            {"key": "controls", "value": len(liability_controls) + len(fraud_reviews), "fragment": "RewardsFraudReviewQueue"},
            {"key": "audit", "value": len(balance_proofs) + len(reconciliations), "fragment": "RewardsEventOutbox"},
            {"key": "dead_letter", "value": snapshot["dead_letter_count"], "fragment": "RewardsDeadLetterQueue"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": snapshot["configuration_bound"],
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "binding_evidence": {
            "owned_tables": snapshot["binding_evidence"]["owned_tables"],
            "runtime_tables": LOYALTY_REWARDS_RUNTIME_TABLES,
            "event_contract": "AppGen-X",
            "required_event_topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC,
            "shared_table_access": False,
            "account_count": snapshot["account_count"],
            "partner_accrual_count": len(partner_accruals),
            "offer_eligibility_count": len(offer_eligibilities),
            "audit_entry_count": len(balance_proofs) + len(reconciliations),
        },
    }


def loyalty_rewards_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    """Render the package-local standalone app shell."""
    workbench = loyalty_rewards_render_workbench(
        state,
        tenant=tenant,
        principal_permissions=principal_permissions,
    )
    return {
        "ok": workbench["ok"],
        "pbc": "loyalty_rewards",
        "shell": loyalty_rewards_standalone_app_contract(),
        "workbench": workbench,
        "side_effects": (),
    }


def _appgen_smoke_state() -> dict:
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    state = loyalty_rewards_empty_state()
    state["configuration"] = {"ok": True, "event_topic": LOYALTY_REWARDS_REQUIRED_EVENT_TOPIC}
    return state


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = loyalty_rewards_ui_contract()
    rendered = loyalty_rewards_render_standalone_app(
        _appgen_smoke_state(),
        tenant="tenant_smoke",
        principal_permissions=tuple(sorted(set(loyalty_rewards_permissions_contract()["permissions"]))),
    )
    return {
        "format": "appgen.pbc-ui-smoke-test.v2",
        "ok": contract["ok"]
        and rendered["ok"]
        and bool(contract["forms"])
        and bool(contract["wizards"])
        and bool(contract["controls"])
        and rendered["workbench"]["binding_evidence"]["shared_table_access"] is False,
        "manifest": {"fragments": contract["fragments"], "routes": contract["routes"]},
        "contract": contract,
        "rendered": rendered["workbench"],
        "side_effects": (),
    }
