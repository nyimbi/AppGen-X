"""Standalone one-PBC application surface for court case management."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from . import agent
from . import runtime
from . import ui
from .court_operations_app import (
    case_detail,
    complete_task,
    court_operations_smoke_test,
    court_workbench,
    create_court_case,
    create_task,
    document_instruction_mutation_plan,
    draft_order,
    empty_court_state,
    receive_filing,
    register_evidence,
    schedule_hearing,
    sign_and_enter_order,
    single_pbc_app_contract,
    add_party,
    cure_filing,
)

PBC_KEY = "court_case_management"
PACKAGE_DIR = Path(__file__).resolve().parent
RELEASE_ARTIFACTS = ("README.md", "implementation-plan.md", "implementation-status.md", "RELEASE_EVIDENCE.md")
MIGRATION_PATH = PACKAGE_DIR / "migrations" / "001_initial.sql"
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.COURT_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_policy": "court_operations_default",
    "workbench_limit": 100,
}
DEFAULT_PARAMETERS = {
    "workbench_limit": 100,
    "deficiency_review_hours": 48,
    "hearing_buffer_minutes": 30,
    "evidence_review_window_hours": 24,
}
DEFAULT_RULES = (
    {"rule_id": "court.case_numbering.default", "scope": "case_intake", "status": "active"},
    {"rule_id": "court.filing.deficiency.default", "scope": "filing_review", "status": "active"},
    {"rule_id": "court.hearing.calendar.default", "scope": "hearing_calendar", "status": "active"},
)


class CourtCaseManagementStandaloneApplication:
    """Mutable, package-local standalone application shell for this PBC."""

    def __init__(self, *, tenant: str = "default", state: dict[str, Any] | None = None) -> None:
        self.tenant = tenant
        self.state = deepcopy(state or empty_court_state())
        self.runtime_state = runtime.court_case_management_empty_state()

    def snapshot(self) -> dict[str, Any]:
        return {
            "app_state": deepcopy(self.state),
            "runtime_state": deepcopy(self.runtime_state),
        }

    def configure(self, configuration: dict[str, Any] | None = None) -> dict[str, Any]:
        candidate = {**DEFAULT_CONFIGURATION, **dict(configuration or {})}
        result = runtime.court_case_management_configure_runtime(self.runtime_state, candidate)
        self.runtime_state = result["state"]
        return {**result, "configuration": candidate}

    def register_defaults(self) -> dict[str, Any]:
        current = self.runtime_state
        parameters = []
        for name, value in DEFAULT_PARAMETERS.items():
            outcome = runtime.court_case_management_set_parameter(current, name, value)
            current = outcome["state"]
            parameters.append(outcome["parameter"])
        rules = []
        for rule in DEFAULT_RULES:
            outcome = runtime.court_case_management_register_rule(current, rule)
            current = outcome["state"]
            rules.append(outcome["rule"])
        self.runtime_state = current
        return {"ok": True, "parameters": tuple(parameters), "rules": tuple(rules), "state": self.runtime_state, "side_effects": ()}

    def create_court_case(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = create_court_case(self.state, {"tenant": self.tenant, **dict(payload)})
        self.state = result["state"]
        return result

    def add_party(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = add_party(self.state, dict(payload))
        self.state = result["state"]
        return result

    def receive_filing(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = receive_filing(self.state, dict(payload))
        self.state = result["state"]
        return result

    def cure_filing(self, filing_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        result = cure_filing(self.state, filing_id, dict(payload))
        self.state = result["state"]
        return result

    def register_evidence(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = register_evidence(self.state, dict(payload))
        self.state = result["state"]
        return result

    def schedule_hearing(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = schedule_hearing(self.state, dict(payload))
        self.state = result["state"]
        return result

    def draft_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = draft_order(self.state, dict(payload))
        self.state = result["state"]
        return result

    def sign_and_enter_order(self, order_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        result = sign_and_enter_order(self.state, order_id, dict(payload))
        self.state = result["state"]
        return result

    def create_task(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = create_task(self.state, dict(payload))
        self.state = result["state"]
        return result

    def complete_task(self, task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        result = complete_task(self.state, task_id, dict(payload))
        self.state = result["state"]
        return result

    def query_workbench(self, *, permissions: tuple[str, ...] | None = None) -> dict[str, Any]:
        result = court_workbench(self.state, permissions=permissions)
        return {**result, "configuration": deepcopy(self.runtime_state.get("configuration", {}))}

    def query_case_detail(self, case_id: str, *, permissions: tuple[str, ...] | None = None) -> dict[str, Any]:
        return case_detail(self.state, case_id, permissions=permissions)

    def document_instruction_plan(self, document: str, instruction: str) -> dict[str, Any]:
        plan = agent.document_instruction_plan(document, instruction)
        return {"ok": plan["ok"], "plan": plan, "side_effects": ()}

    def datastore_crud_plan(self, action: str, table: str | None = None, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return agent.datastore_crud_plan(action, table=table, payload=payload)

    def receive_event(self, event: dict[str, Any]) -> dict[str, Any]:
        result = runtime.court_case_management_receive_event(self.runtime_state, event)
        self.runtime_state = result["state"]
        return result


def standalone_manifest() -> dict[str, Any]:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "app_class": "CourtCaseManagementStandaloneApplication",
        "implementation_directory": f"src/pyAppGen/pbcs/{PBC_KEY}",
        "service_methods": (
            "configure",
            "register_defaults",
            "create_court_case",
            "add_party",
            "receive_filing",
            "cure_filing",
            "register_evidence",
            "schedule_hearing",
            "draft_order",
            "sign_and_enter_order",
            "create_task",
            "complete_task",
            "query_workbench",
            "query_case_detail",
            "document_instruction_plan",
            "datastore_crud_plan",
            "receive_event",
        ),
        "ui_surfaces": ("forms", "wizards", "controls", "workbench", "detail"),
        "docs": RELEASE_ARTIFACTS,
        "event_contract": "AppGen-X",
        "event_topic": runtime.COURT_CASE_MANAGEMENT_REQUIRED_EVENT_TOPIC,
        "allowed_backends": runtime.COURT_CASE_MANAGEMENT_ALLOWED_DATABASE_BACKENDS,
        "stream_engine_picker_visible": False,
    }


def build_standalone_app(*, tenant: str = "default") -> CourtCaseManagementStandaloneApplication:
    return CourtCaseManagementStandaloneApplication(tenant=tenant)


def documentation_presence() -> dict[str, Any]:
    docs = tuple({"path": name, "exists": (PACKAGE_DIR / name).exists()} for name in RELEASE_ARTIFACTS)
    return {"ok": all(item["exists"] for item in docs), "docs": docs, "side_effects": ()}


def standalone_smoke_test() -> dict[str, Any]:
    from .routes import dispatch_standalone_route

    app = build_standalone_app(tenant="tenant-smoke")
    config = app.configure()
    defaults = app.register_defaults()
    created = app.create_court_case(
        {
            "court": "CIV",
            "division": "LAW",
            "filing_year": 2026,
            "case_type": "civil",
            "caption": "Roe v. Example",
            "assigned_judge": "Judge Lane",
        }
    )
    party = app.add_party({"case_id": created["court_case"]["id"], "party_name": "Jane Roe", "role": "plaintiff", "lead_counsel": "A. Counsel"})
    filing = app.receive_filing(
        {
            "case_id": created["court_case"]["id"],
            "filing_type": "motion",
            "document_title": "Motion to Compel",
            "received_at": "2026-01-02",
            "deficiency_codes": ("missing_signature",),
            "cure_deadline": "2026-01-09",
        }
    )
    cured = app.cure_filing(filing["filing"]["id"], {"defects_cured": True, "evidence": "signed packet"})
    evidence = app.register_evidence(
        {
            "case_id": created["court_case"]["id"],
            "filing_id": filing["filing"]["id"],
            "description": "Exhibit A",
            "submitted_by": "Jane Roe",
            "submitted_at": "2026-01-03",
        }
    )
    hearing = app.schedule_hearing(
        {
            "case_id": created["court_case"]["id"],
            "hearing_type": "motion",
            "scheduled_at": "2026-01-20T09:00:00",
            "courtroom": "4A",
            "session_block": "AM",
            "assigned_judge": "Judge Lane",
        }
    )
    order = app.draft_order({"case_id": created["court_case"]["id"], "title": "Scheduling Order", "draft_text": "Set hearing."})
    entered = app.sign_and_enter_order(order["court_order"]["id"], {"judge_signature": "Judge Lane", "signed_at": "2026-01-03T10:00:00"})
    task = app.create_task({"case_id": created["court_case"]["id"], "title": "Serve order", "task_type": "service", "assignee": "clerk.one"})
    completed = app.complete_task(task["task"]["id"], {"completed_by": "clerk.one", "completion_notes": "Served all parties."})
    detail = app.query_case_detail(created["court_case"]["id"], permissions=("court_case_management.admin",))
    workbench = app.query_workbench(permissions=("court_case_management.admin",))
    document = app.document_instruction_plan("Exhibit packet", "log evidence")
    crud = app.datastore_crud_plan("update", table="court_case_management_case_task", payload={"status": "completed"})
    handled = app.receive_event({"event_type": runtime.COURT_CASE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "evt-1"})
    duplicate = app.receive_event({"event_type": runtime.COURT_CASE_MANAGEMENT_CONSUMED_EVENT_TYPES[0], "idempotency_key": "evt-1"})
    route = dispatch_standalone_route("GET", "/court-case-management-workbench", {}, app=app)
    checks = (
        config["ok"],
        defaults["ok"],
        created["ok"],
        party["ok"],
        cured["ok"],
        evidence["ok"],
        hearing["ok"],
        entered["ok"],
        completed["ok"],
        detail["ok"],
        workbench["ok"],
        document["ok"],
        crud["ok"],
        handled["ok"],
        duplicate.get("duplicate") is True,
        route["ok"],
    )
    return {
        "ok": all(checks),
        "manifest": standalone_manifest(),
        "state": app.snapshot(),
        "workbench": workbench,
        "detail": detail,
        "route": route,
        "document": document,
        "side_effects": (),
    }


def pbc_source_artifact_contract() -> dict[str, Any]:
    docs = documentation_presence()
    migration_sql = MIGRATION_PATH.read_text(encoding="utf-8")
    return {
        "ok": docs["ok"] and MIGRATION_PATH.exists() and "court_case_management_evidence_item" in migration_sql and "court_case_management_case_task" in migration_sql,
        "pbc": PBC_KEY,
        "docs": docs,
        "migration_path": str(MIGRATION_PATH.relative_to(PACKAGE_DIR)),
        "side_effects": (),
    }


def pbc_implementation_release_audit() -> dict[str, Any]:
    from . import events, routes, services

    smoke = standalone_smoke_test()
    source = pbc_source_artifact_contract()
    service = services.standalone_service_manifest()
    ui_contract = ui.court_case_management_ui_contract()
    event_contract = events.event_contract_manifest()
    boundary = runtime.court_case_management_verify_owned_table_boundary(runtime.COURT_CASE_MANAGEMENT_OWNED_TABLES)
    checks = (
        {"id": "source_artifacts", "ok": source["ok"]},
        {"id": "standalone_smoke", "ok": smoke["ok"]},
        {"id": "service_methods", "ok": service["ok"] and len(service["service_methods"]) >= 12},
        {"id": "ui_forms_wizards_controls", "ok": bool(ui_contract.get("forms")) and bool(ui_contract.get("wizards")) and bool(ui_contract.get("controls"))},
        {"id": "routes_present", "ok": routes.api_route_contracts()["ok"] and len(routes.api_route_contracts()["routes"]) >= 8},
        {"id": "event_contract", "ok": event_contract["ok"] and event_contract["event_contract"] == "AppGen-X"},
        {"id": "owned_boundary", "ok": boundary["ok"]},
    )
    return {"ok": all(check["ok"] for check in checks), "pbc": PBC_KEY, "checks": checks, "smoke": smoke, "side_effects": ()}


def pbc_generation_smoke_audit() -> dict[str, Any]:
    from . import routes

    smoke = standalone_smoke_test()
    ui_contract = ui.court_case_management_ui_contract()
    return {
        "ok": smoke["ok"] and routes.api_route_contracts()["ok"] and len(ui_contract["forms"]) >= 7 and len(ui_contract["wizards"]) >= 6 and len(ui_contract["controls"]) >= 8,
        "pbc": PBC_KEY,
        "route_count": len(routes.api_route_contracts()["routes"]),
        "ui_counts": {
            "forms": len(ui_contract["forms"]),
            "wizards": len(ui_contract["wizards"]),
            "controls": len(ui_contract["controls"]),
        },
        "smoke": smoke,
        "side_effects": (),
    }
