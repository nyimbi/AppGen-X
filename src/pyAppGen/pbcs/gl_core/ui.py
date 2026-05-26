"""UI contract for the General Ledger Core PBC."""

from __future__ import annotations

from .runtime import GL_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import GL_CORE_CONSUMED_EVENT_TYPES
from .runtime import GL_CORE_EMITTED_EVENT_TYPES
from .runtime import GL_CORE_OWNED_TABLES
from .runtime import GL_CORE_REQUIRED_EVENT_TOPIC
from .runtime import gl_core_permissions_contract


GL_CORE_UI_FRAGMENT_KEYS = (
    "GeneralLedgerWorkbench",
    "JournalEntryConsole",
    "TrialBalanceView",
    "AccountProjectionExplorer",
    "CloseCommandCenter",
    "ReconciliationQueue",
    "PolicyRuleStudio",
    "LedgerParameterConsole",
    "LedgerConfigurationPanel",
    "AuditProofViewer",
    "ControlsDashboard",
)


def gl_core_ui_contract() -> dict:
    return {
        "format": "appgen.gl-core-ui-contract.v1",
        "ok": True,
        "pbc": "gl_core",
        "implementation_directory": "src/pyAppGen/pbcs/gl_core",
        "fragments": GL_CORE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/gl_core",
            "/workbench/pbcs/gl_core/journals",
            "/workbench/pbcs/gl_core/trial-balance",
            "/workbench/pbcs/gl_core/projections",
            "/workbench/pbcs/gl_core/close",
            "/workbench/pbcs/gl_core/reconciliations",
            "/workbench/pbcs/gl_core/rules",
            "/workbench/pbcs/gl_core/parameters",
            "/workbench/pbcs/gl_core/configuration",
            "/workbench/pbcs/gl_core/audit-proof",
            "/workbench/pbcs/gl_core/controls",
        ),
        "panels": (
            {
                "key": "posting",
                "fragment": "JournalEntryConsole",
                "binds_to": ("journal_event", "journal_line", "outbox"),
                "commands": ("append_ledger_event", "predict_posting_validation"),
            },
            {
                "key": "close",
                "fragment": "CloseCommandCenter",
                "binds_to": ("account_projection", "close_snapshot", "control_assertion"),
                "commands": ("build_projection", "create_continuous_close_snapshot", "run_control_tests"),
            },
            {
                "key": "reconciliation",
                "fragment": "ReconciliationQueue",
                "binds_to": ("reconciliation_case", "federated_view"),
                "commands": ("suggest_reconciliation", "resolve_reconciliation_game"),
            },
            {
                "key": "governance",
                "fragment": "PolicyRuleStudio",
                "binds_to": ("policy_rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime"),
            },
        ),
        "action_permissions": gl_core_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": GL_CORE_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "approval_threshold",
                "materiality_threshold",
                "close_tolerance",
                "revaluation_threshold",
                "retention_days",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("journal_posting", "approval", "close", "reconciliation", "revaluation", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
        },
        "event_surfaces": {
            "emits": GL_CORE_EMITTED_EVENT_TYPES,
            "consumes": GL_CORE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {"owned_tables": GL_CORE_OWNED_TABLES, "shared_table_access": False},
    }


def gl_core_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = gl_core_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    events = tuple(event for event in state.get("events", ()) if event["tenant"] == tenant)
    projection = _projection_summary(state, tenant)
    cards = (
        {"key": "journal_events", "value": len(events), "fragment": "JournalEntryConsole"},
        {"key": "accounts", "value": projection["account_count"], "fragment": "AccountProjectionExplorer"},
        {"key": "trial_balance", "value": projection["trial_balance"], "fragment": "TrialBalanceView"},
        {"key": "rules", "value": len(state.get("rules", {})), "fragment": "PolicyRuleStudio"},
        {"key": "outbox_events", "value": len(state.get("outbox", ())), "fragment": "AuditProofViewer"},
        {"key": "inbox_events", "value": len(state.get("inbox", ())), "fragment": "ControlsDashboard"},
        {"key": "dead_letter_events", "value": len(state.get("dead_letter", state.get("dead_letters", ()))), "fragment": "ControlsDashboard"},
    )
    return {
        "format": "appgen.gl-core-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/gl_core",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": GL_CORE_OWNED_TABLES,
            "outbox_table": "gl_core_appgen_outbox_event",
            "inbox_table": "gl_core_appgen_inbox_event",
            "dead_letter_table": "gl_core_dead_letter_event",
        },
    }


def _projection_summary(state: dict, tenant: str) -> dict:
    balances: dict[str, float] = {}
    for event in state.get("events", ()):
        if event["tenant"] != tenant:
            continue
        for line in event["payload"].get("lines", ()):
            account = line["account"]
            balances[account] = balances.get(account, 0.0) + float(line.get("debit", 0)) - float(line.get("credit", 0))
    return {"account_count": len(balances), "trial_balance": round(sum(balances.values()), 6)}

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
    contract = gl_core_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = gl_core_render_workbench(
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
