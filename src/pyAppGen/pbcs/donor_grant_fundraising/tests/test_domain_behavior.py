"""Domain behavior coverage for donor_grant_fundraising improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.donor_grant_fundraising.fundraising_control import (
    EVENT_CONTRACT,
    FUNDRAISING_CONTROL_CAPABILITIES,
    evaluate_fundraising_control,
    improve1_fundraising_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.donor_grant_fundraising.runtime import (
    DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS,
    DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC,
    donor_grant_fundraising_build_release_evidence,
    donor_grant_fundraising_runtime_capabilities,
    donor_grant_fundraising_runtime_smoke,
)
from pyAppGen.pbcs.donor_grant_fundraising.ui import donor_grant_fundraising_ui_contract


def test_all_50_fundraising_controls_execute_with_owned_tables_events_and_agent_surfaces() -> None:
    contract = improve1_fundraising_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == DONOR_GRANT_FUNDRAISING_ALLOWED_DATABASE_BACKENDS
    assert contract["event_contract"] == EVENT_CONTRACT
    assert contract["event_topic"] == DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False
    assert len(FUNDRAISING_CONTROL_CAPABILITIES) == 50

    allowed_tables = set(contract["owned_tables"])
    assert {item["feature_number"] for item in contract["capabilities"]} == set(range(1, 51))
    for item in contract["capabilities"]:
        assert item["status"] == "implemented"
        assert item["read_tables"] == ()
        assert item["shared_table_access"] is False
        assert set(item["target_tables"]).issubset(allowed_tables)
        assert item["event"]["contract"] == EVENT_CONTRACT
        assert item["event"]["topic"] == DONOR_GRANT_FUNDRAISING_REQUIRED_EVENT_TOPIC
        assert item["event"]["idempotency_key"]
        assert item["ui_surface"].startswith("DonorGrantFundraising")
        assert item["service_api"]
        assert item["agent_skill"].startswith("donor_grant_fundraising_skills.")
        assert item["release_evidence"]["code_artifact_model"]
        assert item["release_evidence"]["ui_surface"]
        assert item["release_evidence"]["service_api"]
        assert item["release_evidence"]["test"]
        assert item["release_evidence"]["evidence"]


def test_fundraising_controls_reject_missing_fields_and_foreign_table_references() -> None:
    missing = evaluate_fundraising_control(1, {"donor_type": "individual"})
    assert missing["ok"] is False
    assert {"relationship_stage", "preferred_channels", "funding_interests", "recognition_preference"}.issubset(set(missing["missing_required_fields"]))

    payload = sample_payload_for(1)
    payload["references"] = ("crm_contact_table",)
    rejected = evaluate_fundraising_control(1, payload)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("crm_contact_table",)


def test_profile_pipeline_proposal_document_and_assistant_mutation_guardrails() -> None:
    donor = sample_payload_for(1)
    donor["donor_type"] = ""
    assert "donor type" in evaluate_fundraising_control(1, donor)["domain_findings"][0]

    pipeline = sample_payload_for(2)
    pipeline["target_stage"] = pipeline["prospect_stage"]
    assert "prospect pipeline" in evaluate_fundraising_control(2, pipeline)["domain_findings"][0]

    proposal = sample_payload_for(8)
    proposal["final_signoff"] = ""
    assert "final signoff" in evaluate_fundraising_control(8, proposal)["domain_findings"][0]

    document = sample_payload_for(19)
    document["confidence"] = "low"
    document["human_confirmation"] = False
    assert "human confirmation" in evaluate_fundraising_control(19, document)["domain_findings"][0]

    mutation = sample_payload_for(22)
    mutation["policy_result"] = "deny"
    assert "policy" in evaluate_fundraising_control(22, mutation)["domain_findings"][0]


def test_policy_tenant_privacy_schema_and_release_scorecard_guardrails() -> None:
    sod = sample_payload_for(37)
    sod["reviewer_independence"] = False
    assert "self-approval" in evaluate_fundraising_control(37, sod)["domain_findings"][0]

    tenant = sample_payload_for(38)
    tenant["assistant_scope"] = "global"
    assert "tenant scoped" in evaluate_fundraising_control(38, tenant)["domain_findings"][0]

    consent = sample_payload_for(39)
    consent["anonymous_giving"] = True
    consent["recognition_limit"] = "public"
    assert "anonymous donor" in evaluate_fundraising_control(39, consent)["domain_findings"][0]

    extension = sample_payload_for(48)
    extension["target_table"] = "external_crm_contact"
    assert "owned fundraising table" in evaluate_fundraising_control(48, extension)["domain_findings"][0]

    scorecard = sample_payload_for(50)
    scorecard["blockers"] = ("unreviewed_control_failure",)
    assert "blockers" in evaluate_fundraising_control(50, scorecard)["domain_findings"][0]


def test_runtime_ui_and_release_evidence_surface_fundraising_control_contract() -> None:
    runtime = donor_grant_fundraising_runtime_capabilities()
    smoke = donor_grant_fundraising_runtime_smoke()
    ui = donor_grant_fundraising_ui_contract()
    release = donor_grant_fundraising_build_release_evidence()

    assert runtime["ok"] is True
    assert "improve1_fundraising_control_contract" in runtime["operations"]
    assert len(runtime["improve1_fundraising_control_capabilities"]) == 50
    assert smoke["checks_by_id"]["improve1_fundraising_control_contract"] is True
    assert smoke["fundraising_control"]["ok"] is True
    assert ui["fundraising_control_contract"]["ok"] is True
    assert len(ui["full_capability_surface"]["fundraising_control_panels"]) == 50
    assert release["generated_artifacts"]["fundraising_control"]["ok"] is True
