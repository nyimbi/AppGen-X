"""Domain behavior coverage for cybersecurity_operations_center improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.cybersecurity_operations_center.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.cybersecurity_operations_center.runtime import (
    CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS,
    CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC,
    cybersecurity_operations_center_runtime_capabilities,
    cybersecurity_operations_center_runtime_smoke,
)
from pyAppGen.pbcs.cybersecurity_operations_center.soc_control import (
    EVENT_CONTRACT,
    SOC_CONTROL_CAPABILITIES,
    evaluate_soc_control,
    improve1_soc_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.cybersecurity_operations_center.ui import cybersecurity_operations_center_ui_contract


def test_all_50_soc_controls_execute_with_owned_tables_events_and_agent_surfaces() -> None:
    contract = improve1_soc_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == CYBERSECURITY_OPERATIONS_CENTER_ALLOWED_DATABASE_BACKENDS
    assert contract["event_contract"] == EVENT_CONTRACT
    assert contract["event_topic"] == CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    allowed_tables = set(contract["owned_tables"])
    seen = {item["feature_number"] for item in contract["capabilities"]}
    assert seen == set(range(1, 51))
    for item in contract["capabilities"]:
        assert item["status"] == "implemented"
        assert item["read_tables"] == ()
        assert item["shared_table_access"] is False
        assert set(item["target_tables"]).issubset(allowed_tables)
        assert item["event"]["contract"] == EVENT_CONTRACT
        assert item["event"]["topic"] == CYBERSECURITY_OPERATIONS_CENTER_REQUIRED_EVENT_TOPIC
        assert item["event"]["idempotency_key"]
        assert item["ui_surface"].startswith("CybersecurityOperationsCenter")
        assert item["service_api"]
        assert item["agent_skill"].startswith("cybersecurity_operations_center_skills.")
        assert item["release_evidence"]["code_artifact_model"]
        assert item["release_evidence"]["ui_surface"]
        assert item["release_evidence"]["service_api"]
        assert item["release_evidence"]["test"]
        assert item["release_evidence"]["evidence"]


def test_soc_controls_reject_missing_fields_and_foreign_table_references() -> None:
    capability = SOC_CONTROL_CAPABILITIES[0]
    missing = evaluate_soc_control(capability, {"current_state": "new"})
    assert missing["ok"] is False
    assert set(missing["missing_required_fields"]) >= {"next_state", "transition_reason", "actor"}

    payload = sample_payload_for(capability)
    payload["references"] = ("shared_security_event_table",)
    foreign = evaluate_soc_control(capability, payload)
    assert foreign["ok"] is False
    assert foreign["invalid_references"] == ("shared_security_event_table",)


def test_soc_lifecycle_dedup_containment_and_human_breakpoint_guardrails() -> None:
    no_transition = sample_payload_for(1)
    no_transition["next_state"] = no_transition["current_state"]
    assert "state transition" in evaluate_soc_control(1, no_transition)["domain_findings"][0]

    excessive_window = sample_payload_for(3)
    excessive_window["time_window_minutes"] = 10_000
    assert "deduplication window" in evaluate_soc_control(3, excessive_window)["domain_findings"][0]

    unapproved_containment = sample_payload_for(9)
    unapproved_containment["approval_path"] = ""
    assert "high-risk containment" in evaluate_soc_control(9, unapproved_containment)["domain_findings"][0]

    autonomous_playbook = sample_payload_for(14)
    autonomous_playbook["requires_human_confirmation"] = False
    assert "human confirmation" in evaluate_soc_control(14, autonomous_playbook)["domain_findings"][0]


def test_validation_only_assistant_tenant_parameter_and_closure_guardrails() -> None:
    persisted_validation = sample_payload_for(24)
    persisted_validation["validation_only"] = False
    assert "validation-only" in evaluate_soc_control(24, persisted_validation)["domain_findings"][0]

    direct_threat_intel_write = sample_payload_for(28)
    direct_threat_intel_write["human_confirmation_required"] = False
    assert "human confirmation" in evaluate_soc_control(28, direct_threat_intel_write)["domain_findings"][0]

    auto_playbook = sample_payload_for(36)
    auto_playbook["analyst_selection_required"] = False
    assert "auto-execute" in evaluate_soc_control(36, auto_playbook)["domain_findings"][0]

    cross_tenant_context = sample_payload_for(37)
    cross_tenant_context["assistant_scope"] = "global"
    assert "tenant-scoped" in evaluate_soc_control(37, cross_tenant_context)["domain_findings"][0]

    unsafe_parameter = sample_payload_for(47)
    unsafe_parameter["value"] = 99
    unsafe_parameter["maximum"] = 10
    assert "bounded safety range" in evaluate_soc_control(47, unsafe_parameter)["domain_findings"][0]

    premature_closure = sample_payload_for(50)
    premature_closure["evidence_complete"] = False
    assert "closure readiness" in evaluate_soc_control(50, premature_closure)["domain_findings"][0]


def test_runtime_ui_and_release_evidence_surface_soc_control_contract() -> None:
    runtime = cybersecurity_operations_center_runtime_capabilities()
    smoke = cybersecurity_operations_center_runtime_smoke()
    ui = cybersecurity_operations_center_ui_contract()
    release = release_readiness_manifest()

    assert runtime["ok"] is True
    assert "improve1_soc_control_contract" in runtime["operations"]
    assert len(runtime["improve1_soc_control_capabilities"]) == 50
    assert smoke["checks_by_id"]["improve1_soc_control_contract"] is True
    assert smoke["soc_control"]["ok"] is True
    assert ui["soc_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["soc_control_panels"]) == 50
    assert release["auxiliary_manifests"]["soc_control"]["ok"] is True
