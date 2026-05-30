"""Executable domain behavior tests for the agriculture_farm_operations PBC."""

from __future__ import annotations

from .. import agent
from .. import implementation_contract
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import smoke_test
from .. import standalone
from .. import ui
from ..capability_assurance import validate_table_stakes_capability_coverage
from ..crop_planning import build_crop_plan_workbench_summary
from ..crop_planning import classify_planting_window
from ..crop_planning import detect_crop_plan_conflicts
from ..crop_planning import evaluate_crop_plan_submission
from ..crop_planning import evaluate_preplant_readiness
from ..domain_depth import DOMAIN_OPERATIONS
from ..domain_depth import domain_capability_surface_contract
from ..domain_depth import domain_depth_contract
from ..domain_depth import execute_domain_operation
from ..services import AgricultureFarmOperationsService
from ..services import service_operation_contracts
from ..services import service_operation_manifest


TENANT = "tenant_alpha"
FIELD_ID = "FIELD-ALPHA"

CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.AGRICULTURE_FARM_OPERATIONS_REQUIRED_EVENT_TOPIC,
    "default_region": "east-africa",
    "calendar_profile": "seasonal",
    "workbench_limit": 100,
}

POLICY_EVENT = {
    "event_type": "PolicyChanged",
    "event_id": "policy-alpha-001",
    "idempotency_key": "policy:alpha:001",
    "payload": {"tenant": TENANT, "policy": "crop-plan-release"},
}

READY_CROP_PLAN = {
    "tenant": TENANT,
    "field_id": FIELD_ID,
    "management_zone": "north-block",
    "crop": "maize",
    "season": "long_rains",
    "market_year": 2026,
    "planting_date": "2026-04-24",
    "planned_start": "2026-04-24",
    "planned_end": "2026-09-15",
    "planting_window": {
        "start": "2026-04-10",
        "optimal_start": "2026-04-20",
        "optimal_end": "2026-05-05",
        "latest": "2026-05-15",
        "minimum_soil_temperature_c": 12,
        "maximum_frost_risk": 0.2,
        "minimum_rainfall_outlook_mm": 20,
        "requires_irrigation_ready": True,
    },
    "conditions": {
        "soil_temperature_c": 15,
        "frost_risk": 0.05,
        "rainfall_outlook_mm": 26,
    },
    "readiness": {
        "soil_fit": True,
        "fertility_ready": True,
        "equipment_ready": True,
        "crew_assigned": True,
        "irrigation_ready": True,
    },
}

BLOCKED_CROP_PLAN = {
    **READY_CROP_PLAN,
    "plan_id": "FIELD-ALPHA-BLOCKED",
    "planting_date": "2026-05-18",
    "conditions": {
        "soil_temperature_c": 8,
        "frost_risk": 0.35,
        "rainfall_outlook_mm": 4,
    },
    "readiness": {
        "soil_fit": True,
        "fertility_ready": False,
        "equipment_ready": True,
        "crew_assigned": False,
        "irrigation_ready": False,
    },
}


def _configured_state() -> dict:
    state = runtime.agriculture_farm_operations_empty_state()
    state = runtime.agriculture_farm_operations_configure_runtime(state, CONFIGURATION)["state"]
    state = runtime.agriculture_farm_operations_set_parameter(state, "workbench_limit", 100)["state"]
    state = runtime.agriculture_farm_operations_set_parameter(state, "window_alert_threshold_days", 3)["state"]
    state = runtime.agriculture_farm_operations_register_rule(
        state,
        {
            "rule_id": "crop_plan_release",
            "tenant": TENANT,
            "scope": "crop_plan",
            "status": "active",
            "required_readiness_checks": ("soil_fit", "fertility_ready", "equipment_ready", "crew_assigned"),
        },
    )["state"]
    state = runtime.agriculture_farm_operations_register_schema_extension(
        state,
        "crop_plan",
        {"agronomy_score": "numeric", "prescription_version": "text"},
    )["state"]
    return state


def _field_state() -> dict:
    state = _configured_state()
    state = runtime.agriculture_farm_operations_receive_event(state, POLICY_EVENT)["state"]
    return runtime.agriculture_farm_operations_command_field(
        state,
        {
            "tenant": TENANT,
            "field_id": FIELD_ID,
            "code": "FIELD-A",
            "name": "Alpha North Field",
            "region": "east-africa",
            "acreage": 180,
            "management_zones": ("north-block", "south-block"),
        },
    )["state"]


def _planned_state() -> dict:
    state = _field_state()
    return runtime.agriculture_farm_operations_record_crop_plan(state, READY_CROP_PLAN)["state"]


def test_crop_plan_window_readiness_conflict_and_exception_logic_are_executable() -> None:
    window = classify_planting_window(READY_CROP_PLAN)
    readiness = evaluate_preplant_readiness(READY_CROP_PLAN, window)
    accepted = evaluate_crop_plan_submission((), READY_CROP_PLAN)
    blocked = evaluate_crop_plan_submission((accepted["plan"],), BLOCKED_CROP_PLAN)
    conflicts = detect_crop_plan_conflicts((accepted["plan"],), {**READY_CROP_PLAN, "plan_id": "FIELD-ALPHA-SECOND"})
    summary = build_crop_plan_workbench_summary((accepted["plan"],), (blocked["exception"],))

    assert window["status"] == "optimal"
    assert window["blocking_codes"] == ()
    assert readiness["status"] == "ready"
    assert accepted["ok"] is True and accepted["accepted"] is True
    assert accepted["plan"]["status"] == "planned"
    assert accepted["emitted_event"] == "AgricultureFarmOperationsCreated"
    assert blocked["ok"] is False and blocked["accepted"] is False
    assert blocked["emitted_event"] == "AgricultureFarmOperationsExceptionOpened"
    assert "overlapping_active_crop_plan" in blocked["exception"]["reason_codes"]
    assert {"missing_fertility_ready", "missing_crew_assigned", "soil_temperature_below_threshold", "frost_risk_above_threshold", "dry_outlook_without_irrigation"}.issubset(set(blocked["exception"]["reason_codes"]))
    assert conflicts and conflicts[0]["reason_code"] == "overlapping_active_crop_plan"
    assert summary["accepted_count"] == 1
    assert summary["blocked_count"] == 1


def test_farm_runtime_services_routes_ui_and_agent_are_executable() -> None:
    state = _planned_state()
    duplicate = runtime.agriculture_farm_operations_receive_event(state, POLICY_EVENT)
    dead = runtime.agriculture_farm_operations_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "event_id": "bad-event", "idempotency_key": "bad-event", "payload": {"tenant": TENANT}},
    )
    blocked = runtime.agriculture_farm_operations_record_crop_plan(dead["state"], BLOCKED_CROP_PLAN)
    query = runtime.agriculture_farm_operations_query_workbench(blocked["state"], {"tenant": TENANT})
    workbench = runtime.agriculture_farm_operations_build_workbench_view(blocked["state"], tenant=TENANT)
    assessment = runtime.agriculture_farm_operations_run_advanced_assessment(blocked["state"], {"tenant": TENANT})
    parser = runtime.agriculture_farm_operations_parse_document_instruction("Scout note for FIELD-ALPHA maize", "create crop plan", {"tenant": TENANT, "field_id": FIELD_ID, "crop": "maize"})
    bad_parameter = runtime.agriculture_farm_operations_set_parameter(blocked["state"], "stream_engine", "picker")
    bad_extension = runtime.agriculture_farm_operations_register_schema_extension(blocked["state"], "shared_crop_plan_table", {"x": "jsonb"})
    schema = runtime.agriculture_farm_operations_build_schema_contract()
    service_contract = runtime.agriculture_farm_operations_build_service_contract()
    api_contract = runtime.agriculture_farm_operations_build_api_contract()
    release = runtime.agriculture_farm_operations_build_release_evidence()
    permissions = runtime.agriculture_farm_operations_permissions_contract()
    boundary_ok = runtime.agriculture_farm_operations_verify_owned_table_boundary(runtime.AGRICULTURE_FARM_OPERATIONS_OWNED_TABLES[:2])
    boundary_bad = runtime.agriculture_farm_operations_verify_owned_table_boundary(("foreign_table",))
    capabilities = runtime.agriculture_farm_operations_runtime_capabilities()
    runtime_smoke = runtime.agriculture_farm_operations_runtime_smoke()

    service = AgricultureFarmOperationsService()
    service_config = service.configure_runtime({"configuration": CONFIGURATION})
    service_field = service.command_field({"field": {"tenant": TENANT, "field_id": "SERVICE-FIELD", "name": "Service Field"}})
    service_plan = service.record_crop_plan({"crop_plan": {**READY_CROP_PLAN, "field_id": "SERVICE-FIELD", "plan_id": "SERVICE-PLAN"}})
    service_query = service.query_workbench({"tenant": TENANT})
    route_validation = routes.validate_api_route_contracts()
    route_field = routes.dispatch_route("POST", "/api/pbc/agriculture_farm_operations/fields", {"field": {"tenant": TENANT, "field_id": "ROUTE-FIELD"}})
    route_assistant = routes.dispatch_route("POST", "/api/pbc/agriculture_farm_operations/assistant/document-plan", {"document": "field note", "instruction": "create crop plan", "context": {"tenant": TENANT, "field_id": FIELD_ID}})
    ui_contract = ui.agriculture_farm_operations_ui_contract()
    rendered = ui.agriculture_farm_operations_render_workbench(blocked["state"], tenant=TENANT)
    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan("Scout note: plant maize in north-block", "create crop plan", {"tenant": TENANT, "field_id": FIELD_ID, "crop": "maize"})
    crud_plan = agent.datastore_crud_plan("create", "agriculture_farm_operations_crop_plan", {"field_id": FIELD_ID})
    rejected_plan = agent.datastore_crud_plan("update", "shared_crop_plan_table", {})
    contribution = agent.composed_agent_contribution()

    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert dead["ok"] is False and dead["dead_letter_table"] == "agriculture_farm_operations_appgen_dead_letter_event"
    assert blocked["ok"] is False
    assert blocked["assistant_plan"]["status"] == "blocked"
    assert blocked["workflow"]["status"] == "blocked"
    assert query["ok"] is True
    assert query["crop_plan_summary"]["accepted_count"] == 1
    assert query["crop_plan_summary"]["blocked_count"] == 1
    assert workbench["ok"] is True and "blocked_operations_inbox" in workbench["widgets"]
    assert assessment["ok"] is True and "assistant_review_ready" in assessment["explanations"]
    assert parser["ok"] is True and parser["requires_human_confirmation"] is True
    assert bad_parameter["ok"] is False and bad_parameter["reason"] == "unknown_parameter"
    assert bad_extension["ok"] is False and bad_extension["reason"] == "unknown_owned_table"
    assert schema["ok"] is True and schema["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert service_contract["ok"] is True and "record_crop_plan" in service_contract["command_methods"]
    assert api_contract["ok"] is True and api_contract["stream_engine_picker_visible"] is False
    assert release["ok"] is True and not release["blocking_gaps"]
    assert permissions["ok"] is True and "agriculture_farm_operations.admin" in permissions["permissions"]
    assert boundary_ok["ok"] is True
    assert boundary_bad["ok"] is False and boundary_bad["invalid_references"] == ("foreign_table",)
    assert capabilities["ok"] is True and capabilities["event_contract"] == "AppGen-X"
    assert runtime_smoke["ok"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert service_config["ok"] is True
    assert service_field["ok"] is True
    assert service_plan["ok"] is True and "AgricultureFarmOperationsCreated" in service_plan["emits"]
    assert service_query["ok"] is True and service_query["operation_kind"] == "query"
    assert route_validation["ok"] is True
    assert route_field["ok"] is True
    assert route_assistant["ok"] is True
    assert ui_contract["ok"] is True and ui_contract["binding_evidence"]["shared_table_access"] is False
    assert rendered["ok"] is True and rendered["cards"][0]["value"] == 1
    assert rendered["cards"][2]["value"] == 1
    assert skills["ok"] is True and len(skills["skills"]) >= 3
    assert chatbot["ok"] is True and chatbot["single_agent_contribution"] == "agriculture_farm_operations_skills"
    assert document_plan["ok"] is True and document_plan["crud_preview"]["target_table"] == "agriculture_farm_operations_crop_plan"
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert rejected_plan["ok"] is False and rejected_plan["reason"] == "foreign_table_rejected"
    assert contribution["ok"] is True and "agriculture_farm_operations_crud" in contribution["dsl_tools"]


def test_farm_standalone_release_evidence_and_package_contract_are_executable() -> None:
    app = standalone.AgricultureFarmOperationsStandaloneApp()
    bootstrapped = app.bootstrap(tenant=TENANT)
    loaded = app.load_demo_workspace(tenant=TENANT)
    rendered = app.render_workbench(tenant=TENANT)
    assistant = app.assistant_workspace(tenant=TENANT)
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
    assert rendered["shell"]["app_id"] == "agriculture_farm_operations_one_pbc_app"
    assert assistant["ok"] is True and assistant["document_plan"]["requires_human_confirmation"] is True
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
    assert all(result["target_table"].startswith("agriculture_farm_operations_") for result in executed_operations)
