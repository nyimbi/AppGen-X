"""Domain behavior coverage for defense_readiness_logistics improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.defense_readiness_logistics.config import ALLOWED_DATABASE_BACKENDS, REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.defense_readiness_logistics.defense_control import (
    DEFENSE_CONTROL_CAPABILITIES,
    EVENT_CONTRACT,
    evaluate_defense_control,
    improve1_defense_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.defense_readiness_logistics.runtime import (
    defense_readiness_logistics_build_release_evidence,
    defense_readiness_logistics_runtime_capabilities,
    defense_readiness_logistics_runtime_smoke,
)
from pyAppGen.pbcs.defense_readiness_logistics.ui import defense_readiness_logistics_ui_contract


def test_all_50_defense_controls_execute_with_owned_tables_events_and_agent_surfaces() -> None:
    contract = improve1_defense_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == ALLOWED_DATABASE_BACKENDS
    assert contract["event_contract"] == EVENT_CONTRACT
    assert contract["event_topic"] == REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    assert len(DEFENSE_CONTROL_CAPABILITIES) == 50

    allowed_tables = set(contract["owned_tables"])
    assert {item["feature_number"] for item in contract["capabilities"]} == set(range(1, 51))
    for item in contract["capabilities"]:
        assert item["status"] == "implemented"
        assert item["read_tables"] == ()
        assert item["shared_table_access"] is False
        assert set(item["target_tables"]).issubset(allowed_tables)
        assert item["event"]["contract"] == EVENT_CONTRACT
        assert item["event"]["topic"] == REQUIRED_EVENT_TOPIC
        assert item["event"]["idempotency_key"]
        assert item["ui_surface"].startswith("DefenseReadinessLogistics")
        assert item["service_api"]
        assert item["agent_skill"].startswith("defense_readiness_logistics_skills.")
        assert item["release_evidence"]["code_artifact_model"]
        assert item["release_evidence"]["ui_surface"]
        assert item["release_evidence"]["service_api"]
        assert item["release_evidence"]["test"]
        assert item["release_evidence"]["evidence"]


def test_defense_controls_reject_missing_fields_and_foreign_table_references() -> None:
    missing = evaluate_defense_control(1, {"current_state": "reported"})
    assert missing["ok"] is False
    assert {"target_state", "reason_code", "actor", "state_history"}.issubset(set(missing["missing_required_fields"]))

    payload = sample_payload_for(1)
    payload["references"] = ("hr_person_table",)
    rejected = evaluate_defense_control(1, payload)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("hr_person_table",)


def test_readiness_inspection_personnel_cannibalization_and_classified_guardrails() -> None:
    lifecycle = sample_payload_for(1)
    lifecycle["target_state"] = lifecycle["current_state"]
    assert "distinct state" in evaluate_defense_control(1, lifecycle)["domain_findings"][0]

    inspection = sample_payload_for(3)
    inspection["checklist_answers"] = ""
    assert "checklist evidence" in evaluate_defense_control(3, inspection)["domain_findings"][0]

    personnel = sample_payload_for(4)
    personnel["bounded_attributes"] = False
    assert "bounded" in evaluate_defense_control(4, personnel)["domain_findings"][0]

    cannibalization = sample_payload_for(7)
    cannibalization["approval"] = ""
    assert "approval evidence" in evaluate_defense_control(7, cannibalization)["domain_findings"][0]

    classified = sample_payload_for(22)
    classified["classification_redaction"] = False
    assert "redaction" in evaluate_defense_control(22, classified)["domain_findings"][0]


def test_qualification_assistant_release_and_after_action_guardrails() -> None:
    qualification = sample_payload_for(26)
    qualification["qualified_count"] = 1
    qualification["required_count"] = 3
    assert "qualified count" in evaluate_defense_control(26, qualification)["domain_findings"][0]

    movement = sample_payload_for(31)
    movement["human_confirmation"] = False
    assert "human confirmation" in evaluate_defense_control(31, movement)["domain_findings"][0]

    assistant = sample_payload_for(48)
    assistant["citations"] = ""
    assert "citations" in evaluate_defense_control(48, assistant)["domain_findings"][0]

    release_gate = sample_payload_for(49)
    release_gate["movement_released"] = ""
    assert "end-to-end release gate" in evaluate_defense_control(49, release_gate)["domain_findings"][0]

    after_action = sample_payload_for(50)
    after_action["approval_required"] = False
    assert "without approval" in evaluate_defense_control(50, after_action)["domain_findings"][0]


def test_runtime_ui_and_release_evidence_surface_defense_control_contract() -> None:
    runtime = defense_readiness_logistics_runtime_capabilities()
    smoke = defense_readiness_logistics_runtime_smoke()
    ui = defense_readiness_logistics_ui_contract()
    release = defense_readiness_logistics_build_release_evidence()

    assert runtime["ok"] is True
    assert "improve1_defense_control_contract" in runtime["operations"]
    assert len(runtime["improve1_defense_control_capabilities"]) == 50
    assert smoke["checks_by_id"]["improve1_defense_control_contract"] is True
    assert smoke["defense_control"]["ok"] is True
    assert ui["defense_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["defense_control_panels"]) == 50
    assert release["generated_artifacts"]["defense_control"]["ok"] is True
