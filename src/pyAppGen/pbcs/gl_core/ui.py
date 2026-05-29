"""UI contract and standalone workbench surface for the gl_core PBC."""

from __future__ import annotations

from .runtime import GL_CORE_ALLOWED_DATABASE_BACKENDS
from .runtime import GL_CORE_CONSUMED_EVENT_TYPES
from .runtime import GL_CORE_EMITTED_EVENT_TYPES
from .runtime import GL_CORE_OWNED_TABLES
from .runtime import GL_CORE_REQUIRED_EVENT_TOPIC
from .runtime import gl_core_build_workbench_view
from .runtime import gl_core_empty_state
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
GL_CORE_FORM_KEYS = (
    "ledger_account_form",
    "accounting_period_form",
    "journal_draft_form",
    "semantic_source_document_form",
    "reconciliation_case_form",
)
GL_CORE_WIZARD_KEYS = (
    "journal_posting_wizard",
    "continuous_close_wizard",
    "agent_assisted_adjustment_wizard",
)
GL_CORE_CONTROL_KEYS = (
    "close_status_banner",
    "trial_balance_meter",
    "policy_decision_panel",
    "event_outbox_timeline",
    "dead_letter_queue",
    "audit_proof_drawer",
)


def gl_core_form_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "ledger_account_form",
            "title": "Chart of Accounts",
            "repository_method": "save_ledger_account",
            "storage_table": "gl_core_ledger_account",
            "fields": ("account_id", "account_code", "account_type", "normal_balance", "parent_account_id", "tenant"),
        },
        {
            "key": "accounting_period_form",
            "title": "Accounting Period",
            "repository_method": "save_accounting_period",
            "storage_table": "gl_core_accounting_period",
            "fields": ("period_id", "fiscal_year", "period_number", "status", "tenant"),
        },
        {
            "key": "journal_draft_form",
            "title": "Journal Draft",
            "repository_method": "save_journal_draft",
            "storage_tables": ("gl_core_journal_entry", "gl_core_journal_line"),
            "command": "append_ledger_event",
            "fields": ("journal_id", "period_id", "source_document_hash", "lines", "tenant"),
        },
        {
            "key": "semantic_source_document_form",
            "title": "Semantic Source Document",
            "repository_method": "save_source_document",
            "storage_table": "gl_core_semantic_source_document",
            "fields": ("document_id", "source_hash", "derived_account", "confidence", "audit_trace", "tenant"),
        },
        {
            "key": "reconciliation_case_form",
            "title": "Reconciliation Case",
            "repository_method": "save_reconciliation_case",
            "storage_table": "gl_core_reconciliation_case",
            "command": "suggest_reconciliation",
            "fields": ("case_id", "source_id", "ledger_event_id", "score", "decision", "tenant"),
        },
    )


def gl_core_wizard_catalog() -> tuple[dict, ...]:
    return (
        {
            "key": "journal_posting_wizard",
            "steps": ("ledger_account_form", "accounting_period_form", "journal_draft_form"),
            "goal": "Prepare, validate, and post one balanced journal inside the GL-owned datastore boundary.",
        },
        {
            "key": "continuous_close_wizard",
            "steps": ("journal_draft_form", "reconciliation_case_form"),
            "goal": "Review the trial balance, run reconciliation, and capture a continuous close snapshot.",
        },
        {
            "key": "agent_assisted_adjustment_wizard",
            "steps": ("semantic_source_document_form", "journal_draft_form"),
            "goal": "Translate finance instructions into a governed journal draft with approval and audit evidence.",
        },
    )


def gl_core_control_catalog() -> tuple[dict, ...]:
    return (
        {"key": "close_status_banner", "type": "banner", "binds_to": "close_snapshot.audit_ready"},
        {"key": "trial_balance_meter", "type": "metric", "binds_to": "projection.trial_balance"},
        {"key": "policy_decision_panel", "type": "panel", "binds_to": "rules"},
        {"key": "event_outbox_timeline", "type": "timeline", "binds_to": "outbox"},
        {"key": "dead_letter_queue", "type": "queue", "binds_to": "dead_letter"},
        {"key": "audit_proof_drawer", "type": "drawer", "binds_to": "audit_proof"},
    )


def gl_core_standalone_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": "gl_core",
        "app_id": "gl_core_one_pbc_app",
        "workbench_route": "/workbench/pbcs/gl_core",
        "navigation": (
            {"key": "journals", "route": "/workbench/pbcs/gl_core/journals"},
            {"key": "trial_balance", "route": "/workbench/pbcs/gl_core/trial-balance"},
            {"key": "close", "route": "/workbench/pbcs/gl_core/close"},
            {"key": "reconciliations", "route": "/workbench/pbcs/gl_core/reconciliations"},
            {"key": "governance", "route": "/workbench/pbcs/gl_core/governance"},
        ),
        "forms": GL_CORE_FORM_KEYS,
        "wizards": GL_CORE_WIZARD_KEYS,
        "controls": GL_CORE_CONTROL_KEYS,
        "single_agent_namespace": "gl_core_skills",
        "side_effects": (),
    }


def gl_core_ui_contract() -> dict:
    return {
        "format": "appgen.gl-core-ui-contract.v2",
        "ok": True,
        "pbc": "gl_core",
        "implementation_directory": "src/pyAppGen/pbcs/gl_core",
        "fragments": GL_CORE_UI_FRAGMENT_KEYS,
        "routes": tuple(item["route"] for item in gl_core_standalone_app_contract()["navigation"]) + (
            "/workbench/pbcs/gl_core",
        ),
        "panels": (
            {
                "key": "posting",
                "fragment": "JournalEntryConsole",
                "binds_to": ("journal_entry", "journal_line", "appgen_outbox_event"),
                "commands": ("append_ledger_event", "predict_posting_validation"),
            },
            {
                "key": "close",
                "fragment": "CloseCommandCenter",
                "binds_to": ("account_projection", "close_snapshot", "control_assertion"),
                "commands": ("build_projection", "create_continuous_close_snapshot"),
            },
            {
                "key": "reconciliation",
                "fragment": "ReconciliationQueue",
                "binds_to": ("reconciliation_case", "ledger_projection"),
                "commands": ("suggest_reconciliation", "generate_audit_proof"),
            },
            {
                "key": "governance",
                "fragment": "PolicyRuleStudio",
                "binds_to": ("policy_rule", "schema_extension", "tenant_ledger_partition"),
                "commands": ("register_rule",),
            },
        ),
        "forms": gl_core_form_catalog(),
        "wizards": gl_core_wizard_catalog(),
        "controls": gl_core_control_catalog(),
        "standalone_app": gl_core_standalone_app_contract(),
        "action_permissions": gl_core_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_currency", "default_timezone", "allowed_account_types", "workbench_limit"),
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
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("journal_posting", "close", "reconciliation", "governance"),
            "required_fields": ("rule_id", "tenant", "scope", "status"),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": GL_CORE_EMITTED_EVENT_TYPES,
            "consumes": GL_CORE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": GL_CORE_OWNED_TABLES,
            "shared_table_access": False,
            "event_contract": "AppGen-X",
            "required_event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
        },
    }


def gl_core_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = gl_core_ui_contract()
    shell = gl_core_standalone_app_contract()
    snapshot = gl_core_build_workbench_view(state, tenant=tenant)
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action
        for action, required_permission in contract["action_permissions"].items()
        if required_permission in permissions
    )
    return {
        "format": "appgen.gl-core-workbench-render.v2",
        "ok": True,
        "tenant": tenant,
        "route": shell["workbench_route"],
        "fragments": contract["fragments"],
        "navigation": shell["navigation"],
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "cards": (
            {"key": "journal_events", "value": snapshot["event_count"], "fragment": "JournalEntryConsole"},
            {"key": "accounts", "value": snapshot["account_count"], "fragment": "AccountProjectionExplorer"},
            {"key": "trial_balance", "value": snapshot["trial_balance"], "fragment": "TrialBalanceView"},
            {"key": "audit_ready", "value": int(snapshot["audit_ready"]), "fragment": "CloseCommandCenter"},
            {"key": "rules", "value": snapshot["rule_count"], "fragment": "PolicyRuleStudio"},
            {"key": "outbox", "value": snapshot["outbox_count"], "fragment": "AuditProofViewer"},
            {"key": "dead_letter", "value": snapshot["dead_letter_count"], "fragment": "ControlsDashboard"},
        ),
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": snapshot["configuration_bound"],
        "rules_bound": tuple(sorted(state.get("rules", {}))),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": snapshot["outbox_count"],
        "inbox_count": snapshot["inbox_count"],
        "dead_letter_count": snapshot["dead_letter_count"],
        "binding_evidence": {
            **snapshot["binding_evidence"],
            "event_contract": "AppGen-X",
        },
        "side_effects": (),
    }


def gl_core_render_standalone_app(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    """Render the package-local standalone app shell."""
    workbench = gl_core_render_workbench(state, tenant=tenant, principal_permissions=principal_permissions)
    return {
        "ok": workbench["ok"],
        "shell": gl_core_standalone_app_contract(),
        "workbench": workbench,
        "side_effects": (),
    }


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = gl_core_ui_contract()
    state = gl_core_empty_state()
    state["configuration"] = {
        "ok": True,
        "event_contract": "AppGen-X",
        "event_topic": GL_CORE_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "user_selectable_event_contract": False,
    }
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = gl_core_render_standalone_app(
        state,
        tenant="tenant_smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered["workbench"].get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    return {
        "format": "appgen.pbc-ui-smoke-test.v2",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible") is False
        and bool(contract.get("parameter_editor"))
        and bool(contract.get("rule_editor"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and bool(event_surfaces)
        and binding_evidence.get("shared_table_access") is not True,
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
