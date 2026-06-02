"""Command and query service layer for the airline_operations_control PBC."""

from __future__ import annotations

from . import runtime
from .events import event_contract_manifest


EVENT_CONTRACT = event_contract_manifest()

_COMMAND_OPERATION_SPECS = (
    {
        "operation": "command_configure_runtime",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/runtime/configuration",
        "permission": "airline_operations_control.admin",
        "owned_tables": ("airline_operations_control_airline_operations_control_runtime_parameter",),
        "emitted_event": None,
    },
    {
        "operation": "command_set_parameter",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/runtime/parameters",
        "permission": "airline_operations_control.admin",
        "owned_tables": ("airline_operations_control_airline_operations_control_runtime_parameter",),
        "emitted_event": None,
    },
    {
        "operation": "command_register_rule",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/runtime/rules",
        "permission": "airline_operations_control.admin",
        "owned_tables": ("airline_operations_control_airline_operations_control_policy_rule",),
        "emitted_event": None,
    },
    {
        "operation": "command_receive_event",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/events/inbox",
        "permission": "airline_operations_control.admin",
        "owned_tables": (
            "airline_operations_control_appgen_inbox_event",
            "airline_operations_control_appgen_dead_letter_event",
        ),
        "emitted_event": None,
    },
    {
        "operation": "command_flight_leg",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/flight-legs",
        "permission": "airline_operations_control.create",
        "owned_tables": (
            "airline_operations_control_flight_leg",
            "airline_operations_control_appgen_outbox_event",
        ),
        "emitted_event": "AirlineOperationsControlCreated",
    },
    {
        "operation": "record_aircraft_rotation",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/aircraft-rotations",
        "permission": "airline_operations_control.update",
        "owned_tables": (
            "airline_operations_control_aircraft_rotation",
            "airline_operations_control_flight_leg",
            "airline_operations_control_appgen_outbox_event",
        ),
        "emitted_event": "AirlineOperationsControlUpdated",
    },
    {
        "operation": "command_crew_pairing",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/crew-pairings",
        "permission": "airline_operations_control.update",
        "owned_tables": (
            "airline_operations_control_crew_pairing",
            "airline_operations_control_appgen_outbox_event",
        ),
        "emitted_event": "AirlineOperationsControlUpdated",
    },
    {
        "operation": "command_disruption_event",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/disruption-events",
        "permission": "airline_operations_control.update",
        "owned_tables": (
            "airline_operations_control_disruption_event",
            "airline_operations_control_appgen_outbox_event",
        ),
        "emitted_event": "AirlineOperationsControlExceptionOpened",
    },
    {
        "operation": "command_reaccommodation_plan",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/reaccommodation-plans",
        "permission": "airline_operations_control.update",
        "owned_tables": (
            "airline_operations_control_reaccommodation_plan",
            "airline_operations_control_appgen_outbox_event",
        ),
        "emitted_event": "AirlineOperationsControlUpdated",
    },
    {
        "operation": "command_operations_decision",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/operations-decisions",
        "permission": "airline_operations_control.approve",
        "owned_tables": (
            "airline_operations_control_operations_decision",
            "airline_operations_control_appgen_outbox_event",
        ),
        "emitted_event": "AirlineOperationsControlApproved",
    },
    {
        "operation": "record_delay_code",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/delay-codes",
        "permission": "airline_operations_control.update",
        "owned_tables": (
            "airline_operations_control_delay_code",
            "airline_operations_control_appgen_outbox_event",
        ),
        "emitted_event": "AirlineOperationsControlUpdated",
    },
    {
        "operation": "plan_recovery_workflow",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/workflows/recovery",
        "permission": "airline_operations_control.update",
        "owned_tables": (
            "airline_operations_control_operations_decision",
            "airline_operations_control_disruption_event",
            "airline_operations_control_reaccommodation_plan",
            "airline_operations_control_appgen_outbox_event",
        ),
        "emitted_event": "AirlineOperationsControlUpdated",
    },
    {
        "operation": "document_instruction_plan",
        "method": "POST",
        "path": "/api/pbc/airline_operations_control/assistant/document-plan",
        "permission": "airline_operations_control.read",
        "owned_tables": (),
        "emitted_event": None,
    },
)

_QUERY_OPERATION_SPECS = (
    {
        "operation": "query_workbench",
        "method": "GET",
        "path": "/api/pbc/airline_operations_control/workbench",
        "permission": "airline_operations_control.read",
        "read_tables": tuple(runtime.AIRLINE_OPERATIONS_CONTROL_RUNTIME_TABLES),
    },
    {
        "operation": "query_schema_contract",
        "method": "GET",
        "path": "/api/pbc/airline_operations_control/schema-contract",
        "permission": "airline_operations_control.read",
        "read_tables": tuple(runtime.AIRLINE_OPERATIONS_CONTROL_RUNTIME_TABLES),
    },
    {
        "operation": "query_service_contract",
        "method": "GET",
        "path": "/api/pbc/airline_operations_control/service-contract",
        "permission": "airline_operations_control.read",
        "read_tables": tuple(runtime.AIRLINE_OPERATIONS_CONTROL_RUNTIME_TABLES),
    },
    {
        "operation": "query_release_evidence",
        "method": "GET",
        "path": "/api/pbc/airline_operations_control/release-evidence",
        "permission": "airline_operations_control.read",
        "read_tables": tuple(runtime.AIRLINE_OPERATIONS_CONTROL_RUNTIME_TABLES),
    },
    {
        "operation": "query_permissions_contract",
        "method": "GET",
        "path": "/api/pbc/airline_operations_control/permissions",
        "permission": "airline_operations_control.read",
        "read_tables": (
            "airline_operations_control_airline_operations_control_policy_rule",
            "airline_operations_control_airline_operations_control_runtime_parameter",
        ),
    },
    {
        "operation": "query_agent_surface",
        "method": "GET",
        "path": "/api/pbc/airline_operations_control/agent",
        "permission": "airline_operations_control.read",
        "read_tables": (
            "airline_operations_control_flight_leg",
            "airline_operations_control_operations_decision",
            "airline_operations_control_appgen_outbox_event",
        ),
    },
)

OPERATION_CONTRACTS = tuple(
    {
        **spec,
        "operation_kind": "command",
        "read_tables": (),
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "idempotency_key": f"airline_operations_control:{spec['operation']}:idempotency_key",
    }
    for spec in _COMMAND_OPERATION_SPECS
) + tuple(
    {
        **spec,
        "operation_kind": "query",
        "owned_tables": (),
        "emitted_event": None,
        "transaction_boundary": "owned_datastore_plus_outbox",
        "event_contract": "AppGen-X",
        "idempotency_key": None,
    }
    for spec in _QUERY_OPERATION_SPECS
)


def service_operation_contracts() -> dict:
    command_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "command")
    query_contracts = tuple(item for item in OPERATION_CONTRACTS if item["operation_kind"] == "query")
    return {
        "ok": bool(OPERATION_CONTRACTS)
        and all(item["event_contract"] == "AppGen-X" for item in OPERATION_CONTRACTS)
        and all(item["transaction_boundary"] == "owned_datastore_plus_outbox" for item in OPERATION_CONTRACTS)
        and all(not item["read_tables"] for item in command_contracts)
        and all(not item["owned_tables"] for item in query_contracts),
        "pbc": "airline_operations_control",
        "operations": tuple(item["operation"] for item in OPERATION_CONTRACTS),
        "command_operations": tuple(item["operation"] for item in command_contracts),
        "query_operations": tuple(item["operation"] for item in query_contracts),
        "contracts": OPERATION_CONTRACTS,
        "side_effects": (),
    }


def service_operation_manifest() -> dict:
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": "airline_operations_control",
        "service_class": "AirlineOperationsControlService",
        "command_operations": contracts["command_operations"],
        "query_operations": contracts["query_operations"],
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def operation_plan(operation_name: str, payload: dict | None = None) -> dict:
    contract = next((item for item in OPERATION_CONTRACTS if item["operation"] == operation_name), None)
    if contract is None:
        return {"ok": False, "reason": "unknown_operation", "operation": operation_name, "side_effects": ()}
    supplied = dict(payload or {})
    return {
        "ok": True,
        "pbc": "airline_operations_control",
        "operation": operation_name,
        "operation_kind": contract["operation_kind"],
        "method": contract["method"],
        "path": contract["path"],
        "permission": contract["permission"],
        "owned_tables": contract["owned_tables"],
        "read_tables": contract["read_tables"],
        "emitted_event": contract["emitted_event"],
        "payload_keys": tuple(sorted(supplied)),
        "transaction_boundary": contract["transaction_boundary"],
        "event_contract": contract["event_contract"],
        "idempotency_key": contract["idempotency_key"],
        "side_effects": (),
    }


class AirlineOperationsControlService:
    """Executable package-local service facade over the airline OCC runtime."""

    def __init__(self, state: dict | None = None):
        self.state = state or runtime.airline_operations_control_empty_state()

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
            "pbc": "airline_operations_control",
            "operation": operation_name,
            "operation_kind": "command",
            "payload": payload,
            "operation_contract": plan,
            "transaction_boundary": plan["transaction_boundary"],
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (plan["emitted_event"],) if plan["emitted_event"] else (),
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
            "pbc": "airline_operations_control",
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
        if operation_name == "command_configure_runtime":
            return runtime.airline_operations_control_configure_runtime(self.state, payload["configuration"])
        if operation_name == "command_set_parameter":
            return runtime.airline_operations_control_set_parameter(self.state, payload["name"], payload["value"])
        if operation_name == "command_register_rule":
            return runtime.airline_operations_control_register_rule(self.state, payload["rule"])
        if operation_name == "command_receive_event":
            return runtime.airline_operations_control_receive_event(self.state, payload["envelope"])
        if operation_name == "command_flight_leg":
            return runtime.airline_operations_control_command_flight_leg(self.state, payload["flight_leg"])
        if operation_name == "record_aircraft_rotation":
            return runtime.airline_operations_control_record_aircraft_rotation(self.state, payload["rotation"])
        if operation_name == "command_crew_pairing":
            return runtime.airline_operations_control_command_crew_pairing(self.state, payload["crew_pairing"])
        if operation_name == "command_disruption_event":
            return runtime.airline_operations_control_command_disruption_event(self.state, payload["disruption_event"])
        if operation_name == "command_reaccommodation_plan":
            return runtime.airline_operations_control_command_reaccommodation_plan(self.state, payload["reaccommodation_plan"])
        if operation_name == "command_operations_decision":
            return runtime.airline_operations_control_command_operations_decision(self.state, payload["operations_decision"])
        if operation_name == "record_delay_code":
            return runtime.airline_operations_control_record_delay_code(self.state, payload["delay_code"])
        if operation_name == "plan_recovery_workflow":
            return runtime.airline_operations_control_plan_recovery_workflow(self.state, payload["workflow"])
        if operation_name == "document_instruction_plan":
            return runtime.airline_operations_control_parse_document_instruction(payload["document"], payload["instruction"])
        if operation_name in runtime.DOMAIN_OPERATIONS:
            return runtime.airline_operations_control_execute_domain_operation(operation_name, payload)
        raise ValueError(f"Unsupported Airline Operations Control command: {operation_name}")

    def _apply_query(self, operation_name: str, payload: dict) -> dict:
        if operation_name == "query_workbench":
            if payload.get("state"):
                return runtime.airline_operations_control_build_workbench_view(payload["state"], tenant=payload.get("tenant", "default"))
            if payload.get("flight_legs") or payload.get("aircraft_rotations"):
                return runtime.airline_operations_control_build_workbench_view(
                    tenant=payload.get("tenant", "default"),
                    flight_legs=tuple(payload.get("flight_legs", ())),
                    aircraft_rotations=tuple(payload.get("aircraft_rotations", ())),
                )
            return runtime.airline_operations_control_build_workbench_view(self.state, tenant=payload.get("tenant", "default"))
        if operation_name == "query_schema_contract":
            return runtime.airline_operations_control_build_schema_contract()
        if operation_name == "query_service_contract":
            return runtime.airline_operations_control_build_service_contract()
        if operation_name == "query_release_evidence":
            from . import release_evidence

            return release_evidence.build_release_evidence()
        if operation_name == "query_permissions_contract":
            return runtime.airline_operations_control_permissions_contract()
        if operation_name == "query_agent_surface":
            from . import agent

            return agent.composed_agent_contribution()
        raise ValueError(f"Unsupported Airline Operations Control query: {operation_name}")

    def command_configure_runtime(self, payload: dict | None = None) -> dict:
        return self._command("command_configure_runtime", payload)

    def command_set_parameter(self, payload: dict | None = None) -> dict:
        return self._command("command_set_parameter", payload)

    def command_register_rule(self, payload: dict | None = None) -> dict:
        return self._command("command_register_rule", payload)

    def command_receive_event(self, payload: dict | None = None) -> dict:
        return self._command("command_receive_event", payload)

    def command_flight_leg(self, payload: dict | None = None) -> dict:
        return self._command("command_flight_leg", payload)

    def record_aircraft_rotation(self, payload: dict | None = None) -> dict:
        return self._command("record_aircraft_rotation", payload)

    def command_crew_pairing(self, payload: dict | None = None) -> dict:
        return self._command("command_crew_pairing", payload)

    def command_disruption_event(self, payload: dict | None = None) -> dict:
        return self._command("command_disruption_event", payload)

    def command_reaccommodation_plan(self, payload: dict | None = None) -> dict:
        return self._command("command_reaccommodation_plan", payload)

    def command_operations_decision(self, payload: dict | None = None) -> dict:
        return self._command("command_operations_decision", payload)

    def record_delay_code(self, payload: dict | None = None) -> dict:
        return self._command("record_delay_code", payload)

    def plan_recovery_workflow(self, payload: dict | None = None) -> dict:
        return self._command("plan_recovery_workflow", payload)

    def document_instruction_plan(self, payload: dict | None = None) -> dict:
        return self._command("document_instruction_plan", payload)

    def query_workbench(self, payload: dict | None = None) -> dict:
        return self._query("query_workbench", payload)

    def query_schema_contract(self, payload: dict | None = None) -> dict:
        return self._query("query_schema_contract", payload)

    def query_service_contract(self, payload: dict | None = None) -> dict:
        return self._query("query_service_contract", payload)

    def query_release_evidence(self, payload: dict | None = None) -> dict:
        return self._query("query_release_evidence", payload)

    def query_permissions_contract(self, payload: dict | None = None) -> dict:
        return self._query("query_permissions_contract", payload)

    def query_agent_surface(self, payload: dict | None = None) -> dict:
        return self._query("query_agent_surface", payload)


def smoke_test() -> dict:
    service = AirlineOperationsControlService()
    service.command_configure_runtime({"configuration": runtime.AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION})
    service.command_set_parameter({"name": "workbench_limit", "value": 20})
    service.command_register_rule({"rule": runtime.AIRLINE_OPERATIONS_CONTROL_DEFAULT_RULE})
    service.command_flight_leg(
        {
            "flight_leg": {
                "tenant": "tenant-smoke",
                "id": "KQ-SVC-1",
                "flight_number": "KQ901",
                "tail_number": "5Y-SVC",
                "origin": "NBO",
                "destination": "MBA",
                "scheduled_departure_at": "2026-05-29T06:00:00+00:00",
                "scheduled_arrival_at": "2026-05-29T07:00:00+00:00",
                "actual_on_block_at": "2026-05-29T07:12:00+00:00",
            }
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"] and query["ok"] and query["result"]["summary_cards"][0]["value"] >= 1,
        "contracts": contracts,
        "query": query,
        "side_effects": (),
    }
