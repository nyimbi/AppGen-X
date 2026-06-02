"""Service layer for the education_student_lifecycle PBC."""

from __future__ import annotations

from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS
from .domain_depth import DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES
from .domain_depth import execute_domain_operation as execute_domain_depth_operation
from .student_lifecycle_app import (
    activate_enrollment,
    award_credential,
    build_student_lifecycle_workbench,
    empty_student_lifecycle_state,
    evaluate_degree_audit,
    finalize_assessment_result,
    maintain_curriculum_plan,
    open_advising_case,
    project_student_risk,
    record_engagement_projection,
    record_hold_projection,
    record_intervention_plan,
    record_transfer_credit,
    register_course_attempt,
    register_student_applicant,
    review_applicant_documents,
    submit_academic_petition,
    prepare_graduation_clearance,
)

PBC_KEY = "education_student_lifecycle"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
APP_COMMAND_HANDLERS = {
    "register_student_applicant": register_student_applicant,
    "review_applicant_documents": review_applicant_documents,
    "activate_enrollment": activate_enrollment,
    "maintain_curriculum_plan": maintain_curriculum_plan,
    "record_hold_projection": record_hold_projection,
    "record_engagement_projection": record_engagement_projection,
    "register_course_attempt": register_course_attempt,
    "finalize_assessment_result": finalize_assessment_result,
    "open_advising_case": open_advising_case,
    "record_intervention_plan": record_intervention_plan,
    "submit_academic_petition": submit_academic_petition,
    "record_transfer_credit": record_transfer_credit,
    "evaluate_degree_audit": evaluate_degree_audit,
    "project_student_risk": project_student_risk,
    "prepare_graduation_clearance": prepare_graduation_clearance,
    "award_credential": award_credential,
}
APP_QUERY_HANDLERS = {"build_student_lifecycle_workbench": build_student_lifecycle_workbench}
COMMAND_OPERATIONS = tuple(dict.fromkeys(("command_student_applicant", "configure_runtime", "set_parameter", "register_rule") + tuple(APP_COMMAND_HANDLERS) + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)))
QUERY_OPERATIONS = ("query_workbench",) + tuple(APP_QUERY_HANDLERS)
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES


def _operation_contract(name, kind):
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES[:2] if kind == "command" else (),
        "read_tables": OWNED_TABLES[:4] if kind == "query" else (),
        "emitted_event": "EducationStudentLifecycleUpdated" if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class EducationStudentLifecycleService:
    def __init__(self, state=None):
        self.state = state or empty_student_lifecycle_state()

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name in APP_COMMAND_HANDLERS:
            result = APP_COMMAND_HANDLERS[name](self.state, payload)
            if "state" in result:
                self.state = result["state"]
            target = next((value.get("table") for value in result.values() if isinstance(value, dict) and value.get("table")), OWNED_TABLES[0])
            return {
                "ok": result["ok"],
                "operation": name,
                "operation_kind": "command",
                "read_only": False,
                "payload": dict(payload),
                "operation_contract": {
                    "operation": name,
                    "operation_kind": "command",
                    "owned_tables": (target,),
                    "read_tables": (),
                    "emitted_event": "EducationStudentLifecycleUpdated",
                    "transaction_boundary": "owned_datastore_plus_outbox",
                },
                "outbox_table": EVENT_CONTRACT["outbox_table"],
                "emits": ("EducationStudentLifecycleUpdated",),
                "transaction_boundary": "owned_datastore_plus_outbox",
                "domain_app": result,
                "side_effects": (),
            }
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

    def _query(self, name, payload):
        if name in APP_QUERY_HANDLERS:
            result = APP_QUERY_HANDLERS[name](self.state)
            return {
                "ok": result["ok"],
                "operation": name,
                "operation_kind": "query",
                "read_only": True,
                "payload": dict(payload),
                "operation_contract": {
                    "operation": name,
                    "operation_kind": "query",
                    "owned_tables": (),
                    "read_tables": OWNED_TABLES,
                    "emitted_event": None,
                    "transaction_boundary": "read_only_projection",
                },
                "outbox_table": None,
                "emits": (),
                "domain_app": result,
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


def service_operation_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "EducationStudentLifecycleService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts():
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, "query") for name in QUERY_OPERATIONS)
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {"ok": operation in manifest["query_operations"] + manifest["command_operations"], "operation": operation, "operation_kind": kind, "payload": dict(payload or {}), "side_effects": ()}


def smoke_test():
    service = EducationStudentLifecycleService()
    command = service.register_student_applicant({"applicant_id": "svc-smoke", "program_code": "BSCS", "required_documents": (), "application_stage": "accepted", "decision_status": "accepted"})
    query = service.build_student_lifecycle_workbench({})
    return {"ok": command["ok"] and query["ok"] and service_operation_contracts()["ok"], "command": command, "query": query, "side_effects": ()}
