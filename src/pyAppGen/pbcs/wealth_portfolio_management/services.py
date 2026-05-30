"""Service layer for the wealth_portfolio_management PBC."""
from __future__ import annotations

from .domain_depth import (
    DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS,
    DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES,
    execute_domain_operation as execute_domain_depth_operation,
)
from .models import (
    BUSINESS_TABLES,
    EVENT_TABLES,
    WealthPortfolioManagementStandaloneStore,
    standalone_model_contract,
    standalone_store_smoke_test,
)

PBC_KEY = "wealth_portfolio_management"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "command_client_portfolio",
            "configure_runtime",
            "set_parameter",
            "register_rule",
        )
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = ("query_workbench",)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES
STANDALONE_COMMAND_OPERATIONS = (
    "create_portfolio",
    "record_investment_policy",
    "record_suitability_profile",
    "record_fee_schedule",
    "record_document_package",
    "generate_trade_proposal",
    "record_performance_snapshot",
    "record_advisor_review",
    "run_compliance_surveillance",
    "receive_event",
)
STANDALONE_QUERY_OPERATIONS = ("build_workbench", "build_portfolio_detail")


def _operation_contract(name, kind):
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES[:2] if kind == "command" else (),
        "read_tables": OWNED_TABLES[:2] if kind == "query" else (),
        "emitted_event": (
            "WealthPortfolioManagementCreated",
            "WealthPortfolioManagementUpdated",
            "WealthPortfolioManagementApproved",
            "WealthPortfolioManagementExceptionOpened",
        )[0]
        if kind == "command"
        else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class WealthPortfolioManagementService:
    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
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
                "emits": (plan.get("emitted_event"),),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_depth": plan,
                "side_effects": (),
            }
        contract = _operation_contract(name, "command")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract["emitted_event"],),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "side_effects": (),
        }

    def _query(self, name, payload):
        contract = _operation_contract(name, "query")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "side_effects": (),
        }


class WealthPortfolioManagementStandaloneService:
    """Executable one-PBC service façade backed by the standalone sqlite store."""

    def __init__(self, store: WealthPortfolioManagementStandaloneStore | None = None) -> None:
        self.store = store or WealthPortfolioManagementStandaloneStore()

    def close(self) -> None:
        self.store.close()

    def create_portfolio(self, payload: dict | None = None) -> dict:
        return self.store.create_client_portfolio(dict(payload or {}))

    def record_investment_policy(self, payload: dict | None = None) -> dict:
        return self.store.record_investment_mandate(dict(payload or {}))

    def record_suitability_profile(self, payload: dict | None = None) -> dict:
        return self.store.record_suitability_profile(dict(payload or {}))

    def record_fee_schedule(self, payload: dict | None = None) -> dict:
        return self.store.record_fee_schedule(dict(payload or {}))

    def record_document_package(self, payload: dict | None = None) -> dict:
        return self.store.record_document_package(dict(payload or {}))

    def generate_trade_proposal(self, payload: dict | None = None) -> dict:
        return self.store.generate_trade_proposal(dict(payload or {}))

    def record_performance_snapshot(self, payload: dict | None = None) -> dict:
        return self.store.record_performance_snapshot(dict(payload or {}))

    def record_advisor_review(self, payload: dict | None = None) -> dict:
        return self.store.record_advisor_review(dict(payload or {}))

    def run_compliance_surveillance(self, payload: dict | None = None) -> dict:
        return self.store.run_compliance_surveillance(dict(payload or {}))

    def receive_event(self, payload: dict | None = None) -> dict:
        return self.store.receive_event(dict(payload or {}))

    def build_workbench(self, payload: dict | None = None) -> dict:
        request = dict(payload or {})
        return self.store.build_workbench(str(request.get("tenant") or "default"))

    def build_portfolio_detail(self, payload: dict | None = None) -> dict:
        request = dict(payload or {})
        return self.store.build_portfolio_detail(str(request.get("portfolio_id")))


def service_operation_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "WealthPortfolioManagementService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts():
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


def standalone_service_operation_contracts() -> dict:
    contracts = tuple(
        {
            "operation": name,
            "operation_kind": "command",
            "owned_tables": BUSINESS_TABLES,
            "event_contract": "AppGen-X",
            "requires_confirmation": name != "receive_event",
            "transaction_boundary": "package_local_sqlite_plus_outbox",
        }
        for name in STANDALONE_COMMAND_OPERATIONS
    ) + tuple(
        {
            "operation": name,
            "operation_kind": "query",
            "read_tables": BUSINESS_TABLES,
            "event_contract": "AppGen-X",
            "requires_confirmation": False,
            "transaction_boundary": "read_only_projection",
        }
        for name in STANDALONE_QUERY_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "model_contract": standalone_model_contract(),
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
    service = WealthPortfolioManagementService()
    command = getattr(service, COMMAND_OPERATIONS[0])({"tenant": "tenant-smoke"})
    query = getattr(service, QUERY_OPERATIONS[0])({"tenant": "tenant-smoke"})
    return {
        "ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "side_effects": (),
    }


def standalone_service_smoke_test() -> dict:
    service = WealthPortfolioManagementStandaloneService()
    try:
        result = standalone_store_smoke_test()
        workbench = service.build_workbench({"tenant": "tenant-smoke"})
        return {
            "ok": result["ok"] and workbench["ok"] and standalone_service_operation_contracts()["ok"],
            "store_smoke": result,
            "workbench": workbench,
            "side_effects": (),
        }
    finally:
        service.close()
