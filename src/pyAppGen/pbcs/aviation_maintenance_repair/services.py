"""Service layer for the standalone aviation maintenance repair slice."""
from __future__ import annotations

from .agent import document_instruction_plan
from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS, execute_domain_operation as execute_domain_depth_operation
from .maintenance_release import build_release_to_service_pack
from .models import BUSINESS_TABLES, OWNED_TABLES, entity_blueprint
from .ui import aviation_maintenance_repair_render_workbench
from .workflows import build_release_to_service_workflow, workflow_catalog

PBC_KEY = "aviation_maintenance_repair"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = (
    "record_aircraft",
    "command_aircraft",
    "record_component",
    "record_work_card",
    "record_deferred_defect",
    "record_airworthiness_directive",
    "plan_document_instruction",
    "assess_release_to_service",
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
) + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
QUERY_OPERATIONS = ("query_workbench", "query_release_packs", "query_document_instruction_queue")


def _operation_contract(name, kind):
    if name in {"record_aircraft", "command_aircraft"}:
        return {"operation": name, "operation_kind": kind, "owned_tables": (f"{PBC_KEY}_aircraft",), "read_tables": (), "emitted_event": "AviationMaintenanceRepairCreated", "transaction_boundary": "owned_datastore_plus_outbox"}
    if name == "record_component":
        return {"operation": name, "operation_kind": kind, "owned_tables": (f"{PBC_KEY}_component",), "read_tables": (f"{PBC_KEY}_aircraft",), "emitted_event": "AviationMaintenanceRepairUpdated", "transaction_boundary": "owned_datastore_plus_outbox"}
    if name == "record_work_card":
        return {"operation": name, "operation_kind": kind, "owned_tables": (f"{PBC_KEY}_work_card",), "read_tables": (f"{PBC_KEY}_aircraft",), "emitted_event": "AviationMaintenanceRepairUpdated", "transaction_boundary": "owned_datastore_plus_outbox"}
    if name == "record_deferred_defect":
        return {"operation": name, "operation_kind": kind, "owned_tables": (f"{PBC_KEY}_deferred_defect",), "read_tables": (f"{PBC_KEY}_aircraft",), "emitted_event": "AviationMaintenanceRepairUpdated", "transaction_boundary": "owned_datastore_plus_outbox"}
    if name == "record_airworthiness_directive":
        return {"operation": name, "operation_kind": kind, "owned_tables": (f"{PBC_KEY}_airworthiness_directive",), "read_tables": (f"{PBC_KEY}_aircraft",), "emitted_event": "AviationMaintenanceRepairUpdated", "transaction_boundary": "owned_datastore_plus_outbox"}
    if name == "plan_document_instruction":
        return {"operation": name, "operation_kind": kind, "owned_tables": BUSINESS_TABLES[:5], "read_tables": BUSINESS_TABLES, "emitted_event": None, "transaction_boundary": "read_only_projection"}
    if name == "assess_release_to_service":
        return {"operation": name, "operation_kind": kind, "owned_tables": (f"{PBC_KEY}_compliance_release", f"{PBC_KEY}_work_card", f"{PBC_KEY}_component"), "read_tables": (f"{PBC_KEY}_aircraft", f"{PBC_KEY}_deferred_defect", f"{PBC_KEY}_airworthiness_directive"), "emitted_event": "AviationMaintenanceRepairApproved", "transaction_boundary": "owned_datastore_plus_outbox"}
    if kind == "query":
        return {"operation": name, "operation_kind": kind, "owned_tables": (), "read_tables": OWNED_TABLES, "emitted_event": None, "transaction_boundary": "read_only_projection"}
    return {"operation": name, "operation_kind": kind, "owned_tables": OWNED_TABLES[:1], "read_tables": (), "emitted_event": "AviationMaintenanceRepairUpdated", "transaction_boundary": "owned_datastore_plus_outbox"}


class AviationMaintenanceRepairService:
    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name == "plan_document_instruction":
            plan = document_instruction_plan(payload.get("document"), payload.get("instruction"), payload.get("context"))
            return {"ok": plan["ok"], "operation": name, "operation_kind": "command", "read_only": True, "payload": dict(payload), "operation_contract": _operation_contract(name, "command"), "document_plan": plan, "side_effects": ()}
        if name == "assess_release_to_service":
            pack = build_release_to_service_pack(payload)
            workflow = build_release_to_service_workflow(payload)
            contract = _operation_contract(name, "command")
            return {"ok": pack["ok"], "operation": name, "operation_kind": "command", "read_only": False, "payload": dict(payload), "operation_contract": contract, "outbox_table": EVENT_CONTRACT["outbox_table"], "emits": (("AviationMaintenanceRepairApproved" if pack["ok"] else "AviationMaintenanceRepairExceptionOpened"),), "transaction_boundary": "owned_datastore_plus_outbox", "release_pack": pack, "workflow": workflow, "side_effects": ()}
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {"ok": plan["ok"], "operation": name, "operation_kind": "command", "read_only": False, "payload": dict(payload), "operation_contract": {"operation": name, "operation_kind": "command", "owned_tables": plan.get("owned_tables", ()), "read_tables": (), "emitted_event": plan.get("emitted_event"), "transaction_boundary": "owned_datastore_plus_outbox"}, "outbox_table": EVENT_CONTRACT["outbox_table"], "emits": (plan.get("emitted_event"),), "transaction_boundary": "owned_datastore_plus_outbox", "domain_depth": plan, "side_effects": ()}
        entity = {
            "record_aircraft": "aircraft",
            "command_aircraft": "aircraft",
            "record_component": "component",
            "record_work_card": "work_card",
            "record_deferred_defect": "deferred_defect",
            "record_airworthiness_directive": "airworthiness_directive",
        }.get(name)
        blueprint = entity_blueprint(entity) if entity else None
        contract = _operation_contract(name, "command")
        return {"ok": True, "operation": name, "operation_kind": "command", "read_only": False, "payload": dict(payload), "operation_contract": contract, "entity_blueprint": blueprint, "outbox_table": EVENT_CONTRACT["outbox_table"], "emits": ((contract["emitted_event"],) if contract["emitted_event"] else ()), "transaction_boundary": contract["transaction_boundary"], "side_effects": ()}

    def _query(self, name, payload):
        contract = _operation_contract(name, "query")
        workbench = aviation_maintenance_repair_render_workbench()
        return {"ok": True, "operation": name, "operation_kind": "query", "read_only": True, "payload": dict(payload), "operation_contract": contract, "workbench": workbench, "workflow_catalog": workflow_catalog(), "outbox_table": None, "emits": (), "side_effects": ()}


def service_operation_manifest():
    return {"ok": True, "pbc": PBC_KEY, "service_class": "AviationMaintenanceRepairService", "command_operations": COMMAND_OPERATIONS, "query_operations": QUERY_OPERATIONS, "event_contract": EVENT_CONTRACT, "workflows": workflow_catalog()["workflows"], "side_effects": ()}


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, "query") for name in QUERY_OPERATIONS)
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {"ok": operation in manifest["query_operations"] + manifest["command_operations"], "operation": operation, "operation_kind": kind, "payload": dict(payload or {}), "side_effects": ()}


def smoke_test():
    service = AviationMaintenanceRepairService()
    command = service.record_aircraft({"tenant": "tenant-smoke", "tail_number": "5Y-SMK", "aircraft_type": "B737"})
    query = service.query_workbench({"tenant": "tenant-smoke"})
    plan = service.plan_document_instruction({"document": "logbook", "instruction": "create work card"})
    return {"ok": command["ok"] and query["ok"] and plan["ok"] and service_operation_contracts()["ok"], "side_effects": ()}
