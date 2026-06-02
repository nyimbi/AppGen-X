"""UI contract for the Fraud Anomaly Detection PBC."""

from __future__ import annotations

from .runtime import FRAUD_ANOMALY_DETECTION_ALLOWED_DATABASE_BACKENDS
from .runtime import FRAUD_ANOMALY_DETECTION_OWNED_TABLES
from .runtime import FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC
from .runtime import FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES
from .app_surface import single_pbc_fraud_anomaly_detection_app_contract


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


def fraud_anomaly_detection_forms_contract() -> dict:
    """Return one-PBC app forms for fraud operations."""
    from .app_surface import fraud_anomaly_detection_forms_contract as _forms

    return _forms()


def fraud_anomaly_detection_wizards_contract() -> dict:
    """Return one-PBC app wizards for fraud operations."""
    from .app_surface import fraud_anomaly_detection_wizards_contract as _wizards

    return _wizards()


def fraud_anomaly_detection_controls_contract() -> dict:
    """Return one-PBC app controls for fraud operations."""
    from .app_surface import fraud_anomaly_detection_controls_contract as _controls

    return _controls()


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
        "rule_editor": {
            "rule_types": ("configuration", "parameter", "release_gate", "domain_policy"),
            "required_fields": ("rule_id", "tenant", "rule_type", "status"),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "forms": fraud_anomaly_detection_forms_contract()["forms"],
        "wizards": fraud_anomaly_detection_wizards_contract()["wizards"],
        "controls": fraud_anomaly_detection_controls_contract()["controls"],
        "single_pbc_app": single_pbc_fraud_anomaly_detection_app_contract(),
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
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "single_pbc_app": contract["single_pbc_app"],
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
            "runtime_tables": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES,
            "eventing": {
                "event_contract": "AppGen-X",
                "required_event_topic": FRAUD_ANOMALY_DETECTION_REQUIRED_EVENT_TOPIC,
                "outbox_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[0],
                "inbox_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[1],
                "dead_letter_table": FRAUD_ANOMALY_DETECTION_RUNTIME_TABLES[2],
                "stream_engine_picker_visible": False,
            },
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
    contract = fraud_anomaly_detection_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = fraud_anomaly_detection_render_workbench(
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
    standalone_app = contract.get("single_pbc_app", {})
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and standalone_app.get("ok") is True
        and standalone_app.get("database_backed") is True
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


from .fraud_control import improve1_fraud_control_contract

_fraud_anomaly_detection_base_ui_contract = fraud_anomaly_detection_ui_contract
_fraud_anomaly_detection_base_render_workbench = fraud_anomaly_detection_render_workbench

def fraud_anomaly_detection_ui_contract() -> dict:
    ui = _fraud_anomaly_detection_base_ui_contract()
    control = improve1_fraud_control_contract()
    surface = dict(ui.get('full_capability_surface', {}))
    surface['fraud_control_panels'] = tuple(item['evidence']['ui_surface'] for item in control['capabilities'])
    surface['fraud_control_service_actions'] = tuple(item['evidence']['service_api'] for item in control['capabilities'])
    surface['fraud_control_tables'] = control['owned_tables']
    return {**ui, 'ok': ui.get('ok') is True and control['ok'], 'full_capability_surface': surface, 'fraud_control_contract': control, 'side_effects': ()}

def fraud_anomaly_detection_render_workbench(state: dict, *, tenant: str, principal_permissions: tuple[str, ...]) -> dict:
    workbench = _fraud_anomaly_detection_base_render_workbench(state, tenant=tenant, principal_permissions=principal_permissions)
    control = improve1_fraud_control_contract()
    return {**workbench, 'ok': workbench.get('ok') is True and control['ok'], 'fraud_control_panels': tuple(item['evidence']['ui_surface'] for item in control['capabilities']), 'fraud_control_service_actions': tuple(item['evidence']['service_api'] for item in control['capabilities']), 'side_effects': ()}
