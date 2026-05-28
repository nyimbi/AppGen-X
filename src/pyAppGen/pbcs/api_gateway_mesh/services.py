"""Command service layer for the api_gateway_mesh PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from . import runtime
from .runtime import api_gateway_mesh_build_api_contract
from .runtime import api_gateway_mesh_build_service_contract

PBC_KEY = "api_gateway_mesh"


def _route_to_contract(route: dict) -> dict:
    method, path = route["route"].split(" ", 1)
    operation = route.get("command") or route.get("query")
    operation_kind = "command" if route.get("command") else "query"
    owned_tables = tuple(
        table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        for table in route.get("owned_tables", ())
    )
    is_command = operation_kind == "command"
    return {
        "operation": operation,
        "operation_kind": operation_kind,
        "method": method,
        "path": path,
        "permission": route["requires_permission"],
        "owned_tables": owned_tables if is_command else (),
        "read_tables": () if is_command else owned_tables,
        "emitted_event": (route.get("emits") or (f"{PBC_KEY}.{operation}.executed",))[0] if is_command else None,
        "consumed_event": tuple(route.get("consumes", ())),
        "idempotency_key": route.get("idempotency_key"),
        "dependency_apis": tuple(route.get("dependency_apis", ())),
        "dependency_projections": tuple(route.get("dependency_projections", ())),
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
    }


OPERATION_CONTRACTS = tuple(
    _route_to_contract(route) for route in api_gateway_mesh_build_api_contract()["routes"]
)


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = api_gateway_mesh_build_service_contract()
    return {
        "ok": runtime_service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] or item["consumed_event"] for item in command_contracts)
        and all(item["read_tables"] for item in query_contracts),
        "pbc": PBC_KEY,
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
    return {
        "ok": bool(contract["owned_tables"] or contract["read_tables"] or contract["consumed_event"]),
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "consumed_event": contract["consumed_event"],
        "idempotency_key": contract["idempotency_key"],
        "dependency_apis": contract["dependency_apis"],
        "dependency_projections": contract["dependency_projections"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


class ApiGatewayMeshService:
    """Executable command facade with explicit-state runtime execution."""

    _STATEFUL_OPERATIONS = {
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "register_service",
        "register_mtls_identity",
        "publish_route",
        "apply_rate_limit",
        "record_health",
        "record_traffic_sample",
        "build_service_map",
        "build_workbench_view",
        "analyze_route_collisions",
        "build_route_publication_safety_case",
        "run_control_tests",
        "run_resilience_drill",
    }

    def _invoke_runtime(self, operation_name: str, payload: dict) -> dict:
        state = payload.get("state")
        if operation_name in self._STATEFUL_OPERATIONS and state is None:
            return {
                "ok": False,
                "executed": False,
                "reason": "state_required",
                "required_payload_keys": ("state",),
            }

        if operation_name == "configure_runtime":
            configuration = dict(payload.get("configuration", payload))
            configuration.pop("state", None)
            return runtime.api_gateway_mesh_configure_runtime(state, configuration)
        if operation_name == "set_parameter":
            return runtime.api_gateway_mesh_set_parameter(
                state,
                payload.get("name") or payload.get("parameter_name"),
                payload.get("value"),
            )
        if operation_name == "register_rule":
            rule = dict(payload.get("rule", payload))
            rule.pop("state", None)
            return runtime.api_gateway_mesh_register_rule(state, rule)
        if operation_name == "register_schema_extension":
            return runtime.api_gateway_mesh_register_schema_extension(
                state,
                payload["table"],
                dict(payload["fields"]),
            )
        if operation_name == "receive_event":
            event = dict(payload.get("event", payload))
            event.pop("state", None)
            return runtime.api_gateway_mesh_receive_event(
                state,
                event,
                simulate_failure=bool(payload.get("simulate_failure", False)),
            )
        if operation_name == "register_service":
            service = dict(payload.get("service", payload))
            service.pop("state", None)
            return runtime.api_gateway_mesh_register_service(state, service)
        if operation_name == "register_mtls_identity":
            identity = dict(payload.get("identity", payload))
            identity.pop("state", None)
            return runtime.api_gateway_mesh_register_mtls_identity(state, identity)
        if operation_name == "publish_route":
            route = dict(payload.get("route", payload))
            route.pop("state", None)
            return runtime.api_gateway_mesh_publish_route(state, route)
        if operation_name == "apply_rate_limit":
            policy = dict(payload.get("policy", payload))
            policy.pop("state", None)
            return runtime.api_gateway_mesh_apply_rate_limit(state, policy)
        if operation_name == "record_health":
            health = dict(payload.get("health", payload))
            health.pop("state", None)
            return runtime.api_gateway_mesh_record_health(state, health)
        if operation_name == "record_traffic_sample":
            sample = dict(payload.get("sample", payload))
            sample.pop("state", None)
            return runtime.api_gateway_mesh_record_traffic_sample(state, sample)
        if operation_name == "build_service_map":
            return runtime.api_gateway_mesh_build_service_map(state, tenant=payload["tenant"])
        if operation_name == "build_workbench_view":
            return runtime.api_gateway_mesh_build_workbench_view(state, tenant=payload["tenant"])
        if operation_name == "analyze_route_collisions":
            route = dict(payload.get("route", payload))
            route.pop("state", None)
            return runtime.api_gateway_mesh_analyze_route_collisions(state, route)
        if operation_name == "build_route_publication_safety_case":
            route = dict(payload.get("route", payload))
            route.pop("state", None)
            return runtime.api_gateway_mesh_build_route_publication_safety_case(state, route)
        if operation_name == "run_control_tests":
            return runtime.api_gateway_mesh_run_control_tests(state)
        if operation_name == "run_resilience_drill":
            return runtime.api_gateway_mesh_run_resilience_drill(state, payload["scenario"])
        if operation_name == "forecast_route_health":
            return runtime.api_gateway_mesh_forecast_route_health(tuple(payload["health_path"]), horizon_minutes=payload["horizon_minutes"])
        if operation_name == "parse_route_request":
            return runtime.api_gateway_mesh_parse_route_request(payload["text"])
        if operation_name == "score_route_risk":
            return runtime.api_gateway_mesh_score_route_risk(dict(payload["signals"]))
        if operation_name == "recommend_exception_resolution":
            return runtime.api_gateway_mesh_recommend_exception_resolution(payload["exception_type"])
        if operation_name == "select_route":
            return runtime.api_gateway_mesh_select_route(dict(payload["event"]), rails=tuple(payload["rails"]))
        if operation_name == "generate_route_proof":
            return runtime.api_gateway_mesh_generate_route_proof(state, payload["route_id"], disclosure=tuple(payload["disclosure"]))
        if operation_name == "screen_policy":
            return runtime.api_gateway_mesh_screen_policy(state, payload["route_id"], restricted_paths=tuple(payload["restricted_paths"]))
        if operation_name == "federate_service_view":
            return runtime.api_gateway_mesh_federate_service_view(state, payload["route_id"], systems=tuple(payload["systems"]))
        if operation_name == "verify_service_identity":
            return runtime.api_gateway_mesh_verify_service_identity(dict(payload["identity"]))
        if operation_name == "rotate_crypto_epoch":
            return runtime.api_gateway_mesh_rotate_crypto_epoch(state, payload["algorithm"])
        if operation_name == "schedule_carbon_aware_routing":
            return runtime.api_gateway_mesh_schedule_carbon_aware_routing(tuple(payload["windows"]))
        if operation_name == "optimize_routes":
            return runtime.api_gateway_mesh_optimize_routes(tuple(payload["candidates"]))
        if operation_name == "allocate_traffic":
            return runtime.api_gateway_mesh_allocate_traffic(tuple(payload["upstreams"]), requests=payload["requests"])
        if operation_name == "detect_traffic_anomaly":
            return runtime.api_gateway_mesh_detect_traffic_anomaly(state)
        if operation_name == "model_stochastic_traffic_exposure":
            return runtime.api_gateway_mesh_model_stochastic_traffic_exposure(
                traffic_path=tuple(payload["traffic_path"]),
                volatility=payload["volatility"],
            )
        if operation_name == "register_governed_model":
            return runtime.api_gateway_mesh_register_governed_model(payload["name"], dict(payload["metadata"]))
        if operation_name == "build_api_contract":
            return runtime.api_gateway_mesh_build_api_contract()
        if operation_name == "build_schema_contract":
            return runtime.api_gateway_mesh_build_schema_contract()
        if operation_name == "build_service_contract":
            return runtime.api_gateway_mesh_build_service_contract()
        if operation_name == "build_release_evidence":
            return runtime.api_gateway_mesh_build_release_evidence()
        if operation_name == "verify_owned_table_boundary":
            return runtime.api_gateway_mesh_verify_owned_table_boundary(tuple(payload.get("references", ())))

        return {"ok": False, "executed": False, "reason": "unsupported_operation"}

    def execute_operation(self, operation_name: str, payload: dict | None = None) -> dict:
        plan = operation_plan(operation_name, payload)
        supplied = dict(payload or {})
        result = {
            "ok": plan["ok"],
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": plan.get("operation_kind"),
            "payload": supplied,
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "executed": False,
            "side_effects": (),
        }
        if plan.get("operation_kind") == "command":
            result.update(
                {
                    "command": operation_name,
                    "read_only": False,
                    "outbox_table": EVENT_CONTRACT["outbox_table"],
                    "emits": (plan.get("emitted_event"),) if plan.get("emitted_event") else (),
                }
            )
        elif plan.get("operation_kind") == "query":
            result.update({"query": operation_name, "read_only": True, "outbox_table": None, "emits": ()})
        if plan["ok"]:
            execution = self._invoke_runtime(operation_name, supplied)
            if execution.get("executed") is not False or execution.get("reason") != "state_required":
                result["executed"] = execution.get("executed", True)
                result["runtime_result"] = execution
                result["ok"] = execution.get("ok", result["ok"])
                for field in (
                    "state",
                    "configuration",
                    "parameter",
                    "rule",
                    "schema_extension",
                    "handler",
                    "service",
                    "identity",
                    "route",
                    "rate_limit",
                    "service_health",
                    "traffic_sample",
                    "collision_analysis",
                    "safety_case",
                    "checks",
                ):
                    if field in execution:
                        result[field] = execution[field]
            else:
                result["requires_state"] = True
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
        "pbc": PBC_KEY,
        "service_class": ApiGatewayMeshService.__name__,
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
    service = ApiGatewayMeshService()
    operation = manifest["operations"][0] if manifest["operations"] else None
    result = service.execute_operation(operation, {"smoke": True}) if operation else {"ok": False}
    return {"ok": manifest["ok"] and result.get("ok") is True, "manifest": manifest, "result": result, "side_effects": ()}
