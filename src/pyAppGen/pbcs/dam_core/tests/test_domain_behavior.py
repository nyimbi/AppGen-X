"""Domain behavior coverage for dam_core improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.dam_core.dam_control import (
    ALLOWED_DATABASE_BACKENDS,
    DAM_CONTROL_CAPABILITIES,
    EVENT_CONTRACT,
    REQUIRED_EVENT_TOPIC,
    evaluate_dam_control,
    improve1_dam_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.dam_core.release_evidence import build_release_evidence
from pyAppGen.pbcs.dam_core.runtime import (
    DAM_CORE_ALLOWED_DATABASE_BACKENDS,
    DAM_CORE_REQUIRED_EVENT_TOPIC,
    dam_core_runtime_capabilities,
    dam_core_runtime_smoke,
)
from pyAppGen.pbcs.dam_core.ui import dam_core_ui_contract


def test_all_50_dam_controls_execute_with_owned_tables_events_and_agent_surfaces() -> None:
    contract = improve1_dam_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == DAM_CORE_ALLOWED_DATABASE_BACKENDS == ALLOWED_DATABASE_BACKENDS
    assert contract["event_contract"] == EVENT_CONTRACT
    assert contract["event_topic"] == DAM_CORE_REQUIRED_EVENT_TOPIC == REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

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
        assert item["ui_surface"].startswith("DamCore")
        assert item["service_api"]
        assert item["agent_skill"].startswith("dam_core_skills.")
        assert item["release_evidence"]["code_artifact_model"]
        assert item["release_evidence"]["ui_surface"]
        assert item["release_evidence"]["service_api"]
        assert item["release_evidence"]["test"]
        assert item["release_evidence"]["evidence"]


def test_dam_controls_reject_missing_fields_and_foreign_table_references() -> None:
    missing = evaluate_dam_control(1, {"tenant": "tenant-a"})
    assert missing["ok"] is False
    assert {"filename", "mime_type", "storage_uri", "fingerprint", "rights_reference", "audit_hash"}.issubset(set(missing["missing_required_fields"]))

    payload = sample_payload_for(1)
    payload["references"] = ("pim_product_table",)
    rejected = evaluate_dam_control(1, payload)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("pim_product_table",)


def test_asset_intake_lifecycle_fingerprint_mime_and_rights_guardrails() -> None:
    intake = sample_payload_for(1)
    intake["fingerprint"] = ""
    assert "asset intake readiness" in evaluate_dam_control(1, intake)["domain_findings"][0]

    lifecycle = sample_payload_for(2)
    lifecycle["target_state"] = lifecycle["current_state"]
    assert "transition" in evaluate_dam_control(2, lifecycle)["domain_findings"][0]

    fingerprint = sample_payload_for(3)
    fingerprint["checksum_valid"] = False
    assert "checksum validation" in evaluate_dam_control(3, fingerprint)["domain_findings"][0]

    mime = sample_payload_for(5)
    mime["mime_type"] = "application/x-msdownload"
    assert "unsupported asset format" in evaluate_dam_control(5, mime)["domain_findings"][0]

    rights = sample_payload_for(12)
    rights["rights_safe"] = False
    assert "rights enforcement" in evaluate_dam_control(12, rights)["domain_findings"][0]


def test_boundary_schema_model_agent_and_publication_proof_guardrails() -> None:
    recommendation = sample_payload_for(23)
    recommendation["required_approval"] = False
    assert "requires approval" in evaluate_dam_control(23, recommendation)["domain_findings"][0]

    boundary = sample_payload_for(37)
    boundary["foreign_table_access"] = True
    assert "foreign table access" in evaluate_dam_control(37, boundary)["domain_findings"][0]

    extension = sample_payload_for(38)
    extension["target_table"] = "product_master"
    assert "owned DAM table" in evaluate_dam_control(38, extension)["domain_findings"][0]

    model = sample_payload_for(39)
    model["validation_metrics"] = {}
    assert "validation metrics" in evaluate_dam_control(39, model)["domain_findings"][0]

    plan = sample_payload_for(48)
    plan["human_confirmation"] = False
    assert "human confirmation" in evaluate_dam_control(48, plan)["domain_findings"][0]

    proof = sample_payload_for(50)
    proof["rendition_ready"] = ""
    assert "publication proof" in evaluate_dam_control(50, proof)["domain_findings"][0]


def test_runtime_ui_and_release_evidence_surface_dam_control_contract() -> None:
    runtime = dam_core_runtime_capabilities()
    smoke = dam_core_runtime_smoke()
    ui = dam_core_ui_contract()
    release = build_release_evidence()

    assert runtime["ok"] is True
    assert "improve1_dam_control_contract" in runtime["operations"]
    assert len(runtime["improve1_dam_control_capabilities"]) == 50
    assert smoke["checks_by_id"]["improve1_dam_control_contract"] is True
    assert smoke["dam_control"]["ok"] is True
    assert ui["dam_control_contract"]["ok"] is True
    assert len(ui["dam_control_panels"]) == 50
    assert release["dam_control"]["ok"] is True
