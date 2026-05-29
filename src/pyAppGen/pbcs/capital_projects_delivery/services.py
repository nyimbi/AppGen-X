"""Service layer for the capital_projects_delivery PBC."""
from __future__ import annotations

from .domain_depth import (
    DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS,
    execute_domain_operation as execute_domain_depth_operation,
)
from .runtime import (
    CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES,
    CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES,
    capital_projects_delivery_approve_capital_project_gate,
    capital_projects_delivery_build_agent_help_contract,
    capital_projects_delivery_build_single_pbc_app_contract,
    capital_projects_delivery_build_workbench_view,
    capital_projects_delivery_build_workflow_contracts,
    capital_projects_delivery_command_capital_project,
    capital_projects_delivery_configure_runtime,
    capital_projects_delivery_empty_state,
    capital_projects_delivery_get_capital_project_detail,
    capital_projects_delivery_parse_document_instruction,
    capital_projects_delivery_query_workbench,
    capital_projects_delivery_record_gate_checklist,
    capital_projects_delivery_register_rule,
    capital_projects_delivery_register_schema_extension,
    capital_projects_delivery_receive_event,
    capital_projects_delivery_run_advanced_assessment,
    capital_projects_delivery_set_parameter,
)

PBC_KEY = "capital_projects_delivery"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
OWNED_TABLES = CAPITAL_PROJECTS_DELIVERY_OWNED_TABLES
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "command_capital_project",
            "record_gate_checklist",
            "approve_capital_project_gate",
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = (
    "query_workbench",
    "get_capital_project_detail",
    "build_workbench_view",
    "build_workflow_contracts",
    "build_single_pbc_app_contract",
    "build_agent_help_contract",
)


def _operation_contract(name, kind):
    emitted_event = None
    owned_tables = ()
    read_tables = ()
    if kind == "command":
        if name == "approve_capital_project_gate":
            emitted_event = CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES[2]
            owned_tables = OWNED_TABLES[:1]
        elif name in ("record_gate_checklist", "receive_event"):
            emitted_event = CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES[1]
            owned_tables = OWNED_TABLES[:1]
        elif name == "command_capital_project":
            emitted_event = CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES[0]
            owned_tables = OWNED_TABLES[:1]
        elif name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            domain_plan = execute_domain_depth_operation(name, {})
            emitted_event = domain_plan.get("emitted_event")
            owned_tables = tuple(domain_plan.get("owned_tables", ()))
        else:
            emitted_event = CAPITAL_PROJECTS_DELIVERY_EMITTED_EVENT_TYPES[0]
            owned_tables = OWNED_TABLES[:1]
    elif name in ("query_workbench", "get_capital_project_detail", "build_workbench_view"):
        read_tables = OWNED_TABLES[:1]
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": owned_tables,
        "read_tables": read_tables,
        "emitted_event": emitted_event,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class CapitalProjectsDeliveryService:
    def __init__(self, state=None):
        self._state = capital_projects_delivery_empty_state() if state is None else state

    @property
    def state(self):
        return self._state

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name == "command_capital_project":
            result = capital_projects_delivery_command_capital_project(self._state, payload)
        elif name == "record_gate_checklist":
            result = capital_projects_delivery_record_gate_checklist(
                self._state,
                payload["project_id"],
                payload.get("criteria_status", {}),
                context={
                    "updated_by": payload.get("updated_by", "unspecified"),
                    "updated_at": payload.get("updated_at", "unspecified"),
                },
            )
        elif name == "approve_capital_project_gate":
            result = capital_projects_delivery_approve_capital_project_gate(
                self._state,
                project_id=payload["project_id"],
                target_stage=payload["target_stage"],
                approver_role=payload["approver_role"],
                approved_by=payload["approved_by"],
                approved_at=payload["approved_at"],
                criteria_status=payload.get("criteria_status"),
                rebaseline_reason=payload.get("rebaseline_reason"),
            )
        elif name == "set_parameter":
            result = capital_projects_delivery_set_parameter(self._state, payload["name"], payload.get("value"))
        elif name == "configure_runtime":
            result = capital_projects_delivery_configure_runtime(self._state, payload)
        elif name == "register_rule":
            result = capital_projects_delivery_register_rule(self._state, payload)
        elif name == "register_schema_extension":
            result = capital_projects_delivery_register_schema_extension(self._state, payload["table"], payload.get("fields", {}))
        elif name == "receive_event":
            result = capital_projects_delivery_receive_event(self._state, payload)
        elif name == "run_advanced_assessment":
            result = capital_projects_delivery_run_advanced_assessment(self._state, payload)
        elif name == "parse_document_instruction":
            result = capital_projects_delivery_parse_document_instruction(payload.get("document", ""), payload.get("instruction", ""))
        elif name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {
                "ok": plan["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": {
                    "operation": name,
                    "operation_kind": "command",
                    "owned_tables": plan.get("owned_tables", ()),
                    "read_tables": (),
                    "emitted_event": plan.get("emitted_event"),
                    "transaction_boundary": "owned_datastore_plus_outbox",
                },
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (plan.get("emitted_event"),) if plan.get("emitted_event") else (),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_depth": plan,
                "side_effects": (),
            }
        else:
            result = {"ok": False, "reason": "unsupported_command", "side_effects": ()}

        if "state" in result:
            self._state = result["state"]
        contract = _operation_contract(name, "command")
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract["emitted_event"],) if contract["emitted_event"] else (),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "result": result,
            "state": self._state,
            "side_effects": (),
        }

    def _query(self, name, payload):
        if name == "query_workbench":
            result = capital_projects_delivery_query_workbench(self._state, payload)
        elif name == "get_capital_project_detail":
            result = capital_projects_delivery_get_capital_project_detail(self._state, payload["project_id"])
        elif name == "build_workbench_view":
            result = capital_projects_delivery_build_workbench_view(tenant=payload.get("tenant", "default"))
        elif name == "build_workflow_contracts":
            result = capital_projects_delivery_build_workflow_contracts()
        elif name == "build_single_pbc_app_contract":
            result = capital_projects_delivery_build_single_pbc_app_contract()
        elif name == "build_agent_help_contract":
            result = capital_projects_delivery_build_agent_help_contract()
        else:
            result = {"ok": False, "reason": "unsupported_query", "side_effects": ()}
        contract = _operation_contract(name, "query")
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "result": result,
            "side_effects": (),
        }


def service_operation_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "CapitalProjectsDeliveryService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, "query") for name in QUERY_OPERATIONS)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test():
    service = CapitalProjectsDeliveryService()
    created = service.command_capital_project({
        "tenant": "tenant-smoke",
        "code": "SVC-SMOKE",
        "name": "Service Smoke",
        "reported_at": "2026-05-29",
    })
    checklist = service.record_gate_checklist({
        "project_id": "SVC-SMOKE",
        "criteria_status": {
            "business_case_defined": True,
            "sponsorship_assigned": True,
        },
        "updated_by": "controls",
        "updated_at": "2026-05-29",
    })
    approved = service.approve_capital_project_gate({
        "project_id": "SVC-SMOKE",
        "target_stage": "screening",
        "approver_role": "project_sponsor",
        "approved_by": "sponsor.user",
        "approved_at": "2026-05-29",
    })
    query = service.query_workbench({"tenant": "tenant-smoke"})
    workflows = service.build_workflow_contracts({})
    return {
        "ok": created["ok"] and checklist["ok"] and approved["ok"] and query["ok"] and workflows["ok"] and service_operation_contracts()["ok"],
        "command": approved,
        "query": query,
        "workflows": workflows,
        "side_effects": (),
    }
