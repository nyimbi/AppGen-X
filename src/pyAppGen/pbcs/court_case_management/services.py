"""Service layer for the court_case_management PBC."""
from __future__ import annotations

from . import standalone
from .court_operations_app import (
    BUSINESS_TABLES,
    add_party,
    case_detail,
    complete_task,
    court_workbench,
    create_court_case,
    create_task,
    draft_order,
    empty_court_state,
    receive_filing,
    register_evidence,
    schedule_hearing,
    sign_and_enter_order,
)
from .domain_depth import DOMAIN_OPERATIONS as DOMAIN_DEPTH_COMMAND_OPERATIONS, DOMAIN_OWNED_TABLES as DOMAIN_DEPTH_OWNED_TABLES, execute_domain_operation as execute_domain_depth_operation

PBC_KEY = "court_case_management"
EVENT_CONTRACT = {
    "outbox_table": f"{PBC_KEY}_appgen_outbox_event",
    "inbox_table": f"{PBC_KEY}_appgen_inbox_event",
    "dead_letter_table": f"{PBC_KEY}_appgen_dead_letter_event",
    "event_contract": "AppGen-X",
}
COURT_COMMAND_OPERATIONS = (
    "create_court_case",
    "add_party",
    "receive_filing",
    "register_evidence",
    "schedule_hearing",
    "create_task",
    "complete_task",
    "draft_order",
    "sign_and_enter_order",
)
COMMAND_OPERATIONS = tuple(
    dict.fromkeys(
        (
            "command_court_case",
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "receive_event",
            "run_advanced_assessment",
            "parse_document_instruction",
        )
        + COURT_COMMAND_OPERATIONS
        + tuple(DOMAIN_DEPTH_COMMAND_OPERATIONS)
    )
)
QUERY_OPERATIONS = ("query_workbench", "query_case_detail")
OWNED_TABLES = DOMAIN_DEPTH_OWNED_TABLES


def _operation_contract(name: str, kind: str) -> dict:
    return {
        "operation": name,
        "operation_kind": kind,
        "owned_tables": BUSINESS_TABLES if kind == "command" else (),
        "read_tables": BUSINESS_TABLES if kind == "query" else (),
        "emitted_event": "CourtCaseManagementCreated" if kind == "command" else None,
        "transaction_boundary": "owned_datastore_plus_outbox" if kind == "command" else "read_only_projection",
    }


class CourtCaseManagementService:
    def __init__(self, state: dict | None = None):
        self.state = state or empty_court_state()

    def __getattr__(self, name: str):
        if name in COMMAND_OPERATIONS:
            return lambda payload=None, _name=name: self._command(_name, payload or {})
        if name in QUERY_OPERATIONS:
            return lambda payload=None, _name=name: self._query(_name, payload or {})
        raise AttributeError(name)

    def _command(self, name: str, payload: dict) -> dict:
        if name == "create_court_case":
            result = create_court_case(self.state, payload)
        elif name == "add_party":
            result = add_party(self.state, payload)
        elif name == "receive_filing":
            result = receive_filing(self.state, payload)
        elif name == "register_evidence":
            result = register_evidence(self.state, payload)
        elif name == "schedule_hearing":
            result = schedule_hearing(self.state, payload)
        elif name == "create_task":
            result = create_task(self.state, payload)
        elif name == "complete_task":
            result = complete_task(self.state, payload.get("task_id"), payload)
        elif name == "draft_order":
            result = draft_order(self.state, payload)
        elif name == "sign_and_enter_order":
            result = sign_and_enter_order(self.state, payload.get("order_id"), payload)
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
        self.state = result["state"]
        return {
            **result,
            "operation": name,
            "operation_kind": "command",
            "transaction_boundary": "owned_datastore_plus_outbox",
            "outbox_table": EVENT_CONTRACT["outbox_table"],
        }

    def _query(self, name: str, payload: dict) -> dict:
        if name == "query_workbench":
            return {**court_workbench(self.state, permissions=tuple(payload.get("permissions", ()))), "operation": name, "operation_kind": "query", "read_only": True}
        if name == "query_case_detail":
            return {
                **case_detail(self.state, payload.get("case_id"), permissions=tuple(payload.get("permissions", ()))),
                "operation": name,
                "operation_kind": "query",
                "read_only": True,
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


class CourtCaseManagementStandaloneService:
    """Executable standalone service wrapper for the one-PBC application."""

    def __init__(self, *, tenant: str = "default") -> None:
        self.app = standalone.CourtCaseManagementStandaloneApplication(tenant=tenant)

    @property
    def state(self) -> dict:
        return self.app.snapshot()

    def configure(self, configuration: dict | None = None) -> dict:
        return self.app.configure(configuration)

    def register_defaults(self) -> dict:
        return self.app.register_defaults()

    def create_court_case(self, payload: dict) -> dict:
        return self.app.create_court_case(payload)

    def add_party(self, payload: dict) -> dict:
        return self.app.add_party(payload)

    def receive_filing(self, payload: dict) -> dict:
        return self.app.receive_filing(payload)

    def cure_filing(self, filing_id: str, payload: dict) -> dict:
        return self.app.cure_filing(filing_id, payload)

    def register_evidence(self, payload: dict) -> dict:
        return self.app.register_evidence(payload)

    def schedule_hearing(self, payload: dict) -> dict:
        return self.app.schedule_hearing(payload)

    def draft_order(self, payload: dict) -> dict:
        return self.app.draft_order(payload)

    def sign_and_enter_order(self, order_id: str, payload: dict) -> dict:
        return self.app.sign_and_enter_order(order_id, payload)

    def create_task(self, payload: dict) -> dict:
        return self.app.create_task(payload)

    def complete_task(self, task_id: str, payload: dict) -> dict:
        return self.app.complete_task(task_id, payload)

    def query_workbench(self, payload: dict | None = None) -> dict:
        payload = payload or {}
        return self.app.query_workbench(permissions=tuple(payload.get("permissions", ())))

    def query_case_detail(self, payload: dict) -> dict:
        return self.app.query_case_detail(payload["case_id"], permissions=tuple(payload.get("permissions", ())))

    def document_instruction_plan(self, document: str, instruction: str) -> dict:
        return self.app.document_instruction_plan(document, instruction)

    def datastore_crud_plan(self, action: str, table: str | None = None, payload: dict | None = None) -> dict:
        return self.app.datastore_crud_plan(action, table=table, payload=payload)

    def receive_event(self, event: dict) -> dict:
        return self.app.receive_event(event)


def standalone_service_manifest() -> dict:
    manifest = standalone.standalone_manifest()
    return {
        "ok": manifest["ok"],
        "pbc": PBC_KEY,
        "service_class": "CourtCaseManagementStandaloneService",
        "service_methods": manifest["service_methods"],
        "query_methods": ("query_workbench", "query_case_detail", "datastore_crud_plan"),
        "event_contract": "AppGen-X",
        "event_topic": EVENT_CONTRACT["outbox_table"].replace("_appgen_outbox_event", ".events"),
        "stream_engine_picker_visible": False,
        "side_effects": (),
    }


def service_operation_manifest() -> dict:
    contracts = service_operation_contracts()
    return {
        "ok": contracts["ok"],
        "pbc": PBC_KEY,
        "service_class": "CourtCaseManagementService",
        "command_operations": COMMAND_OPERATIONS,
        "query_operations": QUERY_OPERATIONS,
        "event_contract": EVENT_CONTRACT,
        "standalone_service": standalone_service_manifest(),
        "side_effects": (),
    }


def service_operation_contracts() -> dict:
    contracts = tuple(_operation_contract(name, "command") for name in COMMAND_OPERATIONS) + tuple(_operation_contract(name, "query") for name in QUERY_OPERATIONS)
    return {"ok": True, "pbc": PBC_KEY, "contracts": contracts, "operation_contract": contracts[0], "side_effects": ()}


def operation_plan(operation: str, payload: dict | None = None) -> dict:
    manifest = service_operation_manifest()
    kind = "query" if operation in manifest["query_operations"] else "command"
    return {"ok": operation in manifest["query_operations"] + manifest["command_operations"], "operation": operation, "operation_kind": kind, "payload": dict(payload or {}), "side_effects": ()}


def smoke_test() -> dict:
    service = CourtCaseManagementStandaloneService(tenant="tenant-smoke")
    service.configure()
    service.register_defaults()
    created = service.create_court_case({"court": "CIV", "division": "LAW", "filing_year": 2026, "case_type": "civil", "caption": "Roe v. Example"})
    queried = service.query_workbench({"permissions": ("court_case_management.admin",)})
    return {"ok": created["ok"] and queried["ok"] and service_operation_contracts()["ok"], "command": created, "query": queried, "side_effects": ()}
