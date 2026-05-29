"""SQLite-backed repository for the standalone treasury_cash PBC app."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
MIGRATION_PATH = PACKAGE_DIR / "migrations" / "001_initial.sql"

TREASURY_CASH_REPOSITORY_TABLES = (
    "treasury_cash_bank_account",
    "treasury_cash_bank_account_signatory",
    "treasury_cash_bank_topology",
    "treasury_cash_balance",
    "treasury_cash_statement",
    "treasury_cash_statement_line",
    "treasury_cash_cash_position",
    "treasury_cash_cash_forecast",
    "treasury_cash_liquidity_plan",
    "treasury_cash_rule",
    "treasury_cash_parameter",
    "treasury_cash_control_assertion",
    "treasury_cash_appgen_outbox_event",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_dumps(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _json_loads(value):
    if value in (None, ""):
        return None
    return json.loads(value)


def repository_manifest() -> dict:
    """Return repository metadata for release evidence and UI contracts."""
    return {
        "ok": True,
        "module": "repository.py",
        "class": "TreasuryCashRepository",
        "database": "sqlite",
        "migration": str(MIGRATION_PATH.relative_to(PACKAGE_DIR)),
        "owned_tables": TREASURY_CASH_REPOSITORY_TABLES,
        "shared_table_access": False,
        "side_effects": (),
    }


class TreasuryCashRepository:
    """Persist treasury forms and workflow outcomes in a standalone SQLite store."""

    def __init__(self, database_path: str = ":memory:"):
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")

    def close(self) -> None:
        self.connection.close()

    def apply_migrations(self) -> tuple[str, ...]:
        sql = MIGRATION_PATH.read_text()
        statements = [line for line in sql.splitlines() if not line.startswith("CREATE SCHEMA")]
        self.connection.executescript("\n".join(statements))
        for table in TREASURY_CASH_REPOSITORY_TABLES:
            self._add_column_if_missing(table, "tenant TEXT")
            self._add_column_if_missing(table, "external_key TEXT")
            self._add_column_if_missing(table, "payload TEXT")
        self.connection.commit()
        return (MIGRATION_PATH.name,)

    def seed_from_plan(self, plan: dict) -> dict:
        inserted = []
        for item in plan.get("rows", ()):
            table = item["table"]
            for row in item.get("rows", ()):
                inserted.append(self._persist_payload(table, row["external_key"], row.get("tenant", "seed"), row.get("status", "active"), row.get("payload", {})))
        self.connection.commit()
        return {
            "ok": bool(inserted),
            "tables": tuple(dict.fromkeys(record["table"] for record in inserted)),
            "inserted": tuple(inserted),
            "side_effects": (),
        }

    def save_bank_account(self, account: dict) -> dict:
        record = self._persist_payload(
            "treasury_cash_bank_account",
            account["account_id"],
            account["tenant"],
            account.get("status", "active"),
            account,
        )
        account_row_id = record["id"]
        signatories = tuple(account.get("signatories", ()))
        signatory_records = tuple(
            self._persist_payload(
                "treasury_cash_bank_account_signatory",
                f"{account['account_id']}:{principal}",
                account["tenant"],
                "active",
                {
                    "account_id": account["account_id"],
                    "principal": principal,
                    "role": "signatory",
                    "approval_limit": account.get("approval_limit", "policy_bound"),
                },
                bank_account_id=account_row_id,
            )
            for principal in signatories
        )
        topology = self._persist_payload(
            "treasury_cash_bank_topology",
            f"topology:{account['bank_id']}",
            account["tenant"],
            "active",
            {
                "bank_id": account["bank_id"],
                "accounts": (account["account_id"],),
                "signatories": signatories,
                "risk_score": account.get("risk_score"),
            },
            bank_account_id=account_row_id,
        )
        self.connection.commit()
        return {
            "ok": True,
            "bank_account": record,
            "signatories": signatory_records,
            "topology": topology,
            "side_effects": (),
        }

    def save_balance(self, balance: dict) -> dict:
        account_row_id = self._required_account_row_id(balance["account_id"], balance["tenant"])
        record = self._persist_payload(
            "treasury_cash_balance",
            balance["balance_id"],
            balance["tenant"],
            balance.get("status", "captured"),
            balance,
            bank_account_id=account_row_id,
        )
        self.connection.commit()
        return {"ok": True, "balance": record, "side_effects": ()}

    def save_statement(self, statement: dict) -> dict:
        account_row_id = self._required_account_row_id(statement["account_id"], statement["tenant"])
        header = self._persist_payload(
            "treasury_cash_statement",
            statement["statement_id"],
            statement["tenant"],
            statement.get("status", "ingested"),
            statement,
            bank_account_id=account_row_id,
        )
        lines = tuple(
            self._persist_payload(
                "treasury_cash_statement_line",
                f"{statement['statement_id']}:{line['line_id']}",
                statement["tenant"],
                "ingested",
                {**line, "statement_id": statement["statement_id"]},
                bank_account_id=account_row_id,
            )
            for line in statement.get("lines", ())
        )
        self.connection.commit()
        return {"ok": True, "statement": header, "lines": lines, "side_effects": ()}

    def save_cash_position(self, position: dict, *, account_id: str) -> dict:
        account_row_id = self._required_account_row_id(account_id, position["tenant"])
        record = self._persist_payload(
            "treasury_cash_cash_position",
            f"position:{position['tenant']}:{position['value_date']}",
            position["tenant"],
            "calculated",
            position,
            bank_account_id=account_row_id,
        )
        self.connection.commit()
        return {"ok": True, "cash_position": record, "side_effects": ()}

    def save_forecast(self, forecast: dict, *, account_id: str) -> dict:
        account_row_id = self._required_account_row_id(account_id, forecast["tenant"])
        record = self._persist_payload(
            "treasury_cash_cash_forecast",
            f"forecast:{forecast['tenant']}:{len(forecast.get('forecast', ())) or 1}",
            forecast["tenant"],
            "generated",
            forecast,
            bank_account_id=account_row_id,
        )
        self.connection.commit()
        return {"ok": True, "cash_forecast": record, "side_effects": ()}

    def save_liquidity_plan(self, plan: dict, *, account_id: str) -> dict:
        account_row_id = self._required_account_row_id(account_id, plan["tenant"])
        record = self._persist_payload(
            "treasury_cash_liquidity_plan",
            f"plan:{plan['tenant']}:{plan['selected_source']}",
            plan["tenant"],
            "recommended",
            plan,
            bank_account_id=account_row_id,
        )
        self.connection.commit()
        return {"ok": True, "liquidity_plan": record, "side_effects": ()}

    def save_control_assertion(self, control: dict, *, tenant: str, account_id: str) -> dict:
        account_row_id = self._required_account_row_id(account_id, tenant)
        record = self._persist_payload(
            "treasury_cash_control_assertion",
            f"control:{tenant}:{account_id}",
            tenant,
            "passed" if control.get("ok") else "failed",
            control,
            bank_account_id=account_row_id,
        )
        self.connection.commit()
        return {"ok": True, "control_assertion": record, "side_effects": ()}

    def save_outbox_events(self, outbox_events: tuple[dict, ...] | list[dict], *, tenant: str) -> dict:
        stored = tuple(
            self._persist_payload(
                "treasury_cash_appgen_outbox_event",
                event.get("idempotency_key") or f"evt:{position}",
                tenant,
                "pending",
                event,
            )
            for position, event in enumerate(outbox_events, start=1)
        )
        self.connection.commit()
        return {"ok": True, "events": stored, "side_effects": ()}

    def list_records(self, table: str, *, tenant: str | None = None, limit: int = 50) -> tuple[dict, ...]:
        columns = self._table_columns(table)
        selected = [column for column in ("id", "tenant", "external_key", "code", "status", "version", "payload", "event_id", "event_type", "attempts") if column in columns]
        query = f"SELECT {', '.join(selected)} FROM {table}"
        params: list[object] = []
        if tenant is not None and "tenant" in columns:
            query += " WHERE tenant = ?"
            params.append(tenant)
        query += " ORDER BY id ASC LIMIT ?"
        params.append(limit)
        rows = self.connection.execute(query, tuple(params)).fetchall()
        return tuple(
            {
                "id": row["id"],
                "tenant": row["tenant"] if "tenant" in row.keys() else None,
                "external_key": row["external_key"] if "external_key" in row.keys() else row["event_id"],
                "code": row["code"] if "code" in row.keys() else row["event_type"],
                "status": row["status"],
                "version": row["version"] if "version" in row.keys() else 1,
                "payload": _json_loads(row["payload"]) or {},
            }
            for row in rows
        )

    def workbench_summary(self, *, tenant: str) -> dict:
        accounts = self.list_records("treasury_cash_bank_account", tenant=tenant)
        balances = self.list_records("treasury_cash_balance", tenant=tenant)
        statements = self.list_records("treasury_cash_statement", tenant=tenant)
        positions = self.list_records("treasury_cash_cash_position", tenant=tenant)
        forecasts = self.list_records("treasury_cash_cash_forecast", tenant=tenant)
        plans = self.list_records("treasury_cash_liquidity_plan", tenant=tenant)
        controls = self.list_records("treasury_cash_control_assertion", tenant=tenant)
        outbox = self.list_records("treasury_cash_appgen_outbox_event", tenant=tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "counts": {
                "bank_accounts": len(accounts),
                "balances": len(balances),
                "statements": len(statements),
                "cash_positions": len(positions),
                "cash_forecasts": len(forecasts),
                "liquidity_plans": len(plans),
                "control_assertions": len(controls),
                "outbox_events": len(outbox),
            },
            "bank_accounts": accounts,
            "liquidity_plans": plans,
            "controls": controls,
            "shared_table_access": False,
            "side_effects": (),
        }

    def database_manifest(self) -> dict:
        manifest = repository_manifest()
        return {
            **manifest,
            "database_path": self.database_path,
        }

    def _required_account_row_id(self, account_id: str, tenant: str) -> int:
        row = self.connection.execute(
            "SELECT id FROM treasury_cash_bank_account WHERE external_key = ? AND tenant = ?",
            (account_id, tenant),
        ).fetchone()
        if row is None:
            raise KeyError(f"Unknown treasury bank account {account_id!r} for tenant {tenant!r}")
        return int(row["id"])

    def _persist_payload(
        self,
        table: str,
        external_key: str,
        tenant: str,
        status: str,
        payload: dict,
        *,
        bank_account_id: int | None = None,
    ) -> dict:
        columns = self._table_columns(table)
        select_columns = ['id']
        if 'version' in columns:
            select_columns.append('version')
        existing = self.connection.execute(
            f"SELECT {', '.join(select_columns)} FROM {table} WHERE external_key = ?",
            (external_key,),
        ).fetchone()
        row_id = int(existing['id']) if existing else self._next_id(table)
        version = int(existing['version']) + 1 if existing and 'version' in existing.keys() else 1
        created_at = _utc_now()
        values = {
            'id': row_id,
            'status': status,
            'tenant': tenant,
            'external_key': external_key,
            'payload': _json_dumps(payload),
            'created_at': created_at,
            'processed_at': None,
            'event_id': external_key,
            'event_type': payload.get('event_type', status),
            'attempts': int(payload.get('attempts', 0)),
        }
        if 'code' in columns:
            values['code'] = external_key
        if 'version' in columns:
            values['version'] = version
        if 'updated_at' in columns:
            values['updated_at'] = created_at
        if 'bank_account_id' in columns:
            values['bank_account_id'] = bank_account_id if bank_account_id is not None else row_id
        insert_columns = tuple(column for column in values if column in columns)
        placeholders = ', '.join('?' for _ in insert_columns)
        update_columns = tuple(column for column in insert_columns if column != 'id')
        update_clause = ', '.join(f"{column} = excluded.{column}" for column in update_columns)
        self.connection.execute(
            f"INSERT INTO {table} ({', '.join(insert_columns)}) VALUES ({placeholders}) "
            f"ON CONFLICT(id) DO UPDATE SET {update_clause}",
            tuple(values[column] for column in insert_columns),
        )
        return {
            'table': table,
            'id': row_id,
            'tenant': tenant,
            'external_key': external_key,
            'status': status,
            'payload': payload,
        }

    def _table_columns(self, table: str) -> set[str]:
        rows = self.connection.execute(f"PRAGMA table_info({table})").fetchall()
        return {row[1] for row in rows}

    def _add_column_if_missing(self, table: str, specification: str) -> None:
        column_name = specification.split()[0]
        if column_name not in self._table_columns(table):
            self.connection.execute(f"ALTER TABLE {table} ADD COLUMN {specification}")

    def _next_id(self, table: str) -> int:
        row = self.connection.execute(f"SELECT COALESCE(MAX(id), 0) AS current_max FROM {table}").fetchone()
        return int(row["current_max"]) + 1
