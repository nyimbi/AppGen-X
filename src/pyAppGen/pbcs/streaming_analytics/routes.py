"""API route contracts for the streaming_analytics PBC."""

from __future__ import annotations

from .services import StreamingAnalyticsService
from .services import service_operation_contracts


def _route_contracts() -> tuple[dict, ...]:
    return tuple(
        {
            "method": contract["method"],
            "path": contract["path"],
            "handler": contract["operation"],
            "permission": contract["permission"],
            "operation": contract["operation"],
            "operation_kind": contract["operation_kind"],
            "owned_tables": contract["owned_tables"],
            "read_tables": contract["read_tables"],
            "emitted_event": contract["emitted_event"],
            "consumed_event": contract["consumed_event"],
            "event_contract": contract["event_contract"],
            "transaction_boundary": contract["transaction_boundary"],
            "idempotency_required": contract["operation_kind"] == "command",
            "idempotency_key": contract["idempotency_key"],
            "shared_table_access": False,
            "stream_engine_picker_visible": False,
        }
        for contract in service_operation_contracts()["contracts"]
    )


API_ROUTE_CONTRACTS = _route_contracts()
ROUTES = tuple(
    {
        "method": contract["method"],
        "path": contract["path"],
        "handler": contract["handler"],
        "permission": contract["permission"],
    }
    for contract in API_ROUTE_CONTRACTS
)


def register_routes(app=None):
    """Return route metadata without mutating an application object."""
    return ROUTES


def api_route_contracts() -> dict:
    """Return executable API route contracts with policy and boundary evidence."""
    contracts = tuple(
        {
            **contract,
            "route_id": f"{contract['method']} {contract['path']}",
        }
        for contract in API_ROUTE_CONTRACTS
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts)
        and all(item["stream_engine_picker_visible"] is False for item in contracts)
        and all(item["shared_table_access"] is False for item in contracts),
        "pbc": "streaming_analytics",
        "contracts": contracts,
        "routes": tuple(item["route_id"] for item in contracts),
        "side_effects": (),
    }


def validate_api_route_contracts() -> dict:
    """Validate routes against service operations, permissions, idempotency, and table boundaries."""
    manifest = api_route_contracts()
    contracts = manifest["contracts"]
    operation_index = {item["operation"]: item for item in service_operation_contracts()["contracts"]}
    service_mismatches = tuple(
        item["route_id"]
        for item in contracts
        if item["operation"] not in operation_index
        or operation_index[item["operation"]]["method"] != item["method"]
        or operation_index[item["operation"]]["path"] != item["path"]
        or operation_index[item["operation"]]["permission"] != item["permission"]
    )
    missing_idempotency = tuple(
        item["route_id"]
        for item in contracts
        if item["idempotency_required"] and not item["idempotency_key"]
    )
    invalid_table_scope = tuple(
        item["route_id"]
        for item in contracts
        for table in item["owned_tables"] + item["read_tables"]
        if not table.startswith("streaming_analytics_")
    )
    return {
        "ok": manifest["ok"] and not service_mismatches and not missing_idempotency and not invalid_table_scope,
        "pbc": "streaming_analytics",
        "contracts": contracts,
        "service_mismatches": service_mismatches,
        "missing_idempotency": missing_idempotency,
        "invalid_table_scope": invalid_table_scope,
        "side_effects": (),
    }


def dispatch_route(method: str, path: str, payload: dict | None = None, *, service: StreamingAnalyticsService | None = None) -> dict:
    """Dispatch a route contract to its service command without external side effects."""
    route = next((item for item in ROUTES if item["method"] == method and item["path"] == path), None)
    if route is None:
        return {"ok": False, "handled": False, "reason": "route_not_found", "side_effects": ()}
    service = service or StreamingAnalyticsService()
    handler = getattr(service, route["handler"])
    result = handler(payload or {})
    return {
        "ok": result.get("ok") is True,
        "handled": True,
        "route": route,
        "result": result,
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Execute configuration, one route, and validate the API contract surface."""
    service = StreamingAnalyticsService()
    from . import runtime

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
    dispatched = dispatch_route(
        "POST",
        "/api/pbc/streaming_analytics/metric-streams",
        {
            "stream": {
                "stream_id": "stream_route_smoke",
                "tenant": "tenant_route_smoke",
                "name": "Route Smoke Stream",
                "event_type": "operational",
                "metric_field": "latency_ms",
                "aggregation": "avg",
                "region": "US",
                "status": "active",
            }
        },
        service=service,
    )
    validation = validate_api_route_contracts()
    return {
        "ok": validation["ok"] and dispatched["ok"],
        "validation": validation,
        "dispatch": dispatched,
        "side_effects": (),
    }
