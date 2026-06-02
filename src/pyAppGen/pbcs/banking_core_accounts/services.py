"""Service layer for the banking_core_accounts PBC."""
from __future__ import annotations

from .domain_depth import (
    DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS,
    DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES,
    execute_domain_operation as execute_domain_depth_operation,
)
from .runtime import (
    PBC_KEY,
    BANKING_CORE_ACCOUNTS_CONTROLS,
    BANKING_CORE_ACCOUNTS_FORMS,
    BANKING_CORE_ACCOUNTS_WIZARDS,
    banking_core_accounts_build_app_surface,
    banking_core_accounts_build_service_contract,
    banking_core_accounts_build_workflow_surface,
    banking_core_accounts_command_deposit_account,
    banking_core_accounts_empty_state,
    banking_core_accounts_open_deposit_account,
    banking_core_accounts_query_account_detail,
    banking_core_accounts_query_workbench,
    banking_core_accounts_transition_deposit_account,
)

EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "command_deposit_account",
            "open_deposit_account",
            "transition_deposit_account",
            "configure_runtime",
            "set_parameter",
            "register_rule",
        )
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = (
    "query_workbench",
    "query_account_detail",
    "build_workbench_view",
    "build_workflow_surface",
)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES


def _operation_contract(name, kind):
    if name in ("command_deposit_account", "open_deposit_account"):
        emitted_event = "BankingCoreAccountsCreated"
        owned_tables = ("banking_core_accounts_deposit_account",)
        read_tables = ()
    elif name == "transition_deposit_account":
        emitted_event = "BankingCoreAccountsUpdated"
        owned_tables = ("banking_core_accounts_deposit_account",)
        read_tables = ()
    elif name == "query_account_detail":
        emitted_event = None
        owned_tables = ()
        read_tables = ("banking_core_accounts_deposit_account",)
    elif kind == "query":
        emitted_event = None
        owned_tables = ()
        read_tables = ("banking_core_accounts_deposit_account",)
    else:
        emitted_event = "BankingCoreAccountsCreated"
        owned_tables = OWNED_TABLES[:2]
        read_tables = ()
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": owned_tables,
        "read_tables": read_tables,
        "emitted_event": emitted_event,
        "transaction_boundary": "owned_datastore_plus_outbox"
        if kind == "command"
        else "read_only_projection",
        "event_contract": "AppGen-X",
        "shared_table_access": False,
    }


class BankingCoreAccountsService:
    def __init__(self, state=None):
        self.state = state or banking_core_accounts_empty_state()

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
                    "event_contract": "AppGen-X",
                    "shared_table_access": False,
                },
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (plan.get("emitted_event"),),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_depth": plan,
                "side_effects": (),
            }

        if name == "command_deposit_account":
            result = banking_core_accounts_command_deposit_account(self.state, payload)
        elif name == "open_deposit_account":
            result = banking_core_accounts_open_deposit_account(self.state, payload)
        elif name == "transition_deposit_account":
            result = banking_core_accounts_transition_deposit_account(self.state, payload)
        else:
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

        if "state" in result:
            self.state = result["state"]
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
            "side_effects": (),
        }

    def _query(self, name, payload):
        if name == "query_workbench":
            result = banking_core_accounts_query_workbench(self.state, payload)
        elif name == "query_account_detail":
            result = banking_core_accounts_query_account_detail(
                self.state, payload.get("account_id") or payload.get("id")
            )
        elif name == "build_workbench_view":
            result = banking_core_accounts_build_app_surface(
                state=self.state, tenant=payload.get("tenant", "default")
            )["workbench"]
        elif name == "build_workflow_surface":
            result = banking_core_accounts_build_workflow_surface(
                state=self.state, tenant=payload.get("tenant", "default")
            )
        else:
            result = {"ok": False, "reason": "unknown_query"}
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
    service_contract = banking_core_accounts_build_service_contract()
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "BankingCoreAccountsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "forms": tuple(form["form_id"] for form in BANKING_CORE_ACCOUNTS_FORMS),
        "wizards": tuple(wizard["wizard_id"] for wizard in BANKING_CORE_ACCOUNTS_WIZARDS),
        "controls": tuple(control["control_id"] for control in BANKING_CORE_ACCOUNTS_CONTROLS),
        "single_pbc_app": True,
        "service_contract": service_contract,
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
    service = BankingCoreAccountsService()
    opened = service.open_deposit_account(
        {
            "tenant": "tenant-smoke",
            "account_id": "SERVICE-001",
            "account_number": "100001",
            "customer_id": "CUST-SERVICE",
            "product_code": "SAVINGS",
            "currency": "KES",
            "actor_id": "maker-1",
            "source_reference": "service-open",
        }
    )
    approved = service.transition_deposit_account(
        {
            "account_id": "SERVICE-001",
            "target_state": "approved",
            "actor_id": "maker-1",
            "approver_id": "checker-1",
            "reason": "documents_verified",
            "source_reference": "service-approve",
        }
    )
    detail = service.query_account_detail({"account_id": "SERVICE-001"})
    workbench = service.query_workbench({"tenant": "tenant-smoke"})
    workflows = service.build_workflow_surface({"tenant": "tenant-smoke"})
    return {
        "ok": opened["ok"]
        and approved["ok"]
        and detail["ok"]
        and workbench["ok"]
        and workflows["ok"]
        and service_operation_contracts()["ok"],
        "opened": opened,
        "approved": approved,
        "detail": detail,
        "workbench": workbench,
        "workflows": workflows,
        "side_effects": (),
    }
