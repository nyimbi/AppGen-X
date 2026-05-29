"""Command and query service layer for the loyalty_rewards PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from . import runtime


_SUPPLEMENTAL_ROUTE_HINTS = {
    "configure_runtime": {"method": "PUT", "path": "/loyalty-rewards/configuration"},
    "set_parameter": {"method": "POST", "path": "/loyalty-rewards/parameters"},
    "register_rule": {"method": "POST", "path": "/loyalty-rewards/rules"},
    "register_schema_extension": {"method": "POST", "path": "/loyalty-rewards/schema-extensions"},
    "register_earning_rule": {"method": "POST", "path": "/loyalty-rewards/earning-rules"},
    "build_workbench_view": {"method": "GET", "path": "/loyalty-rewards/workbench"},
    "permissions_contract": {"method": "GET", "path": "/loyalty-rewards/permissions"},
}


def _method_path(route: str) -> tuple[str, str]:
    method, path = route.split(" ", 1)
    return method, path


def _prefix_tables(tables: tuple[str, ...] | list[str] | None) -> tuple[str, ...]:
    prefixed = []
    for table in tuple(tables or ()):
        prefixed.append(table if table.startswith("loyalty_rewards_") else f"loyalty_rewards_{table}")
    return tuple(prefixed)


def _route_backed_contracts() -> tuple[dict, ...]:
    api = runtime.loyalty_rewards_build_api_contract()
    contracts = []
    for route in api["routes"]:
        operation = route.get("command") or route.get("query")
        if not operation:
            continue
        method, path = _method_path(route["route"])
        is_command = "command" in route
        owned_tables = _prefix_tables(route.get("owned_tables", ())) if is_command else ()
        read_tables = () if is_command else _prefix_tables(route.get("owned_tables", ()))
        if is_command and not owned_tables and operation == "receive_event":
            owned_tables = tuple(runtime.LOYALTY_REWARDS_RUNTIME_TABLES[1:])
        contracts.append(
            {
                "operation": operation,
                "operation_kind": "command" if is_command else "query",
                "method": method,
                "path": path,
                "permission": route["requires_permission"],
                "owned_tables": owned_tables,
                "read_tables": read_tables,
                "emitted_event": (tuple(route.get("emits", ())) or (None,))[0] if is_command else None,
                "consumed_event": tuple(route.get("consumes", ())),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
                "idempotency_key": route.get("idempotency_key"),
                "routed": True,
            }
        )
    return tuple(contracts)


_ROUTE_CONTRACTS = _route_backed_contracts()
_ROUTE_INDEX = {contract["operation"]: contract for contract in _ROUTE_CONTRACTS}


def _supplemental_contracts() -> tuple[dict, ...]:
    runtime_service = runtime.loyalty_rewards_build_service_contract()
    all_owned = _prefix_tables(runtime_service.get("mutates_only", ()))
    contracts = []
    for operation in runtime_service.get("command_methods", ()) + runtime_service.get("query_methods", ()):
        if operation in _ROUTE_INDEX:
            continue
        hint = _SUPPLEMENTAL_ROUTE_HINTS.get(operation, {})
        is_command = operation in runtime_service.get("command_methods", ())
        contracts.append(
            {
                "operation": operation,
                "operation_kind": "command" if is_command else "query",
                "method": hint.get("method"),
                "path": hint.get("path"),
                "permission": runtime_service.get("permission_requirements", {}).get(operation),
                "owned_tables": all_owned if is_command and operation != "verify_owned_table_boundary" else (),
                "read_tables": () if is_command else all_owned,
                "emitted_event": None,
                "consumed_event": (),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
                "idempotency_key": None,
                "routed": False,
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _ROUTE_CONTRACTS + _supplemental_contracts()


def service_operation_contracts() -> dict:
    """Return route-bound and standalone service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = runtime.loyalty_rewards_build_service_contract()
    return {
        "ok": runtime_service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] or item["consumed_event"] or item["operation"] == "verify_owned_table_boundary" for item in command_contracts)
        and all(item["read_tables"] or item["operation"] == "permissions_contract" for item in query_contracts),
        "pbc": "loyalty_rewards",
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "route_contracts": _ROUTE_CONTRACTS,
        "runtime_service_contract": runtime_service,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    """Plan one service operation without mutating state."""
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    table_scope = contract["owned_tables"] or contract["read_tables"] or tuple(runtime.LOYALTY_REWARDS_RUNTIME_TABLES)
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": "loyalty_rewards",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract.get("method"), "path": contract.get("path")},
        "permission": contract.get("permission"),
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract.get("emitted_event"),
        "consumed_event": contract.get("consumed_event", ()),
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "idempotency_key": contract.get("idempotency_key"),
        "routed": contract.get("routed", False),
        "side_effects": (),
    }


def _unwrap(payload: dict, *keys: str) -> dict:
    for key in keys:
        if isinstance(payload.get(key), dict):
            return dict(payload[key])
    return dict(payload)


class LoyaltyRewardsService:
    """Executable package-local service facade over the loyalty runtime."""

    def __init__(self, state: dict | None = None):
        self.state = state or runtime.loyalty_rewards_empty_state()

    def _command(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        result = self._apply_command(operation_name, payload)
        if "state" in result:
            self.state = result["state"]
        return {
            "ok": result.get("ok") is True,
            "pbc": "loyalty_rewards",
            "operation": operation_name,
            "operation_kind": "command",
            "payload": payload,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (plan["emitted_event"],) if plan.get("emitted_event") else (),
            "consumes": plan.get("consumed_event", ()),
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def _query(self, operation_name: str, payload: dict | None = None) -> dict:
        payload = dict(payload or {})
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        result = self._apply_query(operation_name, payload)
        return {
            "ok": result.get("ok") is True,
            "pbc": "loyalty_rewards",
            "operation": operation_name,
            "operation_kind": "query",
            "payload": payload,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "emits": (),
            "result": result,
            "state": self.state,
            "side_effects": (),
        }

    def _apply_command(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "configure_runtime":
            return runtime.loyalty_rewards_configure_runtime(self.state, payload.get("configuration", payload))
        if operation_name == "set_parameter":
            return runtime.loyalty_rewards_set_parameter(self.state, payload["name"], payload["value"])
        if operation_name == "register_rule":
            return runtime.loyalty_rewards_register_rule(self.state, payload.get("rule", payload))
        if operation_name == "register_schema_extension":
            return runtime.loyalty_rewards_register_schema_extension(self.state, payload["table"], payload["fields"])
        if operation_name == "register_earning_rule":
            return runtime.loyalty_rewards_register_earning_rule(self.state, payload.get("earning_rule", payload))
        if operation_name == "enroll_member":
            return runtime.loyalty_rewards_enroll_member(self.state, _unwrap(payload, "account", "member"))
        if operation_name == "receive_event":
            return runtime.loyalty_rewards_receive_event(self.state, payload.get("envelope", payload.get("event", payload)), simulate_failure=payload.get("simulate_failure", False))
        if operation_name == "issue_points":
            return runtime.loyalty_rewards_issue_points(self.state, _unwrap(payload, "ledger_entry", "command"))
        if operation_name == "adjust_points":
            return runtime.loyalty_rewards_adjust_points(self.state, _unwrap(payload, "adjustment", "command"))
        if operation_name == "create_redemption":
            return runtime.loyalty_rewards_create_redemption(self.state, _unwrap(payload, "redemption", "command"))
        if operation_name == "expire_points":
            return runtime.loyalty_rewards_expire_points(self.state, payload["account_id"], points=int(payload["points"]))
        if operation_name == "qualify_tier":
            return runtime.loyalty_rewards_qualify_tier(self.state, payload["account_id"])
        if operation_name == "grant_referral_reward":
            return runtime.loyalty_rewards_grant_referral_reward(self.state, _unwrap(payload, "referral", "command"))
        if operation_name == "record_partner_accrual":
            return runtime.loyalty_rewards_record_partner_accrual(self.state, _unwrap(payload, "partner_accrual", "command"))
        if operation_name == "evaluate_offer_eligibility":
            return runtime.loyalty_rewards_evaluate_offer_eligibility(self.state, _unwrap(payload, "eligibility", "command"))
        if operation_name == "schedule_expiration":
            return runtime.loyalty_rewards_schedule_expiration(self.state, _unwrap(payload, "schedule", "command"))
        if operation_name == "snapshot_liability":
            return runtime.loyalty_rewards_snapshot_liability(self.state, payload["tenant"])
        if operation_name == "review_fraud_risk":
            return runtime.loyalty_rewards_review_fraud_risk(self.state, _unwrap(payload, "review", "command"))
        if operation_name == "score_churn_risk":
            return runtime.loyalty_rewards_score_churn_risk(self.state, _unwrap(payload, "score", "command"))
        if operation_name == "forecast_breakage":
            return runtime.loyalty_rewards_forecast_breakage(self.state, _unwrap(payload, "forecast", "command"))
        if operation_name == "simulate_offer":
            return runtime.loyalty_rewards_simulate_offer(self.state, _unwrap(payload, "simulation", "command"))
        if operation_name == "resolve_loyalty_exception":
            return runtime.loyalty_rewards_resolve_loyalty_exception(self.state, _unwrap(payload, "exception", "command"))
        if operation_name == "reconcile_balance":
            return runtime.loyalty_rewards_reconcile_balance(self.state, payload["account_id"])
        if operation_name == "generate_balance_proof":
            return runtime.loyalty_rewards_generate_balance_proof(self.state, _unwrap(payload, "proof", "command"))
        if operation_name == "screen_rewards_policy":
            return runtime.loyalty_rewards_screen_rewards_policy(self.state, _unwrap(payload, "screening", "command"))
        if operation_name == "run_liability_controls":
            return runtime.loyalty_rewards_run_liability_controls(self.state, payload["tenant"])
        if operation_name == "federate_rewards_view":
            return runtime.loyalty_rewards_federate_rewards_view(self.state, _unwrap(payload, "view", "command"))
        if operation_name == "register_governed_model":
            return runtime.loyalty_rewards_register_governed_model(self.state, _unwrap(payload, "model", "command"))
        if operation_name == "verify_owned_table_boundary":
            return runtime.loyalty_rewards_verify_owned_table_boundary(tuple(payload.get("references", ())))
        raise ValueError(f"Unsupported Loyalty Rewards command: {operation_name}")

    def _apply_query(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "build_workbench_view":
            return runtime.loyalty_rewards_build_workbench_view(self.state, tenant=payload.get("tenant", "tenant_alpha"))
        if operation_name == "build_api_contract":
            return runtime.loyalty_rewards_build_api_contract()
        if operation_name == "build_schema_contract":
            return runtime.loyalty_rewards_build_schema_contract()
        if operation_name == "build_service_contract":
            return runtime.loyalty_rewards_build_service_contract()
        if operation_name == "build_release_evidence":
            from . import release_evidence
            return release_evidence.build_release_evidence()
        if operation_name == "permissions_contract":
            return runtime.loyalty_rewards_permissions_contract()
        raise ValueError(f"Unsupported Loyalty Rewards query: {operation_name}")

    def execute_operation(self, operation_name: str, payload: dict | None = None) -> dict:
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        if plan["operation_kind"] == "command":
            return self._command(operation_name, payload)
        return self._query(operation_name, payload)

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
        "route_contracts": contracts["route_contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "stateful_runtime": True,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute focused service operations through the facade."""
    from . import seed_data

    manifest = service_operation_manifest()
    service = LoyaltyRewardsService()
    configured = service.execute_operation("configure_runtime", {"configuration": seed_data.default_configuration()})
    parameter = service.execute_operation("set_parameter", {"name": "base_points_per_currency_unit", "value": 10.0})
    register_rule = service.execute_operation("register_rule", {"rule": seed_data.default_rules()[0]})
    register_earning_rule = service.execute_operation("register_earning_rule", {"earning_rule": seed_data.default_earning_rules()[0]})
    query = service.execute_operation("build_service_contract", {})
    return {
        "ok": manifest["ok"]
        and configured.get("ok") is True
        and parameter.get("ok") is True
        and register_rule.get("ok") is True
        and register_earning_rule.get("ok") is True
        and query.get("ok") is True,
        "manifest": manifest,
        "result": query,
        "side_effects": (),
    }
