"""Package manifest for the audit_ledger PBC."""

from __future__ import annotations

from .runtime import AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
from .runtime import AUDIT_LEDGER_CONSUMED_EVENT_TYPES
from .runtime import AUDIT_LEDGER_EMITTED_EVENT_TYPES
from .runtime import AUDIT_LEDGER_OWNED_TABLES
from .runtime import AUDIT_LEDGER_RUNTIME_CAPABILITY_KEYS
from .runtime import AUDIT_LEDGER_STANDARD_FEATURE_KEYS
from .runtime import audit_ledger_build_api_contract

PBC_KEY = 'audit_ledger'


def _logical_tables() -> tuple[str, ...]:
    return tuple(table.removeprefix(f"{PBC_KEY}_") for table in AUDIT_LEDGER_OWNED_TABLES)


PBC_MANIFEST = {
    "pbc": "audit_ledger",
    "label": "Unified Audit Trail and Cryptographic Ledger",
    "mesh": "platform",
    "description": "Append-only signed mutation, security, and user-action evidence.",
    "datastore_backend": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS[0],
    "tables": _logical_tables(),
    "apis": tuple(route["route"] for route in audit_ledger_build_api_contract()["routes"]),
    "emits": AUDIT_LEDGER_EMITTED_EVENT_TYPES,
    "consumes": AUDIT_LEDGER_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": (
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
    ),
    "permissions": (
        "audit_ledger.read",
        "audit_ledger.seal",
        "audit_ledger.verify",
        "audit_ledger.export",
        "audit_ledger.publish",
        "audit_ledger.event",
        "audit_ledger.configure",
        "audit_ledger.audit",
    ),
    "configuration": (
        "AUDIT_LEDGER_DATABASE_URL",
        "AUDIT_LEDGER_EVENT_TOPIC",
        "AUDIT_LEDGER_RETRY_LIMIT",
        "AUDIT_LEDGER_SIGNATURE_ALGORITHM",
        "AUDIT_LEDGER_DEFAULT_TIMEZONE",
        "AUDIT_LEDGER_ALLOWED_CLASSIFICATIONS",
    ),
    "capabilities": AUDIT_LEDGER_RUNTIME_CAPABILITY_KEYS,
    "standard_features": AUDIT_LEDGER_STANDARD_FEATURE_KEYS,
    "workflows": tuple(
        item
        for item in audit_ledger_build_api_contract()["routes"]
        for item in (item.get("command") or item.get("query"),)
        if item
    ),
    "analytics": (
        "audit_event_sealed_throughput",
        "signature_chain_verification_rate",
        "forensic_export_prepared_throughput",
        "control_assertion_failure_rate",
        "audit_projection_handoff_latency",
        "dead_letter_recovery_rate",
        "tamper_risk_score",
        "evidence_health_forecast",
    ),
    "advanced_capabilities": AUDIT_LEDGER_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py", "tests/test_runtime_capabilities.py"),
    "docs": ("SPECIFICATION.md", "RELEASE_EVIDENCE.md"),
}
