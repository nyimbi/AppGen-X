"""UI contract for the Audit Ledger PBC."""

from __future__ import annotations

from .runtime import AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
from .runtime import AUDIT_LEDGER_CONSUMED_EVENT_TYPES
from .runtime import AUDIT_LEDGER_EMITTED_EVENT_TYPES
from .runtime import AUDIT_LEDGER_OWNED_TABLES
from .runtime import AUDIT_LEDGER_REQUIRED_EVENT_TOPIC


AUDIT_LEDGER_UI_FRAGMENT_KEYS = (
    "AuditLedgerWorkbench",
    "AuditEventSearch",
    "SignatureChainVerifier",
    "ForensicExportConsole",
    "AuditRetryEvidenceConsole",
    "AuditReleaseEvidencePanel",
    "RetentionPolicyBoard",
    "AccessEvidenceView",
    "ControlAssertionBoard",
    "ProofDisclosureDesigner",
    "AuditAnomalyDashboard",
    "AuditRuleStudio",
    "AuditParameterConsole",
    "AuditConfigurationPanel",
)


def audit_ledger_ui_contract() -> dict:
    return {
        "format": "appgen.audit-ledger-ui-contract.v1",
        "ok": True,
        "pbc": "audit_ledger",
        "implementation_directory": "src/pyAppGen/pbcs/audit_ledger",
        "fragments": AUDIT_LEDGER_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/audit_ledger",
            "/workbench/pbcs/audit_ledger/events",
            "/workbench/pbcs/audit_ledger/signature-chain",
            "/workbench/pbcs/audit_ledger/forensic-exports",
            "/workbench/pbcs/audit_ledger/retry-evidence",
            "/workbench/pbcs/audit_ledger/release-evidence",
            "/workbench/pbcs/audit_ledger/retention",
            "/workbench/pbcs/audit_ledger/access-evidence",
            "/workbench/pbcs/audit_ledger/controls",
            "/workbench/pbcs/audit_ledger/proofs",
            "/workbench/pbcs/audit_ledger/rules",
            "/workbench/pbcs/audit_ledger/parameters",
            "/workbench/pbcs/audit_ledger/configuration",
        ),
        "panels": (
            {"key": "events", "fragment": "AuditEventSearch", "binds_to": ("audit_event", "signature_chain"), "commands": ("record_audit_event", "verify_signature_chain")},
            {"key": "forensics", "fragment": "ForensicExportConsole", "binds_to": ("forensic_export", "retention_policy"), "commands": ("prepare_forensic_export", "define_retention_policy")},
            {"key": "runtime", "fragment": "AuditRetryEvidenceConsole", "binds_to": ("appgen_inbox_event", "dead_letter_event"), "commands": ("receive_event", "build_release_evidence")},
            {"key": "release", "fragment": "AuditReleaseEvidencePanel", "binds_to": ("configuration", "rule", "parameter"), "commands": ("build_release_evidence",)},
            {"key": "controls", "fragment": "ControlAssertionBoard", "binds_to": ("control_assertion", "access_evidence"), "commands": ("assert_control", "record_access_evidence")},
            {"key": "governance", "fragment": "AuditRuleStudio", "binds_to": ("rule", "parameter", "configuration"), "commands": ("register_rule", "set_parameter", "configure_runtime")},
        ),
        "action_permissions": {
            "record_audit_event": "audit_ledger.seal",
            "record_access_evidence": "audit_ledger.seal",
            "define_retention_policy": "audit_ledger.configure",
            "assert_control": "audit_ledger.audit",
            "prepare_forensic_export": "audit_ledger.export",
            "verify_signature_chain": "audit_ledger.verify",
            "register_rule": "audit_ledger.configure",
            "set_parameter": "audit_ledger.configure",
            "configure_runtime": "audit_ledger.configure",
            "run_control_tests": "audit_ledger.audit",
            "receive_event": "audit_ledger.event",
            "build_release_evidence": "audit_ledger.read",
            "publish_audit_projection": "audit_ledger.publish",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "signature_algorithm", "default_timezone"),
            "allowed_database_backends": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "required_event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "retention_days",
                "export_batch_limit",
                "tamper_risk_threshold",
                "control_failure_threshold",
                "proof_disclosure_limit",
                "review_sla_hours",
            ),
        },
        "rule_editor": {
            "rule_types": ("mutation", "access", "retention", "export", "control", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "classification", "minimum_retention_days", "requires_export_approval", "severity", "status"),
        },
        "event_surfaces": {
            "emits": AUDIT_LEDGER_EMITTED_EVENT_TYPES,
            "consumes": AUDIT_LEDGER_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": AUDIT_LEDGER_OWNED_TABLES,
            "outbox_table": "audit_ledger_appgen_outbox_event",
            "inbox_table": "audit_ledger_appgen_inbox_event",
            "dead_letter_table": "audit_ledger_dead_letter_event",
            "shared_table_access": False,
            "configuration": {
                "event_contract": "AppGen-X",
                "required_event_topic": AUDIT_LEDGER_REQUIRED_EVENT_TOPIC,
                "stream_engine_picker_visible": False,
            },
        },
    }


def audit_ledger_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = audit_ledger_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    events = tuple(item for item in state["audit_events"].values() if item["tenant"] == tenant)
    access = tuple(item for item in state["access_evidence"].values() if item["tenant"] == tenant)
    exports = tuple(item for item in state["forensic_exports"].values() if item["tenant"] == tenant)
    controls = tuple(item for item in state["control_assertions"].values() if item["tenant"] == tenant)
    retry_evidence = tuple(state.get("retry_evidence", ()))
    dead_letters = tuple(state.get("dead_letter", state.get("dead_letters", ())))
    cards = (
        {"key": "events", "value": len(events), "fragment": "AuditEventSearch"},
        {"key": "access_evidence", "value": len(access), "fragment": "AccessEvidenceView"},
        {"key": "exports", "value": len(exports), "fragment": "ForensicExportConsole"},
        {"key": "retry_evidence", "value": len(retry_evidence), "fragment": "AuditRetryEvidenceConsole"},
        {"key": "dead_letter", "value": len(dead_letters), "fragment": "AuditRetryEvidenceConsole"},
        {"key": "release_evidence", "value": int(bool(state["configuration"].get("ok")) and bool(state.get("rules")) and bool(state.get("parameters"))), "fragment": "AuditReleaseEvidencePanel"},
        {"key": "controls", "value": len(controls), "fragment": "ControlAssertionBoard"},
        {"key": "release_blocking", "value": len(tuple(item for item in controls if item["release_blocking"])), "fragment": "ControlAssertionBoard"},
    )
    return {
        "format": "appgen.audit-ledger-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/audit_ledger",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "inbox_count": len(state.get("inbox", ())),
        "retry_evidence_count": len(retry_evidence),
        "dead_letter_count": len(dead_letters),
        "release_evidence_ready": bool(state["configuration"].get("ok")) and bool(state.get("rules")) and bool(state.get("parameters")),
        "binding_evidence": contract["binding_evidence"],
    }
