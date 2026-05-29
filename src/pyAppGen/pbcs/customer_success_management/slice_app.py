"""Standalone executable slice app for the customer_success_management PBC."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

from .domain_depth import (
    DOMAIN_ADVANCED_CAPABILITIES,
    DOMAIN_CONSUMED_EVENTS,
    DOMAIN_EVENTS,
    DOMAIN_OPERATIONS,
    DOMAIN_OWNED_TABLES,
    DOMAIN_PARAMETERS,
    DOMAIN_RULES,
)
from .manifest import PBC_MANIFEST

PBC_KEY = "customer_success_management"
PACKAGE_DIR = Path(__file__).resolve().parent
MIGRATION_PATH = PACKAGE_DIR / "migrations" / "001_initial.sql"
RELEASE_ARTIFACTS = (
    "README.md",
    "SPECIFICATION.md",
    "RELEASE_EVIDENCE.md",
    "implementation-plan.md",
    "implementation-status.md",
)
APPGEN_X_TOPIC = f"pbc.{PBC_KEY}.events"
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb", "sqlite")
LEGACY_EMITTED_EVENTS = tuple(PBC_MANIFEST["emits"])
LEGACY_CONSUMED_EVENTS = tuple(PBC_MANIFEST["consumes"])
EMITTED_EVENTS = tuple(dict.fromkeys(tuple(DOMAIN_EVENTS) + LEGACY_EMITTED_EVENTS))
CONSUMED_EVENTS = tuple(
    dict.fromkeys(tuple(DOMAIN_CONSUMED_EVENTS) + LEGACY_CONSUMED_EVENTS)
)
PERMISSIONS = (
    f"{PBC_KEY}.read",
    f"{PBC_KEY}.create",
    f"{PBC_KEY}.update",
    f"{PBC_KEY}.approve",
    f"{PBC_KEY}.admin",
    f"{PBC_KEY}.operate",
)

EVENT_ALIASES = {
    "SubscriptionRenewed": "SubscriptionActivated",
    "ServiceTicketResolved": "TicketClosed",
}
EMITTED_EVENT_ALIASES = {
    "CustomerHealthChanged": "HealthScoreChanged",
    "RenewalPlanCreated": "RenewalMotionStarted",
    "ExpansionSignalDetected": "PlaybookLaunched",
    "ChurnRiskRaised": "ChurnRiskChanged",
}

BUSINESS_TABLES = tuple(DOMAIN_OWNED_TABLES)
EVENT_TABLES = (
    f"{PBC_KEY}_appgen_outbox_event",
    f"{PBC_KEY}_appgen_inbox_event",
    f"{PBC_KEY}_appgen_dead_letter_event",
)
RUNTIME_TABLES = BUSINESS_TABLES + EVENT_TABLES

TABLE_DESCRIPTION_OVERRIDES = {
    f"{PBC_KEY}_customer_success_account": "Primary success account record with readiness and renewal posture.",
    f"{PBC_KEY}_success_plan": "Outcome plan linking stakeholders, milestones, and value hypotheses.",
    f"{PBC_KEY}_onboarding_milestone": "Customer onboarding milestone tracking and time-to-value evidence.",
    f"{PBC_KEY}_customer_touchpoint": "Structured customer touchpoint with channel, outcome, and follow-up evidence.",
    f"{PBC_KEY}_adoption_signal": "Normalized product, support, billing, or manual adoption telemetry.",
    f"{PBC_KEY}_health_score": "Computed explainable customer health score.",
    f"{PBC_KEY}_health_score_component": "Weighted score component for health explainability.",
    f"{PBC_KEY}_success_playbook": "Actionable playbook for success interventions.",
    f"{PBC_KEY}_playbook_task": "Success playbook task with assignee and SLA.",
    f"{PBC_KEY}_customer_escalation": "Cross-functional customer escalation record.",
    f"{PBC_KEY}_renewal_motion": "Renewal preparation and risk posture artifact.",
    f"{PBC_KEY}_expansion_opportunity": "Success-qualified expansion opportunity.",
    f"{PBC_KEY}_executive_business_review": "Executive review packet and talking points.",
    f"{PBC_KEY}_customer_objective": "Customer-owned objective and target metric.",
    f"{PBC_KEY}_customer_value_realization": "Value hypothesis and realized outcome evidence.",
    f"{PBC_KEY}_churn_risk_signal": "Churn-risk score and rationale.",
    f"{PBC_KEY}_success_exception_case": "Boundary-safe exception and remediation case.",
    f"{PBC_KEY}_success_policy_rule": "Compiled deterministic success policy.",
    f"{PBC_KEY}_success_runtime_parameter": "Bounded runtime parameter.",
    f"{PBC_KEY}_success_schema_extension": "Owned schema extension registration.",
    f"{PBC_KEY}_success_control_assertion": "Release or runtime control assertion.",
    f"{PBC_KEY}_success_governed_model": "Governed AI or scoring model metadata.",
}

ROUTE_DEFINITIONS = (
    {"method": "POST", "path": "/success-accounts", "operation": "create_success_account"},
    {"method": "POST", "path": "/success-plans", "operation": "create_success_plan"},
    {"method": "POST", "path": "/touchpoints", "operation": "record_touchpoint"},
    {"method": "POST", "path": "/health-scores", "operation": "calculate_health_score"},
    {"method": "POST", "path": "/playbooks", "operation": "launch_playbook"},
    {"method": "POST", "path": "/renewal-motions", "operation": "start_renewal_motion"},
    {"method": "POST", "path": "/agent/document-plan", "operation": "document_instruction_plan"},
    {"method": "POST", "path": "/agent/crud-plan", "operation": "datastore_crud_plan"},
    {"method": "GET", "path": "/customer-success-workbench", "operation": "query_workbench"},
)

FORM_DEFINITIONS = (
    {
        "id": "success_account_intake",
        "title": "Success account intake",
        "operation": "create_success_account",
        "fields": (
            "tenant",
            "code",
            "customer_name",
            "segment",
            "lifecycle_stage",
            "owner",
            "renewal_date",
        ),
    },
    {
        "id": "touchpoint_log",
        "title": "Customer touchpoint",
        "operation": "record_touchpoint",
        "fields": ("success_account_id", "channel", "purpose", "outcome", "owner", "occurred_at"),
    },
    {
        "id": "health_score_override",
        "title": "Health score override",
        "operation": "calculate_health_score",
        "fields": ("success_account_id", "adoption", "support", "billing", "engagement", "value"),
    },
    {
        "id": "renewal_motion_form",
        "title": "Renewal motion",
        "operation": "start_renewal_motion",
        "fields": ("success_account_id", "renewal_date", "owner", "risks", "value_story"),
    },
)

WIZARD_DEFINITIONS = (
    {
        "id": "onboarding_readiness",
        "title": "Onboarding readiness wizard",
        "steps": ("intake", "milestones", "stakeholders", "handoff"),
    },
    {
        "id": "touchpoint_follow_up",
        "title": "Touchpoint follow-up wizard",
        "steps": ("prepare", "engage", "capture", "next-best-action"),
    },
    {
        "id": "health_recovery",
        "title": "Health recovery wizard",
        "steps": ("signal-intake", "touchpoint", "score", "playbook", "exec-brief"),
    },
    {
        "id": "renewal_close_plan",
        "title": "Renewal close plan",
        "steps": ("coverage", "value-proof", "risk-plan", "commercial-handoff"),
    },
)

CONTROL_DEFINITIONS = (
    {"id": "policy_rule_editor", "type": "rule-editor", "targets": tuple(DOMAIN_RULES)},
    {"id": "runtime_parameter_editor", "type": "parameter-editor", "targets": tuple(DOMAIN_PARAMETERS)},
    {"id": "touchpoint_timeline", "type": "timeline", "targets": (f"{PBC_KEY}_customer_touchpoint", f"{PBC_KEY}_playbook_task")},
    {"id": "agent_mutation_guard", "type": "approval-guard", "targets": ("document_instruction_plan", "datastore_crud_plan")},
    {"id": "event_replay_console", "type": "event-console", "targets": EVENT_TABLES},
)


@dataclass(frozen=True)
class TableSpec:
    logical_name: str
    owned_table: str
    description: str
    foreign_key_table: str | None = None


TABLE_SPECS = tuple(
    TableSpec(
        logical_name=table.removeprefix(f"{PBC_KEY}_"),
        owned_table=table,
        description=TABLE_DESCRIPTION_OVERRIDES.get(table, table.removeprefix(f"{PBC_KEY}_").replace("_", " ").title()),
        foreign_key_table=f"{PBC_KEY}_customer_success_account"
        if table.startswith(f"{PBC_KEY}_")
        and table not in EVENT_TABLES
        and table != f"{PBC_KEY}_customer_success_account"
        and table not in (
            f"{PBC_KEY}_success_policy_rule",
            f"{PBC_KEY}_success_runtime_parameter",
            f"{PBC_KEY}_success_schema_extension",
            f"{PBC_KEY}_success_control_assertion",
            f"{PBC_KEY}_success_governed_model",
        )
        else None,
    )
    for table in RUNTIME_TABLES
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _code(prefix: str, tenant: str, unique_source: Any) -> str:
    return f"{prefix}-{tenant}-{_digest(unique_source)[:10]}".upper()


def _dedupe(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(items))


class SQLiteOwnedRepository:
    """Minimal package-local owned datastore for the standalone slice app."""

    def __init__(self, database_url: str = ":memory:") -> None:
        self.database_url = database_url
        self.connection = sqlite3.connect(database_url)
        self.connection.row_factory = sqlite3.Row

    def bootstrap(self) -> None:
        self.connection.executescript(MIGRATION_PATH.read_text(encoding="utf-8"))
        self.connection.commit()

    def insert(self, table: str, record: dict[str, Any]) -> dict[str, Any]:
        fields = tuple(record)
        placeholders = ", ".join("?" for _ in fields)
        sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"
        self.connection.execute(sql, tuple(record[field] for field in fields))
        self.connection.commit()
        inserted = self.fetch_one(table, record["id"])
        return inserted if inserted is not None else dict(record)

    def update_payload(self, table: str, record_id: str, payload: dict[str, Any]) -> None:
        updated_at = _utcnow()
        sql = f"UPDATE {table} SET payload = ?, updated_at = ? WHERE id = ?"
        self.connection.execute(sql, (_json(payload), updated_at, record_id))
        self.connection.commit()

    def fetch_all(
        self,
        table: str,
        *,
        tenant: str | None = None,
        limit: int | None = None,
        where: str | None = None,
        params: tuple[Any, ...] = (),
    ) -> tuple[dict[str, Any], ...]:
        sql = f"SELECT * FROM {table}"
        clauses = []
        values: list[Any] = []
        if tenant is not None:
            clauses.append("tenant = ?")
            values.append(tenant)
        if where:
            clauses.append(where)
            values.extend(params)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY created_at DESC"
        if limit is not None:
            sql += f" LIMIT {int(limit)}"
        rows = self.connection.execute(sql, tuple(values)).fetchall()
        return tuple(self._row_to_dict(row) for row in rows)

    def fetch_one(self, table: str, record_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            f"SELECT * FROM {table} WHERE id = ?",
            (record_id,),
        ).fetchone()
        return self._row_to_dict(row) if row is not None else None

    def has_event_idempotency_key(self, idempotency_key: str) -> bool:
        for table in EVENT_TABLES[1:]:
            row = self.connection.execute(
                f"SELECT 1 FROM {table} WHERE idempotency_key = ? LIMIT 1",
                (idempotency_key,),
            ).fetchone()
            if row is not None:
                return True
        return False

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        record = dict(row)
        payload = record.get("payload")
        if isinstance(payload, str) and payload:
            try:
                record["payload"] = json.loads(payload)
            except json.JSONDecodeError:
                pass
        return record


class CustomerSuccessManagementSliceApp:
    """One-PBC standalone app with an owned package-local datastore."""

    def __init__(self, database_url: str = ":memory:") -> None:
        self.repo = SQLiteOwnedRepository(database_url=database_url)
        self.repo.bootstrap()
        self.configuration = {
            "database_backend": "sqlite" if database_url == ":memory:" else "postgresql",
            "event_topic": APPGEN_X_TOPIC,
            "event_contract": "AppGen-X",
        }
        self.parameters = {parameter: None for parameter in DOMAIN_PARAMETERS}
        self.rules = {rule: None for rule in DOMAIN_RULES}

    def configure_runtime(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        config = dict(config or {})
        backend = config.get("database_backend", self.configuration["database_backend"])
        topic = config.get("event_topic", APPGEN_X_TOPIC)
        ok = backend in ALLOWED_DATABASE_BACKENDS and topic == APPGEN_X_TOPIC
        if ok:
            self.configuration.update(config)
        return {"ok": ok, "configuration": dict(self.configuration), "side_effects": ()}

    def set_parameter(self, name: str, value: Any) -> dict[str, Any]:
        bounded = name in DOMAIN_PARAMETERS
        if bounded:
            self.parameters[name] = value
        record = self._insert_record(
            f"{PBC_KEY}_success_runtime_parameter",
            {
                "tenant": "system",
                "code": name,
                "title": name.replace("_", " ").title(),
                "status": "active" if bounded else "rejected",
                "payload": {"value": value, "bounded": bounded},
            },
        )
        return {"ok": bounded, "parameter": record, "side_effects": ()}

    def register_rule(self, rule: dict[str, Any]) -> dict[str, Any]:
        rule_id = rule.get("rule_id", "unnamed_rule")
        compiled = {
            **dict(rule),
            "compiled_hash": _digest((rule_id, rule)),
            "event_contract": "AppGen-X",
        }
        self.rules[rule_id] = compiled
        record = self._insert_record(
            f"{PBC_KEY}_success_policy_rule",
            {
                "tenant": rule.get("tenant", "system"),
                "code": rule_id,
                "title": rule_id.replace("_", " ").title(),
                "status": "compiled",
                "payload": compiled,
            },
        )
        return {"ok": True, "rule": record, "side_effects": ()}

    def register_schema_extension(self, table: str, fields: dict[str, Any]) -> dict[str, Any]:
        if table not in BUSINESS_TABLES and table not in {spec.logical_name for spec in TABLE_SPECS}:
            return {"ok": False, "reason": "unknown_owned_table", "side_effects": ()}
        owned_table = table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        record = self._insert_record(
            f"{PBC_KEY}_success_schema_extension",
            {
                "tenant": "system",
                "code": owned_table,
                "title": f"Extension for {owned_table}",
                "status": "proposed",
                "payload": {"table": owned_table, "fields": dict(fields)},
            },
        )
        return {"ok": True, "table": owned_table, "extension": record, "side_effects": ()}

    def create_success_account(self, payload: dict[str, Any]) -> dict[str, Any]:
        required = ("tenant", "code", "customer_name", "segment", "lifecycle_stage", "owner", "renewal_date")
        missing = tuple(field for field in required if not payload.get(field))
        if missing:
            return {"ok": False, "missing_fields": missing, "side_effects": ()}
        account = self._insert_record(
            f"{PBC_KEY}_customer_success_account",
            {
                "tenant": payload["tenant"],
                "code": payload["code"],
                "title": payload["customer_name"],
                "owner": payload["owner"],
                "status": payload.get("status", "onboarding"),
                "score": float(payload.get("current_health", 0.72)),
                "payload": {
                    **dict(payload),
                    "readiness_checks": {
                        "segment": bool(payload.get("segment")),
                        "lifecycle_stage": bool(payload.get("lifecycle_stage")),
                        "owner": bool(payload.get("owner")),
                        "renewal_date": bool(payload.get("renewal_date")),
                        "touchpoint_strategy": bool(payload.get("touchpoint_strategy", "onboarding_outreach")),
                    },
                },
            },
        )
        success_plan = self.create_success_plan(
            {
                "tenant": payload["tenant"],
                "success_account_id": account["id"],
                "code": payload.get("plan_code", f"{payload['code']}-PLAN"),
                "title": payload.get("plan_title", "Default success plan"),
                "owner": payload["owner"],
                "objectives": payload.get("objectives", ("time_to_value", "renewal_readiness")),
            }
        )
        onboarding = self.track_onboarding_milestone(
            {
                "tenant": payload["tenant"],
                "success_account_id": account["id"],
                "code": payload.get("milestone_code", f"{payload['code']}-DISCOVERY"),
                "title": "Discovery and kickoff",
                "owner": payload["owner"],
                "due_on": payload.get(
                    "first_value_due_on",
                    (datetime.now(timezone.utc) + timedelta(days=14)).date().isoformat(),
                ),
            }
        )
        touchpoint = self.record_touchpoint(
            {
                "tenant": payload["tenant"],
                "success_account_id": account["id"],
                "code": payload.get("touchpoint_code", f"{payload['code']}-KICKOFF"),
                "title": payload.get("touchpoint_title", "Kickoff touchpoint"),
                "owner": payload["owner"],
                "channel": payload.get("touchpoint_channel", "video"),
                "purpose": payload.get("touchpoint_purpose", "onboarding_kickoff"),
                "outcome": payload.get("touchpoint_outcome", "next_steps_confirmed"),
                "next_step": payload.get("touchpoint_next_step", "schedule adoption workshop"),
                "occurred_at": payload.get("touchpoint_occurred_at", _utcnow()),
                "status": "completed",
            }
        )
        event = self._emit_event("SuccessAccountCreated", account["tenant"], account["id"], account["payload"])
        return {
            "ok": True,
            "record": account,
            "success_plan": success_plan["record"],
            "onboarding_milestone": onboarding["record"],
            "touchpoint": touchpoint["record"],
            "event": event,
            "side_effects": (),
        }

    def create_success_plan(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_success_plan",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("PLAN", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Success plan"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "active"),
                "payload": {"objectives": tuple(payload.get("objectives", ())), **dict(payload)},
            },
        )
        return {"ok": True, "record": record, "side_effects": ()}

    def track_onboarding_milestone(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_onboarding_milestone",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("MS", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Onboarding milestone"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "open"),
                "due_on": payload.get("due_on"),
                "payload": dict(payload),
            },
        )
        return {"ok": True, "record": record, "side_effects": ()}

    def record_touchpoint(self, payload: dict[str, Any]) -> dict[str, Any]:
        touchpoint_payload = {
            "channel": payload.get("channel", "email"),
            "purpose": payload.get("purpose", "customer_outreach"),
            "outcome": payload.get("outcome", "pending"),
            "next_step": payload.get("next_step", "follow_up"),
            "occurred_at": payload.get("occurred_at", _utcnow()),
            **dict(payload),
        }
        record = self._insert_record(
            f"{PBC_KEY}_customer_touchpoint",
            {
                "tenant": touchpoint_payload.get("tenant", "default"),
                "success_account_id": touchpoint_payload.get("success_account_id"),
                "code": touchpoint_payload.get(
                    "code",
                    _code("TP", touchpoint_payload.get("tenant", "default"), touchpoint_payload),
                ),
                "title": touchpoint_payload.get("title", f"{touchpoint_payload['channel'].title()} touchpoint"),
                "owner": touchpoint_payload.get("owner", "unassigned"),
                "status": touchpoint_payload.get("status", "completed"),
                "score": float(touchpoint_payload.get("sentiment", 0.75)),
                "due_on": touchpoint_payload.get("due_on"),
                "payload": touchpoint_payload,
            },
        )
        event = self._emit_event(
            "CustomerTouchpointLogged",
            touchpoint_payload.get("tenant", "default"),
            touchpoint_payload.get("success_account_id"),
            {
                "touchpoint_id": record["id"],
                "channel": touchpoint_payload["channel"],
                "outcome": touchpoint_payload["outcome"],
            },
        )
        return {"ok": True, "record": record, "event": event, "side_effects": ()}

    def ingest_adoption_signal(self, payload: dict[str, Any]) -> dict[str, Any]:
        normalized = {
            "source": payload.get("source", "product_usage"),
            "metric": payload.get("metric", "active_users"),
            "trend": payload.get("trend", "stable"),
            "confidence": float(payload.get("confidence", 0.8)),
            **dict(payload),
        }
        record = self._insert_record(
            f"{PBC_KEY}_adoption_signal",
            {
                "tenant": normalized.get("tenant", "default"),
                "success_account_id": normalized.get("success_account_id"),
                "code": normalized.get("code", _code("ADOPT", normalized.get("tenant", "default"), normalized)),
                "title": normalized.get("metric", "adoption signal"),
                "status": normalized.get("status", "captured"),
                "score": float(normalized.get("value", normalized.get("confidence", 0.8))),
                "payload": normalized,
            },
        )
        return {"ok": True, "record": record, "side_effects": ()}

    def calculate_health_score(self, payload: dict[str, Any]) -> dict[str, Any]:
        weights = {
            "adoption": 0.25,
            "support": 0.15,
            "billing": 0.15,
            "engagement": 0.2,
            "value": 0.15,
            "renewal": 0.1,
        }
        components = {
            name: float(payload.get(name, 0.7))
            for name in weights
        }
        weighted = sum(components[name] * weight for name, weight in weights.items())
        score_record = self._insert_record(
            f"{PBC_KEY}_health_score",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("HLTH", payload.get("tenant", "default"), payload)),
                "title": "Customer health",
                "status": "calculated",
                "score": round(weighted, 4),
                "payload": {"components": components, "weights": weights, **dict(payload)},
            },
        )
        component_records = tuple(
            self._insert_record(
                f"{PBC_KEY}_health_score_component",
                {
                    "tenant": payload.get("tenant", "default"),
                    "success_account_id": payload.get("success_account_id"),
                    "code": f"{score_record['code']}-{name}".upper(),
                    "title": f"{name.title()} component",
                    "status": "explained",
                    "score": round(value, 4),
                    "payload": {
                        "component": name,
                        "weight": weights[name],
                        "value": value,
                        "explanation": f"{name} contributed {round(value * weights[name], 4)} to the overall score.",
                    },
                },
            )
            for name, value in components.items()
        )
        event = self._emit_event(
            "HealthScoreChanged",
            payload.get("tenant", "default"),
            payload.get("success_account_id"),
            {"score": score_record["score"], "components": components},
        )
        return {
            "ok": True,
            "record": score_record,
            "components": component_records,
            "event": event,
            "side_effects": (),
        }

    def explain_health_component(self, payload: dict[str, Any]) -> dict[str, Any]:
        component = payload.get("component", "adoption")
        explanation = {
            "component": component,
            "reason": f"{component} is below target and should trigger targeted outreach.",
            "recommended_actions": ("review signals", "launch playbook", "brief account owner"),
        }
        return {"ok": True, "explanation": explanation, "side_effects": ()}

    def launch_playbook(self, payload: dict[str, Any]) -> dict[str, Any]:
        playbook = self._insert_record(
            f"{PBC_KEY}_success_playbook",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("PLAY", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Health recovery playbook"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "active"),
                "payload": dict(payload),
            },
        )
        tasks = tuple(
            self._insert_record(
                f"{PBC_KEY}_playbook_task",
                {
                    "tenant": payload.get("tenant", "default"),
                    "success_account_id": payload.get("success_account_id"),
                    "code": f"{playbook['code']}-T{index + 1}",
                    "title": title,
                    "owner": payload.get("owner", "unassigned"),
                    "status": "open",
                    "due_on": (
                        datetime.now(timezone.utc) + timedelta(hours=24 * (index + 1))
                    ).date().isoformat(),
                    "payload": {"playbook_id": playbook["id"], "title": title},
                },
            )
            for index, title in enumerate(
                payload.get(
                    "tasks",
                    ("review account plan", "contact executive sponsor", "schedule recovery review"),
                )
            )
        )
        event = self._emit_event(
            "PlaybookLaunched",
            payload.get("tenant", "default"),
            payload.get("success_account_id"),
            {"playbook_id": playbook["id"], "task_count": len(tasks)},
        )
        return {"ok": True, "record": playbook, "tasks": tasks, "event": event, "side_effects": ()}

    def complete_playbook_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_playbook_task",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("TASK", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Completed playbook task"),
                "owner": payload.get("owner", "unassigned"),
                "status": "completed",
                "payload": dict(payload),
            },
        )
        return {"ok": True, "record": record, "side_effects": ()}

    def open_customer_escalation(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_customer_escalation",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("ESC", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Customer escalation"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "open"),
                "score": float(payload.get("severity", 0.8)),
                "payload": dict(payload),
            },
        )
        event = self._emit_event(
            "CustomerEscalationOpened",
            payload.get("tenant", "default"),
            payload.get("success_account_id"),
            {"escalation_id": record["id"], "severity": record["score"]},
        )
        return {"ok": True, "record": record, "event": event, "side_effects": ()}

    def start_renewal_motion(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_renewal_motion",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("REN", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Renewal motion"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "active"),
                "due_on": payload.get("renewal_date"),
                "payload": dict(payload),
            },
        )
        event = self._emit_event(
            "RenewalMotionStarted",
            payload.get("tenant", "default"),
            payload.get("success_account_id"),
            {"renewal_motion_id": record["id"], "renewal_date": payload.get("renewal_date")},
        )
        return {"ok": True, "record": record, "event": event, "side_effects": ()}

    def identify_expansion_opportunity(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_expansion_opportunity",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("EXP", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Expansion opportunity"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "qualified"),
                "score": float(payload.get("confidence", 0.75)),
                "payload": dict(payload),
            },
        )
        return {"ok": True, "record": record, "side_effects": ()}

    def prepare_executive_review(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_executive_business_review",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("EBR", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Executive business review"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "draft"),
                "payload": dict(payload),
            },
        )
        return {"ok": True, "record": record, "side_effects": ()}

    def record_customer_objective(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_customer_objective",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("OBJ", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Customer objective"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "active"),
                "score": float(payload.get("progress", 0.0)),
                "payload": dict(payload),
            },
        )
        return {"ok": True, "record": record, "side_effects": ()}

    def measure_value_realization(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_customer_value_realization",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("VAL", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Value realization"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "measured"),
                "score": float(payload.get("realized_value", 0.0)),
                "payload": dict(payload),
            },
        )
        return {"ok": True, "record": record, "side_effects": ()}

    def score_churn_risk(self, payload: dict[str, Any]) -> dict[str, Any]:
        health_score = float(payload.get("health_score", 0.7))
        payment_risk = float(payload.get("payment_risk", 0.2))
        support_risk = float(payload.get("support_risk", 0.2))
        risk = round(max(0.0, min(1.0, (1.0 - health_score) * 0.6 + payment_risk * 0.2 + support_risk * 0.2)), 4)
        record = self._insert_record(
            f"{PBC_KEY}_churn_risk_signal",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("RISK", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Churn risk"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "open"),
                "score": risk,
                "payload": dict(payload),
            },
        )
        event = self._emit_event(
            "ChurnRiskChanged",
            payload.get("tenant", "default"),
            payload.get("success_account_id"),
            {"risk_score": risk},
        )
        return {"ok": True, "record": record, "event": event, "side_effects": ()}

    def resolve_success_exception(self, payload: dict[str, Any]) -> dict[str, Any]:
        record = self._insert_record(
            f"{PBC_KEY}_success_exception_case",
            {
                "tenant": payload.get("tenant", "default"),
                "success_account_id": payload.get("success_account_id"),
                "code": payload.get("code", _code("EXC", payload.get("tenant", "default"), payload)),
                "title": payload.get("title", "Success exception"),
                "owner": payload.get("owner", "unassigned"),
                "status": payload.get("status", "resolved"),
                "payload": dict(payload),
            },
        )
        return {"ok": True, "record": record, "side_effects": ()}

    def compile_success_rule(self, payload: dict[str, Any]) -> dict[str, Any]:
        compiled = {
            **dict(payload),
            "compiled_hash": _digest(payload),
            "scope": payload.get("scope", "tenant"),
            "effective": payload.get("effective", _utcnow()),
        }
        return self.register_rule(compiled)

    def simulate_renewal_outcome(self, payload: dict[str, Any]) -> dict[str, Any]:
        current_health = float(payload.get("current_health", 0.72))
        adoption_uplift = float(payload.get("adoption_uplift", 0.05))
        exec_engagement = float(payload.get("executive_engagement", 0.1))
        renewal_probability = round(max(0.0, min(1.0, current_health + adoption_uplift + exec_engagement)), 4)
        return {
            "ok": True,
            "simulation": {
                "renewal_probability": renewal_probability,
                "revenue_retained": round(float(payload.get("arr", 100000.0)) * renewal_probability, 2),
                "recommended_action": "advance to renewal room" if renewal_probability >= 0.8 else "launch recovery playbook",
            },
            "side_effects": (),
        }

    def document_instruction_plan(self, document: str, instruction: str) -> dict[str, Any]:
        lowered = f"{document} {instruction}".lower()
        candidate_tables = tuple(
            table
            for table in BUSINESS_TABLES
            if any(token in lowered for token in table.removeprefix(f"{PBC_KEY}_").split("_"))
        )[:4] or BUSINESS_TABLES[:4]
        matched_operations = tuple(
            operation
            for operation in DOMAIN_OPERATIONS
            if any(token in lowered for token in operation.split("_"))
        )[:4] or DOMAIN_OPERATIONS[:4]
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "document_digest": _digest(document),
            "instruction": instruction,
            "candidate_tables": candidate_tables,
            "matched_operations": matched_operations,
            "requires_human_confirmation": True,
            "crud_preview": {"operation": "update", "event_contract": "AppGen-X"},
            "side_effects": (),
        }

    def datastore_crud_plan(
        self, action: str, table: str | None = None, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        target = table or BUSINESS_TABLES[0]
        owned = target.startswith(f"{PBC_KEY}_") and target in RUNTIME_TABLES
        if not owned:
            return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "action": action,
            "table": target,
            "payload": dict(payload or {}),
            "requires_confirmation": action in {"create", "update", "delete"},
            "event_contract": "AppGen-X",
            "side_effects": (),
        }

    def receive_event(self, event: dict[str, Any]) -> dict[str, Any]:
        raw_event_type = event.get("event_type", "")
        event_type = EVENT_ALIASES.get(raw_event_type, raw_event_type)
        idempotency_key = event.get("idempotency_key") or _digest((event_type, event))
        if self.repo.has_event_idempotency_key(idempotency_key):
            return {"ok": True, "duplicate": True, "idempotency_key": idempotency_key, "side_effects": ()}
        if event_type not in DOMAIN_CONSUMED_EVENTS:
            dead_letter = self._record_event(
                EVENT_TABLES[2],
                event_type=raw_event_type or "UnknownEvent",
                tenant=event.get("tenant", "default"),
                success_account_id=event.get("success_account_id"),
                status="dead_lettered",
                idempotency_key=idempotency_key,
                payload={"event": dict(event), "reason": "unsupported_event"},
                last_error="unsupported_event",
            )
            return {
                "ok": False,
                "duplicate": False,
                "dead_letter_table": EVENT_TABLES[2],
                "event": dead_letter,
                "idempotency_key": idempotency_key,
                "side_effects": (),
            }
        inbox = self._record_event(
            EVENT_TABLES[1],
            event_type=event_type,
            tenant=event.get("tenant", "default"),
            success_account_id=event.get("success_account_id"),
            status="processed",
            idempotency_key=idempotency_key,
            payload=dict(event),
        )
        derived_actions = []
        if event_type == "PaymentFailed":
            derived_actions.append(
                self.score_churn_risk(
                    {
                        "tenant": event.get("tenant", "default"),
                        "success_account_id": event.get("success_account_id"),
                        "payment_risk": 1.0,
                        "health_score": 0.45,
                    }
                )
            )
        elif event_type == "SubscriptionActivated":
            derived_actions.append(
                self.track_onboarding_milestone(
                    {
                        "tenant": event.get("tenant", "default"),
                        "success_account_id": event.get("success_account_id"),
                        "title": "Subscription activated",
                    }
                )
            )
        elif event_type == "TicketClosed":
            derived_actions.append(
                self.complete_playbook_task(
                    {
                        "tenant": event.get("tenant", "default"),
                        "success_account_id": event.get("success_account_id"),
                        "title": "Follow up after support ticket closure",
                    }
                )
            )
        return {
            "ok": True,
            "duplicate": False,
            "event": inbox,
            "derived_actions": tuple(derived_actions),
            "idempotency_key": idempotency_key,
            "side_effects": (),
        }

    def query_workbench(self, tenant: str = "default", limit: int = 25) -> dict[str, Any]:
        accounts = self.repo.fetch_all(f"{PBC_KEY}_customer_success_account", tenant=tenant, limit=limit)
        touchpoints = self.repo.fetch_all(f"{PBC_KEY}_customer_touchpoint", tenant=tenant, limit=limit)
        risks = self.repo.fetch_all(f"{PBC_KEY}_churn_risk_signal", tenant=tenant, limit=limit)
        renewals = self.repo.fetch_all(f"{PBC_KEY}_renewal_motion", tenant=tenant, limit=limit)
        playbooks = self.repo.fetch_all(f"{PBC_KEY}_success_playbook", tenant=tenant, limit=limit)
        tasks = self.repo.fetch_all(f"{PBC_KEY}_playbook_task", tenant=tenant, limit=limit)
        summary = {
            "account_count": len(accounts),
            "touchpoint_count": len(touchpoints),
            "at_risk_count": len(tuple(item for item in risks if float(item.get("score") or 0.0) >= 0.5)),
            "open_playbooks": len(tuple(item for item in playbooks if item.get("status") != "completed")),
            "open_tasks": len(tuple(item for item in tasks if item.get("status") != "completed")),
            "renewal_motions": len(renewals),
        }
        return {
            "ok": True,
            "tenant": tenant,
            "summary": summary,
            "records": {
                "accounts": accounts,
                "touchpoints": touchpoints,
                "risks": risks,
                "renewals": renewals,
                "playbooks": playbooks,
                "tasks": tasks,
            },
            "forms": FORM_DEFINITIONS,
            "wizards": WIZARD_DEFINITIONS,
            "controls": CONTROL_DEFINITIONS,
            "side_effects": (),
        }

    def build_workbench_view(self, tenant: str = "default") -> dict[str, Any]:
        workbench = self.query_workbench(tenant=tenant)
        return {
            "ok": workbench["ok"],
            "pbc": PBC_KEY,
            "tenant": tenant,
            "view": "CustomerSuccessManagementWorkbench",
            "panels": (
                "command_center",
                "accounts",
                "touchpoint_timeline",
                "health_cockpit",
                "playbook_board",
                "renewal_room",
                "agent_assistant",
                "release_evidence",
            ),
            "forms": workbench["forms"],
            "wizards": workbench["wizards"],
            "controls": workbench["controls"],
            "summary": workbench["summary"],
            "side_effects": (),
        }

    def run_operation(self, operation: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        if not hasattr(self, operation):
            return {"ok": False, "reason": "unknown_operation", "operation": operation, "side_effects": ()}
        handler = getattr(self, operation)
        if operation in {"query_workbench", "build_workbench_view"}:
            return handler(**payload)
        if operation == "document_instruction_plan":
            return handler(payload.get("document", ""), payload.get("instruction", ""))
        if operation == "datastore_crud_plan":
            return handler(payload.get("action", "read"), payload.get("table"), payload.get("payload"))
        return handler(payload)

    def _insert_record(self, table: str, payload: dict[str, Any]) -> dict[str, Any]:
        now = _utcnow()
        record = {
            "id": payload.get("id", _digest((table, payload, now))[:18]),
            "tenant": payload.get("tenant", "default"),
            "code": payload.get("code", _code("REC", payload.get("tenant", "default"), payload)),
            "title": payload.get("title", payload.get("code", table.removeprefix(f"{PBC_KEY}_"))),
            "owner": payload.get("owner"),
            "status": payload.get("status", "draft"),
            "version": int(payload.get("version", 1)),
            "success_account_id": payload.get("success_account_id"),
            "score": payload.get("score"),
            "due_on": payload.get("due_on"),
            "event_type": payload.get("event_type"),
            "topic": payload.get("topic"),
            "idempotency_key": payload.get("idempotency_key"),
            "attempts": int(payload.get("attempts", 0)),
            "last_error": payload.get("last_error"),
            "payload": _json(payload.get("payload", {})),
            "effective_at": payload.get("effective_at", now),
            "created_at": now,
            "updated_at": now,
        }
        return self.repo.insert(table, record)

    def _record_event(
        self,
        table: str,
        *,
        event_type: str,
        tenant: str,
        success_account_id: str | None,
        status: str,
        idempotency_key: str,
        payload: dict[str, Any],
        last_error: str | None = None,
    ) -> dict[str, Any]:
        return self._insert_record(
            table,
            {
                "tenant": tenant,
                "code": event_type,
                "title": event_type,
                "status": status,
                "success_account_id": success_account_id,
                "event_type": event_type,
                "topic": APPGEN_X_TOPIC,
                "idempotency_key": idempotency_key,
                "attempts": 1,
                "last_error": last_error,
                "payload": payload,
            },
        )

    def _emit_event(
        self,
        event_type: str,
        tenant: str,
        success_account_id: str | None,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        canonical = EMITTED_EVENT_ALIASES.get(event_type, event_type)
        idempotency_key = _digest((canonical, tenant, success_account_id, payload))
        return self._record_event(
            EVENT_TABLES[0],
            event_type=canonical,
            tenant=tenant,
            success_account_id=success_account_id,
            status="pending",
            idempotency_key=idempotency_key,
            payload=payload,
        )


def build_standalone_app(database_url: str = ":memory:") -> CustomerSuccessManagementSliceApp:
    return CustomerSuccessManagementSliceApp(database_url=database_url)


def build_models_contract() -> dict[str, Any]:
    fields = (
        {"name": "id", "type": "string", "primary_key": True, "nullable": False},
        {"name": "tenant", "type": "string", "required": True},
        {"name": "code", "type": "string", "required": True, "searchable": True},
        {"name": "title", "type": "string", "required": False},
        {"name": "owner", "type": "string", "required": False},
        {"name": "status", "type": "string", "required": True, "default": "draft"},
        {"name": "version", "type": "integer", "required": True, "default": 1},
        {"name": "success_account_id", "type": "string", "required": False},
        {"name": "score", "type": "number", "required": False},
        {"name": "due_on", "type": "date", "required": False},
        {"name": "event_type", "type": "string", "required": False},
        {"name": "topic", "type": "string", "required": False},
        {"name": "idempotency_key", "type": "string", "required": False},
        {"name": "attempts", "type": "integer", "required": False},
        {"name": "last_error", "type": "string", "required": False},
        {"name": "payload", "type": "json", "required": False},
        {"name": "effective_at", "type": "datetime", "required": True},
        {"name": "created_at", "type": "datetime", "required": True},
        {"name": "updated_at", "type": "datetime", "required": True},
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "models": tuple(
            {
                "class_name": "".join(part.title() for part in spec.logical_name.split("_")),
                "table": spec.owned_table,
                "fields": fields,
                "relationships": (
                    {
                        "field": "success_account_id",
                        "target_table": f"{PBC_KEY}_customer_success_account",
                        "target_column": "id",
                        "cardinality": "many-to-one",
                        "ownership": "same_pbc",
                    },
                )
                if spec.foreign_key_table
                else (),
            }
            for spec in TABLE_SPECS
        ),
        "side_effects": (),
    }


def build_schema_contract() -> dict[str, Any]:
    models = build_models_contract()
    return {
        "format": f"appgen.{PBC_KEY}.owned-schema-contract.v1",
        "ok": models["ok"],
        "pbc": PBC_KEY,
        "tables": tuple(
            {
                "logical_table": spec.logical_name,
                "owned_table": spec.owned_table,
                "description": spec.description,
                "fields": next(model["fields"] for model in models["models"] if model["table"] == spec.owned_table),
                "relationships": next(
                    model["relationships"] for model in models["models"] if model["table"] == spec.owned_table
                ),
            }
            for spec in TABLE_SPECS
        ),
        "migrations": ("migrations/001_initial.sql",),
        "models": models["models"],
        "owned_tables": RUNTIME_TABLES,
        "shared_table_access": False,
        "database_backends": ALLOWED_DATABASE_BACKENDS[:-1],
        "side_effects": (),
    }


def build_service_contract() -> dict[str, Any]:
    commands = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        *DOMAIN_OPERATIONS,
        "document_instruction_plan",
        "datastore_crud_plan",
        "receive_event",
    )
    queries = ("query_workbench", "build_workbench_view")
    return {
        "format": f"appgen.{PBC_KEY}.service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": commands,
        "query_methods": queries,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "mutates_only": BUSINESS_TABLES + EVENT_TABLES,
        "external_dependencies": {
            "apis": (),
            "events": DOMAIN_CONSUMED_EVENTS,
            "api_projections": ("customer_projection", "subscription_projection", "billing_projection"),
            "shared_tables": (),
        },
        "side_effects": (),
    }


def build_api_contract() -> dict[str, Any]:
    return {
        "format": f"appgen.{PBC_KEY}.api-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "routes": tuple(
            {
                **route,
                "idempotency_key": f"{PBC_KEY}:{route['method']}:{route['path']}",
                "required_permission": f"{PBC_KEY}.operate" if route["method"] == "POST" else f"{PBC_KEY}.read",
                "stream_engine_picker_visible": False,
            }
            for route in ROUTE_DEFINITIONS
        ),
        "event_contract": "AppGen-X",
        "shared_table_access": False,
        "side_effects": (),
    }


def build_event_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contract": "AppGen-X",
        "topic": APPGEN_X_TOPIC,
        "outbox_table": EVENT_TABLES[0],
        "inbox_table": EVENT_TABLES[1],
        "dead_letter_table": EVENT_TABLES[2],
        "emitted": EMITTED_EVENTS,
        "consumed": CONSUMED_EVENTS,
        "stream_engine_picker_visible": False,
        "idempotency": "required",
        "side_effects": (),
    }


def build_ui_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "fragments": tuple(PBC_MANIFEST["ui_fragments"]),
        "workbench_view": "CustomerSuccessManagementWorkbench",
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "advanced_panels": tuple(DOMAIN_ADVANCED_CAPABILITIES),
        "action_permissions": PERMISSIONS,
        "side_effects": (),
    }


def build_agent_contract() -> dict[str, Any]:
    skills = (
        "guide_user",
        "read_records",
        "create_record",
        "update_record",
        "plan_document_changes",
        "preview_mutation",
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "namespace": f"{PBC_KEY}_skills",
        "skills": tuple(
            {
                "name": f"{PBC_KEY}_{skill}",
                "scope": PBC_KEY,
                "requires_confirmation_for_mutation": skill not in {"guide_user", "read_records"},
                "uses_appgen_event_contract": True,
            }
            for skill in skills
        ),
        "capabilities": (
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "release_evidence_navigation",
        ),
        "side_effects": (),
    }


def build_seed_plan() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rows": (
            {
                "table": f"{PBC_KEY}_customer_success_account",
                "code": "CS-DEMO-001",
                "status": "active",
            },
            {
                "table": f"{PBC_KEY}_customer_touchpoint",
                "code": "TP-DEMO-001",
                "status": "completed",
            },
            {
                "table": f"{PBC_KEY}_success_runtime_parameter",
                "code": "workbench_limit",
                "status": "active",
            },
            {
                "table": f"{PBC_KEY}_success_policy_rule",
                "code": "health_score_policy",
                "status": "compiled",
            },
        ),
        "side_effects": (),
    }

def verify_owned_table_boundary(references: tuple[str, ...] | list[str] = ()) -> dict[str, Any]:
    allowed = set(RUNTIME_TABLES) | set(CONSUMED_EVENTS) | {
        "api_dependency",
        "projection_dependency",
        "customer_projection",
        "subscription_projection",
        "billing_projection",
    }
    foreign = tuple(
        reference
        for reference in references
        if reference not in allowed and not str(reference).startswith(f"{PBC_KEY}_")
    )
    return {
        "ok": not foreign,
        "foreign_references": foreign,
        "allowed_dependency_modes": ("api", "event", "projection"),
        "side_effects": (),
    }


def dispatch_route(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    *,
    app: CustomerSuccessManagementSliceApp | None = None,
) -> dict[str, Any]:
    route = next((item for item in ROUTE_DEFINITIONS if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "reason": "route_not_found", "side_effects": ()}
    app = app or build_standalone_app()
    if route["operation"] == "query_workbench":
        result = app.query_workbench(tenant=(payload or {}).get("tenant", "default"))
    elif route["operation"] == "document_instruction_plan":
        result = app.document_instruction_plan(
            (payload or {}).get("document", ""),
            (payload or {}).get("instruction", ""),
        )
    elif route["operation"] == "datastore_crud_plan":
        result = app.datastore_crud_plan(
            (payload or {}).get("action", "read"),
            (payload or {}).get("table"),
            (payload or {}).get("payload"),
        )
    else:
        result = app.run_operation(route["operation"], payload or {})
    return {"ok": result.get("ok") is True, "route": route, "result": result, "side_effects": ()}


def slice_app_smoke_test() -> dict[str, Any]:
    app = build_standalone_app()
    config = app.configure_runtime({"database_backend": "sqlite", "event_topic": APPGEN_X_TOPIC})
    account = app.create_success_account(
        {
            "tenant": "tenant-smoke",
            "code": "CSM-SMOKE",
            "customer_name": "Northwind Health",
            "segment": "enterprise",
            "lifecycle_stage": "onboarding",
            "owner": "csm-1",
            "renewal_date": "2026-12-31",
        }
    )
    touchpoint = app.record_touchpoint(
        {
            "tenant": "tenant-smoke",
            "success_account_id": account["record"]["id"],
            "channel": "phone",
            "purpose": "renewal_alignment",
            "outcome": "executive_follow_up_scheduled",
            "owner": "csm-1",
        }
    )
    health = app.calculate_health_score(
        {"tenant": "tenant-smoke", "success_account_id": account["record"]["id"], "adoption": 0.8, "support": 0.7}
    )
    playbook = app.launch_playbook({"tenant": "tenant-smoke", "success_account_id": account["record"]["id"]})
    renewal = app.start_renewal_motion(
        {"tenant": "tenant-smoke", "success_account_id": account["record"]["id"], "renewal_date": "2026-12-31"}
    )
    document_plan = app.document_instruction_plan("Renewal risk memo", "update health and renewal touchpoints")
    crud_plan = app.datastore_crud_plan("update", table=f"{PBC_KEY}_success_plan", payload={"status": "active"})
    handled = app.receive_event(
        {"event_type": "PaymentFailed", "tenant": "tenant-smoke", "success_account_id": account["record"]["id"]}
    )
    duplicate = app.receive_event(
        {
            "event_type": "PaymentFailed",
            "tenant": "tenant-smoke",
            "success_account_id": account["record"]["id"],
            "idempotency_key": handled["idempotency_key"],
        }
    )
    workbench = app.query_workbench("tenant-smoke")
    route = dispatch_route(
        "POST",
        "/touchpoints",
        {
            "tenant": "tenant-smoke",
            "success_account_id": account["record"]["id"],
            "channel": "email",
            "purpose": "health_follow_up",
            "outcome": "reply_pending",
            "owner": "csm-1",
        },
        app=app,
    )
    workbench_route = dispatch_route("GET", "/customer-success-workbench", {"tenant": "tenant-smoke"}, app=app)
    return {
        "ok": all(
            (
                config["ok"],
                account["ok"],
                touchpoint["ok"],
                health["ok"],
                playbook["ok"],
                renewal["ok"],
                document_plan["ok"],
                crud_plan["ok"],
                handled["ok"],
                duplicate["duplicate"] is True,
                workbench["summary"]["account_count"] >= 1,
                workbench["summary"]["touchpoint_count"] >= 2,
                route["ok"],
                workbench_route["ok"],
            )
        ),
        "configuration": config,
        "account": account,
        "touchpoint": touchpoint,
        "health": health,
        "playbook": playbook,
        "renewal": renewal,
        "document_plan": document_plan,
        "crud_plan": crud_plan,
        "handled_event": handled,
        "duplicate_event": duplicate,
        "workbench": workbench,
        "route": route,
        "workbench_route": workbench_route,
        "side_effects": (),
    }

def pbc_source_artifact_contract() -> dict[str, Any]:
    schema = build_schema_contract()
    docs = tuple(path for path in RELEASE_ARTIFACTS if (PACKAGE_DIR / path).exists())
    missing_docs = tuple(path for path in RELEASE_ARTIFACTS if path not in docs)
    migration_sql = MIGRATION_PATH.read_text(encoding="utf-8")
    return {
        "ok": schema["ok"] and not missing_docs and "CREATE TABLE" in migration_sql,
        "pbc": PBC_KEY,
        "schema_contract": schema,
        "missing_docs": missing_docs,
        "migration_path": str(MIGRATION_PATH.relative_to(PACKAGE_DIR)),
        "side_effects": (),
    }


def pbc_implementation_release_audit() -> dict[str, Any]:
    service = build_service_contract()
    api = build_api_contract()
    ui = build_ui_contract()
    agent = build_agent_contract()
    events = build_event_contract()
    boundary = verify_owned_table_boundary(RUNTIME_TABLES + ("api_dependency",))
    smoke = slice_app_smoke_test()
    checks = (
        {"id": "service_contract", "ok": service["ok"]},
        {"id": "api_contract", "ok": api["ok"]},
        {"id": "ui_surface", "ok": ui["ok"] and bool(ui["forms"]) and bool(ui["wizards"]) and bool(ui["controls"])},
        {"id": "agent_contract", "ok": agent["ok"]},
        {"id": "event_contract", "ok": events["ok"] and events["contract"] == "AppGen-X"},
        {"id": "owned_boundary", "ok": boundary["ok"]},
        {"id": "slice_smoke", "ok": smoke["ok"]},
    )
    return {
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "smoke": smoke,
        "side_effects": (),
    }


def pbc_generation_smoke_audit() -> dict[str, Any]:
    smoke = slice_app_smoke_test()
    route_contract = build_api_contract()
    models = build_models_contract()
    return {
        "ok": smoke["ok"] and route_contract["ok"] and models["ok"],
        "pbc": PBC_KEY,
        "route_count": len(route_contract["routes"]),
        "model_count": len(models["models"]),
        "smoke": smoke,
        "side_effects": (),
    }


def build_release_evidence() -> dict[str, Any]:
    source = pbc_source_artifact_contract()
    implementation = pbc_implementation_release_audit()
    generation = pbc_generation_smoke_audit()
    checks = (
        {"id": "pbc_source_artifact_contract", "ok": source["ok"]},
        {"id": "pbc_implementation_release_audit", "ok": implementation["ok"]},
        {"id": "pbc_generation_smoke_audit", "ok": generation["ok"]},
        {"id": "owned_table_depth", "ok": len(BUSINESS_TABLES) >= 20},
        {"id": "domain_operation_depth", "ok": len(DOMAIN_OPERATIONS) >= 15},
        {"id": "forms_wizards_controls_present", "ok": bool(FORM_DEFINITIONS) and bool(WIZARD_DEFINITIONS) and bool(CONTROL_DEFINITIONS)},
    )
    return {
        "format": f"appgen.{PBC_KEY}.release-evidence.v1",
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "checks": checks,
        "blocking_gaps": tuple(check["id"] for check in checks if not check["ok"]),
        "boundary_gaps": source["schema_contract"].get("boundary_gaps", ()),
        "audits": {
            "pbc_source_artifact_contract": source,
            "pbc_implementation_release_audit": implementation,
            "pbc_generation_smoke_audit": generation,
        },
        "side_effects": (),
    }


def build_runtime_capabilities() -> dict[str, Any]:
    smoke = slice_app_smoke_test()
    return {
        "format": f"appgen.{PBC_KEY}.runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": PBC_KEY,
        "implementation_directory": "src/pyAppGen/pbcs/customer_success_management",
        "owned_tables": RUNTIME_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS[:-1],
        "capabilities": _dedupe(tuple(PBC_MANIFEST["advanced_capabilities"])),
        "standard_features": _dedupe(tuple(PBC_MANIFEST["standard_features"])),
        "operations": _dedupe(tuple(build_service_contract()["command_methods"] + build_service_contract()["query_methods"])),
        "smoke": smoke,
        "side_effects": (),
    }
