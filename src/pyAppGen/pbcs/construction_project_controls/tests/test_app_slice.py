from pyAppGen.pbcs.construction_project_controls.agent import document_instruction_plan
from pyAppGen.pbcs.construction_project_controls.routes import dispatch_route
from pyAppGen.pbcs.construction_project_controls.runtime import (
    construction_project_controls_build_go_live_scorecard,
    construction_project_controls_build_workbench_view,
    construction_project_controls_empty_state,
    construction_project_controls_get_construction_project_detail,
    construction_project_controls_query_workbench,
)
from pyAppGen.pbcs.construction_project_controls.services import ConstructionProjectControlsService
from pyAppGen.pbcs.construction_project_controls.ui import construction_project_controls_ui_contract


def _create_seeded_service():
    service = ConstructionProjectControlsService(construction_project_controls_empty_state())
    created = dispatch_route(
        "POST /construction-projects",
        {
            "tenant": "tenant-a",
            "code": "CP-200",
            "name": "Controls Slice Project",
            "reported_at": "2026-05-29",
            "approved_budget": 200000.0,
            "original_budget": 200000.0,
        },
        service=service,
    )
    baseline = dispatch_route(
        "POST /construction-projects/{project_id}/baseline-revisions",
        {
            "project_id": "CP-200",
            "baseline_start_date": "2026-06-01",
            "baseline_finish_date": "2026-11-30",
            "freeze_reason": "IFC complete",
            "approved_by": "controls.lead",
            "approved_at": "2026-05-29",
            "approver_role": "project_controls_manager",
        },
        service=service,
    )
    work_package = dispatch_route(
        "POST /work-packages",
        {
            "project_id": "CP-200",
            "wbs_code": "1.1",
            "name": "Concrete foundations",
            "control_account": "CIV-01",
            "discipline": "civil",
            "area": "podium",
            "contractor": "BuildCo",
            "progress_method": "quantity_installed",
            "planned_quantity": 100.0,
            "measurement_unit": "m3",
            "planned_percent_complete": 40.0,
            "approved_budget": 75000.0,
        },
        service=service,
    )
    progress = dispatch_route(
        "POST /site-progress",
        {
            "project_id": "CP-200",
            "work_package_id": work_package["result"]["result"]["record"]["id"],
            "measurement_date": "2026-06-30",
            "installed_quantity": 50.0,
            "actual_cost_incurred": 30000.0,
            "submission_key": "cp-200-progress-1",
            "evidence_bundle": {"photos": 5, "inspection_report": "IR-77"},
        },
        service=service,
    )
    risk = dispatch_route(
        "POST /schedule-risks",
        {
            "project_id": "CP-200",
            "work_package_id": work_package["result"]["result"]["record"]["id"],
            "current_float_days": -1,
            "prior_float_days": 4,
            "owner": "scheduler",
        },
        service=service,
    )
    return service, created, baseline, work_package, progress, risk


def test_project_controls_flow_computes_wbs_progress_and_earned_value():
    service, created, baseline, work_package, progress, risk = _create_seeded_service()
    detail = service.get_construction_project_detail({"project_id": "CP-200"})["result"]

    assert created["ok"] is True
    assert baseline["ok"] is True
    assert work_package["ok"] is True
    assert progress["ok"] is True
    assert risk["ok"] is True
    assert detail["ok"] is True
    assert detail["project"]["baseline"]["status"] == "frozen"
    assert detail["project"]["metrics"]["bcwp"] == 37500.0
    assert detail["project"]["metrics"]["acwp"] == 30000.0
    assert detail["project"]["metrics"]["cpi"] == 1.25
    assert detail["project"]["metrics"]["spi"] == 1.25
    assert detail["project"]["wbs_hierarchy"][0]["wbs_code"] == "1.1"
    assert detail["project"]["schedule_risks"][0]["path_status"] == "critical"


def test_progress_alias_and_document_instruction_preview_are_supported():
    service, _, _, work_package, _, _ = _create_seeded_service()
    alias = dispatch_route(
        "POST /site-progresss",
        {
            "project_id": "CP-200",
            "work_package_id": work_package["result"]["result"]["record"]["id"],
            "measurement_date": "2026-07-07",
            "installed_quantity": 70.0,
            "actual_cost_incurred": 5000.0,
            "submission_key": "cp-200-progress-2",
            "evidence_bundle": {"photos": 2},
        },
        service=service,
    )
    plan = document_instruction_plan(
        "Site minutes: RFI 004 on WBS 1.1 requires response by 2026-07-10",
        "Draft an RFI record",
    )
    assert alias["ok"] is True
    assert plan["ok"] is True
    assert plan["domain_plan"]["target_entity"] == "rfi"
    assert "rfi" in plan["candidate_tables"][0]


def test_workbench_ui_and_release_scorecard_surface_the_one_pbc_app():
    service, _, _, _, _, _ = _create_seeded_service()
    workbench = service.query_workbench({"tenant": "tenant-a"})["result"]
    ui = construction_project_controls_ui_contract()
    direct = construction_project_controls_query_workbench(service._state, {"project_id": "CP-200"})
    detail = construction_project_controls_get_construction_project_detail(service._state, "CP-200")
    scorecard = construction_project_controls_build_go_live_scorecard(service._state, project_id="CP-200")

    assert workbench["ok"] is True
    assert workbench["summary"]["project_count"] == 1
    assert construction_project_controls_build_workbench_view()["views"] == (
        "portfolio_risk_board",
        "wbs_rollup_tree",
        "earned_value_dashboard",
        "exception_queue",
    )
    assert direct["ok"] is True
    assert detail["ok"] is True
    assert scorecard["scorecard"]["categories"]["data_model_ready"] is True
    assert ui["ok"] is True
    assert len(ui["forms"]) >= 5
    assert len(ui["wizards"]) >= 3
    assert len(ui["controls"]) >= 5
