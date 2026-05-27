"""Command service layer for the loyalty_rewards PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from .runtime import LOYALTY_REWARDS_RUNTIME_TABLES
from .runtime import loyalty_rewards_build_api_contract
from .runtime import loyalty_rewards_build_service_contract


def _method_path(route: str) -> tuple[str, str]:
    method, path = route.split(" ", 1)
    return method, path


def _operation_name(route: dict) -> str | None:
    return route.get("command") or route.get("query")


def _owned_tables(route: dict) -> tuple[str, ...]:
    return tuple(
        table if table.startswith("loyalty_rewards_") else f"loyalty_rewards_{table}"
        for table in route.get("owned_tables", ())
    )


def _build_operation_contracts() -> tuple[dict, ...]:
    api = loyalty_rewards_build_api_contract()
    fallback_emitted = api["emits"][0]
    contracts = []
    for route in api["routes"]:
        operation = _operation_name(route)
        if not operation:
            continue
        method, path = _method_path(route["route"])
        is_command = "command" in route
        table_scope = _owned_tables(route)
        if is_command and not table_scope and operation == "receive_event":
            table_scope = (LOYALTY_REWARDS_RUNTIME_TABLES[1], LOYALTY_REWARDS_RUNTIME_TABLES[2])
        contracts.append(
            {
                "operation": operation,
                "operation_kind": "command" if is_command else "query",
                "method": method,
                "path": path,
                "permission": route["requires_permission"],
                "owned_tables": table_scope if is_command else (),
                "read_tables": () if is_command else table_scope,
                "emitted_event": (tuple(route.get("emits", ())) or (fallback_emitted,))[0] if is_command else None,
                "consumed_event": tuple(route.get("consumes", ())),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _build_operation_contracts()


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = loyalty_rewards_build_service_contract()
    return {
        "ok": runtime_service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] or item["consumed_event"] for item in command_contracts)
        and all(item["read_tables"] for item in query_contracts),
        "pbc": "loyalty_rewards",
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
    table_scope = contract["owned_tables"] or contract["read_tables"] or tuple(LOYALTY_REWARDS_RUNTIME_TABLES)
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": "loyalty_rewards",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "consumed_event": contract["consumed_event"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


class LoyaltyRewardsService:
    """Side-effect-free service facade for generated route dispatch."""

    def execute_operation(self, operation_name: str, payload: dict | None = None) -> dict:
        plan = operation_plan(operation_name, payload)
        operation_kind = plan.get("operation_kind")
        result = {
            "ok": plan["ok"],
            "pbc": "loyalty_rewards",
            "operation": operation_name,
            "operation_kind": operation_kind,
            "payload": dict(payload or {}),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if operation_kind == "command":
            result.update(
                {
                    "command": operation_name,
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (plan.get("emitted_event"),),
                    "consumes": plan.get("consumed_event", ()),
                }
            )
        elif operation_kind == "query":
            result.update(
                {
                    "query": operation_name,
                    "read_only": True,
                    "outbox_table": None,
                    "emits": (),
                }
            )
        return result

    def __getattr__(self, operation_name: str):
        if operation_name in service_operation_contracts()["operations"]:
            return lambda payload=None: self.execute_operation(operation_name, payload or {})
        raise AttributeError(operation_name)


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": "loyalty_rewards",
        "service_class": LoyaltyRewardsService.__name__,
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute one side-effect-free service operation through the facade."""
    manifest = service_operation_manifest()
    service = LoyaltyRewardsService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = service.execute_operation(operation, {"smoke": True}) if operation else {"ok": False}
    return {
        "ok": manifest["ok"] and result.get("ok") is True and result.get("operation_contract", {}).get("ok") is True,
        "manifest": manifest,
        "result": result,
        "side_effects": (),
    }
