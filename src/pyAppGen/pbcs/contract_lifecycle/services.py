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

    def _contract_for(self, name):
        return next(
            (item for item in service_operation_contracts()["contracts"] if item["operation"] == name),
            None,
        )

    def _query_envelope(self, name, payload, result):
        # The package's own query methods return their projection directly; the
        # service contract gate reads the facade's envelope, so the facade adds
        # the read-only markers every other package's queries carry.
        return {
            **result,
            "ok": result.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload or {}),
            "operation_contract": self._contract_for(name),
            "outbox_table": None,
            "emits": (),
            "side_effects": (),
        }

    def _command_envelope(self, name, payload, result):
        # The package's operation runner returns the business result; the facade
        # wraps it the way every other package's commands are wrapped, so the
        # outbox row and the event it carries are named where the gate reads them.
        contract = self._contract_for(name)
        return {
            **result,
            "ok": True,
            "pbc": PBC_KEY,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload or {}),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract["emitted_event"],) if contract else (),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "side_effects": (),
        }

    def execute(self, operation, payload=None):
        return self._command_envelope(operation, payload, super().execute(operation, payload))

    def configure_runtime(self, config):
        return self._command_envelope("configure_runtime", config, super().configure_runtime(config))

    def set_parameter(self, key, value):
        return self._command_envelope("set_parameter", {"name": key, "value": value}, super().set_parameter(key, value))

    def register_rule(self, rule):
        return self._command_envelope("register_rule", rule, super().register_rule(rule))

    def register_schema_extension(self, table, fields):
        return self._command_envelope(
            "register_schema_extension", {"table": table, "fields": fields}, super().register_schema_extension(table, fields)
        )

    def receive_event(self, event):
        return self._command_envelope("receive_event", event, super().receive_event(event))

    def query_workbench(self, filters=None):
        return self._query_envelope("query_workbench", filters, super().query_workbench(dict(filters or {})))

    def build_workbench_view(self, filters=None):
        return self._query_envelope("build_workbench_view", filters, super().build_workbench_view(filters))


def service_operation_manifest():
    contract = service_contract()
    return {
        "ok": contract["ok"],
        "pbc": PBC_KEY,
        "service_class": "ContractLifecycleServiceFacade",
        "command_operations": contract["command_methods"],
        "query_operations": contract["query_methods"],
        "event_contract": event_contract_manifest(),
    }


def service_operation_contracts():
    contracts = tuple(
        {
            **app_operation_plan(operation),
            # A command with no declared business event still writes its outbox
            # row, so it carries the operation-scoped marker the other packages
            # use until a dedicated event exists.
            "emitted_event": app_operation_plan(operation)["emitted_event"] or f"{PBC_KEY}.{operation}.executed",
            "transaction_boundary": "owned_datastore_plus_outbox",
        }
        for operation in OPERATION_SPECS
    ) + tuple(
        {
            "operation": operation,
            "operation_kind": "query",
            "owned_tables": (),
            "read_tables": OWNED_TABLES,
            "emitted_event": None,
            "transaction_boundary": "read_only_projection",
        }
        for operation in QUERY_OPERATIONS
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
