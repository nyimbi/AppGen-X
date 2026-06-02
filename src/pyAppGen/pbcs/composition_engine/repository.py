"""SQLite-backed repository for the standalone Composition Engine PBC."""

from __future__ import annotations

from datetime import UTC
from datetime import datetime
import json
import re
from pathlib import Path
import sqlite3
from typing import Any

from .runtime import COMPOSITION_ENGINE_RUNTIME_TABLES

PACKAGE_DIR = Path(__file__).resolve().parent
MIGRATIONS_DIR = PACKAGE_DIR / "migrations"
PBC_KEY = "composition_engine"
OWNED_TABLES = (
    "composition_engine_composition_workspace",
    "composition_engine_component_registry",
    "composition_engine_ui_fragment",
    "composition_engine_layout_binding",
    "composition_engine_dsl_artifact",
    "composition_engine_composition_plan",
    "composition_engine_composition_validation_run",
    "composition_engine_package_registration_plan",
    "composition_engine_package_index_entry",
    "composition_engine_release_evidence",
    "composition_engine_composition_rule",
    "composition_engine_composition_parameter",
    "composition_engine_composition_configuration",
)
ALL_TABLES = OWNED_TABLES + COMPOSITION_ENGINE_RUNTIME_TABLES


def _utcnow() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def _json_dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str)


def _json_loads(value: Any) -> Any:
    if value in (None, ""):
        return None
    if isinstance(value, (dict, list, tuple, int, float, bool)):
        return value
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return value


class CompositionEngineRepository:
    """Owns standalone SQLite persistence for composition runtime state."""

    def __init__(self, database_path: str = ":memory:") -> None:
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def apply_migrations(self) -> tuple[str, ...]:
        applied: list[str] = []
        for migration_path in sorted(MIGRATIONS_DIR.glob("*.sql")):
            script = migration_path.read_text(encoding="utf-8")
            script = re.sub(r"^CREATE SCHEMA IF NOT EXISTS [^;]+;\n\n", "", script, flags=re.MULTILINE)
            self.connection.executescript(script)
            applied.append(migration_path.name)
        self.connection.commit()
        return tuple(applied)

    def reset(self) -> None:
        for table in reversed(ALL_TABLES):
            self.connection.execute(f"DELETE FROM {table}")
        self.connection.commit()

    def sync_state(self, state: dict[str, Any]) -> dict[str, Any]:
        self.reset()
        writers = (
            self._sync_workspaces,
            self._sync_components,
            self._sync_fragments,
            self._sync_bindings,
            self._sync_dsl_artifacts,
            self._sync_composition_plans,
            self._sync_validation_runs,
            self._sync_package_registration_plans,
            self._sync_package_index_entries,
            self._sync_release_evidence,
            self._sync_rules,
            self._sync_parameters,
            self._sync_configuration,
            self._sync_outbox,
            self._sync_inbox,
            self._sync_dead_letters,
        )
        for writer in writers:
            writer(state)
        self.connection.commit()
        return self.database_manifest()

    def list_rows(self, table: str, *, tenant: str | None = None) -> tuple[dict[str, Any], ...]:
        sql = f"SELECT * FROM {table}"
        params: tuple[Any, ...] = ()
        if tenant is not None:
            sql += " WHERE tenant = ?"
            params = (tenant,)
        sql += " ORDER BY id ASC"
        rows = self.connection.execute(sql, params).fetchall()
        return tuple(self._row_to_dict(row) for row in rows)

    def fetch_workspace(self, workspace_id: str) -> dict[str, Any] | None:
        row = self.connection.execute(
            """
            SELECT *
            FROM composition_engine_composition_workspace
            WHERE workspace_id = ?
            LIMIT 1
            """,
            (workspace_id,),
        ).fetchone()
        return self._row_to_dict(row) if row else None

    def workspace_summary(self, *, tenant: str) -> dict[str, Any]:
        workspaces = self.list_rows("composition_engine_composition_workspace", tenant=tenant)
        bindings = self.list_rows("composition_engine_layout_binding", tenant=tenant)
        package_plans = self.list_rows("composition_engine_package_registration_plan", tenant=tenant)
        release_rows = self.list_rows("composition_engine_release_evidence", tenant=tenant)
        return {
            "ok": True,
            "tenant": tenant,
            "workspace_count": len(workspaces),
            "published_count": len(tuple(item for item in workspaces if item.get("status") == "published")),
            "binding_count": len(bindings),
            "package_plan_count": len(package_plans),
            "release_evidence_count": len(release_rows),
            "side_effects": (),
        }

    def database_manifest(self) -> dict[str, Any]:
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "database_path": self.database_path,
            "owned_tables": OWNED_TABLES,
            "runtime_tables": COMPOSITION_ENGINE_RUNTIME_TABLES,
            "migration_dir": str(MIGRATIONS_DIR),
            "shared_table_access": False,
            "side_effects": (),
        }

    def _sync_workspaces(self, state: dict[str, Any]) -> None:
        for index, workspace in enumerate(sorted(state.get("workspaces", {}).values(), key=lambda item: item["workspace_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_composition_workspace (
                    id, tenant, workspace_id, name, owner, target, version, status,
                    selected_pbcs, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    workspace["tenant"],
                    workspace["workspace_id"],
                    workspace["name"],
                    workspace["owner"],
                    workspace["target"],
                    int(workspace.get("version", 1)),
                    workspace["status"],
                    _json_dumps(tuple(workspace.get("selected_pbcs", ()))),
                    now,
                    now,
                ),
            )

    def _sync_components(self, state: dict[str, Any]) -> None:
        for index, component in enumerate(sorted(state.get("components", {}).values(), key=lambda item: item["component_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_component_registry (
                    id, tenant, component_id, pbc, fragment, permissions, schemas,
                    status, compatibility, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    component["tenant"],
                    component["component_id"],
                    component["pbc"],
                    component["fragment"],
                    _json_dumps(tuple(component.get("permissions", ()))),
                    _json_dumps(tuple(component.get("schemas", ()))),
                    component.get("status", "registered"),
                    component.get("compatibility", "schema_validated"),
                    now,
                    now,
                ),
            )

    def _sync_fragments(self, state: dict[str, Any]) -> None:
        for index, fragment in enumerate(sorted(state.get("fragments", {}).values(), key=lambda item: item["fragment_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_ui_fragment (
                    id, tenant, fragment_id, component_id, route, slots, events,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    fragment["tenant"],
                    fragment["fragment_id"],
                    fragment["component_id"],
                    fragment["route"],
                    _json_dumps(tuple(fragment.get("slots", ()))),
                    _json_dumps(tuple(fragment.get("events", ()))),
                    fragment.get("status", "available"),
                    now,
                    now,
                ),
            )

    def _sync_bindings(self, state: dict[str, Any]) -> None:
        for index, binding in enumerate(sorted(state.get("bindings", {}).values(), key=lambda item: item["binding_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_layout_binding (
                    id, tenant, binding_id, workspace_id, page, slot,
                    fragment_id, projection, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    binding["tenant"],
                    binding["binding_id"],
                    binding["workspace_id"],
                    binding["page"],
                    binding["slot"],
                    binding["fragment_id"],
                    binding["projection"],
                    binding.get("status", "valid"),
                    now,
                    now,
                ),
            )

    def _sync_dsl_artifacts(self, state: dict[str, Any]) -> None:
        for index, artifact in enumerate(sorted(state.get("dsl_artifacts", {}).values(), key=lambda item: item["artifact_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_dsl_artifact (
                    id, tenant, artifact_id, workspace_id, route_count, checksum,
                    event_contract, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    state.get("workspaces", {}).get(artifact["workspace_id"], {}).get("tenant", "system"),
                    artifact["artifact_id"],
                    artifact["workspace_id"],
                    int(artifact.get("route_count", 0)),
                    artifact.get("checksum", ""),
                    artifact.get("dsl", {}).get("event_contract", "AppGen-X"),
                    "generated" if artifact.get("ok") else "draft",
                    now,
                    now,
                ),
            )

    def _sync_composition_plans(self, state: dict[str, Any]) -> None:
        for index, plan in enumerate(sorted(state.get("composition_plans", {}).values(), key=lambda item: item["workspace_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_composition_plan (
                    id, tenant, workspace_id, selected_pbcs, route_count, bindings,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    plan["tenant"],
                    plan["workspace_id"],
                    _json_dumps(tuple(plan.get("selected_pbcs", ()))),
                    int(plan.get("route_count", 0)),
                    _json_dumps(tuple(plan.get("bindings", ()))),
                    plan.get("status", "validated"),
                    now,
                    now,
                ),
            )

    def _sync_validation_runs(self, state: dict[str, Any]) -> None:
        for index, validation in enumerate(sorted(state.get("validation_runs", {}).values(), key=lambda item: item["validation_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_composition_validation_run (
                    id, tenant, validation_id, workspace_id, decision, blockers,
                    missing_fragments, route_count, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    validation["tenant"],
                    validation["validation_id"],
                    validation["workspace_id"],
                    validation["decision"],
                    _json_dumps(tuple(validation.get("blockers", ()))),
                    _json_dumps(tuple(validation.get("missing_fragments", ()))),
                    int(validation.get("route_count", 0)),
                    now,
                    now,
                ),
            )

    def _sync_package_registration_plans(self, state: dict[str, Any]) -> None:
        for index, plan in enumerate(sorted(state.get("package_registration_plans", {}).values(), key=lambda item: item["plan_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_package_registration_plan (
                    id, tenant, plan_id, workspace_id, requested_by, status,
                    side_effect_free, writes_performed, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    plan["tenant"],
                    plan["plan_id"],
                    plan["workspace_id"],
                    plan["requested_by"],
                    plan["status"],
                    "true" if plan.get("side_effect_free") else "false",
                    _json_dumps(tuple(plan.get("writes_performed", ()))),
                    now,
                    now,
                ),
            )

    def _sync_package_index_entries(self, state: dict[str, Any]) -> None:
        for index, entry in enumerate(sorted(state.get("package_index_entries", {}).values(), key=lambda item: item["workspace_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_package_index_entry (
                    id, tenant, workspace_id, selected_pbcs, status, entry_source,
                    indexed_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    entry["tenant"],
                    entry["workspace_id"],
                    _json_dumps(tuple(entry.get("selected_pbcs", ()))),
                    entry.get("status", "planned"),
                    entry.get("entry_source", "standalone_runtime"),
                    now,
                    now,
                    now,
                ),
            )

    def _sync_release_evidence(self, state: dict[str, Any]) -> None:
        for index, evidence in enumerate(sorted(state.get("release_evidence", {}).values(), key=lambda item: item["workspace_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_release_evidence (
                    id, tenant, workspace_id, version, route_count, release_risk,
                    status, package_registration_plan, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    evidence["tenant"],
                    evidence["workspace_id"],
                    int(evidence.get("version", 1)),
                    int(evidence.get("route_count", 0)),
                    str(evidence.get("release_risk", "0.0")),
                    evidence.get("status", "published"),
                    _json_dumps(evidence.get("package_registration_plan", {})),
                    now,
                    now,
                ),
            )

    def _sync_rules(self, state: dict[str, Any]) -> None:
        for index, rule in enumerate(sorted(state.get("rules", {}).values(), key=lambda item: item["rule_id"]), start=1):
            now = _utcnow()
            self.connection.execute(
                """
                INSERT INTO composition_engine_composition_rule (
                    id, tenant, rule_id, scope, required_fragments, allowed_meshes,
                    route_policy, requires_approval, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    rule["tenant"],
                    rule["rule_id"],
                    rule["scope"],
                    _json_dumps(tuple(rule.get("required_fragments", ()))),
                    _json_dumps(tuple(rule.get("allowed_meshes", ()))),
                    rule.get("route_policy", "balanced"),
                    "true" if rule.get("requires_approval") else "false",
                    rule.get("status", "active"),
                    now,
                    now,
                ),
            )

    def _sync_parameters(self, state: dict[str, Any]) -> None:
        now = _utcnow()
        for index, (key, value) in enumerate(sorted(state.get("parameters", {}).items()), start=1):
            self.connection.execute(
                """
                INSERT INTO composition_engine_composition_parameter (
                    id, tenant, parameter_id, key, value, effective_at, status,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    "system",
                    f"parameter::{key}",
                    key,
                    _json_dumps(value),
                    now,
                    "active",
                    now,
                    now,
                ),
            )

    def _sync_configuration(self, state: dict[str, Any]) -> None:
        configuration = dict(state.get("configuration", {}))
        if not configuration:
            return
        now = _utcnow()
        self.connection.execute(
            """
            INSERT INTO composition_engine_composition_configuration (
                id, tenant, configuration_id, database_backend, event_topic,
                retry_limit, default_timezone, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                "system",
                "runtime::default",
                configuration.get("database_backend", "postgresql"),
                configuration.get("event_topic", "appgen.composition.events"),
                str(configuration.get("retry_limit", 3)),
                configuration.get("default_timezone", "UTC"),
                "active" if configuration.get("ok") else "draft",
                now,
                now,
            ),
        )

    def _sync_outbox(self, state: dict[str, Any]) -> None:
        for index, event in enumerate(state.get("outbox", ()), start=1):
            now = _utcnow()
            payload = dict(event.get("payload", {}))
            self.connection.execute(
                f"""
                INSERT INTO {COMPOSITION_ENGINE_RUNTIME_TABLES[0]} (
                    id, tenant, event_id, event_type, payload, idempotency_key,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    payload.get("tenant", "system"),
                    event.get("event_id"),
                    event.get("event_type"),
                    _json_dumps(payload),
                    event.get("idempotency_key"),
                    event.get("status", "pending"),
                    now,
                    now,
                ),
            )

    def _sync_inbox(self, state: dict[str, Any]) -> None:
        for index, event in enumerate(state.get("inbox", ()), start=1):
            now = _utcnow()
            self.connection.execute(
                f"""
                INSERT INTO {COMPOSITION_ENGINE_RUNTIME_TABLES[1]} (
                    id, tenant, event_id, event_type, payload, idempotency_key,
                    attempts, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    event.get("tenant", "system"),
                    event.get("event_id"),
                    event.get("event_type"),
                    _json_dumps(event),
                    event.get("idempotency_key", f"{event.get('event_type')}:{event.get('event_id')}"),
                    int(event.get("attempts", 1)),
                    now,
                    now,
                ),
            )

    def _sync_dead_letters(self, state: dict[str, Any]) -> None:
        for index, event in enumerate(state.get("dead_letter", state.get("dead_letters", ())), start=1):
            now = _utcnow()
            self.connection.execute(
                f"""
                INSERT INTO {COMPOSITION_ENGINE_RUNTIME_TABLES[2]} (
                    id, tenant, event_id, event_type, reason, payload,
                    attempts, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    index,
                    event.get("tenant", "system"),
                    event.get("event_id"),
                    event.get("event_type"),
                    event.get("reason", "dead_letter"),
                    _json_dumps(event),
                    int(event.get("attempts", 1)),
                    now,
                    now,
                ),
            )

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        record = dict(row)
        for key, value in tuple(record.items()):
            if isinstance(value, str) and value and value[:1] in {"[", "{", '"'}:
                parsed = _json_loads(value)
                record[key] = parsed
        return record


def repository_manifest() -> dict[str, Any]:
    """Return the standalone repository contract without mutating a database."""
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "repository_class": "CompositionEngineRepository",
        "owned_tables": OWNED_TABLES,
        "runtime_tables": COMPOSITION_ENGINE_RUNTIME_TABLES,
        "migration_files": tuple(path.name for path in sorted(MIGRATIONS_DIR.glob("*.sql"))),
        "shared_table_access": False,
        "database_backends": ("sqlite",),
        "side_effects": (),
    }


def smoke_test() -> dict[str, Any]:
    """Exercise migrations and snapshot persistence for the standalone repository."""
    repository = CompositionEngineRepository()
    applied = repository.apply_migrations()
    repository.sync_state(
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": "appgen.composition.events",
                "retry_limit": 3,
                "default_timezone": "UTC",
                "ok": True,
            },
            "parameters": {"route_budget": 24},
            "rules": {
                "rule_demo": {
                    "tenant": "tenant_demo",
                    "rule_id": "rule_demo",
                    "scope": "workspace",
                    "required_fragments": ("CompositionWorkbench",),
                    "allowed_meshes": ("platform",),
                    "route_policy": "balanced",
                    "requires_approval": True,
                    "status": "active",
                }
            },
            "schema_extensions": {},
            "workspaces": {
                "ws_demo": {
                    "tenant": "tenant_demo",
                    "workspace_id": "ws_demo",
                    "name": "Demo Workspace",
                    "owner": "ops",
                    "target": "web",
                    "version": 1,
                    "status": "draft",
                    "selected_pbcs": ("customer_360",),
                }
            },
            "components": {},
            "fragments": {},
            "bindings": {},
            "dsl_artifacts": {},
            "composition_plans": {},
            "validation_runs": {},
            "package_registration_plans": {},
            "package_index_entries": {},
            "release_evidence": {},
            "events": [],
            "outbox": [],
            "inbox": [],
            "dead_letters": [],
            "dead_letter": [],
            "handled_events": {},
            "retry_evidence": [],
            "schema_projections": {},
            "route_projections": {},
            "audit_projections": {},
            "access_policy_projections": {},
            "workflow_projections": {},
            "package_registration_projections": {},
            "crypto_epoch": 1,
        }
    )
    summary = repository.workspace_summary(tenant="tenant_demo")
    workspace = repository.fetch_workspace("ws_demo")
    repository.close()
    return {
        "ok": bool(applied) and summary["workspace_count"] == 1 and workspace is not None,
        "applied_migrations": applied,
        "summary": summary,
        "workspace": workspace,
        "side_effects": (),
    }
