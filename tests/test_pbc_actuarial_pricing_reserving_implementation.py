from pyAppGen.pbcs.actuarial_pricing_reserving.actuarial_engine import (
    activate_rating_model,
    actuarial_engine_release_evidence,
    assumption_impact_analysis,
    calculate_development_factors,
    calculate_premium_trace,
    chain_ladder_reserve,
    expected_loss_reserve,
    reserve_rollforward,
    select_active_assumption,
    select_rating_model,
    validate_experience_study,
    validate_loss_triangle,
)
from pyAppGen.pbcs.actuarial_pricing_reserving.release_evidence import release_readiness_manifest


def _rating_model(**overrides):
    model = {
        "model_id": "auto-preferred",
        "version": "2026.1",
        "product": "personal_auto",
        "jurisdiction": "KE",
        "segment": "preferred",
        "state": "approved",
        "approval_id": "apr-1",
        "effective_from": "2026-01-01",
        "effective_to": "2026-12-31",
        "base_rate": "1000",
        "minimum_premium": "750",
        "factor_sequence": ("territory", "driver_age_band"),
    }
    model.update(overrides)
    return model


def _factor_library():
    return {
        "territory": {
            "required": True,
            "allowed_values": ("urban", "rural"),
            "relativities": {"urban": "1.20", "rural": "0.90"},
        },
        "driver_age_band": {
            "required": True,
            "allowed_values": ("adult", "youth"),
            "relativities": {"adult": "1.00", "youth": "1.45"},
        },
    }


def _triangle():
    return (
        {"origin_period": "2024", "development_age": 12, "value": "1000"},
        {"origin_period": "2024", "development_age": 24, "value": "1500"},
        {"origin_period": "2024", "development_age": 36, "value": "1800"},
        {"origin_period": "2025", "development_age": 12, "value": "1200"},
        {"origin_period": "2025", "development_age": 24, "value": "1680"},
        {"origin_period": "2025", "development_age": 36, "value": "2016"},
    )


def test_rating_model_governance_and_selection():
    activation = activate_rating_model(_rating_model())
    assert activation["ok"] is True
    assert activation["model"]["state"] == "active"

    retired = activate_rating_model(_rating_model(state="retired", approval_id="apr-old"))
    assert retired["ok"] is False
    assert retired["reason"] == "model_not_approved_for_activation"

    selected = select_rating_model(
        (activation["model"], _rating_model(version="2025.1", state="active", effective_from="2025-01-01", effective_to="2025-12-31")),
        product="personal_auto",
        jurisdiction="KE",
        segment="preferred",
        as_of="2026-05-28",
    )
    assert selected["ok"] is True
    assert selected["selected_model"]["version"] == "2026.1"
    assert selected["side_effects"] == ()


def test_premium_trace_reconstructs_governed_rating():
    model = activate_rating_model(_rating_model())["model"]
    result = calculate_premium_trace(
        model,
        _factor_library(),
        {"territory": "urban", "driver_age_band": "youth"},
        additive_adjustments=({"name": "policy_fee", "amount": "25"},),
    )
    assert result["ok"] is True
    assert result["premium"] == "1765.00"
    assert [step["factor"] for step in result["factor_trace"]] == ["territory", "driver_age_band"]

    invalid = calculate_premium_trace(model, _factor_library(), {"territory": "unknown", "driver_age_band": "adult"})
    assert invalid["ok"] is False
    assert invalid["reason"] == "invalid_factor_inputs"


def test_assumption_registry_and_impact_analysis_are_side_effect_free():
    assumptions = (
        {
            "assumption_type": "loss_trend",
            "selected_value": "0.045",
            "state": "active",
            "approval_id": "assump-1",
            "effective_from": "2026-01-01",
        },
        {
            "assumption_type": "loss_trend",
            "selected_value": "0.030",
            "state": "retired",
            "approval_id": "assump-old",
            "effective_from": "2025-01-01",
        },
    )
    selected = select_active_assumption(assumptions, assumption_type="loss_trend", as_of="2026-05-28")
    assert selected["ok"] is True
    assert selected["assumption"]["selected_value"] == "0.045"

    impact = assumption_impact_analysis(
        selected["assumption"],
        {"assumption_type": "loss_trend", "selected_value": "0.060", "materiality_threshold": "0.01"},
        ({"cohort": "preferred", "basis": "1000000"},),
    )
    assert impact["ok"] is True
    assert impact["requires_approval"] is True
    assert impact["impacts"][0]["delta"] == "15000.00"
    assert impact["side_effects"] == ()


def test_experience_study_quality_and_loss_triangle_governance():
    study = {
        "study_id": "exp-2026",
        "cohort": "preferred-auto",
        "exposure_basis": "earned_car_years",
        "period_basis": "accident_year",
        "data_vintage": "2026Q1",
        "quality_score_floor": "0.95",
        "data_quality": {"completeness": "0.99", "timeliness": "0.97"},
    }
    assert validate_experience_study(study)["ok"] is True
    assert validate_experience_study({**study, "data_quality": {"completeness": "0.80"}})["ok"] is False

    triangle = validate_loss_triangle(_triangle())
    assert triangle["ok"] is True
    broken = validate_loss_triangle(_triangle()[:-1])
    assert broken["ok"] is False
    assert broken["missing_cells"]


def test_reserve_methods_and_rollforward_evidence():
    factors = calculate_development_factors(_triangle())
    assert factors["ok"] is True
    assert factors["factors"][0]["factor"] == "1.4455"

    reserve = chain_ladder_reserve(_triangle())
    assert reserve["ok"] is True
    assert reserve["method"] == "chain_ladder"
    assert reserve["total_unpaid_loss"] == "0.00"

    expected = expected_loss_reserve(
        (
            {"cohort": "preferred", "earned_premium": "1000000", "paid_or_reported_loss": "540000"},
            {"cohort": "standard", "earned_premium": "500000", "paid_or_reported_loss": "310000"},
        ),
        "0.62",
    )
    assert expected["ok"] is True
    assert expected["total_unpaid_loss"] == "80000.00"

    rollforward = reserve_rollforward(
        "1000000",
        {"paid_loss": "-250000", "case_movement": "50000", "assumption_change": "20000"},
        "820000",
    )
    assert rollforward["ok"] is True
    assert rollforward["unexplained_variance"] == "0.00"


def test_actuarial_engine_is_part_of_release_evidence():
    engine = actuarial_engine_release_evidence()
    assert engine["ok"] is True
    assert "premium_calculation_trace" in engine["implemented_backlog_items"]
    assert engine["shared_table_access"] is False

    release = release_readiness_manifest()
    assert release["ok"] is True
    assert "actuarial_engine" in release["sections"]
    assert release["evidence"]["actuarial_engine"]["implemented_backlog_items"] == engine["implemented_backlog_items"]
