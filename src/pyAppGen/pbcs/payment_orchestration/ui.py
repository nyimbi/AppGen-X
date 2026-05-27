"""UI contract for the Payment Orchestration PBC."""

from __future__ import annotations

from .runtime import PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS
from .runtime import PAYMENT_ORCHESTRATION_OWNED_TABLES
from .runtime import PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC
from .runtime import payment_orchestration_build_workbench_view
from .runtime import payment_orchestration_permissions_contract


PAYMENT_ORCHESTRATION_UI_FRAGMENT_KEYS = (
    "PaymentOrchestrationWorkbench",
    "PaymentIntentConsole",
    "GatewayRoutingBoard",
    "PaymentTokenVault",
    "FraudCheckQueue",
    "AuthorizationReviewConsole",
    "CaptureRefundConsole",
    "SettlementEvidencePanel",
    "PayoutSchedulingPanel",
    "DisputeResolutionDesk",
    "PaymentRuleStudio",
    "PaymentParameterConsole",
    "PaymentConfigurationPanel",
    "PaymentEventOutbox",
    "PaymentInboxMonitor",
    "PaymentDeadLetterQueue",
)


def payment_orchestration_ui_contract() -> dict:
    return {
        "format": "appgen.payment-orchestration-ui-contract.v1",
        "ok": True,
        "pbc": "payment_orchestration",
        "implementation_directory": "src/pyAppGen/pbcs/payment_orchestration",
        "fragments": PAYMENT_ORCHESTRATION_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/payment_orchestration",
            "/workbench/pbcs/payment_orchestration/intents",
            "/workbench/pbcs/payment_orchestration/gateways",
            "/workbench/pbcs/payment_orchestration/tokens",
            "/workbench/pbcs/payment_orchestration/fraud",
            "/workbench/pbcs/payment_orchestration/settlement",
            "/workbench/pbcs/payment_orchestration/rules",
            "/workbench/pbcs/payment_orchestration/parameters",
            "/workbench/pbcs/payment_orchestration/configuration",
            "/workbench/pbcs/payment_orchestration/events",
        ),
        "panels": (
            {
                "key": "intent_console",
                "fragment": "PaymentIntentConsole",
                "binds_to": ("payment_intent", "payment_token"),
                "commands": (
                    "create_payment_intent",
                    "authorize_payment",
                    "capture_payment",
                    "settle_payment",
                    "schedule_payout",
                    "refund_payment",
                    "open_dispute",
                    "resolve_dispute",
                    "void_payment",
                ),
            },
            {
                "key": "routing",
                "fragment": "GatewayRoutingBoard",
                "binds_to": ("payment_gateway", "gateway_route"),
                "commands": ("register_gateway", "route_gateway", "simulate_gateway_route"),
            },
            {
                "key": "risk",
                "fragment": "FraudCheckQueue",
                "binds_to": (
                    "fraud_check",
                    "payment_orchestration_appgen_inbox_event",
                    "payment_orchestration_appgen_outbox_event",
                ),
                "commands": ("request_fraud_check", "receive_event", "score_payment_risk"),
            },
            {
                "key": "settlement",
                "fragment": "SettlementEvidencePanel",
                "binds_to": (
                    "payment_capture",
                    "payment_refund",
                    "payment_settlement",
                    "payment_payout",
                    "payment_dispute",
                    "payment_reconciliation_handoff",
                ),
                "commands": (
                    "capture_payment",
                    "settle_payment",
                    "schedule_payout",
                    "refund_payment",
                    "open_dispute",
                    "resolve_dispute",
                    "generate_payment_proof",
                ),
            },
            {
                "key": "governance",
                "fragment": "PaymentRuleStudio",
                "binds_to": ("payment_rule", "payment_parameter", "payment_configuration"),
                "commands": (
                    "register_rule",
                    "set_parameter",
                    "configure_runtime",
                    "run_control_tests",
                ),
            },
        ),
        "action_permissions": payment_orchestration_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_currency",
                "default_timezone",
            ),
            "allowed_database_backends": PAYMENT_ORCHESTRATION_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": PAYMENT_ORCHESTRATION_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "authorization_threshold",
                "fraud_review_threshold",
                "capture_amount_tolerance",
                "retry_limit",
                "gateway_latency_weight",
                "gateway_cost_weight",
                "gateway_auth_weight",
                "settlement_risk_weight",
                "max_capture_attempts",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("gateway_routing", "capture", "refund", "fraud", "settlement"),
            "required_fields": (
                "rule_id",
                "tenant",
                "rule_type",
                "allowed_gateways",
                "allowed_currencies",
                "allowed_regions",
                "risk_ceiling",
                "capture_policy",
                "status",
            ),
        },
        "event_surfaces": {
            "emits": (
                "PaymentIntentCreated",
                "PaymentAuthorized",
                "PaymentCaptured",
                "PaymentSettled",
                "PaymentPayoutScheduled",
                "PaymentRefunded",
                "PaymentVoided",
                "PaymentDisputeOpened",
                "PaymentDisputeResolved",
                "PaymentFailed",
                "FraudCheckRequested",
            ),
            "consumes": ("CheckoutCompleted", "FraudRiskScored"),
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
            "shared_table_access": False,
        },
    }


def payment_orchestration_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = payment_orchestration_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(
        action
        for action, required_permission in action_permissions.items()
        if required_permission in permissions
    )
    view = payment_orchestration_build_workbench_view(state, tenant=tenant)
    cards = (
        {
            "key": "intents",
            "value": view["intent_count"],
            "fragment": "PaymentIntentConsole",
        },
        {
            "key": "gateways",
            "value": view["gateway_count"],
            "fragment": "GatewayRoutingBoard",
        },
        {
            "key": "tokens",
            "value": view["token_count"],
            "fragment": "PaymentTokenVault",
        },
        {
            "key": "captures",
            "value": view["captured_count"],
            "fragment": "CaptureRefundConsole",
        },
        {
            "key": "authorizations",
            "value": view["authorization_count"],
            "fragment": "AuthorizationReviewConsole",
        },
        {
            "key": "settlements",
            "value": view["settlement_count"],
            "fragment": "SettlementEvidencePanel",
        },
        {
            "key": "payouts",
            "value": view["payout_count"],
            "fragment": "PayoutSchedulingPanel",
        },
        {
            "key": "disputes",
            "value": view["dispute_count"],
            "fragment": "DisputeResolutionDesk",
        },
        {
            "key": "dead_letter",
            "value": view["dead_letter_count"],
            "fragment": "PaymentDeadLetterQueue",
        },
    )
    return {
        "format": "appgen.payment-orchestration-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/payment_orchestration",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(
            action for action in action_permissions if action not in visible_actions
        ),
        "configuration_bound": view["configuration_bound"],
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "inbox_count": view["inbox_count"],
        "dead_letter_count": view["dead_letter_count"],
        "binding_evidence": {
            "owned_tables": PAYMENT_ORCHESTRATION_OWNED_TABLES,
            "outbox_table": "payment_orchestration_appgen_outbox_event",
            "inbox_table": "payment_orchestration_appgen_inbox_event",
            "dead_letter_table": "payment_orchestration_dead_letter_event",
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
    contract = payment_orchestration_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = payment_orchestration_render_workbench(
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
