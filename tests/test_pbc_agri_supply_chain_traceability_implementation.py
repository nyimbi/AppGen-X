from pyAppGen.pbcs.agri_supply_chain_traceability import (
    agri_supply_chain_traceability_build_release_evidence,
    agri_supply_chain_traceability_assess_release_readiness,
    agri_supply_chain_traceability_command_farm_lot,
    agri_supply_chain_traceability_empty_state,
    agri_supply_chain_traceability_query_workbench,
    agri_supply_chain_traceability_record_certification,
    agri_supply_chain_traceability_record_provenance_proof,
    agri_supply_chain_traceability_record_recall_link,
    agri_supply_chain_traceability_record_storage_event,
    agri_supply_chain_traceability_record_transport_leg,
)
from pyAppGen.pbcs.agri_supply_chain_traceability.agent import agent_skill_manifest, chatbot_interface_contract, document_instruction_plan
from pyAppGen.pbcs.agri_supply_chain_traceability.services import service_operation_manifest
from pyAppGen.pbcs.agri_supply_chain_traceability.ui import agri_supply_chain_traceability_render_workbench, agri_supply_chain_traceability_ui_contract


def test_release_gate_approves_release_ready_candidate():
    state = agri_supply_chain_traceability_empty_state()
    farm_lot = agri_supply_chain_traceability_command_farm_lot(
        state,
        {
            "tenant": "co-op",
            "id": "LOT-001",
            "site_id": "SITE-1",
            "commodity": "maize",
        },
    )
    certification = agri_supply_chain_traceability_record_certification(
        farm_lot["state"],
        {
            "tenant": "co-op",
            "id": "CERT-001",
            "covered_farm_lot_ids": ("LOT-001",),
            "covered_site_ids": ("SITE-1",),
            "covered_commodities": ("maize",),
            "valid_from": "2026-01-01",
            "valid_to": "2026-12-31",
        },
    )
    storage = agri_supply_chain_traceability_record_storage_event(
        certification["state"],
        {
            "tenant": "co-op",
            "id": "STORE-001",
            "subject_ids": ("SHIP-001",),
            "farm_lot_id": "LOT-001",
            "status": "released",
        },
    )
    transport = agri_supply_chain_traceability_record_transport_leg(
        storage["state"],
        {
            "tenant": "co-op",
            "id": "LEG-001",
            "subject_ids": ("SHIP-001",),
            "farm_lot_id": "LOT-001",
            "seal_state": "intact",
            "receiving_confirmed": True,
            "status": "in_transit",
        },
    )
    provenance = agri_supply_chain_traceability_record_provenance_proof(
        transport["state"],
        {
            "tenant": "co-op",
            "id": "PROOF-001",
            "subject_ids": ("SHIP-001",),
            "source_farm_lot_ids": ("LOT-001",),
        },
    )

    assessment = agri_supply_chain_traceability_assess_release_readiness(
        provenance["state"],
        {
            "tenant": "co-op",
            "candidate_id": "SHIP-001",
            "farm_lot_id": "LOT-001",
            "commodity": "maize",
            "site_id": "SITE-1",
            "shipment_date": "2026-05-28",
        },
    )

    verdict = assessment["release_assessment"]
    assert verdict["approved"] is True
    assert verdict["release_status"] == "approved"
    assert verdict["blockers"] == ()
    assert set(verdict["passed_checks"]) >= {
        "farm_lot_active",
        "provenance_complete",
        "certification_covered",
        "storage_clear",
        "transport_clear",
        "no_active_recall",
        "quality_holds_cleared",
    }
    assert assessment["state"]["outbox"][-1]["event_type"] == "AgriSupplyChainTraceabilityApproved"

    workbench = agri_supply_chain_traceability_query_workbench(assessment["state"], {"tenant": "co-op"})
    assert len(workbench["release_assessments"]) == 1
    assert workbench["release_assessments"][0]["candidate"]["candidate_id"] == "SHIP-001"


def test_release_gate_blocks_certificate_exception_and_quality_holds():
    state = agri_supply_chain_traceability_empty_state()
    farm_lot = agri_supply_chain_traceability_command_farm_lot(
        state,
        {
            "tenant": "co-op",
            "id": "LOT-FAIL",
            "site_id": "SITE-9",
            "commodity": "avocado",
        },
    )
    certification = agri_supply_chain_traceability_record_certification(
        farm_lot["state"],
        {
            "tenant": "co-op",
            "id": "CERT-FAIL",
            "covered_farm_lot_ids": ("LOT-FAIL",),
            "covered_site_ids": ("SITE-9",),
            "covered_commodities": ("avocado",),
            "valid_from": "2025-01-01",
            "valid_to": "2025-12-31",
        },
    )
    storage = agri_supply_chain_traceability_record_storage_event(
        certification["state"],
        {
            "tenant": "co-op",
            "id": "STORE-FAIL",
            "subject_ids": ("SHIP-FAIL",),
            "farm_lot_id": "LOT-FAIL",
            "exception_open": True,
            "temperature_breach": True,
            "status": "exception",
        },
    )
    transport = agri_supply_chain_traceability_record_transport_leg(
        storage["state"],
        {
            "tenant": "co-op",
            "id": "LEG-FAIL",
            "subject_ids": ("SHIP-FAIL",),
            "farm_lot_id": "LOT-FAIL",
            "seal_state": "broken",
            "receiving_confirmed": False,
            "status": "blocked",
        },
    )
    recall = agri_supply_chain_traceability_record_recall_link(
        transport["state"],
        {
            "tenant": "co-op",
            "id": "RECALL-FAIL",
            "subject_ids": ("SHIP-FAIL",),
            "farm_lot_id": "LOT-FAIL",
            "recall_status": "active",
        },
    )

    assessment = agri_supply_chain_traceability_assess_release_readiness(
        recall["state"],
        {
            "tenant": "co-op",
            "candidate_id": "SHIP-FAIL",
            "farm_lot_id": "LOT-FAIL",
            "commodity": "avocado",
            "site_id": "SITE-9",
            "shipment_date": "2026-05-28",
            "pending_lab_results": ("LAB-22",),
            "pending_corrective_actions": ("CAPA-9",),
        },
    )

    verdict = assessment["release_assessment"]
    blocker_codes = {blocker["code"] for blocker in verdict["blockers"]}
    assert verdict["approved"] is False
    assert verdict["release_status"] == "blocked"
    assert {
        "provenance_missing",
        "certification_out_of_scope_or_expired",
        "storage_exception_open",
        "transport_exception_open",
        "active_recall",
        "quality_hold_open",
    }.issubset(blocker_codes)
    assert assessment["state"]["outbox"][-1]["event_type"] == "AgriSupplyChainTraceabilityExceptionOpened"


def test_release_gate_slice_is_exposed_in_service_ui_and_agent_contracts():
    service_manifest = service_operation_manifest()
    release_evidence = agri_supply_chain_traceability_build_release_evidence()
    ui_contract = agri_supply_chain_traceability_ui_contract()
    workbench = agri_supply_chain_traceability_render_workbench()
    agent_manifest = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    instruction = document_instruction_plan("release note", "Prepare shipment release evidence")

    assert "assess_release_readiness" in service_manifest["command_operations"]
    assert any(check["id"] == "release_gate_execution" and check["ok"] for check in release_evidence["checks"])
    assert release_evidence["generated_artifacts"]["release_gate"]["operation"] == "assess_release_readiness"
    assert "assess_release_readiness" in ui_contract["full_capability_surface"]["operation_actions"]
    assert workbench["release_gate_panel"]["action"] == "assess_release_readiness"
    assert any(skill["name"].endswith("assess_release_readiness") for skill in agent_manifest["skills"])
    assert "release_gate_preview" in chatbot["capabilities"]
    assert instruction["release_gate_preview"]["suggested"] is True
