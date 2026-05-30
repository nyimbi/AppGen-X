"""Domain behavior coverage for data_product_catalog improve1 controls."""

from __future__ import annotations

from pyAppGen.pbcs.data_product_catalog.blueprint import ALLOWED_DATABASE_BACKENDS, REQUIRED_EVENT_TOPIC
from pyAppGen.pbcs.data_product_catalog.data_product_control import (
    DATA_PRODUCT_CONTROL_CAPABILITIES,
    EVENT_CONTRACT,
    evaluate_data_product_control,
    improve1_data_product_control_contract,
    sample_payload_for,
)
from pyAppGen.pbcs.data_product_catalog.release_evidence import build_release_evidence
from pyAppGen.pbcs.data_product_catalog.runtime import data_product_catalog_runtime_capabilities, data_product_catalog_runtime_smoke
from pyAppGen.pbcs.data_product_catalog.ui import data_product_catalog_ui_contract


def test_all_50_data_product_controls_execute_with_owned_tables_events_and_agent_surfaces() -> None:
    contract = improve1_data_product_control_contract()

    assert contract["ok"] is True
    assert contract["capability_count"] == 50
    assert contract["database_backends"] == ALLOWED_DATABASE_BACKENDS
    assert contract["event_contract"] == EVENT_CONTRACT
    assert contract["event_topic"] == REQUIRED_EVENT_TOPIC
    assert contract["stream_engine_picker_visible"] is False

    allowed_tables = set(contract["owned_tables"])
    assert {item["feature_number"] for item in contract["capabilities"]} == set(range(1, 51))
    assert len(DATA_PRODUCT_CONTROL_CAPABILITIES) == 50
    for item in contract["capabilities"]:
        assert item["status"] == "implemented"
        assert item["read_tables"] == ()
        assert item["shared_table_access"] is False
        assert set(item["target_tables"]).issubset(allowed_tables)
        assert item["event"]["contract"] == EVENT_CONTRACT
        assert item["event"]["topic"] == REQUIRED_EVENT_TOPIC
        assert item["event"]["idempotency_key"]
        assert item["ui_surface"].startswith("DataProductCatalog")
        assert item["service_api"]
        assert item["agent_skill"].startswith("data_product_catalog_skills.")
        assert item["release_evidence"]["code_artifact_model"]
        assert item["release_evidence"]["ui_surface"]
        assert item["release_evidence"]["service_api"]
        assert item["release_evidence"]["test"]
        assert item["release_evidence"]["evidence"]


def test_data_product_controls_reject_missing_fields_and_foreign_table_references() -> None:
    missing = evaluate_data_product_control(1, {"target_consumers": "analysts"})
    assert missing["ok"] is False
    assert {"value_proposition", "business_outcomes", "source_domain", "lifecycle_state"}.issubset(set(missing["missing_required_fields"]))

    payload = sample_payload_for(1)
    payload["references"] = ("enterprise_customer_table",)
    rejected = evaluate_data_product_control(1, payload)
    assert rejected["ok"] is False
    assert rejected["invalid_references"] == ("enterprise_customer_table",)


def test_product_lifecycle_contract_access_and_classification_guardrails() -> None:
    lifecycle = sample_payload_for(2)
    lifecycle["target_state"] = lifecycle["current_state"]
    assert "transition" in evaluate_data_product_control(2, lifecycle)["domain_findings"][0]

    breaking = sample_payload_for(6)
    breaking["change_class"] = "breaking"
    breaking["required_approvals"] = ""
    assert "Breaking".lower() in evaluate_data_product_control(6, breaking)["domain_findings"][0].lower()

    access = sample_payload_for(14)
    access["legal_basis"] = ""
    assert "legal basis" in evaluate_data_product_control(14, access)["domain_findings"][0]

    recommendation = sample_payload_for(15)
    recommendation["human_approval"] = False
    assert "human approval" in evaluate_data_product_control(15, recommendation)["domain_findings"][0]

    classification = sample_payload_for(26)
    classification["reviewer_approval"] = ""
    assert "reviewer approval" in evaluate_data_product_control(26, classification)["domain_findings"][0]


def test_policy_federation_agent_release_and_workbench_guardrails() -> None:
    policy = sample_payload_for(37)
    policy["simulation"] = ""
    assert "simulation" in evaluate_data_product_control(37, policy)["domain_findings"][0]

    federation = sample_payload_for(38)
    federation["allowed_dependency_mode"] = "shared_table"
    assert "api, event, or projection" in evaluate_data_product_control(38, federation)["domain_findings"][0]

    agent = sample_payload_for(45)
    agent["human_confirmation"] = False
    assert "human confirmation" in evaluate_data_product_control(45, agent)["domain_findings"][0]

    release = sample_payload_for(47)
    release["handler_proofs"] = ""
    assert "release evidence" in evaluate_data_product_control(47, release)["domain_findings"][0]

    workbench = sample_payload_for(50)
    workbench["agent_panel"] = ""
    assert "workbench coverage" in evaluate_data_product_control(50, workbench)["domain_findings"][0]


def test_runtime_ui_and_release_evidence_surface_data_product_control_contract() -> None:
    runtime = data_product_catalog_runtime_capabilities()
    smoke = data_product_catalog_runtime_smoke()
    ui = data_product_catalog_ui_contract()
    release = build_release_evidence()

    assert runtime["ok"] is True
    assert "improve1_data_product_control_contract" in runtime["operations"]
    assert len(runtime["improve1_data_product_control_capabilities"]) == 50
    assert smoke["checks_by_id"]["improve1_data_product_control_contract"] is True
    assert smoke["data_product_control"]["ok"] is True
    assert ui["data_product_control_contract"]["ok"] is True
    assert len(ui["data_product_control_panels"]) == 50
    assert release["data_product_control"]["ok"] is True
