"""UI contract for the Payment Orchestration PBC."""

from __future__ import annotations


PAYMENT_ORCHESTRATION_UI_FRAGMENT_KEYS = (
    "PaymentOrchestrationWorkbench",
    "PaymentIntentConsole",
    "GatewayRoutingBoard",
    "PaymentTokenVault",
    "FraudCheckQueue",
    "CaptureRefundConsole",
    "SettlementEvidencePanel",
    "PaymentRuleStudio",
    "PaymentParameterConsole",
    "PaymentConfigurationPanel",
    "PaymentEventOutbox",
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
        ),
        "panels": (
            {"key": "intents", "fragment": "PaymentIntentConsole", "binds_to": ("payment_intent", "payment_token"), "commands": ("create_payment_intent", "capture_payment", "refund_payment", "void_payment")},
            {"key": "routing", "fragment": "GatewayRoutingBoard", "binds_to": ("payment_gateway", "gateway_route"), "commands": ("register_gateway", "route_gateway")},
            {"key": "risk", "fragment": "FraudCheckQueue", "binds_to": ("fraud_check", "inbox", "outbox"), "commands": ("request_fraud_check", "receive_event")},
            {"key": "governance", "fragment": "PaymentRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests")},
        ),
        "action_permissions": {
            "create_payment_intent": "payment_orchestration.intent",
            "route_gateway": "payment_orchestration.intent",
            "request_fraud_check": "payment_orchestration.intent",
            "capture_payment": "payment_orchestration.capture",
            "refund_payment": "payment_orchestration.refund",
            "void_payment": "payment_orchestration.refund",
            "register_gateway": "payment_orchestration.configure",
            "register_rule": "payment_orchestration.configure",
            "set_parameter": "payment_orchestration.configure",
            "configure_runtime": "payment_orchestration.configure",
            "run_control_tests": "payment_orchestration.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
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
            "required_fields": ("rule_id", "tenant", "rule_type", "allowed_gateways", "allowed_currencies", "allowed_regions", "risk_ceiling", "capture_policy", "status"),
        },
        "event_surfaces": {
            "emits": ("PaymentCaptured", "PaymentFailed", "FraudCheckRequested"),
            "consumes": ("CheckoutCompleted", "FraudRiskScored"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def payment_orchestration_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    contract = payment_orchestration_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, permission in action_permissions.items() if permission in permissions)
    view = _view_counts(state, tenant)
    cards = (
        {"key": "intents", "value": view["intent_count"], "fragment": "PaymentIntentConsole"},
        {"key": "captured", "value": view["captured_count"], "fragment": "CaptureRefundConsole"},
        {"key": "gateways", "value": view["gateway_count"], "fragment": "GatewayRoutingBoard"},
        {"key": "fraud_checks", "value": view["fraud_check_count"], "fragment": "FraudCheckQueue"},
        {"key": "outbox", "value": view["outbox_count"], "fragment": "PaymentEventOutbox"},
        {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "PaymentDeadLetterQueue"},
    )
    return {
        "format": "appgen.payment-orchestration-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/payment_orchestration",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    intents = tuple(intent for intent in state.get("intents", {}).values() if intent["tenant"] == tenant)
    gateways = tuple(gateway for gateway in state.get("gateways", {}).values() if gateway["tenant"] == tenant)
    fraud = tuple(check for check in state.get("fraud_checks", {}).values() if check.get("tenant") == tenant)
    return {
        "intent_count": len(intents),
        "captured_count": len(tuple(intent for intent in intents if intent["status"] in {"captured", "partially_refunded"})),
        "gateway_count": len(gateways),
        "fraud_check_count": len(fraud),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
        },
    }
