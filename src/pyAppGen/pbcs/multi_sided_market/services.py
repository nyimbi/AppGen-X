"""Command and query service layer for the multi_sided_market PBC."""

from __future__ import annotations

from .runtime import MULTI_SIDED_MARKET_OWNED_TABLES, multi_sided_market_build_service_contract

PBC_KEY = "multi_sided_market"
EVENT_CONTRACT = {
    "contract": "appgen_event_contract",
    "runtime_profile_visibility": "read_only_platform_metadata",
    "adapter": "appgen_event_adapter",
    "topic": "pbc.multi_sided_market.events",
    "outbox_table": "multi_sided_market_appgen_outbox_event",
    "inbox_table": "multi_sided_market_appgen_inbox_event",
    "dead_letter_table": "multi_sided_market_appgen_dead_letter_event",
}
COMMAND_ROUTES = {
    "command_market_participants": ("POST", "/api/pbc/multi_sided_market/participants", "multi_sided_market.command.participant"),
    "command_market_listings": ("POST", "/api/pbc/multi_sided_market/listings", "multi_sided_market.command.listing"),
    "command_market_service_offers": ("POST", "/api/pbc/multi_sided_market/service-offers", "multi_sided_market.command.service_offer"),
    "command_market_trade_orders": ("POST", "/api/pbc/multi_sided_market/trade-orders", "multi_sided_market.command.trade_order"),
    "command_market_barter_offers": ("POST", "/api/pbc/multi_sided_market/barter-offers", "multi_sided_market.command.barter_offer"),
    "command_market_sale_orders": ("POST", "/api/pbc/multi_sided_market/sale-orders", "multi_sided_market.command.sale_order"),
    "command_market_bookings": ("POST", "/api/pbc/multi_sided_market/bookings", "multi_sided_market.command.booking"),
    "command_market_rentals": ("POST", "/api/pbc/multi_sided_market/rentals", "multi_sided_market.command.rental"),
    "command_market_loans": ("POST", "/api/pbc/multi_sided_market/loans", "multi_sided_market.command.loan"),
    "command_market_escrow": ("POST", "/api/pbc/multi_sided_market/escrow", "multi_sided_market.command.escrow"),
    "command_market_settlements": ("POST", "/api/pbc/multi_sided_market/settlements", "multi_sided_market.command.settlement"),
    "command_market_disputes": ("POST", "/api/pbc/multi_sided_market/disputes", "multi_sided_market.command.dispute"),
}
QUERY_ROUTES = {
    "query_market_workbench": ("GET", "/api/pbc/multi_sided_market-workbench", "multi_sided_market.query.workbench"),
}


def _operation_contracts() -> tuple[dict, ...]:
    service_contract = multi_sided_market_build_service_contract()
    event_map = service_contract["operation_event_map"]
    commands = tuple(
        {
            "operation": operation,
            "operation_kind": "command",
            "method": route[0],
            "path": route[1],
            "permission": route[2],
            "owned_tables": MULTI_SIDED_MARKET_OWNED_TABLES,
            "read_tables": (),
            "emitted_event": event_map[operation],
            "transaction_boundary": "owned_datastore_plus_outbox",
            "event_contract": "AppGen-X",
        }
        for operation, route in COMMAND_ROUTES.items()
    )
    queries = tuple(
        {
            "operation": operation,
            "operation_kind": "query",
            "method": route[0],
            "path": route[1],
            "permission": route[2],
            "owned_tables": (),
            "read_tables": MULTI_SIDED_MARKET_OWNED_TABLES,
            "emitted_event": None,
            "transaction_boundary": "owned_datastore_read",
            "event_contract": "AppGen-X",
        }
        for operation, route in QUERY_ROUTES.items()
    )
    return commands + queries


OPERATION_CONTRACTS = _operation_contracts()


def service_operation_contracts():
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    event_map = multi_sided_market_build_service_contract()["operation_event_map"]
    exact_events = all(item["emitted_event"] == event_map[item["operation"]] for item in command_contracts)
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and exact_events
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] and item["emitted_event"] is None for item in query_contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "operation_event_map": event_map,
        "side_effects": (),
    }


def operation_plan(operation_name, payload=None):
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "operation_contract": contract,
        "side_effects": (),
    }


class MultiSidedMarketService:
    """Side-effect-free market command/query facade."""

    def _execute(self, operation_name, payload):
        plan = operation_plan(operation_name, payload)
        result = {
            "ok": plan["ok"],
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": plan.get("operation_kind"),
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "side_effects": (),
        }
        if plan.get("operation_kind") == "command":
            result.update({"command": operation_name, "read_only": False, "outbox_table": EVENT_CONTRACT["outbox_table"], "emits": (plan.get("emitted_event"),)})
        elif plan.get("operation_kind") == "query":
            result.update({"query": operation_name, "read_only": True, "outbox_table": None, "emits": ()})
        return result

    def _command(self, command_name, payload):
        return self._execute(command_name, payload)

    def _query(self, query_name, payload):
        return self._execute(query_name, payload)

    def command_market_participants(self, payload=None):
        return self._command("command_market_participants", payload or {})

    def command_market_listings(self, payload=None):
        return self._command("command_market_listings", payload or {})

    def command_market_service_offers(self, payload=None):
        return self._command("command_market_service_offers", payload or {})

    def command_market_trade_orders(self, payload=None):
        return self._command("command_market_trade_orders", payload or {})

    def command_market_barter_offers(self, payload=None):
        return self._command("command_market_barter_offers", payload or {})

    def command_market_sale_orders(self, payload=None):
        return self._command("command_market_sale_orders", payload or {})

    def command_market_bookings(self, payload=None):
        return self._command("command_market_bookings", payload or {})

    def command_market_rentals(self, payload=None):
        return self._command("command_market_rentals", payload or {})

    def command_market_loans(self, payload=None):
        return self._command("command_market_loans", payload or {})

    def command_market_escrow(self, payload=None):
        return self._command("command_market_escrow", payload or {})

    def command_market_settlements(self, payload=None):
        return self._command("command_market_settlements", payload or {})

    def command_market_disputes(self, payload=None):
        return self._command("command_market_disputes", payload or {})

    def query_market_workbench(self, payload=None):
        return self._query("query_market_workbench", payload or {})


def service_operation_manifest():
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": "MultiSidedMarketService",
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "operation_event_map": contracts["operation_event_map"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test():
    manifest = service_operation_manifest()
    service = MultiSidedMarketService()
    operation = manifest["operations"][0]
    result = getattr(service, operation)({"smoke": True})
    return {"ok": manifest["ok"] and result["ok"] and result["operation_contract"]["ok"], "manifest": manifest, "result": result, "side_effects": ()}
