"""Command and query service layer for the streaming_analytics PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from . import runtime


PBC_KEY = "streaming_analytics"


def _method_path(route: str) -> tuple[str, str]:
    method, path = route.split(" ", 1)
    return method, path


def _operation_name(route: dict) -> str | None:
    return route.get("command") or route.get("query")


def _table_scope(route: dict) -> tuple[str, ...]:
    return tuple(
        table if table.startswith(f"{PBC_KEY}_") else f"{PBC_KEY}_{table}"
        for table in route.get("owned_tables", ())
    )


def _build_operation_contracts() -> tuple[dict, ...]:
    api_contract = runtime.streaming_analytics_build_api_contract()
    contracts = []
    for route in api_contract["routes"]:
        operation = _operation_name(route)
        if not operation:
            continue
        method, path = _method_path(route["route"])
        kind = "command" if "command" in route else "query"
        tables = _table_scope(route)
        contracts.append(
            {
                "operation": operation,
                "operation_kind": kind,
                "method": method,
                "path": f"/api/pbc/{PBC_KEY}{path}",
                "permission": route["requires_permission"],
                "owned_tables": tables if kind == "command" else (),
                "read_tables": () if kind == "command" else tables,
                "emitted_event": (tuple(route.get("emits", ())) or (None,))[0] if kind == "command" else None,
                "consumed_event": tuple(route.get("consumes", ())),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
                "idempotency_key": route.get("idempotency_key") if kind == "command" else None,
                "shared_table_access": False,
                "stream_engine_picker_visible": False,
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _build_operation_contracts()


def service_operation_contracts() -> dict:
    """Return route-bound service operation contracts for this PBC."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = runtime.streaming_analytics_build_service_contract()
    return {
        "ok": runtime_service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] or item["operation"] == "receive_event" for item in command_contracts)
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
        "ok": True,
        "pbc": PBC_KEY,
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "consumed_event": contract["consumed_event"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "idempotency_key": contract["idempotency_key"],
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


class StreamingAnalyticsService:
    """Executable package-local service facade over the streaming analytics runtime."""

    def __init__(self, state: dict | None = None):
        self.state = state or runtime.streaming_analytics_empty_state()

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
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": "command",
            "payload": payload,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (plan["emitted_event"],) if plan["emitted_event"] else (),
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
            "ok": result.get("ok") is True if isinstance(result, dict) and "ok" in result else True,
            "pbc": PBC_KEY,
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
            return runtime.streaming_analytics_configure_runtime(self.state, payload["configuration"])
        if operation_name == "set_parameter":
            return runtime.streaming_analytics_set_parameter(self.state, payload["name"], payload["value"])
        if operation_name == "register_rule":
            return runtime.streaming_analytics_register_rule(self.state, payload["rule"])
        if operation_name == "register_schema_extension":
            return runtime.streaming_analytics_register_schema_extension(self.state, payload["table"], payload["fields"])
        if operation_name == "register_metric_stream":
            return runtime.streaming_analytics_register_metric_stream(self.state, payload["stream"])
        if operation_name == "define_window":
            return runtime.streaming_analytics_define_window(self.state, payload["window"])
        if operation_name == "receive_event":
            return runtime.streaming_analytics_receive_event(self.state, payload["envelope"], simulate_failure=payload.get("simulate_failure", False))
        if operation_name == "ingest_metric_event":
            return runtime.streaming_analytics_ingest_metric_event(self.state, payload["event"])
        if operation_name == "create_dashboard_projection":
            return runtime.streaming_analytics_create_dashboard_projection(self.state, payload["projection"])
        if operation_name == "record_ingestion_checkpoint":
            return runtime.streaming_analytics_record_ingestion_checkpoint(self.state, payload["checkpoint"])
        if operation_name == "evaluate_data_quality":
            return runtime.streaming_analytics_evaluate_data_quality(self.state, payload["event_id"])
        if operation_name == "open_replay_job":
            return runtime.streaming_analytics_open_replay_job(self.state, payload["replay_job"])
        if operation_name == "advance_watermark":
            return runtime.streaming_analytics_advance_watermark(self.state, payload["watermark"])
        if operation_name == "apply_retention_policy":
            return runtime.streaming_analytics_apply_retention_policy(self.state, payload["policy"])
        if operation_name == "evaluate_threshold_alert":
            return runtime.streaming_analytics_evaluate_threshold_alert(self.state, payload["alert"])
        if operation_name == "forecast_metric":
            return runtime.streaming_analytics_forecast_metric(self.state, payload["forecast"])
        if operation_name == "score_operational_risk":
            return runtime.streaming_analytics_score_operational_risk(self.state, payload["risk"])
        if operation_name == "resolve_metric_exception":
            return runtime.streaming_analytics_resolve_metric_exception(self.state, payload["exception"])
        if operation_name == "recompute_window":
            return runtime.streaming_analytics_recompute_window(self.state, payload["recomputation"])
        if operation_name == "run_kpi_controls":
            return runtime.streaming_analytics_run_kpi_controls(self.state, payload["assertion"])
        if operation_name == "generate_snapshot_proof":
            return runtime.streaming_analytics_generate_snapshot_proof(self.state, payload["proof"])
        if operation_name == "screen_metric_policy":
            return runtime.streaming_analytics_screen_metric_policy(self.state, payload["screening"])
        if operation_name == "build_analytics_federation_view":
            return runtime.streaming_analytics_build_analytics_federation_view(self.state, payload["view"])
        if operation_name == "register_governed_model":
            return runtime.streaming_analytics_register_governed_model(self.state, payload["model"])
        raise ValueError(f"Unsupported Streaming Analytics command: {operation_name}")

    def _apply_query(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "kpi_snapshot":
            tenant = payload.get("tenant")
            snapshots = tuple(
                item
                for item in self.state.get("kpi_snapshots", {}).values()
                if tenant is None or item["tenant"] == tenant
            )
            return {"ok": True, "items": snapshots, "count": len(snapshots), "tenant": tenant}
        if operation_name == "dashboard_projection":
            tenant = payload.get("tenant")
            projections = tuple(
                item
                for item in self.state.get("dashboard_projections", {}).values()
                if tenant is None or item["tenant"] == tenant
            )
            return {"ok": True, "items": projections, "count": len(projections), "tenant": tenant}
        if operation_name == "build_workbench_view":
            return runtime.streaming_analytics_build_workbench_view(self.state, tenant=payload["tenant"])
        if operation_name == "build_api_contract":
            return runtime.streaming_analytics_build_api_contract()
        if operation_name == "build_schema_contract":
            return runtime.streaming_analytics_build_schema_contract()
        if operation_name == "build_service_contract":
            return runtime.streaming_analytics_build_service_contract()
        if operation_name == "build_release_evidence":
            from . import release_evidence
            return release_evidence.build_release_evidence()
        if operation_name == "permissions_contract":
            return runtime.streaming_analytics_permissions_contract()
        raise ValueError(f"Unsupported Streaming Analytics query: {operation_name}")

    def execute_operation(self, operation_name: str, payload: dict | None = None) -> dict:
        contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
        if contract is None:
            return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
        if contract["operation_kind"] == "command":
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
        "pbc": PBC_KEY,
        "service_class": StreamingAnalyticsService.__name__,
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute configuration, one command, and one query through the facade."""
    service = StreamingAnalyticsService()
    service.state = runtime.streaming_analytics_configure_runtime(
        service.state,
        {
            "database_backend": "postgresql",
            "event_topic": runtime.STREAMING_ANALYTICS_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_timezone": "UTC",
            "supported_event_types": ("audit", "order", "payment", "operational"),
            "supported_regions": ("US",),
            "retention_days": 90,
            "watermark_seconds": 120,
            "aggregation_mode": "policy",
            "workbench_limit": 100,
        },
    )["state"]
    service.state = runtime.streaming_analytics_set_parameter(service.state, "quality_score_threshold", 0.9)["state"]
    service.state = runtime.streaming_analytics_set_parameter(service.state, "workbench_limit", 100)["state"]
    service.register_metric_stream(
        {
            "stream": {
                "stream_id": "stream_smoke",
                "tenant": "tenant_smoke",
                "name": "Smoke Stream",
                "event_type": "operational",
                "metric_field": "latency_ms",
                "aggregation": "avg",
                "region": "US",
                "status": "active",
            }
        }
    )
    service.define_window(
        {
            "window": {
                "window_id": "window_smoke",
                "tenant": "tenant_smoke",
                "stream_id": "stream_smoke",
                "window_minutes": 15,
                "status": "active",
            }
        }
    )
    service.ingest_metric_event(
        {
            "event": {
                "event_id": "metric_smoke",
                "tenant": "tenant_smoke",
                "event_type": "operational",
                "region": "US",
                "values": {"latency_ms": 250.0},
            }
        }
    )
    query = service.build_workbench_view({"tenant": "tenant_smoke"})
    return {
        "ok": service_operation_manifest()["ok"] and query["ok"] and query["result"]["stream_count"] == 1,
        "manifest": service_operation_manifest(),
        "result": query,
        "side_effects": (),
    }
