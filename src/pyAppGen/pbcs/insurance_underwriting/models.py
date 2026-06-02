"""Owned schema metadata and sqlite-backed standalone store for insurance underwriting."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .config import DEFAULT_RUNTIME_PARAMETERS, DEFAULT_RULES, evaluate_rule
from .events import CONSUMED, EMITTED, build_event_envelope


PBC_KEY = "insurance_underwriting"
MIGRATION_PATH = Path(__file__).with_name("migrations") / "001_initial.sql"


def _field(
    name: str,
    field_type: str,
    *,
    required: bool = True,
    primary_key: bool = False,
    nullable: bool | None = None,
) -> dict:
    return {
        "name": name,
        "type": field_type,
        "required": required,
        "primary_key": primary_key,
        "nullable": not required if nullable is None else nullable,
    }


def _owned(logical_table: str, fields: tuple[dict, ...]) -> dict:
    return {
        "logical_table": logical_table,
        "owned_table": f"{PBC_KEY}_{logical_table}",
        "fields": fields,
        "owned_by": PBC_KEY,
    }


OWNED_SCHEMA = {
    "schema": PBC_KEY,
    "table_prefix": f"{PBC_KEY}_",
    "tables": (
        _owned(
            "underwriting_submission",
            (
                _field("submission_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("product_line", "string"),
                _field("applicant_name", "string"),
                _field("jurisdiction", "string"),
                _field("source", "string", required=False),
                _field("broker_code", "string", required=False),
                _field("requested_limit", "decimal"),
                _field("declared_revenue", "decimal", required=False),
                _field("completeness_score", "decimal"),
                _field("lifecycle_state", "string"),
                _field("referral_flag", "boolean"),
                _field("effective_date", "date", required=False),
                _field("exposure_locations_json", "json"),
                _field("prior_losses_json", "json"),
                _field("documents_json", "json"),
                _field("metadata_json", "json"),
                _field("created_at", "datetime"),
                _field("updated_at", "datetime"),
            ),
        ),
        _owned(
            "risk_profile",
            (
                _field("risk_profile_id", "string", primary_key=True),
                _field("submission_id", "string"),
                _field("tenant", "string"),
                _field("industry_code", "string"),
                _field("hazard_score", "decimal"),
                _field("catastrophe_score", "decimal"),
                _field("prior_loss_count", "integer"),
                _field("appetite_result", "string"),
                _field("risk_notes", "string", required=False),
                _field("hazard_factors_json", "json"),
                _field("financial_signals_json", "json"),
                _field("created_at", "datetime"),
                _field("updated_at", "datetime"),
            ),
        ),
        _owned(
            "rating_factor",
            (
                _field("factor_id", "string", primary_key=True),
                _field("submission_id", "string"),
                _field("tenant", "string"),
                _field("factor_type", "string"),
                _field("selected_value", "decimal"),
                _field("weight", "decimal"),
                _field("source", "string"),
                _field("override_reason", "string", required=False),
                _field("supported", "boolean"),
                _field("transformation_json", "json"),
                _field("created_at", "datetime"),
            ),
        ),
        _owned(
            "quote",
            (
                _field("quote_id", "string", primary_key=True),
                _field("submission_id", "string"),
                _field("tenant", "string"),
                _field("version", "integer"),
                _field("scenario_name", "string"),
                _field("premium", "decimal"),
                _field("rate", "decimal"),
                _field("status", "string"),
                _field("valid_until", "date"),
                _field("subjectivity_count", "integer"),
                _field("subjectivities_json", "json"),
                _field("exclusions_json", "json"),
                _field("pricing_trace_json", "json"),
                _field("created_at", "datetime"),
            ),
        ),
        _owned(
            "underwriting_decision",
            (
                _field("decision_id", "string", primary_key=True),
                _field("submission_id", "string"),
                _field("quote_id", "string"),
                _field("tenant", "string"),
                _field("decision_type", "string"),
                _field("status", "string"),
                _field("authority_level", "string"),
                _field("approved_by", "string", required=False),
                _field("rationale", "string", required=False),
                _field("referral_open", "boolean"),
                _field("decision_packet_json", "json"),
                _field("approved_at", "datetime", required=False),
                _field("created_at", "datetime"),
            ),
        ),
        _owned(
            "bind_package",
            (
                _field("bind_package_id", "string", primary_key=True),
                _field("submission_id", "string"),
                _field("quote_id", "string"),
                _field("tenant", "string"),
                _field("status", "string"),
                _field("checklist_json", "json"),
                _field("subjectivities_json", "json"),
                _field("missing_items_json", "json"),
                _field("handoff_event_id", "string", required=False),
                _field("created_at", "datetime"),
            ),
        ),
        _owned(
            "exclusion",
            (
                _field("exclusion_id", "string", primary_key=True),
                _field("submission_id", "string"),
                _field("quote_id", "string", required=False),
                _field("tenant", "string"),
                _field("clause_code", "string"),
                _field("reason", "string"),
                _field("customer_explanation", "string"),
                _field("approval_required", "boolean"),
                _field("approved_by", "string", required=False),
                _field("created_at", "datetime"),
            ),
        ),
        _owned(
            "insurance_underwriting_policy_rule",
            (
                _field("rule_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("rule_type", "string"),
                _field("version", "integer"),
                _field("status", "string"),
                _field("definition_json", "json"),
                _field("compiled_hash", "string"),
                _field("created_at", "datetime"),
                _field("updated_at", "datetime"),
            ),
        ),
        _owned(
            "insurance_underwriting_runtime_parameter",
            (
                _field("parameter_name", "string", primary_key=True),
                _field("tenant", "string"),
                _field("value_json", "json"),
                _field("bounded_min", "decimal", required=False),
                _field("bounded_max", "decimal", required=False),
                _field("updated_at", "datetime"),
            ),
        ),
        _owned(
            "insurance_underwriting_schema_extension",
            (
                _field("extension_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("table_name", "string"),
                _field("field_name", "string"),
                _field("field_type", "string"),
                _field("status", "string"),
                _field("approved_by", "string", required=False),
                _field("created_at", "datetime"),
            ),
        ),
        _owned(
            "insurance_underwriting_control_assertion",
            (
                _field("assertion_id", "string", primary_key=True),
                _field("tenant", "string"),
                _field("control_name", "string"),
                _field("subject", "string"),
                _field("status", "string"),
                _field("evidence_json", "json"),
                _field("checked_at", "datetime"),
            ),
        ),
        _owned(
            "insurance_underwriting_governed_model",
            (
                _field("model_key", "string", primary_key=True),
                _field("tenant", "string"),
                _field("version", "string"),
                _field("domain", "string"),
                _field("status", "string"),
                _field("freshness_date", "date"),
                _field("requirements_json", "json"),
                _field("created_at", "datetime"),
            ),
        ),
        _owned(
            "appgen_outbox_event",
            (
                _field("event_id", "string", primary_key=True),
                _field("aggregate_id", "string"),
                _field("aggregate_type", "string"),
                _field("event_type", "string"),
                _field("topic", "string"),
                _field("payload_json", "json"),
                _field("tenant", "string", required=False),
                _field("created_at", "datetime"),
            ),
        ),
        _owned(
            "appgen_inbox_event",
            (
                _field("event_id", "string", primary_key=True),
                _field("event_type", "string"),
                _field("source_pbc", "string", required=False),
                _field("tenant", "string", required=False),
                _field("payload_json", "json"),
                _field("idempotency_key", "string"),
                _field("created_at", "datetime"),
            ),
        ),
        _owned(
            "appgen_dead_letter_event",
            (
                _field("event_id", "string", primary_key=True),
                _field("event_type", "string"),
                _field("tenant", "string", required=False),
                _field("payload_json", "json"),
                _field("reason", "string"),
                _field("retry_count", "integer"),
                _field("created_at", "datetime"),
            ),
        ),
    ),
}
OWNED_TABLES = tuple(table["owned_table"] for table in OWNED_SCHEMA["tables"])
BUSINESS_TABLES = OWNED_TABLES[:-3]
EVENT_TABLES = OWNED_TABLES[-3:]


TABLE_SQL = {
    "insurance_underwriting_underwriting_submission": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_underwriting_submission (
            submission_id TEXT PRIMARY KEY,
            tenant TEXT NOT NULL,
            product_line TEXT NOT NULL,
            applicant_name TEXT NOT NULL,
            jurisdiction TEXT NOT NULL,
            source TEXT,
            broker_code TEXT,
            requested_limit REAL NOT NULL,
            declared_revenue REAL,
            completeness_score REAL NOT NULL,
            lifecycle_state TEXT NOT NULL,
            referral_flag INTEGER NOT NULL,
            effective_date TEXT,
            exposure_locations_json TEXT NOT NULL,
            prior_losses_json TEXT NOT NULL,
            documents_json TEXT NOT NULL,
            metadata_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_risk_profile": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_risk_profile (
            risk_profile_id TEXT PRIMARY KEY,
            submission_id TEXT NOT NULL,
            tenant TEXT NOT NULL,
            industry_code TEXT NOT NULL,
            hazard_score REAL NOT NULL,
            catastrophe_score REAL NOT NULL,
            prior_loss_count INTEGER NOT NULL,
            appetite_result TEXT NOT NULL,
            risk_notes TEXT,
            hazard_factors_json TEXT NOT NULL,
            financial_signals_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_rating_factor": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_rating_factor (
            factor_id TEXT PRIMARY KEY,
            submission_id TEXT NOT NULL,
            tenant TEXT NOT NULL,
            factor_type TEXT NOT NULL,
            selected_value REAL NOT NULL,
            weight REAL NOT NULL,
            source TEXT NOT NULL,
            override_reason TEXT,
            supported INTEGER NOT NULL,
            transformation_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_quote": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_quote (
            quote_id TEXT PRIMARY KEY,
            submission_id TEXT NOT NULL,
            tenant TEXT NOT NULL,
            version INTEGER NOT NULL,
            scenario_name TEXT NOT NULL,
            premium REAL NOT NULL,
            rate REAL NOT NULL,
            status TEXT NOT NULL,
            valid_until TEXT NOT NULL,
            subjectivity_count INTEGER NOT NULL,
            subjectivities_json TEXT NOT NULL,
            exclusions_json TEXT NOT NULL,
            pricing_trace_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_underwriting_decision": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_underwriting_decision (
            decision_id TEXT PRIMARY KEY,
            submission_id TEXT NOT NULL,
            quote_id TEXT NOT NULL,
            tenant TEXT NOT NULL,
            decision_type TEXT NOT NULL,
            status TEXT NOT NULL,
            authority_level TEXT NOT NULL,
            approved_by TEXT,
            rationale TEXT,
            referral_open INTEGER NOT NULL,
            decision_packet_json TEXT NOT NULL,
            approved_at TEXT,
            created_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_bind_package": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_bind_package (
            bind_package_id TEXT PRIMARY KEY,
            submission_id TEXT NOT NULL,
            quote_id TEXT NOT NULL,
            tenant TEXT NOT NULL,
            status TEXT NOT NULL,
            checklist_json TEXT NOT NULL,
            subjectivities_json TEXT NOT NULL,
            missing_items_json TEXT NOT NULL,
            handoff_event_id TEXT,
            created_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_exclusion": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_exclusion (
            exclusion_id TEXT PRIMARY KEY,
            submission_id TEXT NOT NULL,
            quote_id TEXT,
            tenant TEXT NOT NULL,
            clause_code TEXT NOT NULL,
            reason TEXT NOT NULL,
            customer_explanation TEXT NOT NULL,
            approval_required INTEGER NOT NULL,
            approved_by TEXT,
            created_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_insurance_underwriting_policy_rule": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_policy_rule (
            rule_id TEXT PRIMARY KEY,
            tenant TEXT NOT NULL,
            rule_type TEXT NOT NULL,
            version INTEGER NOT NULL,
            status TEXT NOT NULL,
            definition_json TEXT NOT NULL,
            compiled_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_insurance_underwriting_runtime_parameter": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_runtime_parameter (
            parameter_name TEXT PRIMARY KEY,
            tenant TEXT NOT NULL,
            value_json TEXT NOT NULL,
            bounded_min REAL,
            bounded_max REAL,
            updated_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_insurance_underwriting_schema_extension": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_schema_extension (
            extension_id TEXT PRIMARY KEY,
            tenant TEXT NOT NULL,
            table_name TEXT NOT NULL,
            field_name TEXT NOT NULL,
            field_type TEXT NOT NULL,
            status TEXT NOT NULL,
            approved_by TEXT,
            created_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_insurance_underwriting_control_assertion": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_control_assertion (
            assertion_id TEXT PRIMARY KEY,
            tenant TEXT NOT NULL,
            control_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            status TEXT NOT NULL,
            evidence_json TEXT NOT NULL,
            checked_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_insurance_underwriting_governed_model": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_insurance_underwriting_governed_model (
            model_key TEXT PRIMARY KEY,
            tenant TEXT NOT NULL,
            version TEXT NOT NULL,
            domain TEXT NOT NULL,
            status TEXT NOT NULL,
            freshness_date TEXT NOT NULL,
            requirements_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_appgen_outbox_event": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_appgen_outbox_event (
            event_id TEXT PRIMARY KEY,
            aggregate_id TEXT NOT NULL,
            aggregate_type TEXT NOT NULL,
            event_type TEXT NOT NULL,
            topic TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            tenant TEXT,
            created_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_appgen_inbox_event": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_appgen_inbox_event (
            event_id TEXT PRIMARY KEY,
            event_type TEXT NOT NULL,
            source_pbc TEXT,
            tenant TEXT,
            payload_json TEXT NOT NULL,
            idempotency_key TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        );
    """,
    "insurance_underwriting_appgen_dead_letter_event": """
        CREATE TABLE IF NOT EXISTS insurance_underwriting_appgen_dead_letter_event (
            event_id TEXT PRIMARY KEY,
            event_type TEXT NOT NULL,
            tenant TEXT,
            payload_json TEXT NOT NULL,
            reason TEXT NOT NULL,
            retry_count INTEGER NOT NULL,
            created_at TEXT NOT NULL
        );
    """,
}


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _stable_hash(value: object) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _dump(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _load(value: Any) -> Any:
    if value in (None, ""):
        return None
    if isinstance(value, (dict, list, tuple)):
        return value
    return json.loads(value)


def migration_alignment_report() -> dict:
    migration_text = MIGRATION_PATH.read_text(encoding="utf-8") if MIGRATION_PATH.exists() else ""
    missing_tables = tuple(
        table for table in OWNED_TABLES if f"CREATE TABLE IF NOT EXISTS {table}" not in migration_text
    )
    return {
        "ok": not missing_tables,
        "migration_path": str(MIGRATION_PATH.relative_to(Path(__file__).parent)),
        "missing_tables": missing_tables,
        "side_effects": (),
    }


class InsuranceUnderwritingStandaloneStore:
    """Package-local sqlite store for standalone underwriting flows."""

    def __init__(self, database_path: str = ":memory:") -> None:
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.apply_schema()
        self._bootstrap_defaults()

    def close(self) -> None:
        self.connection.close()

    def apply_schema(self) -> None:
        migration_sql = MIGRATION_PATH.read_text(encoding="utf-8")
        self.connection.executescript(migration_sql)
        self.connection.commit()

    def _bootstrap_defaults(self) -> None:
        now = _now()
        for rule in DEFAULT_RULES:
            self.connection.execute(
                """
                INSERT OR IGNORE INTO insurance_underwriting_insurance_underwriting_policy_rule (
                    rule_id, tenant, rule_type, version, status, definition_json, compiled_hash, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    rule["rule_id"],
                    "default",
                    rule["rule_type"],
                    1,
                    "active",
                    _dump(rule),
                    _stable_hash(rule),
                    now,
                    now,
                ),
            )
        for name, value in DEFAULT_RUNTIME_PARAMETERS.items():
            self.connection.execute(
                """
                INSERT OR IGNORE INTO insurance_underwriting_insurance_underwriting_runtime_parameter (
                    parameter_name, tenant, value_json, bounded_min, bounded_max, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    "default",
                    _dump(value),
                    0.0 if isinstance(value, (int, float)) else None,
                    100000000.0 if isinstance(value, (int, float)) else None,
                    now,
                ),
            )
        self.connection.commit()

    def _fetchone(self, sql: str, params: tuple[Any, ...] = ()) -> dict | None:
        row = self.connection.execute(sql, params).fetchone()
        return dict(row) if row else None

    def _fetchall(self, sql: str, params: tuple[Any, ...] = ()) -> list[dict]:
        return [dict(row) for row in self.connection.execute(sql, params).fetchall()]

    def _jsonify_record(self, record: dict, json_keys: tuple[str, ...]) -> dict:
        hydrated = dict(record)
        for key in json_keys:
            hydrated[key] = _load(hydrated.get(key))
        return hydrated

    def _write_outbox(self, event_type: str, aggregate_type: str, aggregate_id: str, tenant: str, payload: dict) -> dict:
        envelope = build_event_envelope(event_type, payload, aggregate_id=aggregate_id)
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_appgen_outbox_event (
                event_id, aggregate_id, aggregate_type, event_type, topic, payload_json, tenant, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                envelope["event_id"],
                aggregate_id,
                aggregate_type,
                event_type,
                envelope["topic"],
                _dump(envelope["payload"]),
                tenant,
                envelope["occurred_at"],
            ),
        )
        self.connection.commit()
        return envelope

    def _get_parameter(self, name: str) -> Any:
        row = self._fetchone(
            "SELECT value_json FROM insurance_underwriting_insurance_underwriting_runtime_parameter WHERE parameter_name = ?",
            (name,),
        )
        if not row:
            return DEFAULT_RUNTIME_PARAMETERS[name]
        return _load(row["value_json"])

    def _submission(self, submission_id: str) -> dict | None:
        row = self._fetchone(
            "SELECT * FROM insurance_underwriting_underwriting_submission WHERE submission_id = ?",
            (submission_id,),
        )
        return self._jsonify_record(
            row,
            ("exposure_locations_json", "prior_losses_json", "documents_json", "metadata_json"),
        ) if row else None

    def _latest_risk_profile(self, submission_id: str) -> dict | None:
        row = self._fetchone(
            "SELECT * FROM insurance_underwriting_risk_profile WHERE submission_id = ? ORDER BY created_at DESC LIMIT 1",
            (submission_id,),
        )
        return self._jsonify_record(row, ("hazard_factors_json", "financial_signals_json")) if row else None

    def _latest_quote(self, submission_id: str) -> dict | None:
        row = self._fetchone(
            "SELECT * FROM insurance_underwriting_quote WHERE submission_id = ? ORDER BY version DESC LIMIT 1",
            (submission_id,),
        )
        return self._jsonify_record(row, ("subjectivities_json", "exclusions_json", "pricing_trace_json")) if row else None

    def _latest_decision(self, submission_id: str) -> dict | None:
        row = self._fetchone(
            "SELECT * FROM insurance_underwriting_underwriting_decision WHERE submission_id = ? ORDER BY created_at DESC LIMIT 1",
            (submission_id,),
        )
        return self._jsonify_record(row, ("decision_packet_json",)) if row else None

    def create_submission(self, payload: dict) -> dict:
        required = ("submission_id", "tenant", "product_line", "applicant_name", "jurisdiction", "requested_limit")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
        completeness_inputs = (
            payload.get("applicant_name"),
            payload.get("product_line"),
            payload.get("jurisdiction"),
            payload.get("requested_limit"),
            payload.get("declared_revenue"),
            payload.get("effective_date"),
            bool(payload.get("exposure_locations")),
            bool(payload.get("prior_losses", ())),
            bool(payload.get("documents", ())),
        )
        completeness_score = round(sum(1 for item in completeness_inputs if item) / len(completeness_inputs), 3)
        auto_bind_limit = float(self._get_parameter("auto_bind_limit"))
        referral_flag = bool(payload.get("referral_flag")) or float(payload["requested_limit"]) > auto_bind_limit
        lifecycle_state = "triage" if completeness_score >= 0.75 else "intake_incomplete"
        now = _now()
        row = {
            "submission_id": payload["submission_id"],
            "tenant": payload["tenant"],
            "product_line": payload["product_line"],
            "applicant_name": payload["applicant_name"],
            "jurisdiction": payload["jurisdiction"],
            "source": payload.get("source", "broker_portal"),
            "broker_code": payload.get("broker_code"),
            "requested_limit": float(payload["requested_limit"]),
            "declared_revenue": float(payload.get("declared_revenue", 0.0)) if payload.get("declared_revenue") is not None else None,
            "completeness_score": completeness_score,
            "lifecycle_state": lifecycle_state,
            "referral_flag": int(referral_flag),
            "effective_date": payload.get("effective_date"),
            "exposure_locations_json": _dump(tuple(payload.get("exposure_locations", ()))),
            "prior_losses_json": _dump(tuple(payload.get("prior_losses", ()))),
            "documents_json": _dump(tuple(payload.get("documents", ()))),
            "metadata_json": _dump(dict(payload.get("metadata", {}))),
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_underwriting_submission (
                submission_id, tenant, product_line, applicant_name, jurisdiction, source, broker_code,
                requested_limit, declared_revenue, completeness_score, lifecycle_state, referral_flag,
                effective_date, exposure_locations_json, prior_losses_json, documents_json, metadata_json,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        event = self._write_outbox(
            EMITTED[0],
            "underwriting_submission",
            row["submission_id"],
            row["tenant"],
            {
                "submission_id": row["submission_id"],
                "lifecycle_state": row["lifecycle_state"],
                "completeness_score": completeness_score,
            },
        )
        self.connection.commit()
        return {
            "ok": True,
            "result": {**self._submission(row["submission_id"]), "next_actions": ("build_risk_profile", "review_rating_factor")},
            "event": event,
            "side_effects": (),
        }

    def build_risk_profile(self, payload: dict) -> dict:
        submission = self._submission(payload.get("submission_id", ""))
        if not submission:
            return {"ok": False, "reason": "submission_not_found", "side_effects": ()}
        hazard_factors = tuple(payload.get("hazard_factors", ()))
        prior_loss_count = int(payload.get("prior_loss_count", 0))
        catastrophe_score = float(payload.get("catastrophe_score", 0.0))
        hazard_score = round(min(0.99, 0.2 + 0.09 * len(hazard_factors) + 0.08 * prior_loss_count + catastrophe_score * 0.4), 3)
        appetite_check = evaluate_rule("risk_appetite_screening", {"hazard_score": hazard_score})
        appetite_result = "decline" if payload.get("prohibited_exposure") else appetite_check["outcome"]
        now = _now()
        row = {
            "risk_profile_id": payload.get("risk_profile_id", f"{submission['submission_id']}-risk"),
            "submission_id": submission["submission_id"],
            "tenant": submission["tenant"],
            "industry_code": payload.get("industry_code", "GEN"),
            "hazard_score": hazard_score,
            "catastrophe_score": catastrophe_score,
            "prior_loss_count": prior_loss_count,
            "appetite_result": appetite_result,
            "risk_notes": payload.get("risk_notes"),
            "hazard_factors_json": _dump(hazard_factors),
            "financial_signals_json": _dump(dict(payload.get("financial_signals", {}))),
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_risk_profile (
                risk_profile_id, submission_id, tenant, industry_code, hazard_score, catastrophe_score,
                prior_loss_count, appetite_result, risk_notes, hazard_factors_json, financial_signals_json,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        self.connection.execute(
            "UPDATE insurance_underwriting_underwriting_submission SET lifecycle_state = ?, updated_at = ? WHERE submission_id = ?",
            ("referred" if appetite_result == "refer" else "risk_assessed", now, submission["submission_id"]),
        )
        event = self._write_outbox(
            EMITTED[1],
            "risk_profile",
            row["risk_profile_id"],
            row["tenant"],
            {"submission_id": row["submission_id"], "appetite_result": appetite_result, "hazard_score": hazard_score},
        )
        self.connection.commit()
        return {
            "ok": True,
            "result": self._latest_risk_profile(submission["submission_id"]),
            "event": event,
            "side_effects": (),
        }

    def review_rating_factor(self, payload: dict) -> dict:
        submission = self._submission(payload.get("submission_id", ""))
        if not submission:
            return {"ok": False, "reason": "submission_not_found", "side_effects": ()}
        supported_sources = {"actuarial_projection", "inspection", "portfolio_feedback", "underwriter_override"}
        supported = payload.get("source") in supported_sources
        if payload.get("source") == "underwriter_override" and not payload.get("override_reason"):
            supported = False
        row = {
            "factor_id": payload.get("factor_id", f"{submission['submission_id']}-{payload.get('factor_type', 'factor')}"),
            "submission_id": submission["submission_id"],
            "tenant": submission["tenant"],
            "factor_type": payload.get("factor_type", "base_rate"),
            "selected_value": float(payload.get("selected_value", 1.0)),
            "weight": float(payload.get("weight", 0.25)),
            "source": payload.get("source", "actuarial_projection"),
            "override_reason": payload.get("override_reason"),
            "supported": int(supported),
            "transformation_json": _dump(dict(payload.get("transformation", {}))),
            "created_at": _now(),
        }
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_rating_factor (
                factor_id, submission_id, tenant, factor_type, selected_value, weight, source,
                override_reason, supported, transformation_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        event = self._write_outbox(
            EMITTED[1],
            "rating_factor",
            row["factor_id"],
            row["tenant"],
            {"submission_id": row["submission_id"], "factor_type": row["factor_type"], "supported": bool(row["supported"])} ,
        )
        self.connection.commit()
        return {"ok": supported, "result": {**row, "supported": bool(row["supported"]), "transformation_json": _load(row["transformation_json"])}, "event": event, "side_effects": ()}

    def generate_quote(self, payload: dict) -> dict:
        submission = self._submission(payload.get("submission_id", ""))
        if not submission:
            return {"ok": False, "reason": "submission_not_found", "side_effects": ()}
        gate = evaluate_rule("submission_completeness_gate", {"completeness_score": submission["completeness_score"]})
        if gate["passed"] is not True:
            return {"ok": False, "reason": "submission_incomplete", "gate": gate, "side_effects": ()}
        risk_profile = self._latest_risk_profile(submission["submission_id"])
        if not risk_profile:
            return {"ok": False, "reason": "risk_profile_missing", "side_effects": ()}
        factors = self._fetchall(
            "SELECT * FROM insurance_underwriting_rating_factor WHERE submission_id = ? ORDER BY created_at ASC",
            (submission["submission_id"],),
        )
        factor_adjustment = 1.0 + sum((row["selected_value"] - 1.0) * row["weight"] for row in factors)
        base_rate = float(payload.get("base_rate", 0.014))
        risk_multiplier = 1.0 + float(risk_profile["hazard_score"]) + float(risk_profile["catastrophe_score"]) / 2.0
        premium = round(max(250.0, float(submission["requested_limit"]) * base_rate * max(0.25, factor_adjustment) * risk_multiplier), 2)
        version_row = self._fetchone(
            "SELECT COALESCE(MAX(version), 0) AS version FROM insurance_underwriting_quote WHERE submission_id = ?",
            (submission["submission_id"],),
        )
        subjectivities = tuple(payload.get("subjectivities", ()))
        if not subjectivities and risk_profile["hazard_score"] >= 0.55:
            subjectivities = ({"name": "site_inspection", "satisfied": False},)
        status = "referred" if risk_profile["appetite_result"] == "refer" or submission["referral_flag"] else "rated"
        valid_until = (datetime.now(UTC) + timedelta(days=int(self._get_parameter("quote_validity_days")))).date().isoformat()
        row = {
            "quote_id": payload.get("quote_id", f"{submission['submission_id']}-quote-v{int(version_row['version']) + 1}"),
            "submission_id": submission["submission_id"],
            "tenant": submission["tenant"],
            "version": int(version_row["version"]) + 1,
            "scenario_name": payload.get("scenario_name", "base"),
            "premium": premium,
            "rate": round(base_rate * max(0.25, factor_adjustment) * risk_multiplier, 6),
            "status": status,
            "valid_until": valid_until,
            "subjectivity_count": len(subjectivities),
            "subjectivities_json": _dump(subjectivities),
            "exclusions_json": _dump(tuple(payload.get("exclusions", ()))),
            "pricing_trace_json": _dump(
                {
                    "factor_adjustment": round(factor_adjustment, 4),
                    "risk_multiplier": round(risk_multiplier, 4),
                    "factor_count": len(factors),
                }
            ),
            "created_at": _now(),
        }
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_quote (
                quote_id, submission_id, tenant, version, scenario_name, premium, rate, status,
                valid_until, subjectivity_count, subjectivities_json, exclusions_json, pricing_trace_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        self.connection.execute(
            "UPDATE insurance_underwriting_underwriting_submission SET lifecycle_state = ?, updated_at = ? WHERE submission_id = ?",
            ("quoted" if status == "rated" else "quote_referred", _now(), submission["submission_id"]),
        )
        event = self._write_outbox(
            EMITTED[1],
            "quote",
            row["quote_id"],
            row["tenant"],
            {"submission_id": row["submission_id"], "premium": premium, "status": status},
        )
        self.connection.commit()
        quote = self._latest_quote(submission["submission_id"])
        return {"ok": True, "result": quote, "event": event, "side_effects": ()}

    def issue_underwriting_decision(self, payload: dict) -> dict:
        submission = self._submission(payload.get("submission_id", ""))
        quote = self._fetchone(
            "SELECT * FROM insurance_underwriting_quote WHERE quote_id = ?",
            (payload.get("quote_id", ""),),
        )
        if not submission or not quote:
            return {"ok": False, "reason": "submission_or_quote_missing", "side_effects": ()}
        risk_profile = self._latest_risk_profile(submission["submission_id"])
        today = datetime.now(UTC).date().isoformat()
        if quote["valid_until"] < today:
            decision_type = "decline"
            status = "expired"
        elif risk_profile and risk_profile["appetite_result"] == "decline":
            decision_type = "decline"
            status = "final"
        elif quote["status"] == "referred" or submission["referral_flag"]:
            decision_type = "refer"
            status = "awaiting_referral"
        else:
            decision_type = "approve"
            status = "final"
        packet = {
            "quote_id": quote["quote_id"],
            "submission_id": submission["submission_id"],
            "premium": quote["premium"],
            "appetite_result": risk_profile["appetite_result"] if risk_profile else "unknown",
            "authority_check": evaluate_rule("authority_matrix", {"requested_limit": submission["requested_limit"]}),
        }
        row = {
            "decision_id": payload.get("decision_id", f"{submission['submission_id']}-decision"),
            "submission_id": submission["submission_id"],
            "quote_id": quote["quote_id"],
            "tenant": submission["tenant"],
            "decision_type": decision_type,
            "status": status,
            "authority_level": payload.get("authority_level", "senior"),
            "approved_by": payload.get("approved_by"),
            "rationale": payload.get("rationale", f"Decision based on {packet['appetite_result']} appetite outcome."),
            "referral_open": int(decision_type == "refer"),
            "decision_packet_json": _dump(packet),
            "approved_at": _now() if decision_type == "approve" else None,
            "created_at": _now(),
        }
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_underwriting_decision (
                decision_id, submission_id, quote_id, tenant, decision_type, status, authority_level,
                approved_by, rationale, referral_open, decision_packet_json, approved_at, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        self.connection.execute(
            "UPDATE insurance_underwriting_quote SET status = ? WHERE quote_id = ?",
            ("approved" if decision_type == "approve" else decision_type, quote["quote_id"]),
        )
        self.connection.execute(
            "UPDATE insurance_underwriting_underwriting_submission SET lifecycle_state = ?, updated_at = ? WHERE submission_id = ?",
            (decision_type, _now(), submission["submission_id"]),
        )
        event = self._write_outbox(
            EMITTED[2] if decision_type == "approve" else EMITTED[3],
            "underwriting_decision",
            row["decision_id"],
            row["tenant"],
            {"submission_id": row["submission_id"], "decision_type": decision_type, "status": status},
        )
        self.connection.commit()
        return {"ok": True, "result": self._latest_decision(submission["submission_id"]), "event": event, "side_effects": ()}

    def assemble_bind_package(self, payload: dict) -> dict:
        submission = self._submission(payload.get("submission_id", ""))
        quote = self._fetchone(
            "SELECT * FROM insurance_underwriting_quote WHERE quote_id = ?",
            (payload.get("quote_id", ""),),
        )
        decision = self._latest_decision(payload.get("submission_id", ""))
        if not submission or not quote or not decision:
            return {"ok": False, "reason": "bind_dependencies_missing", "side_effects": ()}
        subjectivities = tuple(payload.get("subjectivities", _load(quote["subjectivities_json"]) or ()))
        missing_items = [
            item["name"]
            for item in subjectivities
            if isinstance(item, dict) and not item.get("satisfied")
        ]
        if payload.get("payment_confirmed") is not True:
            missing_items.append("payment_confirmation")
        if quote["status"] != "approved":
            missing_items.append("approved_quote")
        readiness = evaluate_rule("bind_readiness", {"missing_items": tuple(missing_items)})
        status = "ready_to_bind" if readiness["passed"] else "blocked"
        row = {
            "bind_package_id": payload.get("bind_package_id", f"{submission['submission_id']}-bind"),
            "submission_id": submission["submission_id"],
            "quote_id": quote["quote_id"],
            "tenant": submission["tenant"],
            "status": status,
            "checklist_json": _dump(
                {
                    "payment_confirmed": payload.get("payment_confirmed", False),
                    "documents": tuple(payload.get("documents", ())),
                    "decision_type": decision["decision_type"],
                }
            ),
            "subjectivities_json": _dump(subjectivities),
            "missing_items_json": _dump(tuple(missing_items)),
            "handoff_event_id": None,
            "created_at": _now(),
        }
        if not readiness["passed"]:
            return {"ok": False, "reason": "bind_not_ready", "missing_items": tuple(missing_items), "side_effects": ()}
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_bind_package (
                bind_package_id, submission_id, quote_id, tenant, status, checklist_json,
                subjectivities_json, missing_items_json, handoff_event_id, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        event = self._write_outbox(
            EMITTED[2],
            "bind_package",
            row["bind_package_id"],
            row["tenant"],
            {"submission_id": row["submission_id"], "quote_id": row["quote_id"], "status": status},
        )
        self.connection.execute(
            "UPDATE insurance_underwriting_bind_package SET handoff_event_id = ? WHERE bind_package_id = ?",
            (event["event_id"], row["bind_package_id"]),
        )
        self.connection.execute(
            "UPDATE insurance_underwriting_underwriting_submission SET lifecycle_state = ?, updated_at = ? WHERE submission_id = ?",
            ("bind_ready", _now(), submission["submission_id"]),
        )
        self.connection.commit()
        result = self._fetchone(
            "SELECT * FROM insurance_underwriting_bind_package WHERE bind_package_id = ?",
            (row["bind_package_id"],),
        )
        return {"ok": True, "result": self._jsonify_record(result, ("checklist_json", "subjectivities_json", "missing_items_json")), "event": event, "side_effects": ()}

    def record_exclusion(self, payload: dict) -> dict:
        submission = self._submission(payload.get("submission_id", ""))
        if not submission:
            return {"ok": False, "reason": "submission_not_found", "side_effects": ()}
        row = {
            "exclusion_id": payload.get("exclusion_id", f"{submission['submission_id']}-exclusion-{payload.get('clause_code', 'custom')}"),
            "submission_id": submission["submission_id"],
            "quote_id": payload.get("quote_id"),
            "tenant": submission["tenant"],
            "clause_code": payload.get("clause_code", "CUSTOM"),
            "reason": payload.get("reason", "Underwriting restriction"),
            "customer_explanation": payload.get("customer_explanation", "Coverage narrowed pending underwriting review."),
            "approval_required": int(payload.get("approval_required", True)),
            "approved_by": payload.get("approved_by"),
            "created_at": _now(),
        }
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_exclusion (
                exclusion_id, submission_id, quote_id, tenant, clause_code, reason,
                customer_explanation, approval_required, approved_by, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        event = self._write_outbox(
            EMITTED[1],
            "exclusion",
            row["exclusion_id"],
            row["tenant"],
            {"submission_id": row["submission_id"], "clause_code": row["clause_code"]},
        )
        self.connection.commit()
        return {"ok": True, "result": row, "event": event, "side_effects": ()}

    def register_rule(self, payload: dict) -> dict:
        now = _now()
        rule_id = payload.get("rule_id")
        if not rule_id:
            return {"ok": False, "reason": "rule_id_required", "side_effects": ()}
        rule = {
            "rule_id": rule_id,
            "tenant": payload.get("tenant", "default"),
            "rule_type": payload.get("rule_type", "custom"),
            "version": int(payload.get("version", 1)),
            "status": payload.get("status", "active"),
            "definition_json": _dump(dict(payload.get("definition", payload))),
            "compiled_hash": _stable_hash(payload),
            "created_at": now,
            "updated_at": now,
        }
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_insurance_underwriting_policy_rule (
                rule_id, tenant, rule_type, version, status, definition_json, compiled_hash, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            tuple(rule.values()),
        )
        self.connection.commit()
        return {"ok": True, "result": {**rule, "definition_json": _load(rule["definition_json"])}, "side_effects": ()}

    def set_parameter(self, payload: dict) -> dict:
        name = payload.get("parameter_name") or payload.get("name")
        if not name:
            return {"ok": False, "reason": "parameter_name_required", "side_effects": ()}
        value = payload.get("value")
        now = _now()
        row = {
            "parameter_name": name,
            "tenant": payload.get("tenant", "default"),
            "value_json": _dump(value),
            "bounded_min": payload.get("bounded_min"),
            "bounded_max": payload.get("bounded_max"),
            "updated_at": now,
        }
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_insurance_underwriting_runtime_parameter (
                parameter_name, tenant, value_json, bounded_min, bounded_max, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            tuple(row.values()),
        )
        self.connection.commit()
        return {"ok": True, "result": {**row, "value_json": _load(row["value_json"])}, "side_effects": ()}

    def receive_event(self, payload: dict) -> dict:
        envelope = build_event_envelope(payload.get("event_type", ""), payload)
        tenant = payload.get("tenant") or payload.get("payload", {}).get("tenant")
        if payload.get("event_type") not in CONSUMED:
            self.connection.execute(
                """
                INSERT OR REPLACE INTO insurance_underwriting_appgen_dead_letter_event (
                    event_id, event_type, tenant, payload_json, reason, retry_count, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    envelope["event_id"],
                    payload.get("event_type"),
                    tenant,
                    _dump(payload),
                    "unsupported_event_type",
                    0,
                    _now(),
                ),
            )
            self.connection.commit()
            return {"ok": False, "reason": "unsupported_event_type", "dead_letter_event_id": envelope["event_id"], "side_effects": ()}
        try:
            self.connection.execute(
                """
                INSERT INTO insurance_underwriting_appgen_inbox_event (
                    event_id, event_type, source_pbc, tenant, payload_json, idempotency_key, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    envelope["event_id"],
                    payload.get("event_type"),
                    payload.get("source_pbc"),
                    tenant,
                    _dump(payload.get("payload", payload)),
                    payload.get("idempotency_key", envelope["idempotency_key"]),
                    _now(),
                ),
            )
        except sqlite3.IntegrityError:
            return {"ok": True, "duplicate": True, "event_id": envelope["event_id"], "side_effects": ()}
        self.connection.execute(
            """
            INSERT OR REPLACE INTO insurance_underwriting_insurance_underwriting_control_assertion (
                assertion_id, tenant, control_name, subject, status, evidence_json, checked_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                f"event-{envelope['event_id']}",
                tenant or "default",
                "consumed_event_capture",
                payload.get("event_type"),
                "captured",
                _dump({"event_id": envelope["event_id"], "source_pbc": payload.get("source_pbc")}),
                _now(),
            ),
        )
        self.connection.commit()
        return {"ok": True, "duplicate": False, "event_id": envelope["event_id"], "side_effects": ()}

    def build_workbench(self, tenant: str) -> dict:
        submissions = self._fetchall(
            "SELECT * FROM insurance_underwriting_underwriting_submission WHERE tenant = ? ORDER BY updated_at DESC",
            (tenant,),
        )
        quotes = self._fetchall(
            "SELECT * FROM insurance_underwriting_quote WHERE tenant = ? ORDER BY created_at DESC",
            (tenant,),
        )
        decisions = self._fetchall(
            "SELECT * FROM insurance_underwriting_underwriting_decision WHERE tenant = ? ORDER BY created_at DESC",
            (tenant,),
        )
        bind_ready = self._fetchall(
            "SELECT * FROM insurance_underwriting_bind_package WHERE tenant = ? AND status = 'ready_to_bind'",
            (tenant,),
        )
        referred = [row for row in submissions if row["lifecycle_state"] in {"referred", "quote_referred", "refer"}]
        incomplete = [row for row in submissions if row["lifecycle_state"] == "intake_incomplete"]
        expiring = [row for row in quotes if row["valid_until"] <= (datetime.now(UTC).date() + timedelta(days=5)).isoformat()]
        return {
            "ok": True,
            "tenant": tenant,
            "submission_count": len(submissions),
            "referral_queue_count": len(referred),
            "incomplete_submission_count": len(incomplete),
            "quote_count": len(quotes),
            "quotes_expiring_count": len(expiring),
            "decision_count": len(decisions),
            "bind_ready_count": len(bind_ready),
            "outbox_count": self._fetchone("SELECT COUNT(*) AS count FROM insurance_underwriting_appgen_outbox_event WHERE tenant = ?", (tenant,))["count"],
            "inbox_count": self._fetchone("SELECT COUNT(*) AS count FROM insurance_underwriting_appgen_inbox_event WHERE tenant = ?", (tenant,))["count"],
            "dead_letter_count": self._fetchone("SELECT COUNT(*) AS count FROM insurance_underwriting_appgen_dead_letter_event WHERE tenant = ?", (tenant,))["count"] if tenant else 0,
            "queues": {
                "incomplete_submissions": tuple(row["submission_id"] for row in incomplete),
                "referrals": tuple(row["submission_id"] for row in referred),
                "quotes_expiring": tuple(row["quote_id"] for row in expiring),
                "bind_ready": tuple(row["bind_package_id"] for row in bind_ready),
            },
            "side_effects": (),
        }

    def get_submission_detail(self, submission_id: str) -> dict:
        submission = self._submission(submission_id)
        if not submission:
            return {"ok": False, "reason": "submission_not_found", "side_effects": ()}
        risk_profile = self._latest_risk_profile(submission_id)
        quotes = [
            self._jsonify_record(row, ("subjectivities_json", "exclusions_json", "pricing_trace_json"))
            for row in self._fetchall(
                "SELECT * FROM insurance_underwriting_quote WHERE submission_id = ? ORDER BY version DESC",
                (submission_id,),
            )
        ]
        decisions = [
            self._jsonify_record(row, ("decision_packet_json",))
            for row in self._fetchall(
                "SELECT * FROM insurance_underwriting_underwriting_decision WHERE submission_id = ? ORDER BY created_at DESC",
                (submission_id,),
            )
        ]
        exclusions = self._fetchall(
            "SELECT * FROM insurance_underwriting_exclusion WHERE submission_id = ? ORDER BY created_at DESC",
            (submission_id,),
        )
        timeline = self.build_timeline(submission_id)
        return {
            "ok": True,
            "submission": submission,
            "risk_profile": risk_profile,
            "quotes": quotes,
            "decisions": decisions,
            "exclusions": exclusions,
            "timeline": timeline,
            "side_effects": (),
        }

    def build_timeline(self, submission_id: str) -> dict:
        direct = self._fetchall(
            "SELECT * FROM insurance_underwriting_appgen_outbox_event WHERE aggregate_id = ? ORDER BY created_at ASC",
            (submission_id,),
        )
        related = self._fetchall(
            "SELECT * FROM insurance_underwriting_appgen_outbox_event WHERE payload_json LIKE ? ORDER BY created_at ASC",
            (f"%{submission_id}%",),
        )
        deduped = {}
        for row in direct + related:
            deduped[row["event_id"]] = self._jsonify_record(row, ("payload_json",))
        events = list(deduped.values())
        return {
            "ok": True,
            "submission_id": submission_id,
            "event_count": len(events),
            "events": events,
            "side_effects": (),
        }


def standalone_model_contract() -> dict:
    alignment = migration_alignment_report()
    return {
        "format": "appgen.insurance-underwriting-standalone-model-contract.v1",
        "ok": alignment["ok"],
        "pbc": PBC_KEY,
        "schema": OWNED_SCHEMA,
        "table_keys": OWNED_TABLES,
        "business_tables": BUSINESS_TABLES,
        "event_tables": EVENT_TABLES,
        "migration_alignment": alignment,
        "side_effects": (),
    }


def standalone_store_smoke_test() -> dict:
    store = InsuranceUnderwritingStandaloneStore()
    try:
        submission = store.create_submission(
            {
                "submission_id": "smoke-submission",
                "tenant": "tenant-smoke",
                "product_line": "property",
                "applicant_name": "Smoke Manufacturing",
                "jurisdiction": "US-NY",
                "requested_limit": 750000.0,
                "declared_revenue": 1800000.0,
                "effective_date": "2026-06-01",
                "exposure_locations": ("Albany",),
                "documents": ("application.pdf",),
                "prior_losses": (),
            }
        )
        risk = store.build_risk_profile(
            {
                "submission_id": "smoke-submission",
                "tenant": "tenant-smoke",
                "hazard_factors": ("fire",),
                "catastrophe_score": 0.2,
            }
        )
        factor = store.review_rating_factor(
            {
                "submission_id": "smoke-submission",
                "tenant": "tenant-smoke",
                "factor_type": "base_rate",
                "selected_value": 1.0,
                "weight": 0.3,
                "source": "actuarial_projection",
            }
        )
        quote = store.generate_quote({"submission_id": "smoke-submission", "tenant": "tenant-smoke"})
        decision = store.issue_underwriting_decision(
            {
                "submission_id": "smoke-submission",
                "quote_id": quote["result"]["quote_id"],
                "tenant": "tenant-smoke",
                "authority_level": "chief",
                "approved_by": "chief-underwriter",
            }
        )
        bind = store.assemble_bind_package(
            {
                "submission_id": "smoke-submission",
                "quote_id": quote["result"]["quote_id"],
                "tenant": "tenant-smoke",
                "subjectivities": ({"name": "signed_application", "satisfied": True},),
                "documents": ("signed_application",),
                "payment_confirmed": True,
            }
        )
        workbench = store.build_workbench("tenant-smoke")
        return {
            "ok": standalone_model_contract()["ok"]
            and submission["ok"]
            and risk["ok"]
            and factor["ok"]
            and quote["ok"]
            and decision["ok"]
            and bind["ok"]
            and workbench["ok"],
            "submission": submission,
            "risk": risk,
            "quote": quote,
            "decision": decision,
            "bind": bind,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        store.close()
