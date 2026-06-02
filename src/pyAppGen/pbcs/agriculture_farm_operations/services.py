"""Command and query service layer for agriculture_farm_operations."""

from __future__ import annotations

from .events import EVENT_CONTRACT
from .runtime import (
    PBC_KEY,
    agriculture_farm_operations_build_api_contract,
    agriculture_farm_operations_build_release_evidence,
    agriculture_farm_operations_build_schema_contract,
    agriculture_farm_operations_build_service_contract,
    agriculture_farm_operations_build_workbench_view,
    agriculture_farm_operations_command_field,
    agriculture_farm_operations_configure_runtime,
    agriculture_farm_operations_empty_state,
    agriculture_farm_operations_parse_document_instruction,
    agriculture_farm_operations_query_workbench,
    agriculture_farm_operations_receive_event,
    agriculture_farm_operations_record_crop_plan,
    agriculture_farm_operations_register_rule,
    agriculture_farm_operations_register_schema_extension,
    agriculture_farm_operations_run_advanced_assessment,
    agriculture_farm_operations_set_parameter,
)

COMMAND_SPECS = (
    {
        "operation": "configure_runtime",
        "method": "POST",
        "path": "/api/pbc/agriculture_farm_operations/runtime/configuration",
        "permission": "agriculture_farm_operations.admin",
        "owned_tables": ("agriculture_farm_operations_agriculture_farm_operations_runtime_parameter",),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "set_parameter",
        "method": "POST",
        "path": "/api/pbc/agriculture_farm_operations/runtime/parameters",
        "permission": "agriculture_farm_operations.admin",
        "owned_tables": ("agriculture_farm_operations_agriculture_farm_operations_runtime_parameter",),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "register_rule",
        "method": "POST",
        "path": "/api/pbc/agriculture_farm_operations/runtime/rules",
        "permission": "agriculture_farm_operations.admin",
        "owned_tables": ("agriculture_farm_operations_agriculture_farm_operations_policy_rule",),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "register_schema_extension",
        "method": "POST",
        "path": "/api/pbc/agriculture_farm_operations/runtime/schema-extensions",
        "permission": "agriculture_farm_operations.admin",
        "owned_tables": ("agriculture_farm_operations_agriculture_farm_operations_schema_extension",),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "receive_event",
        "method": "POST",
        "path": "/api/pbc/agriculture_farm_operations/events/inbox",
        "permission": "agriculture_farm_operations.admin",
        "owned_tables": (
            "agriculture_farm_operations_appgen_inbox_event",
            "agriculture_farm_operations_appgen_dead_letter_event",
        ),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "command_field",
        "method": "POST",
        "path": "/api/pbc/agriculture_farm_operations/fields",
        "permission": "agriculture_farm_operations.create",
        "owned_tables": ("agriculture_farm_operations_field", "agriculture_farm_operations_appgen_outbox_event"),
        "read_tables": (),
        "emitted_event": "AgricultureFarmOperationsCreated",
    },
    {
        "operation": "record_crop_plan",
        "method": "POST",
        "path": "/api/pbc/agriculture_farm_operations/crop-plans",
        "permission": "agriculture_farm_operations.create",
        "owned_tables": ("agriculture_farm_operations_crop_plan",),
        "read_tables": ("agriculture_farm_operations_field",),
        "emitted_event": "AgricultureFarmOperationsCreated",
    },
    {
        "operation": "parse_document_instruction",
        "method": "POST",
        "path": "/api/pbc/agriculture_farm_operations/assistant/document-plan",
        "permission": "agriculture_farm_operations.update",
        "owned_tables": (),
        "read_tables": ("agriculture_farm_operations_crop_plan", "agriculture_farm_operations_field"),
        "emitted_event": None,
    },
    {
        "operation": "run_advanced_assessment",
        "method": "POST",
        "path": "/api/pbc/agriculture_farm_operations/advanced-assessment",
        "permission": "agriculture_farm_operations.approve",
        "owned_tables": (),
        "read_tables": (
            "agriculture_farm_operations_field",
            "agriculture_farm_operations_crop_plan",
            "agriculture_farm_operations_appgen_outbox_event",
        ),
        "emitted_event": None,
    },
)
QUERY_SPECS = (
    {
        "operation": "query_workbench",
        "method": "GET",
        "path": "/api/pbc/agriculture_farm_operations/workbench",
        "permission": "agriculture_farm_operations.read",
        "owned_tables": (),
        "read_tables": (
            "agriculture_farm_operations_field",
            "agriculture_farm_operations_crop_plan",
            "agriculture_farm_operations_appgen_outbox_event",
        ),
        "emitted_event": None,
    },
    {
        "operation": "query_api_contract",
        "method": "GET",
        "path": "/api/pbc/agriculture_farm_operations/api-contract",
        "permission": "agriculture_farm_operations.read",
        "owned_tables": (),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "query_schema_contract",
        "method": "GET",
        "path": "/api/pbc/agriculture_farm_operations/schema-contract",
        "permission": "agriculture_farm_operations.read",
        "owned_tables": (),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "query_service_contract",
        "method": "GET",
        "path": "/api/pbc/agriculture_farm_operations/service-contract",
        "permission": "agriculture_farm_operations.read",
        "owned_tables": (),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "query_release_evidence",
        "method": "GET",
        "path": "/api/pbc/agriculture_farm_operations/release-evidence",
        "permission": "agriculture_farm_operations.read",
        "owned_tables": (),
        "read_tables": (),
        "emitted_event": None,
    },
    {
        "operation": "query_agent_surface",
        "method": "GET",
        "path": "/api/pbc/agriculture_farm_operations/assistant",
        "permission": "agriculture_farm_operations.read",
        "owned_tables": (),
        "read_tables": (
            "agriculture_farm_operations_field",
            "agriculture_farm_operations_crop_plan",
        ),
        "emitted_event": None,
    },
    {
        "operation": "build_workbench_view",
        "method": "GET",
        "path": "/api/pbc/agriculture_farm_operations/workbench-view",
        "permission": "agriculture_farm_operations.read",
        "owned_tables": (),
        "read_tables": (
            "agriculture_farm_operations_field",
            "agriculture_farm_operations_crop_plan",
        ),
        "emitted_event": None,
    },
)
COMMAND_OPERATIONS = tuple(item["operation"] for item in COMMAND_SPECS)
QUERY_OPERATIONS = tuple(item["operation"] for item in QUERY_SPECS)
ALL_SPECS = COMMAND_SPECS + QUERY_SPECS


def _spec(operation: str) -> dict:
    return next(item for item in ALL_SPECS if item["operation"] == operation)


def _operation_contract(spec: dict, operation_kind: str) -> dict:
    return {
        **spec,
        "operation_kind": operation_kind,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "idempotency_key": f"{PBC_KEY}:{spec['operation']}:idempotency_key" if operation_kind == "command" else None,
        "shared_table_access": False,
        "stream_engine_picker_visible": False,
    }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "AgricultureFarmOperationsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(spec, "command") for spec in COMMAND_SPECS) + tuple(
        _operation_contract(spec, "query") for spec in QUERY_SPECS
    )
    return {
        "ok": bool(contracts)
        and all(item["event_contract"] == "AppGen-X" for item in contracts)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in contracts),
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    if operation not in COMMAND_OPERATIONS + QUERY_OPERATIONS:
        return {"ok": False, "operation": operation, "reason": "unknown_operation", "side_effects": ()}
    spec = _spec(operation)
    kind = "query" if operation in QUERY_OPERATIONS else "command"
    return {**_operation_contract(spec, kind), "ok": True, "payload": dict(payload or {}), "side_effects": ()}


class AgricultureFarmOperationsService:
    def __init__(self, state: dict | None = None):
        self.state = state or agriculture_farm_operations_empty_state()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _apply_command(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "configure_runtime":
            return agriculture_farm_operations_configure_runtime(self.state, payload.get("configuration", payload))
        if operation_name == "set_parameter":
            return agriculture_farm_operations_set_parameter(self.state, payload["name"], payload["value"])
        if operation_name == "register_rule":
            return agriculture_farm_operations_register_rule(self.state, payload.get("rule", payload))
        if operation_name == "register_schema_extension":
            return agriculture_farm_operations_register_schema_extension(self.state, payload["table"], payload["fields"])
        if operation_name == "receive_event":
            return agriculture_farm_operations_receive_event(self.state, payload.get("envelope", payload))
        if operation_name == "command_field":
            return agriculture_farm_operations_command_field(self.state, payload.get("field", payload))
        if operation_name == "record_crop_plan":
            return agriculture_farm_operations_record_crop_plan(self.state, payload.get("crop_plan", payload))
        if operation_name == "parse_document_instruction":
            return agriculture_farm_operations_parse_document_instruction(
                payload["document"], payload["instruction"], payload.get("context")
            )
        if operation_name == "run_advanced_assessment":
            return agriculture_farm_operations_run_advanced_assessment(self.state, payload)
        raise ValueError(f"Unsupported agriculture_farm_operations command: {operation_name}")

    def _apply_query(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "query_workbench":
            return agriculture_farm_operations_query_workbench(self.state, payload)
        if operation_name == "query_api_contract":
            return agriculture_farm_operations_build_api_contract()
        if operation_name == "query_schema_contract":
            return agriculture_farm_operations_build_schema_contract()
        if operation_name == "query_service_contract":
            return agriculture_farm_operations_build_service_contract()
        if operation_name == "query_release_evidence":
            from . import release_evidence

            return release_evidence.build_release_evidence()
        if operation_name == "query_agent_surface":
            from . import agent

            return {
                "ok": True,
                "agent_manifest": agent.agent_skill_manifest(),
                "chatbot": agent.chatbot_interface_contract(),
                "workspace": agent.standalone_agent_workspace_contract(),
                "side_effects": (),
            }
        if operation_name == "build_workbench_view":
            return agriculture_farm_operations_build_workbench_view(self.state, tenant=payload.get("tenant", "default"))
        raise ValueError(f"Unsupported agriculture_farm_operations query: {operation_name}")

    def _command(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        result = self._apply_command(operation_name, payload)
        if "state" in result:
            self.state = result["state"]
        response = {
            "ok": result.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": "command",
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": tuple(filter(None, (plan["emitted_event"], result.get("emitted_event")))),
            "result": result,
            "state": self.state,
            "side_effects": (),
        }
        if operation_name == "record_crop_plan":
            response.update(
                {
                    "read_only": False,
                    "domain_depth": result,
                    "planning_preview": result,
                }
            )
        return response

    def _query(self, operation_name: str, payload: dict) -> dict:
        plan = operation_plan(operation_name, payload)
        if not plan["ok"]:
            return plan
        result = self._apply_query(operation_name, payload)
        response = {
            "ok": result.get("ok") is True,
            "pbc": PBC_KEY,
            "operation": operation_name,
            "operation_kind": "query",
            "payload": dict(payload),
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "emits": (),
            "result": result,
            "state": self.state,
            "side_effects": (),
        }
        if operation_name == "query_workbench":
            response["workbench_projection"] = result["crop_plan_summary"]
        return response


def smoke_test() -> dict:
    service = AgricultureFarmOperationsService()
    configure = service.configure_runtime(
        {
            "configuration": {
                "database_backend": "postgresql",
                "event_topic": "pbc.agriculture_farm_operations.events",
                "retry_limit": 5,
                "default_region": "east-africa",
                "calendar_profile": "seasonal",
                "workbench_limit": 100,
            }
        }
    )
    field = service.command_field(
        {
            "field": {
                "tenant": "tenant-smoke",
                "field_id": "field-service-smoke",
                "code": "FIELD-SVC",
                "name": "Service Smoke Field",
                "acreage": 90,
                "management_zones": ("north",),
            }
        }
    )
    crop_plan = service.record_crop_plan(
        {
            "tenant": "tenant-smoke",
            "field_id": "field-service-smoke",
            "management_zone": "north",
            "crop": "maize",
            "season": "long_rains",
            "market_year": 2026,
            "planting_date": "2026-04-24",
            "planned_start": "2026-04-24",
            "planned_end": "2026-09-15",
            "planting_window": {
                "start": "2026-04-10",
                "optimal_start": "2026-04-20",
                "optimal_end": "2026-05-05",
                "latest": "2026-05-15",
            },
            "readiness": {
                "soil_fit": True,
                "fertility_ready": True,
                "equipment_ready": True,
                "crew_assigned": True,
            },
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": configure["ok"] and field["ok"] and crop_plan["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "result": crop_plan,
        "query": query,
        "side_effects": (),
    }
