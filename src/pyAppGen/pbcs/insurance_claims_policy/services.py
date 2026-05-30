"""Executable service layer for the insurance_claims_policy PBC."""

from __future__ import annotations

from copy import deepcopy

from .events import EVENT_TABLES
from .models import OWNED_TABLES
from .standalone import InsuranceClaimsPolicyStandaloneApp
from .standalone import standalone_manifest

PBC_KEY = "insurance_claims_policy"
READ_SCOPE = OWNED_TABLES


def _command(operation: str, path: str, permission: str, owned_tables: tuple[str, ...], emitted_event: str | None = None) -> dict:
    return {
        "operation": operation,
        "service_method": operation,
        "operation_kind": "command",
        "method": "POST",
        "path": path,
        "permission": permission,
        "owned_tables": owned_tables,
        "read_tables": (),
        "emitted_event": emitted_event,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


def _query(operation: str, path: str, permission: str, read_tables: tuple[str, ...] = READ_SCOPE, *, method: str = "GET") -> dict:
    return {
        "operation": operation,
        "service_method": operation,
        "operation_kind": "query",
        "method": method,
        "path": path,
        "permission": permission,
        "owned_tables": (),
        "read_tables": read_tables,
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
    }


OPERATION_CONTRACTS = (
    _command("configure", "/api/pbc/insurance_claims_policy/runtime/configuration", "insurance_claims_policy.admin", (f"{PBC_KEY}_insurance_runtime_parameter",)),
    _command("register_defaults", "/api/pbc/insurance_claims_policy/runtime/defaults", "insurance_claims_policy.admin", (f"{PBC_KEY}_insurance_runtime_parameter", f"{PBC_KEY}_insurance_policy_rule", f"{PBC_KEY}_insurance_control_assertion", f"{PBC_KEY}_insurance_governed_model")),
    _command("create_insurance_policy", "/api/pbc/insurance_claims_policy/policies", "insurance_claims_policy.create", (f"{PBC_KEY}_insurance_policy",), "PolicyCreated"),
    _command("register_policy_holder", "/api/pbc/insurance_claims_policy/policy-holders", "insurance_claims_policy.update", (f"{PBC_KEY}_policy_holder",)),
    _command("define_policy_coverage", "/api/pbc/insurance_claims_policy/coverages", "insurance_claims_policy.update", (f"{PBC_KEY}_policy_coverage",)),
    _command("record_endorsement", "/api/pbc/insurance_claims_policy/endorsements", "insurance_claims_policy.update", (f"{PBC_KEY}_policy_endorsement",)),
    _command("create_premium_schedule", "/api/pbc/insurance_claims_policy/premium-schedules", "insurance_claims_policy.update", (f"{PBC_KEY}_premium_schedule",)),
    _command("record_premium_payment", "/api/pbc/insurance_claims_policy/premium-payments", "insurance_claims_policy.update", (f"{PBC_KEY}_premium_payment",)),
    _command("open_claim", "/api/pbc/insurance_claims_policy/claims", "insurance_claims_policy.create", (f"{PBC_KEY}_claim_record",), "ClaimOpened"),
    _command("record_loss_event", "/api/pbc/insurance_claims_policy/loss-events", "insurance_claims_policy.update", (f"{PBC_KEY}_loss_event",)),
    _command("register_claimant", "/api/pbc/insurance_claims_policy/claimants", "insurance_claims_policy.update", (f"{PBC_KEY}_claimant",)),
    _command("attach_claim_document", "/api/pbc/insurance_claims_policy/claim-documents", "insurance_claims_policy.update", (f"{PBC_KEY}_claim_document",)),
    _command("determine_coverage", "/api/pbc/insurance_claims_policy/coverage-determinations", "insurance_claims_policy.approve", (f"{PBC_KEY}_coverage_determination",), "CoverageDetermined"),
    _command("set_claim_reserve", "/api/pbc/insurance_claims_policy/claim-reserves", "insurance_claims_policy.approve", (f"{PBC_KEY}_claim_reserve",), "ReserveChanged"),
    _command("record_reserve_change", "/api/pbc/insurance_claims_policy/reserve-changes", "insurance_claims_policy.approve", (f"{PBC_KEY}_reserve_change", f"{PBC_KEY}_claim_reserve"), "ReserveChanged"),
    _command("adjudicate_claim", "/api/pbc/insurance_claims_policy/adjudications", "insurance_claims_policy.approve", (f"{PBC_KEY}_claim_adjudication",), "ClaimAdjudicated"),
    _command("create_settlement_offer", "/api/pbc/insurance_claims_policy/settlement-offers", "insurance_claims_policy.approve", (f"{PBC_KEY}_settlement_offer",)),
    _command("execute_settlement_payment", "/api/pbc/insurance_claims_policy/settlement-payments", "insurance_claims_policy.approve", (f"{PBC_KEY}_settlement_payment",), "SettlementPaid"),
    _command("record_subrogation_recovery", "/api/pbc/insurance_claims_policy/recoveries", "insurance_claims_policy.approve", (f"{PBC_KEY}_subrogation_recovery",)),
    _command("send_claim_communication", "/api/pbc/insurance_claims_policy/communications", "insurance_claims_policy.update", (f"{PBC_KEY}_claim_communication",)),
    _command("score_fraud_indicator", "/api/pbc/insurance_claims_policy/fraud-indicators", "insurance_claims_policy.approve", (f"{PBC_KEY}_fraud_indicator",)),
    _command("resolve_claim_exception", "/api/pbc/insurance_claims_policy/exceptions/resolve", "insurance_claims_policy.approve", (f"{PBC_KEY}_claim_exception_case",)),
    _command("compile_insurance_rule", "/api/pbc/insurance_claims_policy/runtime/rules/compile", "insurance_claims_policy.admin", (f"{PBC_KEY}_insurance_policy_rule",)),
    _command("register_schema_extension", "/api/pbc/insurance_claims_policy/runtime/schema-extensions", "insurance_claims_policy.admin", (f"{PBC_KEY}_insurance_schema_extension",)),
    _query("simulate_loss_exposure", "/api/pbc/insurance_claims_policy/simulations/loss-exposure", "insurance_claims_policy.read", method="POST"),
    _command("receive_event", "/api/pbc/insurance_claims_policy/events/inbox", "insurance_claims_policy.admin", (EVENT_TABLES["inbox_table"], EVENT_TABLES["dead_letter_table"])),
    _query("document_intake", "/api/pbc/insurance_claims_policy/assistant/document-intake", "insurance_claims_policy.read", method="POST"),
    _query("crud_mutation_plan", "/api/pbc/insurance_claims_policy/assistant/crud-plan", "insurance_claims_policy.read", method="POST"),
    _query("get_policy_snapshot", "/api/pbc/insurance_claims_policy/policies/snapshot", "insurance_claims_policy.read", method="POST"),
    _query("get_claim_snapshot", "/api/pbc/insurance_claims_policy/claims/snapshot", "insurance_claims_policy.read", method="POST"),
    _query("workbench", "/api/pbc/insurance_claims_policy/workbench", "insurance_claims_policy.read"),
    _query("release_snapshot", "/api/pbc/insurance_claims_policy/release-snapshot", "insurance_claims_policy.read"),
)

_OPERATION_INDEX = {item["operation"]: item for item in OPERATION_CONTRACTS}


class InsuranceClaimsPolicyService:
    """Stateful package-local service facade backed by the standalone app."""

    def __init__(self, state: dict | None = None):
        self.app = InsuranceClaimsPolicyStandaloneApp(state=state)

    @property
    def state(self) -> dict:
        return self.app.state

    def _execute(self, operation_name: str, payload: dict | None = None) -> dict:
        contract = _OPERATION_INDEX.get(operation_name)
        if contract is None:
            return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
        supplied = deepcopy(dict(payload or {}))
        handler = getattr(self.app, operation_name)
        if operation_name == "configure":
            result = handler(supplied.get("configuration", supplied))
        elif operation_name == "register_defaults":
            result = handler(tenant=supplied.get("tenant", "tenant_demo"))
        elif operation_name == "set_parameter":
            result = self.app.set_parameter(supplied["name"], supplied["value"])
        elif operation_name == "register_rule":
            result = self.app.register_rule(supplied.get("rule", supplied))
        elif operation_name == "register_schema_extension":
            result = self.app.register_schema_extension(supplied.get("extension", supplied))
        elif operation_name == "document_intake":
            result = handler(supplied.get("document", ""), supplied.get("instruction", ""))
        elif operation_name == "crud_mutation_plan":
            result = handler(supplied.get("action", "create"), supplied.get("table"), supplied.get("payload"))
        elif operation_name in {"get_policy_snapshot", "get_claim_snapshot"}:
            identifier = supplied.get("policy_id") if operation_name == "get_policy_snapshot" else supplied.get("claim_id")
            result = handler(identifier)
        elif operation_name == "workbench":
            result = handler(tenant=supplied.get("tenant"), permissions=supplied.get("permissions"))
        elif operation_name == "release_snapshot":
            result = handler()
        elif operation_name == "receive_event":
            result = handler(supplied.get("envelope", supplied))
        else:
            result = handler(supplied)
        return {
            "ok": result.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": contract["operation_kind"],
            "payload": supplied,
            "operation_contract": contract,
            "transaction_boundary": contract["transaction_boundary"],
            "read_only": contract["operation_kind"] == "query",
            "outbox_table": EVENT_TABLES["outbox_table"] if contract["operation_kind"] == "command" else None,
            "emits": (contract["emitted_event"],) if contract.get("emitted_event") else (),
            "result": result,
            "state": self.app.state,
            "side_effects": (),
        }

    def __getattr__(self, name: str):
        if name in _OPERATION_INDEX:
            return lambda payload=None, _name=name: self._execute(_name, payload)
        raise AttributeError(name)


def service_operation_contracts() -> dict:
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] and not item["read_tables"] for item in command_contracts)
        and all(item["read_tables"] and not item["owned_tables"] for item in query_contracts),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def service_operation_manifest() -> dict:
    manifest = standalone_manifest()
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": "InsuranceClaimsPolicyService",
        "service_methods": manifest["service_methods"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "outbox_table": EVENT_TABLES["outbox_table"],
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    contract = _OPERATION_INDEX.get(operation_name)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    return {
        "ok": True,
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
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = InsuranceClaimsPolicyService()
    service.configure({"configuration": {"database_backend": "postgresql", "event_topic": "pbc.insurance_claims_policy.events"}})
    service.register_defaults({"tenant": "tenant_smoke"})
    policy = service.create_insurance_policy({"tenant": "tenant_smoke", "policy_number": "POL-SMOKE"})
    query = service.workbench({"tenant": "tenant_smoke"})
    return {
        "ok": service_operation_contracts()["ok"] and policy["ok"] and query["ok"],
        "policy": policy,
        "query": query,
        "side_effects": (),
    }
