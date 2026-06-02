"""Executable domain behavior tests for the agri_supply_chain_traceability PBC."""

from __future__ import annotations

from .. import agent
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import smoke_test
from .. import standalone
from .. import ui
from .. import implementation_contract
from ..capability_assurance import validate_table_stakes_capability_coverage
from ..domain_depth import DOMAIN_OPERATIONS
from ..domain_depth import domain_capability_surface_contract
from ..domain_depth import domain_depth_contract
from ..domain_depth import execute_domain_operation
from ..release_gate import evaluate_release_readiness
from ..services import AgriSupplyChainTraceabilityService
from ..services import service_operation_contracts
from ..services import service_operation_manifest


TENANT = "tenant_alpha"
LOT_ID = "LOT-ALPHA"
SHIPMENT_ID = "SHIP-ALPHA"

CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_REQUIRED_EVENT_TOPIC,
    "workbench_limit": 50,
}

POLICY_EVENT = {
    "event_type": "PolicyChanged",
    "event_id": "policy-alpha-001",
    "idempotency_key": "policy:alpha:001",
    "payload": {"tenant": TENANT, "policy_id": "traceability-alpha", "status": "published"},
}


def _configured_state() -> dict:
    state = runtime.agri_supply_chain_traceability_empty_state()
    state = runtime.agri_supply_chain_traceability_configure_runtime(state, CONFIGURATION)["state"]
    state = runtime.agri_supply_chain_traceability_set_parameter(state, "quality_score_floor", 0.82)["state"]
    state = runtime.agri_supply_chain_traceability_set_parameter(state, "risk_threshold", 0.36)["state"]
    state = runtime.agri_supply_chain_traceability_register_rule(
        state,
        {
            "rule_id": "release_gate",
            "tenant": TENANT,
            "scope": "release_readiness",
            "status": "active",
            "block_on_cold_chain_breach": True,
            "block_on_seal_failure": True,
        },
    )["state"]
    state = runtime.agri_supply_chain_traceability_register_schema_extension(
        state,
        "farm_lot",
        {"regenerative_score": "numeric", "geo_boundary": "jsonb"},
    )["state"]
    return state


def _ready_state() -> dict:
    state = _configured_state()
    state = runtime.agri_supply_chain_traceability_receive_event(state, POLICY_EVENT)["state"]
    state = runtime.agri_supply_chain_traceability_command_farm_lot(
        state,
        {
            "id": LOT_ID,
            "tenant": TENANT,
            "site_id": "SITE-ALPHA",
            "commodity": "maize",
            "season": "2026-main",
            "status": "active",
        },
    )["state"]
    state = runtime.agri_supply_chain_traceability_record_input_batch(
        state,
        {
            "id": "INPUT-ALPHA",
            "tenant": TENANT,
            "farm_lot_id": LOT_ID,
            "supplier": "SoilWorks",
            "applied_at": "2026-04-02",
            "status": "recorded",
        },
    )["state"]
    state = runtime.agri_supply_chain_traceability_record_certification(
        state,
        {
            "id": "CERT-ALPHA",
            "tenant": TENANT,
            "farm_lot_id": LOT_ID,
            "covered_farm_lot_ids": (LOT_ID,),
            "covered_site_ids": ("SITE-ALPHA",),
            "covered_commodities": ("maize",),
            "valid_from": "2026-01-01",
            "valid_to": "2026-12-31",
            "status": "active",
        },
    )["state"]
    state = runtime.agri_supply_chain_traceability_record_storage_event(
        state,
        {
            "id": "STORE-ALPHA",
            "tenant": TENANT,
            "subject_ids": (SHIPMENT_ID,),
            "farm_lot_id": LOT_ID,
            "status": "released",
            "temperature_breach": False,
        },
    )["state"]
    state = runtime.agri_supply_chain_traceability_record_transport_leg(
        state,
        {
            "id": "LEG-ALPHA",
            "tenant": TENANT,
            "subject_ids": (SHIPMENT_ID,),
            "farm_lot_id": LOT_ID,
            "status": "in_transit",
            "seal_state": "intact",
            "receiving_confirmed": True,
        },
    )["state"]
    state = runtime.agri_supply_chain_traceability_record_provenance_proof(
        state,
        {
            "id": "PROOF-ALPHA",
            "tenant": TENANT,
            "subject_ids": (SHIPMENT_ID,),
            "source_farm_lot_ids": (LOT_ID,),
            "status": "verified",
        },
    )["state"]
    return state


def _candidate(**overrides: object) -> dict:
    candidate = {
        "tenant": TENANT,
        "candidate_id": SHIPMENT_ID,
        "farm_lot_id": LOT_ID,
        "commodity": "maize",
        "site_id": "SITE-ALPHA",
        "shipment_date": "2026-05-28",
    }
    candidate.update(overrides)
    return candidate


def test_agri_traceability_release_gate_approves_complete_lineage_and_blocks_exceptions() -> None:
    state = _ready_state()
    ready_verdict = evaluate_release_readiness(tuple(state["records"].values()), _candidate(), parameters={"risk_threshold": 0.36})
    approved = runtime.agri_supply_chain_traceability_assess_release_readiness(state, _candidate())
    blocked_storage_state = runtime.agri_supply_chain_traceability_record_storage_event(
        state,
        {
            "id": "STORE-BREACH",
            "tenant": TENANT,
            "subject_ids": (SHIPMENT_ID,),
            "farm_lot_id": LOT_ID,
            "status": "quarantined",
            "temperature_breach": True,
            "quarantine_state": "active",
        },
    )["state"]
    blocked_recall_state = runtime.agri_supply_chain_traceability_record_recall_link(
        blocked_storage_state,
        {
            "id": "RECALL-ALPHA",
            "tenant": TENANT,
            "subject_ids": (SHIPMENT_ID,),
            "farm_lot_id": LOT_ID,
            "recall_status": "active",
            "status": "active",
        },
    )["state"]
    blocked = runtime.agri_supply_chain_traceability_assess_release_readiness(blocked_recall_state, _candidate())

    assert ready_verdict["ok"] is True and ready_verdict["approved"] is True
    assert ready_verdict["passed_checks"] == (
        "farm_lot_active",
        "provenance_complete",
        "certification_covered",
        "storage_clear",
        "transport_clear",
        "no_active_recall",
        "quality_holds_cleared",
    )
    assert approved["ok"] is True
    assert approved["release_assessment"]["release_status"] == "approved"
    assert approved["state"]["outbox"][-1]["event_type"] == "AgriSupplyChainTraceabilityApproved"
    assert blocked["ok"] is True
    assert blocked["release_assessment"]["release_status"] == "blocked"
    assert {item["code"] for item in blocked["release_assessment"]["blockers"]} >= {"storage_exception_open", "active_recall"}
    assert blocked["state"]["outbox"][-1]["event_type"] == "AgriSupplyChainTraceabilityExceptionOpened"


def test_agri_runtime_services_routes_ui_and_agent_are_executable() -> None:
    state = _ready_state()
    duplicate = runtime.agri_supply_chain_traceability_receive_event(state, POLICY_EVENT)
    dead = runtime.agri_supply_chain_traceability_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "event_id": "bad-event", "idempotency_key": "bad-event", "payload": {"tenant": TENANT}},
    )
    query = runtime.agri_supply_chain_traceability_query_workbench(state, {"tenant": TENANT})
    workbench = runtime.agri_supply_chain_traceability_build_workbench_view(tenant=TENANT)
    assessment = runtime.agri_supply_chain_traceability_run_advanced_assessment(state, {"tenant": TENANT})
    parser = runtime.agri_supply_chain_traceability_parse_document_instruction("Organic certificate for LOT-ALPHA", "prepare release review")
    bad_extension = runtime.agri_supply_chain_traceability_register_schema_extension(state, "shared_traceability_table", {"x": "jsonb"})
    schema = runtime.agri_supply_chain_traceability_build_schema_contract()
    service_contract = runtime.agri_supply_chain_traceability_build_service_contract()
    api_contract = runtime.agri_supply_chain_traceability_build_api_contract()
    release = runtime.agri_supply_chain_traceability_build_release_evidence()
    permissions = runtime.agri_supply_chain_traceability_permissions_contract()
    boundary_ok = runtime.agri_supply_chain_traceability_verify_owned_table_boundary(runtime.AGRI_SUPPLY_CHAIN_TRACEABILITY_OWNED_TABLES[:2])
    boundary_bad = runtime.agri_supply_chain_traceability_verify_owned_table_boundary(("foreign_table",))
    capabilities = runtime.agri_supply_chain_traceability_runtime_capabilities()
    runtime_smoke = runtime.agri_supply_chain_traceability_runtime_smoke()

    service = AgriSupplyChainTraceabilityService()
    service_config = service.configure_runtime({"configuration": CONFIGURATION})
    service_lot = service.command_farm_lot({"farm_lot": {"tenant": TENANT, "id": "SERVICE-LOT", "site_id": "SITE-ALPHA", "commodity": "maize"}})
    service_query = service.query_workbench({"tenant": TENANT})
    route_validation = routes.validate_api_route_contracts()
    route_lot = routes.dispatch_route("POST", "/api/pbc/agri_supply_chain_traceability/farm-lots", {"farm_lot": {"tenant": TENANT, "id": "ROUTE-LOT"}})
    route_assistant = routes.dispatch_route("POST", "/api/pbc/agri_supply_chain_traceability/assistant/document-plans", {"document": "certificate", "instruction": "release shipment"})
    ui_contract = ui.agri_supply_chain_traceability_ui_contract()
    rendered = ui.agri_supply_chain_traceability_render_workbench(state, tenant=TENANT)
    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan("Cold chain storage document for LOT-ALPHA", "log storage exception")
    release_plan = agent.document_instruction_plan("Provenance packet for SHIP-ALPHA", "prepare release review")
    crud_plan = agent.datastore_crud_plan("create", "agri_supply_chain_traceability_farm_lot", {"id": LOT_ID})
    rejected_plan = agent.datastore_crud_plan("update", "shared_traceability_table", {})
    contribution = agent.composed_agent_contribution()

    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert dead["ok"] is False and dead["dead_letter_table"] == "agri_supply_chain_traceability_appgen_dead_letter_event"
    assert query["ok"] is True and len(query["records"]) == 6
    assert workbench["ok"] is True and workbench["release_gate_panel"]["action"] == "assess_release_readiness"
    assert assessment["ok"] is True and "agent_review_ready" in assessment["explanations"]
    assert parser["ok"] is True and parser["requires_human_confirmation"] is True
    assert bad_extension["ok"] is False and bad_extension["reason"] == "unknown_owned_table"
    assert schema["ok"] is True and schema["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert service_contract["ok"] is True and "assess_release_readiness" in service_contract["command_methods"]
    assert api_contract["ok"] is True and api_contract["stream_engine_picker_visible"] is False
    assert release["ok"] is True and not release["blocking_gaps"]
    assert permissions["ok"] is True and "agri_supply_chain_traceability.admin" in permissions["permissions"]
    assert boundary_ok["ok"] is True
    assert boundary_bad["ok"] is False and boundary_bad["invalid_references"] == ("foreign_table",)
    assert capabilities["ok"] is True and capabilities["event_contract"] == "AppGen-X"
    assert runtime_smoke["ok"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert service_config["ok"] is True
    assert service_lot["ok"] is True and service_lot["emits"] == ("AgriSupplyChainTraceabilityCreated",)
    assert service_query["ok"] is True and service_query["read_only"] is True
    assert route_validation["ok"] is True
    assert route_lot["ok"] is True
    assert route_assistant["ok"] is True
    assert ui_contract["ok"] is True and ui_contract["binding_evidence"]["shared_table_access"] is False
    assert rendered["ok"] is True and rendered["workbench"]["cards"][0]["value"] == 1
    assert rendered["release_gate_panel"]["release_status"] == "not_run"
    assert skills["ok"] is True and len(skills["skills"]) >= 5
    assert chatbot["ok"] is True and chatbot["single_agent_contribution"] == "agri_supply_chain_traceability_skills"
    assert document_plan["ok"] is True and document_plan["mutation_preview"]["operation"] == "record_storage_event"
    assert release_plan["ok"] is True and release_plan["release_gate_preview"]["operation"] == "assess_release_readiness"
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert rejected_plan["ok"] is False and rejected_plan["reason"] == "foreign_table_rejected"
    assert contribution["ok"] is True and "agri_supply_chain_traceability_crud" in contribution["dsl_tools"]


def test_agri_standalone_release_evidence_and_package_contract_are_executable() -> None:
    app = standalone.AgriSupplyChainTraceabilityStandaloneApp()
    bootstrapped = app.bootstrap(tenant=TENANT)
    loaded = app.load_demo_workspace(tenant=TENANT)
    rendered = app.render_workbench(tenant=TENANT)
    snapshot = app.release_snapshot()
    standalone_manifest = standalone.standalone_app_manifest()
    standalone_smoke = standalone.smoke_test()
    release_build = release_evidence.build_release_evidence()
    release_manifest = release_evidence.release_readiness_manifest()
    release_validation = release_evidence.validate_release_evidence()
    capability_validation = validate_table_stakes_capability_coverage()
    package_contract = implementation_contract()
    package_smoke = smoke_test()
    domain = domain_depth_contract()
    surface = domain_capability_surface_contract()
    executed_operations = tuple(execute_domain_operation(operation, {"tenant": TENANT}) for operation in DOMAIN_OPERATIONS[:6])

    assert bootstrapped["ok"] is True and bootstrapped["state"]["configuration"]["event_contract"] == "AppGen-X"
    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert rendered["workbench"]["cards"][0]["value"] >= 1
    assert rendered["release_gate_panel"]["release_status"] == "approved"
    assert rendered["shell"]["app_id"] == "agri_supply_chain_traceability_one_pbc_app"
    assert snapshot["ok"] is True
    assert standalone_manifest["ok"] is True and standalone_manifest["app"]["forms"]
    assert standalone_smoke["ok"] is True
    assert release_build["ok"] is True
    assert release_manifest["ok"] is True
    assert release_validation["ok"] is True
    assert capability_validation["ok"] is True
    assert package_contract["advanced_runtime"]["ok"] is True
    assert package_contract["standalone_app_contract"]["ok"] is True
    assert package_smoke["ok"] is True
    assert domain["ok"] is True and domain["event_contract"] == "AppGen-X"
    assert surface["ok"] is True and surface["coverage"]["shared_table_access"] is False
    assert all(result["ok"] is True for result in executed_operations)
    assert all(result["target_table"].startswith("agri_supply_chain_traceability_") for result in executed_operations)
