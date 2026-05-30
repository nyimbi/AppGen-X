"""Domain behavior coverage for electronic_health_records_core improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.electronic_health_records_core.ehr_control import (
    EHR_ALLOWED_DATABASE_BACKENDS,
    EHR_CONTROL_CAPABILITIES,
    EHR_DECLARED_DEPENDENCIES,
    EHR_REQUIRED_EVENT_TOPIC,
    EVENT_CONTRACT,
    evaluate_ehr_control,
    improve1_ehr_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.electronic_health_records_core.runtime import (
    ELECTRONIC_HEALTH_RECORDS_CORE_ALLOWED_DATABASE_BACKENDS as RUNTIME_BACKENDS,
    ELECTRONIC_HEALTH_RECORDS_CORE_REQUIRED_EVENT_TOPIC as RUNTIME_TOPIC,
    electronic_health_records_core_build_release_evidence,
    electronic_health_records_core_runtime_capabilities,
    electronic_health_records_core_runtime_smoke,
)
from pyAppGen.pbcs.electronic_health_records_core.ui import electronic_health_records_core_ui_contract


def test_all_50_ehr_controls_execute_with_owned_tables_events_and_agent_surfaces() -> None:
    contract = improve1_ehr_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == EHR_ALLOWED_DATABASE_BACKENDS == RUNTIME_BACKENDS
    assert contract["event_contract"] == EVENT_CONTRACT
    assert contract["event_topic"] == EHR_REQUIRED_EVENT_TOPIC == RUNTIME_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    assert len(EHR_CONTROL_CAPABILITIES) == 50

    owned_tables = set(contract["owned_tables"])
    declared_dependencies = set(contract["declared_dependencies"])
    assert declared_dependencies == set(EHR_DECLARED_DEPENDENCIES)
    assert {item["feature_number"] for item in contract["capabilities"]} == set(range(1, 51))
    for item in contract["capabilities"]:
        assert item["status"] == "implemented"
        assert item["read_tables"] == ()
        assert item["shared_table_access"] is False
        assert set(item["target_tables"]).issubset(owned_tables)
        assert set(item["declared_dependencies"]).issubset(declared_dependencies)
        assert item["event"]["contract"] == EVENT_CONTRACT
        assert item["event"]["topic"] == EHR_REQUIRED_EVENT_TOPIC
        assert item["event"]["idempotency_key"]
        assert item["event"]["dead_letter_table"] == "electronic_health_records_core_appgen_dead_letter_event"
        assert item["ui_surface"]
        assert item["service_api"]
        assert item["agent_skill"].startswith("electronic_health_records_core_skills.")
        assert item["configuration"]["stream_engine_picker_visible"] is False
        assert item["configuration"]["database_backends"] == EHR_ALLOWED_DATABASE_BACKENDS
        assert item["retry_dead_letter_evidence"]["retry_policy"] == "bounded_retry_with_idempotency_key"
        assert item["release_evidence"]["code_artifact_model"]
        assert item["release_evidence"]["ui_surface"]
        assert item["release_evidence"]["service_api"]
        assert item["release_evidence"]["test"]
        assert item["release_evidence"]["evidence"]


def test_ehr_controls_reject_missing_fields_and_undeclared_references() -> None:
    missing = evaluate_ehr_control(1, {"identity_confidence": "low"})
    assert missing["ok"] is False
    assert {"duplicate_candidates", "review_decision", "source_lineage", "reversible_link"}.issubset(set(missing["missing_required_fields"]))

    payload = sample_payload_for(37)
    payload["references"] = ("patient_identity_projection", "pharmacy_claims_table")
    rejected = evaluate_ehr_control(37, payload)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("pharmacy_claims_table",)


def test_chart_order_observation_medication_access_and_agent_guardrails() -> None:
    merge = sample_payload_for(1)
    merge["merge_action"] = "auto_merge"
    assert "reviewed before merge" in evaluate_ehr_control(1, merge)["domain_findings"][0]

    order = sample_payload_for(5)
    order["to_state"] = order["from_state"]
    assert "move state" in evaluate_ehr_control(5, order)["domain_findings"][0]

    observation = sample_payload_for(7)
    observation["unit_compatible"] = False
    assert "unit" in evaluate_ehr_control(7, observation)["domain_findings"][0]

    critical = sample_payload_for(8)
    critical["acknowledgement_evidence"] = ""
    assert "acknowledgement" in evaluate_ehr_control(8, critical)["domain_findings"][0]

    medication = sample_payload_for(10)
    medication["reconciliation_complete"] = False
    assert "medication reconciliation" in evaluate_ehr_control(10, medication)["domain_findings"][0]

    access = sample_payload_for(17)
    access["consent_allowed"] = False
    access["break_glass_reason"] = ""
    assert "break-glass" in evaluate_ehr_control(17, access)["domain_findings"][0]

    agent = sample_payload_for(26)
    agent["citations"] = ()
    assert "citations" in evaluate_ehr_control(26, agent)["domain_findings"][0]

    command = sample_payload_for(27)
    command["confirmation"] = False
    assert "confirmation" in evaluate_ehr_control(27, command)["domain_findings"][0]


def test_privacy_downtime_boundary_integrity_model_and_composition_guardrails() -> None:
    extension = sample_payload_for(29)
    extension["target_table"] = "external_specialty_chart_table"
    assert "owned EHR table" in evaluate_ehr_control(29, extension)["domain_findings"][0]

    retention = sample_payload_for(31)
    retention["legal_hold"] = True
    retention["delete_requested"] = True
    assert "legal hold" in evaluate_ehr_control(31, retention)["domain_findings"][0]

    analytics = sample_payload_for(32)
    analytics["low_count_suppression"] = False
    assert "low-count" in evaluate_ehr_control(32, analytics)["domain_findings"][0]

    downtime = sample_payload_for(34)
    downtime["conflict_detected"] = True
    downtime["reviewer_confirmation"] = False
    assert "review" in evaluate_ehr_control(34, downtime)["domain_findings"][0]

    boundary = sample_payload_for(37)
    boundary["violations"] = ("care_coordination_note_table",)
    assert "boundary proof" in evaluate_ehr_control(37, boundary)["domain_findings"][0]

    integrity = sample_payload_for(46)
    integrity["hash_chain_valid"] = False
    assert "proof chain" in evaluate_ehr_control(46, integrity)["domain_findings"][0]

    model = sample_payload_for(47)
    model["approval_status"] = "expired"
    assert "approved model" in evaluate_ehr_control(47, model)["domain_findings"][0]

    dsl = sample_payload_for(50)
    dsl["stream_engine_picker_visible"] = True
    assert "stream-engine picker" in evaluate_ehr_control(50, dsl)["domain_findings"][0]


def test_runtime_ui_and_release_evidence_surface_ehr_control_contract() -> None:
    runtime = electronic_health_records_core_runtime_capabilities()
    smoke = electronic_health_records_core_runtime_smoke()
    ui = electronic_health_records_core_ui_contract()
    release = electronic_health_records_core_build_release_evidence()

    assert runtime["ok"] is True
    assert "improve1_ehr_control_contract" in runtime["operations"]
    assert len(runtime["improve1_ehr_control_capabilities"]) == 50
    assert smoke["checks_by_id"]["improve1_ehr_control_contract"] is True
    assert smoke["ehr_control"]["ok"] is True
    assert ui["ehr_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["ehr_control_panels"]) == 50
    assert release["generated_artifacts"]["ehr_control"]["ok"] is True
