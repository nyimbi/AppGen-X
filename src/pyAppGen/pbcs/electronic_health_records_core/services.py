"""Service layer for the electronic_health_records_core PBC."""
from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES
from .domain_depth import execute_domain_operation as execute_domain_depth_operation
from .ehr_core_app import (
    acknowledge_critical_result,
    assemble_patient_summary,
    attest_care_note,
    create_medication_list,
    create_patient_chart,
    ehr_core_workbench,
    empty_ehr_state,
    review_chart_merge,
    review_clinical_order,
    record_care_note,
    record_clinical_encounter,
    simulate_allergy,
    transition_clinical_order,
    approve_observation,
)

PBC_KEY = "electronic_health_records_core"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
EHR_CORE_COMMANDS = (
    "create_patient_chart",
    "review_chart_merge",
    "record_clinical_encounter",
    "review_clinical_order",
    "transition_clinical_order",
    "approve_observation",
    "acknowledge_critical_result",
    "simulate_allergy",
    "create_medication_list",
    "record_care_note",
    "attest_care_note",
)
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(("command_patient_chart", "configure_runtime", "set_parameter", "register_rule") + EHR_CORE_COMMANDS + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS))
)
QUERY_OPERATIONS = ("query_workbench", "assemble_patient_summary")
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES[:4] if kind == "command" else (),
        "read_tables": OWNED_TABLES[:4] if kind == "query" else (),
        "emitted_event": "ElectronicHealthRecordsCoreCreated" if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class ElectronicHealthRecordsCoreService:
    def __init__(self, state: dict | None = None):
        self.state = state or empty_ehr_state()

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        handler_map = {
            "create_patient_chart": lambda: create_patient_chart(self.state, payload),
            "review_chart_merge": lambda: review_chart_merge(self.state, payload["chart_id"], payload),
            "record_clinical_encounter": lambda: record_clinical_encounter(self.state, payload),
            "review_clinical_order": lambda: review_clinical_order(self.state, payload),
            "transition_clinical_order": lambda: transition_clinical_order(self.state, payload["order_id"], payload),
            "approve_observation": lambda: approve_observation(self.state, payload),
            "acknowledge_critical_result": lambda: acknowledge_critical_result(self.state, payload["observation_id"], payload),
            "simulate_allergy": lambda: simulate_allergy(self.state, payload),
            "create_medication_list": lambda: create_medication_list(self.state, payload),
            "record_care_note": lambda: record_care_note(self.state, payload),
            "attest_care_note": lambda: attest_care_note(self.state, payload["note_id"], payload),
        }
        if name in handler_map:
            result = handler_map[name]()
            self.state = result["state"]
            return {
                **result,
                "operation": name,
                "operation_kind": "command",
                "transaction_boundary": "owned_datastore_plus_outbox",
                "outbox_table": EVENT_CONTRACT["outbox_table"],
            }
        if name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
            plan = execute_domain_depth_operation(name, payload)
            return {
                "ok": plan["ok"],
                "operation": name,
                "operation_kind": plan["operation_kind"],
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": {
                    "operation": name,
                    "operation_kind": plan["operation_kind"],
                    "owned_tables": plan.get("owned_tables", ()),
                    "read_tables": plan.get("read_tables", ()),
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
            return {**ehr_core_workbench(self.state, payload), "operation": name, "operation_kind": "query", "read_only": True}
        if name == "assemble_patient_summary":
            result = assemble_patient_summary(self.state, payload["chart_id"], payload)
            return {**result, "operation": name, "operation_kind": "query", "read_only": True}
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
        "service_class": "ElectronicHealthRecordsCoreService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(
        _operation_contract(name, "query") for name in QUERY_OPERATIONS
    )
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


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
    service = ElectronicHealthRecordsCoreService()
    command = service.create_patient_chart(
        {
            "tenant": "tenant-smoke",
            "patient_ref": "patient-smoke",
            "legal_name": "Smoke Patient",
            "date_of_birth": "1975-01-01",
            "gender": "unknown",
        }
    )
    query = service.query_workbench({"tenant": "tenant-smoke"})
    return {
        "ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"],
        "command": command,
        "query": query,
        "side_effects": (),
    }
