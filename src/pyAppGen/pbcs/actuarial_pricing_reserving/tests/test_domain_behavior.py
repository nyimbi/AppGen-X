"""Executable domain behavior tests for the actuarial_pricing_reserving PBC."""

from __future__ import annotations

from .. import agent
from .. import implementation_contract
from .. import release_evidence
from .. import routes
from .. import runtime
from .. import smoke_test
from .. import standalone
from .. import ui
from ..actuarial_engine import activate_rating_model
from ..actuarial_engine import assumption_impact_analysis
from ..actuarial_engine import calculate_development_factors
from ..actuarial_engine import calculate_premium_trace
from ..actuarial_engine import chain_ladder_reserve
from ..actuarial_engine import expected_loss_reserve
from ..actuarial_engine import reserve_rollforward
from ..actuarial_engine import select_active_assumption
from ..actuarial_engine import select_rating_model
from ..actuarial_engine import validate_experience_study
from ..actuarial_engine import validate_factor_inputs
from ..actuarial_engine import validate_loss_triangle
from ..actuarial_engine import validate_rating_model
from ..domain_depth import DOMAIN_OPERATIONS
from ..domain_depth import domain_capability_surface_contract
from ..domain_depth import domain_depth_contract
from ..domain_depth import execute_domain_operation
from ..services import ActuarialPricingReservingService
from ..services import service_operation_contracts
from ..services import service_operation_manifest


TENANT = "tenant_alpha"

RATING_MODEL = {
    "model_id": "AUTO-GLM-2026",
    "version": "2026.1",
    "product": "auto",
    "jurisdiction": "KE",
    "segment": "standard",
    "state": "approved",
    "approval_id": "APR-1",
    "effective_from": "2026-01-01",
    "effective_to": "2026-12-31",
    "base_rate": "1000",
    "factor_sequence": ("territory", "age_band"),
    "minimum_premium": "500",
}

FACTOR_LIBRARY = {
    "territory": {
        "required": True,
        "allowed_values": ("urban", "rural"),
        "relativities": {"urban": "1.20", "rural": "0.90"},
    },
    "age_band": {
        "required": True,
        "allowed_values": ("adult", "young"),
        "relativities": {"adult": "1.00", "young": "1.35"},
    },
}

TRIANGLE = (
    {"origin_period": "2024", "development_age": "12", "value": "100"},
    {"origin_period": "2024", "development_age": "24", "value": "150"},
    {"origin_period": "2025", "development_age": "12", "value": "120"},
    {"origin_period": "2025", "development_age": "24", "value": "180"},
)

CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": runtime.ACTUARIAL_PRICING_RESERVING_REQUIRED_EVENT_TOPIC,
}

POLICY_EVENT = {
    "event_type": "PolicyChanged",
    "event_id": "policy_evt_001",
    "idempotency_key": "policy:auto:001",
    "payload": {"tenant": TENANT, "policy_id": "pol_001", "exposure": "earned_car_year"},
}


def _configured_state() -> dict:
    state = runtime.actuarial_pricing_reserving_empty_state()
    state = runtime.actuarial_pricing_reserving_configure_runtime(state, CONFIGURATION)["state"]
    state = runtime.actuarial_pricing_reserving_set_parameter(state, "quality_score_floor", "0.95")["state"]
    state = runtime.actuarial_pricing_reserving_set_parameter(state, "materiality_threshold", "0.010")["state"]
    state = runtime.actuarial_pricing_reserving_register_rule(
        state,
        {"rule_id": "rate_governance", "scope": "pricing", "status": "active", "approval_required": True},
    )["state"]
    state = runtime.actuarial_pricing_reserving_register_schema_extension(
        state,
        "rating_model",
        {"model_validation_summary": "jsonb", "filing_context": "jsonb"},
    )["state"]
    return state


def test_actuarial_rating_assumption_study_and_reserve_domain_behavior_executes() -> None:
    model_validation = validate_rating_model(RATING_MODEL)
    activation = activate_rating_model(RATING_MODEL)
    selection = select_rating_model(
        ({**RATING_MODEL, "state": "active"}, {**RATING_MODEL, "model_id": "OLD", "version": "2025.1", "state": "active", "effective_from": "2025-01-01"}),
        product="auto",
        jurisdiction="KE",
        segment="standard",
        as_of="2026-06-30",
    )
    factor_validation = validate_factor_inputs(FACTOR_LIBRARY, {"territory": "urban", "age_band": "adult"})
    premium = calculate_premium_trace(
        RATING_MODEL,
        FACTOR_LIBRARY,
        {"territory": "urban", "age_band": "adult"},
        additive_adjustments=({"name": "expense_load", "amount": "25"},),
    )
    assumption = select_active_assumption(
        ({"assumption_type": "loss_trend", "selected_value": "0.060", "state": "active", "approval_id": "A-1", "effective_from": "2026-01-01"},),
        assumption_type="loss_trend",
        as_of="2026-06-30",
    )
    impact = assumption_impact_analysis(
        {"assumption_type": "loss_trend", "selected_value": "0.060"},
        {"assumption_type": "loss_trend", "selected_value": "0.085", "materiality_threshold": "0.010"},
        ({"cohort": "auto", "basis": "1000000"},),
    )
    study = validate_experience_study(
        {
            "study_id": "EXP-2026-Q1",
            "cohort": "auto-standard",
            "exposure_basis": "earned_car_year",
            "period_basis": "accident_year",
            "data_vintage": "2026-04-30",
            "data_quality": {"completeness": "0.98", "timeliness": "0.97"},
        }
    )
    triangle_validation = validate_loss_triangle(TRIANGLE)
    factors = calculate_development_factors(TRIANGLE)
    reserve = chain_ladder_reserve(TRIANGLE)
    expected = expected_loss_reserve(
        ({"cohort": "auto", "earned_premium": "250000", "paid_or_reported_loss": "125000"},),
        "0.68",
    )
    rollforward = reserve_rollforward("100000", {"paid_loss": "-20000", "case_movement": "25000", "assumption_change": "5000"}, "110000")
    uncertainty = standalone.reserve_uncertainty_distribution(reserve["total_unpaid_loss"])
    credibility = standalone.credibility_blend("1.20", "1.05", "0.40")
    dislocation = standalone.rate_dislocation_analysis(("100",), ("140",), cap="0.15")
    freshness = standalone.dependency_freshness_gate(
        {
            "policy_exposure_projection": {"freshness_score": "0.99", "stale_policy": "block"},
            "claims_projection": {"freshness_score": "0.97", "stale_policy": "block"},
        }
    )

    assert model_validation["ok"] is True
    assert activation["ok"] is True and activation["model"]["state"] == "active"
    assert selection["ok"] is True and selection["selected_model"]["model_id"] == "AUTO-GLM-2026"
    assert factor_validation["ok"] is True
    assert premium["ok"] is True and premium["premium"] == "1225.00"
    assert premium["factor_trace"][0]["factor"] == "territory"
    assert assumption["ok"] is True and assumption["assumption"]["approval_id"] == "A-1"
    assert impact["ok"] is True and impact["requires_approval"] is True
    assert impact["impacts"][0]["delta"] == "25000.00"
    assert study["ok"] is True
    assert triangle_validation["ok"] is True
    assert factors["ok"] is True and factors["factors"][0]["factor"] == "1.5000"
    assert reserve["ok"] is True and reserve["total_unpaid_loss"] == "0.00"
    assert expected["ok"] is True and expected["total_unpaid_loss"] == "45000.00"
    assert rollforward["ok"] is True and rollforward["unexplained_variance"] == "0.00"
    assert uncertainty["ok"] is True and uncertainty["percentiles"][2]["percentile"] == "P95"
    assert credibility["ok"] is True and credibility["blended_indication"] == "1.1100"
    assert dislocation["ok"] is True and dislocation["cohorts"][0]["capped"] is True
    assert freshness["ok"] is True


def test_actuarial_runtime_events_services_routes_ui_and_agent_are_executable() -> None:
    state = _configured_state()
    received = runtime.actuarial_pricing_reserving_receive_event(state, POLICY_EVENT)
    duplicate = runtime.actuarial_pricing_reserving_receive_event(received["state"], POLICY_EVENT)
    dead = runtime.actuarial_pricing_reserving_receive_event(
        duplicate["state"],
        {"event_type": "UnexpectedEvent", "event_id": "bad_evt", "idempotency_key": "bad_evt", "payload": {"tenant": TENANT}},
    )
    command = runtime.actuarial_pricing_reserving_command_rating_model(
        dead["state"],
        {"tenant": TENANT, "code": "AUTO-GLM-2026", "status": "candidate"},
    )
    query = runtime.actuarial_pricing_reserving_query_workbench(command["state"], {"tenant": TENANT})
    assessment = runtime.actuarial_pricing_reserving_run_advanced_assessment(command["state"], {"tenant": TENANT})
    parser = runtime.actuarial_pricing_reserving_parse_document_instruction(
        "Actuarial memo requests reserve close and trend assumption update.",
        "create reserve estimate and assumption impact preview",
    )
    schema_extension_bad = runtime.actuarial_pricing_reserving_register_schema_extension(
        command["state"],
        "shared_actuarial_table",
        {"x": "jsonb"},
    )
    schema = runtime.actuarial_pricing_reserving_build_schema_contract()
    service_contract = runtime.actuarial_pricing_reserving_build_service_contract()
    api_contract = runtime.actuarial_pricing_reserving_build_api_contract()
    release = runtime.actuarial_pricing_reserving_build_release_evidence()
    permissions = runtime.actuarial_pricing_reserving_permissions_contract()
    workbench = runtime.actuarial_pricing_reserving_build_workbench_view(tenant=TENANT)
    boundary_ok = runtime.actuarial_pricing_reserving_verify_owned_table_boundary(runtime.ACTUARIAL_PRICING_RESERVING_OWNED_TABLES[:2])
    boundary_bad = runtime.actuarial_pricing_reserving_verify_owned_table_boundary(("foreign_table",))
    capabilities = runtime.actuarial_pricing_reserving_runtime_capabilities()
    runtime_smoke = runtime.actuarial_pricing_reserving_runtime_smoke()
    service = ActuarialPricingReservingService()
    service_command = service.create_rating_model({"tenant": TENANT, "model_id": "AUTO-GLM-2026"})
    service_query = service.query_workbench({"tenant": TENANT})
    route_contracts = routes.api_route_contracts()
    route_validation = routes.validate_api_route_contracts()
    route_dispatch = routes.dispatch_route("POST /rating-models", {"tenant": TENANT})
    ui_contract = ui.actuarial_pricing_reserving_ui_contract()
    rendered = ui.actuarial_pricing_reserving_render_workbench()
    skills = agent.agent_skill_manifest()
    chatbot = agent.chatbot_interface_contract()
    document_plan = agent.document_instruction_plan(
        "Reserve close memo with trend assumption and capital stress.",
        "create reserve estimate and run capital scenario",
    )
    crud_plan = agent.datastore_crud_plan(
        "create",
        "actuarial_pricing_reserving_reserve_estimate",
        {"reserve_estimate_id": "RES-1"},
    )
    blocked_plan = agent.datastore_crud_plan("update", "shared_reserve_table", {})
    contribution = agent.composed_agent_contribution()

    assert received["ok"] is True and received["state"]["inbox"]
    assert duplicate["ok"] is True and duplicate["duplicate"] is True
    assert dead["ok"] is False and dead["dead_letter_table"] == "actuarial_pricing_reserving_appgen_dead_letter_event"
    assert command["ok"] is True and command["record"]["tenant"] == TENANT
    assert command["state"]["outbox"][-1]["event_type"] == "ActuarialPricingReservingCreated"
    assert query["ok"] is True and query["read_only"] is True
    assert assessment["ok"] is True and "agent_review_ready" in assessment["explanations"]
    assert parser["ok"] is True and parser["requires_human_confirmation"] is True
    assert schema_extension_bad["ok"] is False and schema_extension_bad["reason"] == "unknown_owned_table"
    assert schema["ok"] is True and schema["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert service_contract["ok"] is True and "create_rating_model" in service_contract["command_methods"]
    assert api_contract["ok"] is True and api_contract["stream_engine_picker_visible"] is False
    assert release["ok"] is True and not release["blocking_gaps"]
    assert permissions["ok"] is True and "actuarial_pricing_reserving.admin" in permissions["permissions"]
    assert workbench["ok"] is True and "ActuarialPricingReservingWorkbench" in workbench["ui_fragments"]
    assert boundary_ok["ok"] is True
    assert boundary_bad["ok"] is False and boundary_bad["invalid_references"] == ("foreign_table",)
    assert capabilities["ok"] is True and capabilities["event_contract"] == "AppGen-X"
    assert runtime_smoke["ok"] is True
    assert service_operation_manifest()["ok"] is True
    assert service_operation_contracts()["ok"] is True
    assert service_command["ok"] is True and service_command["transaction_boundary"] == "owned_datastore_plus_outbox"
    assert service_query["ok"] is True and service_query["read_only"] is True
    assert route_contracts["ok"] is True and "GET /actuarial-pricing-reserving/app" in route_contracts["routes"]
    assert route_validation["ok"] is True
    assert route_dispatch["ok"] is True
    assert ui_contract["ok"] is True and ui_contract["stream_engine_picker_visible"] is False
    assert rendered["ok"] is True and rendered["form_count"] >= 7 and rendered["wizard_count"] >= 6
    assert skills["ok"] is True
    assert chatbot["ok"] is True and chatbot["single_agent_contribution"] == "actuarial_pricing_reserving_skills"
    assert document_plan["ok"] is True and document_plan["requires_human_confirmation"] is True
    assert any(item["operation"] == "create_reserve_estimate" for item in document_plan["candidate_commands"])
    assert crud_plan["ok"] is True and crud_plan["requires_confirmation"] is True
    assert blocked_plan["ok"] is False
    assert contribution["ok"] is True and "actuarial_pricing_reserving_crud" in contribution["dsl_tools"]


def test_actuarial_standalone_release_controls_and_package_metadata_are_executable() -> None:
    forms = standalone.actuarial_forms_contract()
    wizards = standalone.actuarial_wizards_contract()
    controls = standalone.actuarial_controls_contract()
    app = standalone.single_pbc_app_contract()
    standalone_smoke = standalone.standalone_smoke_test()
    simulation = standalone.full_actuarial_release_simulation()
    validation = standalone.model_validation_gate(
        RATING_MODEL,
        {"validation_id": "VAL-1", "reviewer_independent": True, "status": "passed", "expires_on": "2027-01-01", "backtest_ok": True},
    )
    drift = standalone.monitor_model_drift(
        {"calibration_error": "0.02", "loss_ratio_emergence": "0.04"},
        {"calibration_error": "0.05", "loss_ratio_emergence": "0.05"},
    )
    memo = standalone.assemble_actuarial_memo(
        {"data": "study", "methods": "chain ladder", "selection": "selected reserve"},
        {"data": ("EXP-2026-Q1",), "methods": ("TRI-1",), "selection": ("RES-1",)},
    )
    run_package = standalone.create_run_package({"model": RATING_MODEL}, {"premium": "1225.00"})
    proof = standalone.verify_evidence_chain(
        (
            {"event_type": "AssumptionApproved", "payload_hash": "A"},
            {"event_type": "ReserveSelected", "payload_hash": "B"},
            {"event_type": "ClosePackageLocked", "payload_hash": run_package["package_hash"]},
        )
    )
    handoff = standalone.finance_handoff_event(
        {"close_package_id": "CLOSE-2026-Q1", "reserve_estimate_id": "RES-1", "risk_margin": "5000", "capital_metric": "1.42"}
    )
    replay = standalone.replay_dead_letter_event({"idempotency_keys": {"idem-1"}}, {"idempotency_key": "idem-1"})
    overlap = standalone.overlap_guardrail(("policy_exposure_projection", "claims_projection", "gl_entry"))
    release_validation = release_evidence.validate_release_evidence()
    release_manifest = release_evidence.release_readiness_manifest()
    release_build = release_evidence.build_release_evidence()
    package_contract = implementation_contract()
    package_smoke = smoke_test()
    domain = domain_depth_contract()
    surface = domain_capability_surface_contract()
    executed_operations = tuple(execute_domain_operation(operation, {"tenant": TENANT}) for operation in DOMAIN_OPERATIONS[:6])

    assert forms["ok"] is True and forms["covered_improve1_items"] == tuple(range(1, 51))
    assert wizards["ok"] is True and wizards["covered_improve1_items"] == tuple(range(1, 51))
    assert controls["ok"] is True and controls["event_contract"] == "AppGen-X"
    assert app["ok"] is True and app["database_backends"] == ("postgresql", "mysql", "mariadb")
    assert app["dsl_exposure"]["agent_skill_namespace"] == "actuarial_pricing_reserving_skills"
    assert standalone_smoke["ok"] is True
    assert simulation["ok"] is True and simulation["blocking_gaps"] == ()
    assert validation["ok"] is True and validation["blocks_activation"] is False
    assert drift["ok"] is True and drift["open_review_task"] is False
    assert memo["ok"] is True
    assert run_package["ok"] is True and run_package["package_hash"]
    assert proof["ok"] is True and len(proof["chain"]) == 3
    assert handoff["ok"] is True and "gl_entry" in handoff["forbidden_writes"]
    assert replay["ok"] is True and replay["duplicate"] is True
    assert overlap["ok"] is False and "gl_entry" in overlap["forbidden_references"]
    assert release_validation["ok"] is True
    assert release_manifest["ok"] is True
    assert release_build["ok"] is True and not release_build["blocking_gaps"]
    assert package_contract["single_pbc_app"]["ok"] is True and package_contract["advanced_runtime"]["ok"] is True
    assert package_smoke["ok"] is True
    assert domain["ok"] is True and domain["event_contract"] == "AppGen-X"
    assert surface["ok"] is True and surface["coverage"]["shared_table_access"] is False
    assert all(result["ok"] is True for result in executed_operations)
    assert all(result["target_table"].startswith("actuarial_pricing_reserving_") for result in executed_operations)
