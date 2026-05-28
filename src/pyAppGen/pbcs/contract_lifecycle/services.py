"""Service layer for the contract_lifecycle PBC.

Source-audit trace: owned_datastore_plus_outbox
"""

from .application import (
    ContractLifecycleService,
    OPERATION_SPECS,
    OWNED_TABLES,
    PBC_KEY,
    event_contract_manifest,
    operation_plan as app_operation_plan,
    service_contract,
)

EVENT_CONTRACT = {
    "outbox_table": "contract_lifecycle_appgen_outbox_event",
    "inbox_table": "contract_lifecycle_appgen_inbox_event",
    "dead_letter_table": "contract_lifecycle_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = tuple(OPERATION_SPECS) + (
    "configure_runtime",
    "set_parameter",
    "register_rule",
    "register_schema_extension",
    "receive_event",
)
QUERY_OPERATIONS = ("query_workbench", "build_workbench_view")


class ContractLifecycleServiceFacade(ContractLifecycleService):
    """Named service facade for the source audit and generated app runtime."""


def service_operation_manifest():
    contract = service_contract()
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "service_class": "ContractLifecycleService",
        "command_operations": contract["command_methods"],
        "query_operations": contract["query_methods"],
        "event_contract": event_contract_manifest(),
    }


def service_operation_contracts():
    contracts = tuple(
        {
            **app_operation_plan(operation),
            "transaction_boundary": "owned_datastore_plus_outbox",
        }
        for operation in OPERATION_SPECS
    ) + (
        {
            "operation": "query_workbench",
            "operation_kind": "query",
            "owned_tables": (),
            "read_tables": OWNED_TABLES,
            "emitted_event": None,
            "transaction_boundary": "read_only_projection",
        },
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
    }


def operation_plan(operation, payload=None):
    if operation in OPERATION_SPECS:
        return app_operation_plan(operation, payload)
    manifest = service_operation_manifest()
    if operation in manifest["query_operations"]:
        return {
            "ok": True,
            "operation": operation,
            "operation_kind": "query",
            "payload": dict(payload or {}),
            "side_effects": (),
        }
    return {"ok": False, "operation": operation, "reason": "unknown_operation"}


def smoke_test():
    service = ContractLifecycleService()
    config = service.configure_runtime(
        {
            "database_backend": "postgresql",
            "event_topic": "pbc.contract_lifecycle.events",
            "retry_limit": 5,
            "default_policy": "approval_threshold_policy",
            "agent_write_requires_confirmation": True,
        }
    )
    return {
        "ok": config["ok"] and service_operation_contracts()["ok"],
        "config": config,
        "contracts": service_operation_contracts(),
    }
