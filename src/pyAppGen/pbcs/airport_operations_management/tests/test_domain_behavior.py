"""Executable domain behavior tests for the airport_operations_management PBC."""

from __future__ import annotations

from pyAppGen.pbcs.airport_operations_management import implementation_contract
from pyAppGen.pbcs.airport_operations_management import runtime
from pyAppGen.pbcs.airport_operations_management import smoke_test
from pyAppGen.pbcs.airport_operations_management.agent import agent_skill_manifest
from pyAppGen.pbcs.airport_operations_management.agent import chatbot_interface_contract
from pyAppGen.pbcs.airport_operations_management.agent import composed_agent_contribution
from pyAppGen.pbcs.airport_operations_management.agent import datastore_crud_plan
from pyAppGen.pbcs.airport_operations_management.agent import document_instruction_plan
from pyAppGen.pbcs.airport_operations_management.agent import gate_assignment_decision_rationale
from pyAppGen.pbcs.airport_operations_management.capability_assurance import validate_table_stakes_capability_coverage
from pyAppGen.pbcs.airport_operations_management.compatibility import build_gate_assignment_compatibility_matrix
from pyAppGen.pbcs.airport_operations_management.compatibility import build_gate_assignment_decision
from pyAppGen.pbcs.airport_operations_management.compatibility import evaluate_stand_compatibility
from pyAppGen.pbcs.airport_operations_management.compatibility import explain_gate_assignment_decision
from pyAppGen.pbcs.airport_operations_management.domain_depth import DOMAIN_OPERATIONS
from pyAppGen.pbcs.airport_operations_management.domain_depth import domain_capability_surface_contract
from pyAppGen.pbcs.airport_operations_management.domain_depth import domain_depth_contract
from pyAppGen.pbcs.airport_operations_management.domain_depth import execute_domain_operation
from pyAppGen.pbcs.airport_operations_management.release_evidence import build_release_evidence
from pyAppGen.pbcs.airport_operations_management.release_evidence import release_readiness_manifest
from pyAppGen.pbcs.airport_operations_management.release_evidence import validate_release_evidence
from pyAppGen.pbcs.airport_operations_management.routes import api_route_contracts
from pyAppGen.pbcs.airport_operations_management.routes import dispatch_route
from pyAppGen.pbcs.airport_operations_management.routes import validate_api_route_contracts
from pyAppGen.pbcs.airport_operations_management.services import AirportOperationsManagementService
from pyAppGen.pbcs.airport_operations_management.services import service_operation_contracts
from pyAppGen.pbcs.airport_operations_management.services import service_operation_manifest
from pyAppGen.pbcs.airport_operations_management.standalone import assistant_document_plan
from pyAppGen.pbcs.airport_operations_management.standalone import baggage_contingency_plan
from pyAppGen.pbcs.airport_operations_management.standalone import build_turnaround_milestone_graph
from pyAppGen.pbcs.airport_operations_management.standalone import full_airport_operations_drill
from pyAppGen.pbcs.airport_operations_management.standalone import gate_change_impact_preview
from pyAppGen.pbcs.airport_operations_management.standalone import go_live_drill_scorecard
from pyAppGen.pbcs.airport_operations_management.standalone import overlap_guardrail
from pyAppGen.pbcs.airport_operations_management.standalone import passenger_flow_forecast
from pyAppGen.pbcs.airport_operations_management.standalone import plan_deicing_queue
from pyAppGen.pbcs.airport_operations_management.standalone import plan_remote_bussing
from pyAppGen.pbcs.airport_operations_management.standalone import reconcile_acdm_slot
from pyAppGen.pbcs.airport_operations_management.standalone import seeded_airport_scenario_library
from pyAppGen.pbcs.airport_operations_management.standalone import single_pbc_app_contract
from pyAppGen.pbcs.airport_operations_management.standalone import standalone_route_contracts
from pyAppGen.pbcs.airport_operations_management.standalone import standalone_smoke_test
from pyAppGen.pbcs.airport_operations_management.ui import airport_operations_management_render_workbench
from pyAppGen.pbcs.airport_operations_management.ui import airport_operations_management_ui_contract


TENANT = "tenant_alpha"
GATE_REQUEST = {
    "tenant": TENANT,
    "id": "ASSIGN-ALPHA",
    "flight_number": "AGX101",
    "aircraft_family": "widebody",
    "wingspan_code": "E",
    "operation_type": "international",
    "requires_hydrant_fuel": True,
    "requires_ground_power": True,
    "prefers_contact_stand": True,
}

NO_STAND_REQUEST = {
    "flight_number": "AGX999",
    "aircraft_family": "widebody",
    "wingspan_code": "F",
    "operation_type": "international",
    "requires_hydrant_fuel": True,
    "requires_ground_power": True,
    "requires_preconditioned_air": True,
    "requires_contact_stand": True,
}

POLICY_EVENT = {
    "event_type": "PolicyChanged",
    "event_id": "policy-alpha-001",
    "idempotency_key": "policy:alpha:001",
    "payload": {"tenant": TENANT, "policy_id": "airport-control", "scope": "stand_allocation"},
}


def _configured_state() -> dict:
    state = runtime.airport_operations_management_empty_state()
    state = runtime.airport_operations_management_configure_runtime(
        state,
        {"database_backend": "postgresql", "event_topic": runtime.AIRPORT_OPERATIONS_MANAGEMENT_REQUIRED_EVENT_TOPIC},
    )["state"]
    state = runtime.airport_operations_management_set_parameter(state, "workbench_limit", 50)["state"]
    state = runtime.airport_operations_management_register_rule(
        state,
        {"rule_id": "stand_compatibility", "tenant": TENANT, "scope": "gate_assignment", "status": "active"},
    )["state"]
    state = runtime.airport_operations_management_register_schema_extension(
        state,
        "gate_assignment",
        {"stand_score": "numeric", "rationale_hash": "text"},
    )["state"]
    return runtime.airport_operations_management_receive_event(state, POLICY_EVENT)["state"]


def _assigned_state() -> dict:
    state = _configured_state()
    return runtime.airport_operations_management_command_gate_assignment(state, GATE_REQUEST)["state"]


def test_airport_gate_stand_compatibility_and_operating_primitives_are_executable() -> None:
    contact_block = evaluate_stand_compatibility(NO_STAND_REQUEST, {"stand_code": "A1", "gate_code": "A1", "supported_aircraft_families": ("narrowbody",), "max_wingspan_code": "C", "international_capable": False, "hydrant_fuel": True, "ground_power": True, "preconditioned_air": False})
    matrix = build_gate_assignment_compatibility_matrix(GATE_REQUEST, occupied_stands=("B6",))
    decision = build_gate_assignment_decision(GATE_REQUEST)
    rejected = build_gate_assignment_decision(NO_STAND_REQUEST)
    explanation = explain_gate_assignment_decision(GATE_REQUEST)
    graph = build_turnaround_milestone_graph({"on_block": {"planned": "09:00"}, "fuel_complete": {"planned": "09:35", "depends_on": ("on_block",)}, "doors_closed": {"planned": "10:00", "depends_on": ("fuel_complete",), "predicted_delay_minutes": 7}})
    remote = plan_remote_bussing(passengers=180, buses_available=2, bus_capacity=90, lead_time_minutes=15)
    deicing = plan_deicing_queue(({"flight_number": "AGX201", "type_i_liters": 900, "type_iv_liters": 200},), pads=1, type_i_liters=1200, type_iv_liters=300)
    slot = reconcile_acdm_slot("10:00", "09:55", "10:10", "10:20")
    baggage = baggage_contingency_plan("R1", ({"belt": "R2", "available": True, "capacity_bags": 250},))
    flow = passenger_flow_forecast({"security": 420, "immigration": 260}, {"security": 500, "immigration": 220})
    impact = gate_change_impact_preview({"passengers": 210, "prm_travelers": 3, "bags": 180})
    scorecard = go_live_drill_scorecard({"stand_allocation": True})

    assert contact_block["decision"] == "blocked"
    assert "wingspan_code_exceeds_stand_limit" in contact_block["reason_codes"]
    assert matrix["ok"] is True and matrix["summary"]["blocked"] >= 1
    assert decision["ok"] is True and decision["recommended_option"]["stand_code"] == "B7"
    assert rejected["ok"] is False and rejected["reason"] == "no_compatible_stand"
    assert explanation["ok"] is True and explanation["recommendation"]["stand_code"] == "B7"
    assert graph["ok"] is True and graph["critical_path"]
    assert remote["ok"] is True and remote["required_buses"] == 2
    assert deicing["ok"] is True and deicing["queue"][0]["pad"] == 1
    assert slot["resync_required"] is True and slot["mismatch_reasons"] == ("tobt",)
    assert baggage["ok"] is True and baggage["selected_alternate"]["belt"] == "R2"
    assert flow["ok"] is False and flow["capacity_breaches"][0]["segment"] == "immigration"
    assert impact["requires_approval"] is True and impact["risk"] == "high"
    assert scorecard["ok"] is False and "gate_change_control" in scorecard["unresolved_gaps"]


def test_airport_runtime_services_routes_ui_and_agent_are_executable() -> None:
    state = _assigned_state()
    duplicate = runtime.airport_operations_management_receive_event(state, POLICY_EVENT)
    dead = runtime.airport_operations_management_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "event_id": "bad-event", "idempotency_key": "bad-event", "payload": {"tenant": TENANT}},
    )
    rejected = runtime.airport_operations_management_command_gate_assignment(dead["state"], {**NO_STAND_REQUEST, "tenant": TENANT, "id": "ASSIGN-BLOCKED"})
    query = runtime.airport_operations_management_query_workbench(rejected["state"], {"tenant": TENANT})
    workbench = runtime.airport_operations_management_build_workbench_view(TENANT)
    assessment = runtime.airport_operations_management_run_advanced_assessment(rejected["state"], {"tenant": TENANT})
    parser = runtime.airport_operations_management_parse_document_instruction("Gate change with deicing and baggage belt issue", "preview stand change")
    bad_extension = runtime.airport_operations_management_register_schema_extension(rejected["state"], "shared_gate_table", {"x": "jsonb"})
    schema = runtime.airport_operations_management_build_schema_contract()
    service_contract = runtime.airport_operations_management_build_service_contract()
    api_contract = runtime.airport_operations_management_build_api_contract()
    release = runtime.airport_operations_management_build_release_evidence()
    permissions = runtime.airport_operations_management_permissions_contract()
    boundary_ok = runtime.airport_operations_management_verify_owned_table_boundary(runtime.AIRPORT_OPERATIONS_MANAGEMENT_OWNED_TABLES[:2])
    boundary_bad = runtime.airport_operations_management_verify_owned_table_boundary(("foreign_table",))
    capabilities = runtime.airport_operations_management_runtime_capabilities()
    runtime_smoke = runtime.airport_operations_management_runtime_smoke()

    service = AirportOperationsManagementService()
    service_command = service.command_gate_assignment({"tenant": TENANT, "flight_number": "SVC101"})
    service_compatibility = service.evaluate_gate_assignment_compatibility(GATE_REQUEST)
    service_query = service.query_workbench({"tenant": TENANT})
    route_validation = validate_api_route_contracts()
    route_dispatch = dispatch_route("POST /gate-assignments", GATE_REQUEST)
    routes = api_route_contracts()
    ui_contract = airport_operations_management_ui_contract()
    rendered = airport_operations_management_render_workbench()
    skills = agent_skill_manifest()
    chatbot = chatbot_interface_contract()
    delegated_plan = document_instruction_plan("Runway closure and baggage belt issue", "generate disruption brief")
    assistant_plan = assistant_document_plan("Gate change with deicing and baggage belt issue", "preview stand change")
    rationale = gate_assignment_decision_rationale(GATE_REQUEST)
    crud_plan = datastore_crud_plan("create", "airport_operations_management_gate_assignment", {"id": "ASSIGN-ALPHA"})
    rejected_plan = datastore_crud_plan("update", "shared_gate_table", {})
    contribution = composed_agent_contribution()

    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert dead["ok"] is False and dead["dead_letter_table"] == "airport_operations_management_appgen_dead_letter_event"
    assert rejected["ok"] is False and rejected["record"]["status"] == "rejected"
    assert query["ok"] is True and len(query["records"]) == 2
    assert any(item["status"] == "rejected" for item in query["decision_queue"])
    assert workbench["ok"] is True and "compatibility_columns" in workbench["decision_support"]
    assert assessment["ok"] is True and "gate_stand_compatibility_evaluated" in assessment["explanations"]
    assert parser["ok"] is True and parser["requires_human_confirmation"] is True
    assert bad_extension["ok"] is False and bad_extension["reason"] == "unknown_owned_table"
    assert schema["ok"] is True and schema["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert service_contract["ok"] is True and "command_gate_assignment" in service_contract["command_methods"]
    assert api_contract["ok"] is True and api_contract["stream_engine_picker_visible"] is False
    assert release["ok"] is True and not release["blocking_gaps"]
    assert permissions["ok"] is True and "airport_operations_management.admin" in permissions["permissions"]
    assert boundary_ok["ok"] is True
    assert boundary_bad["ok"] is False and boundary_bad["invalid_references"] == ("foreign_table",)
    assert capabilities["ok"] is True and capabilities["event_contract"] == "AppGen-X"
    assert runtime_smoke["ok"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert service_command["ok"] is True and service_command["emits"] == ("AirportOperationsManagementCreated",)
    assert service_compatibility["ok"] is True and service_compatibility["compatibility_plan"]["ok"] is True
    assert service_query["ok"] is True and service_query["read_only"] is True
    assert route_validation["ok"] is True
    assert route_dispatch["ok"] is True
    assert "GET /airport-operations-management/app" in routes["routes"]
    assert ui_contract["ok"] is True and ui_contract["full_capability_surface"]["coverage"]["shared_table_access"] is False
    assert rendered["ok"] is True and rendered["standalone_app"]["ok"] is True
    assert skills["ok"] is True and len(skills["skills"]) >= 5
    assert chatbot["ok"] is True and chatbot["single_agent_contribution"] == "airport_operations_management_skills"
    assert delegated_plan["ok"] is True and delegated_plan["requires_human_confirmation"] is True
    assert assistant_plan["ok"] is True and assistant_plan["escalation_required"] is True
    assert rationale["ok"] is True and rationale["recommendation"]["stand_code"] == "B7"
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert rejected_plan["ok"] is False and rejected_plan["reason"] == "foreign_table_rejected"
    assert contribution["ok"] is True and contribution["standalone_app"]["pbc"] == "airport_operations_management"


def test_airport_standalone_release_evidence_and_package_contract_are_executable() -> None:
    seeds = seeded_airport_scenario_library()
    drill = full_airport_operations_drill()
    app = single_pbc_app_contract()
    routes = standalone_route_contracts()
    release_build = build_release_evidence()
    release_manifest = release_readiness_manifest()
    release_validation = validate_release_evidence()
    capability_validation = validate_table_stakes_capability_coverage()
    package_contract = implementation_contract()
    package_smoke = smoke_test()
    standalone_smoke = standalone_smoke_test()
    overlap_ok = overlap_guardrail(("aodb_flight_projection", "weather_projection") + runtime.AIRPORT_OPERATIONS_MANAGEMENT_OWNED_TABLES[:2])
    overlap_bad = overlap_guardrail(("aodb_flight",))
    domain = domain_depth_contract()
    surface = domain_capability_surface_contract()
    executed_operations = tuple(execute_domain_operation(operation, {"tenant": TENANT}) for operation in DOMAIN_OPERATIONS[:6])

    assert seeds["ok"] is True
    assert drill["ok"] is True and drill["blocking_gaps"] == ()
    assert app["ok"] is True
    assert app["forms"]["covered_improve1_items"] == tuple(range(1, 51))
    assert app["wizards"]["covered_improve1_items"] == tuple(range(1, 51))
    assert app["controls"]["covered_improve1_items"] == tuple(range(1, 51))
    assert routes["ok"] is True
    assert release_build["ok"] is True
    assert release_manifest["ok"] is True
    assert release_validation["ok"] is True
    assert capability_validation["ok"] is True
    assert package_contract["advanced_runtime"]["ok"] is True
    assert package_contract["single_pbc_app"]["ok"] is True
    assert package_smoke["ok"] is True
    assert standalone_smoke["ok"] is True
    assert overlap_ok["ok"] is True
    assert overlap_bad["ok"] is False and overlap_bad["forbidden_references"] == ("aodb_flight",)
    assert domain["ok"] is True and domain["event_contract"] == "AppGen-X"
    assert surface["ok"] is True and surface["coverage"]["shared_table_access"] is False
    assert all(result["ok"] is True for result in executed_operations)
    assert all(result["target_table"].startswith("airport_operations_management_") for result in executed_operations)
