"""SQLite-backed repository for the standalone audit_ledger PBC app."""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from .runtime import AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS
from .runtime import audit_ledger_assert_control
from .runtime import audit_ledger_build_notarization_bundle
from .runtime import audit_ledger_build_release_evidence
from .runtime import audit_ledger_build_workbench_view
from .runtime import audit_ledger_configure_runtime
from .runtime import audit_ledger_define_retention_policy
from .runtime import audit_ledger_empty_state
from .runtime import audit_ledger_prepare_forensic_export
from .runtime import audit_ledger_publish_audit_projection
from .runtime import audit_ledger_receive_event
from .runtime import audit_ledger_record_access_evidence
from .runtime import audit_ledger_record_audit_event
from .runtime import audit_ledger_register_rule
from .runtime import audit_ledger_set_parameter
from .runtime import audit_ledger_verify_signature_chain


def _json_dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _json_load(value: str | None, default: Any) -> Any:
    if value in (None, ""):
        return default
    return json.loads(value)


def _bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, ""):
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).lower() in {"1", "true", "yes"}


def _row_to_dict(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def standalone_sqlite_schema() -> str:
    """Return the SQLite schema used by the standalone one-PBC app."""
    return """
    CREATE TABLE IF NOT EXISTS audit_ledger_configuration (
        tenant TEXT NOT NULL,
        configuration_id TEXT PRIMARY KEY,
        database_backend TEXT NOT NULL,
        event_topic TEXT NOT NULL,
        retry_limit INTEGER NOT NULL,
        signature_algorithm TEXT NOT NULL,
        default_timezone TEXT NOT NULL,
        allowed_classifications_json TEXT NOT NULL,
        export_modes_json TEXT NOT NULL,
        workbench_limit INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_parameter (
        tenant TEXT NOT NULL,
        parameter_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        value TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_rule (
        tenant TEXT NOT NULL,
        rule_id TEXT PRIMARY KEY,
        scope TEXT NOT NULL,
        classification TEXT NOT NULL,
        minimum_retention_days INTEGER NOT NULL,
        requires_legal_hold_review INTEGER NOT NULL,
        requires_export_approval INTEGER NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_audit_event (
        tenant TEXT NOT NULL,
        audit_id TEXT PRIMARY KEY,
        source_pbc TEXT NOT NULL,
        aggregate_id TEXT NOT NULL,
        actor TEXT NOT NULL,
        action TEXT NOT NULL,
        classification TEXT NOT NULL,
        payload_hash TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        sequence INTEGER NOT NULL,
        previous_hash TEXT NOT NULL,
        event_hash TEXT NOT NULL,
        signature TEXT NOT NULL,
        signature_algorithm TEXT NOT NULL,
        canonicalization_profile TEXT NOT NULL,
        canonical_payload_json TEXT NOT NULL,
        occurred_at TEXT NOT NULL,
        timestamp_basis TEXT NOT NULL,
        causality_json TEXT NOT NULL,
        correction_json TEXT,
        admissibility_json TEXT NOT NULL,
        tamper_risk REAL NOT NULL,
        sealed INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_signature_chain (
        tenant TEXT NOT NULL,
        chain_link_id TEXT PRIMARY KEY,
        audit_id TEXT NOT NULL,
        sequence INTEGER NOT NULL,
        previous_hash TEXT NOT NULL,
        event_hash TEXT NOT NULL,
        signature TEXT NOT NULL,
        payload_hash TEXT NOT NULL,
        verified INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_retention_policy (
        tenant TEXT NOT NULL,
        policy_id TEXT PRIMARY KEY,
        classification TEXT NOT NULL,
        retention_days INTEGER NOT NULL,
        legal_hold INTEGER NOT NULL,
        disposal_action TEXT NOT NULL,
        status TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_forensic_export (
        tenant TEXT NOT NULL,
        export_id TEXT PRIMARY KEY,
        classification TEXT NOT NULL,
        requested_by TEXT NOT NULL,
        purpose TEXT NOT NULL,
        event_count INTEGER NOT NULL,
        checksum TEXT NOT NULL,
        proof_bundle TEXT NOT NULL,
        status TEXT NOT NULL,
        approval_required INTEGER NOT NULL,
        selected_fields_json TEXT NOT NULL,
        withheld_fields_json TEXT NOT NULL,
        risk_flags_json TEXT NOT NULL,
        proof_coverage_json TEXT NOT NULL,
        verifier_instructions_json TEXT NOT NULL,
        chain_of_custody_json TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_access_evidence (
        tenant TEXT NOT NULL,
        evidence_id TEXT PRIMARY KEY,
        principal TEXT NOT NULL,
        resource TEXT NOT NULL,
        action TEXT NOT NULL,
        decision TEXT NOT NULL,
        context_hash TEXT NOT NULL,
        context_json TEXT NOT NULL,
        policy_source TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_control_assertion (
        tenant TEXT NOT NULL,
        control_id TEXT PRIMARY KEY,
        control_name TEXT NOT NULL,
        status TEXT NOT NULL,
        severity TEXT NOT NULL,
        evidence_hash TEXT NOT NULL,
        evidence_json TEXT NOT NULL,
        release_blocking INTEGER NOT NULL,
        remediation TEXT
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_projection_link (
        tenant TEXT NOT NULL,
        projection_id TEXT PRIMARY KEY,
        audit_id TEXT NOT NULL,
        target_system TEXT NOT NULL,
        systems_json TEXT NOT NULL,
        projection_hash TEXT NOT NULL,
        handoff_status TEXT NOT NULL,
        handoffs_json TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_appgen_outbox_event (
        tenant TEXT NOT NULL,
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        topic TEXT NOT NULL,
        idempotency_key TEXT NOT NULL,
        status TEXT NOT NULL,
        audit_hash TEXT NOT NULL,
        payload_json TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_appgen_inbox_event (
        tenant TEXT,
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        idempotency_key TEXT NOT NULL,
        attempts INTEGER NOT NULL,
        status TEXT NOT NULL,
        received_at TEXT NOT NULL,
        payload_json TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audit_ledger_dead_letter_event (
        tenant TEXT,
        event_id TEXT PRIMARY KEY,
        event_type TEXT NOT NULL,
        idempotency_key TEXT NOT NULL,
        attempts INTEGER NOT NULL,
        reason TEXT NOT NULL,
        recorded_at TEXT NOT NULL,
        payload_json TEXT NOT NULL
    );
    """


class AuditLedgerRepository:
    """Persist standalone audit-ledger state in SQLite."""

    def __init__(self, database_path: str = ":memory:", connection: sqlite3.Connection | None = None):
        self.database_path = database_path
        self.connection = connection or sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self._ensure_schema()

    def close(self) -> None:
        self.connection.close()

    def _ensure_schema(self) -> None:
        self.connection.executescript(standalone_sqlite_schema())
        self.connection.commit()

    def _query_one(self, sql: str, params: tuple[Any, ...] = ()) -> dict | None:
        return _row_to_dict(self.connection.execute(sql, params).fetchone())

    def _query_all(self, sql: str, params: tuple[Any, ...] = ()) -> tuple[dict, ...]:
        rows = self.connection.execute(sql, params).fetchall()
        return tuple(_row_to_dict(row) for row in rows if row is not None)

    def repository_contract(self) -> dict:
        return {
            "format": "appgen.audit-ledger-standalone-repository.v1",
            "ok": True,
            "pbc": "audit_ledger",
            "repository": "AuditLedgerRepository",
            "database_path": self.database_path,
            "runtime_backend_allowlist": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS,
            "tables": (
                "audit_ledger_configuration",
                "audit_ledger_parameter",
                "audit_ledger_rule",
                "audit_ledger_audit_event",
                "audit_ledger_signature_chain",
                "audit_ledger_retention_policy",
                "audit_ledger_forensic_export",
                "audit_ledger_access_evidence",
                "audit_ledger_control_assertion",
                "audit_ledger_projection_link",
                "audit_ledger_appgen_outbox_event",
                "audit_ledger_appgen_inbox_event",
                "audit_ledger_dead_letter_event",
            ),
            "side_effects": (),
        }

    def load_state(self) -> dict:
        state = audit_ledger_empty_state()
        configuration = self._query_one(
            "SELECT * FROM audit_ledger_configuration ORDER BY rowid DESC LIMIT 1"
        )
        if configuration:
            state["configuration"] = {
                "database_backend": configuration["database_backend"],
                "event_topic": configuration["event_topic"],
                "retry_limit": configuration["retry_limit"],
                "signature_algorithm": configuration["signature_algorithm"],
                "default_timezone": configuration["default_timezone"],
                "allowed_classifications": tuple(
                    _json_load(configuration["allowed_classifications_json"], [])
                ),
                "export_modes": tuple(_json_load(configuration["export_modes_json"], [])),
                "workbench_limit": configuration["workbench_limit"],
                "ok": True,
                "event_contract": "AppGen-X",
                "allowed_database_backends": AUDIT_LEDGER_ALLOWED_DATABASE_BACKENDS,
                "stream_engine_picker_visible": False,
                "user_selectable_event_contract": False,
            }

        for row in self._query_all("SELECT * FROM audit_ledger_parameter ORDER BY parameter_id"):
            state["parameters"][row["name"]] = _json_load(row["value"], row["value"])

        for row in self._query_all("SELECT * FROM audit_ledger_rule ORDER BY rule_id"):
            state["rules"][row["rule_id"]] = {
                "tenant": row["tenant"],
                "rule_id": row["rule_id"],
                "scope": row["scope"],
                "classification": row["classification"],
                "minimum_retention_days": row["minimum_retention_days"],
                "requires_legal_hold_review": _bool_value(row["requires_legal_hold_review"]),
                "requires_export_approval": _bool_value(row["requires_export_approval"]),
                "severity": row["severity"],
                "status": row["status"],
                "enabled": row["status"] == "active",
            }

        for row in self._query_all(
            "SELECT * FROM audit_ledger_audit_event ORDER BY tenant, sequence, audit_id"
        ):
            state["audit_events"][row["audit_id"]] = {
                "tenant": row["tenant"],
                "audit_id": row["audit_id"],
                "source_pbc": row["source_pbc"],
                "aggregate_id": row["aggregate_id"],
                "actor": row["actor"],
                "action": row["action"],
                "classification": row["classification"],
                "payload_hash": row["payload_hash"],
                "payload": _json_load(row["payload_json"], {}),
                "sequence": row["sequence"],
                "previous_hash": row["previous_hash"],
                "event_hash": row["event_hash"],
                "signature": row["signature"],
                "signature_algorithm": row["signature_algorithm"],
                "canonicalization_profile": row["canonicalization_profile"],
                "canonical_payload": _json_load(row["canonical_payload_json"], {}),
                "occurred_at": row["occurred_at"],
                "timestamp_basis": row["timestamp_basis"],
                "causality": _json_load(row["causality_json"], {}),
                "correction": _json_load(row["correction_json"], None),
                "admissibility": _json_load(row["admissibility_json"], {}),
                "tamper_risk": float(row["tamper_risk"]),
                "sealed": _bool_value(row["sealed"]),
            }

        for row in self._query_all(
            "SELECT * FROM audit_ledger_signature_chain ORDER BY tenant, sequence"
        ):
            state["signature_chain"][row["audit_id"]] = {
                "tenant": row["tenant"],
                "chain_link_id": row["chain_link_id"],
                "audit_id": row["audit_id"],
                "sequence": row["sequence"],
                "previous_hash": row["previous_hash"],
                "event_hash": row["event_hash"],
                "signature": row["signature"],
                "payload_hash": row["payload_hash"],
                "verified": _bool_value(row["verified"]),
            }

        for row in self._query_all(
            "SELECT * FROM audit_ledger_retention_policy ORDER BY policy_id"
        ):
            state["retention_policies"][row["policy_id"]] = {
                "tenant": row["tenant"],
                "policy_id": row["policy_id"],
                "classification": row["classification"],
                "retention_days": row["retention_days"],
                "legal_hold": _bool_value(row["legal_hold"]),
                "disposal_action": row["disposal_action"],
                "status": row["status"],
            }

        for row in self._query_all(
            "SELECT * FROM audit_ledger_forensic_export ORDER BY export_id"
        ):
            state["forensic_exports"][row["export_id"]] = {
                "tenant": row["tenant"],
                "export_id": row["export_id"],
                "classification": row["classification"],
                "requested_by": row["requested_by"],
                "purpose": row["purpose"],
                "event_count": row["event_count"],
                "checksum": row["checksum"],
                "proof_bundle": row["proof_bundle"],
                "status": row["status"],
                "approval_required": _bool_value(row["approval_required"]),
                "selected_fields": tuple(_json_load(row["selected_fields_json"], [])),
                "withheld_fields": tuple(_json_load(row["withheld_fields_json"], [])),
                "risk_flags": tuple(_json_load(row["risk_flags_json"], [])),
                "proof_coverage": _json_load(row["proof_coverage_json"], {}),
                "verifier_instructions": tuple(
                    _json_load(row["verifier_instructions_json"], [])
                ),
                "chain_of_custody": tuple(_json_load(row["chain_of_custody_json"], [])),
            }

        for row in self._query_all(
            "SELECT * FROM audit_ledger_access_evidence ORDER BY evidence_id"
        ):
            state["access_evidence"][row["evidence_id"]] = {
                "tenant": row["tenant"],
                "evidence_id": row["evidence_id"],
                "principal": row["principal"],
                "resource": row["resource"],
                "action": row["action"],
                "decision": row["decision"],
                "context_hash": row["context_hash"],
                "context": _json_load(row["context_json"], {}),
                "policy_source": row["policy_source"],
            }

        for row in self._query_all(
            "SELECT * FROM audit_ledger_control_assertion ORDER BY control_id"
        ):
            state["control_assertions"][row["control_id"]] = {
                "tenant": row["tenant"],
                "control_id": row["control_id"],
                "control": row["control_name"],
                "status": row["status"],
                "severity": row["severity"],
                "evidence_hash": row["evidence_hash"],
                "evidence": tuple(_json_load(row["evidence_json"], [])),
                "release_blocking": _bool_value(row["release_blocking"]),
                "remediation": row["remediation"],
            }

        for row in self._query_all(
            "SELECT * FROM audit_ledger_projection_link ORDER BY projection_id"
        ):
            state["projections"][row["projection_id"]] = {
                "tenant": row["tenant"],
                "projection_id": row["projection_id"],
                "audit_id": row["audit_id"],
                "target_system": row["target_system"],
                "systems": tuple(_json_load(row["systems_json"], [])),
                "projection_hash": row["projection_hash"],
                "handoff_status": row["handoff_status"],
                "handoffs": tuple(_json_load(row["handoffs_json"], [])),
            }

        outbox = self._query_all("SELECT * FROM audit_ledger_appgen_outbox_event ORDER BY event_id")
        state["outbox"] = [
            {
                "tenant": row["tenant"],
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "topic": row["topic"],
                "idempotency_key": row["idempotency_key"],
                "status": row["status"],
                "audit_hash": row["audit_hash"],
                "payload": _json_load(row["payload_json"], {}),
            }
            for row in outbox
        ]
        state["events"] = [
            {
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "tenant": row["tenant"],
                "aggregate_id": _json_load(row["payload_json"], {}).get("audit_id") or row["event_id"],
                "payload": _json_load(row["payload_json"], {}),
                "hash": row["audit_hash"],
            }
            for row in outbox
        ]

        inbox = self._query_all("SELECT * FROM audit_ledger_appgen_inbox_event ORDER BY event_id")
        state["inbox"] = [
            {
                "tenant": row["tenant"],
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "idempotency_key": row["idempotency_key"],
                "attempts": row["attempts"],
                "status": row["status"],
                "received_at": row["received_at"],
                "payload": _json_load(row["payload_json"], {}),
            }
            for row in inbox
        ]
        state["handled_events"] = {
            row["idempotency_key"]: {
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "status": row["status"],
                "attempts": row["attempts"],
                "idempotency_key": row["idempotency_key"],
            }
            for row in inbox
        }
        state["retry_evidence"] = [
            {
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "attempts": row["attempts"],
                "status": row["status"],
            }
            for row in inbox
            if row["status"] in {"retrying", "dead_letter"}
        ]

        dead_letters = self._query_all(
            "SELECT * FROM audit_ledger_dead_letter_event ORDER BY event_id"
        )
        dead_letter_rows = [
            {
                "tenant": row["tenant"],
                "event_id": row["event_id"],
                "event_type": row["event_type"],
                "idempotency_key": row["idempotency_key"],
                "attempts": row["attempts"],
                "reason": row["reason"],
                "recorded_at": row["recorded_at"],
                "payload": _json_load(row["payload_json"], {}),
            }
            for row in dead_letters
        ]
        state["dead_letters"] = list(dead_letter_rows)
        state["dead_letter"] = list(dead_letter_rows)
        return state

    def _replace_rows(self, table: str, columns: tuple[str, ...], rows: list[dict]) -> None:
        self.connection.execute(f"DELETE FROM {table}")
        placeholders = ", ".join("?" for _ in columns)
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        for row in rows:
            self.connection.execute(sql, tuple(row[column] for column in columns))

    def persist_state(self, state: dict) -> dict:
        configuration_rows = []
        configuration = state.get("configuration", {})
        if configuration.get("ok"):
            configuration_rows.append(
                {
                    "tenant": "platform",
                    "configuration_id": "audit_ledger:default",
                    "database_backend": configuration["database_backend"],
                    "event_topic": configuration["event_topic"],
                    "retry_limit": int(configuration["retry_limit"]),
                    "signature_algorithm": configuration["signature_algorithm"],
                    "default_timezone": configuration["default_timezone"],
                    "allowed_classifications_json": _json_dump(
                        tuple(configuration.get("allowed_classifications", ()))
                    ),
                    "export_modes_json": _json_dump(tuple(configuration.get("export_modes", ()))),
                    "workbench_limit": int(configuration.get("workbench_limit", 100)),
                }
            )
        self._replace_rows(
            "audit_ledger_configuration",
            (
                "tenant",
                "configuration_id",
                "database_backend",
                "event_topic",
                "retry_limit",
                "signature_algorithm",
                "default_timezone",
                "allowed_classifications_json",
                "export_modes_json",
                "workbench_limit",
            ),
            configuration_rows,
        )

        self._replace_rows(
            "audit_ledger_parameter",
            ("tenant", "parameter_id", "name", "value"),
            [
                {
                    "tenant": "platform",
                    "parameter_id": f"parameter:{name}",
                    "name": name,
                    "value": _json_dump(value),
                }
                for name, value in sorted(state.get("parameters", {}).items())
            ],
        )

        self._replace_rows(
            "audit_ledger_rule",
            (
                "tenant",
                "rule_id",
                "scope",
                "classification",
                "minimum_retention_days",
                "requires_legal_hold_review",
                "requires_export_approval",
                "severity",
                "status",
            ),
            [
                {
                    "tenant": rule["tenant"],
                    "rule_id": rule["rule_id"],
                    "scope": rule["scope"],
                    "classification": rule["classification"],
                    "minimum_retention_days": int(rule["minimum_retention_days"]),
                    "requires_legal_hold_review": int(bool(rule.get("requires_legal_hold_review"))),
                    "requires_export_approval": int(bool(rule.get("requires_export_approval"))),
                    "severity": rule["severity"],
                    "status": rule["status"],
                }
                for rule in sorted(state.get("rules", {}).values(), key=lambda item: item["rule_id"])
            ],
        )

        self._replace_rows(
            "audit_ledger_audit_event",
            (
                "tenant",
                "audit_id",
                "source_pbc",
                "aggregate_id",
                "actor",
                "action",
                "classification",
                "payload_hash",
                "payload_json",
                "sequence",
                "previous_hash",
                "event_hash",
                "signature",
                "signature_algorithm",
                "canonicalization_profile",
                "canonical_payload_json",
                "occurred_at",
                "timestamp_basis",
                "causality_json",
                "correction_json",
                "admissibility_json",
                "tamper_risk",
                "sealed",
            ),
            [
                {
                    "tenant": event["tenant"],
                    "audit_id": event["audit_id"],
                    "source_pbc": event["source_pbc"],
                    "aggregate_id": event["aggregate_id"],
                    "actor": event["actor"],
                    "action": event["action"],
                    "classification": event["classification"],
                    "payload_hash": event["payload_hash"],
                    "payload_json": _json_dump(event.get("payload", {})),
                    "sequence": int(event["sequence"]),
                    "previous_hash": event["previous_hash"],
                    "event_hash": event["event_hash"],
                    "signature": event["signature"],
                    "signature_algorithm": event.get("signature_algorithm", "dilithium3_simulated"),
                    "canonicalization_profile": event.get("canonicalization_profile", ""),
                    "canonical_payload_json": _json_dump(event.get("canonical_payload", {})),
                    "occurred_at": event.get("occurred_at", ""),
                    "timestamp_basis": event.get("timestamp_basis", ""),
                    "causality_json": _json_dump(event.get("causality", {})),
                    "correction_json": _json_dump(event.get("correction")),
                    "admissibility_json": _json_dump(event.get("admissibility", {})),
                    "tamper_risk": float(event.get("tamper_risk", 0.0)),
                    "sealed": int(bool(event.get("sealed"))),
                }
                for event in sorted(state.get("audit_events", {}).values(), key=lambda item: item["sequence"])
            ],
        )

        self._replace_rows(
            "audit_ledger_signature_chain",
            (
                "tenant",
                "chain_link_id",
                "audit_id",
                "sequence",
                "previous_hash",
                "event_hash",
                "signature",
                "payload_hash",
                "verified",
            ),
            [
                {
                    "tenant": chain["tenant"],
                    "chain_link_id": chain["chain_link_id"],
                    "audit_id": chain["audit_id"],
                    "sequence": int(chain["sequence"]),
                    "previous_hash": chain["previous_hash"],
                    "event_hash": chain["event_hash"],
                    "signature": chain["signature"],
                    "payload_hash": chain["payload_hash"],
                    "verified": int(bool(chain["verified"])),
                }
                for chain in sorted(state.get("signature_chain", {}).values(), key=lambda item: item["sequence"])
            ],
        )

        self._replace_rows(
            "audit_ledger_retention_policy",
            (
                "tenant",
                "policy_id",
                "classification",
                "retention_days",
                "legal_hold",
                "disposal_action",
                "status",
            ),
            [
                {
                    "tenant": policy["tenant"],
                    "policy_id": policy["policy_id"],
                    "classification": policy["classification"],
                    "retention_days": int(policy["retention_days"]),
                    "legal_hold": int(bool(policy["legal_hold"])),
                    "disposal_action": policy["disposal_action"],
                    "status": policy["status"],
                }
                for policy in sorted(state.get("retention_policies", {}).values(), key=lambda item: item["policy_id"])
            ],
        )

        self._replace_rows(
            "audit_ledger_forensic_export",
            (
                "tenant",
                "export_id",
                "classification",
                "requested_by",
                "purpose",
                "event_count",
                "checksum",
                "proof_bundle",
                "status",
                "approval_required",
                "selected_fields_json",
                "withheld_fields_json",
                "risk_flags_json",
                "proof_coverage_json",
                "verifier_instructions_json",
                "chain_of_custody_json",
            ),
            [
                {
                    "tenant": export["tenant"],
                    "export_id": export["export_id"],
                    "classification": export["classification"],
                    "requested_by": export["requested_by"],
                    "purpose": export.get("purpose", "forensic_export"),
                    "event_count": int(export["event_count"]),
                    "checksum": export["checksum"],
                    "proof_bundle": export["proof_bundle"],
                    "status": export["status"],
                    "approval_required": int(bool(export.get("approval_required"))),
                    "selected_fields_json": _json_dump(tuple(export.get("selected_fields", ()))),
                    "withheld_fields_json": _json_dump(tuple(export.get("withheld_fields", ()))),
                    "risk_flags_json": _json_dump(tuple(export.get("risk_flags", ()))),
                    "proof_coverage_json": _json_dump(export.get("proof_coverage", {})),
                    "verifier_instructions_json": _json_dump(tuple(export.get("verifier_instructions", ()))),
                    "chain_of_custody_json": _json_dump(tuple(export.get("chain_of_custody", ()))),
                }
                for export in sorted(state.get("forensic_exports", {}).values(), key=lambda item: item["export_id"])
            ],
        )

        self._replace_rows(
            "audit_ledger_access_evidence",
            (
                "tenant",
                "evidence_id",
                "principal",
                "resource",
                "action",
                "decision",
                "context_hash",
                "context_json",
                "policy_source",
            ),
            [
                {
                    "tenant": evidence["tenant"],
                    "evidence_id": evidence["evidence_id"],
                    "principal": evidence["principal"],
                    "resource": evidence["resource"],
                    "action": evidence["action"],
                    "decision": evidence["decision"],
                    "context_hash": evidence["context_hash"],
                    "context_json": _json_dump(evidence.get("context", {})),
                    "policy_source": evidence["policy_source"],
                }
                for evidence in sorted(state.get("access_evidence", {}).values(), key=lambda item: item["evidence_id"])
            ],
        )

        self._replace_rows(
            "audit_ledger_control_assertion",
            (
                "tenant",
                "control_id",
                "control_name",
                "status",
                "severity",
                "evidence_hash",
                "evidence_json",
                "release_blocking",
                "remediation",
            ),
            [
                {
                    "tenant": assertion["tenant"],
                    "control_id": assertion["control_id"],
                    "control_name": assertion["control"],
                    "status": assertion["status"],
                    "severity": assertion["severity"],
                    "evidence_hash": assertion["evidence_hash"],
                    "evidence_json": _json_dump(tuple(assertion.get("evidence", ()))),
                    "release_blocking": int(bool(assertion["release_blocking"])),
                    "remediation": assertion.get("remediation"),
                }
                for assertion in sorted(state.get("control_assertions", {}).values(), key=lambda item: item["control_id"])
            ],
        )

        self._replace_rows(
            "audit_ledger_projection_link",
            (
                "tenant",
                "projection_id",
                "audit_id",
                "target_system",
                "systems_json",
                "projection_hash",
                "handoff_status",
                "handoffs_json",
            ),
            [
                {
                    "tenant": projection["tenant"],
                    "projection_id": projection["projection_id"],
                    "audit_id": projection["audit_id"],
                    "target_system": projection["target_system"],
                    "systems_json": _json_dump(tuple(projection.get("systems", ()))),
                    "projection_hash": projection["projection_hash"],
                    "handoff_status": projection["handoff_status"],
                    "handoffs_json": _json_dump(tuple(projection.get("handoffs", ()))),
                }
                for projection in sorted(state.get("projections", {}).values(), key=lambda item: item["projection_id"])
            ],
        )

        self._replace_rows(
            "audit_ledger_appgen_outbox_event",
            (
                "tenant",
                "event_id",
                "event_type",
                "topic",
                "idempotency_key",
                "status",
                "audit_hash",
                "payload_json",
            ),
            [
                {
                    "tenant": item["tenant"],
                    "event_id": item["event_id"],
                    "event_type": item["event_type"],
                    "topic": item["topic"],
                    "idempotency_key": item["idempotency_key"],
                    "status": item["status"],
                    "audit_hash": item["audit_hash"],
                    "payload_json": _json_dump(item.get("payload", {})),
                }
                for item in state.get("outbox", [])
            ],
        )

        self._replace_rows(
            "audit_ledger_appgen_inbox_event",
            (
                "tenant",
                "event_id",
                "event_type",
                "idempotency_key",
                "attempts",
                "status",
                "received_at",
                "payload_json",
            ),
            [
                {
                    "tenant": item.get("tenant"),
                    "event_id": item["event_id"],
                    "event_type": item["event_type"],
                    "idempotency_key": item["idempotency_key"],
                    "attempts": int(item["attempts"]),
                    "status": item["status"],
                    "received_at": item["received_at"],
                    "payload_json": _json_dump(item.get("payload", {})),
                }
                for item in state.get("inbox", [])
            ],
        )

        dead_letters = state.get("dead_letters", state.get("dead_letter", []))
        self._replace_rows(
            "audit_ledger_dead_letter_event",
            (
                "tenant",
                "event_id",
                "event_type",
                "idempotency_key",
                "attempts",
                "reason",
                "recorded_at",
                "payload_json",
            ),
            [
                {
                    "tenant": item.get("tenant"),
                    "event_id": item["event_id"],
                    "event_type": item["event_type"],
                    "idempotency_key": item["idempotency_key"],
                    "attempts": int(item["attempts"]),
                    "reason": item["reason"],
                    "recorded_at": item["recorded_at"],
                    "payload_json": _json_dump(item.get("payload", {})),
                }
                for item in dead_letters
            ],
        )
        self.connection.commit()
        return {"ok": True, "state": self.load_state(), "side_effects": ()}

    def _run(self, operation, *args, **kwargs) -> dict:
        current_state = self.load_state()
        result = operation(current_state, *args, **kwargs)
        if result.get("state") is not None:
            persisted = self.persist_state(result["state"])
            result = {**result, "state": persisted["state"]}
        return result

    def configure_runtime(self, configuration: dict) -> dict:
        return self._run(audit_ledger_configure_runtime, configuration)

    def set_parameter(self, name: str, value: Any) -> dict:
        return self._run(audit_ledger_set_parameter, name, value)

    def register_rule(self, rule: dict) -> dict:
        return self._run(audit_ledger_register_rule, rule)

    def receive_event(self, envelope: dict, *, simulate_failure: bool = False) -> dict:
        return self._run(audit_ledger_receive_event, envelope, simulate_failure=simulate_failure)

    def record_audit_event(self, audit_event: dict) -> dict:
        return self._run(audit_ledger_record_audit_event, audit_event)

    def record_access_evidence(self, evidence: dict) -> dict:
        return self._run(audit_ledger_record_access_evidence, evidence)

    def define_retention_policy(self, policy: dict) -> dict:
        return self._run(audit_ledger_define_retention_policy, policy)

    def assert_control(self, assertion: dict) -> dict:
        return self._run(audit_ledger_assert_control, assertion)

    def prepare_forensic_export(self, export: dict) -> dict:
        return self._run(audit_ledger_prepare_forensic_export, export)

    def verify_signature_chain(self, *, tenant: str) -> dict:
        return self._run(audit_ledger_verify_signature_chain, tenant=tenant)

    def publish_audit_projection(self, audit_id: str, *, systems: tuple[str, ...]) -> dict:
        return self._run(audit_ledger_publish_audit_projection, audit_id, systems=systems)

    def build_workbench(self, *, tenant: str) -> dict:
        state = self.load_state()
        snapshot = audit_ledger_build_workbench_view(state, tenant=tenant)
        return {"ok": True, "tenant": tenant, "snapshot": snapshot, "state": state, "side_effects": ()}

    def release_snapshot(self, *, tenant: str) -> dict:
        state = self.load_state()
        notarization = audit_ledger_build_notarization_bundle(state, tenant=tenant)
        release_evidence = audit_ledger_build_release_evidence()
        return {
            "ok": notarization["ok"] and release_evidence["ok"],
            "tenant": tenant,
            "notarization": notarization["bundle"],
            "release_evidence": release_evidence,
            "side_effects": (),
        }

    def ledger_summary(self, *, tenant: str) -> dict:
        state = self.load_state()
        snapshot = audit_ledger_build_workbench_view(state, tenant=tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "event_count": snapshot["event_count"],
            "export_count": snapshot["export_count"],
            "control_count": snapshot["control_count"],
            "pending_export_approval_count": snapshot["pending_export_approval_count"],
            "outbox_count": len(state.get("outbox", [])),
            "inbox_count": len(state.get("inbox", [])),
            "side_effects": (),
        }


def repository_smoke_test() -> dict:
    """Exercise standalone persistence and reload."""
    repository = AuditLedgerRepository()
    try:
        configured = repository.configure_runtime(
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.audit.events",
                "retry_limit": 3,
                "signature_algorithm": "dilithium3_simulated",
                "allowed_classifications": ("public", "internal", "regulated"),
                "export_modes": ("proof_bundle", "forensic_archive"),
                "default_timezone": "UTC",
                "workbench_limit": 100,
            }
        )
        parameter = repository.set_parameter("retention_days", 2555)
        rule = repository.register_rule(
            {
                "rule_id": "audit_ledger.release_gate",
                "tenant": "tenant_smoke",
                "scope": "export",
                "classification": "regulated",
                "minimum_retention_days": 2555,
                "requires_legal_hold_review": True,
                "requires_export_approval": True,
                "severity": "blocking",
                "status": "active",
            }
        )
        event = repository.record_audit_event(
            {
                "audit_id": "audit_smoke",
                "tenant": "tenant_smoke",
                "source_pbc": "gateway_route_projection",
                "aggregate_id": "route_smoke",
                "actor": "ops_user",
                "action": "publish_route",
                "classification": "regulated",
                "payload": {"route_id": "route_smoke", "method": "POST"},
                "occurred_at": "2026-05-29T08:00:00Z",
            }
        )
        export = repository.prepare_forensic_export(
            {
                "export_id": "export_smoke",
                "tenant": "tenant_smoke",
                "classification": "regulated",
                "requested_by": "auditor",
                "purpose": "incident_review",
                "disclosure": ("audit_id", "actor", "action", "payload_hash"),
            }
        )
        verified = repository.verify_signature_chain(tenant="tenant_smoke")
        summary = repository.ledger_summary(tenant="tenant_smoke")
        return {
            "ok": configured["ok"]
            and parameter["ok"]
            and rule["ok"]
            and event["ok"]
            and export["ok"]
            and verified["ok"]
            and summary["event_count"] == 1,
            "repository": repository.repository_contract(),
            "summary": summary,
            "side_effects": (),
        }
    finally:
        repository.close()
