"""Service layer for the water_wastewater_operations PBC."""

from . import operations_engine as engine
from .runtime import (
    water_wastewater_operations_build_api_contract,
    water_wastewater_operations_build_release_evidence,
    water_wastewater_operations_build_schema_contract,
    water_wastewater_operations_build_service_contract,
    water_wastewater_operations_build_workbench_view,
    water_wastewater_operations_configure_runtime,
    water_wastewater_operations_parse_document_instruction,
    water_wastewater_operations_query_workbench,
    water_wastewater_operations_receive_event,
    water_wastewater_operations_register_rule,
    water_wastewater_operations_register_schema_extension,
    water_wastewater_operations_run_advanced_assessment,
    water_wastewater_operations_set_parameter,
)

PBC_KEY = engine.PBC_KEY
EVENT_CONTRACT = {
    "outbox_table": engine.RUNTIME_TABLES[0],
    "inbox_table": engine.RUNTIME_TABLES[1],
    "dead_letter_table": engine.RUNTIME_TABLES[2],
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
) + engine.DOMAIN_OPERATIONS
QUERY_OPERATIONS = (
    "query_workbench",
    "build_workbench_view",
    "build_schema_contract",
    "build_service_contract",
    "build_release_evidence",
    "build_api_contract",
    "run_advanced_assessment",
    "parse_document_instruction",
)
OWNED_TABLES = engine.OWNED_TABLES


def _operation_contract(name, kind):
    preview = engine.preview_domain_operation(name, {}) if name in engine.DOMAIN_OPERATIONS else None
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": preview["owned_tables"] if preview else OWNED_TABLES,
        "read_tables": () if kind == "command" else OWNED_TABLES,
        "emitted_event": preview["emitted_event"] if preview else (engine.EMITTED_EVENT_TYPES[0] if kind == "command" else None),
        "transaction_boundary": "water_wastewater_operations_owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class WaterWastewaterOperationsService:
    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name == "configure_runtime":
            result = water_wastewater_operations_configure_runtime(engine.empty_state(), payload)
        elif name == "set_parameter":
            result = water_wastewater_operations_set_parameter(engine.empty_state(), payload["name"], payload["value"])
        elif name == "register_rule":
            result = water_wastewater_operations_register_rule(engine.empty_state(), payload)
        elif name == "register_schema_extension":
            result = water_wastewater_operations_register_schema_extension(engine.empty_state(), payload["table"], payload.get("fields"))
        elif name == "receive_event":
            result = water_wastewater_operations_receive_event(engine.empty_state(), payload)
        else:
            result = engine.run_domain_operation(engine.empty_state(), name, payload)
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
            "transaction_boundary": contract["transaction_boundary"],
            "domain_depth": result,
            "side_effects": (),
        }

    def _query(self, name, payload):
        tenant = payload.get("tenant", "default")
        if name == "query_workbench":
            result = water_wastewater_operations_query_workbench(engine.empty_state(), filters=payload.get("filters"), tenant=tenant)
        elif name == "build_workbench_view":
            result = water_wastewater_operations_build_workbench_view(engine.empty_state(), tenant=tenant, filters=payload.get("filters"))
        elif name == "build_schema_contract":
            result = water_wastewater_operations_build_schema_contract()
        elif name == "build_service_contract":
            result = water_wastewater_operations_build_service_contract()
        elif name == "build_release_evidence":
            result = water_wastewater_operations_build_release_evidence()
        elif name == "build_api_contract":
            result = water_wastewater_operations_build_api_contract()
        elif name == "run_advanced_assessment":
            result = water_wastewater_operations_run_advanced_assessment(engine.empty_state(), payload)
        else:
            result = water_wastewater_operations_parse_document_instruction(payload.get("document", ""), payload.get("instruction", ""))
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
            "side_effects": (),
        }


def service_operation_manifest():
    return {"ok": True, "pbc": PBC_KEY, "service_class": "WaterWastewaterOperationsService", "command_operations": COMMAND_OPERATIONS, "query_operations": QUERY_OPERATIONS, "event_contract": EVENT_CONTRACT, "side_effects": ()}


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, "query") for name in QUERY_OPERATIONS)
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {"ok": operation in manifest["query_operations"] + manifest["command_operations"], "operation": operation, "operation_kind": kind, "payload": dict(payload or {}), "side_effects": ()}


def smoke_test():
    service = WaterWastewaterOperationsService()
    command = getattr(service, "register_treatment_plant")({"plant_code": "PLANT-1", "plant_name": "North WTP", "utility_type": "drinking_water", "operating_state": "normal"})
    query = getattr(service, "build_workbench_view")({"tenant": "default"})
    return {"ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"], "command": command, "query": query, "side_effects": ()}
