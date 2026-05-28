"""Service layer for the construction_project_controls PBC."""
from __future__ import annotations

from .domain_depth import (
    DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS,
    execute_domain_operation as execute_domain_depth_operation,
)
from .runtime import (
    CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES,
    CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES,
    construction_project_controls_approve_baseline_revision,
    construction_project_controls_build_agent_help_contract,
    construction_project_controls_build_single_pbc_app_contract,
    construction_project_controls_build_workbench_view,
    construction_project_controls_command_construction_project,
    construction_project_controls_configure_runtime,
    construction_project_controls_create_change_event,
    construction_project_controls_empty_state,
    construction_project_controls_freeze_reporting_period,
    construction_project_controls_get_construction_project_detail,
    construction_project_controls_parse_document_instruction,
    construction_project_controls_query_workbench,
    construction_project_controls_receive_event,
    construction_project_controls_record_schedule_risk,
    construction_project_controls_record_site_progress,
    construction_project_controls_record_work_package,
    construction_project_controls_register_rule,
    construction_project_controls_register_schema_extension,
    construction_project_controls_review_rfi,
    construction_project_controls_run_advanced_assessment,
    construction_project_controls_set_parameter,
    construction_project_controls_approve_submittal,
)

PBC_KEY = "construction_project_controls"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
OWNED_TABLES = CONSTRUCTION_PROJECT_CONTROLS_OWNED_TABLES
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "command_construction_project",
            "approve_baseline_revision",
            "record_work_package",
            "review_rfi",
            "approve_submittal",
            "record_site_progress",
            "create_change_event",
            "record_schedule_risk",
            "freeze_reporting_period",
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = (
    "query_workbench",
    "get_construction_project_detail",
    "build_workbench_view",
    "build_single_pbc_app_contract",
    "build_agent_help_contract",
)


def _operation_contract(name, kind):
    emitted_event = None
    if kind == "command":
        if name in ("approve_baseline_revision", "approve_submittal", "freeze_reporting_period"):
            emitted_event = CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[2]
        elif name in ("record_schedule_risk",):
            emitted_event = CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[3]
        else:
            emitted_event = CONSTRUCTION_PROJECT_CONTROLS_EMITTED_EVENT_TYPES[1]
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": OWNED_TABLES[:2] if kind == "command" else (),
        "read_tables": OWNED_TABLES[:2] if kind == "query" else (),
        "emitted_event": emitted_event,
        "transaction_boundary": (
            "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection"
        ),
    }


class ConstructionProjectControlsService:
    def __init__(self, state=None):
        self._state = construction_project_controls_empty_state() if state is None else state

    def __getattr__(self, name):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name, payload):
        if name == "command_construction_project":
            result = construction_project_controls_command_construction_project(self._state, payload)
        elif name == "approve_baseline_revision":
            result = construction_project_controls_approve_baseline_revision(self._state, payload)
        elif name == "record_work_package":
            result = construction_project_controls_record_work_package(self._state, payload)
        elif name == "review_rfi":
            result = construction_project_controls_review_rfi(self._state, payload)
        elif name == "approve_submittal":
            result = construction_project_controls_approve_submittal(self._state, payload)
        elif name == "record_site_progress":
            result = construction_project_controls_record_site_progress(self._state, payload)
        elif name == "create_change_event":
            result = construction_project_controls_create_change_event(self._state, payload)
        elif name == "record_schedule_risk":
            result = construction_project_controls_record_schedule_risk(self._state, payload)
        elif name == "freeze_reporting_period":
            result = construction_project_controls_freeze_reporting_period(self._state, payload)
        elif name == "configure_runtime":
            result = construction_project_controls_configure_runtime(self._state, payload)
        elif name == "set_parameter":
            result = construction_project_controls_set_parameter(
                self._state,
                payload["name"],
                payload.get("value"),
            )
        elif name == "register_rule":
            result = construction_project_controls_register_rule(self._state, payload)
        elif name == "register_schema_extension":
            result = construction_project_controls_register_schema_extension(
                self._state,
                payload["table"],
                payload.get("fields", {}),
            )
        elif name == "receive_event":
            result = construction_project_controls_receive_event(self._state, payload)
        elif name == "run_advanced_assessment":
            result = construction_project_controls_run_advanced_assessment(self._state, payload)
        elif name == "parse_document_instruction":
            result = construction_project_controls_parse_document_instruction(
                payload.get("document", ""),
                payload.get("instruction", ""),
            )
        elif name in DOMAIN_DEPTH_COMMAND_OPERATIONS:
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
        else:
            result = {"ok": False, "reason": "unsupported_command", "side_effects": ()}

        if "state" in result:
            self._state = result["state"]
        contract = _operation_contract(name, "command")
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "command",
            "read_only": False,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": EVENT_CONTRACT["outbox_table"],
            "emits": (contract["emitted_event"],) if contract["emitted_event"] else (),
            "transaction_boundary": "owned_datastore_plus_outbox",
            "result": result,
            "state": self._state,
            "side_effects": (),
        }

    def _query(self, name, payload):
        if name == "query_workbench":
            result = construction_project_controls_query_workbench(self._state, payload)
        elif name == "get_construction_project_detail":
            result = construction_project_controls_get_construction_project_detail(
                self._state,
                payload["project_id"],
            )
        elif name == "build_workbench_view":
            result = construction_project_controls_build_workbench_view(
                tenant=payload.get("tenant", "default"),
            )
        elif name == "build_single_pbc_app_contract":
            result = construction_project_controls_build_single_pbc_app_contract()
        elif name == "build_agent_help_contract":
            result = construction_project_controls_build_agent_help_contract()
        else:
            result = {"ok": False, "reason": "unsupported_query", "side_effects": ()}
        contract = _operation_contract(name, "query")
        return {
            "ok": result["ok"],
            "operation": name,
            "operation_kind": "query",
            "read_only": True,
            "payload": dict(payload),
            "operation_contract": contract,
            "outbox_table": None,
            "emits": (),
            "result": result,
            "side_effects": (),
        }


def service_operation_manifest():
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "service_class": "ConstructionProjectControlsService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def service_operation_contracts():
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


def operation_plan(operation, payload=None):
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {
        "ok": operation in manifest["query_operations"] + manifest["command_operations"],
        "operation": operation,
        "operation_kind": kind,
        "payload": dict(payload or {}),
        "side_effects": (),
    }


def smoke_test():
    service = ConstructionProjectControlsService()
    created = service.command_construction_project(
        {
            "tenant": "tenant-smoke",
            "code": "CP-100",
            "name": "Service Smoke",
            "reported_at": "2026-05-29",
            "approved_budget": 150000.0,
        }
    )
    baseline = service.approve_baseline_revision(
        {
            "project_id": "CP-100",
            "baseline_start_date": "2026-06-01",
            "baseline_finish_date": "2026-09-15",
            "freeze_reason": "Approved recovery plan",
            "approved_by": "controls.lead",
            "approved_at": "2026-05-29",
            "approver_role": "project_controls_manager",
        }
    )
    workbench = service.query_workbench({"tenant": "tenant-smoke"})
    detail = service.get_construction_project_detail({"project_id": "CP-100"})
    app = service.build_single_pbc_app_contract()
    return {
        "ok": created["ok"] and baseline["ok"] and workbench["ok"] and detail["ok"] and app["ok"],
        "created": created,
        "baseline": baseline,
        "workbench": workbench,
        "detail": detail,
        "app": app,
        "side_effects": (),
    }
