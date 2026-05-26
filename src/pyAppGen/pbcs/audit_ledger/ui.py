"""UI contract for the Audit Ledger PBC."""

from __future__ import annotations


AUDIT_LEDGER_UI_FRAGMENT_KEYS = (
    "AuditLedgerWorkbench",
    "AuditEventSearch",
    "SignatureChainVerifier",
    "ForensicExportConsole",
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
            "publish_audit_projection": "audit_ledger.read",
            "register_rule": "audit_ledger.configure",
            "set_parameter": "audit_ledger.configure",
            "configure_runtime": "audit_ledger.configure",
            "run_control_tests": "audit_ledger.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "signature_algorithm", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
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
            "emits": ("AuditEventSealed", "SignatureChainVerified", "RetentionPolicyChanged", "ForensicExportPrepared", "ControlAssertionFailed", "AuditProjectionPublished"),
            "consumes": ("AccessPolicyChanged", "WorkflowCompleted", "RoutePublished", "SchemaAccepted", "PbcDeployed", "CompositionPublished"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
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
    cards = (
        {"key": "events", "value": len(events), "fragment": "AuditEventSearch"},
        {"key": "access_evidence", "value": len(access), "fragment": "AccessEvidenceView"},
        {"key": "exports", "value": len(exports), "fragment": "ForensicExportConsole"},
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
    }
