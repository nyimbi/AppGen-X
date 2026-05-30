from pyAppGen.pbcs.construction_project_controls.project_control import (
    CAPABILITY_TABLES,
    EVENT_CONTRACT,
    PROJECT_CONTROL_CAPABILITIES,
    PROJECT_CONTROL_FUNCTIONS,
    REQUIRED_FIELDS,
    SLUG_BY_NUMBER,
    evaluate_project_control,
    improve1_project_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.construction_project_controls.runtime import (
    CONSTRUCTION_PROJECT_CONTROLS_ALLOWED_DATABASE_BACKENDS,
    construction_project_controls_build_release_evidence,
    construction_project_controls_runtime_capabilities,
    construction_project_controls_runtime_smoke,
)
from pyAppGen.pbcs.construction_project_controls.ui import construction_project_controls_ui_contract


def test_all_50_project_controls_execute_with_owned_tables_events_and_agent_surfaces():
    assert len(PROJECT_CONTROL_CAPABILITIES) == 50
    assert set(PROJECT_CONTROL_CAPABILITIES) == set(PROJECT_CONTROL_FUNCTIONS)

    for capability in PROJECT_CONTROL_CAPABILITIES:
        result = PROJECT_CONTROL_FUNCTIONS[capability](sample_payload_for(capability))
        assert result["ok"] is True, capability
        assert result["feature_number"] in range(1, 51)
        assert result["target_table"] == CAPABILITY_TABLES[capability]
        assert result["target_table"].startswith("construction_project_controls_")
        assert result["read_tables"] == ()
        assert result["event"]["event_contract"] == EVENT_CONTRACT
        assert result["event"]["topic"] == "pbc.construction_project_controls.events"
        assert result["stream_engine_picker_visible"] is False
        assert result["shared_table_access"] is False
        assert result["configuration"]["database_backends"] == ("postgresql", "mysql", "mariadb")
        assert result["agent_skill"].startswith("construction_project_controls_skills.")
        assert result["release_evidence"]["test_artifact"].endswith("tests/test_domain_behavior.py")


def test_project_controls_reject_missing_fields_and_foreign_table_access():
    first = PROJECT_CONTROL_CAPABILITIES[0]
    missing = evaluate_project_control(first, {})
    assert missing["ok"] is False
    assert set(missing["missing_required_fields"]) == set(REQUIRED_FIELDS[first])

    foreign = sample_payload_for(first)
    foreign["referenced_tables"] = ("project_schedule_table",)
    rejected = evaluate_project_control(first, foreign)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("project_schedule_table",)


def test_wbs_baseline_progress_schedule_and_change_controls_surface_review_findings():
    wbs = sample_payload_for(SLUG_BY_NUMBER[1])
    wbs["parent_wbs_code"] = wbs["wbs_code"]
    assert "wbs_cannot_parent_itself" in evaluate_project_control(SLUG_BY_NUMBER[1], wbs)["domain_findings"]

    baseline = sample_payload_for(SLUG_BY_NUMBER[2])
    baseline["approved_by"] = "draft"
    assert "baseline_freeze_requires_authorized_approval" in evaluate_project_control(SLUG_BY_NUMBER[2], baseline)["domain_findings"]

    progress = sample_payload_for(SLUG_BY_NUMBER[3])
    progress.update({"measurement_method": "spreadsheet_percent", "installed_quantity": 200})
    progress_review = evaluate_project_control(SLUG_BY_NUMBER[3], progress)
    assert "unsupported_progress_measurement_method" in progress_review["domain_findings"]
    assert "installed_quantity_exceeds_plan" in progress_review["domain_findings"]

    schedule = sample_payload_for(SLUG_BY_NUMBER[10])
    schedule["open_ends"] = 4
    assert "schedule_update_has_open_ended_logic" in evaluate_project_control(SLUG_BY_NUMBER[10], schedule)["domain_findings"]

    change = sample_payload_for(SLUG_BY_NUMBER[7])
    change.update({"approval_state": "pending", "cost_impact": 15000, "time_impact": 3})
    assert "change_impact_cannot_hit_forecast_before_approval" in evaluate_project_control(SLUG_BY_NUMBER[7], change)["domain_findings"]


def test_agent_document_policy_boundary_closeout_and_release_controls_require_governance():
    assistant = sample_payload_for(SLUG_BY_NUMBER[25])
    assistant["human_approval"] = False
    assistant_review = evaluate_project_control(SLUG_BY_NUMBER[25], assistant)
    assert "assistant_variance_narrative_requires_citations_and_approval" in assistant_review["domain_findings"]
    assert assistant_review["requires_human_confirmation"] is True

    document = sample_payload_for(SLUG_BY_NUMBER[39])
    document["confirmation_state"] = "draft"
    assert "document_instruction_requires_confirmed_preview" in evaluate_project_control(SLUG_BY_NUMBER[39], document)["domain_findings"]

    boundary = sample_payload_for(SLUG_BY_NUMBER[44])
    boundary["dependency_mode"] = "shared_table"
    assert "adjacent_system_boundary_must_use_api_event_or_projection" in evaluate_project_control(SLUG_BY_NUMBER[44], boundary)["domain_findings"]

    closeout = sample_payload_for(SLUG_BY_NUMBER[47])
    closeout["archive_blockers"] = ("open_change_event",)
    assert "closeout_archive_blocked_by_open_items" in evaluate_project_control(SLUG_BY_NUMBER[47], closeout)["domain_findings"]

    scorecard = sample_payload_for(SLUG_BY_NUMBER[50])
    scorecard["control_pass_rate"] = 0.71
    assert "go_live_scorecard_blocks_low_control_pass_rate" in evaluate_project_control(SLUG_BY_NUMBER[50], scorecard)["domain_findings"]


def test_runtime_ui_and_release_evidence_surface_project_control_contract():
    contract = improve1_project_control_contract()
    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == CONSTRUCTION_PROJECT_CONTROLS_ALLOWED_DATABASE_BACKENDS

    runtime = construction_project_controls_runtime_capabilities()
    smoke = construction_project_controls_runtime_smoke()
    release = construction_project_controls_build_release_evidence()
    ui = construction_project_controls_ui_contract()

    assert runtime["improve1_project_control"]["ok"] is True
    assert smoke["improve1_project_control"]["ok"] is True
    assert any(check["id"] == "improve1_project_control" and check["ok"] for check in smoke["checks"])
    assert release["generated_artifacts"]["improve1_project_control"]["capability_count"] == 50
    assert len(ui["project_control_panels"]) == 50
    assert ui["project_control_contract"]["ok"] is True
