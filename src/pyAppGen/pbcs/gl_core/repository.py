"""Package-local repository helpers for standalone gl_core usage."""

from __future__ import annotations

from . import models
from .runtime import GL_CORE_OWNED_TABLES
from .runtime import gl_core_empty_state


PBC_KEY = "gl_core"
REPOSITORY_TABLES = (
    "gl_core_ledger_account",
    "gl_core_accounting_period",
    "gl_core_policy_rule",
    "gl_core_tenant_ledger_partition",
    "gl_core_journal_entry",
    "gl_core_journal_line",
    "gl_core_semantic_source_document",
    "gl_core_reconciliation_case",
    "gl_core_close_snapshot",
)
_IDENTITY_FIELDS = {
    "gl_core_ledger_account": "account_id",
    "gl_core_accounting_period": "period_id",
    "gl_core_policy_rule": "rule_id",
    "gl_core_tenant_ledger_partition": "partition_id",
    "gl_core_journal_entry": "journal_id",
    "gl_core_journal_line": "line_id",
    "gl_core_semantic_source_document": "document_id",
    "gl_core_reconciliation_case": "case_id",
    "gl_core_close_snapshot": "snapshot_id",
}


def _ensure_repository_state(state: dict | None) -> dict:
    next_state = dict(state or gl_core_empty_state())
    repository_tables = {
        table: tuple((next_state.get("repository_tables") or {}).get(table, ()))
        for table in REPOSITORY_TABLES
    }
    next_state["repository_tables"] = repository_tables
    return next_state


def _sql_literal(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def gl_core_repository_manifest() -> dict:
    """Return standalone repository coverage for database-backed GL forms."""
    return {
        "ok": all(table in GL_CORE_OWNED_TABLES for table in REPOSITORY_TABLES),
        "pbc": PBC_KEY,
        "tables": REPOSITORY_TABLES,
        "identity_fields": dict(_IDENTITY_FIELDS),
        "write_modes": ("insert", "upsert", "append_only"),
        "side_effects": (),
    }


class GlCoreRepository:
    """Repository facade that records package-local rows plus SQL write plans."""

    def __init__(self, state: dict | None = None):
        self.state = _ensure_repository_state(state)

    def database_write_plan(self, table: str, rows: tuple[dict, ...]) -> dict:
        """Build a deterministic SQL insert plan without touching a database."""
        if table not in REPOSITORY_TABLES:
            return {"ok": False, "reason": "unknown_table", "table": table, "side_effects": ()}
        columns = tuple(sorted({key for row in rows for key in row}))
        values_sql = tuple(
            "(" + ", ".join(_sql_literal(row.get(column)) for column in columns) + ")"
            for row in rows
        )
        sql = f"INSERT INTO {table} (" + ", ".join(columns) + ") VALUES " + ", ".join(values_sql)
        return {
            "ok": True,
            "table": table,
            "columns": columns,
            "row_count": len(rows),
            "sql": sql,
            "side_effects": (),
        }

    def _write_rows(self, table: str, rows: tuple[dict, ...]) -> dict:
        if table not in REPOSITORY_TABLES:
            return {"ok": False, "reason": "unknown_table", "table": table, "side_effects": ()}
        current = tuple(self.state["repository_tables"].get(table, ()))
        prepared = []
        identity_field = _IDENTITY_FIELDS[table]
        for offset, row in enumerate(rows, start=1):
            payload = dict(row)
            payload.setdefault("id", len(current) + offset)
            payload.setdefault("tenant", "tenant_demo")
            if not payload.get(identity_field):
                return {
                    "ok": False,
                    "reason": "missing_identity_field",
                    "table": table,
                    "identity_field": identity_field,
                    "side_effects": (),
                }
            model_payload = models.instantiate_model(table, payload)
            if not model_payload["ok"]:
                return {"ok": False, "reason": "invalid_model", "table": table, "side_effects": ()}
            prepared.append(payload)
        next_tables = dict(self.state["repository_tables"])
        next_tables[table] = current + tuple(prepared)
        self.state = {**self.state, "repository_tables": next_tables}
        return {
            "ok": True,
            "table": table,
            "rows": tuple(prepared),
            "row_count": len(prepared),
            "write_plan": self.database_write_plan(table, tuple(prepared)),
            "state": self.state,
            "side_effects": (),
        }

    def save_ledger_account(self, account: dict) -> dict:
        return self._write_rows("gl_core_ledger_account", (account,))

    def save_accounting_period(self, period: dict) -> dict:
        return self._write_rows("gl_core_accounting_period", (period,))

    def save_source_document(self, document: dict) -> dict:
        return self._write_rows("gl_core_semantic_source_document", (document,))

    def save_reconciliation_case(self, case: dict) -> dict:
        return self._write_rows("gl_core_reconciliation_case", (case,))

    def save_close_snapshot(self, snapshot: dict) -> dict:
        return self._write_rows("gl_core_close_snapshot", (snapshot,))

    def save_journal_draft(self, journal: dict, lines: tuple[dict, ...]) -> dict:
        journal_payload = {
            "tenant": journal.get("tenant", "tenant_demo"),
            "journal_id": journal.get("journal_id"),
            "period_id": journal.get("period_id"),
            "status": journal.get("status", "draft"),
            "source_document_hash": journal.get("source_document_hash", "document-hash"),
            "approval_state": journal.get("approval_state", "pending"),
        }
        header = self._write_rows("gl_core_journal_entry", (journal_payload,))
        if not header["ok"]:
            return header
        line_rows = []
        for position, line in enumerate(lines, start=1):
            line_rows.append(
                {
                    "tenant": journal_payload["tenant"],
                    "journal_id": journal_payload["journal_id"],
                    "line_id": line.get("line_id", f"{journal_payload['journal_id']}-line-{position}"),
                    "account_id": line.get("account_id"),
                    "debit": line.get("debit", 0),
                    "credit": line.get("credit", 0),
                    "currency": line.get("currency", "USD"),
                    "dimensions": line.get("dimensions", {}),
                }
            )
        detail = self._write_rows("gl_core_journal_line", tuple(line_rows))
        return {
            "ok": header["ok"] and detail["ok"],
            "journal_entry": header,
            "journal_lines": detail,
            "state": self.state,
            "write_plans": (header.get("write_plan"), detail.get("write_plan")),
            "side_effects": (),
        }

    def list_records(self, table: str, *, tenant: str | None = None) -> dict:
        rows = tuple(self.state["repository_tables"].get(table, ()))
        if tenant is not None:
            rows = tuple(row for row in rows if row.get("tenant") == tenant)
        return {
            "ok": table in REPOSITORY_TABLES,
            "table": table,
            "rows": rows,
            "row_count": len(rows),
            "side_effects": (),
        }

    def seed_defaults(self, *, tenant: str = "tenant_demo") -> dict:
        from .seed_data import SEED_DATA

        results = []
        for item in SEED_DATA:
            adjusted_rows = tuple({**row, "tenant": tenant} for row in item.get("rows", ()))
            results.append(self._write_rows(item["table"], adjusted_rows))
        return {
            "ok": all(result["ok"] for result in results),
            "results": tuple(results),
            "state": self.state,
            "side_effects": (),
        }


def smoke_test() -> dict:
    """Exercise repository manifests, SQL planning, and draft persistence."""
    repository = GlCoreRepository()
    seeded = repository.seed_defaults(tenant="tenant_smoke")
    journal = repository.save_journal_draft(
        {
            "tenant": "tenant_smoke",
            "journal_id": "je-smoke-001",
            "period_id": "2026-05",
            "source_document_hash": "doc-smoke-001",
        },
        (
            {"account_id": "cash_main", "debit": 100.0, "credit": 0.0, "dimensions": {"entity": "hq"}},
            {"account_id": "product_revenue", "debit": 0.0, "credit": 100.0, "dimensions": {"entity": "hq"}},
        ),
    )
    listed = repository.list_records("gl_core_journal_line", tenant="tenant_smoke")
    return {
        "ok": gl_core_repository_manifest()["ok"] and seeded["ok"] and journal["ok"] and listed["row_count"] == 2,
        "manifest": gl_core_repository_manifest(),
        "seeded": seeded,
        "journal": journal,
        "listed": listed,
        "side_effects": (),
    }
