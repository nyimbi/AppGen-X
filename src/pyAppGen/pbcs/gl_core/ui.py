"""UI contract for the General Ledger Core PBC."""

from __future__ import annotations


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
        "action_permissions": {
            "append_ledger_event": "gl_core.post",
            "predict_posting_validation": "gl_core.post",
            "build_projection": "gl_core.read",
            "create_continuous_close_snapshot": "gl_core.close",
            "suggest_reconciliation": "gl_core.reconcile",
            "generate_audit_proof": "gl_core.audit",
            "register_rule": "gl_core.configure",
            "set_parameter": "gl_core.configure",
            "configure_runtime": "gl_core.configure",
            "run_control_tests": "gl_core.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
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
            "emits": ("JournalPosted", "CloseSnapshotCreated", "ReconciliationSuggested", "PostingPolicyChanged", "LedgerProjectionBuilt"),
            "consumes": ("InvoiceApproved", "PaymentCaptured", "PayrollPosted", "AssetDepreciated", "TaxCalculated"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
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
