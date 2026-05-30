"""Standalone one-PBC application surface for the Port Terminal Operations package."""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any

from .agent import standalone_agent_workspace_contract
from .controls import port_terminal_operations_control_catalog
from .domain_depth import DOMAIN_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES
from .domain_depth import execute_domain_operation
from .forms import port_terminal_operations_form_contracts
from .runtime import PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS
from .runtime import PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC
from .runtime import port_terminal_operations_build_workbench_view
from .runtime import port_terminal_operations_command_vessel_call
from .runtime import port_terminal_operations_configure_runtime
from .runtime import port_terminal_operations_empty_state
from .runtime import port_terminal_operations_parse_document_instruction
from .runtime import port_terminal_operations_register_rule
from .runtime import port_terminal_operations_run_advanced_assessment
from .runtime import port_terminal_operations_set_parameter
from .wizards import port_terminal_operations_wizard_contracts

PBC_KEY = "port_terminal_operations"

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "retry_limit": 5,
    "default_policy": "terminal_default",
    "tenant_isolation": "strict",
    "workbench_limit": 100,
}

DEFAULT_PARAMETERS = {
    "quality_score_floor": 0.85,
    "materiality_threshold": 0.15,
    "approval_sla_hours": 4,
    "risk_threshold": 0.7,
    "forecast_horizon_days": 14,
    "workbench_limit": 100,
}

DEFAULT_RULES = (
    {
        "rule_id": "port_terminal_operations.vessel_call.default",
        "scope": "vessel_call",
        "status": "active",
        "requires_eta_confidence": True,
        "minimum_eta_confidence": 0.65,
    },
    {
        "rule_id": "port_terminal_operations.berth_plan.default",
        "scope": "berth_plan",
        "status": "active",
        "checks": ("loa", "draft", "tide", "crane_overlap"),
    },
    {
        "rule_id": "port_terminal_operations.gate.default",
        "scope": "gate_transaction",
        "status": "active",
        "requires_customs_release": True,
        "enforces_appointment_window": True,
    },
)

STANDALONE_ROUTE_CONTRACTS = (
    {
        "operation": "create_vessel_call",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/vessel-calls",
        "handler": "create_vessel_call",
        "permission": "port_terminal_operations.create",
        "table": "port_terminal_operations_vessel_call",
        "form": "PortTerminalVesselCallForm",
        "wizard": "VesselArrivalNominationWizard",
    },
    {
        "operation": "record_berth_plan",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/berth-plans",
        "handler": "record_berth_plan",
        "permission": "port_terminal_operations.update",
        "table": "port_terminal_operations_berth_plan",
        "form": "PortTerminalBerthPlanForm",
        "wizard": "VesselArrivalNominationWizard",
    },
    {
        "operation": "review_container_move",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/container-moves",
        "handler": "review_container_move",
        "permission": "port_terminal_operations.update",
        "table": "port_terminal_operations_container_move",
        "form": "PortTerminalContainerMoveForm",
        "wizard": "ContainerFlowExceptionWizard",
    },
    {
        "operation": "approve_yard_slot",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/yard-slots",
        "handler": "approve_yard_slot",
        "permission": "port_terminal_operations.approve",
        "table": "port_terminal_operations_yard_slot",
        "form": "PortTerminalYardSlotForm",
        "wizard": "ContainerFlowExceptionWizard",
    },
    {
        "operation": "simulate_gate_transaction",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/gate-transactions",
        "handler": "simulate_gate_transaction",
        "permission": "port_terminal_operations.update",
        "table": "port_terminal_operations_gate_transaction",
        "form": "PortTerminalGateTransactionForm",
        "wizard": "ContainerFlowExceptionWizard",
    },
    {
        "operation": "create_terminal_equipment",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/terminal-equipment",
        "handler": "create_terminal_equipment",
        "permission": "port_terminal_operations.create",
        "table": "port_terminal_operations_terminal_equipment",
        "form": "PortTerminalEquipmentDispatchForm",
        "wizard": "EquipmentFallbackDispatchWizard",
    },
    {
        "operation": "record_customs_handoff",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/customs-handoffs",
        "handler": "record_customs_handoff",
        "permission": "port_terminal_operations.update",
        "table": "port_terminal_operations_customs_handoff",
        "form": "PortTerminalCustomsHandoffForm",
        "wizard": "ContainerFlowExceptionWizard",
    },
    {
        "operation": "review_port_terminal_operations_policy_rule",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/policy-rules",
        "handler": "review_port_terminal_operations_policy_rule",
        "permission": "port_terminal_operations.admin",
        "table": "port_terminal_operations_port_terminal_operations_policy_rule",
        "form": "PortTerminalPolicyRuleForm",
        "wizard": "DocumentInstructionIntakeWizard",
    },
    {
        "operation": "approve_port_terminal_operations_runtime_parameter",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/runtime-parameters",
        "handler": "approve_port_terminal_operations_runtime_parameter",
        "permission": "port_terminal_operations.admin",
        "table": "port_terminal_operations_port_terminal_operations_runtime_parameter",
        "form": "PortTerminalRuntimeParameterForm",
        "wizard": "DocumentInstructionIntakeWizard",
    },
    {
        "operation": "simulate_port_terminal_operations_schema_extension",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/schema-extensions",
        "handler": "simulate_port_terminal_operations_schema_extension",
        "permission": "port_terminal_operations.admin",
        "table": "port_terminal_operations_port_terminal_operations_schema_extension",
        "form": "PortTerminalSchemaExtensionForm",
        "wizard": "ReleaseReadinessWizard",
    },
    {
        "operation": "create_port_terminal_operations_control_assertion",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/control-assertions",
        "handler": "create_port_terminal_operations_control_assertion",
        "permission": "port_terminal_operations.approve",
        "table": "port_terminal_operations_port_terminal_operations_control_assertion",
        "form": "PortTerminalControlAssertionForm",
        "wizard": "ReleaseReadinessWizard",
    },
    {
        "operation": "record_port_terminal_operations_governed_model",
        "operation_kind": "command",
        "method": "POST",
        "path": "/app/port-terminal-operations/governed-models",
        "handler": "record_port_terminal_operations_governed_model",
        "permission": "port_terminal_operations.admin",
        "table": "port_terminal_operations_port_terminal_operations_governed_model",
        "form": "PortTerminalGovernedModelForm",
        "wizard": "ReleaseReadinessWizard",
    },
    {
        "operation": "workbench",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/port-terminal-operations/workbench",
        "handler": "workbench",
        "permission": "port_terminal_operations.read",
        "table": "port_terminal_operations_vessel_call",
        "form": None,
        "wizard": None,
    },
    {
        "operation": "release_readiness",
        "operation_kind": "query",
        "method": "GET",
        "path": "/app/port-terminal-operations/release-readiness",
        "handler": "release_readiness",
        "permission": "port_terminal_operations.admin",
        "table": "port_terminal_operations_port_terminal_operations_control_assertion",
        "form": None,
        "wizard": "ReleaseReadinessWizard",
    },
)


def _copy_payload(payload: dict[str, Any] | None) -> dict[str, Any]:
    return deepcopy(dict(payload or {}))


def _hash_token(*parts: Any) -> str:
    digest = hashlib.sha256(repr(parts).encode("utf-8")).hexdigest()
    return digest


def _ensure_state(state: dict[str, Any] | None) -> dict[str, Any]:
    base = deepcopy(state) if state is not None else port_terminal_operations_empty_state()
    defaults: dict[str, Any] = {
        "table_records": {table: {} for table in DOMAIN_OWNED_TABLES},
        "operation_journal": (),
        "documents": (),
        "release_notes": (),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "records": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }
    for key, default in defaults.items():
        if key not in base:
            base[key] = deepcopy(default)
    if not isinstance(base.get("idempotency_keys"), set):
        base["idempotency_keys"] = set(base.get("idempotency_keys", ()))
    for table in DOMAIN_OWNED_TABLES:
        base["table_records"].setdefault(table, {})
    return base


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_class": "PortTerminalOperationsStandaloneApp",
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "service_methods": tuple(dict.fromkeys(item["handler"] for item in STANDALONE_ROUTE_CONTRACTS))
        + ("configure", "register_defaults", "document_instruction_plan", "advanced_assessment"),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench"),
        "docs": (
            "README.md",
            "SPECIFICATION.md",
            "implementation-plan.md",
            "implementation-status.md",
            "RELEASE_EVIDENCE.md",
        ),
        "event_contract": "AppGen-X",
        "event_topic": PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
        "stream_engine_picker_visible": False,
        "allowed_backends": PORT_TERMINAL_OPERATIONS_ALLOWED_DATABASE_BACKENDS,
    }


class PortTerminalOperationsStandaloneApp:
    """Package-local standalone shell for operating the Port Terminal Operations PBC."""

    def __init__(self, *, tenant: str = "default", state: dict[str, Any] | None = None) -> None:
        self.tenant = tenant
        self.state = _ensure_state(state)

    def snapshot(self) -> dict[str, Any]:
        return deepcopy(self.state)

    def configure(self, configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        candidate = {**DEFAULT_CONFIGURATION, **_copy_payload(configuration)}
        result = port_terminal_operations_configure_runtime(self.state, candidate)
        self.state = _ensure_state(result["state"])
        return {**result, "state": self.snapshot(), "side_effects": ()}

    def register_defaults(self) -> dict[str, Any]:
        if not self.state.get("configuration", {}).get("ok"):
            self.configure()
        parameter_results = []
        for key, value in DEFAULT_PARAMETERS.items():
            parameter_results.append(port_terminal_operations_set_parameter(self.state, key, value))
            self.state = _ensure_state(parameter_results[-1]["state"])
        rule_results = []
        for rule in DEFAULT_RULES:
            rule_results.append(port_terminal_operations_register_rule(self.state, {**rule, "tenant": self.tenant}))
            self.state = _ensure_state(rule_results[-1]["state"])
        return {
            "ok": all(item["ok"] for item in parameter_results + rule_results),
            "parameters": tuple(item["parameter"] for item in parameter_results),
            "rules": tuple(item["rule"] for item in rule_results),
            "state": self.snapshot(),
            "side_effects": (),
        }

    def create_vessel_call(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        candidate = _copy_payload(payload)
        candidate.setdefault("tenant", self.tenant)
        candidate.setdefault("code", candidate.get("vessel_code", "VESSEL-001"))
        result = port_terminal_operations_command_vessel_call(self.state, candidate)
        self.state = _ensure_state(result["state"])
        record = {
            **result["record"],
            "table": "port_terminal_operations_vessel_call",
            "operation": "create_vessel_call",
            "record_id": result["record"]["id"],
        }
        self.state["records"][record["record_id"]] = record
        self.state["table_records"]["port_terminal_operations_vessel_call"][record["record_id"]] = record
        self.state["operation_journal"] = (
            *tuple(self.state.get("operation_journal", ())),
            {"operation": "create_vessel_call", "record_id": record["record_id"], "table": record["table"]},
        )
        return {
            "ok": result["ok"],
            "operation": "create_vessel_call",
            "record": record,
            "event": self.state["outbox"][-1] if self.state.get("outbox") else None,
            "state": self.snapshot(),
            "side_effects": (),
        }

    def _record_domain_operation(self, operation: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        candidate = _copy_payload(payload)
        candidate.setdefault("tenant", self.tenant)
        plan = execute_domain_operation(operation, candidate)
        if not plan["ok"]:
            return {**plan, "state": self.snapshot(), "side_effects": ()}
        record_id = (
            candidate.get("record_id")
            or candidate.get("id")
            or candidate.get("code")
            or f"{operation}_{len(self.state['records']) + 1:05d}"
        )
        table = plan["target_table"]
        record = {
            "record_id": record_id,
            "tenant": candidate["tenant"],
            "operation": operation,
            "table": table,
            "status": candidate.get("status", "planned" if operation.startswith("simulate") else "active"),
            "payload": candidate,
            "event_contract": plan["event_contract"],
            "emitted_event": plan["emitted_event"],
            "evidence_hash": plan["evidence_hash"],
            "idempotency_key": plan["idempotency_key"],
        }
        self.state["records"][record_id] = record
        self.state["table_records"][table][record_id] = record
        self.state["outbox"].append(
            {
                "event_type": plan["emitted_event"],
                "topic": PORT_TERMINAL_OPERATIONS_REQUIRED_EVENT_TOPIC,
                "record_id": record_id,
                "table": table,
                "payload": deepcopy(candidate),
                "idempotency_key": plan["idempotency_key"],
            }
        )
        self.state["operation_journal"] = (
            *tuple(self.state.get("operation_journal", ())),
            {"operation": operation, "record_id": record_id, "table": table, "tenant": candidate["tenant"]},
        )
        return {
            "ok": True,
            "operation": operation,
            "record": record,
            "plan": plan,
            "state": self.snapshot(),
            "side_effects": (),
        }

    def record_berth_plan(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("record_berth_plan", payload)

    def review_container_move(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("review_container_move", payload)

    def approve_yard_slot(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("approve_yard_slot", payload)

    def simulate_gate_transaction(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("simulate_gate_transaction", payload)

    def create_terminal_equipment(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("create_terminal_equipment", payload)

    def record_customs_handoff(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("record_customs_handoff", payload)

    def review_port_terminal_operations_policy_rule(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("review_port_terminal_operations_policy_rule", payload)

    def approve_port_terminal_operations_runtime_parameter(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("approve_port_terminal_operations_runtime_parameter", payload)

    def simulate_port_terminal_operations_schema_extension(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("simulate_port_terminal_operations_schema_extension", payload)

    def create_port_terminal_operations_control_assertion(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("create_port_terminal_operations_control_assertion", payload)

    def record_port_terminal_operations_governed_model(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._record_domain_operation("record_port_terminal_operations_governed_model", payload)

    def workbench(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        request = _copy_payload(payload)
        tenant = request.get("tenant", self.tenant)
        workbench_contract = port_terminal_operations_build_workbench_view(tenant=tenant)
        table_counts = {
            table: sum(1 for record in records.values() if record.get("tenant") == tenant)
            for table, records in self.state.get("table_records", {}).items()
        }
        active_records = tuple(
            record
            for record in self.state.get("records", {}).values()
            if record.get("tenant") == tenant
        )
        summary = {
            "tenant": tenant,
            "record_count": len(active_records),
            "vessel_call_count": table_counts.get("port_terminal_operations_vessel_call", 0),
            "berth_plan_count": table_counts.get("port_terminal_operations_berth_plan", 0),
            "container_move_count": table_counts.get("port_terminal_operations_container_move", 0),
            "yard_slot_count": table_counts.get("port_terminal_operations_yard_slot", 0),
            "gate_transaction_count": table_counts.get("port_terminal_operations_gate_transaction", 0),
            "equipment_count": table_counts.get("port_terminal_operations_terminal_equipment", 0),
            "customs_handoff_count": table_counts.get("port_terminal_operations_customs_handoff", 0),
            "outbox_count": len(self.state.get("outbox", ())),
            "inbox_count": len(self.state.get("inbox", ())),
            "dead_letter_count": len(self.state.get("dead_letter", ())),
            "table_counts": table_counts,
            "records": active_records,
        }
        return {
            "ok": workbench_contract["ok"],
            "operation": "workbench",
            "result": summary,
            "contract": workbench_contract,
            "state": self.snapshot(),
            "side_effects": (),
        }

    def document_instruction_plan(self, document: str | None = None, instruction: str | None = None) -> dict[str, Any]:
        plan = port_terminal_operations_parse_document_instruction(document or "", instruction or "")
        digest = _hash_token(PBC_KEY, document or "", instruction or "")
        document_entry = {
            "document_digest": digest,
            "instruction": instruction or "",
            "candidate_tables": plan["candidate_tables"],
        }
        self.state["documents"] = (*tuple(self.state.get("documents", ())), document_entry)
        return {
            **plan,
            "document_digest": digest,
            "wizard_candidates": ("DocumentInstructionIntakeWizard",),
            "form_candidates": ("PortTerminalEventInboxForm", "PortTerminalPolicyRuleForm"),
            "side_effects": (),
        }

    def advanced_assessment(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        result = port_terminal_operations_run_advanced_assessment(self.state, payload)
        return {**result, "state": self.snapshot(), "side_effects": ()}

    def release_readiness(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        from .release_evidence import build_release_evidence

        evidence = build_release_evidence()
        return {
            "ok": evidence["ok"],
            "operation": "release_readiness",
            "result": evidence,
            "state": self.snapshot(),
            "side_effects": (),
        }


def port_terminal_operations_standalone_route_contracts() -> dict[str, Any]:
    contracts = tuple(
        {
            **item,
            "route_id": f"{item['method']} {item['path']}",
        }
        for item in STANDALONE_ROUTE_CONTRACTS
    )
    return {
        "format": "appgen.port-terminal-operations-standalone-route-contract.v1",
        "ok": bool(contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def dispatch_standalone_route(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    *,
    app: PortTerminalOperationsStandaloneApp | None = None,
) -> dict[str, Any]:
    manifest = port_terminal_operations_standalone_route_contracts()
    route = next(
        (
            item
            for item in manifest["contracts"]
            if item["method"] == method and item["path"] == path
        ),
        None,
    )
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    local_app = app or PortTerminalOperationsStandaloneApp()
    result = getattr(local_app, route["handler"])(payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def port_terminal_operations_standalone_app_contract() -> dict[str, Any]:
    forms = port_terminal_operations_form_contracts()
    wizards = port_terminal_operations_wizard_contracts()
    controls = port_terminal_operations_control_catalog()
    routes = port_terminal_operations_standalone_route_contracts()
    agent = standalone_agent_workspace_contract()
    manifest = standalone_manifest()
    return {
        "format": "appgen.port-terminal-operations-standalone-app.v1",
        "ok": all(
            item.get("ok") is True
            for item in (forms, wizards, controls, routes, agent, manifest)
        ),
        "pbc": PBC_KEY,
        "manifest": manifest,
        "forms": forms,
        "wizards": wizards,
        "controls": controls,
        "routes": routes,
        "agent": agent,
        "docs": tuple(
            {
                "path": name,
                "exists": (Path(__file__).resolve().parent / name).exists(),
            }
            for name in manifest["docs"]
        ),
        "side_effects": (),
    }


def port_terminal_operations_bootstrap_standalone_app(
    *,
    tenant: str = "default",
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    app = PortTerminalOperationsStandaloneApp(tenant=tenant, state=state)
    app.configure()
    app.register_defaults()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app": app,
        "contract": port_terminal_operations_standalone_app_contract(),
        "side_effects": (),
    }


def port_terminal_operations_standalone_app_smoke() -> dict[str, Any]:
    bundle = port_terminal_operations_bootstrap_standalone_app(tenant="tenant_smoke")
    app = bundle["app"]
    create = app.create_vessel_call(
        {
            "record_id": "vessel_smoke",
            "vessel_code": "MV-SMOKE",
            "service_lane": "EA1",
            "eta": "2026-06-01T08:00:00Z",
            "confidence_band": "firm",
        }
    )
    berth = app.record_berth_plan(
        {
            "record_id": "berth_smoke",
            "vessel_code": "MV-SMOKE",
            "berth_id": "B-07",
            "window_start": "2026-06-01T10:00:00Z",
            "window_end": "2026-06-01T18:00:00Z",
        }
    )
    move = app.review_container_move(
        {
            "record_id": "move_smoke",
            "container_id": "MSKU1234567",
            "move_kind": "discharge",
            "source_location": "BAY-12",
            "target_location": "YARD-A1",
        }
    )
    gate = app.simulate_gate_transaction(
        {
            "record_id": "gate_smoke",
            "transaction_id": "GT-001",
            "appointment_window": "2026-06-01T19:00:00Z/2026-06-01T20:00:00Z",
            "direction": "out",
        }
    )
    workbench = app.workbench({"tenant": "tenant_smoke"})
    document = app.document_instruction_plan(
        "Vessel amendment received from carrier.",
        "Update berth nomination and review customs handoff.",
    )
    assessment = app.advanced_assessment({"scenario": "crane outage"})
    from .ui import port_terminal_operations_render_standalone_workbench

    rendered = port_terminal_operations_render_standalone_workbench(workbench["result"])
    return {
        "ok": bundle["contract"]["ok"]
        and create["ok"]
        and berth["ok"]
        and move["ok"]
        and gate["ok"]
        and workbench["ok"]
        and document["ok"]
        and assessment["ok"]
        and rendered["ok"],
        "contract": bundle["contract"],
        "create": create,
        "berth": berth,
        "move": move,
        "gate": gate,
        "workbench": workbench,
        "document": document,
        "assessment": assessment,
        "rendered": rendered,
        "side_effects": (),
    }
