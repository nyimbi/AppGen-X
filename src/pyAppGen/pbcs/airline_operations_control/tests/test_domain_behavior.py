"""Executable domain behavior tests for the airline_operations_control PBC."""

from __future__ import annotations

from pyAppGen.pbcs.airline_operations_control import implementation_contract
from pyAppGen.pbcs.airline_operations_control import smoke_test
from pyAppGen.pbcs.airline_operations_control import runtime
from pyAppGen.pbcs.airline_operations_control.agent import agent_skill_manifest
from pyAppGen.pbcs.airline_operations_control.agent import chatbot_interface_contract
from pyAppGen.pbcs.airline_operations_control.agent import composed_agent_contribution
from pyAppGen.pbcs.airline_operations_control.agent import datastore_crud_plan
from pyAppGen.pbcs.airline_operations_control.agent import document_instruction_plan
from pyAppGen.pbcs.airline_operations_control.capability_assurance import validate_table_stakes_capability_coverage
from pyAppGen.pbcs.airline_operations_control.domain_depth import DOMAIN_OPERATIONS
from pyAppGen.pbcs.airline_operations_control.domain_depth import domain_capability_surface_contract
from pyAppGen.pbcs.airline_operations_control.domain_depth import domain_depth_contract
from pyAppGen.pbcs.airline_operations_control.domain_depth import execute_domain_operation
from pyAppGen.pbcs.airline_operations_control.operations_planning import assess_turn_feasibility
from pyAppGen.pbcs.airline_operations_control.operations_planning import build_operational_workbench
from pyAppGen.pbcs.airline_operations_control.operations_planning import build_tail_rotation_graph
from pyAppGen.pbcs.airline_operations_control.operations_planning import normalize_flight_leg
from pyAppGen.pbcs.airline_operations_control.release_evidence import build_release_evidence
from pyAppGen.pbcs.airline_operations_control.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.airline_operations_control.release_evidence import validate_release_evidence
from pyAppGen.pbcs.airline_operations_control.routes import dispatch_route
from pyAppGen.pbcs.airline_operations_control.routes import validate_api_route_contracts
from pyAppGen.pbcs.airline_operations_control.services import AirlineOperationsControlService
from pyAppGen.pbcs.airline_operations_control.services import service_operation_contracts
from pyAppGen.pbcs.airline_operations_control.services import service_operation_manifest
from pyAppGen.pbcs.airline_operations_control.standalone import AirlineOperationsControlStandaloneApp
from pyAppGen.pbcs.airline_operations_control.standalone import smoke_test as standalone_smoke_test
from pyAppGen.pbcs.airline_operations_control.standalone import standalone_app_manifest
from pyAppGen.pbcs.airline_operations_control.ui import airline_operations_control_render_workbench
from pyAppGen.pbcs.airline_operations_control.ui import airline_operations_control_ui_contract


TENANT = "tenant_alpha"
TAIL = "5Y-ALP"

INBOUND_LEG = {
    "tenant": TENANT,
    "id": "ALP100",
    "flight_number": "AL100",
    "tail_number": TAIL,
    "origin": "NBO",
    "destination": "MBA",
    "scheduled_departure_at": "2026-05-30T06:00:00+00:00",
    "scheduled_arrival_at": "2026-05-30T07:00:00+00:00",
    "actual_off_block_at": "2026-05-30T06:18:00+00:00",
    "actual_on_block_at": "2026-05-30T07:24:00+00:00",
}

OUTBOUND_LEG = {
    "tenant": TENANT,
    "id": "ALP101",
    "flight_number": "AL101",
    "tail_number": TAIL,
    "origin": "MBA",
    "destination": "KIS",
    "scheduled_departure_at": "2026-05-30T07:45:00+00:00",
    "scheduled_arrival_at": "2026-05-30T08:40:00+00:00",
    "aircraft_type": "narrowbody",
    "crew_change_required": True,
    "catering_required": True,
    "station_type": "outstation",
}

DIVERTED_LEG = {
    "tenant": TENANT,
    "id": "ALP102",
    "flight_number": "AL102",
    "tail_number": "5Y-DIV",
    "origin": "NBO",
    "destination": "KGL",
    "scheduled_departure_at": "2026-05-30T09:00:00+00:00",
    "scheduled_arrival_at": "2026-05-30T11:00:00+00:00",
    "diversion_decided_at": "2026-05-30T10:20:00+00:00",
    "diverted_to": "EBB",
}

POLICY_EVENT = {
    "event_type": "PolicyChanged",
    "event_id": "policy-alpha-001",
    "idempotency_key": "policy:alpha:001",
    "payload": {"tenant": TENANT, "policy_id": "daily-occ", "scope": "network_control"},
}


def _configured_state() -> dict:
    state = runtime.airline_operations_control_empty_state()
    state = runtime.airline_operations_control_configure_runtime(state, runtime.AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION)["state"]
    for name, value in runtime.AIRLINE_OPERATIONS_CONTROL_DEFAULT_PARAMETERS.items():
        state = runtime.airline_operations_control_set_parameter(state, name, value)["state"]
    state = runtime.airline_operations_control_register_rule(
        state,
        {**runtime.AIRLINE_OPERATIONS_CONTROL_DEFAULT_RULE, "tenant": TENANT},
    )["state"]
    state = runtime.airline_operations_control_register_schema_extension(
        state,
        "flight_leg",
        {"network_risk_score": "numeric", "decision_fingerprint": "text"},
    )["state"]
    return runtime.airline_operations_control_receive_event(state, POLICY_EVENT)["state"]


def _operational_state() -> dict:
    state = _configured_state()
    state = runtime.airline_operations_control_command_flight_leg(state, INBOUND_LEG)["state"]
    state = runtime.airline_operations_control_command_flight_leg(state, OUTBOUND_LEG)["state"]
    state = runtime.airline_operations_control_record_aircraft_rotation(
        state,
        {
            "tenant": TENANT,
            "rotation_id": "ROT-ALPHA",
            "tail_number": TAIL,
            "operating_day": "2026-05-30",
            "leg_ids": ("ALP100", "ALP101"),
            "spare_tail_candidates": ("5Y-SP1", "5Y-SP2"),
        },
    )["state"]
    state = runtime.airline_operations_control_command_crew_pairing(
        state,
        {
            "tenant": TENANT,
            "crew_pairing_id": "CP-ALPHA",
            "remaining_duty_minutes": 52,
            "legality_state": "legal",
            "reserve_activation_required": True,
        },
    )["state"]
    state = runtime.airline_operations_control_command_disruption_event(
        state,
        {
            "tenant": TENANT,
            "disruption_event_id": "DIS-ALPHA",
            "event_type": "weather",
            "severity": "high",
            "affected_leg_ids": ("ALP101",),
            "source_lineage": ("metar", "dispatcher_note"),
        },
    )["state"]
    state = runtime.airline_operations_control_command_reaccommodation_plan(
        state,
        {
            "tenant": TENANT,
            "reaccommodation_plan_id": "REAC-ALPHA",
            "passenger_count": 34,
            "manual_review_required": True,
            "blocked_reason": "special_assistance_boundary",
        },
    )["state"]
    state = runtime.airline_operations_control_command_operations_decision(
        state,
        {
            "tenant": TENANT,
            "operations_decision_id": "DEC-ALPHA",
            "decision_type": "tail_swap",
            "selected_action": "swap_tail",
            "alternatives": ("delay", "cancel", "ferry"),
            "approval_state": "approved",
        },
    )["state"]
    state = runtime.airline_operations_control_record_delay_code(
        state,
        {"tenant": TENANT, "delay_code_id": "DLY-ALPHA", "primary_code": "93", "contributing_codes": ("11", "41")},
    )["state"]
    return runtime.airline_operations_control_plan_recovery_workflow(
        state,
        {
            "tenant": TENANT,
            "workflow_id": "WF-ALPHA",
            "focus_leg_ids": ("ALP101",),
            "linked_disruption_id": "DIS-ALPHA",
            "linked_rotation_id": "ROT-ALPHA",
            "selected_decision_id": "DEC-ALPHA",
        },
    )["state"]


def test_airline_timeline_turn_rotation_and_diversion_logic_are_executable() -> None:
    inbound = normalize_flight_leg(INBOUND_LEG)
    outbound = normalize_flight_leg(OUTBOUND_LEG)
    diverted = normalize_flight_leg(DIVERTED_LEG)
    turn = assess_turn_feasibility(inbound, outbound)
    graph = build_tail_rotation_graph((inbound, outbound), {"tenant": TENANT, "rotation_id": "ROT-ALPHA", "tail_number": TAIL, "leg_ids": ("ALP100", "ALP101")})
    workbench = build_operational_workbench((inbound, outbound, diverted), tenant=TENANT)

    assert inbound["authoritative_status"] == "arrived"
    assert inbound["delay_minutes"] == 18
    assert outbound["authoritative_status"] == "scheduled"
    assert diverted["branch"] == "diverted"
    assert diverted["completion_airport"] == "EBB"
    assert turn["ok"] is True
    assert turn["status"] == "impossible"
    assert turn["risk_level"] == "high"
    assert turn["buffer_minutes"] < 0
    assert "late_inbound" in turn["reasons"]
    assert graph["ok"] is True and graph["broken_turn_count"] == 1
    assert graph["recovery_outlook"] == "degrading"
    assert "ALP101" in graph["critical_leg_ids"]
    assert workbench["ok"] is True
    assert workbench["metrics"]["flight_leg_count"] == 3
    assert workbench["metrics"]["broken_turn_count"] == 1
    assert workbench["attention_queue"][0]["reason"] == "impossible"
    assert any(item["reason"] == "diverted" for item in workbench["attention_queue"])


def test_airline_runtime_services_routes_ui_and_agent_are_executable() -> None:
    state = _operational_state()
    duplicate = runtime.airline_operations_control_receive_event(state, POLICY_EVENT)
    dead = runtime.airline_operations_control_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "event_id": "bad-event", "idempotency_key": "bad-event", "payload": {"tenant": TENANT}},
    )
    query = runtime.airline_operations_control_query_workbench(dead["state"], {"tenant": TENANT})
    workbench = runtime.airline_operations_control_build_workbench_view(dead["state"], tenant=TENANT)
    assessment = runtime.airline_operations_control_run_advanced_assessment(dead["state"], {"tenant": TENANT})
    parser = runtime.airline_operations_control_parse_document_instruction("Crew disruption and tail swap for ALP101", "create recovery decision")
    bad_extension = runtime.airline_operations_control_register_schema_extension(dead["state"], "shared_flight_leg_table", {"x": "jsonb"})
    schema = runtime.airline_operations_control_build_schema_contract()
    service_contract = runtime.airline_operations_control_build_service_contract()
    api_contract = runtime.airline_operations_control_build_api_contract()
    release = runtime.airline_operations_control_build_release_evidence()
    permissions = runtime.airline_operations_control_permissions_contract()
    boundary_ok = runtime.airline_operations_control_verify_owned_table_boundary(runtime.AIRLINE_OPERATIONS_CONTROL_OWNED_TABLES[:2])
    boundary_bad = runtime.airline_operations_control_verify_owned_table_boundary(("foreign_table",))
    capabilities = runtime.airline_operations_control_runtime_capabilities()
    runtime_smoke = runtime.airline_operations_control_runtime_smoke()

    service = AirlineOperationsControlService()
    service_config = service.command_configure_runtime({"configuration": runtime.AIRLINE_OPERATIONS_CONTROL_DEFAULT_CONFIGURATION})
    service_leg = service.command_flight_leg({"flight_leg": {**INBOUND_LEG, "id": "SVC-IN", "tail_number": "5Y-SVC"}})
    service_query = service.query_workbench({"tenant": TENANT})
    route_validation = validate_api_route_contracts()
    route_leg = dispatch_route("POST", "/api/pbc/airline_operations_control/flight-legs", {"flight_leg": {**INBOUND_LEG, "id": "ROUTE-IN"}})
    route_assistant = dispatch_route("POST", "/api/pbc/airline_operations_control/assistant/document-plan", {"document": "tail swap note", "instruction": "create decision"})
    ui_contract = airline_operations_control_ui_contract()
    rendered = airline_operations_control_render_workbench(dead["state"], tenant=TENANT)
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    doc_plan = document_instruction_plan("Weather disruption and passenger reaccommodation for ALP101", "create recovery decision")
    crud_plan = datastore_crud_plan("create", "airline_operations_control_operations_decision", {"id": "DEC-ALPHA"})
    rejected_plan = datastore_crud_plan("update", "shared_flight_leg_table", {})
    contribution = composed_agent_contribution()

    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert dead["ok"] is False and dead["dead_letter_table"] == "airline_operations_control_appgen_dead_letter_event"
    assert query["ok"] is True and query["workbench"]["metrics"]["broken_turn_count"] == 1
    assert query["supplemental"]["operations_decision_count"] == 1
    assert workbench["ok"] is True and workbench["summary_cards"][1]["value"] == 1
    assert assessment["ok"] is True and "release_evidence_ready" in assessment["explanations"]
    assert parser["ok"] is True and "airline_operations_control_operations_decision" in parser["candidate_tables"]
    assert bad_extension["ok"] is False and bad_extension["reason"] == "unknown_owned_table"
    assert schema["ok"] is True and schema["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert service_contract["ok"] is True and "record_aircraft_rotation" in service_contract["command_methods"]
    assert api_contract["ok"] is True and api_contract["stream_engine_picker_visible"] is False
    assert release["ok"] is True and not release["blocking_gaps"]
    assert permissions["ok"] is True and "airline_operations_control.admin" in permissions["permissions"]
    assert boundary_ok["ok"] is True
    assert boundary_bad["ok"] is False and boundary_bad["invalid_references"] == ("foreign_table",)
    assert capabilities["ok"] is True and capabilities["event_contract"] == "AppGen-X"
    assert runtime_smoke["ok"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert service_config["ok"] is True
    assert service_leg["ok"] is True and service_leg["emits"] == ("AirlineOperationsControlCreated",)
    assert service_query["ok"] is True and service_query["operation_kind"] == "query"
    assert route_validation["ok"] is True
    assert route_leg["ok"] is True
    assert route_assistant["ok"] is True
    assert ui_contract["ok"] is True and ui_contract["binding_evidence"]["shared_table_access"] is False
    assert rendered["ok"] is True and rendered["cards"][0]["value"] == 2
    assert rendered["attention_queue"][0]["reason"] == "impossible"
    assert skills["ok"] is True and len(skills["skills"]) >= 4
    assert chatbot["ok"] is True and chatbot["single_agent_contribution"] == "airline_operations_control_skills"
    assert doc_plan["ok"] is True and "airline_operations_control_reaccommodation_plan" in doc_plan["candidate_tables"]
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert rejected_plan["ok"] is False and rejected_plan["reason"] == "foreign_table_rejected"
    assert contribution["ok"] is True and "airline_operations_control_rotation_recovery" in contribution["dsl_tools"]


def test_airline_standalone_release_evidence_and_package_contract_are_executable() -> None:
    app = AirlineOperationsControlStandaloneApp()
    bootstrapped = app.bootstrap(tenant=TENANT)
    loaded = app.load_demo_workspace(tenant=TENANT)
    rendered = app.render_workbench(tenant=TENANT)
    snapshot = app.release_snapshot()
    standalone_manifest_result = standalone_app_manifest()
    standalone_smoke = standalone_smoke_test()
    release_build = build_release_evidence()
    release_manifest = release_readiness_manifest()
    release_validation = validate_release_evidence()
    capability_validation = validate_table_stakes_capability_coverage()
    package_contract = implementation_contract()
    package_smoke = smoke_test()
    domain = domain_depth_contract()
    surface = domain_capability_surface_contract()
    executed_operations = tuple(execute_domain_operation(operation, {"tenant": TENANT}) for operation in DOMAIN_OPERATIONS[:6])

    assert bootstrapped["ok"] is True and bootstrapped["state"]["configuration"]["event_contract"] == "AppGen-X"
    assert loaded["ok"] is True
    assert rendered["ok"] is True
    assert rendered["cards"][0]["value"] >= 1
    assert rendered["workbench"]["workbench"]["metrics"]["broken_turn_count"] == 1
    assert rendered["shell"]["app_id"] == "airline_operations_control_one_pbc_app"
    assert snapshot["ok"] is True
    assert standalone_manifest_result["ok"] is True and standalone_manifest_result["app"]["forms"]
    assert standalone_smoke["ok"] is True
    assert release_build["ok"] is True
    assert release_manifest["ok"] is True
    assert release_validation["ok"] is True
    assert capability_validation["ok"] is True
    assert package_contract["advanced_runtime"]["ok"] is True
    assert package_contract["standalone_app"]["ok"] is True
    assert package_smoke["ok"] is True
    assert domain["ok"] is True and domain["event_contract"] == "AppGen-X"
    assert surface["ok"] is True and surface["coverage"]["shared_table_access"] is False
    assert all(result["ok"] is True for result in executed_operations)
    assert all(result["target_table"].startswith("airline_operations_control_") for result in executed_operations)
