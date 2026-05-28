"""Executable service layer for the cdp_segmentation PBC."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from .runtime import CDP_SEGMENTATION_RUNTIME_TABLES
from .runtime import cdp_segmentation_activate_segment
from .runtime import cdp_segmentation_allocate_activation
from .runtime import cdp_segmentation_build_api_contract
from .runtime import cdp_segmentation_build_release_evidence
from .runtime import cdp_segmentation_build_schema_contract
from .runtime import cdp_segmentation_build_service_contract
from .runtime import cdp_segmentation_build_workbench_view
from .runtime import cdp_segmentation_configure_runtime
from .runtime import cdp_segmentation_define_segment
from .runtime import cdp_segmentation_detect_profile_anomaly
from .runtime import cdp_segmentation_evaluate_segments
from .runtime import cdp_segmentation_federate_customer_view
from .runtime import cdp_segmentation_forecast_audience
from .runtime import cdp_segmentation_generate_profile_proof
from .runtime import cdp_segmentation_heal_profile_merge
from .runtime import cdp_segmentation_ingest_customer_event
from .runtime import cdp_segmentation_parse_segment_rule
from .runtime import cdp_segmentation_permissions_contract
from .runtime import cdp_segmentation_receive_event
from .runtime import cdp_segmentation_register_governed_model
from .runtime import cdp_segmentation_register_rule
from .runtime import cdp_segmentation_register_schema_extension
from .runtime import cdp_segmentation_resolve_audience_exception
from .runtime import cdp_segmentation_run_data_quality_controls
from .runtime import cdp_segmentation_score_lifecycle_risk
from .runtime import cdp_segmentation_screen_consent_policy
from .runtime import cdp_segmentation_set_parameter
from .runtime import cdp_segmentation_simulate_segment_membership
from .runtime import cdp_segmentation_upsert_profile_property
from .runtime import cdp_segmentation_verify_owned_table_boundary


def _method_path(route: str) -> tuple[str, str]:
    method, path = route.split(" ", 1)
    return method, path


def _operation_name(route: dict) -> str | None:
    return route.get("command") or route.get("query")


def _owned_tables(route: dict) -> tuple[str, ...]:
    return tuple(
        table if table.startswith("cdp_segmentation_") else f"cdp_segmentation_{table}"
        for table in route.get("owned_tables", ())
    )


def _build_operation_contracts() -> tuple[dict, ...]:
    api = cdp_segmentation_build_api_contract()
    fallback_emitted = api["emits"][0]
    contracts = []
    for route in api["routes"]:
        operation = _operation_name(route)
        if not operation:
            continue
        method, path = _method_path(route["route"])
        is_command = "command" in route
        table_scope = _owned_tables(route)
        if is_command and not table_scope and operation == "receive_event":
            table_scope = (CDP_SEGMENTATION_RUNTIME_TABLES[1], CDP_SEGMENTATION_RUNTIME_TABLES[2])
        contracts.append(
            {
                "operation": operation,
                "operation_kind": "command" if is_command else "query",
                "method": method,
                "path": path,
                "permission": route["requires_permission"],
                "owned_tables": table_scope if is_command else (),
                "read_tables": () if is_command else table_scope,
                "emitted_event": (tuple(route.get("emits", ())) or (fallback_emitted,))[0] if is_command else None,
                "consumed_event": tuple(route.get("consumes", ())),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "event_contract": "AppGen-X",
                "stream_engine_picker_visible": False,
                "shared_table_access": False,
            }
        )
    return tuple(contracts)


OPERATION_CONTRACTS = _build_operation_contracts()


def service_operation_contracts() -> dict:
    """Return route-bound service contracts."""
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    runtime_service = cdp_segmentation_build_service_contract()
    return {
        "ok": runtime_service["ok"]
        and bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(item["owned_tables"] or item["consumed_event"] for item in command_contracts)
        and all(item["read_tables"] for item in query_contracts),
        "pbc": "cdp_segmentation",
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
    table_scope = contract["owned_tables"] or contract["read_tables"] or tuple(
        table if table.startswith("cdp_segmentation_") else f"cdp_segmentation_{table}"
        for table in CDP_SEGMENTATION_RUNTIME_TABLES
    )
    return {
        "ok": bool(table_scope) and contract["event_contract"] == "AppGen-X",
        "pbc": "cdp_segmentation",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "route": {"method": contract["method"], "path": contract["path"]},
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "consumed_event": contract["consumed_event"],
        "payload_keys": tuple(sorted(key for key in supplied if key != "state")),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "stream_engine_picker_visible": False,
        "shared_table_access": False,
        "side_effects": (),
    }


def _runtime_execute(operation_name: str, state: dict, payload: dict) -> dict:
    if operation_name == "configure_runtime":
        return cdp_segmentation_configure_runtime(state, payload)
    if operation_name == "set_parameter":
        return cdp_segmentation_set_parameter(state, payload["name"], payload["value"])
    if operation_name == "register_rule":
        return cdp_segmentation_register_rule(state, payload)
    if operation_name == "register_schema_extension":
        return cdp_segmentation_register_schema_extension(state, payload["table"], payload["fields"])
    if operation_name == "receive_event":
        return cdp_segmentation_receive_event(state, payload, simulate_failure=bool(payload.get("simulate_failure", False)))
    if operation_name == "ingest_customer_event":
        return cdp_segmentation_ingest_customer_event(state, payload)
    if operation_name == "upsert_profile_property":
        return cdp_segmentation_upsert_profile_property(state, payload)
    if operation_name == "define_segment":
        return cdp_segmentation_define_segment(state, payload)
    if operation_name == "evaluate_segments":
        return cdp_segmentation_evaluate_segments(state, payload["customer_id"])
    if operation_name == "activate_segment":
        return cdp_segmentation_activate_segment(state, payload["segment_id"])
    if operation_name == "simulate_segment_membership":
        return cdp_segmentation_simulate_segment_membership(state, payload)
    if operation_name == "forecast_audience":
        return cdp_segmentation_forecast_audience(state, payload)
    if operation_name == "resolve_audience_exception":
        return cdp_segmentation_resolve_audience_exception(state, payload)
    if operation_name == "parse_segment_rule":
        return cdp_segmentation_parse_segment_rule(state, payload)
    if operation_name == "score_lifecycle_risk":
        return cdp_segmentation_score_lifecycle_risk(state, payload)
    if operation_name == "heal_profile_merge":
        return cdp_segmentation_heal_profile_merge(state, payload)
    if operation_name == "generate_profile_proof":
        return cdp_segmentation_generate_profile_proof(state, payload)
    if operation_name == "screen_consent_policy":
        return cdp_segmentation_screen_consent_policy(state, payload)
    if operation_name == "run_data_quality_controls":
        return cdp_segmentation_run_data_quality_controls(state, payload["tenant"])
    if operation_name == "federate_customer_view":
        return cdp_segmentation_federate_customer_view(state, payload)
    if operation_name == "allocate_activation":
        return cdp_segmentation_allocate_activation(state, payload)
    if operation_name == "detect_profile_anomaly":
        return cdp_segmentation_detect_profile_anomaly(state, payload)
    if operation_name == "register_governed_model":
        return cdp_segmentation_register_governed_model(state, payload)
    if operation_name == "build_workbench_view":
        return cdp_segmentation_build_workbench_view(state, tenant=payload["tenant"])
    if operation_name == "verify_owned_table_boundary":
        return cdp_segmentation_verify_owned_table_boundary(tuple(payload.get("references", ())))
    if operation_name == "build_api_contract":
        return cdp_segmentation_build_api_contract()
    if operation_name == "build_schema_contract":
        return cdp_segmentation_build_schema_contract()
    if operation_name == "build_service_contract":
        return cdp_segmentation_build_service_contract()
    if operation_name == "build_release_evidence":
        return cdp_segmentation_build_release_evidence()
    if operation_name == "permissions_contract":
        return cdp_segmentation_permissions_contract()
    raise AttributeError(operation_name)


class CdpSegmentationService:
    """Service facade with plan mode and explicit-state execution mode."""

    def execute_operation(self, operation_name: str, payload: dict | None = None) -> dict:
        supplied = dict(payload or {})
        state = supplied.pop("state", None)
        plan = operation_plan(operation_name, supplied)
        result = {
            "ok": plan["ok"],
            "pbc": "cdp_segmentation",
            "operation": operation_name,
            "operation_kind": plan.get("operation_kind"),
            "payload": supplied,
            "operation_contract": plan,
            "transaction_boundary": plan.get("transaction_boundary"),
            "mode": "execute" if state is not None else "plan",
            "side_effects": (),
        }
        if state is None:
            if plan.get("operation_kind") == "command":
                result.update(
                    {
                        "command": operation_name,
                        "read_only": False,
                        "outbox_table": EVENT_CONTRACT["outbox_table"],
                        "emits": (plan.get("emitted_event"),),
                        "consumes": plan.get("consumed_event", ()),
                    }
                )
            else:
                result.update({"query": operation_name, "read_only": True, "outbox_table": None, "emits": ()})
            return result

        execution = _runtime_execute(operation_name, state, supplied)
        result.update(
            {
                "ok": execution.get("ok", result["ok"]),
                "execution": execution,
                "state": execution.get("state"),
                "read_only": plan.get("operation_kind") == "query",
                "outbox_table": EVENT_CONTRACT["outbox_table"] if plan.get("operation_kind") == "command" else None,
                "emits": (plan.get("emitted_event"),) if plan.get("operation_kind") == "command" else (),
                "consumes": plan.get("consumed_event", ()),
            }
        )
        if plan.get("operation_kind") == "command":
            result["command"] = operation_name
        else:
            result["query"] = operation_name
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
        "pbc": "cdp_segmentation",
        "service_class": CdpSegmentationService.__name__,
        "operations": contracts["operations"],
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "operation_contracts": contracts["contracts"],
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise planning and explicit-state execution paths."""
    from .runtime import CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC
    from .runtime import cdp_segmentation_empty_state

    manifest = service_operation_manifest()
    service = CdpSegmentationService()
    first_operation = manifest["operations"][0] if manifest["operations"] else None
    plan_result = service.execute_operation(first_operation, {}) if first_operation else {"ok": False}
    state = cdp_segmentation_empty_state()
    configured = service.execute_operation(
        "configure_runtime",
        {
            "state": state,
            "database_backend": "postgresql",
            "event_topic": CDP_SEGMENTATION_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_region": "US",
            "supported_regions": ("US",),
            "supported_event_types": ("profile", "payment", "shipment", "engagement"),
            "identity_keys": ("customer_id", "email"),
            "default_timezone": "UTC",
            "activation_mode": "policy",
            "workbench_limit": 50,
        },
    )
    return {
        "ok": manifest["ok"]
        and plan_result["ok"]
        and configured["ok"]
        and configured["mode"] == "execute"
        and configured["state"]["configuration"]["ok"] is True,
        "manifest": manifest,
        "plan_result": plan_result,
        "result": configured,
        "side_effects": (),
    }
