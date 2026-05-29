"""Database-backed repository for the energy_trading_risk one-PBC app."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone
import json
from pathlib import Path
import sqlite3

PACKAGE_DIR = Path(__file__).resolve().parent
MIGRATIONS_DIR = PACKAGE_DIR / "migrations"



def _json_dumps(value) -> str:
    return json.dumps(value, sort_keys=True)



def _json_loads(value):
    if value in (None, ""):
        return None
    return json.loads(value)



def _record_timestamp(record: dict) -> str:
    payload = dict(record.get("payload", {}))
    return (
        payload.get("submitted_at")
        or payload.get("as_of")
        or payload.get("effective_from")
        or payload.get("settled_at")
        or datetime.now(timezone.utc).isoformat()
    )


class EnergyTradingRiskRepository:
    """Applies owned migrations and persists the standalone energy risk slice."""

    def __init__(self, database_path: str = ":memory:"):
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def apply_migrations(self) -> tuple[str, ...]:
        applied = []
        for migration_path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            self.connection.executescript(migration_path.read_text())
            applied.append(migration_path.name)
        self.connection.commit()
        return tuple(applied)

    def _save_record(self, table: str, record: dict) -> dict:
        stored_payload = dict(record)
        timestamp = _record_timestamp(record)
        self.connection.execute(
            f"""
            INSERT OR REPLACE INTO {table} (
                id,
                tenant,
                code,
                status,
                version,
                payload,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["id"],
                record.get("tenant", "default"),
                stored_payload.get("payload", {}).get("code", record["id"]),
                record.get("status", "active"),
                int(record.get("version", 1)),
                _json_dumps(stored_payload),
                timestamp,
                timestamp,
            ),
        )
        self.connection.commit()
        return record

    def _save_events(self, tenant: str, events=(), occurred_at: str | None = None) -> None:
        timestamp = occurred_at or datetime.now(timezone.utc).isoformat()
        for index, event in enumerate(events, start=1):
            payload = dict(event.get("payload", {}))
            event_id = event.get("idempotency_key", f"{payload.get('id', 'event')}-{index}")
            self.connection.execute(
                """
                INSERT OR REPLACE INTO energy_trading_risk_appgen_outbox_event (
                    id, tenant, code, status, version, payload, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    tenant,
                    event.get("event_type"),
                    "pending",
                    1,
                    _json_dumps(
                        {
                            "event_type": event.get("event_type"),
                            "topic": event.get("topic"),
                            "payload": payload,
                            "idempotency_key": event.get("idempotency_key"),
                        }
                    ),
                    timestamp,
                    timestamp,
                ),
            )
        self.connection.commit()

    def _list_records(self, table: str, tenant: str | None = None, status: str | None = None, limit: int = 100) -> tuple[dict, ...]:
        query = f"""
            SELECT id, tenant, code, status, version, payload
            FROM {table}
            WHERE 1 = 1
        """
        params = []
        if tenant:
            query += " AND tenant = ?"
            params.append(tenant)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY created_at ASC, id ASC LIMIT ?"
        params.append(limit)
        rows = self.connection.execute(query, params).fetchall()
        records = []
        for row in rows:
            payload = _json_loads(row["payload"]) or {}
            if isinstance(payload, dict):
                payload.setdefault("id", row["id"])
                payload.setdefault("tenant", row["tenant"])
                payload.setdefault("status", row["status"])
                payload.setdefault("version", row["version"])
                records.append(payload)
            else:
                records.append(
                    {
                        "id": row["id"],
                        "tenant": row["tenant"],
                        "status": row["status"],
                        "version": row["version"],
                        "payload": {},
                    }
                )
        return tuple(records)

    def save_energy_contract(self, record: dict, events=()) -> dict:
        saved = self._save_record("energy_trading_risk_energy_contract", record)
        self._save_events(saved.get("tenant", "default"), events, _record_timestamp(saved))
        return saved

    def save_trade_position(self, record: dict, events=()) -> dict:
        saved = self._save_record("energy_trading_risk_trade_position", record)
        self._save_events(saved.get("tenant", "default"), events, _record_timestamp(saved))
        return saved

    def save_nomination(self, record: dict, events=()) -> dict:
        saved = self._save_record("energy_trading_risk_nomination", record)
        self._save_events(saved.get("tenant", "default"), events, _record_timestamp(saved))
        return saved

    def save_schedule(self, record: dict, events=()) -> dict:
        saved = self._save_record("energy_trading_risk_schedule", record)
        self._save_events(saved.get("tenant", "default"), events, _record_timestamp(saved))
        return saved

    def save_settlement(self, record: dict, events=()) -> dict:
        saved = self._save_record("energy_trading_risk_settlement", record)
        self._save_events(saved.get("tenant", "default"), events, _record_timestamp(saved))
        return saved

    def save_market_price_curve(self, record: dict, events=()) -> dict:
        saved = self._save_record("energy_trading_risk_market_price_curve", record)
        self._save_events(saved.get("tenant", "default"), events, _record_timestamp(saved))
        return saved

    def save_exposure_limit(self, record: dict, events=()) -> dict:
        saved = self._save_record("energy_trading_risk_exposure_limit", record)
        self._save_events(saved.get("tenant", "default"), events, _record_timestamp(saved))
        return saved

    def list_energy_contracts(self, tenant: str | None = None, status: str | None = None, limit: int = 100) -> tuple[dict, ...]:
        return self._list_records("energy_trading_risk_energy_contract", tenant, status, limit)

    def list_trade_positions(self, tenant: str | None = None, status: str | None = None, limit: int = 100) -> tuple[dict, ...]:
        return self._list_records("energy_trading_risk_trade_position", tenant, status, limit)

    def list_nominations(self, tenant: str | None = None, status: str | None = None, limit: int = 100) -> tuple[dict, ...]:
        return self._list_records("energy_trading_risk_nomination", tenant, status, limit)

    def list_schedules(self, tenant: str | None = None, status: str | None = None, limit: int = 100) -> tuple[dict, ...]:
        return self._list_records("energy_trading_risk_schedule", tenant, status, limit)

    def list_settlements(self, tenant: str | None = None, status: str | None = None, limit: int = 100) -> tuple[dict, ...]:
        return self._list_records("energy_trading_risk_settlement", tenant, status, limit)

    def list_market_price_curves(self, tenant: str | None = None, status: str | None = None, limit: int = 100) -> tuple[dict, ...]:
        return self._list_records("energy_trading_risk_market_price_curve", tenant, status, limit)

    def list_exposure_limits(self, tenant: str | None = None, status: str | None = None, limit: int = 100) -> tuple[dict, ...]:
        return self._list_records("energy_trading_risk_exposure_limit", tenant, status, limit)

    def list_outbox_events(self, limit: int = 100) -> tuple[dict, ...]:
        rows = self.connection.execute(
            """
            SELECT id, tenant, code, status, version, payload
            FROM energy_trading_risk_appgen_outbox_event
            ORDER BY created_at ASC, id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return tuple(
            {
                "id": row["id"],
                "tenant": row["tenant"],
                "event_type": row["code"],
                "status": row["status"],
                "version": row["version"],
                "payload": _json_loads(row["payload"]) or {},
            }
            for row in rows
        )

    def database_manifest(self) -> dict:
        return {
            "ok": True,
            "database_path": self.database_path,
            "owned_tables": (
                "energy_trading_risk_energy_contract",
                "energy_trading_risk_trade_position",
                "energy_trading_risk_nomination",
                "energy_trading_risk_schedule",
                "energy_trading_risk_settlement",
                "energy_trading_risk_exposure_limit",
                "energy_trading_risk_market_price_curve",
                "energy_trading_risk_appgen_outbox_event",
            ),
            "migration_dir": str(MIGRATIONS_DIR),
            "shared_table_access": False,
            "side_effects": (),
        }
