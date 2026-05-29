"""Package-local persistence for the standalone MRP Engine application."""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from typing import Any

from . import runtime, seed_data

PBC_KEY = "mrp_engine"
STATE_TABLE = "mrp_engine_runtime_state"
FORM_TABLE = "mrp_engine_form_submission"
WORKFLOW_TABLE = "mrp_engine_workflow_run"
CONTROL_TABLE = "mrp_engine_control_execution"
AGENT_TABLE = "mrp_engine_agent_session"
READ_MODEL_TABLE = "mrp_engine_workbench_read_model"

_SCHEMA = f"""
CREATE TABLE IF NOT EXISTS {STATE_TABLE} (tenant TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {FORM_TABLE} (submission_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, form_key TEXT NOT NULL, action TEXT NOT NULL, subject_id TEXT, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (workflow_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, wizard_key TEXT NOT NULL, subject_id TEXT, status TEXT NOT NULL, context_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (control_run_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, control_key TEXT NOT NULL, allowed INTEGER NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {AGENT_TABLE} (session_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, skill_name TEXT NOT NULL, scope TEXT NOT NULL, requires_confirmation INTEGER NOT NULL, payload_json TEXT NOT NULL, result_json TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (read_model_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, bom_count INTEGER NOT NULL, demand_count INTEGER NOT NULL, run_count INTEGER NOT NULL, planned_order_count INTEGER NOT NULL, released_order_count INTEGER NOT NULL, shortage_total REAL NOT NULL, payload_json TEXT NOT NULL, updated_at TEXT NOT NULL);
"""


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def _load(value: str | None) -> Any:
    return None if value is None else json.loads(value)


def _now() -> str:
    return "local-harness-clock"


class MrpEngineStandaloneRepository:
    """Persist standalone MRP state, activity logs, controls, and read models."""

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
        return (STATE_TABLE, FORM_TABLE, WORKFLOW_TABLE, CONTROL_TABLE, AGENT_TABLE, READ_MODEL_TABLE)

    def load_state(self, tenant: str) -> dict:
        row = self.connection.execute(f"SELECT state_json FROM {STATE_TABLE} WHERE tenant = ?", (tenant,)).fetchone()
        if row is None:
            return runtime.mrp_engine_empty_state()
        loaded = _load(row["state_json"])
        return loaded if isinstance(loaded, dict) else runtime.mrp_engine_empty_state()

    def save_state(self, tenant: str, state: dict) -> dict:
        self.connection.execute(
            f"INSERT INTO {STATE_TABLE} VALUES (?, ?, ?) ON CONFLICT(tenant) DO UPDATE SET state_json = excluded.state_json, updated_at = excluded.updated_at",
            (tenant, _json(state), _now()),
        )
        self._sync_read_model(tenant, state)
        self.connection.commit()
        return {"ok": True, "tenant": tenant}

    def _sync_read_model(self, tenant: str, state: dict) -> None:
        boms = tuple(item for item in state.get("boms", {}).values() if item.get("tenant") == tenant)
        demands = tuple(item for item in state.get("demands", {}).values() if item.get("tenant") == tenant)
        runs = tuple(item for item in state.get("mrp_runs", {}).values() if item.get("tenant") == tenant)
        orders = tuple(item for item in state.get("planned_orders", {}).values() if item.get("tenant") == tenant)
        payload = runtime.mrp_engine_build_workbench_view(state, tenant=tenant) if state.get("configuration") else {"ok": True, "tenant": tenant}
        row = {
            "read_model_id": f"{tenant}:workbench",
            "tenant": tenant,
            "bom_count": len(boms),
            "demand_count": len(demands),
            "run_count": len(runs),
            "planned_order_count": len(orders),
            "released_order_count": len(tuple(item for item in orders if item.get("status") == "released")),
            "shortage_total": round(sum(float(item.get("shortage_qty", 0)) for item in orders), 2),
            "payload_json": _json(payload),
            "updated_at": _now(),
        }
        self.connection.execute(f"DELETE FROM {READ_MODEL_TABLE} WHERE tenant = ?", (tenant,))
        self.connection.execute(f"INSERT INTO {READ_MODEL_TABLE} ({', '.join(row)}) VALUES ({', '.join('?' for _ in row)})", tuple(row.values()))

    def _record(self, table: str, prefix: str, tenant: str, fields: tuple[Any, ...]) -> None:
        count = self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        self.connection.execute(f"INSERT INTO {table} VALUES ({', '.join('?' for _ in range(len(fields) + 1))})", (f"{prefix}_{count + 1:05d}", *fields))

    def _form(self, tenant: str, form_key: str, action: str, subject_id: str | None, payload: dict, result: dict) -> None:
        self._record(FORM_TABLE, "form", tenant, (tenant, form_key, action, subject_id, _json(payload), _json(result), _now()))

    def _workflow(self, tenant: str, wizard_key: str, subject_id: str | None, context: dict, result: dict) -> None:
        self._record(WORKFLOW_TABLE, "workflow", tenant, (tenant, wizard_key, subject_id, "completed" if result.get("ok") else "blocked", _json(context), _json(result), _now()))

    def _control(self, tenant: str, control_key: str, result: dict) -> None:
        self._record(CONTROL_TABLE, "control", tenant, (tenant, control_key, int(bool(result.get("ok"))), _json(result), _now()))

    def _result(self, tenant: str, result: dict) -> dict:
        if result.get("ok") is True and "state" in result:
            self.save_state(tenant, result["state"])
        return result

    def configure_runtime(self, tenant: str, configuration: dict) -> dict:
        normalized = {**configuration, "allowed_sites": tuple(configuration.get("allowed_sites", ())), "allowed_order_types": tuple(configuration.get("allowed_order_types", ())), "allowed_procurement_routes": tuple(configuration.get("allowed_procurement_routes", ())), "allowed_production_routes": tuple(configuration.get("allowed_production_routes", ())) }
        result = runtime.mrp_engine_configure_runtime(self.load_state(tenant), normalized)
        self._form(tenant, "MrpConfigurationForm", "configure_runtime", None, configuration, result)
        return self._result(tenant, result)

    def set_parameter(self, tenant: str, name: str, value: float) -> dict:
        result = runtime.mrp_engine_set_parameter(self.load_state(tenant), name, value)
        self._form(tenant, "MrpParameterForm", "set_parameter", name, {"name": name, "value": value}, result)
        return self._result(tenant, result)

    def register_rule(self, tenant: str, rule: dict) -> dict:
        result = runtime.mrp_engine_register_rule(self.load_state(tenant), rule)
        self._form(tenant, "MrpRuleForm", "register_rule", rule.get("rule_id"), rule, result)
        return self._result(tenant, result)

    def register_bom(self, tenant: str, bom: dict) -> dict:
        result = runtime.mrp_engine_register_bom(self.load_state(tenant), bom)
        self._form(tenant, "BomForm", "register_bom", bom.get("bom_id"), bom, result)
        return self._result(tenant, result)

    def ingest_demand_projection(self, tenant: str, demand: dict) -> dict:
        result = runtime.mrp_engine_ingest_demand_projection(self.load_state(tenant), demand)
        self._form(tenant, "DemandProjectionForm", "ingest_demand_projection", demand.get("demand_id"), demand, result)
        return self._result(tenant, result)

    def ingest_inventory_projection(self, tenant: str, inventory: dict) -> dict:
        result = runtime.mrp_engine_ingest_inventory_projection(self.load_state(tenant), inventory)
        self._form(tenant, "InventoryProjectionForm", "ingest_inventory_projection", inventory.get("inventory_id"), inventory, result)
        return self._result(tenant, result)

    def create_mrp_run(self, tenant: str, mrp_run: dict) -> dict:
        result = runtime.mrp_engine_create_mrp_run(self.load_state(tenant), mrp_run)
        self._workflow(tenant, "MrpRunWizard", mrp_run.get("run_id"), mrp_run, result)
        return self._result(tenant, result)

    def calculate_material_plan(self, tenant: str, run_id: str) -> dict:
        result = runtime.mrp_engine_calculate_material_plan(self.load_state(tenant), run_id)
        self._workflow(tenant, "NettingAndPeggingWizard", run_id, {"run_id": run_id}, result)
        return self._result(tenant, result)

    def release_planned_order(self, tenant: str, planned_order_id: str, released_by: str) -> dict:
        result = runtime.mrp_engine_release_planned_order(self.load_state(tenant), planned_order_id, released_by=released_by)
        self._workflow(tenant, "PlannedOrderReleaseWizard", planned_order_id, {"planned_order_id": planned_order_id}, result)
        return self._result(tenant, result)

    def run_control_tests(self, tenant: str) -> dict:
        result = runtime.mrp_engine_run_control_tests(self.load_state(tenant))
        self._control(tenant, "mrp_release_controls", result)
        self.connection.commit()
        return result

    def generate_supply_proof(self, tenant: str, planned_order_id: str, disclosure: tuple[str, ...]) -> dict:
        result = runtime.mrp_engine_generate_supply_proof(self.load_state(tenant), planned_order_id, disclosure=tuple(disclosure))
        self._control(tenant, "supply_availability_proof", result)
        self.connection.commit()
        return result

    def run_agent_skill(self, tenant: str, skill_name: str, payload: dict) -> dict:
        from . import agent
        plan = agent.document_instruction_plan(payload.get("document"), payload.get("instructions"))
        result = {"ok": plan["ok"], "skill_name": skill_name, "plan": plan, "requires_confirmation": True}
        count = self.connection.execute(f"SELECT COUNT(*) FROM {AGENT_TABLE}").fetchone()[0]
        self.connection.execute(f"INSERT INTO {AGENT_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (f"agent_{count + 1:05d}", tenant, skill_name, payload.get("scope", "planning"), 1, _json(payload), _json(result), _now()))
        self.connection.commit()
        return result

    def build_workbench(self, tenant: str) -> dict:
        state = self.load_state(tenant)
        return {"ok": True, **runtime.mrp_engine_build_workbench_view(state, tenant=tenant), "activity_counts": self.activity_counts(tenant), "read_model": self.read_model(tenant)}

    def read_model(self, tenant: str) -> dict:
        row = self.connection.execute(f"SELECT * FROM {READ_MODEL_TABLE} WHERE tenant = ?", (tenant,)).fetchone()
        if row is None:
            return {"ok": False, "tenant": tenant, "reason": "read_model_not_found"}
        data = dict(row)
        data["payload"] = _load(data.pop("payload_json"))
        data["ok"] = True
        return data

    def activity_counts(self, tenant: str) -> dict:
        return {
            "forms": self.connection.execute(f"SELECT COUNT(*) FROM {FORM_TABLE} WHERE tenant = ?", (tenant,)).fetchone()[0],
            "workflows": self.connection.execute(f"SELECT COUNT(*) FROM {WORKFLOW_TABLE} WHERE tenant = ?", (tenant,)).fetchone()[0],
            "controls": self.connection.execute(f"SELECT COUNT(*) FROM {CONTROL_TABLE} WHERE tenant = ?", (tenant,)).fetchone()[0],
            "agent_sessions": self.connection.execute(f"SELECT COUNT(*) FROM {AGENT_TABLE} WHERE tenant = ?", (tenant,)).fetchone()[0],
        }

    def seed_demo_workspace(self, tenant: str = "tenant_demo") -> dict:
        bundle = seed_data.standalone_seed_bundle(tenant=tenant)
        self.configure_runtime(tenant, bundle["configuration"])
        for name, value in bundle["parameters"].items():
            self.set_parameter(tenant, name, value)
        for rule in bundle["rules"]:
            self.register_rule(tenant, rule)
        bom = self.register_bom(tenant, bundle["bom"])
        demand = self.ingest_demand_projection(tenant, bundle["demand_projection"])
        inventory = self.ingest_inventory_projection(tenant, bundle["inventory_projection"])
        run = self.create_mrp_run(tenant, bundle["mrp_run"])
        plan = self.calculate_material_plan(tenant, bundle["mrp_run"]["run_id"])
        release = self.release_planned_order(tenant, "po_run_demo_100_component_a", "planner_1")
        controls = self.run_control_tests(tenant)
        proof = self.generate_supply_proof(tenant, "po_run_demo_100_component_a", ("planned_order_id", "item", "quantity"))
        agent = self.run_agent_skill(tenant, "mrp_engine.document_instruction_intake", {"document": bundle["document"], "instructions": bundle["instructions"], "scope": "seed"})
        return {"ok": all(item.get("ok") for item in (bom, demand, inventory, run, plan, release, controls, proof, agent)), "tenant": tenant, "bundle": bundle, "workbench": self.build_workbench(tenant)}


def standalone_repository_contract() -> dict:
    return {"format": "appgen.mrp-engine-standalone-repository.v1", "ok": True, "pbc": PBC_KEY, "repository_class": "MrpEngineStandaloneRepository", "local_harness_backend": "sqlite3", "deployment_database_backends": runtime.MRP_ENGINE_ALLOWED_DATABASE_BACKENDS, "tables": (STATE_TABLE, FORM_TABLE, WORKFLOW_TABLE, CONTROL_TABLE, AGENT_TABLE, READ_MODEL_TABLE), "side_effects": ()}


def standalone_repository_smoke_test() -> dict:
    repo = MrpEngineStandaloneRepository()
    try:
        seeded = repo.seed_demo_workspace()
        return {"ok": seeded["ok"] and repo.read_model("tenant_demo")["ok"], "seeded": seeded, "contract": standalone_repository_contract(), "side_effects": ()}
    finally:
        repo.close()
