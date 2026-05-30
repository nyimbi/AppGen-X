"""Executable service layer for the workflow_orchestration PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from .repository import WorkflowOrchestrationRepository
from .repository import repository_snapshot
from .runtime import workflow_orchestration_append_audit_entry
from .runtime import workflow_orchestration_assign_human_task
from .runtime import workflow_orchestration_build_api_contract
from .runtime import workflow_orchestration_build_schema_contract
from .runtime import workflow_orchestration_build_service_contract
from .runtime import workflow_orchestration_build_workbench_view
from .runtime import workflow_orchestration_capture_metric_snapshot
from .runtime import workflow_orchestration_complete_workflow
from .runtime import workflow_orchestration_configure_runtime
from .runtime import workflow_orchestration_correlate_event
from .runtime import workflow_orchestration_define_workflow
from .runtime import workflow_orchestration_empty_state
from .runtime import workflow_orchestration_execute_compensation
from .runtime import workflow_orchestration_open_exception_case
from .runtime import workflow_orchestration_permissions_contract
from .runtime import workflow_orchestration_publish_workflow_version
from .runtime import workflow_orchestration_record_approval_decision
from .runtime import workflow_orchestration_record_completion_proof
from .runtime import workflow_orchestration_record_policy_screening
from .runtime import workflow_orchestration_record_simulation_run
from .runtime import workflow_orchestration_record_step_result
from .runtime import workflow_orchestration_receive_event
from .runtime import workflow_orchestration_register_escalation_rule
from .runtime import workflow_orchestration_register_governed_model_evidence
from .runtime import workflow_orchestration_register_integration_endpoint
from .runtime import workflow_orchestration_register_retry_policy
from .runtime import workflow_orchestration_register_rule
from .runtime import workflow_orchestration_register_schema_extension
from .runtime import workflow_orchestration_register_sla_policy
from .runtime import workflow_orchestration_register_transition_guard
from .runtime import workflow_orchestration_runtime_capabilities
from .runtime import workflow_orchestration_runtime_smoke
from .runtime import workflow_orchestration_schedule_timer
from .runtime import workflow_orchestration_set_parameter
from .runtime import workflow_orchestration_signal_instance
from .runtime import workflow_orchestration_start_instance


PBC_KEY = "workflow_orchestration"


def _route_to_contract(route: dict) -> dict:
    method, path = route["route"].split(" ", 1)
    operation = route.get("command") or route.get("query")
    operation_kind = "command" if route.get("command") else "query"
    owned_tables = tuple(
        table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        for table in route.get("owned_tables", ())
    )
    if operation_kind == "command" and not owned_tables:
        owned_tables = (EVENT_CONTRACT["inbox_table"],)
    return {
        "operation": operation,
        "operation_kind": operation_kind,
        "method": method,
        "path": f"/api/pbc/{PBC_KEY}{path}",
        "permission": route["requires_permission"],
        "owned_tables": owned_tables if operation_kind == "command" else (),
        "read_tables": () if operation_kind == "command" else owned_tables,
        "emitted_event": (route.get("emits") or (f"{PBC_KEY}.{operation}.executed",))[0] if operation_kind == "command" else None,
        "consumed_event": tuple(route.get("consumes", ())),
        "idempotency_key": route.get("idempotency_key"),
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
    }


OPERATION_CONTRACTS = tuple(_route_to_contract(route) for route in workflow_orchestration_build_api_contract()["routes"])


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = workflow_orchestration_build_service_contract()
    return {
        "ok": runtime_service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] or item["consumed_event"] for item in command_contracts)
        and all(item["read_tables"] for item in query_contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "runtime_service_contract": runtime_service,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": bool(contract["owned_tables"] or contract["read_tables"] or contract["consumed_event"]),
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "consumed_event": contract["consumed_event"],
        "idempotency_key": contract["idempotency_key"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


class WorkflowOrchestrationService:
    """Executable package-local service facade over workflow runtime state."""

    def __init__(self, state: dict | None = None):
        self.state = state or workflow_orchestration_empty_state()
        self.repository = WorkflowOrchestrationRepository(self.state)

    def _sync(self, result: dict) -> dict:
        if "state" in result:
            self.state = result["state"]
            self.repository.sync_state(self.state)
        return result

    def _command(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        result = self._sync(self._apply_command(operation_name, payload))
        return {
            "ok": result.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": "command",
            "payload": payload,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (plan["emitted_event"],) if plan.get("emitted_event") else (),
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def _query(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        result = self._apply_query(operation_name, payload)
        return {
            "ok": result.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": "query",
            "payload": payload,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "emits": (),
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def _apply_command(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "configure_runtime":
            return workflow_orchestration_configure_runtime(self.state, payload["configuration"])
        if operation_name == "set_parameter":
            return workflow_orchestration_set_parameter(self.state, payload["name"], payload["value"])
        if operation_name == "register_rule":
            return workflow_orchestration_register_rule(self.state, payload["rule"])
        if operation_name == "register_schema_extension":
            return workflow_orchestration_register_schema_extension(self.state, payload["target"], payload["fields"])
        if operation_name == "receive_event":
            return workflow_orchestration_receive_event(self.state, payload["envelope"], simulate_failure=payload.get("simulate_failure", False))
        if operation_name == "define_workflow":
            return workflow_orchestration_define_workflow(self.state, payload["workflow"])
        if operation_name == "publish_workflow_version":
            return workflow_orchestration_publish_workflow_version(self.state, payload["version"])
        if operation_name == "register_transition_guard":
            return workflow_orchestration_register_transition_guard(self.state, payload["guard"])
        if operation_name == "start_instance":
            return workflow_orchestration_start_instance(self.state, payload["instance"])
        if operation_name == "signal_instance":
            return workflow_orchestration_signal_instance(self.state, payload["instance_id"], payload["signal"])
        if operation_name == "schedule_timer":
            return workflow_orchestration_schedule_timer(self.state, payload["timer"])
        if operation_name == "register_retry_policy":
            return workflow_orchestration_register_retry_policy(self.state, payload["policy"])
        if operation_name == "register_sla_policy":
            return workflow_orchestration_register_sla_policy(self.state, payload["policy"])
        if operation_name == "register_escalation_rule":
            return workflow_orchestration_register_escalation_rule(self.state, payload["rule"])
        if operation_name == "record_step_result":
            return workflow_orchestration_record_step_result(self.state, payload["step"])
        if operation_name == "execute_compensation":
            return workflow_orchestration_execute_compensation(self.state, payload["compensation"])
        if operation_name == "assign_human_task":
            return workflow_orchestration_assign_human_task(self.state, payload["assignment"])
        if operation_name == "record_approval_decision":
            return workflow_orchestration_record_approval_decision(self.state, payload["decision"])
        if operation_name == "register_integration_endpoint":
            return workflow_orchestration_register_integration_endpoint(self.state, payload["endpoint"])
        if operation_name == "correlate_event":
            return workflow_orchestration_correlate_event(self.state, payload["correlation"])
        if operation_name == "capture_metric_snapshot":
            return workflow_orchestration_capture_metric_snapshot(self.state, payload["snapshot"])
        if operation_name == "open_exception_case":
            return workflow_orchestration_open_exception_case(self.state, payload["case"])
        if operation_name == "record_simulation_run":
            return workflow_orchestration_record_simulation_run(self.state, payload["simulation"])
        if operation_name == "record_policy_screening":
            return workflow_orchestration_record_policy_screening(self.state, payload["screening"])
        if operation_name == "record_completion_proof":
            return workflow_orchestration_record_completion_proof(self.state, payload["proof"])
        if operation_name == "append_audit_entry":
            return workflow_orchestration_append_audit_entry(self.state, payload["action"], payload["entry_payload"])
        if operation_name == "register_governed_model_evidence":
            return workflow_orchestration_register_governed_model_evidence(self.state, payload["evidence"])
        if operation_name == "complete_workflow":
            return workflow_orchestration_complete_workflow(self.state, payload["instance_id"])
        raise ValueError(f"Unsupported workflow_orchestration command: {operation_name}")

    def _apply_query(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "build_workbench_view":
            tenant = payload.get("tenant", "tenant_demo")
            workbench = workflow_orchestration_build_workbench_view(self.state, tenant=tenant)
            return {
                "ok": True,
                "workbench": workbench,
                "repository": self.repository.snapshot(tenant=tenant),
                "permissions": workflow_orchestration_permissions_contract(),
            }
        if operation_name == "build_schema_contract":
            return workflow_orchestration_build_schema_contract()
        if operation_name == "build_service_contract":
            return workflow_orchestration_build_service_contract()
        if operation_name == "build_release_evidence":
            from . import release_evidence

            return release_evidence.build_release_evidence()
        raise ValueError(f"Unsupported workflow_orchestration query: {operation_name}")

    def __getattr__(self, operation_name: str):
        contracts = service_operation_contracts()
        if operation_name in contracts["command_operations"]:
            return lambda payload=None: self._command(operation_name, payload)
        if operation_name in contracts["query_operations"]:
            return lambda payload=None: self._query(operation_name, payload)
        raise AttributeError(operation_name)


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": WorkflowOrchestrationService.__name__,
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "repository": repository_snapshot()["repository"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute configuration, core commands, and package queries through the facade."""
    service = WorkflowOrchestrationService()
    service.configure_runtime(
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": "appgen.workflow.events",
                "retry_limit": 3,
                "allowed_signal_sources": ("api_gateway_mesh", "schema_registry"),
                "default_versioning": "semantic",
                "default_timezone": "UTC",
                "workbench_limit": 100,
            }
        }
    )
    service.set_parameter({"name": "default_retry_limit", "value": 3})
    service.set_parameter({"name": "timer_jitter_seconds", "value": 30})
    service.register_rule(
        {
            "rule": {
                "rule_id": "workflow.demo.release_gate",
                "tenant": "tenant_demo",
                "scope": "release_gate",
                "trigger": "publish",
                "allowed_signals": ("approve", "reject"),
                "requires_compensation": True,
                "severity": "blocking",
                "status": "active",
            }
        }
    )
    service.define_workflow(
        {
            "workflow": {
                "workflow_id": "invoice_recovery",
                "tenant": "tenant_demo",
                "owner_pbc": "billing",
                "version": "1.0.0",
                "states": ("draft", "awaiting_approval", "recovered", "completed"),
                "transitions": (("draft", "submit", "awaiting_approval"), ("awaiting_approval", "recover", "recovered"), ("recovered", "complete", "completed")),
                "participants": ("invoice_management", "collections_ops"),
            }
        }
    )
    service.publish_workflow_version(
        {
            "version": {
                "version_id": "invoice_recovery_v1",
                "tenant": "tenant_demo",
                "workflow_id": "invoice_recovery",
                "semantic_version": "1.0.0",
                "status": "published",
            }
        }
    )
    service.register_transition_guard(
        {
            "guard": {
                "guard_id": "invoice_guard_recover",
                "tenant": "tenant_demo",
                "workflow_id": "invoice_recovery",
                "from_state": "awaiting_approval",
                "signal": "recover",
                "expression": "context.amount_due > 0",
                "status": "active",
            }
        }
    )
    service.start_instance(
        {
            "instance": {
                "instance_id": "invoice_recovery_instance_1",
                "tenant": "tenant_demo",
                "workflow_id": "invoice_recovery",
                "correlation_id": "inv-1",
                "context": {"invoice_id": "inv-1", "amount_due": 1500},
            }
        }
    )
    service.signal_instance(
        {
            "instance_id": "invoice_recovery_instance_1",
            "signal": {
                "signal": "submit",
                "source_pbc": "invoice_management",
                "payload": {"submitted_by": "collections_agent"},
            },
        }
    )
    workbench = service.build_workbench_view({"tenant": "tenant_demo"})
    release = service.build_release_evidence({})
    repository = repository_snapshot(service.state, tenant="tenant_demo")
    runtime_smoke = workflow_orchestration_runtime_smoke()
    capabilities = workflow_orchestration_runtime_capabilities()
    return {
        "ok": workbench["ok"]
        and release["ok"]
        and repository["ok"]
        and runtime_smoke["ok"]
        and capabilities["ok"],
        "service": service_operation_manifest(),
        "result": workbench,
        "workbench": workbench,
        "release": release,
        "repository": repository,
        "runtime_smoke": runtime_smoke,
        "capabilities": capabilities,
        "side_effects": (),
    }
