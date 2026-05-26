"""UI contract for the Fraud Anomaly Detection PBC."""

from __future__ import annotations

from .runtime import FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS
from .runtime import FRAUD_ANOMALY_DETECTION_OWNED_TABLES


FRAUD_ANOMALY_DETECTION_UI_FRAGMENT_KEYS = (
    "FraudAnomalyDetectionWorkbench",
    "RiskSignalMonitor",
    "AnomalyScoreBoard",
    "FraudRuleStudio",
    "RiskCaseConsole",
    "IdentityLinkAnalysisPanel",
    "ExplainabilityConsole",
    "LossExposurePanel",
    "FraudParameterConsole",
    "FraudConfigurationPanel",
    "RiskEventInbox",
    "RiskEventOutbox",
    "PolicyChangeMonitor",
    "RiskDeadLetterQueue",
)


def fraud_anomaly_detection_ui_contract() -> dict:
    return {
        "format": "appgen.fraud-anomaly-detection-ui-contract.v1",
        "ok": True,
        "pbc": "fraud_anomaly_detection",
        "implementation_directory": "src/pyAppGen/pbcs/fraud_anomaly_detection",
        "fragments": FRAUD_ANOMALY_DETECTION_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/fraud_anomaly_detection",
            "/workbench/pbcs/fraud_anomaly_detection/signals",
            "/workbench/pbcs/fraud_anomaly_detection/scores",
            "/workbench/pbcs/fraud_anomaly_detection/rules",
            "/workbench/pbcs/fraud_anomaly_detection/cases",
            "/workbench/pbcs/fraud_anomaly_detection/configuration",
        ),
        "action_permissions": {
            "ingest_risk_signal": "fraud_anomaly_detection.event.write",
            "score_anomaly": "fraud_anomaly_detection.anomaly_score.write",
            "open_risk_case": "fraud_anomaly_detection.risk_case.write",
            "receive_event": "fraud_anomaly_detection.event.consume",
            "register_fraud_rule": "fraud_anomaly_detection.fraud_rule.write",
            "register_rule": "fraud_anomaly_detection.configure",
            "set_parameter": "fraud_anomaly_detection.configure",
            "configure_runtime": "fraud_anomaly_detection.configure",
            "run_control_tests": "fraud_anomaly_detection.audit",
        },
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "default_region",
                "default_timezone",
                "scoring_mode",
            ),
            "allowed_database_backends": FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "checkout_risk_weight",
                "payment_risk_weight",
                "access_policy_risk_weight",
                "anomaly_alert_threshold",
                "case_open_threshold",
                "baseline_min_events",
                "behavior_decay_days",
                "identity_linkage_weight",
                "supervised_override_weight",
                "workbench_limit",
            ),
        },
        "event_surfaces": {
            "emits": ("FraudRiskScored", "RiskCaseOpened"),
            "consumes": ("CheckoutCompleted", "PaymentCaptured", "AccessPolicyChanged"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
    }


def fraud_anomaly_detection_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = fraud_anomaly_detection_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, permission in contract["action_permissions"].items()
        if permission in permissions
    )
    view = _view_counts(state, tenant)
    return {
        "format": "appgen.fraud-anomaly-detection-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/fraud_anomaly_detection",
        "fragments": contract["fragments"],
        "cards": (
            {"key": "signals", "value": view["signal_count"], "fragment": "RiskSignalMonitor"},
            {"key": "scores", "value": view["anomaly_score_count"], "fragment": "AnomalyScoreBoard"},
            {"key": "rules", "value": view["fraud_rule_count"], "fragment": "FraudRuleStudio"},
            {"key": "cases", "value": view["case_count"], "fragment": "RiskCaseConsole"},
            {"key": "loss_exposure", "value": view["total_loss_exposure"], "fragment": "LossExposurePanel"},
            {"key": "dead_letter", "value": view["dead_letter_count"], "fragment": "RiskDeadLetterQueue"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(
            action
            for action in contract["action_permissions"]
            if action not in visible_actions
        ),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": view["binding_evidence"],
    }


def _view_counts(state: dict, tenant: str) -> dict:
    signals = tuple(item for item in state.get("risk_signals", {}).values() if item["tenant"] == tenant)
    scores = tuple(item for item in state.get("anomaly_scores", {}).values() if item["tenant"] == tenant)
    fraud_rules = tuple(item for item in state.get("fraud_rules", {}).values() if item["tenant"] == tenant)
    cases = tuple(item for item in state.get("risk_cases", {}).values() if item["tenant"] == tenant)
    return {
        "signal_count": len(signals),
        "anomaly_score_count": len(scores),
        "fraud_rule_count": len(fraud_rules),
        "case_count": len(cases),
        "total_loss_exposure": round(sum(float(item["risk_score"]) * 1000.0 for item in scores), 2),
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "binding_evidence": {
            "configuration": bool(state.get("configuration", {}).get("ok")),
            "rules": tuple(sorted(state.get("rules", {}))),
            "parameters": tuple(sorted(state.get("parameters", {}))),
            "owned_tables": FRAUD_ANOMALY_DETECTION_OWNED_TABLES,
        },
    }
