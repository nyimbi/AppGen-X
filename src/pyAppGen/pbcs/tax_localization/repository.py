"""SQLite-backed repository contract for the tax_localization standalone PBC."""

from __future__ import annotations

import json
import sqlite3
import tempfile
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent


def _json_dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _json_loads(value: str | None):
    if value in (None, ""):
        return None
    return json.loads(value)


class TaxLocalizationRepository:
    """Persist the package-owned tax slice without touching shared tables."""

    def __init__(self, database_path: str = ":memory:"):
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def apply_schema(self) -> tuple[str, ...]:
        statements = (
            """
            CREATE TABLE IF NOT EXISTS tax_localization_tax_jurisdiction (
                jurisdiction_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                country TEXT NOT NULL,
                region TEXT NOT NULL,
                locality TEXT NOT NULL,
                currency TEXT NOT NULL,
                status TEXT NOT NULL,
                risk_score REAL NOT NULL,
                payload TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tax_localization_tax_rule (
                rule_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                jurisdiction_id TEXT NOT NULL,
                tax_type TEXT NOT NULL,
                product_class TEXT NOT NULL,
                rate REAL NOT NULL,
                status TEXT NOT NULL,
                compiled_hash TEXT,
                payload TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tax_localization_tax_calculation (
                calculation_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                jurisdiction_id TEXT NOT NULL,
                customer_id TEXT NOT NULL,
                order_id TEXT NOT NULL,
                tax_total REAL NOT NULL,
                taxable_total REAL NOT NULL,
                status TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tax_localization_invoice_tax_record (
                invoice_id TEXT PRIMARY KEY,
                calculation_id TEXT NOT NULL,
                tenant TEXT NOT NULL,
                tax_total REAL NOT NULL,
                status TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tax_localization_tax_filing (
                filing_id TEXT PRIMARY KEY,
                tenant TEXT NOT NULL,
                jurisdiction_id TEXT NOT NULL,
                period TEXT NOT NULL,
                liability REAL NOT NULL,
                status TEXT NOT NULL,
                approved_by TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS tax_localization_appgen_outbox_event (
                idempotency_key TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                tenant TEXT NOT NULL,
                payload TEXT NOT NULL,
                status TEXT NOT NULL
            )
            """,
        )
        for statement in statements:
            self.connection.execute(statement)
        self.connection.commit()
        return (
            "tax_localization_tax_jurisdiction",
            "tax_localization_tax_rule",
            "tax_localization_tax_calculation",
            "tax_localization_invoice_tax_record",
            "tax_localization_tax_filing",
            "tax_localization_appgen_outbox_event",
        )

    def _upsert(self, table: str, identifier_field: str, payload: dict) -> dict:
        encoded = _json_dumps(payload)
        if table == "tax_localization_tax_jurisdiction":
            self.connection.execute(
                """
                INSERT OR REPLACE INTO tax_localization_tax_jurisdiction (
                    jurisdiction_id, tenant, country, region, locality, currency, status, risk_score, payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["jurisdiction_id"],
                    payload["tenant"],
                    payload["country"],
                    payload["region"],
                    payload["locality"],
                    payload["currency"],
                    payload["status"],
                    float(payload.get("risk_score", 0.0)),
                    encoded,
                ),
            )
        elif table == "tax_localization_tax_rule":
            self.connection.execute(
                """
                INSERT OR REPLACE INTO tax_localization_tax_rule (
                    rule_id, tenant, jurisdiction_id, tax_type, product_class, rate, status, compiled_hash, payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["rule_id"],
                    payload["tenant"],
                    payload["jurisdiction_id"],
                    payload["tax_type"],
                    payload["product_class"],
                    float(payload["rate"]),
                    payload["status"],
                    payload.get("compiled_hash"),
                    encoded,
                ),
            )
        elif table == "tax_localization_tax_calculation":
            self.connection.execute(
                """
                INSERT OR REPLACE INTO tax_localization_tax_calculation (
                    calculation_id, tenant, jurisdiction_id, customer_id, order_id, tax_total, taxable_total, status, payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["calculation_id"],
                    payload["tenant"],
                    payload["jurisdiction_id"],
                    payload["customer_id"],
                    payload["order_id"],
                    float(payload["tax_total"]),
                    float(payload["taxable_total"]),
                    payload["status"],
                    encoded,
                ),
            )
        elif table == "tax_localization_invoice_tax_record":
            self.connection.execute(
                """
                INSERT OR REPLACE INTO tax_localization_invoice_tax_record (
                    invoice_id, calculation_id, tenant, tax_total, status, payload
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["invoice_id"],
                    payload["calculation_id"],
                    payload["tenant"],
                    float(payload["tax_total"]),
                    payload["status"],
                    encoded,
                ),
            )
        elif table == "tax_localization_tax_filing":
            self.connection.execute(
                """
                INSERT OR REPLACE INTO tax_localization_tax_filing (
                    filing_id, tenant, jurisdiction_id, period, liability, status, approved_by, payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["filing_id"],
                    payload["tenant"],
                    payload["jurisdiction_id"],
                    payload["period"],
                    float(payload["liability"]),
                    payload["status"],
                    payload["approved_by"],
                    encoded,
                ),
            )
        else:
            raise KeyError(table)
        self.connection.commit()
        return payload

    def record_outbox_event(self, event: dict) -> dict:
        payload = dict(event.get("payload", {}))
        self.connection.execute(
            """
            INSERT OR REPLACE INTO tax_localization_appgen_outbox_event (
                idempotency_key, event_type, tenant, payload, status
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                event["idempotency_key"],
                event["event_type"],
                payload.get("tenant", event.get("tenant", "tenant_alpha")),
                _json_dumps(payload),
                event.get("status", "pending"),
            ),
        )
        self.connection.commit()
        return event

    def save_jurisdiction(self, jurisdiction: dict) -> dict:
        return self._upsert("tax_localization_tax_jurisdiction", "jurisdiction_id", jurisdiction)

    def save_rule(self, rule: dict) -> dict:
        return self._upsert("tax_localization_tax_rule", "rule_id", rule)

    def save_calculation(self, calculation: dict) -> dict:
        return self._upsert("tax_localization_tax_calculation", "calculation_id", calculation)

    def save_invoice_tax_record(self, record: dict) -> dict:
        return self._upsert("tax_localization_invoice_tax_record", "invoice_id", record)

    def save_filing(self, filing: dict) -> dict:
        return self._upsert("tax_localization_tax_filing", "filing_id", filing)

    def save_runtime_snapshot(self, state: dict) -> dict:
        for jurisdiction in state.get("jurisdictions", {}).values():
            self.save_jurisdiction(jurisdiction)
        for rule in state.get("rules", {}).values():
            self.save_rule(rule)
        for calculation in state.get("calculations", {}).values():
            self.save_calculation(calculation)
        for record in state.get("invoice_tax", {}).values():
            self.save_invoice_tax_record(record)
        for filing in state.get("filings", {}).values():
            self.save_filing(filing)
        for event in state.get("outbox", ()):
            self.record_outbox_event(event)
        return {
            "ok": True,
            "tables": self.database_manifest()["owned_tables"],
            "counts": {
                "jurisdictions": len(self.list_jurisdictions()),
                "calculations": len(self.list_calculations()),
                "filings": len(self.list_filings()),
                "outbox": len(self.list_outbox_events()),
            },
            "side_effects": (),
        }

    def _list_payloads(self, table: str, limit: int = 50) -> tuple[dict, ...]:
        rows = self.connection.execute(
            f"SELECT payload FROM {table} ORDER BY rowid ASC LIMIT ?",
            (limit,),
        ).fetchall()
        return tuple((_json_loads(row["payload"]) or {}) for row in rows)

    def list_jurisdictions(self, limit: int = 50) -> tuple[dict, ...]:
        return self._list_payloads("tax_localization_tax_jurisdiction", limit)

    def list_calculations(self, limit: int = 50) -> tuple[dict, ...]:
        return self._list_payloads("tax_localization_tax_calculation", limit)

    def list_filings(self, limit: int = 50) -> tuple[dict, ...]:
        return self._list_payloads("tax_localization_tax_filing", limit)

    def list_outbox_events(self, limit: int = 50) -> tuple[dict, ...]:
        rows = self.connection.execute(
            """
            SELECT idempotency_key, event_type, tenant, payload, status
            FROM tax_localization_appgen_outbox_event
            ORDER BY rowid ASC LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return tuple(
            {
                "idempotency_key": row["idempotency_key"],
                "event_type": row["event_type"],
                "tenant": row["tenant"],
                "payload": _json_loads(row["payload"]) or {},
                "status": row["status"],
            }
            for row in rows
        )

    def database_manifest(self) -> dict:
        return {
            "ok": True,
            "pbc": "tax_localization",
            "database_path": self.database_path,
            "local_repository_backend": "sqlite",
            "owned_tables": (
                "tax_localization_tax_jurisdiction",
                "tax_localization_tax_rule",
                "tax_localization_tax_calculation",
                "tax_localization_invoice_tax_record",
                "tax_localization_tax_filing",
                "tax_localization_appgen_outbox_event",
            ),
            "shared_table_access": False,
            "side_effects": (),
        }


def smoke_test() -> dict:
    from .runtime import tax_localization_calculate_tax_quote
    from .runtime import tax_localization_configure_runtime
    from .runtime import tax_localization_empty_state
    from .runtime import tax_localization_prepare_tax_filing
    from .runtime import tax_localization_record_invoice_tax
    from .runtime import tax_localization_register_jurisdiction
    from .runtime import tax_localization_register_tax_rule

    handle = tempfile.NamedTemporaryFile(prefix="tax_localization_", suffix=".sqlite3", delete=False)
    handle.close()
    repo = TaxLocalizationRepository(handle.name)
    try:
        repo.apply_schema()
        state = tax_localization_empty_state()
        state = tax_localization_configure_runtime(
            state,
            {
                "database_backend": "postgresql",
                "event_topic": "appgen.tax.events",
                "retry_limit": 3,
                "default_currency": "USD",
                "default_timezone": "UTC",
                "authority_channels": ("authority_api",),
            },
        )["state"]
        state = tax_localization_register_jurisdiction(
            state,
            {
                "jurisdiction_id": "us_ny_new_york",
                "tenant": "tenant_alpha",
                "country": "US",
                "region": "NY",
                "locality": "New York",
                "currency": "USD",
                "authority_channel": "authority_api",
                "filing_frequency": "monthly",
                "risk_score": 0.08,
            },
        )["state"]
        state = tax_localization_register_tax_rule(
            state,
            {
                "rule_id": "rule_general_goods",
                "tenant": "tenant_alpha",
                "jurisdiction_id": "us_ny_new_york",
                "tax_type": "sales_tax",
                "product_class": "general_goods",
                "rate": 0.08875,
                "effective_from": "2026-01-01",
                "effective_to": "2026-12-31",
                "version": 1,
                "status": "active",
                "approval": {"approved_by": "tax_controller", "approved_at": "2026-05-29"},
            },
        )["state"]
        quote = tax_localization_calculate_tax_quote(
            state,
            {
                "quote_id": "quote_repo_001",
                "tenant": "tenant_alpha",
                "jurisdiction_id": "us_ny_new_york",
                "customer_id": "cust_1",
                "order_id": "order_1",
                "lines": (
                    {
                        "line_id": "line_1",
                        "product_id": "sku_1",
                        "product_class": "general_goods",
                        "amount": 125.0,
                        "quantity": 2,
                    },
                ),
            },
        )
        state = quote["state"]
        state = tax_localization_record_invoice_tax(state, "invoice_repo_001", "quote_repo_001")["state"]
        state = tax_localization_prepare_tax_filing(
            state,
            filing_id="filing_repo_001",
            jurisdiction_id="us_ny_new_york",
            period="2026-05",
            approved_by="tax_controller",
        )["state"]
        persisted = repo.save_runtime_snapshot(state)
        manifest = repo.database_manifest()
        return {
            "ok": persisted["ok"] and manifest["ok"] and len(repo.list_jurisdictions()) == 1 and len(repo.list_outbox_events()) >= 3,
            "manifest": manifest,
            "persisted": persisted,
            "jurisdictions": repo.list_jurisdictions(),
            "calculations": repo.list_calculations(),
            "filings": repo.list_filings(),
            "outbox": repo.list_outbox_events(),
            "side_effects": (),
        }
    finally:
        repo.close()
        Path(handle.name).unlink(missing_ok=True)
