"""SQLite-backed repository for the standalone ar_credit PBC app."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPOSITORY_TABLES = (
    "ar_credit_runtime_snapshot",
    "ar_credit_workflow_run",
    "ar_credit_release_snapshot",
)


def _json_dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)


def _json_loads(value: str | None) -> object:
    if value in (None, ""):
        return None
    return json.loads(value)


class ArCreditRepository:
    """Persist standalone AR runtime state, workflow runs, and release snapshots."""

    def __init__(self, database_path: str = ":memory:"):
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def apply_migrations(self) -> tuple[str, ...]:
        statements = (
            (
                "create_runtime_snapshot",
                """
                CREATE TABLE IF NOT EXISTS ar_credit_runtime_snapshot (
                    tenant TEXT NOT NULL,
                    snapshot_kind TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (tenant, snapshot_kind)
                )
                """,
            ),
            (
                "create_workflow_run",
                """
                CREATE TABLE IF NOT EXISTS ar_credit_workflow_run (
                    run_id TEXT PRIMARY KEY,
                    tenant TEXT NOT NULL,
                    workflow_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    summary_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """,
            ),
            (
                "create_release_snapshot",
                """
                CREATE TABLE IF NOT EXISTS ar_credit_release_snapshot (
                    snapshot_id TEXT PRIMARY KEY,
                    tenant TEXT NOT NULL,
                    evidence_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """,
            ),
        )
        applied = []
        for migration_name, statement in statements:
            self.connection.execute(statement)
            applied.append(migration_name)
        self.connection.commit()
        return tuple(applied)

    def save_state(self, tenant: str, state: dict, *, snapshot_kind: str = "latest", captured_at: str = "1970-01-01T00:00:00Z") -> dict:
        payload = _json_dumps(state)
        self.connection.execute(
            """
            INSERT INTO ar_credit_runtime_snapshot (
                tenant,
                snapshot_kind,
                state_json,
                created_at,
                updated_at
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(tenant, snapshot_kind) DO UPDATE SET
                state_json = excluded.state_json,
                updated_at = excluded.updated_at
            """,
            (tenant, snapshot_kind, payload, captured_at, captured_at),
        )
        self.connection.commit()
        return {
            "ok": True,
            "tenant": tenant,
            "snapshot_kind": snapshot_kind,
            "state_size_bytes": len(payload.encode("utf-8")),
            "side_effects": (),
        }

    def load_state(self, tenant: str, *, snapshot_kind: str = "latest") -> dict | None:
        row = self.connection.execute(
            """
            SELECT state_json
            FROM ar_credit_runtime_snapshot
            WHERE tenant = ? AND snapshot_kind = ?
            """,
            (tenant, snapshot_kind),
        ).fetchone()
        if row is None:
            return None
        loaded = _json_loads(row["state_json"])
        return dict(loaded or {})

    def record_workflow_run(
        self,
        *,
        run_id: str,
        tenant: str,
        workflow_name: str,
        status: str,
        summary: dict,
        created_at: str,
    ) -> dict:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO ar_credit_workflow_run (
                run_id,
                tenant,
                workflow_name,
                status,
                summary_json,
                created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (run_id, tenant, workflow_name, status, _json_dumps(summary), created_at),
        )
        self.connection.commit()
        return {
            "ok": True,
            "run_id": run_id,
            "tenant": tenant,
            "workflow_name": workflow_name,
            "status": status,
            "side_effects": (),
        }

    def list_workflow_runs(self, *, tenant: str, limit: int = 25) -> tuple[dict, ...]:
        rows = self.connection.execute(
            """
            SELECT run_id, tenant, workflow_name, status, summary_json, created_at
            FROM ar_credit_workflow_run
            WHERE tenant = ?
            ORDER BY created_at ASC, run_id ASC
            LIMIT ?
            """,
            (tenant, limit),
        ).fetchall()
        return tuple(
            {
                "run_id": row["run_id"],
                "tenant": row["tenant"],
                "workflow_name": row["workflow_name"],
                "status": row["status"],
                "summary": dict(_json_loads(row["summary_json"]) or {}),
                "created_at": row["created_at"],
            }
            for row in rows
        )

    def save_release_snapshot(self, *, snapshot_id: str, tenant: str, evidence: dict, created_at: str) -> dict:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO ar_credit_release_snapshot (
                snapshot_id,
                tenant,
                evidence_json,
                created_at
            ) VALUES (?, ?, ?, ?)
            """,
            (snapshot_id, tenant, _json_dumps(evidence), created_at),
        )
        self.connection.commit()
        return {
            "ok": True,
            "snapshot_id": snapshot_id,
            "tenant": tenant,
            "side_effects": (),
        }

    def latest_release_snapshot(self, *, tenant: str) -> dict | None:
        row = self.connection.execute(
            """
            SELECT snapshot_id, tenant, evidence_json, created_at
            FROM ar_credit_release_snapshot
            WHERE tenant = ?
            ORDER BY created_at DESC, snapshot_id DESC
            LIMIT 1
            """,
            (tenant,),
        ).fetchone()
        if row is None:
            return None
        return {
            "snapshot_id": row["snapshot_id"],
            "tenant": row["tenant"],
            "evidence": dict(_json_loads(row["evidence_json"]) or {}),
            "created_at": row["created_at"],
        }

    def database_manifest(self) -> dict:
        return {
            "ok": True,
            "database_path": self.database_path,
            "owned_tables": REPOSITORY_TABLES,
            "shared_table_access": False,
            "side_effects": (),
        }
