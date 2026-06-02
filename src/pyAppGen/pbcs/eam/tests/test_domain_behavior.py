"""Domain behavior coverage for EAM improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.eam.eam_control import (
    EAM_ALLOWED_DATABASE_BACKENDS,
    EAM_CONTROL_CAPABILITIES,
    EAM_DECLARED_DEPENDENCIES,
    EAM_REQUIRED_EVENT_TOPIC,
    EVENT_CONTRACT,
    evaluate_eam_control,
    improve1_eam_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.eam.runtime import (
    EAM_ALLOWED_DATABASE_BACKENDS as RUNTIME_BACKENDS,
    EAM_REQUIRED_EVENT_TOPIC as RUNTIME_TOPIC,
    eam_build_release_evidence,
    eam_runtime_capabilities,
    eam_runtime_smoke,
)
from pyAppGen.pbcs.eam.ui import eam_ui_contract
from pyAppGen.pbcs.eam.release_evidence import build_release_evidence


def test_all_50_eam_controls_execute_with_owned_tables_events_and_agent_surfaces() -> None:
    contract = improve1_eam_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == EAM_ALLOWED_DATABASE_BACKENDS == RUNTIME_BACKENDS
    assert contract["event_contract"] == EVENT_CONTRACT
    assert contract["event_topic"] == EAM_REQUIRED_EVENT_TOPIC == RUNTIME_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    assert len(EAM_CONTROL_CAPABILITIES) == 50

    owned_tables = set(contract["owned_tables"])
    declared_dependencies = set(contract["declared_dependencies"])
    assert declared_dependencies == set(EAM_DECLARED_DEPENDENCIES)
    assert {item["feature_number"] for item in contract["capabilities"]} == set(range(1, 51))
    for item in contract["capabilities"]:
        assert item["status"] == "implemented"
        assert item["read_tables"] == ()
        assert item["shared_table_access"] is False
        assert set(item["target_tables"]).issubset(owned_tables)
        assert set(item["declared_dependencies"]).issubset(declared_dependencies)
        assert item["event"]["contract"] == EVENT_CONTRACT
        assert item["event"]["topic"] == EAM_REQUIRED_EVENT_TOPIC
        assert item["event"]["idempotency_key"]
        assert item["event"]["dead_letter_table"] == "maintenance_dead_letter"
        assert item["ui_surface"]
        assert item["service_api"]
        assert item["agent_skill"].startswith("eam_skills.")
        assert item["configuration"]["stream_engine_picker_visible"] is False
        assert item["configuration"]["database_backends"] == EAM_ALLOWED_DATABASE_BACKENDS
        assert item["retry_dead_letter_evidence"]["retry_policy"] == "bounded_retry_with_idempotency_key"
        assert item["release_evidence"]["code_artifact_model"]
        assert item["release_evidence"]["ui_surface"]
        assert item["release_evidence"]["service_api"]
        assert item["release_evidence"]["test"]
        assert item["release_evidence"]["evidence"]


def test_eam_controls_reject_missing_fields_and_undeclared_references() -> None:
    missing = evaluate_eam_control(1, {"equipment_class": "compressor"})
    assert missing["ok"] is False
    assert {"site", "location", "criticality", "meter_setup", "safety_requirements"}.issubset(set(missing["missing_required_fields"]))

    payload = sample_payload_for(37)
    payload["references"] = ("inventory_spares_projection", "inventory_source_table")
    rejected = evaluate_eam_control(37, payload)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("inventory_source_table",)


def test_asset_plan_condition_work_order_mobile_and_safety_guardrails() -> None:
    hierarchy = sample_payload_for(2)
    hierarchy["parent_equipment_id"] = hierarchy["equipment_id"]
    assert "own parent" in evaluate_eam_control(2, hierarchy)["domain_findings"][0]

    plan = sample_payload_for(7)
    plan["release_approval"] = ""
    assert "approval" in evaluate_eam_control(7, plan)["domain_findings"][0]

    reading = sample_payload_for(10)
    reading["confidence_score"] = "low"
    assert "low confidence" in evaluate_eam_control(10, reading)["domain_findings"][0]

    transition = sample_payload_for(12)
    transition["target_state"] = transition["current_state"]
    assert "new state" in evaluate_eam_control(12, transition)["domain_findings"][0]

    mobile = sample_payload_for(15)
    mobile["mobile_state"] = "completed"
    mobile["offline_queue"] = ("photo-1",)
    assert "unsynced" in evaluate_eam_control(15, mobile)["domain_findings"][0]

    permit = sample_payload_for(18)
    permit["isolations"] = ()
    assert "isolation" in evaluate_eam_control(18, permit)["domain_findings"][0]


def test_spares_projection_boundary_agent_document_control_and_proof_guardrails() -> None:
    spare = sample_payload_for(20)
    spare["reservation_id"] = ""
    assert "reservation" in evaluate_eam_control(20, spare)["domain_findings"][0]

    projection = sample_payload_for(34)
    projection["projection_freshness"] = "stale"
    assert "fresh" in evaluate_eam_control(34, projection)["domain_findings"][0]

    boundary = sample_payload_for(37)
    boundary["violations"] = ("production_work_order_table",)
    assert "owned-boundary" in evaluate_eam_control(37, boundary)["domain_findings"][0]

    agent = sample_payload_for(41)
    agent["human_confirmation"] = False
    assert "human confirmation" in evaluate_eam_control(41, agent)["domain_findings"][0]

    document = sample_payload_for(42)
    document["confidence"] = "low"
    document["human_confirmation"] = False
    assert "human confirmation" in evaluate_eam_control(42, document)["domain_findings"][0]

    control = sample_payload_for(48)
    control["control_result"] = "fail"
    assert "blocking exception" in evaluate_eam_control(48, control)["domain_findings"][0]

    readiness = sample_payload_for(49)
    readiness["readiness_score"] = 0.6
    assert "release threshold" in evaluate_eam_control(49, readiness)["domain_findings"][0]

    proof = sample_payload_for(50)
    proof["completion_event"] = "WorkOrderScheduled"
    assert "MaintenanceCompleted" in evaluate_eam_control(50, proof)["domain_findings"][0]


def test_runtime_ui_and_release_evidence_surface_eam_control_contract() -> None:
    runtime = eam_runtime_capabilities()
    smoke = eam_runtime_smoke()
    ui = eam_ui_contract()
    runtime_release = eam_build_release_evidence()
    package_release = build_release_evidence()

    assert runtime["ok"] is True
    assert "improve1_eam_control_contract" in runtime["operations"]
    assert len(runtime["improve1_eam_control_capabilities"]) == 50
    assert smoke["checks_by_id"]["improve1_eam_control_contract"] is True
    assert smoke["eam_control"]["ok"] is True
    assert ui["eam_control_contract"]["ok"] is True
    assert len(ui["binding_evidence"]["improve1_control_panels"]) == 50
    assert runtime_release["eam_control"]["ok"] is True
    assert package_release["eam_control"]["ok"] is True
