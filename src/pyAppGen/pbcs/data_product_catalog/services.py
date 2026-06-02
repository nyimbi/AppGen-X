"""Service layer for the data_product_catalog PBC."""
from __future__ import annotations

from .blueprint import EVENT_CONTRACT, OPERATION_BLUEPRINTS, OWNED_TABLES, PBC_KEY, QUERY_BLUEPRINTS
from .runtime import (
    DataProductCatalogApp,
    data_product_catalog_build_workbench_view,
    data_product_catalog_command_data_product,
    data_product_catalog_configure_runtime,
    data_product_catalog_execute_domain_operation,
    data_product_catalog_list_controls,
    data_product_catalog_list_forms,
    data_product_catalog_list_wizards,
    data_product_catalog_parse_document_instruction,
    data_product_catalog_query_workbench,
    data_product_catalog_receive_event,
    data_product_catalog_register_rule,
    data_product_catalog_register_schema_extension,
    data_product_catalog_run_advanced_assessment,
    data_product_catalog_set_parameter,
    data_product_catalog_empty_state,
)

EVENT_CONTRACT_MANIFEST = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": EVENT_CONTRACT,
}
COMMAND_OPERATIONS = (
    "command_data_product",
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
) + tuple(item["name"] for item in OPERATION_BLUEPRINTS)
QUERY_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "query_workbench",
            "build_workbench_view",
            "list_forms",
            "list_wizards",
            "list_controls",
            "document_instruction_plan",
            "run_advanced_assessment",
        )
        + tuple(item["name"] for item in QUERY_BLUEPRINTS if item["name"] != "query_workbench")
    )
)


def _operation_contract(name: str, kind: str) -> dict:
    operation_spec = next((item for item in OPERATION_BLUEPRINTS if item["name"] == name), None)
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": (operation_spec["target_table"],) if kind == "command" and operation_spec else OWNED_TABLES,
        "read_tables": OWNED_TABLES if kind == "query" else (),
        "emitted_event": operation_spec["emitted_event"] if operation_spec else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class DataProductCatalogService:
    def __init__(self, state: dict | None = None) -> None:
        self.app = DataProductCatalogApp(state or data_product_catalog_empty_state())

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name == "configure_runtime":
            result = data_product_catalog_configure_runtime(self.app.state, payload)
            self.app.state = result["state"]
        elif name == "set_parameter":
            result = data_product_catalog_set_parameter(self.app.state, payload["name"], payload["value"])
            if result["ok"]:
                self.app.state = result["state"]
        elif name == "register_rule":
            result = data_product_catalog_register_rule(self.app.state, payload)
            if result["ok"]:
                self.app.state = result["state"]
        elif name == "register_schema_extension":
            result = data_product_catalog_register_schema_extension(self.app.state, payload["table"], payload["fields"])
            if result["ok"]:
                self.app.state = result["state"]
        elif name == "receive_event":
            result = data_product_catalog_receive_event(self.app.state, payload)
            self.app.state = result["state"]
        elif name == "command_data_product":
            result = data_product_catalog_command_data_product(self.app.state, payload)
            self.app.state = result["state"]
        else:
            result = data_product_catalog_execute_domain_operation(self.app.state, name, payload)
            self.app.state = result["state"]
        contract = _operation_contract(name, "command")
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT_MANIFEST["outbox_table"],
            "emits": (contract["emitted_event"],) if contract["emitted_event"] else (),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "domain_depth": result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == "query_workbench":
            result = data_product_catalog_query_workbench(self.app.state, payload)
        elif name == "build_workbench_view":
            result = data_product_catalog_build_workbench_view(self.app.state, payload.get("tenant", "default"))
        elif name == "list_forms":
            result = data_product_catalog_list_forms()
        elif name == "list_wizards":
            result = data_product_catalog_list_wizards()
        elif name == "list_controls":
            result = data_product_catalog_list_controls()
        elif name == "document_instruction_plan":
            result = data_product_catalog_parse_document_instruction(payload.get("document", ""), payload.get("instruction", ""))
        elif name == "run_advanced_assessment":
            result = data_product_catalog_run_advanced_assessment(self.app.state, payload)
        else:
            result = {"ok": name in tuple(item["name"] for item in QUERY_BLUEPRINTS), "payload": dict(payload)}
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


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "DataProductCatalogService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT_MANIFEST,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    known = operation in manifest["query_operations"] + manifest["command_operations"]
    return {
        "ok": known,
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = DataProductCatalogService()
    command = service.create_data_product({"tenant": "tenant-smoke", "code": "CUSTOMER360", "product_type": "analytical", "value_proposition": "Trusted customer profile"})
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "side_effects": (),
    }
