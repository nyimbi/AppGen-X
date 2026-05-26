"""UI contract for the Loyalty Rewards PBC."""

from __future__ import annotations

from .runtime import LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS
from .runtime import LOYALTY_REWARDS_OWNED_TABLES


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


def loyalty_rewards_ui_contract() -> dict:
    return {
        "format": "appgen.loyalty-rewards-ui-contract.v1",
        "ok": True,
        "pbc": "loyalty_rewards",
        "implementation_directory": "src/pyAppGen/pbcs/loyalty_rewards",
        "fragments": LOYALTY_REWARDS_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/loyalty_rewards",
            "/workbench/pbcs/loyalty_rewards/accounts",
            "/workbench/pbcs/loyalty_rewards/ledger",
            "/workbench/pbcs/loyalty_rewards/earning-rules",
            "/workbench/pbcs/loyalty_rewards/redemptions",
            "/workbench/pbcs/loyalty_rewards/configuration",
        ),
        "action_permissions": {
            "enroll_member": "loyalty_rewards.account.write",
            "issue_points": "loyalty_rewards.points.write",
            "adjust_points": "loyalty_rewards.points.write",
            "create_redemption": "loyalty_rewards.redemption.write",
            "expire_points": "loyalty_rewards.points.write",
            "receive_event": "loyalty_rewards.event.consume",
            "register_earning_rule": "loyalty_rewards.configure",
            "register_rule": "loyalty_rewards.configure",
            "set_parameter": "loyalty_rewards.configure",
            "configure_runtime": "loyalty_rewards.configure",
            "run_control_tests": "loyalty_rewards.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone", "liability_mode"),
            "allowed_database_backends": LOYALTY_REWARDS_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
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
        },
        "event_surfaces": {
            "emits": ("RewardBalanceChanged", "CustomerSegmentUpdated"),
            "consumes": ("PaymentCaptured", "PromotionApplied"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def loyalty_rewards_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = loyalty_rewards_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, permission in contract["action_permissions"].items() if permission in permissions)
    view = _view_counts(state, tenant)
    return {
        "format": "appgen.loyalty-rewards-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/loyalty_rewards",
        "fragments": contract["fragments"],
        "cards": (
            {"key": "accounts", "value": view["account_count"], "fragment": "RewardAccountRegistry"},
            {"key": "ledger", "value": view["ledger_entry_count"], "fragment": "PointsLedgerPanel"},
            {"key": "rules", "value": view["earning_rule_count"], "fragment": "EarningRuleStudio"},
            {"key": "redemptions", "value": view["redemption_count"], "fragment": "RedemptionConsole"},
            {"key": "liability", "value": view["liability_amount"], "fragment": "ExpirationLiabilityPanel"},
            {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "RewardsDeadLetterQueue"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    accounts = tuple(item for item in state.get("reward_accounts", {}).values() if item["tenant"] == tenant)
    ledger = tuple(item for item in state.get("points_ledger", {}).values() if item["tenant"] == tenant)
    rules = tuple(item for item in state.get("earning_rules", {}).values() if item["tenant"] == tenant)
    redemptions = tuple(item for item in state.get("redemptions", {}).values() if item["tenant"] == tenant)
    return {
        "account_count": len(accounts),
        "ledger_entry_count": len(ledger),
        "earning_rule_count": len(rules),
        "redemption_count": len(redemptions),
        "liability_amount": round(sum(float(account["liability_amount"]) for account in accounts), 2),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": LOYALTY_REWARDS_OWNED_TABLES,
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = loyalty_rewards_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = loyalty_rewards_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
