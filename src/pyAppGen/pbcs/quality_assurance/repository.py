"""Package-local persistence for the standalone Quality Assurance application."""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from typing import Any

from . import runtime
from . import seed_data


PBC_KEY = "quality_assurance"
STATE_TABLE = "quality_assurance_runtime_state"
FORM_TABLE = "quality_assurance_form_submission"
WORKFLOW_TABLE = "quality_assurance_workflow_run"
CONTROL_TABLE = "quality_assurance_control_execution"
AGENT_TABLE = "quality_assurance_agent_session"
READ_MODEL_TABLE = "quality_assurance_workbench_read_model"

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
    subject_id TEXT,
    payload_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS {WORKFLOW_TABLE} (
    workflow_run_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    wizard_key TEXT NOT NULL,
    subject_id TEXT,
    status TEXT NOT NULL,
    context_json TEXT NOT NULL,
    result_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS {CONTROL_TABLE} (
    control_run_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    control_key TEXT NOT NULL,
    allowed INTEGER NOT NULL,
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
CREATE TABLE IF NOT EXISTS {READ_MODEL_TABLE} (
    read_model_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    plan_count INTEGER NOT NULL,
    result_count INTEGER NOT NULL,
    hold_count INTEGER NOT NULL,
    open_nc_count INTEGER NOT NULL,
    released_hold_count INTEGER NOT NULL,
    failed_result_count INTEGER NOT NULL,
    cpk_minimum REAL NOT NULL,
    payload_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def _load(value: str | None) -> Any:
    return None if value is None else json.loads(value)


def _now() -> str:
    return "local-harness-clock"


class QualityAssuranceStandaloneRepository:
    """Persist standalone QA state, activity logs, controls, and read models."""

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
            return runtime.quality_assurance_empty_state()
        loaded = _load(row["state_json"])
        return loaded if isinstance(loaded, dict) else runtime.quality_assurance_empty_state()

    def save_state(self, tenant: str, state: dict) -> dict:
        self.connection.execute(
            f"""
            INSERT INTO {STATE_TABLE} (tenant, state_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(tenant) DO UPDATE SET state_json = excluded.state_json, updated_at = excluded.updated_at
            """,
            (tenant, _json(state), _now()),
        )
        self._sync_read_model(tenant, state)
        self.connection.commit()
        return {"ok": True, "tenant": tenant, "updated_at": _now()}

    def _sync_read_model(self, tenant: str, state: dict) -> None:
        plans = tuple(item for item in state.get("plans", {}).values() if item.get("tenant") == tenant)
        results = tuple(item for item in state.get("results", {}).values() if item.get("tenant") == tenant)
        holds = tuple(item for item in state.get("holds", {}).values() if item.get("tenant") == tenant)
        ncs = tuple(item for item in state.get("nonconformances", {}).values() if item.get("tenant") == tenant)
        payload = runtime.quality_assurance_build_workbench_view(state, tenant=tenant) if state.get("configuration") else {"ok": True, "tenant": tenant}
        row = {
            "read_model_id": f"{tenant}:workbench",
            "tenant": tenant,
            "plan_count": len(plans),
            "result_count": len(results),
            "hold_count": len(holds),
            "open_nc_count": len(tuple(item for item in ncs if item.get("status") != "closed")),
            "released_hold_count": len(tuple(item for item in holds if item.get("status") == "released")),
            "failed_result_count": len(tuple(item for item in results if item.get("decision") == "fail")),
            "cpk_minimum": float(state.get("parameters", {}).get("cpk_minimum", 0)),
            "payload_json": _json(payload),
            "updated_at": _now(),
        }
        self.connection.execute(f"DELETE FROM {READ_MODEL_TABLE} WHERE tenant = ?", (tenant,))
        self.connection.execute(
            f"INSERT INTO {READ_MODEL_TABLE} ({', '.join(row)}) VALUES ({', '.join('?' for _ in row)})",
            tuple(row.values()),
        )

    def _tenant(self, payload: dict | None = None, default: str = "tenant_demo") -> str:
        payload = payload or {}
        return str(payload.get("tenant") or default)

    def _record_form(self, tenant: str, form_key: str, action: str, payload: dict, result: dict, subject_id: str | None = None) -> None:
        count = self.connection.execute(f"SELECT COUNT(*) FROM {FORM_TABLE}").fetchone()[0]
        self.connection.execute(
            f"INSERT INTO {FORM_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (f"form_{count + 1:05d}", tenant, form_key, action, subject_id, _json(payload), _json(result), _now()),
        )

    def _record_workflow(self, tenant: str, wizard_key: str, context: dict, result: dict, subject_id: str | None = None) -> None:
        count = self.connection.execute(f"SELECT COUNT(*) FROM {WORKFLOW_TABLE}").fetchone()[0]
        self.connection.execute(
            f"INSERT INTO {WORKFLOW_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (f"workflow_{count + 1:05d}", tenant, wizard_key, subject_id, "completed" if result.get("ok") else "blocked", _json(context), _json(result), _now()),
        )

    def _record_control(self, tenant: str, control_key: str, result: dict) -> None:
        count = self.connection.execute(f"SELECT COUNT(*) FROM {CONTROL_TABLE}").fetchone()[0]
        self.connection.execute(
            f"INSERT INTO {CONTROL_TABLE} VALUES (?, ?, ?, ?, ?, ?)",
            (f"control_{count + 1:05d}", tenant, control_key, int(bool(result.get("ok"))), _json(result), _now()),
        )

    def _result(self, tenant: str, result: dict) -> dict:
        if result.get("ok") is True and "state" in result:
            self.save_state(tenant, result["state"])
        return result

    def configure_runtime(self, tenant: str, configuration: dict) -> dict:
        result = runtime.quality_assurance_configure_runtime(self.load_state(tenant), {**configuration, "allowed_sites": tuple(configuration.get("allowed_sites", ())), "allowed_inspection_sources": tuple(configuration.get("allowed_inspection_sources", ())), "allowed_hold_reasons": tuple(configuration.get("allowed_hold_reasons", ())), "allowed_dispositions": tuple(configuration.get("allowed_dispositions", ()))})
        self._record_form(tenant, "QualityConfigurationForm", "configure_runtime", configuration, result)
        return self._result(tenant, result)

    def set_parameter(self, tenant: str, name: str, value: float) -> dict:
        result = runtime.quality_assurance_set_parameter(self.load_state(tenant), name, value)
        self._record_form(tenant, "QualityParameterForm", "set_parameter", {"name": name, "value": value}, result, name)
        return self._result(tenant, result)

    def register_rule(self, tenant: str, rule: dict) -> dict:
        result = runtime.quality_assurance_register_rule(self.load_state(tenant), rule)
        self._record_form(tenant, "QualityRuleForm", "register_rule", rule, result, rule.get("rule_id"))
        return self._result(tenant, result)

    def create_inspection_plan(self, tenant: str, plan: dict) -> dict:
        result = runtime.quality_assurance_create_inspection_plan(self.load_state(tenant), plan)
        self._record_form(tenant, "InspectionPlanForm", "create_inspection_plan", plan, result, plan.get("plan_id"))
        return self._result(tenant, result)

    def record_inspection_result(self, tenant: str, result_payload: dict) -> dict:
        result = runtime.quality_assurance_record_inspection_result(self.load_state(tenant), result_payload)
        self._record_form(tenant, "InspectionResultForm", "record_inspection_result", result_payload, result, result_payload.get("result_id"))
        return self._result(tenant, result)

    def create_quality_hold(self, tenant: str, hold: dict) -> dict:
        result = runtime.quality_assurance_create_quality_hold(self.load_state(tenant), hold)
        self._record_form(tenant, "QualityHoldForm", "create_quality_hold", hold, result, hold.get("hold_id"))
        return self._result(tenant, result)

    def raise_nonconformance(self, tenant: str, nonconformance: dict) -> dict:
        result = runtime.quality_assurance_raise_nonconformance(self.load_state(tenant), nonconformance)
        self._record_form(tenant, "NonConformanceForm", "raise_nonconformance", nonconformance, result, nonconformance.get("nonconformance_id"))
        return self._result(tenant, result)

    def disposition_nonconformance(self, tenant: str, nonconformance_id: str, disposition: str, approved_by: str) -> dict:
        result = runtime.quality_assurance_disposition_nonconformance(self.load_state(tenant), nonconformance_id, disposition=disposition, approved_by=approved_by)
        self._record_workflow(tenant, "NonConformanceDispositionWizard", {"nonconformance_id": nonconformance_id, "disposition": disposition}, result, nonconformance_id)
        return self._result(tenant, result)

    def release_quality_hold(self, tenant: str, hold_id: str, released_by: str) -> dict:
        result = runtime.quality_assurance_release_quality_hold(self.load_state(tenant), hold_id, released_by=released_by)
        self._record_workflow(tenant, "HoldReleaseWizard", {"hold_id": hold_id, "released_by": released_by}, result, hold_id)
        return self._result(tenant, result)

    def run_control_tests(self, tenant: str) -> dict:
        result = runtime.quality_assurance_run_control_tests(self.load_state(tenant))
        self._record_control(tenant, "quality_release_controls", result)
        self.connection.commit()
        return result

    def generate_quality_proof(self, tenant: str, result_id: str, disclosure: tuple[str, ...]) -> dict:
        result = runtime.quality_assurance_generate_quality_proof(self.load_state(tenant), result_id, disclosure=tuple(disclosure))
        self._record_control(tenant, "quality_proof", result)
        self.connection.commit()
        return result

    def run_agent_skill(self, tenant: str, skill_name: str, payload: dict) -> dict:
        from . import agent

        plan = agent.document_instruction_plan(payload.get("document"), payload.get("instructions"))
        result = {"ok": plan["ok"], "skill_name": skill_name, "plan": plan, "requires_confirmation": True}
        count = self.connection.execute(f"SELECT COUNT(*) FROM {AGENT_TABLE}").fetchone()[0]
        self.connection.execute(
            f"INSERT INTO {AGENT_TABLE} VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (f"agent_{count + 1:05d}", tenant, skill_name, payload.get("scope", "quality"), 1, _json(payload), _json(result), _now()),
        )
        self.connection.commit()
        return result

    def build_workbench(self, tenant: str) -> dict:
        state = self.load_state(tenant)
        workbench = runtime.quality_assurance_build_workbench_view(state, tenant=tenant)
        counts = self.activity_counts(tenant)
        return {"ok": True, **workbench, "activity_counts": counts, "read_model": self.read_model(tenant)}

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
        plan = self.create_inspection_plan(tenant, bundle["inspection_plan"])
        result = self.record_inspection_result(tenant, bundle["inspection_result"])
        hold = self.create_quality_hold(tenant, bundle["quality_hold"])
        nc = self.raise_nonconformance(tenant, bundle["nonconformance"])
        disposition = self.disposition_nonconformance(tenant, bundle["nonconformance"]["nonconformance_id"], disposition="rework", approved_by="qa_manager")
        release = self.release_quality_hold(tenant, bundle["quality_hold"]["hold_id"], released_by="qa_manager")
        controls = self.run_control_tests(tenant)
        proof = self.generate_quality_proof(tenant, bundle["inspection_result"]["result_id"], ("result_id", "lot_id", "decision"))
        agent = self.run_agent_skill(tenant, "quality_assurance.document_instruction_intake", {"document": bundle["document"], "instructions": bundle["instructions"], "scope": "seed"})
        return {"ok": all(item.get("ok") for item in (plan, result, hold, nc, disposition, release, controls, proof, agent)), "tenant": tenant, "bundle": bundle, "workbench": self.build_workbench(tenant)}


def standalone_repository_contract() -> dict:
    return {
        "format": "appgen.quality-assurance-standalone-repository.v1",
        "ok": True,
        "pbc": PBC_KEY,
        "repository_class": "QualityAssuranceStandaloneRepository",
        "local_harness_backend": "sqlite3",
        "deployment_database_backends": runtime.QUALITY_ASSURANCE_ALLOWED_DATABASE_BACKENDS,
        "tables": (STATE_TABLE, FORM_TABLE, WORKFLOW_TABLE, CONTROL_TABLE, AGENT_TABLE, READ_MODEL_TABLE),
        "side_effects": (),
    }


def standalone_repository_smoke_test() -> dict:
    repo = QualityAssuranceStandaloneRepository()
    try:
        seeded = repo.seed_demo_workspace()
        return {"ok": seeded["ok"] and repo.read_model("tenant_demo")["ok"], "seeded": seeded, "contract": standalone_repository_contract(), "side_effects": ()}
    finally:
        repo.close()
