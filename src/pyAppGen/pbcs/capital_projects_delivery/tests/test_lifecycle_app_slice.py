from pyAppGen.pbcs.capital_projects_delivery.agent import chatbot_interface_contract
from pyAppGen.pbcs.capital_projects_delivery.routes import dispatch_route
from pyAppGen.pbcs.capital_projects_delivery.runtime import (
    GATE_DEFINITIONS,
    capital_projects_delivery_approve_capital_project_gate,
    capital_projects_delivery_build_single_pbc_app_contract,
    capital_projects_delivery_build_workbench_view,
    capital_projects_delivery_command_capital_project,
    capital_projects_delivery_empty_state,
    capital_projects_delivery_get_capital_project_detail,
    capital_projects_delivery_query_workbench,
    capital_projects_delivery_record_gate_checklist,
)
from pyAppGen.pbcs.capital_projects_delivery.services import CapitalProjectsDeliveryService
from pyAppGen.pbcs.capital_projects_delivery.ui import capital_projects_delivery_ui_contract


def test_capital_project_creation_defaults_to_governed_lifecycle():
    created = capital_projects_delivery_command_capital_project(
        capital_projects_delivery_empty_state(),
        {
            "tenant": "tenant-a",
            "code": "PRJ-100",
            "name": "Gate Controlled Project",
            "reported_at": "2026-05-29",
        },
    )
    record = created["record"]
    assert created["ok"] is True
    assert record["lifecycle_stage"] == "idea"
    assert record["next_stage"] == "screening"
    assert record["gate_status"] == "blocked"
    assert created["state"]["outbox"][-1]["event_type"] == "CapitalProjectsDeliveryCreated"


def test_gate_transition_rejects_missing_exit_criteria_and_records_exception():
    created = capital_projects_delivery_command_capital_project(
        capital_projects_delivery_empty_state(),
        {
            "tenant": "tenant-a",
            "code": "PRJ-101",
            "name": "Blocked Project",
            "reported_at": "2026-05-29",
        },
    )
    rejected = capital_projects_delivery_approve_capital_project_gate(
        created["state"],
        project_id="PRJ-101",
        target_stage="screening",
        approver_role=GATE_DEFINITIONS["screening"]["required_approver_role"],
        approved_by="sponsor.user",
        approved_at="2026-05-29",
    )
    assert rejected["ok"] is False
    assert rejected["reason"] == "exit_criteria_incomplete"
    assert rejected["validation"]["blocked_criteria"] == (
        "business_case_defined",
        "sponsorship_assigned",
    )
    assert rejected["state"]["outbox"][-1]["event_type"] == "CapitalProjectsDeliveryExceptionOpened"


def test_gate_approval_requires_rebaseline_reason_on_backward_move():
    created = capital_projects_delivery_command_capital_project(
        capital_projects_delivery_empty_state(),
        {
            "tenant": "tenant-a",
            "code": "PRJ-102",
            "name": "Rollback Project",
            "reported_at": "2026-05-29",
        },
    )
    checklist = capital_projects_delivery_record_gate_checklist(
        created["state"],
        "PRJ-102",
        {"business_case_defined": True, "sponsorship_assigned": True},
        context={"updated_by": "controls", "updated_at": "2026-05-29"},
    )
    approved = capital_projects_delivery_approve_capital_project_gate(
        checklist["state"],
        project_id="PRJ-102",
        target_stage="screening",
        approver_role="project_sponsor",
        approved_by="sponsor.user",
        approved_at="2026-05-29",
    )
    rejected_rollback = capital_projects_delivery_approve_capital_project_gate(
        approved["state"],
        project_id="PRJ-102",
        target_stage="idea",
        approver_role="project_sponsor",
        approved_by="sponsor.user",
        approved_at="2026-05-30",
    )
    accepted_rollback = capital_projects_delivery_approve_capital_project_gate(
        approved["state"],
        project_id="PRJ-102",
        target_stage="idea",
        approver_role="project_sponsor",
        approved_by="sponsor.user",
        approved_at="2026-05-30",
        rebaseline_reason="Scope reset after sanction challenge",
    )
    assert rejected_rollback["ok"] is False
    assert rejected_rollback["reason"] == "rebaseline_reason_required"
    assert accepted_rollback["ok"] is True
    assert accepted_rollback["record"]["rebaseline_required"] is True
    assert accepted_rollback["record"]["rebaseline_count"] == 1
    assert accepted_rollback["approval"]["rebaseline_reason"] == "Scope reset after sanction challenge"


def test_single_pbc_service_routes_workbench_and_agent_help_are_usable():
    app_contract = capital_projects_delivery_build_single_pbc_app_contract()
    service = CapitalProjectsDeliveryService()

    create = dispatch_route(
        "POST /capital-projects",
        {
            "tenant": "tenant-b",
            "code": "PRJ-103",
            "name": "App Usability Project",
            "reported_at": "2026-05-29",
        },
        service=service,
    )
    checklist = dispatch_route(
        "POST /capital-projects/{project_id}/gate-checklists",
        {
            "project_id": "PRJ-103",
            "criteria_status": {
                "business_case_defined": True,
                "sponsorship_assigned": True,
            },
            "updated_by": "controls",
            "updated_at": "2026-05-29",
        },
        service=service,
    )
    approve = dispatch_route(
        "POST /capital-projects/{project_id}/gate-approvals",
        {
            "project_id": "PRJ-103",
            "target_stage": "screening",
            "approver_role": "project_sponsor",
            "approved_by": "sponsor.user",
            "approved_at": "2026-05-29",
        },
        service=service,
    )
    detail = service.get_capital_project_detail({"project_id": "PRJ-103"})["result"]
    workbench = service.query_workbench({"tenant": "tenant-b"})["result"]
    ui = capital_projects_delivery_ui_contract()
    agent_help = chatbot_interface_contract()

    assert app_contract["ok"] is True
    assert create["ok"] is True and checklist["ok"] is True and approve["ok"] is True
    assert detail["ok"] is True
    assert detail["project"]["lifecycle_stage"] == "screening"
    assert len(detail["forms"]) >= 3
    assert len(detail["controls"]) >= 4
    assert workbench["ok"] is True
    assert workbench["summary"]["project_count"] == 1
    assert capital_projects_delivery_build_workbench_view()["views"] == (
        "gate_status_board",
        "readiness_grid",
        "approval_queue",
    )
    assert capital_projects_delivery_query_workbench(service._state, {"tenant": "tenant-b"})["ok"] is True
    assert capital_projects_delivery_get_capital_project_detail(service._state, "PRJ-103")["ok"] is True
    assert ui["ok"] is True
    assert len(ui["forms"]) >= 3
    assert len(ui["wizards"]) >= 2
    assert agent_help["ok"] is True
    assert agent_help["help_contract"]["guided_tasks"]
