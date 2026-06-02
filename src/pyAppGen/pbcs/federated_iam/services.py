"""Command service layer for the federated_iam PBC."""

from __future__ import annotations

from dataclasses import dataclass

from . import permissions
from . import seed_data
from .runtime import federated_iam_approve_privileged_access
from .runtime import federated_iam_assign_role
from .runtime import federated_iam_build_api_contract
from .runtime import federated_iam_build_release_evidence
from .runtime import federated_iam_build_schema_contract
from .runtime import federated_iam_build_service_contract
from .runtime import federated_iam_build_workbench_view
from .runtime import federated_iam_configure_runtime
from .runtime import federated_iam_evaluate_policy
from .runtime import federated_iam_grant_token
from .runtime import federated_iam_link_identity
from .runtime import federated_iam_receive_event
from .runtime import federated_iam_register_identity_provider
from .runtime import federated_iam_register_principal
from .runtime import federated_iam_register_rule
from .runtime import federated_iam_register_schema_extension
from .runtime import federated_iam_recommend_exception_resolution
from .runtime import federated_iam_route_authorization
from .runtime import federated_iam_run_control_tests
from .runtime import federated_iam_score_access_risk
from .runtime import federated_iam_set_parameter
from .runtime import federated_iam_simulate_policy_change
from .runtime import federated_iam_verify_credential
from .runtime import federated_iam_verify_owned_table_boundary
from .runtime import federated_iam_forecast_access_risk
from .runtime import federated_iam_generate_policy_proof
from .runtime import federated_iam_parse_access_request
from .runtime import federated_iam_provision_tenant
from .runtime import federated_iam_screen_access_policy


PBC_KEY = "federated_iam"
_COMMANDS = {
    "configure_runtime": federated_iam_configure_runtime,
    "set_parameter": federated_iam_set_parameter,
    "register_rule": federated_iam_register_rule,
    "register_schema_extension": federated_iam_register_schema_extension,
    "receive_event": federated_iam_receive_event,
    "provision_tenant": federated_iam_provision_tenant,
    "register_principal": federated_iam_register_principal,
    "register_identity_provider": federated_iam_register_identity_provider,
    "link_identity": federated_iam_link_identity,
    "verify_credential": federated_iam_verify_credential,
    "assign_role": federated_iam_assign_role,
    "evaluate_policy": federated_iam_evaluate_policy,
    "grant_token": federated_iam_grant_token,
    "approve_privileged_access": federated_iam_approve_privileged_access,
    "run_control_tests": federated_iam_run_control_tests,
    "verify_owned_table_boundary": federated_iam_verify_owned_table_boundary,
}
_QUERIES = {
    "build_workbench_view": federated_iam_build_workbench_view,
    "simulate_policy_change": federated_iam_simulate_policy_change,
    "forecast_access_risk": federated_iam_forecast_access_risk,
    "parse_access_request": federated_iam_parse_access_request,
    "score_access_risk": federated_iam_score_access_risk,
    "recommend_exception_resolution": federated_iam_recommend_exception_resolution,
    "route_authorization": federated_iam_route_authorization,
    "generate_policy_proof": federated_iam_generate_policy_proof,
    "screen_access_policy": federated_iam_screen_access_policy,
    "build_api_contract": federated_iam_build_api_contract,
    "build_schema_contract": federated_iam_build_schema_contract,
    "build_service_contract": federated_iam_build_service_contract,
    "build_release_evidence": federated_iam_build_release_evidence,
}


def _physical_table_name(table: str) -> str:
    return table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"


def _route_contracts() -> tuple[dict, ...]:
    api_contract = federated_iam_build_api_contract()
    contracts = []
    for route in api_contract["routes"]:
        method, path = route["route"].split(" ", 1)
        operation = route.get("command") or route.get("query")
        operation_kind = "command" if route.get("command") else "query"
        owned_tables = tuple(_physical_table_name(table) for table in route.get("owned_tables", ()))
        contracts.append(
            {
                "operation": operation,
                "operation_kind": operation_kind,
                "method": method,
                "path": path,
                "permission": route["requires_permission"],
                "owned_tables": owned_tables if operation_kind == "command" else (),
                "read_tables": owned_tables if operation_kind == "query" else (),
                "emitted_event": tuple(route.get("emits", ())),
                "consumed_events": tuple(route.get("consumes", ())),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": route["event_contract"],
                "event_topic": route["event_topic"],
                "idempotency_required": "idempotency_key" in route,
                "idempotency_key": route.get("idempotency_key"),
                "shared_table_access": route.get("shared_table_access", False),
                "stream_engine_picker_visible": False,
                "dependency_apis": tuple(route.get("dependency_apis", ())),
                "dependency_projections": tuple(route.get("dependency_projections", ())),
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _route_contracts()


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    commands = tuple(item["operation"] for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    queries = tuple(item["operation"] for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["stream_engine_picker_visible"] is False for item in OPERATION_CONTRACTS)
        and all(item["shared_table_access"] is False for item in OPERATION_CONTRACTS),
        "pbc": PBC_KEY,
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": commands,
        "query_operations": queries,
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
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
        "consumed_events": contract["consumed_events"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "dependency_apis": contract["dependency_apis"],
        "dependency_projections": contract["dependency_projections"],
        "idempotency_required": contract["idempotency_required"],
        "idempotency_key": contract["idempotency_key"],
        "side_effects": (),
    }


@dataclass
class FederatedIamService:
    """Stateful but deterministic wrapper around the runtime service surface."""

    state: dict | None = None
    granted_permissions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.state is None:
            self.state = seed_data.build_seed_state()["state"]

    def _authorize(self, operation_name: str) -> dict:
        return permissions.authorize(operation_name, self.granted_permissions)

    def _execute_command(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        auth = self._authorize(operation_name)
        if not auth["allowed"]:
            return {
                "ok": False,
                "reason": "forbidden",
                "operation": operation_name,
                "authorization": auth,
                "operation_contract": plan,
                "side_effects": (),
            }
        result = self._invoke_command(operation_name, payload)
        if "state" in result:
            self.state = result["state"]
        return {
            "ok": result.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": "command",
            "payload": dict(payload),
            "authorization": auth,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "outbox_table": "federated_iam_appgen_outbox_event",
            "emits": plan["emitted_event"],
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def _execute_query(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        auth = self._authorize(operation_name)
        if not auth["allowed"]:
            return {
                "ok": False,
                "reason": "forbidden",
                "operation": operation_name,
                "authorization": auth,
                "operation_contract": plan,
                "side_effects": (),
            }
        result = self._invoke_query(operation_name, payload)
        return {
            "ok": result.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": "query",
            "payload": dict(payload),
            "authorization": auth,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "read_only": True,
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def _invoke_command(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "configure_runtime":
            return _COMMANDS[operation_name](self.state, payload)
        if operation_name == "set_parameter":
            return _COMMANDS[operation_name](self.state, payload["name"], payload["value"])
        if operation_name == "register_rule":
            return _COMMANDS[operation_name](self.state, payload)
        if operation_name == "register_schema_extension":
            return _COMMANDS[operation_name](self.state, payload["table"], payload["fields"])
        if operation_name == "receive_event":
            return _COMMANDS[operation_name](self.state, payload)
        if operation_name == "run_control_tests":
            return _COMMANDS[operation_name](self.state)
        if operation_name == "verify_owned_table_boundary":
            return _COMMANDS[operation_name](tuple(payload.get("references", ())))
        return _COMMANDS[operation_name](self.state, payload)

    def _invoke_query(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "build_workbench_view":
            tenant = payload.get("tenant") or next(iter(self.state["tenants"]), "tenant_seed_alpha")
            return _QUERIES[operation_name](self.state, tenant=tenant)
        if operation_name == "simulate_policy_change":
            return _QUERIES[operation_name](self.state, payload["principal_id"], proposed_role=payload["proposed_role"])
        if operation_name == "forecast_access_risk":
            return _QUERIES[operation_name](tuple(payload["risk_path"]), horizon_days=payload["horizon_days"])
        if operation_name == "parse_access_request":
            return _QUERIES[operation_name](payload["text"])
        if operation_name == "score_access_risk":
            return _QUERIES[operation_name](payload)
        if operation_name == "recommend_exception_resolution":
            return _QUERIES[operation_name](payload["exception_type"])
        if operation_name == "route_authorization":
            return _QUERIES[operation_name](payload["event"], rails=tuple(payload["rails"]))
        if operation_name == "generate_policy_proof":
            return _QUERIES[operation_name](self.state, payload["decision_id"], disclosure=tuple(payload["disclosure"]))
        if operation_name == "screen_access_policy":
            return _QUERIES[operation_name](self.state, payload["decision_id"], restricted_actions=tuple(payload["restricted_actions"]))
        return _QUERIES[operation_name]()

    def execute(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
        if contract is None:
            return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
        if contract["operation_kind"] == "command":
            return self._execute_command(operation_name, payload)
        return self._execute_query(operation_name, payload)


def service_operation_manifest() -> dict:
    """Return the executable service operation surface."""
    runtime_contract = federated_iam_build_service_contract()
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"] and runtime_contract["ok"],
        "pbc": PBC_KEY,
        "service_class": "FederatedIamService",
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": runtime_contract["transaction_boundary"],
        "outbox_table": runtime_contract["retry_dead_letter_evidence"]["outbox_table"],
        "service_contract": runtime_contract,
        "side_effects": (),
    }


def create_seeded_service(granted_permissions: tuple[str, ...] = ()) -> FederatedIamService:
    """Return a service preloaded with package seed state."""
    effective_permissions = granted_permissions or tuple(permissions.permission_manifest()["permissions"])
    return FederatedIamService(state=seed_data.build_seed_state()["state"], granted_permissions=effective_permissions)


def smoke_test() -> dict:
    """Execute seed-backed command and query operations through the facade."""
    manifest = service_operation_manifest()
    service = create_seeded_service()
    command_result = service.execute(
        "set_parameter",
        {"name": "token_ttl_minutes", "value": 90},
    )
    query_result = service.execute(
        "build_workbench_view",
        {"tenant": "tenant_seed_alpha"},
    )
    return {
        "ok": manifest["ok"] and command_result["ok"] and query_result["ok"],
        "manifest": manifest,
        "result": command_result,
        "query": query_result,
        "side_effects": (),
    }
