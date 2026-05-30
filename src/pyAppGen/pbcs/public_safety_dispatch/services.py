"""Service layer for the public_safety_dispatch PBC."""
from __future__ import annotations

from .standalone import APPGEN_X_TOPIC, PBC_KEY, build_service_contract, build_standalone_app

EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
    "topic": APPGEN_X_TOPIC,
    "transaction_boundary": "owned_datastore_plus_outbox",
}


class PublicSafetyDispatchService:
    def __init__(self) -> None:
        self.app = build_standalone_app()

    def __getattr__(self, name):
        contract = build_service_contract()
        if name in contract["command_methods"]:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in contract["query_methods"]:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name == "document_instruction_plan":
            result = self.app.document_instruction_plan(payload.get("document", ""), payload.get("instruction", "preview"))
        elif name == "datastore_crud_plan":
            result = self.app.datastore_crud_plan(payload.get("action", "create"), payload.get("table"), payload.get("payload"))
        elif name == "run_advanced_assessment":
            result = self.app.run_advanced_assessment(tenant=payload.get("tenant", "tenant_alpha"))
        else:
            result = getattr(self.app, name)(payload)
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "transaction_boundary": EVENT_CONTRACT["transaction_boundary"],
            "operation_contract": operation_plan(name)["operation_contract"],
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            **result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == "query_workbench":
            self.app.load_demo_workspace(payload.get("tenant", "tenant_alpha"))
            result = self.app.query_workbench(payload.get("tenant", "tenant_alpha"))
        elif name == "build_workbench_view":
            self.app.load_demo_workspace(payload.get("tenant", "tenant_alpha"))
            result = self.app.build_workbench_view(payload.get("tenant", "tenant_alpha"))
        else:
            result = self.app.verify_owned_table_boundary(tuple(payload.get("references", ())))
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": operation_plan(name)["operation_contract"],
            **result,
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    contract = build_service_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "PublicSafetyDispatchService",
        "command_operations": contract["command_methods"],
        "query_operations": contract["query_methods"],
        "event_contract": EVENT_CONTRACT,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "standalone_service": contract,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contract = build_service_contract()
    contracts = tuple(
        {
            "operation": name,
            "operation_kind": "command",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "event_contract": contract["event_contract"],
        }
        for name in contract["command_methods"]
    ) + tuple(
        {
            "operation": name,
            "operation_kind": "query",
            "transaction_boundary": "read_only_projection",
            "event_contract": contract["event_contract"],
        }
        for name in contract["query_methods"]
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    contract = build_service_contract()
    if operation in contract["command_methods"]:
        kind = "command"
        boundary = "owned_datastore_plus_outbox"
    elif operation in contract["query_methods"]:
        kind = "query"
        boundary = "read_only_projection"
    else:
        return {"ok": False, "operation": operation, "reason": "unknown_operation", "side_effects": ()}
    return {
        "ok": True,
        "operation": operation,
        "payload": dict(payload or {}),
        "operation_kind": kind,
        "operation_contract": {
            "operation": operation,
            "operation_kind": kind,
            "transaction_boundary": boundary,
            "event_contract": contract["event_contract"],
        },
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = PublicSafetyDispatchService()
    command = service.create_emergency_call(
        {
            "tenant": "tenant_smoke",
            "caller_name": "Taylor Brooks",
            "callback_number": "5550101111",
            "chief_complaint": "Possible fire alarm",
            "narrative": "Alarm sounding with smoke in hallway.",
            "address": "12 Main St",
            "jurisdiction": "central_city",
            "beat": "beat-3",
        }
    )
    query = service.query_workbench({"tenant": "tenant_smoke"})
    return {"ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"], "command": command, "query": query, "side_effects": ()}
