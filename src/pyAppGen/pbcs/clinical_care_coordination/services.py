"""Service layer for the clinical_care_coordination PBC."""

from __future__ import annotations

from .care_coordination_app import (
    OWNED_TABLES as CARE_COORDINATION_OWNED_TABLES,
    add_care_team_member,
    care_coordination_workbench,
    close_care_gap,
    complete_transition_plan,
    create_care_plan,
    create_referral,
    create_transition_plan,
    empty_care_coordination_state,
    open_care_gap,
    receive_referral_result,
    record_encounter_and_tasks,
    record_outcome_measure,
    transition_care_plan,
)
from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES
from .domain_depth import execute_domain_operation as execute_domain_depth_operation


PBC_KEY = "clinical_care_coordination"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
CARE_COORDINATION_COMMANDS = (
    "create_care_plan",
    "transition_care_plan",
    "add_care_team_member",
    "create_referral",
    "receive_referral_result",
    "record_encounter_and_tasks",
    "open_care_gap",
    "close_care_gap",
    "create_transition_plan",
    "complete_transition_plan",
    "record_outcome_measure",
)
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        ("command_patient_care_plan", "configure_runtime", "set_parameter", "register_rule")
        + CARE_COORDINATION_COMMANDS
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = ("query_workbench", "query_service_contract")
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    emitted_event = None
    if kind == "command":
        if name == "create_care_plan":
            emitted_event = "ClinicalCareCoordinationCreated"
        elif name == "complete_transition_plan":
            emitted_event = "ClinicalCareCoordinationApproved"
        elif name == "open_care_gap":
            emitted_event = "ClinicalCareCoordinationExceptionOpened"
        else:
            emitted_event = "ClinicalCareCoordinationUpdated"
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": CARE_COORDINATION_OWNED_TABLES if kind == "command" else (),
        "read_tables": CARE_COORDINATION_OWNED_TABLES if kind == "query" else CARE_COORDINATION_OWNED_TABLES,
        "emitted_event": emitted_event,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


def _wrap_result(name: str, result: dict) -> dict:
    return {
        **result,
        "operation": name,
        "operation_kind": "command",
        "transaction_boundary": "owned_datastore_plus_outbox",
        "outbox_table": EVENT_CONTRACT["outbox_table"],
        "operation_contract": _operation_contract(name, "command"),
    }


class ClinicalCareCoordinationService:
    def __init__(self, state: dict | None = None):
        self.state = state or empty_care_coordination_state()

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name == "create_care_plan":
            result = create_care_plan(self.state, payload)
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "transition_care_plan":
            result = transition_care_plan(
                self.state,
                payload.get("care_plan_id", ""),
                payload.get("target_state", ""),
                payload.get("reason", ""),
                payload.get("actor_role", ""),
            )
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "add_care_team_member":
            result = add_care_team_member(self.state, payload)
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "create_referral":
            result = create_referral(self.state, payload)
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "receive_referral_result":
            result = receive_referral_result(self.state, payload.get("referral_id"), payload)
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "record_encounter_and_tasks":
            result = record_encounter_and_tasks(self.state, payload)
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "open_care_gap":
            result = open_care_gap(self.state, payload)
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "close_care_gap":
            result = close_care_gap(self.state, payload.get("care_gap_id", ""), payload.get("evidence", {}))
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "create_transition_plan":
            result = create_transition_plan(self.state, payload)
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "complete_transition_plan":
            result = complete_transition_plan(self.state, payload.get("transition_plan_id", ""))
            self.state = result["state"]
            return _wrap_result(name, result)
        if name == "record_outcome_measure":
            result = record_outcome_measure(self.state, payload)
            self.state = result["state"]
            return _wrap_result(name, result)
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {
                "ok": plan["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": {
                    "operation": name,
                    "operation_kind": "command",
                    "owned_tables": plan.get("owned_tables", ()),
                    "read_tables": (),
                    "emitted_event": plan.get("emitted_event"),
                    "transaction_boundary": "owned_datastore_plus_outbox",
                },
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": (plan.get("emitted_event"),),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_depth": plan,
                "side_effects": (),
            }
        contract = _operation_contract(name, "command")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract["emitted_event"],),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "side_effects": (),
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == "query_workbench":
            return {
                **care_coordination_workbench(self.state),
                "operation": name,
                "operation_kind": "query",
                "read_only": True,
            }
        if name == "query_service_contract":
            return {
                "ok": True,
                "operation": name,
                "operation_kind": "query",
                "read_only": True,
                "result": service_operation_contracts(),
                "side_effects": (),
            }
        contract = _operation_contract(name, "query")
        return {
            "ok": True,
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "side_effects": (),
        }


def service_operation_manifest() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "ClinicalCareCoordinationService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "contracts": contracts,
        "operation_contract": contracts[0],
        "side_effects": (),
    }


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test() -> dict:
    service = ClinicalCareCoordinationService()
    command = service.create_care_plan(
        {
            "patient_ref": "patient-smoke",
            "problem": "post discharge follow-up",
            "goal": "close referral loop",
            "responsible_role": "primary_coordinator",
            "review_cadence_days": 7,
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "side_effects": (),
    }
