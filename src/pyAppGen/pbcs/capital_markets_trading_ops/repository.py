"""Database-backed repository for the capital_markets_trading_ops one-PBC app."""
from __future__ import annotations

import json
from pathlib import Path
import sqlite3

PACKAGE_DIR = Path(__file__).resolve().parent
MIGRATIONS_DIR = PACKAGE_DIR / 'migrations'


def _json_dumps(value) -> str:
    return json.dumps(value, sort_keys=True)


def _json_loads(value):
    if value in (None, ''):
        return None
    return json.loads(value)


class CapitalMarketsTradingOpsRepository:
    """Applies owned migrations and persists trade-order slice records."""

    def __init__(self, database_path: str = ':memory:'):
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def apply_migrations(self) -> tuple[str, ...]:
        applied = []
        for migration_path in sorted(MIGRATIONS_DIR.glob('*.sql')):
            self.connection.executescript(migration_path.read_text())
            applied.append(migration_path.name)
        self.connection.commit()
        return tuple(applied)

    def save_trade_order(self, record: dict, events=()) -> dict:
        payload = dict(record.get('payload', {}))
        validation = dict(record.get('validation', {}))
        self.connection.execute(
            """
            INSERT OR REPLACE INTO capital_markets_trading_ops_trade_order (
                id,
                tenant,
                code,
                status,
                version,
                payload,
                created_at,
                updated_at,
                lifecycle_state,
                status_badge,
                workbench_queue,
                release_ready,
                trade_order_signature,
                validation_payload,
                actionable_remediation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record['id'],
                record.get('tenant', 'default'),
                payload.get('code', record['id']),
                record.get('status'),
                record.get('version', 1),
                _json_dumps(payload),
                payload.get('submitted_at'),
                payload.get('submitted_at'),
                record.get('lifecycle_state'),
                record.get('status_badge'),
                record.get('workbench_queue'),
                1 if record.get('release_ready') else 0,
                record.get('trade_order_signature'),
                _json_dumps(validation),
                _json_dumps(record.get('actionable_remediation', ())),
            ),
        )
        for index, event in enumerate(events, start=1):
            event_payload = dict(event.get('payload', {}))
            self.connection.execute(
                """
                INSERT OR REPLACE INTO capital_markets_trading_ops_appgen_outbox_event (
                    id, tenant, code, status, version, payload, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.get('idempotency_key', f"{record['id']}-event-{index}"),
                    record.get('tenant', 'default'),
                    event.get('event_type'),
                    'pending',
                    1,
                    _json_dumps(
                        {
                            'event_type': event.get('event_type'),
                            'topic': event.get('topic'),
                            'payload': event_payload,
                            'idempotency_key': event.get('idempotency_key'),
                        }
                    ),
                    payload.get('submitted_at'),
                    payload.get('submitted_at'),
                ),
            )
        self.connection.commit()
        return record

    def list_trade_orders(self, tenant: str | None = None, status: str | None = None, workbench_queue: str | None = None, limit: int = 50) -> tuple[dict, ...]:
        query = """
            SELECT
                id,
                tenant,
                code,
                status,
                version,
                payload,
                lifecycle_state,
                status_badge,
                workbench_queue,
                release_ready,
                trade_order_signature,
                validation_payload,
                actionable_remediation
            FROM capital_markets_trading_ops_trade_order
            WHERE 1 = 1
        """
        params = []
        if tenant:
            query += " AND tenant = ?"
            params.append(tenant)
        if status:
            query += " AND status = ?"
            params.append(status)
        if workbench_queue:
            query += " AND workbench_queue = ?"
            params.append(workbench_queue)
        query += " ORDER BY created_at ASC, id ASC LIMIT ?"
        params.append(limit)
        rows = self.connection.execute(query, params).fetchall()
        return tuple(
            {
                'id': row['id'],
                'tenant': row['tenant'],
                'code': row['code'],
                'status': row['status'],
                'version': row['version'],
                'payload': _json_loads(row['payload']) or {},
                'lifecycle_state': row['lifecycle_state'],
                'status_badge': row['status_badge'],
                'workbench_queue': row['workbench_queue'],
                'release_ready': bool(row['release_ready']),
                'trade_order_signature': row['trade_order_signature'],
                'validation': _json_loads(row['validation_payload']) or {},
                'actionable_remediation': tuple(_json_loads(row['actionable_remediation']) or ()),
            }
            for row in rows
        )

    def list_outbox_events(self, limit: int = 50) -> tuple[dict, ...]:
        rows = self.connection.execute(
            """
            SELECT id, tenant, code, status, version, payload
            FROM capital_markets_trading_ops_appgen_outbox_event
            ORDER BY created_at ASC, id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return tuple(
            {
                'id': row['id'],
                'tenant': row['tenant'],
                'event_type': row['code'],
                'status': row['status'],
                'version': row['version'],
                'payload': _json_loads(row['payload']) or {},
            }
            for row in rows
        )

    def database_manifest(self) -> dict:
        return {
            'ok': True,
            'database_path': self.database_path,
            'owned_tables': (
                'capital_markets_trading_ops_trade_order',
                'capital_markets_trading_ops_appgen_outbox_event',
            ),
            'migration_dir': str(MIGRATIONS_DIR),
            'shared_table_access': False,
            'side_effects': (),
        }
