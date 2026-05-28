"""Service layer for the chemical_batch_compliance PBC."""

from __future__ import annotations

from .slice_app import COMMAND_METHODS
from .slice_app import EVENT_TABLES
from .slice_app import OPERATION_EVENTS
from .slice_app import OPERATION_TABLES
from .slice_app import OUTBOX_TABLE
from .slice_app import PBC_KEY
from .slice_app import QUERY_METHODS
from .slice_app import build_service_contract as chemical_batch_compliance_build_service_contract
from .slice_app import empty_state
from .slice_app import operation_contract as _operation_contract
from .slice_app import run_slice_smoke
from .slice_app import service_callable

EVENT_CONTRACT = {
    "outbox_table": OUTBOX_TABLE,
    "inbox_table": EVENT_TABLES[1],
    "dead_letter_table": EVENT_TABLES[2],
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = COMMAND_METHODS
QUERY_OPERATIONS = QUERY_METHODS
OWNED_TABLES = tuple(dict.fromkeys(table for tables in OPERATION_TABLES.values() for table in tables))


class ChemicalBatchComplianceService:
    """Stateful package-local service harness for one-PBC execution."""

    def __init__(self, state: dict | None = None) -> None:
        self.state = state or empty_state()

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        result = service_callable(name)(self.state, dict(payload))
        if result.get("ok") and "state" in result:
            self.state = result["state"]
        return {
            "ok": result.get("ok", False),
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "command"),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": ((OPERATION_EVENTS.get(name),) if OPERATION_EVENTS.get(name) else ()),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "result": result,
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        result = service_callable(name)(self.state, dict(payload))
        return {
            "ok": result.get("ok", False),
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "query"),
            "outbox_table": None,
            "emits": (),
            "result": result,
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "ChemicalBatchComplianceService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    known = operation in manifest["query_operations"] + manifest["command_operations"]
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": known,
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "owned_tables": _operation_contract(operation, kind).get("owned_tables", ()) if known else (),
        "side_effects": (),
    }


def smoke_test() -> dict:
    smoke = run_slice_smoke()
    service = ChemicalBatchComplianceService()
    command = service.create_formula_revision(
        {
            "tenant": "tenant-demo",
            "formula_code": "SERV-1",
            "revision": "A",
            "product_name": "Service Formula",
            "target_concentration": {"assay_pct": 95.0},
            "composition_window": {"solvent_pct_min": 10, "solvent_pct_max": 12},
            "effectivity_start": "2026-01-01",
        }
    )
    query = service.query_workbench({"tenant": "tenant-demo"})
    return {
        "ok": smoke["ok"] and command["ok"] and query["ok"] and chemical_batch_compliance_build_service_contract()["ok"],
        "command": command,
        "query": query,
        "side_effects": (),
    }
