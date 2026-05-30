"""SQLite-backed repository and read models for standalone global_inventory_visibility."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime

from . import runtime
from . import seed_data


PBC_KEY = "global_inventory_visibility"
_JSON_TEXT_COLUMNS = {"payload", "evidence_payload"}
_META_DEFAULTS = {
    "processed_event_keys": (),
    "retry_evidence": {},
    "adjustments": {},
    "schema_extensions": {},
    "crypto_epoch": {"epoch": 1, "algorithm": "sha3_256"},
}
_RUNTIME_META_KEYS = tuple(_META_DEFAULTS)
_EVENT_TABLE_CHANNELS = {
    "global_inventory_visibility_appgen_outbox_event": "outbox",
    "global_inventory_visibility_appgen_inbox_event": "inbox",
}
STANDALONE_SQLITE_TABLES = (
    {
        "table": "global_inventory_visibility_inventory_configuration",
        "columns": (
            ("configuration_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("database_backend", "TEXT NOT NULL"),
            ("event_topic", "TEXT NOT NULL"),
            ("retry_limit", "INTEGER NOT NULL"),
            ("workbench_limit", "REAL NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_inventory_parameter",
        "columns": (
            ("parameter_name", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("parameter_value", "REAL NOT NULL"),
            ("lower_bound", "REAL NOT NULL"),
            ("upper_bound", "REAL NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_inventory_rule",
        "columns": (
            ("rule_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("scope", "TEXT NOT NULL"),
            ("rule_type", "TEXT NOT NULL"),
            ("status", "TEXT NOT NULL"),
            ("compiled_hash", "TEXT NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_supply_node",
        "columns": (
            ("node_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("node_type", "TEXT NOT NULL"),
            ("region", "TEXT NOT NULL"),
            ("health_score", "REAL NOT NULL"),
            ("carbon_intensity", "REAL NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_inventory_pool",
        "columns": (
            ("pool_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("item_id", "TEXT NOT NULL"),
            ("pool_type", "TEXT NOT NULL"),
            ("allocation_policy", "TEXT NOT NULL"),
            ("safety_stock_units", "REAL NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_availability_snapshot",
        "columns": (
            ("snapshot_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("pool_id", "TEXT NOT NULL"),
            ("node_id", "TEXT NOT NULL"),
            ("on_hand", "REAL NOT NULL"),
            ("reserved", "REAL NOT NULL"),
            ("allocated", "REAL NOT NULL"),
            ("in_transit", "REAL NOT NULL"),
            ("freshness_score", "REAL NOT NULL"),
            ("staleness_minutes", "REAL NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_inventory_projection",
        "columns": (
            ("projection_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("pool_id", "TEXT NOT NULL"),
            ("item_id", "TEXT NOT NULL"),
            ("available_to_promise", "REAL NOT NULL"),
            ("capable_to_promise", "REAL NOT NULL"),
            ("freshness_score", "REAL NOT NULL"),
            ("confidence_score", "REAL NOT NULL"),
            ("in_transit", "REAL NOT NULL"),
            ("stale_snapshot_count", "INTEGER NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_inventory_reservation",
        "columns": (
            ("reservation_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("pool_id", "TEXT NOT NULL"),
            ("order_id", "TEXT NOT NULL"),
            ("channel", "TEXT NOT NULL"),
            ("quantity", "REAL NOT NULL"),
            ("status", "TEXT NOT NULL"),
            ("ttl_minutes", "REAL NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_inventory_control_assertion",
        "columns": (
            ("assertion_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("control_name", "TEXT NOT NULL"),
            ("control_status", "TEXT NOT NULL"),
            ("evidence_hash", "TEXT NOT NULL"),
            ("evidence_payload", "TEXT NOT NULL"),
            ("checked_at", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_appgen_outbox_event",
        "columns": (
            ("event_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("event_type", "TEXT NOT NULL"),
            ("topic", "TEXT NOT NULL"),
            ("idempotency_key", "TEXT NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("hash", "TEXT NOT NULL"),
            ("previous_hash", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_appgen_inbox_event",
        "columns": (
            ("event_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("event_type", "TEXT NOT NULL"),
            ("idempotency_key", "TEXT NOT NULL"),
            ("attempts", "INTEGER NOT NULL"),
            ("status", "TEXT NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("hash", "TEXT NOT NULL"),
            ("previous_hash", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_dead_letter_event",
        "columns": (
            ("event_id", "TEXT PRIMARY KEY"),
            ("tenant", "TEXT NOT NULL"),
            ("event_type", "TEXT NOT NULL"),
            ("idempotency_key", "TEXT NOT NULL"),
            ("attempts", "INTEGER NOT NULL"),
            ("reason", "TEXT NOT NULL"),
            ("payload", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_event_log",
        "columns": (
            ("event_sequence", "INTEGER PRIMARY KEY"),
            ("event_id", "TEXT NOT NULL UNIQUE"),
            ("event_type", "TEXT NOT NULL"),
            ("channel", "TEXT NOT NULL"),
            ("tenant", "TEXT"),
            ("pool_id", "TEXT"),
            ("idempotency_key", "TEXT NOT NULL"),
            ("payload", "TEXT NOT NULL"),
            ("previous_hash", "TEXT NOT NULL"),
            ("hash", "TEXT NOT NULL"),
        ),
    },
    {
        "table": "global_inventory_visibility_runtime_meta",
        "columns": (
            ("meta_key", "TEXT PRIMARY KEY"),
            ("payload", "TEXT NOT NULL"),
            ("updated_at", "TEXT NOT NULL"),
        ),
    },
)


def standalone_repository_contract() -> dict:
    tables = tuple(item["table"] for item in STANDALONE_SQLITE_TABLES)
    return {
        "format": "appgen.global-inventory-visibility-standalone-repository.v1",
        "ok": bool(tables) and all(table.startswith(f"{PBC_KEY}_") for table in tables),
        "pbc": PBC_KEY,
        "repository_class": "GlobalInventoryVisibilityRepository",
        "development_database_backend": "sqlite",
        "deployment_database_backends": runtime.GLOBAL_INVENTORY_VISIBILITY_ALLOWED_DATABASE_BACKENDS,
        "tables": STANDALONE_SQLITE_TABLES,
        "table_keys": tables,
        "event_tables": (
            "global_inventory_visibility_appgen_outbox_event",
            "global_inventory_visibility_appgen_inbox_event",
            "global_inventory_visibility_dead_letter_event",
            "global_inventory_visibility_event_log",
        ),
        "read_models": (
            "build_pool_read_model",
            "get_global_availability",
            "build_workbench",
            "build_release_read_model",
        ),
        "workflows": (
            "seed_demo_workspace",
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_supply_node",
            "register_inventory_pool",
            "record_availability_snapshot",
            "refresh_projection",
            "reserve_inventory",
            "receive_event",
            "generate_pool_proof",
        ),
        "side_effects": (),
    }


def standalone_sqlite_schema() -> str:
    statements = []
    for table in STANDALONE_SQLITE_TABLES:
        columns = ",\n  ".join(f"{name} {column_type}" for name, column_type in table["columns"])
        statements.append(f"CREATE TABLE IF NOT EXISTS {table['table']} (\n  {columns}\n);")
    return "\n\n".join(statements)

def _standalone_timestamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _standalone_json(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def _row_to_dict(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    data = dict(row)
    for key in tuple(data):
        if key in _JSON_TEXT_COLUMNS and isinstance(data[key], str):
            try:
                data[key] = json.loads(data[key])
            except json.JSONDecodeError:
                continue
    return data


class GlobalInventoryVisibilityRepository:
    """SQLite-backed repository for package-local one-PBC usage."""

    def __init__(self, database_path: str = ":memory:", connection: sqlite3.Connection | None = None):
        self.database_path = database_path
        self.connection = connection or sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self._ensure_schema()

    def close(self) -> None:
        self.connection.close()

    def _ensure_schema(self) -> None:
        self.connection.executescript(standalone_sqlite_schema())
        self.connection.commit()

    def _query_one(self, sql: str, params: tuple = ()) -> dict | None:
        return _row_to_dict(self.connection.execute(sql, params).fetchone())

    def _query_all(self, sql: str, params: tuple = ()) -> tuple[dict, ...]:
        rows = self.connection.execute(sql, params).fetchall()
        return tuple(_row_to_dict(row) for row in rows if row is not None)

    def _read_meta(self, key: str):
        row = self._query_one(
            "SELECT payload FROM global_inventory_visibility_runtime_meta WHERE meta_key = ?",
            (key,),
        )
        if row is None:
            default = _META_DEFAULTS[key]
            return list(default) if isinstance(default, tuple) else dict(default) if isinstance(default, dict) else default
        return row["payload"]

    def _write_meta(self, key: str, value) -> None:
        self.connection.execute(
            "DELETE FROM global_inventory_visibility_runtime_meta WHERE meta_key = ?",
            (key,),
        )
        self.connection.execute(
            "INSERT INTO global_inventory_visibility_runtime_meta (meta_key, payload, updated_at) VALUES (?, ?, ?)",
            (key, _standalone_json(value), _standalone_timestamp()),
        )

    def _load_state(self) -> dict:
        state = runtime.global_inventory_visibility_empty_state()
        config = self._query_one(
            "SELECT payload FROM global_inventory_visibility_inventory_configuration ORDER BY updated_at DESC LIMIT 1"
        )
        if config:
            state["configuration"] = config["payload"]
        parameters = self._query_all(
            "SELECT parameter_name, parameter_value FROM global_inventory_visibility_inventory_parameter ORDER BY parameter_name"
        )
        state["parameters"] = {
            row["parameter_name"]: row["parameter_value"] for row in parameters
        }
        rules = self._query_all(
            "SELECT rule_id, payload FROM global_inventory_visibility_inventory_rule ORDER BY rule_id"
        )
        state["rules"] = {row["rule_id"]: row["payload"] for row in rules}
        nodes = self._query_all(
            "SELECT node_id, payload FROM global_inventory_visibility_supply_node ORDER BY node_id"
        )
        state["supply_nodes"] = {row["node_id"]: row["payload"] for row in nodes}
        pools = self._query_all(
            "SELECT pool_id, payload FROM global_inventory_visibility_inventory_pool ORDER BY pool_id"
        )
        state["inventory_pools"] = {row["pool_id"]: row["payload"] for row in pools}
        snapshots = self._query_all(
            "SELECT snapshot_id, payload FROM global_inventory_visibility_availability_snapshot ORDER BY snapshot_id"
        )
        state["availability_snapshots"] = {row["snapshot_id"]: row["payload"] for row in snapshots}
        projections = self._query_all(
            "SELECT projection_id, payload FROM global_inventory_visibility_inventory_projection ORDER BY projection_id"
        )
        state["inventory_projections"] = {row["projection_id"]: row["payload"] for row in projections}
        reservations = self._query_all(
            "SELECT reservation_id, payload FROM global_inventory_visibility_inventory_reservation ORDER BY reservation_id"
        )
        state["reservations"] = {row["reservation_id"]: row["payload"] for row in reservations}
        state["outbox"] = tuple(
            row["payload"]
            for row in self._query_all(
                "SELECT payload FROM global_inventory_visibility_appgen_outbox_event ORDER BY event_id"
            )
        )
        state["inbox"] = tuple(
            row["payload"]
            for row in self._query_all(
                "SELECT payload FROM global_inventory_visibility_appgen_inbox_event ORDER BY event_id"
            )
        )
        state["dead_letters"] = tuple(
            row["payload"]
            for row in self._query_all(
                "SELECT payload FROM global_inventory_visibility_dead_letter_event ORDER BY event_id"
            )
        )
        state["events"] = tuple(
            row["payload"]
            for row in self._query_all(
                "SELECT payload FROM global_inventory_visibility_event_log ORDER BY event_sequence"
            )
        )
        state["processed_event_keys"] = tuple(self._read_meta("processed_event_keys"))
        state["retry_evidence"] = dict(self._read_meta("retry_evidence"))
        state["adjustments"] = dict(self._read_meta("adjustments"))
        state["schema_extensions"] = dict(self._read_meta("schema_extensions"))
        state["crypto_epoch"] = dict(self._read_meta("crypto_epoch"))
        return state

    def _rewrite_table(self, table: str, rows: tuple[dict, ...]) -> None:
        self.connection.execute(f"DELETE FROM {table}")
        if not rows:
            return
        columns = tuple(rows[0])
        placeholders = ", ".join("?" for _ in columns)
        self.connection.executemany(
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
            [tuple(row[column] for column in columns) for row in rows],
        )

    def _persist_control_assertions(self, state: dict) -> None:
        controls = runtime.global_inventory_visibility_run_control_tests(state)
        assertions = tuple(
            {
                "assertion_id": f"assertion_{index:03d}",
                "tenant": state.get("configuration", {}).get("tenant", state.get("configuration", {}).get("default_tenant", "tenant_demo")),
                "control_name": check["id"],
                "control_status": "pass" if check["ok"] else "fail",
                "evidence_hash": runtime._hash_payload(check),
                "evidence_payload": _standalone_json(check),
                "checked_at": _standalone_timestamp(),
            }
            for index, check in enumerate(controls["checks"], start=1)
        )
        self._rewrite_table("global_inventory_visibility_inventory_control_assertion", assertions)

    def _persist_state(self, state: dict) -> None:
        config = state.get("configuration", {})
        tenant = config.get("tenant") or next(
            (
                pool["tenant"]
                for pool in state.get("inventory_pools", {}).values()
                if pool.get("tenant")
            ),
            "tenant_demo",
        )
        now = _standalone_timestamp()
        configuration_rows = ()
        if config:
            configuration_rows = (
                {
                    "configuration_id": "active",
                    "tenant": tenant,
                    "database_backend": config.get("database_backend", "postgresql"),
                    "event_topic": config.get("event_topic", runtime.GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC),
                    "retry_limit": int(config.get("retry_limit", 3)),
                    "workbench_limit": float(config.get("workbench_limit", 100)),
                    "payload": _standalone_json(config),
                    "updated_at": now,
                },
            )
        parameter_rows = tuple(
            {
                "parameter_name": name,
                "tenant": tenant,
                "parameter_value": float(value),
                "lower_bound": float(runtime._ALLOWED_PARAMETERS[name][0]),
                "upper_bound": float(runtime._ALLOWED_PARAMETERS[name][1]),
                "payload": _standalone_json({"name": name, "value": value, "bounds": runtime._ALLOWED_PARAMETERS[name]}),
                "updated_at": now,
            }
            for name, value in sorted(state.get("parameters", {}).items())
        )
        rule_rows = tuple(
            {
                "rule_id": rule_id,
                "tenant": rule["tenant"],
                "scope": rule["scope"],
                "rule_type": rule["rule_type"],
                "status": rule["status"],
                "compiled_hash": rule["compiled_hash"],
                "payload": _standalone_json(rule),
                "updated_at": now,
            }
            for rule_id, rule in sorted(state.get("rules", {}).items())
        )
        node_rows = tuple(
            {
                "node_id": node_id,
                "tenant": node["tenant"],
                "node_type": node["node_type"],
                "region": node["region"],
                "health_score": float(node["health_score"]),
                "carbon_intensity": float(node["carbon_intensity"]),
                "payload": _standalone_json(node),
                "updated_at": now,
            }
            for node_id, node in sorted(state.get("supply_nodes", {}).items())
        )
        pool_rows = tuple(
            {
                "pool_id": pool_id,
                "tenant": pool["tenant"],
                "item_id": pool["item_id"],
                "pool_type": pool["pool_type"],
                "allocation_policy": pool["allocation_policy"],
                "safety_stock_units": float(pool["safety_stock_units"]),
                "payload": _standalone_json(pool),
                "updated_at": now,
            }
            for pool_id, pool in sorted(state.get("inventory_pools", {}).items())
        )
        snapshot_rows = tuple(
            {
                "snapshot_id": snapshot_id,
                "tenant": snapshot["tenant"],
                "pool_id": snapshot["pool_id"],
                "node_id": snapshot["node_id"],
                "on_hand": float(snapshot["on_hand"]),
                "reserved": float(snapshot["reserved"]),
                "allocated": float(snapshot["allocated"]),
                "in_transit": float(snapshot["in_transit"]),
                "freshness_score": float(snapshot["freshness_score"]),
                "staleness_minutes": float(snapshot["staleness_minutes"]),
                "payload": _standalone_json(snapshot),
                "updated_at": now,
            }
            for snapshot_id, snapshot in sorted(state.get("availability_snapshots", {}).items())
        )
        projection_rows = tuple(
            {
                "projection_id": projection_id,
                "tenant": projection["tenant"],
                "pool_id": projection["pool_id"],
                "item_id": projection["item_id"],
                "available_to_promise": float(projection["available_to_promise"]),
                "capable_to_promise": float(projection["capable_to_promise"]),
                "freshness_score": float(projection["freshness_score"]),
                "confidence_score": float(projection["confidence_score"]),
                "in_transit": float(projection["in_transit"]),
                "stale_snapshot_count": int(projection["stale_snapshot_count"]),
                "payload": _standalone_json(projection),
                "updated_at": now,
            }
            for projection_id, projection in sorted(state.get("inventory_projections", {}).items())
        )
        reservation_rows = tuple(
            {
                "reservation_id": reservation_id,
                "tenant": reservation["tenant"],
                "pool_id": reservation["pool_id"],
                "order_id": reservation["order_id"],
                "channel": reservation["channel"],
                "quantity": float(reservation["quantity"]),
                "status": reservation["status"],
                "ttl_minutes": float(reservation["ttl_minutes"]),
                "payload": _standalone_json(reservation),
                "updated_at": now,
            }
            for reservation_id, reservation in sorted(state.get("reservations", {}).items())
        )
        outbox_rows = tuple(
            {
                "event_id": event["event_id"],
                "tenant": event["payload"].get("tenant", tenant),
                "event_type": event["event_type"],
                "topic": runtime.GLOBAL_INVENTORY_VISIBILITY_REQUIRED_EVENT_TOPIC,
                "idempotency_key": event["idempotency_key"],
                "payload": _standalone_json(event),
                "hash": event["hash"],
                "previous_hash": event["previous_hash"],
            }
            for event in state.get("outbox", ())
        )
        inbox_rows = tuple(
            {
                "event_id": event["event_id"],
                "tenant": event["payload"].get("tenant", tenant),
                "event_type": event["event_type"],
                "idempotency_key": event["idempotency_key"],
                "attempts": int(state.get("retry_evidence", {}).get(event["idempotency_key"], 0)),
                "status": "processed",
                "payload": _standalone_json(event),
                "hash": event["hash"],
                "previous_hash": event["previous_hash"],
            }
            for event in state.get("inbox", ())
        )
        dead_letter_rows = tuple(
            {
                "event_id": dead_letter["event_id"],
                "tenant": dead_letter.get("tenant", tenant),
                "event_type": dead_letter["event_type"],
                "idempotency_key": dead_letter["idempotency_key"],
                "attempts": int(dead_letter.get("retry_count", dead_letter.get("attempts", 0))),
                "reason": dead_letter["reason"],
                "payload": _standalone_json(dead_letter),
            }
            for dead_letter in state.get("dead_letters", ())
        )
        event_log_rows = tuple(
            {
                "event_sequence": index,
                "event_id": event["event_id"],
                "event_type": event["event_type"],
                "channel": "outbox" if event in state.get("outbox", ()) else "inbox" if event in state.get("inbox", ()) else "event",
                "tenant": event["payload"].get("tenant", tenant),
                "pool_id": event["payload"].get("pool_id"),
                "idempotency_key": event["idempotency_key"],
                "payload": _standalone_json(event),
                "previous_hash": event["previous_hash"],
                "hash": event["hash"],
            }
            for index, event in enumerate(state.get("events", ()), start=1)
        )
        self._rewrite_table("global_inventory_visibility_inventory_configuration", configuration_rows)
        self._rewrite_table("global_inventory_visibility_inventory_parameter", parameter_rows)
        self._rewrite_table("global_inventory_visibility_inventory_rule", rule_rows)
        self._rewrite_table("global_inventory_visibility_supply_node", node_rows)
        self._rewrite_table("global_inventory_visibility_inventory_pool", pool_rows)
        self._rewrite_table("global_inventory_visibility_availability_snapshot", snapshot_rows)
        self._rewrite_table("global_inventory_visibility_inventory_projection", projection_rows)
        self._rewrite_table("global_inventory_visibility_inventory_reservation", reservation_rows)
        self._rewrite_table("global_inventory_visibility_appgen_outbox_event", outbox_rows)
        self._rewrite_table("global_inventory_visibility_appgen_inbox_event", inbox_rows)
        self._rewrite_table("global_inventory_visibility_dead_letter_event", dead_letter_rows)
        self._rewrite_table("global_inventory_visibility_event_log", event_log_rows)
        for key in _RUNTIME_META_KEYS:
            value = state.get(key, _META_DEFAULTS[key])
            self._write_meta(key, value)
        self._persist_control_assertions(state)
        self.connection.commit()

    def _result(self, result: dict) -> dict:
        if result.get("ok") is True and "state" in result:
            self._persist_state(result["state"])
        return result

    def reset(self) -> dict:
        empty = runtime.global_inventory_visibility_empty_state()
        self._persist_state(empty)
        return {"ok": True, "state": empty, "side_effects": ()}

    def configure_runtime(self, configuration: dict) -> dict:
        state = self._load_state()
        return self._result(runtime.global_inventory_visibility_configure_runtime(state, configuration))

    def set_parameter(self, name: str, value: float | int) -> dict:
        state = self._load_state()
        return self._result(runtime.global_inventory_visibility_set_parameter(state, name, value))

    def register_rule(self, rule: dict) -> dict:
        state = self._load_state()
        return self._result(runtime.global_inventory_visibility_register_rule(state, rule))

    def register_supply_node(self, node: dict) -> dict:
        state = self._load_state()
        return self._result(runtime.global_inventory_visibility_register_supply_node(state, node))

    def register_inventory_pool(self, pool: dict) -> dict:
        state = self._load_state()
        return self._result(runtime.global_inventory_visibility_register_inventory_pool(state, pool))

    def record_availability_snapshot(self, snapshot: dict) -> dict:
        state = self._load_state()
        return self._result(runtime.global_inventory_visibility_record_availability_snapshot(state, snapshot))

    def refresh_projection(self, *, tenant: str, pool_id: str) -> dict:
        state = self._load_state()
        return self._result(runtime.global_inventory_visibility_project_availability(state, tenant=tenant, pool_id=pool_id))

    def reserve_inventory(self, reservation: dict) -> dict:
        state = self._load_state()
        return self._result(runtime.global_inventory_visibility_reserve_inventory(state, reservation))

    def receive_event(self, event: dict) -> dict:
        state = self._load_state()
        return self._result(runtime.global_inventory_visibility_ingest_event(state, event))

    def generate_pool_proof(self, *, pool_id: str, disclosure: tuple[str, ...]) -> dict:
        state = self._load_state()
        return runtime.global_inventory_visibility_generate_availability_proof(
            state,
            pool_id=pool_id,
            disclosure=disclosure,
        )

    def build_pool_read_model(self, *, pool_id: str, tenant: str | None = None) -> dict:
        state = self._load_state()
        pool = state["inventory_pools"].get(pool_id)
        if pool is None:
            return {"ok": False, "reason": "pool_not_found", "pool_id": pool_id}
        active_tenant = tenant or pool["tenant"]
        snapshots = self._query_all(
            "SELECT payload FROM global_inventory_visibility_availability_snapshot WHERE pool_id = ? ORDER BY snapshot_id",
            (pool_id,),
        )
        projections = self._query_all(
            "SELECT payload FROM global_inventory_visibility_inventory_projection WHERE pool_id = ? ORDER BY projection_id",
            (pool_id,),
        )
        reservations = self._query_all(
            "SELECT payload FROM global_inventory_visibility_inventory_reservation WHERE pool_id = ? ORDER BY reservation_id",
            (pool_id,),
        )
        latest_projection = projections[-1]["payload"] if projections else None
        aggregate = runtime.global_inventory_visibility_get_global_availability(
            state,
            tenant=active_tenant,
            item_id=pool["item_id"],
        ) if projections else {
            "ok": True,
            "tenant": active_tenant,
            "item_id": pool["item_id"],
            "projection_count": 0,
            "available_to_promise": 0.0,
            "capable_to_promise": 0.0,
            "freshness_score": 0.0,
            "stale_snapshot_count": 0,
            "pools": (pool_id,),
        }
        return {
            "ok": True,
            "tenant": active_tenant,
            "pool": pool,
            "snapshots": tuple(row["payload"] for row in snapshots),
            "latest_projection": latest_projection,
            "reservations": tuple(row["payload"] for row in reservations),
            "aggregate": aggregate,
            "nodes": tuple(
                state["supply_nodes"][node_id] for node_id in pool.get("node_ids", ()) if node_id in state["supply_nodes"]
            ),
            "release_controls": self._query_all(
                "SELECT control_name, control_status, evidence_payload, checked_at FROM global_inventory_visibility_inventory_control_assertion ORDER BY assertion_id"
            ),
        }

    def list_inventory_pools(self, tenant: str) -> tuple[dict, ...]:
        return tuple(
            row["payload"]
            for row in self._query_all(
                "SELECT payload FROM global_inventory_visibility_inventory_pool WHERE tenant = ? ORDER BY pool_id",
                (tenant,),
            )
        )

    def list_supply_nodes(self, tenant: str) -> tuple[dict, ...]:
        return tuple(
            row["payload"]
            for row in self._query_all(
                "SELECT payload FROM global_inventory_visibility_supply_node WHERE tenant = ? ORDER BY node_id",
                (tenant,),
            )
        )

    def get_global_availability(self, *, tenant: str, item_id: str | None = None) -> dict:
        state = self._load_state()
        return runtime.global_inventory_visibility_get_global_availability(state, tenant=tenant, item_id=item_id)

    def build_workbench(self, tenant: str) -> dict:
        state = self._load_state()
        workbench = runtime.global_inventory_visibility_build_workbench_view(state, tenant=tenant)
        freshness_alert_count = self.connection.execute(
            "SELECT COUNT(*) FROM global_inventory_visibility_inventory_projection WHERE tenant = ? AND stale_snapshot_count > 0",
            (tenant,),
        ).fetchone()[0]
        release_control_failures = self.connection.execute(
            "SELECT COUNT(*) FROM global_inventory_visibility_inventory_control_assertion WHERE control_status != 'pass'",
        ).fetchone()[0]
        proof_targets = tuple(pool["pool_id"] for pool in self.list_inventory_pools(tenant))
        return {
            "ok": True,
            "tenant": tenant,
            **workbench,
            "pool_ids": proof_targets,
            "freshness_alert_count": freshness_alert_count,
            "release_control_failure_count": release_control_failures,
            "pool_read_models": tuple(
                self.build_pool_read_model(pool_id=pool_id, tenant=tenant)
                for pool_id in proof_targets
            ),
        }

    def build_release_read_model(self, tenant: str) -> dict:
        state = self._load_state()
        controls = runtime.global_inventory_visibility_run_control_tests(state)
        workbench = self.build_workbench(tenant)
        proof_rows = tuple(
            self.generate_pool_proof(
                pool_id=pool_id,
                disclosure=("available_to_promise", "capable_to_promise", "freshness_score"),
            )
            for pool_id in workbench.get("pool_ids", ())
        )
        return {
            "ok": controls["ok"] and workbench["ok"] and all(item["ok"] for item in proof_rows),
            "tenant": tenant,
            "control_tests": controls,
            "workbench": workbench,
            "proofs": proof_rows,
            "assertions": self._query_all(
                "SELECT assertion_id, control_name, control_status, evidence_hash, checked_at FROM global_inventory_visibility_inventory_control_assertion ORDER BY assertion_id"
            ),
        }

    def seed_demo_workspace(self, *, tenant: str = "tenant_demo") -> dict:
        bundle = seed_data.standalone_seed_bundle(tenant=tenant)
        state = runtime.global_inventory_visibility_empty_state()
        configuration = {**bundle["configuration"], "tenant": tenant}
        state = runtime.global_inventory_visibility_configure_runtime(state, configuration)["state"]
        for name, value in bundle["parameters"].items():
            state = runtime.global_inventory_visibility_set_parameter(state, name, value)["state"]
        for rule in bundle["rules"]:
            state = runtime.global_inventory_visibility_register_rule(state, rule)["state"]
        for node in bundle["supply_nodes"]:
            state = runtime.global_inventory_visibility_register_supply_node(state, node)["state"]
        for pool in bundle["inventory_pools"]:
            state = runtime.global_inventory_visibility_register_inventory_pool(state, pool)["state"]
        for snapshot in bundle["availability_snapshots"]:
            state = runtime.global_inventory_visibility_record_availability_snapshot(state, snapshot)["state"]
        for pool in bundle["inventory_pools"]:
            state = runtime.global_inventory_visibility_project_availability(
                state,
                tenant=tenant,
                pool_id=pool["pool_id"],
            )["state"]
        for reservation in bundle["reservations"]:
            state = runtime.global_inventory_visibility_reserve_inventory(state, reservation)["state"]
        for event in bundle["events"]:
            state = runtime.global_inventory_visibility_ingest_event(state, event)["state"]
        for pool in bundle["inventory_pools"]:
            state = runtime.global_inventory_visibility_project_availability(
                state,
                tenant=tenant,
                pool_id=pool["pool_id"],
            )["state"]
        self._persist_state(state)
        return {
            "ok": True,
            "tenant": tenant,
            "seed_bundle": bundle,
            "workbench": self.build_workbench(tenant),
            "side_effects": (),
        }


def standalone_repository_smoke_test() -> dict:
    repository = GlobalInventoryVisibilityRepository()
    try:
        seeded = repository.seed_demo_workspace()
        workbench = repository.build_workbench("tenant_demo")
        primary_pool = repository.build_pool_read_model(pool_id="pool_global_primary", tenant="tenant_demo")
        aggregate = repository.get_global_availability(tenant="tenant_demo", item_id="sku_100")
        release = repository.build_release_read_model("tenant_demo")
        proof = repository.generate_pool_proof(
            pool_id="pool_global_primary",
            disclosure=("available_to_promise", "capable_to_promise", "freshness_score"),
        )
        return {
            "ok": seeded["ok"] and workbench["ok"] and primary_pool["ok"] and aggregate["ok"] and release["ok"] and proof["ok"],
            "contract": standalone_repository_contract(),
            "seeded": seeded,
            "workbench": workbench,
            "primary_pool": primary_pool,
            "aggregate": aggregate,
            "release": release,
            "proof": proof,
            "side_effects": (),
        }
    finally:
        repository.close()
