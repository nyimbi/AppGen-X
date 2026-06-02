"""Repository and table-binding helpers for workflow_orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from .runtime import WORKFLOW_ORCHESTRATION_OWNED_TABLES
from .runtime import WORKFLOW_ORCHESTRATION_RUNTIME_TABLES
from .runtime import workflow_orchestration_empty_state


PBC_KEY = "workflow_orchestration"
TABLE_PREFIX = f"{PBC_KEY}_"


@dataclass(frozen=True)
class TableBinding:
    """Describe how one owned table maps to runtime state."""

    logical_table: str
    table: str
    state_key: str
    primary_key: str
    runtime_table: bool = False


TABLE_BINDINGS = (
    TableBinding("workflow_definition", f"{TABLE_PREFIX}workflow_definition", "definitions", "workflow_id"),
    TableBinding("workflow_version", f"{TABLE_PREFIX}workflow_version", "workflow_versions", "version_id"),
    TableBinding("workflow_instance", f"{TABLE_PREFIX}workflow_instance", "instances", "instance_id"),
    TableBinding("workflow_signal", f"{TABLE_PREFIX}workflow_signal", "signals", "signal_id"),
    TableBinding("workflow_transition_guard", f"{TABLE_PREFIX}workflow_transition_guard", "workflow_transition_guards", "guard_id"),
    TableBinding("timer_task", f"{TABLE_PREFIX}timer_task", "timers", "timer_id"),
    TableBinding("workflow_retry_policy", f"{TABLE_PREFIX}workflow_retry_policy", "workflow_retry_policies", "policy_id"),
    TableBinding("workflow_sla_policy", f"{TABLE_PREFIX}workflow_sla_policy", "workflow_sla_policies", "policy_id"),
    TableBinding("workflow_escalation_rule", f"{TABLE_PREFIX}workflow_escalation_rule", "workflow_escalation_rules", "escalation_id"),
    TableBinding("saga_step", f"{TABLE_PREFIX}saga_step", "saga_steps", "step_id"),
    TableBinding("compensation", f"{TABLE_PREFIX}compensation", "compensations", "compensation_id"),
    TableBinding("human_task", f"{TABLE_PREFIX}human_task", "human_tasks", "task_id"),
    TableBinding("human_task_assignment", f"{TABLE_PREFIX}human_task_assignment", "human_task_assignments", "assignment_id"),
    TableBinding("workflow_approval_decision", f"{TABLE_PREFIX}workflow_approval_decision", "workflow_approval_decisions", "decision_id"),
    TableBinding("workflow_integration_endpoint", f"{TABLE_PREFIX}workflow_integration_endpoint", "workflow_integration_endpoints", "endpoint_id"),
    TableBinding("workflow_event_correlation", f"{TABLE_PREFIX}workflow_event_correlation", "workflow_event_correlations", "correlation_id"),
    TableBinding("workflow_metric_snapshot", f"{TABLE_PREFIX}workflow_metric_snapshot", "workflow_metric_snapshots", "snapshot_id"),
    TableBinding("workflow_exception_case", f"{TABLE_PREFIX}workflow_exception_case", "workflow_exception_cases", "case_id"),
    TableBinding("workflow_simulation_run", f"{TABLE_PREFIX}workflow_simulation_run", "workflow_simulation_runs", "simulation_id"),
    TableBinding("workflow_policy_screening", f"{TABLE_PREFIX}workflow_policy_screening", "workflow_policy_screenings", "screening_id"),
    TableBinding("workflow_completion_proof", f"{TABLE_PREFIX}workflow_completion_proof", "workflow_completion_proofs", "proof_id"),
    TableBinding("workflow_audit_entry", f"{TABLE_PREFIX}workflow_audit_entry", "workflow_audit_entries", "audit_entry_id"),
    TableBinding("workflow_governed_model_evidence", f"{TABLE_PREFIX}workflow_governed_model_evidence", "workflow_governed_model_evidence", "evidence_id"),
    TableBinding("workflow_rule", f"{TABLE_PREFIX}workflow_rule", "rules", "rule_id"),
    TableBinding("workflow_parameter", f"{TABLE_PREFIX}workflow_parameter", "parameters", "parameter_name"),
    TableBinding("workflow_configuration", f"{TABLE_PREFIX}workflow_configuration", "configuration", "configuration_id"),
    TableBinding("workflow_orchestration_appgen_outbox_event", WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[0], "outbox", "event_id", runtime_table=True),
    TableBinding("workflow_orchestration_appgen_inbox_event", WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[1], "inbox", "event_id", runtime_table=True),
    TableBinding("workflow_orchestration_dead_letter_event", WORKFLOW_ORCHESTRATION_RUNTIME_TABLES[2], "dead_letter", "event_id", runtime_table=True),
)


def _binding_for_table(table: str) -> TableBinding | None:
    normalized = table if table.startswith(TABLE_PREFIX) else f"{TABLE_PREFIX}{table}"
    return next((binding for binding in TABLE_BINDINGS if binding.table == normalized), None)


def _normalize_rows(binding: TableBinding, state: dict) -> tuple[dict, ...]:
    bucket = state.get(binding.state_key)
    if binding.logical_table == "workflow_parameter":
        return tuple(
            {
                "parameter_name": name,
                "parameter_value": value,
                "tenant": "tenant_demo",
                "effective_at": "1970-01-01T00:00:00Z",
                "changed_by": "system",
            }
            for name, value in sorted((bucket or {}).items())
        )
    if binding.logical_table == "workflow_configuration":
        if not bucket:
            return ()
        return (
            {
                "configuration_id": "workflow_orchestration.default",
                "tenant": "tenant_demo",
                **dict(bucket),
            },
        )
    if binding.logical_table == "workflow_orchestration_dead_letter_event":
        dead_letter_rows = state.get("dead_letter") or state.get("dead_letters") or ()
        return tuple(dict(row) for row in dead_letter_rows)
    if isinstance(bucket, dict):
        return tuple(dict(row) for row in bucket.values())
    if isinstance(bucket, (list, tuple)):
        return tuple(dict(row) if isinstance(row, dict) else {"value": row} for row in bucket)
    return ()


def workflow_orchestration_repository_contract() -> dict:
    """Return the database-backed repository contract for this package."""
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "backend": "owned_relational_tables",
        "table_prefix": TABLE_PREFIX,
        "owned_tables": tuple(f"{TABLE_PREFIX}{table}" for table in WORKFLOW_ORCHESTRATION_OWNED_TABLES),
        "runtime_tables": WORKFLOW_ORCHESTRATION_RUNTIME_TABLES,
        "bindings": tuple(
            {
                "logical_table": binding.logical_table,
                "table": binding.table,
                "state_key": binding.state_key,
                "primary_key": binding.primary_key,
                "runtime_table": binding.runtime_table,
            }
            for binding in TABLE_BINDINGS
        ),
        "shared_table_access": False,
        "side_effects": (),
    }


class WorkflowOrchestrationRepository:
    """In-package repository facade over the standalone runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or workflow_orchestration_empty_state()

    def sync_state(self, state: dict) -> dict:
        self.state = state
        return {"ok": True, "state": self.state, "side_effects": ()}

    def table_rows(self, table: str, *, tenant: str | None = None) -> tuple[dict, ...]:
        binding = _binding_for_table(table)
        if binding is None:
            return ()
        rows = _normalize_rows(binding, self.state)
        if tenant is None:
            return rows
        return tuple(row for row in rows if row.get("tenant") in {None, tenant})

    def table_count(self, table: str, *, tenant: str | None = None) -> int:
        return len(self.table_rows(table, tenant=tenant))

    def snapshot(self, *, tenant: str | None = None) -> dict:
        rows = tuple(
            {
                "table": binding.table,
                "logical_table": binding.logical_table,
                "row_count": self.table_count(binding.table, tenant=tenant),
                "primary_key": binding.primary_key,
                "runtime_table": binding.runtime_table,
            }
            for binding in TABLE_BINDINGS
        )
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "tenant": tenant,
            "tables": rows,
            "non_empty_tables": tuple(row["table"] for row in rows if row["row_count"] > 0),
            "side_effects": (),
        }


def repository_snapshot(state: dict | None = None, *, tenant: str | None = None) -> dict:
    repository = WorkflowOrchestrationRepository(state)
    snapshot = repository.snapshot(tenant=tenant)
    return {
        "ok": snapshot["ok"],
        "pbc": PBC_KEY,
        "repository": workflow_orchestration_repository_contract(),
        "snapshot": snapshot,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise repository bindings against a deterministic runtime state."""
    state = workflow_orchestration_empty_state()
    state["configuration"] = {
        "database_backend": "postgresql",
        "event_topic": "appgen.workflow.events",
        "event_contract": "AppGen-X",
    }
    state["definitions"]["workflow-demo"] = {
        "workflow_id": "workflow-demo",
        "tenant": "tenant_demo",
        "owner_pbc": "order_management",
        "version": "1.0.0",
        "states": ("draft", "completed"),
        "transitions": (("draft", "complete", "completed"),),
        "participants": ("payment_orchestration",),
        "status": "active",
    }
    state["instances"]["instance-demo"] = {
        "instance_id": "instance-demo",
        "tenant": "tenant_demo",
        "workflow_id": "workflow-demo",
        "current_state": "draft",
        "status": "running",
    }
    repository = WorkflowOrchestrationRepository(state)
    definition_rows = repository.table_rows("workflow_definition", tenant="tenant_demo")
    snapshot = repository.snapshot(tenant="tenant_demo")
    return {
        "ok": bool(definition_rows) and snapshot["ok"] and f"{TABLE_PREFIX}workflow_definition" in snapshot["non_empty_tables"],
        "repository": workflow_orchestration_repository_contract(),
        "definition_rows": definition_rows,
        "snapshot": snapshot,
        "side_effects": (),
    }
