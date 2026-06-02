"""Package-local persistence for the standalone DOM application."""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from typing import Any


PBC_KEY = "dom"
STATE_TABLE = "dom_runtime_state"
FORM_TABLE = "dom_form_submission"
WORKFLOW_TABLE = "dom_workflow_run"
CONTROL_TABLE = "dom_control_execution"
AGENT_TABLE = "dom_agent_session"
ORDER_READ_MODEL_TABLE = "dom_order_read_model"
EXCEPTION_READ_MODEL_TABLE = "dom_exception_read_model"

_SCHEMA = f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (
    tenant TEXT PRIMARY KEY,
    state_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS {FORM_TABLE} (
    submission_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    form_key TEXT NOT NULL,
    action TEXT NOT NULL,
    order_id TEXT,
    payload_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (
    workflow_run_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    wizard_key TEXT NOT NULL,
    order_id TEXT,
    status TEXT NOT NULL,
    context_json TEXT NOT NULL,
    steps_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (
    control_run_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_key TEXT NOT NULL,
    action TEXT NOT NULL,
    order_id TEXT,
    allowed INTEGER NOT NULL,
    payload_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (
    session_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    skill_name TEXT NOT NULL,
    scope TEXT NOT NULL,
    requires_confirmation INTEGER NOT NULL,
    payload_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS {ORDER_READ_MODEL_TABLE} (
    order_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL,
    channel TEXT NOT NULL,
    service_level TEXT NOT NULL,
    total REAL NOT NULL,
    promise_date_hint TEXT,
    atp_confidence REAL NOT NULL,
    active_hold_count INTEGER NOT NULL,
    open_exception_count INTEGER NOT NULL,
    open_backorder_count INTEGER NOT NULL,
    cancellation_status TEXT,
    shipment_status TEXT,
    payload_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS {EXCEPTION_READ_MODEL_TABLE} (
    exception_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    order_id TEXT NOT NULL,
    exception_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    blocking INTEGER NOT NULL,
    reason TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def _json_dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def _json_loads(value: str | None) -> Any:
    if value in (None, ""):
        return None
    return json.loads(value)


class DomStandaloneRepository:
    """Persist standalone DOM state, activity logs, and read models in SQLite."""

    def __init__(self, database_path: str = ":memory:") -> None:
        self.database_path = database_path
        if database_path != ":memory:":
            Path(database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self.apply_migrations()

    def close(self) -> None:
        self.connection.close()

    def apply_migrations(self) -> tuple[str, ...]:
        self.connection.executescript(_SCHEMA)
        self.connection.commit()
        return (
            STATE_TABLE,
            FORM_TABLE,
            WORKFLOW_TABLE,
            CONTROL_TABLE,
            AGENT_TABLE,
            ORDER_READ_MODEL_TABLE,
            EXCEPTION_READ_MODEL_TABLE,
        )

    def save_state(self, tenant: str, state: dict[str, Any], *, updated_at: str) -> dict[str, Any]:
        self.connection.execute(
            f"""
            INSERT INTO {STATE_TABLE} (tenant, state_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(tenant) DO UPDATE SET
                state_json = excluded.state_json,
                updated_at = excluded.updated_at
            """,
            (tenant, _json_dumps(state), updated_at),
        )
        self.connection.commit()
        return {"ok": True, "tenant": tenant, "updated_at": updated_at, "state_size": len(state)}

    def load_state(self, tenant: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            f"SELECT state_json FROM {STATE_TABLE} WHERE tenant = ?",
            (tenant,),
        ).fetchone()
        if row is None:
            return None
        loaded = _json_loads(row["state_json"])
        return loaded if isinstance(loaded, dict) else None

    def sync_read_models(self, tenant: str, state: dict[str, Any], *, updated_at: str) -> dict[str, Any]:
        orders = tuple(
            order
            for order in state.get("orders", {}).values()
            if order.get("tenant") == tenant
        )
        exceptions = tuple(
            item
            for item in state.get("exceptions", {}).values()
            if state.get("orders", {}).get(item.get("order_id"), {}).get("tenant") == tenant
        )
        self.connection.execute(f"DELETE FROM {ORDER_READ_MODEL_TABLE} WHERE tenant = ?", (tenant,))
        self.connection.execute(f"DELETE FROM {EXCEPTION_READ_MODEL_TABLE} WHERE tenant = ?", (tenant,))

        for order in orders:
            order_id = order["order_id"]
            holds = tuple(
                hold
                for hold in state.get("holds", {}).values()
                if hold.get("order_id") == order_id and hold.get("status") == "open"
            )
            open_exceptions = tuple(
                item
                for item in exceptions
                if item.get("order_id") == order_id and item.get("status") == "open"
            )
            backorders = tuple(
                item
                for item in state.get("backorders", {}).values()
                if item.get("order_id") == order_id and item.get("status") == "open"
            )
            cancellation = next(
                (
                    item
                    for item in reversed(tuple(state.get("cancellations", {}).values()))
                    if item.get("order_id") == order_id
                ),
                None,
            )
            shipment = state.get("shipment_statuses", {}).get(order_id)
            payload = {
                "order": order,
                "promise": state.get("promises", {}).get(order_id),
                "channel_context": state.get("channel_contexts", {}).get(order_id),
                "controls": state.get("order_controls", {}).get(order_id),
            }
            self.connection.execute(
                f"""
                INSERT OR REPLACE INTO {ORDER_READ_MODEL_TABLE} (
                    order_id,
                    tenant,
                    customer_id,
                    status,
                    channel,
                    service_level,
                    total,
                    promise_date_hint,
                    atp_confidence,
                    active_hold_count,
                    open_exception_count,
                    open_backorder_count,
                    cancellation_status,
                    shipment_status,
                    payload_json,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    order_id,
                    tenant,
                    order.get("customer_id", "unknown_customer"),
                    order.get("status", "draft"),
                    order.get("channel", "web"),
                    order.get("service_level", "standard"),
                    float(order.get("total", 0.0)),
                    (state.get("promises", {}).get(order_id) or {}).get("promise_date_hint"),
                    float((state.get("promises", {}).get(order_id) or {}).get("atp_confidence", 0.0)),
                    len(holds),
                    len(open_exceptions),
                    len(backorders),
                    cancellation.get("status") if cancellation else None,
                    shipment.get("status") if isinstance(shipment, dict) else order.get("status"),
                    _json_dumps(payload),
                    updated_at,
                ),
            )

        for item in exceptions:
            self.connection.execute(
                f"""
                INSERT OR REPLACE INTO {EXCEPTION_READ_MODEL_TABLE} (
                    exception_id,
                    tenant,
                    order_id,
                    exception_type,
                    severity,
                    status,
                    blocking,
                    reason,
                    payload_json,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item["exception_id"],
                    tenant,
                    item["order_id"],
                    item.get("type", "unspecified"),
                    item.get("severity", "medium"),
                    item.get("status", "open"),
                    1 if item.get("blocking", True) else 0,
                    item.get("reason", ""),
                    _json_dumps(item),
                    updated_at,
                ),
            )

        self.connection.commit()
        return {
            "ok": True,
            "tenant": tenant,
            "updated_at": updated_at,
            "order_read_models": len(orders),
            "exception_read_models": len(exceptions),
        }

    def record_form_submission(
        self,
        *,
        submission_id: str,
        tenant: str,
        form_key: str,
        action: str,
        order_id: str | None,
        payload: dict[str, Any],
        result: dict[str, Any],
        created_at: str,
    ) -> dict[str, Any]:
        self.connection.execute(
            f"""
            INSERT OR REPLACE INTO {FORM_TABLE} (
                submission_id, tenant, form_key, action, order_id, payload_json, result_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (submission_id, tenant, form_key, action, order_id, _json_dumps(payload), _json_dumps(result), created_at),
        )
        self.connection.commit()
        return {"submission_id": submission_id, "tenant": tenant, "form_key": form_key, "action": action}

    def record_workflow_run(
        self,
        *,
        workflow_run_id: str,
        tenant: str,
        wizard_key: str,
        order_id: str | None,
        status: str,
        context: dict[str, Any],
        steps: tuple[dict[str, Any], ...],
        result: dict[str, Any],
        created_at: str,
    ) -> dict[str, Any]:
        self.connection.execute(
            f"""
            INSERT OR REPLACE INTO {WORKFLOW_TABLE} (
                workflow_run_id, tenant, wizard_key, order_id, status, context_json, steps_json, result_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                workflow_run_id,
                tenant,
                wizard_key,
                order_id,
                status,
                _json_dumps(context),
                _json_dumps(steps),
                _json_dumps(result),
                created_at,
            ),
        )
        self.connection.commit()
        return {"workflow_run_id": workflow_run_id, "tenant": tenant, "wizard_key": wizard_key, "status": status}

    def record_control_execution(
        self,
        *,
        control_run_id: str,
        tenant: str,
        control_key: str,
        action: str,
        order_id: str | None,
        allowed: bool,
        payload: dict[str, Any],
        result: dict[str, Any],
        created_at: str,
    ) -> dict[str, Any]:
        self.connection.execute(
            f"""
            INSERT OR REPLACE INTO {CONTROL_TABLE} (
                control_run_id, tenant, control_key, action, order_id, allowed, payload_json, result_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                control_run_id,
                tenant,
                control_key,
                action,
                order_id,
                1 if allowed else 0,
                _json_dumps(payload),
                _json_dumps(result),
                created_at,
            ),
        )
        self.connection.commit()
        return {"control_run_id": control_run_id, "tenant": tenant, "control_key": control_key, "allowed": allowed}

    def record_agent_session(
        self,
        *,
        session_id: str,
        tenant: str,
        skill_name: str,
        scope: str,
        requires_confirmation: bool,
        payload: dict[str, Any],
        result: dict[str, Any],
        created_at: str,
    ) -> dict[str, Any]:
        self.connection.execute(
            f"""
            INSERT OR REPLACE INTO {AGENT_TABLE} (
                session_id, tenant, skill_name, scope, requires_confirmation, payload_json, result_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                tenant,
                skill_name,
                scope,
                1 if requires_confirmation else 0,
                _json_dumps(payload),
                _json_dumps(result),
                created_at,
            ),
        )
        self.connection.commit()
        return {"session_id": session_id, "tenant": tenant, "skill_name": skill_name, "scope": scope}

    def _list_rows(self, table: str, *, tenant: str, order_column: str, limit: int = 20) -> tuple[dict[str, Any], ...]:
        rows = self.connection.execute(
            f"SELECT * FROM {table} WHERE tenant = ? ORDER BY {order_column} DESC LIMIT ?",
            (tenant, limit),
        ).fetchall()
        decoded = []
        for row in rows:
            item = dict(row)
            for key in tuple(item):
                if key.endswith("_json"):
                    item[key.removesuffix("_json")] = _json_loads(item.pop(key))
            if "allowed" in item:
                item["allowed"] = bool(item["allowed"])
            if "requires_confirmation" in item:
                item["requires_confirmation"] = bool(item["requires_confirmation"])
            if "blocking" in item:
                item["blocking"] = bool(item["blocking"])
            decoded.append(item)
        return tuple(decoded)

    def list_form_submissions(self, tenant: str, *, limit: int = 20) -> tuple[dict[str, Any], ...]:
        return self._list_rows(FORM_TABLE, tenant=tenant, order_column="created_at", limit=limit)

    def list_workflow_runs(self, tenant: str, *, limit: int = 20) -> tuple[dict[str, Any], ...]:
        return self._list_rows(WORKFLOW_TABLE, tenant=tenant, order_column="created_at", limit=limit)

    def list_control_executions(self, tenant: str, *, limit: int = 20) -> tuple[dict[str, Any], ...]:
        return self._list_rows(CONTROL_TABLE, tenant=tenant, order_column="created_at", limit=limit)

    def list_agent_sessions(self, tenant: str, *, limit: int = 20) -> tuple[dict[str, Any], ...]:
        return self._list_rows(AGENT_TABLE, tenant=tenant, order_column="created_at", limit=limit)

    def list_order_read_models(
        self,
        tenant: str,
        *,
        status: str | None = None,
        limit: int = 50,
    ) -> tuple[dict[str, Any], ...]:
        query = f"SELECT * FROM {ORDER_READ_MODEL_TABLE} WHERE tenant = ?"
        params: list[Any] = [tenant]
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY updated_at DESC, order_id ASC LIMIT ?"
        params.append(limit)
        rows = self.connection.execute(query, params).fetchall()
        return tuple(
            {
                **{key: row[key] for key in row.keys() if key != "payload_json"},
                "payload": _json_loads(row["payload_json"]) or {},
            }
            for row in rows
        )

    def list_exception_read_models(
        self,
        tenant: str,
        *,
        status: str | None = None,
        limit: int = 50,
    ) -> tuple[dict[str, Any], ...]:
        query = f"SELECT * FROM {EXCEPTION_READ_MODEL_TABLE} WHERE tenant = ?"
        params: list[Any] = [tenant]
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY updated_at DESC, exception_id ASC LIMIT ?"
        params.append(limit)
        rows = self.connection.execute(query, params).fetchall()
        return tuple(
            {
                **{key: row[key] for key in row.keys() if key != "payload_json"},
                "blocking": bool(row["blocking"]),
                "payload": _json_loads(row["payload_json"]) or {},
            }
            for row in rows
        )

    def activity_dashboard(self, tenant: str, *, limit: int = 10) -> dict[str, Any]:
        forms = self.list_form_submissions(tenant, limit=limit)
        workflows = self.list_workflow_runs(tenant, limit=limit)
        controls = self.list_control_executions(tenant, limit=limit)
        sessions = self.list_agent_sessions(tenant, limit=limit)
        orders = self.list_order_read_models(tenant, limit=limit)
        exceptions = self.list_exception_read_models(tenant, limit=limit)
        has_state = self.load_state(tenant) is not None
        return {
            "ok": True,
            "tenant": tenant,
            "has_state": has_state,
            "counts": {
                "forms": len(forms),
                "workflows": len(workflows),
                "controls": len(controls),
                "agent_sessions": len(sessions),
                "orders": len(orders),
                "exceptions": len(exceptions),
            },
            "recent_forms": forms,
            "recent_workflows": workflows,
            "recent_controls": controls,
            "recent_agent_sessions": sessions,
            "recent_orders": orders,
            "recent_exceptions": exceptions,
        }

    def repository_manifest(self) -> dict[str, Any]:
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "repository_class": "DomStandaloneRepository",
            "database_path": self.database_path,
            "harness_backend": "sqlite3",
            "state_table": STATE_TABLE,
            "activity_tables": (FORM_TABLE, WORKFLOW_TABLE, CONTROL_TABLE, AGENT_TABLE),
            "read_model_tables": (ORDER_READ_MODEL_TABLE, EXCEPTION_READ_MODEL_TABLE),
            "shared_table_access": False,
            "supported_runtime_backends": ("postgresql", "mysql", "mariadb"),
            "side_effects": (),
        }


def smoke_test() -> dict[str, Any]:
    repository = DomStandaloneRepository()
    state = {
        "orders": {
            "order_100": {
                "tenant": "tenant_alpha",
                "order_id": "order_100",
                "customer_id": "cust_100",
                "status": "captured",
                "channel": "web",
                "service_level": "standard",
                "total": 220.0,
            }
        },
        "promises": {
            "order_100": {
                "promise_date_hint": "T+2d",
                "atp_confidence": 0.91,
            }
        },
        "holds": {
            "hold_100": {
                "hold_id": "hold_100",
                "order_id": "order_100",
                "status": "open",
            }
        },
        "exceptions": {
            "exception_100": {
                "exception_id": "exception_100",
                "order_id": "order_100",
                "type": "fraud_review",
                "severity": "high",
                "status": "open",
                "blocking": True,
                "reason": "manual review",
            }
        },
        "backorders": {},
        "cancellations": {},
        "channel_contexts": {
            "order_100": {"channel": "web"}
        },
        "order_controls": {
            "order_100": {"validation_issues": ()}
        },
        "shipment_statuses": {},
    }
    repository.save_state("tenant_alpha", state, updated_at="2026-01-01T00:00:00Z")
    repository.sync_read_models("tenant_alpha", state, updated_at="2026-01-01T00:00:00Z")
    repository.record_form_submission(
        submission_id="form_00001",
        tenant="tenant_alpha",
        form_key="order_capture_form",
        action="capture_order",
        order_id="order_100",
        payload={"order_id": "order_100"},
        result={"ok": True},
        created_at="2026-01-01T00:00:01Z",
    )
    repository.record_workflow_run(
        workflow_run_id="workflow_00001",
        tenant="tenant_alpha",
        wizard_key="order_intake_wizard",
        order_id="order_100",
        status="completed",
        context={"order_id": "order_100"},
        steps=({"step": "capture", "ok": True},),
        result={"ok": True},
        created_at="2026-01-01T00:00:02Z",
    )
    repository.record_control_execution(
        control_run_id="control_00001",
        tenant="tenant_alpha",
        control_key="run_control_tests",
        action="run_control_tests",
        order_id="order_100",
        allowed=True,
        payload={"order_id": "order_100"},
        result={"ok": True},
        created_at="2026-01-01T00:00:03Z",
    )
    repository.record_agent_session(
        session_id="agent_00001",
        tenant="tenant_alpha",
        skill_name="dom.document_instruction_intake",
        scope="preview",
        requires_confirmation=True,
        payload={"document": "order order_100"},
        result={"ok": True},
        created_at="2026-01-01T00:00:04Z",
    )
    dashboard = repository.activity_dashboard("tenant_alpha")
    read_models = repository.list_order_read_models("tenant_alpha")
    exceptions = repository.list_exception_read_models("tenant_alpha")
    state = repository.load_state("tenant_alpha")
    manifest = repository.repository_manifest()
    repository.close()
    return {
        "ok": manifest["ok"]
        and state is not None
        and dashboard["counts"]["forms"] == 1
        and dashboard["counts"]["workflows"] == 1
        and dashboard["counts"]["controls"] == 1
        and dashboard["counts"]["agent_sessions"] == 1
        and dashboard["counts"]["orders"] == 1
        and dashboard["counts"]["exceptions"] == 1
        and read_models[0]["active_hold_count"] == 1
        and exceptions[0]["blocking"] is True,
        "manifest": manifest,
        "dashboard": dashboard,
        "read_models": read_models,
        "exceptions": exceptions,
        "state": state,
        "side_effects": (),
    }
