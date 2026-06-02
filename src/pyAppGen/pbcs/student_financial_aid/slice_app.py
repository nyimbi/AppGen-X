"""Standalone executable slice app for the student_financial_aid PBC."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any

from .manifest import PBC_MANIFEST

PBC_KEY = "student_financial_aid"
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
ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
EMITTED_EVENTS = tuple(PBC_MANIFEST["emits"])
CONSUMED_EVENTS = tuple(PBC_MANIFEST["consumes"])
PERMISSIONS = tuple(PBC_MANIFEST["permissions"])
RULE_KEYS = (
    "aid_year_policy",
    "dependency_review_policy",
    "verification_resolution_policy",
    "sap_policy",
    "need_analysis_policy",
    "award_packaging_policy",
    "disbursement_policy",
    "return_of_funds_policy",
    "professional_judgment_policy",
    "appeal_policy",
    "compliance_policy",
)
PARAMETER_KEYS = (
    "workbench_limit",
    "verification_due_days",
    "minimum_sap_gpa",
    "minimum_sap_pace",
    "default_loan_cap",
    "default_work_study_cap",
    "packaging_buffer_amount",
    "communication_sla_hours",
)
DOMAIN_OPERATIONS = (
    "setup_aid_year",
    "create_student_aid_profile",
    "intake_aid_application",
    "review_dependency_and_verification",
    "register_document_artifact",
    "evaluate_sap",
    "capture_cost_of_attendance",
    "analyze_need",
    "package_awards",
    "schedule_disbursement",
    "review_return_refund_overaward",
    "submit_professional_judgment",
    "record_appeal",
    "track_compliance_obligation",
    "log_communication",
)
BUSINESS_TABLES = (
    f"{PBC_KEY}_aid_year",
    f"{PBC_KEY}_student_aid_profile",
    f"{PBC_KEY}_aid_application",
    f"{PBC_KEY}_dependency_review",
    f"{PBC_KEY}_verification_item",
    f"{PBC_KEY}_document_artifact",
    f"{PBC_KEY}_sap_evaluation",
    f"{PBC_KEY}_cost_of_attendance_budget",
    f"{PBC_KEY}_need_analysis",
    f"{PBC_KEY}_award_package",
    f"{PBC_KEY}_award_line",
    f"{PBC_KEY}_scholarship_resource",
    f"{PBC_KEY}_grant_eligibility",
    f"{PBC_KEY}_loan_offer",
    f"{PBC_KEY}_work_study_plan",
    f"{PBC_KEY}_disbursement_schedule",
    f"{PBC_KEY}_refund_return_case",
    f"{PBC_KEY}_overaward_case",
    f"{PBC_KEY}_professional_judgment_case",
    f"{PBC_KEY}_aid_appeal",
    f"{PBC_KEY}_aid_compliance_obligation",
    f"{PBC_KEY}_communication_log",
    f"{PBC_KEY}_policy_rule",
    f"{PBC_KEY}_runtime_parameter",
    f"{PBC_KEY}_schema_extension",
    f"{PBC_KEY}_control_assertion",
    f"{PBC_KEY}_governed_model",
)
EVENT_TABLES = (
    f"{PBC_KEY}_appgen_outbox_event",
    f"{PBC_KEY}_appgen_inbox_event",
    f"{PBC_KEY}_appgen_dead_letter_event",
)
RUNTIME_TABLES = BUSINESS_TABLES + EVENT_TABLES
COMMAND_METHODS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
) + DOMAIN_OPERATIONS + (
    "run_advanced_assessment",
    "parse_document_instruction",
    "build_schema_contract",
    "build_service_contract",
    "build_release_evidence",
)
QUERY_METHODS = (
    "query_workbench",
    "build_workbench_view",
)
ROUTE_DEFINITIONS = (
    {"method": "POST", "path": "/aid-years", "operation": "setup_aid_year"},
    {"method": "POST", "path": "/student-aid-profiles", "operation": "create_student_aid_profile"},
    {"method": "POST", "path": "/aid-applications", "operation": "intake_aid_application"},
    {"method": "POST", "path": "/dependency-reviews", "operation": "review_dependency_and_verification"},
    {"method": "POST", "path": "/verification-documents", "operation": "register_document_artifact"},
    {"method": "POST", "path": "/sap-evaluations", "operation": "evaluate_sap"},
    {"method": "POST", "path": "/cost-of-attendance-budgets", "operation": "capture_cost_of_attendance"},
    {"method": "POST", "path": "/need-analyses", "operation": "analyze_need"},
    {"method": "POST", "path": "/award-packages", "operation": "package_awards"},
    {"method": "POST", "path": "/disbursement-schedules", "operation": "schedule_disbursement"},
    {"method": "POST", "path": "/refund-return-reviews", "operation": "review_return_refund_overaward"},
    {"method": "POST", "path": "/professional-judgment-cases", "operation": "submit_professional_judgment"},
    {"method": "POST", "path": "/aid-appeals", "operation": "record_appeal"},
    {"method": "POST", "path": "/compliance-obligations", "operation": "track_compliance_obligation"},
    {"method": "POST", "path": "/communications", "operation": "log_communication"},
    {"method": "POST", "path": "/agent/document-plan", "operation": "document_instruction_plan"},
    {"method": "POST", "path": "/agent/crud-plan", "operation": "datastore_crud_plan"},
    {"method": "GET", "path": "/student-financial-aid-workbench", "operation": "query_workbench"},
)
FORM_DEFINITIONS = (
    {
        "id": "aid_year_setup",
        "title": "Aid year setup",
        "operation": "setup_aid_year",
        "fields": (
            "tenant",
            "aid_year_code",
            "award_year_label",
            "packaging_start_date",
            "packaging_end_date",
            "default_budget_mode",
        ),
    },
    {
        "id": "student_aid_profile_intake",
        "title": "Student aid profile",
        "operation": "create_student_aid_profile",
        "fields": (
            "tenant",
            "aid_year_code",
            "student_id",
            "student_name",
            "program",
            "residency",
            "dependency_status",
            "enrollment_intensity",
        ),
    },
    {
        "id": "fafsa_isir_intake",
        "title": "FAFSA/ISIR-equivalent intake",
        "operation": "intake_aid_application",
        "fields": (
            "tenant",
            "aid_year_code",
            "student_aid_profile_id",
            "application_id",
            "student_aid_index",
            "household_size",
            "family_members_in_college",
            "verification_selected",
        ),
    },
    {
        "id": "award_packaging",
        "title": "Packaging worksheet",
        "operation": "package_awards",
        "fields": (
            "tenant",
            "aid_year_code",
            "student_aid_profile_id",
            "need_analysis_id",
            "scholarship_amount",
            "grant_amount",
            "loan_amount",
            "work_study_amount",
        ),
    },
    {
        "id": "professional_judgment",
        "title": "Professional judgment",
        "operation": "submit_professional_judgment",
        "fields": (
            "tenant",
            "aid_year_code",
            "student_aid_profile_id",
            "case_reason",
            "adjusted_field",
            "adjusted_value",
            "reviewer",
        ),
    },
    {
        "id": "appeal_form",
        "title": "Aid appeal",
        "operation": "record_appeal",
        "fields": (
            "tenant",
            "aid_year_code",
            "student_aid_profile_id",
            "appeal_type",
            "reason",
            "committee_decision",
            "conditions",
        ),
    },
)
WIZARD_DEFINITIONS = (
    {
        "id": "eligibility_review_wizard",
        "title": "Eligibility review wizard",
        "steps": (
            "profile",
            "application",
            "dependency",
            "verification",
            "sap",
            "need-analysis",
        ),
    },
    {
        "id": "packaging_release_wizard",
        "title": "Packaging and release wizard",
        "steps": (
            "budget",
            "need",
            "awards",
            "disbursement",
            "notices",
        ),
    },
    {
        "id": "exception_resolution_wizard",
        "title": "Exception resolution wizard",
        "steps": (
            "overaward",
            "return-of-funds",
            "professional-judgment",
            "appeal",
            "compliance",
        ),
    },
)
CONTROL_DEFINITIONS = (
    {"id": "policy_rule_editor", "type": "rule-editor", "targets": RULE_KEYS},
    {"id": "runtime_parameter_editor", "type": "parameter-editor", "targets": PARAMETER_KEYS},
    {"id": "award_matrix_preview", "type": "packaging-control", "targets": ("package_awards", "schedule_disbursement")},
    {"id": "disbursement_gate_checklist", "type": "approval-checklist", "targets": ("schedule_disbursement", "review_return_refund_overaward")},
    {"id": "agent_mutation_guard", "type": "approval-guard", "targets": ("document_instruction_plan", "datastore_crud_plan")},
    {"id": "event_replay_console", "type": "event-console", "targets": EVENT_TABLES},
)
TABLE_DESCRIPTION_OVERRIDES = {
    f"{PBC_KEY}_aid_year": "Aid-year calendar, packaging windows, and annual controls.",
    f"{PBC_KEY}_student_aid_profile": "Student aid identity, residency, program, and enrollment profile.",
    f"{PBC_KEY}_aid_application": "FAFSA/ISIR-equivalent application intake and lifecycle record.",
    f"{PBC_KEY}_dependency_review": "Dependency, household, and special-circumstance review evidence.",
    f"{PBC_KEY}_verification_item": "Verification checklist item with due dates and discrepancy handling.",
    f"{PBC_KEY}_document_artifact": "Governed document-tracking artifact for tax, identity, appeal, and verification files.",
    f"{PBC_KEY}_sap_evaluation": "Satisfactory academic progress evaluation result and appeal posture.",
    f"{PBC_KEY}_cost_of_attendance_budget": "Cost-of-attendance budget by component and student category.",
    f"{PBC_KEY}_need_analysis": "Need-analysis trace with aid index, resources, and unmet need.",
    f"{PBC_KEY}_award_package": "Packaging outcome across scholarships, grants, loans, and work study.",
    f"{PBC_KEY}_award_line": "Individual aid-line detail for a packaging decision.",
    f"{PBC_KEY}_scholarship_resource": "Institutional or external scholarship resource evidence.",
    f"{PBC_KEY}_grant_eligibility": "Grant-eligibility record and capped amount.",
    f"{PBC_KEY}_loan_offer": "Loan counseling and promissory-note-aware offer record.",
    f"{PBC_KEY}_work_study_plan": "Work-study allocation and supervisor planning artifact.",
    f"{PBC_KEY}_disbursement_schedule": "Disbursement release schedule and blocker checklist.",
    f"{PBC_KEY}_refund_return_case": "Return-of-funds or refund review record.",
    f"{PBC_KEY}_overaward_case": "Overaward case, adjustment plan, and closure evidence.",
    f"{PBC_KEY}_professional_judgment_case": "Professional-judgment case preserving original and adjusted facts.",
    f"{PBC_KEY}_aid_appeal": "Appeal submission, committee decision, and conditions record.",
    f"{PBC_KEY}_aid_compliance_obligation": "Compliance calendar obligation with owner and due date.",
    f"{PBC_KEY}_communication_log": "Student communication, notices, and outreach log.",
    f"{PBC_KEY}_policy_rule": "Compiled student-aid policy rule.",
    f"{PBC_KEY}_runtime_parameter": "Bounded runtime parameter.",
    f"{PBC_KEY}_schema_extension": "Owned schema extension registration.",
    f"{PBC_KEY}_control_assertion": "Control assertion and audit evidence.",
    f"{PBC_KEY}_governed_model": "Governed AI model registration and preview policy.",
}


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
        description=TABLE_DESCRIPTION_OVERRIDES.get(
            table,
            table.removeprefix(f"{PBC_KEY}_").replace("_", " ").title(),
        ),
        foreign_key_table=(
            f"{PBC_KEY}_student_aid_profile"
            if table.startswith(f"{PBC_KEY}_")
            and table not in EVENT_TABLES
            and table
            not in {
                f"{PBC_KEY}_aid_year",
                f"{PBC_KEY}_student_aid_profile",
                f"{PBC_KEY}_policy_rule",
                f"{PBC_KEY}_runtime_parameter",
                f"{PBC_KEY}_schema_extension",
                f"{PBC_KEY}_control_assertion",
                f"{PBC_KEY}_governed_model",
            }
            else None
        ),
    )
    for table in RUNTIME_TABLES
)
MODEL_FIELDS = (
    "id",
    "tenant",
    "code",
    "status",
    "aid_year_code",
    "primary_subject_id",
    "secondary_subject_id",
    "record_stage",
    "amount",
    "currency",
    "payload",
    "created_at",
    "updated_at",
)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _load_json(value: Any) -> Any:
    if isinstance(value, str):
        return json.loads(value)
    return value


def _code(prefix: str, tenant: str, unique_source: Any) -> str:
    return f"{prefix}-{tenant}-{_digest(unique_source)[:8]}".upper()


def _dedupe(items: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(items))


def _money(value: Any, default: float = 0.0) -> float:
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return round(default, 2)


def _class_name(table: str) -> str:
    return "".join(part.capitalize() for part in table.split("_"))


class SQLiteOwnedRepository:
    """Minimal package-local owned datastore for the standalone slice app."""

    def __init__(self, database_url: str = ":memory:") -> None:
        self.connection = sqlite3.connect(database_url)
        self.connection.row_factory = sqlite3.Row

    def bootstrap(self) -> None:
        self.connection.executescript(MIGRATION_PATH.read_text(encoding="utf-8"))
        self.connection.commit()

    def insert(self, table: str, record: dict[str, Any]) -> dict[str, Any]:
        serialized = {
            key: (_json(value) if key == "payload" else value)
            for key, value in record.items()
        }
        fields = tuple(serialized)
        placeholders = ", ".join("?" for _ in fields)
        sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"
        self.connection.execute(sql, tuple(serialized[field] for field in fields))
        self.connection.commit()
        fetched = self.fetch_one(table, record["id"])
        return fetched if fetched is not None else dict(record)

    def fetch_one(self, table: str, record_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            f"SELECT * FROM {table} WHERE id = ?",
            (record_id,),
        ).fetchone()
        return self._row_to_dict(row) if row else None

    def fetch_latest(
        self,
        table: str,
        *,
        tenant: str | None = None,
        primary_subject_id: str | None = None,
        code: str | None = None,
    ) -> dict[str, Any] | None:
        clauses = []
        values: list[Any] = []
        if tenant is not None:
            clauses.append("tenant = ?")
            values.append(tenant)
        if primary_subject_id is not None:
            clauses.append("primary_subject_id = ?")
            values.append(primary_subject_id)
        if code is not None:
            clauses.append("code = ?")
            values.append(code)
        sql = f"SELECT * FROM {table}"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY created_at DESC LIMIT 1"
        row = self.connection.execute(sql, tuple(values)).fetchone()
        return self._row_to_dict(row) if row else None

    def fetch_all(
        self,
        table: str,
        *,
        tenant: str | None = None,
        limit: int | None = None,
        where: str | None = None,
        params: tuple[Any, ...] = (),
    ) -> tuple[dict[str, Any], ...]:
        clauses = []
        values: list[Any] = []
        if tenant is not None:
            clauses.append("tenant = ?")
            values.append(tenant)
        if where:
            clauses.append(where)
            values.extend(params)
        sql = f"SELECT * FROM {table}"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY created_at DESC"
        if limit is not None:
            sql += f" LIMIT {int(limit)}"
        rows = self.connection.execute(sql, tuple(values)).fetchall()
        return tuple(self._row_to_dict(row) for row in rows)

    def count(
        self,
        table: str,
        *,
        tenant: str | None = None,
        where: str | None = None,
        params: tuple[Any, ...] = (),
    ) -> int:
        clauses = []
        values: list[Any] = []
        if tenant is not None:
            clauses.append("tenant = ?")
            values.append(tenant)
        if where:
            clauses.append(where)
            values.extend(params)
        sql = f"SELECT COUNT(*) AS c FROM {table}"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        row = self.connection.execute(sql, tuple(values)).fetchone()
        return int(row["c"] if row else 0)

    def _row_to_dict(self, row: sqlite3.Row) -> dict[str, Any]:
        data = dict(row)
        if "payload" in data:
            data["payload"] = _load_json(data["payload"])
        return data


def build_standalone_app(database_url: str = ":memory:") -> "StudentFinancialAidSliceApp":
    return StudentFinancialAidSliceApp(SQLiteOwnedRepository(database_url))


class StudentFinancialAidSliceApp:
    def __init__(self, repository: SQLiteOwnedRepository) -> None:
        self.repository = repository
        self.repository.bootstrap()
        self._handled_event_keys: set[str] = set()

    def _create_record(
        self,
        table: str,
        *,
        tenant: str,
        code: str,
        status: str,
        payload: dict[str, Any],
        aid_year_code: str = "",
        primary_subject_id: str = "",
        secondary_subject_id: str = "",
        record_stage: str = "",
        amount: float = 0.0,
        currency: str = "USD",
    ) -> dict[str, Any]:
        now = _utcnow()
        record = {
            "id": _digest((table, tenant, code, payload, now))[:24],
            "tenant": tenant,
            "code": code,
            "status": status,
            "aid_year_code": aid_year_code,
            "primary_subject_id": primary_subject_id,
            "secondary_subject_id": secondary_subject_id,
            "record_stage": record_stage,
            "amount": _money(amount),
            "currency": currency,
            "payload": dict(payload),
            "created_at": now,
            "updated_at": now,
        }
        return self.repository.insert(table, record)

    def _event(self, event_type: str, tenant: str, payload: dict[str, Any]) -> dict[str, Any]:
        envelope = {
            "event_type": event_type,
            "topic": APPGEN_X_TOPIC,
            "payload": dict(payload),
            "idempotency_key": _digest((event_type, payload)),
            "event_contract": "AppGen-X",
        }
        event = self._create_record(
            EVENT_TABLES[0],
            tenant=tenant,
            code=_code("OUTBOX", tenant, envelope),
            status="ready",
            payload=envelope,
            primary_subject_id=payload.get("student_aid_profile_id", ""),
            aid_year_code=payload.get("aid_year_code", ""),
            record_stage=event_type,
        )
        return {"event": event, "event_type": event_type}

    def _latest_amount(self, table: str, tenant: str, primary_subject_id: str) -> float:
        record = self.repository.fetch_latest(
            table,
            tenant=tenant,
            primary_subject_id=primary_subject_id,
        )
        return _money(record["amount"]) if record else 0.0

    def _summary(self, tenant: str) -> dict[str, Any]:
        return {
            "aid_year_count": self.repository.count(BUSINESS_TABLES[0], tenant=tenant),
            "profile_count": self.repository.count(BUSINESS_TABLES[1], tenant=tenant),
            "application_count": self.repository.count(BUSINESS_TABLES[2], tenant=tenant),
            "verification_open_count": self.repository.count(BUSINESS_TABLES[4], tenant=tenant, where="status != ?", params=("complete",)),
            "packaged_count": self.repository.count(BUSINESS_TABLES[9], tenant=tenant, where="status IN (?, ?)", params=("packaged", "review_required")),
            "scheduled_disbursement_count": self.repository.count(BUSINESS_TABLES[15], tenant=tenant, where="status = ?", params=("scheduled",)),
            "exception_count": self.repository.count(BUSINESS_TABLES[17], tenant=tenant) + self.repository.count(BUSINESS_TABLES[16], tenant=tenant),
            "compliance_open_count": self.repository.count(BUSINESS_TABLES[20], tenant=tenant, where="status != ?", params=("complete",)),
            "communication_count": self.repository.count(BUSINESS_TABLES[21], tenant=tenant),
        }

    def configure_runtime(self, config: dict[str, Any]) -> dict[str, Any]:
        configuration = {
            **dict(config),
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        }
        ok = (
            configuration.get("database_backend") in ALLOWED_DATABASE_BACKENDS
            and configuration.get("event_topic", APPGEN_X_TOPIC) == APPGEN_X_TOPIC
        )
        return {
            "ok": ok,
            "configuration": configuration,
            "side_effects": (),
        }

    def set_parameter(self, name: str, value: Any) -> dict[str, Any]:
        parameter = self._create_record(
            BUSINESS_TABLES[23],
            tenant="system",
            code=name,
            status="active",
            payload={"name": name, "value": value, "bounded": name in PARAMETER_KEYS},
            record_stage="parameter",
        )
        return {"ok": name in PARAMETER_KEYS, "parameter": parameter, "side_effects": ()}

    def register_rule(self, rule: dict[str, Any]) -> dict[str, Any]:
        rule_id = rule.get("rule_id", "unnamed_rule")
        compiled = {**dict(rule), "compiled_hash": _digest(rule), "event_contract": "AppGen-X"}
        record = self._create_record(
            BUSINESS_TABLES[22],
            tenant="system",
            code=rule_id,
            status="compiled",
            payload=compiled,
            record_stage="rule",
        )
        return {"ok": True, "rule": record, "side_effects": ()}

    def register_schema_extension(self, table: str, fields: dict[str, Any]) -> dict[str, Any]:
        owned_name = table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        if owned_name not in RUNTIME_TABLES:
            return {"ok": False, "reason": "unknown_owned_table", "table": owned_name, "side_effects": ()}
        record = self._create_record(
            BUSINESS_TABLES[24],
            tenant="system",
            code=owned_name,
            status="registered",
            payload={"table": owned_name, "fields": dict(fields)},
            primary_subject_id=owned_name,
            record_stage="schema_extension",
        )
        return {"ok": True, "record": record, "table": owned_name, "fields": dict(fields), "side_effects": ()}

    def setup_aid_year(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code") or payload.get("code") or "2026-2027"
        year = self._create_record(
            BUSINESS_TABLES[0],
            tenant=tenant,
            code=aid_year_code,
            status="active",
            payload={
                "award_year_label": payload.get("award_year_label", aid_year_code),
                "packaging_start_date": payload.get("packaging_start_date", "2026-01-01"),
                "packaging_end_date": payload.get("packaging_end_date", "2027-06-30"),
                "default_budget_mode": payload.get("default_budget_mode", "standard"),
            },
            aid_year_code=aid_year_code,
            record_stage="setup",
        )
        obligations = tuple(
            self._create_record(
                BUSINESS_TABLES[20],
                tenant=tenant,
                code=f"{aid_year_code}-{code}",
                status="open",
                payload={"obligation": title, "owner": payload.get("owner", "aid-ops"), "due_date": due_date},
                aid_year_code=aid_year_code,
                record_stage="compliance",
            )
            for code, title, due_date in (
                ("VERIFICATION", "Verification closeout", "2026-10-15"),
                ("DISBURSEMENT", "Disbursement reconciliation", "2026-12-01"),
                ("CLOSEOUT", "Aid year reporting closeout", "2027-07-15"),
            )
        )
        control = self._create_record(
            BUSINESS_TABLES[25],
            tenant=tenant,
            code=f"CTRL-{aid_year_code}",
            status="active",
            payload={"control": "aid_year_ready", "aid_year_code": aid_year_code, "owner": payload.get("owner", "aid-director")},
            aid_year_code=aid_year_code,
            record_stage="control",
        )
        event = self._event(EMITTED_EVENTS[0], tenant, {"aid_year_id": year["id"], "aid_year_code": aid_year_code})
        return {
            "ok": True,
            "record": year,
            "compliance_obligations": obligations,
            "control_assertion": control,
            "event_type": event["event_type"],
            "side_effects": (),
        }

    def create_student_aid_profile(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        student_id = payload.get("student_id") or payload.get("code") or _code("STU", tenant, payload)
        record = self._create_record(
            BUSINESS_TABLES[1],
            tenant=tenant,
            code=student_id,
            status="active",
            payload={
                "student_name": payload.get("student_name", "Student Example"),
                "program": payload.get("program", "Undergraduate"),
                "residency": payload.get("residency", "in_state"),
                "dependency_status": payload.get("dependency_status", "dependent"),
                "enrollment_intensity": payload.get("enrollment_intensity", "full_time"),
            },
            aid_year_code=aid_year_code,
            primary_subject_id=student_id,
            record_stage="profile",
        )
        event = self._event(EMITTED_EVENTS[0], tenant, {"student_aid_profile_id": record["id"], "aid_year_code": aid_year_code})
        return {"ok": True, "record": record, "event_type": event["event_type"], "side_effects": ()}

    def intake_aid_application(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        application_code = payload.get("application_id") or payload.get("code") or _code("FAFSA", tenant, payload)
        verification_selected = bool(payload.get("verification_selected", True))
        application = self._create_record(
            BUSINESS_TABLES[2],
            tenant=tenant,
            code=application_code,
            status="submitted",
            payload={
                "student_aid_index": _money(payload.get("student_aid_index"), 2500.0),
                "household_size": int(payload.get("household_size", 3)),
                "family_members_in_college": int(payload.get("family_members_in_college", 1)),
                "fafsa_isir_equivalent": True,
                "verification_selected": verification_selected,
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            record_stage="application",
        )
        dependency = self._create_record(
            BUSINESS_TABLES[3],
            tenant=tenant,
            code=f"DEP-{application_code}",
            status="pending_review",
            payload={
                "dependency_status": payload.get("dependency_status", "dependent"),
                "household_size": int(payload.get("household_size", 3)),
                "special_circumstances": bool(payload.get("special_circumstances", False)),
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=application["id"],
            record_stage="dependency",
        )
        verification_items = tuple(
            self._create_record(
                BUSINESS_TABLES[4],
                tenant=tenant,
                code=f"VERIFY-{application_code}-{index}",
                status="pending" if verification_selected else "waived",
                payload={"required_document": name, "due_date": "2026-09-15", "selection_reason": "application-selected"},
                aid_year_code=aid_year_code,
                primary_subject_id=profile_id,
                secondary_subject_id=application["id"],
                record_stage="verification",
            )
            for index, name in enumerate(("identity", "income", "household"), start=1)
        )
        documents = tuple(
            self._create_record(
                BUSINESS_TABLES[5],
                tenant=tenant,
                code=f"DOC-{application_code}-{index}",
                status="received",
                payload={"document_type": doc, "source": "student", "confidence": 0.86},
                aid_year_code=aid_year_code,
                primary_subject_id=profile_id,
                secondary_subject_id=application["id"],
                record_stage="document",
            )
            for index, doc in enumerate(payload.get("documents", ("fafsa-intake",)), start=1)
        )
        notice = self._create_record(
            BUSINESS_TABLES[21],
            tenant=tenant,
            code=f"COMM-{application_code}",
            status="sent",
            payload={"channel": "portal", "template": "application_received", "message": "Application received and queued for review."},
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=application["id"],
            record_stage="communication",
        )
        event = self._event(EMITTED_EVENTS[0], tenant, {"application_id": application["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {
            "ok": True,
            "record": application,
            "dependency_review": dependency,
            "verification_items": verification_items,
            "documents": documents,
            "notification": notice,
            "event_type": event["event_type"],
            "side_effects": (),
        }

    def review_dependency_and_verification(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        unresolved = int(payload.get("unresolved_count", 0))
        status = "approved" if unresolved == 0 and payload.get("dependency_override") != "pending" else "needs_follow_up"
        review = self._create_record(
            BUSINESS_TABLES[3],
            tenant=tenant,
            code=payload.get("code") or _code("DEP-REVIEW", tenant, payload),
            status=status,
            payload={
                "dependency_override": payload.get("dependency_override", "not_requested"),
                "reviewer": payload.get("reviewer", "aid-counselor"),
                "household_size": int(payload.get("household_size", 3)),
                "unresolved_count": unresolved,
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=payload.get("aid_application_id", ""),
            record_stage="verification_review",
        )
        verification = self._create_record(
            BUSINESS_TABLES[4],
            tenant=tenant,
            code=payload.get("verification_code") or _code("VERIFY", tenant, payload),
            status="complete" if unresolved == 0 else "pending",
            payload={"review_status": status, "required_document": payload.get("required_document", "signed-statement")},
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=review["id"],
            record_stage="verification",
        )
        event_type = EMITTED_EVENTS[2] if status == "approved" else EMITTED_EVENTS[1]
        self._event(event_type, tenant, {"student_aid_profile_id": profile_id, "dependency_review_id": review["id"], "aid_year_code": aid_year_code})
        return {"ok": True, "record": review, "verification_item": verification, "event_type": event_type, "side_effects": ()}

    def register_document_artifact(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        record = self._create_record(
            BUSINESS_TABLES[5],
            tenant=tenant,
            code=payload.get("code") or _code("DOC", tenant, payload),
            status=payload.get("status", "received"),
            payload={
                "document_type": payload.get("document_type", "tax-transcript"),
                "source": payload.get("source", "student-upload"),
                "extracted_fields": tuple(payload.get("extracted_fields", ("agi", "household_size"))),
                "confidence": float(payload.get("confidence", 0.82)),
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=payload.get("aid_application_id", ""),
            record_stage="document",
        )
        self._event(EMITTED_EVENTS[1], tenant, {"document_artifact_id": record["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {"ok": True, "record": record, "event_type": EMITTED_EVENTS[1], "side_effects": ()}

    def evaluate_sap(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        gpa = float(payload.get("gpa", 2.6))
        pace = float(payload.get("pace", 0.82))
        timeframe_remaining = float(payload.get("timeframe_remaining", 0.9))
        if gpa >= 2.0 and pace >= 0.67 and timeframe_remaining > 0:
            status = "pass"
        elif gpa >= 1.8 and pace >= 0.60:
            status = "warning"
        elif payload.get("appeal_status") == "approved":
            status = "probation"
        else:
            status = "suspension"
        record = self._create_record(
            BUSINESS_TABLES[6],
            tenant=tenant,
            code=payload.get("code") or _code("SAP", tenant, payload),
            status=status,
            payload={
                "gpa": gpa,
                "pace": pace,
                "timeframe_remaining": timeframe_remaining,
                "appeal_status": payload.get("appeal_status", "not_requested"),
                "next_review_date": payload.get("next_review_date", "2026-12-15"),
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            record_stage="sap",
        )
        event_type = EMITTED_EVENTS[2] if status in {"pass", "warning", "probation"} else EMITTED_EVENTS[3]
        self._event(event_type, tenant, {"sap_evaluation_id": record["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {"ok": True, "record": record, "event_type": event_type, "side_effects": ()}

    def capture_cost_of_attendance(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        components = {
            "tuition": _money(payload.get("tuition", 8500.0)),
            "fees": _money(payload.get("fees", 1200.0)),
            "housing": _money(payload.get("housing", 4800.0)),
            "food": _money(payload.get("food", 2400.0)),
            "books": _money(payload.get("books", 900.0)),
            "transportation": _money(payload.get("transportation", 700.0)),
            "personal": _money(payload.get("personal", 600.0)),
            "dependent_care": _money(payload.get("dependent_care", 0.0)),
        }
        total = round(sum(components.values()), 2)
        record = self._create_record(
            BUSINESS_TABLES[7],
            tenant=tenant,
            code=payload.get("code") or _code("COA", tenant, payload),
            status="approved",
            payload={**components, "housing_status": payload.get("housing_status", "off_campus")},
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            record_stage="budget",
            amount=total,
        )
        self._event(EMITTED_EVENTS[1], tenant, {"budget_id": record["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {"ok": True, "record": record, "total": total, "event_type": EMITTED_EVENTS[1], "side_effects": ()}

    def analyze_need(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        coa_total = _money(payload.get("coa_total"), self._latest_amount(BUSINESS_TABLES[7], tenant, profile_id) or 15000.0)
        student_aid_index = _money(payload.get("student_aid_index"), 2500.0)
        external_resources = _money(payload.get("external_resources"), 0.0)
        other_resources = _money(payload.get("other_resources"), 0.0)
        total_resources = round(student_aid_index + external_resources + other_resources, 2)
        unmet_need = round(max(coa_total - total_resources, 0.0), 2)
        record = self._create_record(
            BUSINESS_TABLES[8],
            tenant=tenant,
            code=payload.get("code") or _code("NEED", tenant, payload),
            status="calculated",
            payload={
                "coa_total": coa_total,
                "student_aid_index": student_aid_index,
                "external_resources": external_resources,
                "other_resources": other_resources,
                "total_resources": total_resources,
                "unmet_need": unmet_need,
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            record_stage="need_analysis",
            amount=unmet_need,
        )
        self._event(EMITTED_EVENTS[1], tenant, {"need_analysis_id": record["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {"ok": True, "record": record, "unmet_need": unmet_need, "event_type": EMITTED_EVENTS[1], "side_effects": ()}

    def package_awards(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        unmet_need = _money(payload.get("unmet_need"), self._latest_amount(BUSINESS_TABLES[8], tenant, profile_id) or 8500.0)
        coa_total = _money(payload.get("coa_total"), unmet_need + 2500.0)
        scholarship = min(_money(payload.get("scholarship_amount"), 2000.0), unmet_need)
        remaining = max(unmet_need - scholarship, 0.0)
        grant = min(_money(payload.get("grant_amount"), 3000.0), remaining)
        remaining = max(remaining - grant, 0.0)
        loan = min(_money(payload.get("loan_amount"), 3500.0), remaining)
        remaining = max(remaining - loan, 0.0)
        work_study = min(_money(payload.get("work_study_amount"), 1500.0), remaining)
        total_awards = round(scholarship + grant + loan + work_study, 2)
        external_resources = _money(payload.get("external_resources"), 0.0)
        overaward_amount = round(max(total_awards + external_resources - coa_total, 0.0), 2)
        package_status = "review_required" if overaward_amount > 0 else "packaged"
        package = self._create_record(
            BUSINESS_TABLES[9],
            tenant=tenant,
            code=payload.get("code") or _code("PKG", tenant, payload),
            status=package_status,
            payload={
                "coa_total": coa_total,
                "unmet_need": unmet_need,
                "external_resources": external_resources,
                "fund_mix": {
                    "scholarship": scholarship,
                    "grant": grant,
                    "loan": loan,
                    "work_study": work_study,
                },
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            record_stage="packaging",
            amount=total_awards,
        )
        line_specs = (
            ("SCH", "scholarship", scholarship),
            ("GRT", "grant", grant),
            ("LOAN", "loan", loan),
            ("WS", "work_study", work_study),
        )
        award_lines = tuple(
            self._create_record(
                BUSINESS_TABLES[10],
                tenant=tenant,
                code=f"{prefix}-{package['code']}",
                status="offered",
                payload={"fund_type": fund_type, "award_package_id": package["id"]},
                aid_year_code=aid_year_code,
                primary_subject_id=profile_id,
                secondary_subject_id=package["id"],
                record_stage="award_line",
                amount=amount,
            )
            for prefix, fund_type, amount in line_specs
            if amount > 0
        )
        scholarship_resource = self._create_record(
            BUSINESS_TABLES[11],
            tenant=tenant,
            code=f"SCH-{package['code']}",
            status="confirmed" if scholarship > 0 else "not_applicable",
            payload={"resource_type": "institutional", "award_package_id": package["id"]},
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=package["id"],
            record_stage="scholarship",
            amount=scholarship,
        )
        grant_eligibility = self._create_record(
            BUSINESS_TABLES[12],
            tenant=tenant,
            code=f"GRT-{package['code']}",
            status="eligible" if grant > 0 else "not_eligible",
            payload={"grant_type": "need_based", "award_package_id": package["id"]},
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=package["id"],
            record_stage="grant",
            amount=grant,
        )
        loan_offer = self._create_record(
            BUSINESS_TABLES[13],
            tenant=tenant,
            code=f"LOAN-{package['code']}",
            status="offered" if loan > 0 else "not_offered",
            payload={"loan_type": "subsidized", "counseling_required": loan > 0, "award_package_id": package["id"]},
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=package["id"],
            record_stage="loan",
            amount=loan,
        )
        work_study_plan = self._create_record(
            BUSINESS_TABLES[14],
            tenant=tenant,
            code=f"WS-{package['code']}",
            status="planned" if work_study > 0 else "not_planned",
            payload={"supervisor": payload.get("supervisor", "career-services"), "award_package_id": package["id"]},
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=package["id"],
            record_stage="work_study",
            amount=work_study,
        )
        overaward_case = None
        event_type = EMITTED_EVENTS[2]
        if overaward_amount > 0:
            overaward_case = self._create_record(
                BUSINESS_TABLES[17],
                tenant=tenant,
                code=f"OVER-{package['code']}",
                status="open",
                payload={"reason": "awards_exceed_cost_of_attendance", "award_package_id": package["id"]},
                aid_year_code=aid_year_code,
                primary_subject_id=profile_id,
                secondary_subject_id=package["id"],
                record_stage="overaward",
                amount=overaward_amount,
            )
            event_type = EMITTED_EVENTS[3]
        self._event(event_type, tenant, {"award_package_id": package["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {
            "ok": True,
            "record": package,
            "award_lines": award_lines,
            "scholarship_resource": scholarship_resource,
            "grant_eligibility": grant_eligibility,
            "loan_offer": loan_offer,
            "work_study_plan": work_study_plan,
            "overaward_case": overaward_case,
            "event_type": event_type,
            "side_effects": (),
        }

    def schedule_disbursement(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        total_amount = _money(payload.get("scheduled_amount"), self._latest_amount(BUSINESS_TABLES[9], tenant, profile_id) or 4000.0)
        blockers = []
        if not payload.get("verification_complete", True):
            blockers.append("verification_pending")
        if payload.get("sap_status", "pass") == "suspension":
            blockers.append("sap_ineligible")
        if not payload.get("acceptance_received", True):
            blockers.append("award_acceptance_missing")
        periods = tuple(payload.get("payment_periods", ("term_1", "term_2")))
        split_amount = round(total_amount / max(len(periods), 1), 2)
        schedules = tuple(
            self._create_record(
                BUSINESS_TABLES[15],
                tenant=tenant,
                code=f"DISB-{period}-{_digest((tenant, profile_id, period))[:6]}",
                status="blocked" if blockers else "scheduled",
                payload={"payment_period": period, "blockers": tuple(blockers), "release_date": payload.get("release_date", "2026-09-01")},
                aid_year_code=aid_year_code,
                primary_subject_id=profile_id,
                secondary_subject_id=payload.get("award_package_id", ""),
                record_stage="disbursement",
                amount=split_amount,
            )
            for period in periods
        )
        event_type = EMITTED_EVENTS[3] if blockers else EMITTED_EVENTS[2]
        self._event(event_type, tenant, {"student_aid_profile_id": profile_id, "aid_year_code": aid_year_code, "blockers": tuple(blockers)})
        return {"ok": True, "records": schedules, "blockers": tuple(blockers), "event_type": event_type, "side_effects": ()}

    def review_return_refund_overaward(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        disbursed_amount = _money(payload.get("disbursed_amount"), 3000.0)
        earned_percent = float(payload.get("earned_percent", 0.45))
        earned_amount = round(disbursed_amount * earned_percent, 2)
        return_amount = round(max(disbursed_amount - earned_amount, 0.0), 2)
        overaward_amount = _money(payload.get("overaward_amount"), return_amount)
        refund_case = self._create_record(
            BUSINESS_TABLES[16],
            tenant=tenant,
            code=payload.get("refund_code") or _code("R2T4", tenant, payload),
            status="open" if return_amount > 0 else "closed",
            payload={"earned_percent": earned_percent, "earned_amount": earned_amount, "withdrawal_date": payload.get("withdrawal_date", "2026-10-10")},
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=payload.get("aid_application_id", ""),
            record_stage="return_refund",
            amount=return_amount,
        )
        overaward_case = self._create_record(
            BUSINESS_TABLES[17],
            tenant=tenant,
            code=payload.get("overaward_code") or _code("OVER", tenant, payload),
            status="open" if overaward_amount > 0 else "closed",
            payload={"reason": payload.get("reason", "enrollment_change_or_withdrawal"), "refund_return_case_id": refund_case["id"]},
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=refund_case["id"],
            record_stage="overaward",
            amount=overaward_amount,
        )
        self._event(EMITTED_EVENTS[3] if overaward_amount > 0 or return_amount > 0 else EMITTED_EVENTS[1], tenant, {"student_aid_profile_id": profile_id, "aid_year_code": aid_year_code, "refund_return_case_id": refund_case["id"]})
        return {"ok": True, "refund_return_case": refund_case, "overaward_case": overaward_case, "event_type": EMITTED_EVENTS[3] if overaward_amount > 0 or return_amount > 0 else EMITTED_EVENTS[1], "side_effects": ()}

    def submit_professional_judgment(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        status = payload.get("status", "pending_review")
        record = self._create_record(
            BUSINESS_TABLES[18],
            tenant=tenant,
            code=payload.get("code") or _code("PJ", tenant, payload),
            status=status,
            payload={
                "case_reason": payload.get("case_reason", "special_circumstance"),
                "adjusted_field": payload.get("adjusted_field", "income"),
                "adjusted_value": payload.get("adjusted_value", 0),
                "reviewer": payload.get("reviewer", "aid-director"),
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            record_stage="professional_judgment",
        )
        event_type = EMITTED_EVENTS[2] if status == "approved" else EMITTED_EVENTS[1]
        self._event(event_type, tenant, {"professional_judgment_case_id": record["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {"ok": True, "record": record, "event_type": event_type, "side_effects": ()}

    def record_appeal(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        decision = payload.get("committee_decision", "pending")
        record = self._create_record(
            BUSINESS_TABLES[19],
            tenant=tenant,
            code=payload.get("code") or _code("APPEAL", tenant, payload),
            status=decision,
            payload={
                "appeal_type": payload.get("appeal_type", "sap"),
                "reason": payload.get("reason", "documented hardship"),
                "committee_decision": decision,
                "conditions": payload.get("conditions", "academic plan required"),
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            secondary_subject_id=payload.get("professional_judgment_case_id", ""),
            record_stage="appeal",
        )
        event_type = EMITTED_EVENTS[2] if decision == "approved" else EMITTED_EVENTS[1]
        self._event(event_type, tenant, {"aid_appeal_id": record["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {"ok": True, "record": record, "event_type": event_type, "side_effects": ()}

    def track_compliance_obligation(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        status = payload.get("status", "open")
        record = self._create_record(
            BUSINESS_TABLES[20],
            tenant=tenant,
            code=payload.get("code") or _code("COMP", tenant, payload),
            status=status,
            payload={
                "obligation": payload.get("obligation", "verification_follow_up"),
                "owner": payload.get("owner", "compliance-officer"),
                "due_date": payload.get("due_date", "2026-11-01"),
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            record_stage="compliance",
        )
        self._event(EMITTED_EVENTS[1], tenant, {"aid_compliance_obligation_id": record["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {"ok": True, "record": record, "event_type": EMITTED_EVENTS[1], "side_effects": ()}

    def log_communication(self, payload: dict[str, Any]) -> dict[str, Any]:
        tenant = payload.get("tenant", "default")
        aid_year_code = payload.get("aid_year_code", "2026-2027")
        profile_id = payload.get("student_aid_profile_id", "")
        record = self._create_record(
            BUSINESS_TABLES[21],
            tenant=tenant,
            code=payload.get("code") or _code("COMM", tenant, payload),
            status=payload.get("status", "sent"),
            payload={
                "channel": payload.get("channel", "portal"),
                "template": payload.get("template", "status_update"),
                "message": payload.get("message", "Student aid update posted."),
            },
            aid_year_code=aid_year_code,
            primary_subject_id=profile_id,
            record_stage="communication",
        )
        self._event(EMITTED_EVENTS[1], tenant, {"communication_log_id": record["id"], "student_aid_profile_id": profile_id, "aid_year_code": aid_year_code})
        return {"ok": True, "record": record, "event_type": EMITTED_EVENTS[1], "side_effects": ()}

    def receive_event(self, event: dict[str, Any]) -> dict[str, Any]:
        tenant = event.get("tenant", "default")
        idem = event.get("idempotency_key") or event.get("event_id") or _digest(event)
        if idem in self._handled_event_keys:
            return {"ok": True, "duplicate": True, "idempotency_key": idem, "side_effects": ()}
        self._handled_event_keys.add(idem)
        envelope = {**dict(event), "event_contract": "AppGen-X", "idempotency_key": idem}
        if event.get("event_type") not in CONSUMED_EVENTS:
            dead = self._create_record(
                EVENT_TABLES[2],
                tenant=tenant,
                code=_code("DLQ", tenant, envelope),
                status="dead_letter",
                payload=envelope,
                record_stage="dead_letter",
            )
            return {"ok": False, "duplicate": False, "dead_letter": dead, "dead_letter_table": EVENT_TABLES[2], "idempotency_key": idem, "side_effects": ()}
        inbox = self._create_record(
            EVENT_TABLES[1],
            tenant=tenant,
            code=_code("INBOX", tenant, envelope),
            status="handled",
            payload=envelope,
            record_stage="inbox",
        )
        return {"ok": True, "duplicate": False, "record": inbox, "idempotency_key": idem, "side_effects": ()}

    def query_workbench(self, tenant: str = "default") -> dict[str, Any]:
        summary = self._summary(tenant)
        records = {
            "aid_years": self.repository.fetch_all(BUSINESS_TABLES[0], tenant=tenant, limit=5),
            "profiles": self.repository.fetch_all(BUSINESS_TABLES[1], tenant=tenant, limit=10),
            "applications": self.repository.fetch_all(BUSINESS_TABLES[2], tenant=tenant, limit=10),
            "verification_items": self.repository.fetch_all(BUSINESS_TABLES[4], tenant=tenant, limit=10),
            "award_packages": self.repository.fetch_all(BUSINESS_TABLES[9], tenant=tenant, limit=10),
            "disbursements": self.repository.fetch_all(BUSINESS_TABLES[15], tenant=tenant, limit=10),
            "exceptions": self.repository.fetch_all(BUSINESS_TABLES[17], tenant=tenant, limit=10),
            "appeals": self.repository.fetch_all(BUSINESS_TABLES[19], tenant=tenant, limit=10),
            "communications": self.repository.fetch_all(BUSINESS_TABLES[21], tenant=tenant, limit=10),
        }
        queues = {
            "verification_queue": self.repository.fetch_all(BUSINESS_TABLES[4], tenant=tenant, where="status != ?", params=("complete",), limit=10),
            "packaging_queue": self.repository.fetch_all(BUSINESS_TABLES[9], tenant=tenant, where="status IN (?, ?)", params=("packaged", "review_required"), limit=10),
            "exception_queue": self.repository.fetch_all(BUSINESS_TABLES[17], tenant=tenant, where="status != ?", params=("closed",), limit=10),
            "appeal_queue": self.repository.fetch_all(BUSINESS_TABLES[19], tenant=tenant, where="status != ?", params=("approved",), limit=10),
            "compliance_queue": self.repository.fetch_all(BUSINESS_TABLES[20], tenant=tenant, where="status != ?", params=("complete",), limit=10),
        }
        return {"ok": True, "tenant": tenant, "summary": summary, "records": records, "queues": queues, "side_effects": ()}

    def build_workbench_view(self, tenant: str = "default") -> dict[str, Any]:
        workbench = self.query_workbench(tenant)
        panels = (
            {"id": "intake_pipeline", "title": "Intake Pipeline", "kpi": workbench["summary"]["application_count"]},
            {"id": "eligibility_controls", "title": "Eligibility Controls", "kpi": workbench["summary"]["verification_open_count"]},
            {"id": "packaging_desk", "title": "Packaging Desk", "kpi": workbench["summary"]["packaged_count"]},
            {"id": "disbursement_and_returns", "title": "Disbursement and Returns", "kpi": workbench["summary"]["scheduled_disbursement_count"]},
            {"id": "appeals_and_compliance", "title": "Appeals and Compliance", "kpi": workbench["summary"]["compliance_open_count"]},
            {"id": "communications", "title": "Communications", "kpi": workbench["summary"]["communication_count"]},
        )
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "tenant": tenant,
            "route": f"/workbench/pbcs/{PBC_KEY}",
            "view": "StudentFinancialAidWorkbench",
            "detail_view": "StudentFinancialAidDetail",
            "assistant_panel": "StudentFinancialAidAssistantPanel",
            "panels": panels,
            "summary": workbench["summary"],
            "queues": workbench["queues"],
            "forms": FORM_DEFINITIONS,
            "wizards": WIZARD_DEFINITIONS,
            "controls": CONTROL_DEFINITIONS,
            "assistant_preview": self.document_instruction_plan("dependency override memo and tax transcript", "update verification and professional judgment"),
            "side_effects": (),
        }

    def document_instruction_plan(self, document: str, instruction: str) -> dict[str, Any]:
        lowered = f"{document} {instruction}".lower()
        extracted_fields = []
        if "dependency" in lowered:
            extracted_fields.append("dependency_status")
        if "tax" in lowered or "income" in lowered:
            extracted_fields.append("income_documents")
        if "sap" in lowered:
            extracted_fields.append("sap_result")
        if "appeal" in lowered:
            extracted_fields.append("appeal_reason")
        if not extracted_fields:
            extracted_fields.extend(("student_identifier", "aid_year_code"))
        candidate_tables = (
            BUSINESS_TABLES[2],
            BUSINESS_TABLES[5],
            BUSINESS_TABLES[18],
            BUSINESS_TABLES[19],
            BUSINESS_TABLES[21],
        )
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "document_digest": _digest(document),
            "instruction": instruction,
            "candidate_tables": candidate_tables,
            "extracted_fields": tuple(extracted_fields),
            "requires_human_confirmation": True,
            "crud_preview": {
                "operation": "update",
                "event_contract": "AppGen-X",
                "target_tables": candidate_tables[:3],
            },
            "safety_checks": (
                "owned_table_only",
                "human_confirmation_required",
                "no_foreign_mutation",
            ),
            "side_effects": (),
        }

    def datastore_crud_plan(self, action: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        target = table or BUSINESS_TABLES[2]
        if not str(target).startswith(f"{PBC_KEY}_"):
            return {"ok": False, "reason": "foreign_table_rejected", "table": target, "side_effects": ()}
        if target not in RUNTIME_TABLES:
            return {"ok": False, "reason": "unknown_owned_table", "table": target, "side_effects": ()}
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

    def run_advanced_assessment(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = dict(payload or {})
        summary = self._summary(payload.get("tenant", "default"))
        score = round(0.72 + min(summary["application_count"], 5) * 0.02 + min(summary["packaged_count"], 5) * 0.01, 4)
        return {
            "ok": True,
            "score": min(score, 0.99),
            "explanations": (
                "aid-year controls registered",
                "need analysis and packaging traceable",
                "assistant previews governed by owned-table boundaries",
            ),
            "payload": payload,
            "side_effects": (),
        }

    def run_operation(self, operation: str, payload: dict[str, Any]) -> dict[str, Any]:
        if operation not in DOMAIN_OPERATIONS:
            return {"ok": False, "reason": "unknown_domain_operation", "operation": operation, "side_effects": ()}
        return getattr(self, operation)(payload)


def build_models_contract() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "models": tuple(
            {
                "class_name": _class_name(spec.owned_table),
                "table": spec.owned_table,
                "fields": MODEL_FIELDS,
            }
            for spec in TABLE_SPECS
        ),
        "side_effects": (),
    }


def build_schema_contract() -> dict[str, Any]:
    tables = tuple(
        {
            "table": spec.owned_table,
            "logical_name": spec.logical_name,
            "description": spec.description,
            "fields": MODEL_FIELDS,
            "primary_key": ("id",),
            "foreign_key_table": spec.foreign_key_table,
            "owned_by": PBC_KEY,
        }
        for spec in TABLE_SPECS
    )
    return {
        "format": f"appgen.{PBC_KEY}.owned-schema-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "tables": tables,
        "migrations": (
            {
                "path": f"pbcs/{PBC_KEY}/migrations/001_initial.sql",
                "operation": "create_owned_tables",
                "tables": RUNTIME_TABLES,
                "backend_allowlist": ALLOWED_DATABASE_BACKENDS,
            },
        ),
        "models": build_models_contract()["models"],
        "database_backends": ALLOWED_DATABASE_BACKENDS,
        "datastore_backends": ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "owned_tables": RUNTIME_TABLES,
        "side_effects": (),
    }


def build_service_contract() -> dict[str, Any]:
    return {
        "format": f"appgen.{PBC_KEY}.service-contract.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "command_methods": COMMAND_METHODS,
        "query_methods": QUERY_METHODS,
        "shared_table_access": False,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
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
        "workbench_view": "StudentFinancialAidWorkbench",
        "forms": FORM_DEFINITIONS,
        "wizards": WIZARD_DEFINITIONS,
        "controls": CONTROL_DEFINITIONS,
        "advanced_panels": tuple(PBC_MANIFEST["advanced_capabilities"]),
        "action_permissions": PERMISSIONS,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def build_agent_contract() -> dict[str, Any]:
    skills = (
        "guide_user",
        "read_records",
        "plan_document_changes",
        "preview_mutation",
        "explain_need_analysis",
        "check_disbursement_readiness",
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "namespace": f"{PBC_KEY}_skills",
        "skills": tuple(
            {
                "name": f"{PBC_KEY}_{skill}",
                "scope": PBC_KEY,
                "requires_confirmation_for_mutation": skill not in {"guide_user", "read_records", "explain_need_analysis", "check_disbursement_readiness"},
                "uses_appgen_event_contract": True,
                "stream_engine_picker_visible": False,
            }
            for skill in skills
        ),
        "capabilities": (
            "document_instruction_intake",
            "governed_datastore_crud",
            "mutation_preview",
            "need_analysis_explainer",
            "disbursement_readiness_preview",
        ),
        "side_effects": (),
    }


def build_seed_plan() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "rows": (
            {"table": BUSINESS_TABLES[0], "code": "2026-2027", "status": "active"},
            {"table": BUSINESS_TABLES[22], "code": "award_packaging_policy", "status": "compiled"},
            {"table": BUSINESS_TABLES[23], "code": "workbench_limit", "status": "active"},
        ),
        "side_effects": (),
    }


def verify_owned_table_boundary(references: tuple[str, ...] | list[str] = ()) -> dict[str, Any]:
    allowed = set(RUNTIME_TABLES) | {"api_dependency", "projection_dependency", "student_projection", "enrollment_projection"}
    foreign = tuple(reference for reference in references if reference not in allowed and not str(reference).startswith(f"{PBC_KEY}_"))
    return {
        "ok": not foreign,
        "foreign_references": foreign,
        "allowed_dependency_modes": ("api", "event", "projection"),
        "shared_table_access": False,
        "side_effects": (),
    }


def dispatch_route(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    *,
    app: StudentFinancialAidSliceApp | None = None,
) -> dict[str, Any]:
    route = next((item for item in ROUTE_DEFINITIONS if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "reason": "route_not_found", "side_effects": ()}
    app = app or build_standalone_app()
    if route["operation"] == "query_workbench":
        result = app.query_workbench((payload or {}).get("tenant", "default"))
    elif route["operation"] == "document_instruction_plan":
        result = app.document_instruction_plan((payload or {}).get("document", ""), (payload or {}).get("instruction", ""))
    elif route["operation"] == "datastore_crud_plan":
        result = app.datastore_crud_plan((payload or {}).get("action", "read"), (payload or {}).get("table"), (payload or {}).get("payload"))
    else:
        result = app.run_operation(route["operation"], payload or {})
    return {"ok": result.get("ok") is True, "route": route, "result": result, "side_effects": ()}


def slice_app_smoke_test() -> dict[str, Any]:
    app = build_standalone_app()
    config = app.configure_runtime({"database_backend": "postgresql", "event_topic": APPGEN_X_TOPIC})
    year = app.setup_aid_year({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "owner": "aid-director"})
    profile = app.create_student_aid_profile({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_id": "S-100", "student_name": "Taylor Rivers", "program": "BS Nursing", "residency": "in_state"})
    application = app.intake_aid_application({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "application_id": "APP-100", "student_aid_index": 1800, "verification_selected": True, "documents": ("tax-transcript", "identity-form")})
    dependency = app.review_dependency_and_verification({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "aid_application_id": application["record"]["id"], "unresolved_count": 0, "reviewer": "aid-counselor"})
    sap = app.evaluate_sap({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "gpa": 2.8, "pace": 0.85})
    budget = app.capture_cost_of_attendance({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "tuition": 9200, "housing": 5100})
    need = app.analyze_need({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "coa_total": budget["total"], "student_aid_index": 1800, "external_resources": 500})
    package = app.package_awards({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "unmet_need": need["unmet_need"], "coa_total": budget["total"], "external_resources": 500})
    disbursement = app.schedule_disbursement({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "award_package_id": package["record"]["id"], "scheduled_amount": package["record"]["amount"], "verification_complete": True, "sap_status": sap["record"]["status"], "acceptance_received": True})
    exception = app.review_return_refund_overaward({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "aid_application_id": application["record"]["id"], "disbursed_amount": package["record"]["amount"], "earned_percent": 0.5})
    judgment = app.submit_professional_judgment({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "case_reason": "income reduction", "adjusted_field": "student_aid_index", "adjusted_value": 1200, "status": "approved"})
    appeal = app.record_appeal({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "professional_judgment_case_id": judgment["record"]["id"], "committee_decision": "approved", "conditions": "midterm SAP check"})
    compliance = app.track_compliance_obligation({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "obligation": "verification_follow_up", "owner": "compliance-officer", "due_date": "2026-10-01"})
    communication = app.log_communication({"tenant": "tenant-smoke", "aid_year_code": "2026-2027", "student_aid_profile_id": profile["record"]["id"], "template": "award_notice", "message": "Packaging complete."})
    document_plan = app.document_instruction_plan("Tax transcript and SAP appeal letter", "update verification and appeal")
    crud_plan = app.datastore_crud_plan("update", table=BUSINESS_TABLES[9], payload={"status": "packaged"})
    handled = app.receive_event({"event_type": CONSUMED_EVENTS[0], "tenant": "tenant-smoke", "idempotency_key": "evt-1"})
    duplicate = app.receive_event({"event_type": CONSUMED_EVENTS[0], "tenant": "tenant-smoke", "idempotency_key": "evt-1"})
    unknown = app.receive_event({"event_type": "UnexpectedEvent", "tenant": "tenant-smoke", "idempotency_key": "evt-2"})
    workbench = app.query_workbench("tenant-smoke")
    route = dispatch_route("GET", "/student-financial-aid-workbench", {"tenant": "tenant-smoke"}, app=app)
    return {
        "ok": all(
            (
                config["ok"],
                year["ok"],
                profile["ok"],
                application["ok"],
                dependency["ok"],
                sap["ok"],
                budget["ok"],
                need["ok"],
                package["ok"],
                disbursement["ok"],
                exception["ok"],
                judgment["ok"],
                appeal["ok"],
                compliance["ok"],
                communication["ok"],
                document_plan["ok"],
                crud_plan["ok"],
                handled["ok"],
                duplicate["duplicate"] is True,
                unknown["ok"] is False,
                workbench["summary"]["application_count"] >= 1,
                route["ok"],
            )
        ),
        "configuration": config,
        "aid_year": year,
        "profile": profile,
        "application": application,
        "dependency": dependency,
        "sap": sap,
        "budget": budget,
        "need": need,
        "package": package,
        "disbursement": disbursement,
        "exception": exception,
        "judgment": judgment,
        "appeal": appeal,
        "compliance": compliance,
        "communication": communication,
        "document_plan": document_plan,
        "crud_plan": crud_plan,
        "handled_event": handled,
        "duplicate_event": duplicate,
        "unknown_event": unknown,
        "workbench": workbench,
        "route": route,
        "side_effects": (),
    }


def pbc_source_artifact_contract() -> dict[str, Any]:
    schema = build_schema_contract()
    docs = tuple(path for path in RELEASE_ARTIFACTS if (PACKAGE_DIR / path).exists())
    missing_docs = tuple(path for path in RELEASE_ARTIFACTS if path not in docs)
    migration_sql = MIGRATION_PATH.read_text(encoding="utf-8")
    return {
        "ok": schema["ok"] and not missing_docs and f"CREATE TABLE IF NOT EXISTS {BUSINESS_TABLES[0]}" in migration_sql,
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
    boundary = verify_owned_table_boundary(RUNTIME_TABLES + ("api_dependency", "projection_dependency"))
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
    api = build_api_contract()
    models = build_models_contract()
    return {
        "ok": smoke["ok"] and api["ok"] and models["ok"],
        "pbc": PBC_KEY,
        "route_count": len(api["routes"]),
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
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "owned_tables": RUNTIME_TABLES,
        "allowed_database_backends": ALLOWED_DATABASE_BACKENDS,
        "capabilities": _dedupe(tuple(PBC_MANIFEST["advanced_capabilities"])),
        "standard_features": _dedupe(tuple(PBC_MANIFEST["standard_features"])),
        "operations": _dedupe(tuple(COMMAND_METHODS + QUERY_METHODS)),
        "smoke": smoke,
        "side_effects": (),
    }
