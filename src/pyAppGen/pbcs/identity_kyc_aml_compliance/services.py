"""Service layer for the identity KYC / AML slice."""

from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS, execute_domain_operation
from .runtime import (
    PBC_KEY,
    identity_kyc_aml_compliance_build_service_contract,
    identity_kyc_aml_compliance_empty_state,
    identity_kyc_aml_compliance_operation_registry,
)

EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COMMAND_OPERATIONS = identity_kyc_aml_compliance_build_service_contract()["command_methods"]
QUERY_OPERATIONS = identity_kyc_aml_compliance_build_service_contract()["query_methods"]


def _operation_contract(name, kind):
    if name in DOMAIN_OPERATIONS:
        plan = execute_domain_operation(name, {})
        owned_tables = plan.get("owned_tables", ())
        emitted_event = plan.get("emitted_event")
    else:
        owned_tables = () if kind == "query" else (f"{PBC_KEY}_kyc_profile",)
        emitted_event = None if kind == "query" else "IdentityKycAmlComplianceUpdated"
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": owned_tables if kind == "command" else (),
        "read_tables": owned_tables if kind == "query" else (),
        "emitted_event": emitted_event,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class IdentityKycAmlComplianceService:
    def __init__(self, state=None):
        self.state = identity_kyc_aml_compliance_empty_state() if state is None else state
        self._registry = identity_kyc_aml_compliance_operation_registry()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name == "parse_document_instruction":
            result = self._registry[name](payload.get("document", ""), payload.get("instruction", ""))
            return {**result, "operation": name, "operation_kind": "command", "read_only": False, "payload": dict(payload)}
        result = self._registry[name](self.state, payload)
        self.state = result.get("state", self.state)
        return {
            **result,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "command"),
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (() if name == "run_advanced_assessment" else (result.get("event", {}) or {}).get("event_type",)),
            "transaction_boundary": "owned_datastore_plus_outbox",
        }

    def _query(self, name, payload):
        if name == "build_workbench_view":
            result = self._registry[name](self.state, tenant=payload.get("tenant", "default"))
        elif name == "build_detail_view":
            result = self._registry[name](self.state, payload["profile_id"])
        else:
            result = self._registry[name](self.state, payload)
        return {
            **result,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": _operation_contract(name, "query"),
            "outbox_table": None,
            "emits": (),
        }


def service_operation_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "IdentityKycAmlComplianceService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


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
    service = IdentityKycAmlComplianceService()
    profile = service.create_kyc_profile(
        {
            "tenant": "tenant-smoke",
            "subject_name": "Test User",
            "customer_type": "individual",
            "jurisdiction": "KE",
            "product_exposure": "checking",
            "channel": "remote",
            "expected_activity": "salary",
        }
    )
    query = service.build_workbench_view({"tenant": "tenant-smoke"})
    return {"ok": profile["ok"] and query["ok"] and service_operation_contracts()["ok"], "command": profile, "query": query, "side_effects": ()}
