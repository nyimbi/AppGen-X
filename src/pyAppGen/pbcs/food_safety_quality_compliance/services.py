"""Service layer for the food_safety_quality_compliance PBC."""

from .slice_app import COMMAND_METHODS
from .slice_app import EVENT_TABLES
from .slice_app import FoodSafetyQualityComplianceService
from .slice_app import OPERATION_EVENTS
from .slice_app import OPERATION_TABLES
from .slice_app import OUTBOX_TABLE
from .slice_app import PBC_KEY
from .slice_app import QUERY_METHODS
from .slice_app import build_service_contract as food_safety_quality_compliance_build_service_contract
from .slice_app import empty_state
from .slice_app import operation_contract as _operation_contract
from .slice_app import run_slice_smoke

EVENT_CONTRACT = {
    "outbox_table": OUTBOX_TABLE,
    "inbox_table": EVENT_TABLES[1],
    "dead_letter_table": EVENT_TABLES[2],
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = COMMAND_METHODS
QUERY_OPERATIONS = QUERY_METHODS
OWNED_TABLES = tuple(dict.fromkeys(table for tables in OPERATION_TABLES.values() for table in tables))


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "FoodSafetyQualityComplianceService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, "query") for name in QUERY_OPERATIONS)
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
    service = FoodSafetyQualityComplianceService(empty_state())
    command = service.create_haccp_plan(
        {
            "tenant": "tenant-demo",
            "plan_code": "SERV-1",
            "version": "A",
            "facility_code": "FAC-1",
            "product_scope": ("meal",),
            "process_steps": ({"step_code": "cook"},),
            "hazard_analysis": ({"hazard_id": "haz-1", "process_step_code": "cook", "requires_ccp": False},),
        }
    )
    query = service.query_workbench({"tenant": "tenant-demo"})
    return {"ok": smoke["ok"] and command["ok"] and query["ok"] and food_safety_quality_compliance_build_service_contract()["ok"], "command": command, "query": query, "side_effects": ()}
