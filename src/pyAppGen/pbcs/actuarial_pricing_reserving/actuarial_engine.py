"""Executable actuarial pricing and reserving primitives.

The functions in this module are intentionally side-effect-free. They return
evidence dictionaries that can be used by generated services, UI workbenches,
agent previews, and release audits without mutating external policy, claims,
reinsurance, investment, or ledger systems.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable, Mapping, Sequence

PBC_KEY = "actuarial_pricing_reserving"
EVENT_CONTRACT = "AppGen-X"

MODEL_STATES = (
    "draft",
    "candidate",
    "validated",
    "approved",
    "active",
    "suspended",
    "retired",
    "superseded",
)
ACTIVATABLE_STATES = ("approved", "active")
ASSUMPTION_ACTIVE_STATES = ("approved", "active")


def _to_decimal(value: object) -> Decimal:
    return Decimal(str(value))


def _money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _date(value: object) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _within_window(record: Mapping[str, object], as_of: date) -> bool:
    start = _date(record.get("effective_from", "0001-01-01"))
    end_value = record.get("effective_to")
    end = _date(end_value) if end_value else date.max
    return start <= as_of <= end


def validate_rating_model(model: Mapping[str, object]) -> dict:
    """Validate core rating model governance fields."""

    required = (
        "model_id",
        "version",
        "product",
        "jurisdiction",
        "segment",
        "state",
        "effective_from",
        "base_rate",
        "factor_sequence",
    )
    missing = tuple(field for field in required if field not in model)
    state = model.get("state")
    problems = []
    if state not in MODEL_STATES:
        problems.append("unknown_state")
    if state in ("active", "approved") and not model.get("approval_id"):
        problems.append("missing_approval")
    if _to_decimal(model.get("base_rate", 0)) <= 0:
        problems.append("base_rate_must_be_positive")
    return {
        "ok": not missing and not problems,
        "pbc": PBC_KEY,
        "missing": missing,
        "problems": tuple(problems),
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def activate_rating_model(model: Mapping[str, object]) -> dict:
    """Return an activation plan for a governed rating model version."""

    validation = validate_rating_model(model)
    state = model.get("state")
    if not validation["ok"]:
        return {
            "ok": False,
            "reason": "invalid_model",
            "validation": validation,
            "side_effects": (),
        }
    if state not in ACTIVATABLE_STATES:
        return {
            "ok": False,
            "reason": "model_not_approved_for_activation",
            "state": state,
            "side_effects": (),
        }
    activated = dict(model)
    activated["state"] = "active"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "model": activated,
        "emitted_event": "ActuarialPricingReservingApproved",
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def select_rating_model(
    models: Iterable[Mapping[str, object]],
    *,
    product: str,
    jurisdiction: str,
    segment: str,
    as_of: object,
) -> dict:
    """Select the newest active model matching scope and effective date."""

    as_of_date = _date(as_of)
    candidates = [
        dict(model)
        for model in models
        if model.get("state") == "active"
        and model.get("product") == product
        and model.get("jurisdiction") == jurisdiction
        and model.get("segment") == segment
        and _within_window(model, as_of_date)
    ]
    candidates.sort(key=lambda item: (_date(item["effective_from"]), str(item["version"])), reverse=True)
    return {
        "ok": bool(candidates),
        "pbc": PBC_KEY,
        "selected_model": candidates[0] if candidates else None,
        "candidate_count": len(candidates),
        "as_of": as_of_date.isoformat(),
        "side_effects": (),
    }


def validate_factor_inputs(
    factor_library: Mapping[str, Mapping[str, object]],
    inputs: Mapping[str, object],
) -> dict:
    """Validate rating inputs against a governed factor library."""

    errors: list[dict] = []
    normalized: dict[str, object] = {}
    for factor_name, definition in factor_library.items():
        required = bool(definition.get("required", True))
        if factor_name not in inputs:
            if required and "default" not in definition:
                errors.append({"factor": factor_name, "reason": "missing_required_factor"})
                continue
            normalized[factor_name] = definition.get("default")
            continue
        value = inputs[factor_name]
        allowed = definition.get("allowed_values")
        if allowed and value not in allowed:
            errors.append({"factor": factor_name, "reason": "unknown_factor_value", "value": value})
            continue
        normalized[factor_name] = value
    return {
        "ok": not errors,
        "pbc": PBC_KEY,
        "normalized_inputs": normalized,
        "errors": tuple(errors),
        "side_effects": (),
    }


def calculate_premium_trace(
    model: Mapping[str, object],
    factor_library: Mapping[str, Mapping[str, object]],
    inputs: Mapping[str, object],
    *,
    additive_adjustments: Sequence[Mapping[str, object]] = (),
    override: Mapping[str, object] | None = None,
) -> dict:
    """Calculate premium and return an auditable factor-by-factor trace."""

    activation = activate_rating_model(model)
    if not activation["ok"]:
        return {"ok": False, "reason": activation["reason"], "activation": activation, "side_effects": ()}
    validation = validate_factor_inputs(factor_library, inputs)
    if not validation["ok"]:
        return {"ok": False, "reason": "invalid_factor_inputs", "validation": validation, "side_effects": ()}

    premium = _to_decimal(model["base_rate"])
    trace = []
    normalized = validation["normalized_inputs"]
    for factor_name in model.get("factor_sequence", ()):
        definition = factor_library[factor_name]
        value = normalized.get(factor_name)
        relativity = _to_decimal(definition.get("relativities", {}).get(value, definition.get("default_relativity", 1)))
        before = premium
        premium *= relativity
        trace.append(
            {
                "factor": factor_name,
                "value": value,
                "relativity": str(relativity),
                "before": str(_money(before)),
                "after": str(_money(premium)),
            }
        )

    adjustment_trace = []
    for adjustment in additive_adjustments:
        amount = _to_decimal(adjustment["amount"])
        before = premium
        premium += amount
        adjustment_trace.append(
            {
                "name": adjustment.get("name", "adjustment"),
                "amount": str(_money(amount)),
                "before": str(_money(before)),
                "after": str(_money(premium)),
            }
        )

    minimum = _to_decimal(model.get("minimum_premium", 0))
    minimum_applied = premium < minimum
    if minimum_applied:
        premium = minimum

    override_evidence = None
    if override:
        if not override.get("reason") or "premium" not in override:
            return {"ok": False, "reason": "invalid_override_evidence", "side_effects": ()}
        override_evidence = {"reason": override["reason"], "original_premium": str(_money(premium))}
        premium = _to_decimal(override["premium"])

    return {
        "ok": True,
        "pbc": PBC_KEY,
        "model_id": model["model_id"],
        "version": model["version"],
        "premium": str(_money(premium)),
        "factor_trace": tuple(trace),
        "adjustment_trace": tuple(adjustment_trace),
        "minimum_applied": minimum_applied,
        "override": override_evidence,
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def select_active_assumption(
    assumptions: Iterable[Mapping[str, object]],
    *,
    assumption_type: str,
    as_of: object,
) -> dict:
    """Select an active approved assumption of the requested type."""

    as_of_date = _date(as_of)
    candidates = [
        dict(item)
        for item in assumptions
        if item.get("assumption_type") == assumption_type
        and item.get("state") in ASSUMPTION_ACTIVE_STATES
        and item.get("approval_id")
        and _within_window(item, as_of_date)
    ]
    candidates.sort(key=lambda item: _date(item["effective_from"]), reverse=True)
    return {
        "ok": bool(candidates),
        "pbc": PBC_KEY,
        "assumption": candidates[0] if candidates else None,
        "side_effects": (),
    }


def assumption_impact_analysis(
    current: Mapping[str, object],
    proposed: Mapping[str, object],
    exposure_bases: Sequence[Mapping[str, object]],
) -> dict:
    """Compare current and proposed assumptions without mutating state."""

    current_value = _to_decimal(current["selected_value"])
    proposed_value = _to_decimal(proposed["selected_value"])
    delta = proposed_value - current_value
    impacts = []
    for exposure in exposure_bases:
        base = _to_decimal(exposure["basis"])
        impacts.append(
            {
                "cohort": exposure.get("cohort", "default"),
                "basis": str(base),
                "current_impact": str(_money(base * current_value)),
                "proposed_impact": str(_money(base * proposed_value)),
                "delta": str(_money(base * delta)),
            }
        )
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "assumption_type": current.get("assumption_type") or proposed.get("assumption_type"),
        "current_value": str(current_value),
        "proposed_value": str(proposed_value),
        "delta": str(delta),
        "impacts": tuple(impacts),
        "requires_approval": abs(delta) >= _to_decimal(proposed.get("materiality_threshold", "0.01")),
        "side_effects": (),
    }


def validate_experience_study(study: Mapping[str, object]) -> dict:
    required = ("study_id", "cohort", "exposure_basis", "period_basis", "data_vintage")
    missing = tuple(field for field in required if not study.get(field))
    quality = study.get("data_quality", {})
    failing_quality = tuple(
        name for name, value in quality.items() if _to_decimal(value) < _to_decimal(study.get("quality_score_floor", "0.95"))
    )
    return {
        "ok": not missing and not failing_quality,
        "pbc": PBC_KEY,
        "missing": missing,
        "failing_quality": failing_quality,
        "side_effects": (),
    }


def validate_loss_triangle(cells: Sequence[Mapping[str, object]]) -> dict:
    origins = tuple(sorted({str(cell["origin_period"]) for cell in cells}))
    ages = tuple(sorted({_to_decimal(cell["development_age"]) for cell in cells}))
    values = {(str(cell["origin_period"]), _to_decimal(cell["development_age"])): _to_decimal(cell["value"]) for cell in cells}
    missing = []
    negative = []
    for origin in origins:
        for age in ages:
            key = (origin, age)
            if key not in values:
                missing.append({"origin_period": origin, "development_age": str(age)})
            elif values[key] < 0:
                negative.append({"origin_period": origin, "development_age": str(age)})
    return {
        "ok": not missing and not negative,
        "pbc": PBC_KEY,
        "origin_periods": origins,
        "development_ages": tuple(str(age) for age in ages),
        "missing_cells": tuple(missing),
        "negative_cells": tuple(negative),
        "side_effects": (),
    }


def calculate_development_factors(cells: Sequence[Mapping[str, object]]) -> dict:
    validation = validate_loss_triangle(cells)
    if not validation["ok"]:
        return {"ok": False, "reason": "invalid_triangle", "validation": validation, "side_effects": ()}
    by_origin = {}
    for cell in cells:
        by_origin.setdefault(str(cell["origin_period"]), {})[_to_decimal(cell["development_age"])] = _to_decimal(cell["value"])
    ages = [_to_decimal(age) for age in validation["development_ages"]]
    factors = []
    for age, next_age in zip(ages, ages[1:]):
        numerator = sum(origin_values[next_age] for origin_values in by_origin.values() if origin_values[age] > 0)
        denominator = sum(origin_values[age] for origin_values in by_origin.values() if origin_values[age] > 0)
        factors.append(
            {
                "from_age": str(age),
                "to_age": str(next_age),
                "factor": str((numerator / denominator).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)),
                "basis": "volume_weighted",
            }
        )
    return {"ok": True, "pbc": PBC_KEY, "factors": tuple(factors), "side_effects": ()}


def chain_ladder_reserve(cells: Sequence[Mapping[str, object]], selected_factors: Sequence[Mapping[str, object]] | None = None) -> dict:
    factor_result = calculate_development_factors(cells)
    if not factor_result["ok"]:
        return factor_result
    factors = selected_factors or factor_result["factors"]
    factor_map = {_to_decimal(item["from_age"]): _to_decimal(item["factor"]) for item in factors}
    by_origin = {}
    for cell in cells:
        by_origin.setdefault(str(cell["origin_period"]), {})[_to_decimal(cell["development_age"])] = _to_decimal(cell["value"])
    estimates = []
    for origin, origin_values in sorted(by_origin.items()):
        latest_age = max(origin_values)
        latest_value = origin_values[latest_age]
        ultimate = latest_value
        for age in sorted(age for age in factor_map if age >= latest_age):
            ultimate *= factor_map[age]
        estimates.append(
            {
                "origin_period": origin,
                "latest_age": str(latest_age),
                "latest_value": str(_money(latest_value)),
                "ultimate_loss": str(_money(ultimate)),
                "unpaid_loss": str(_money(ultimate - latest_value)),
                "method": "chain_ladder",
            }
        )
    total_unpaid = sum(_to_decimal(item["unpaid_loss"]) for item in estimates)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "method": "chain_ladder",
        "selected_factors": tuple(factors),
        "estimates": tuple(estimates),
        "total_unpaid_loss": str(_money(total_unpaid)),
        "side_effects": (),
    }


def expected_loss_reserve(exposures: Sequence[Mapping[str, object]], expected_loss_ratio: object) -> dict:
    ratio = _to_decimal(expected_loss_ratio)
    estimates = []
    for exposure in exposures:
        earned_premium = _to_decimal(exposure["earned_premium"])
        paid_or_reported = _to_decimal(exposure.get("paid_or_reported_loss", 0))
        ultimate = earned_premium * ratio
        estimates.append(
            {
                "cohort": exposure.get("cohort", "default"),
                "ultimate_loss": str(_money(ultimate)),
                "unpaid_loss": str(_money(ultimate - paid_or_reported)),
                "method": "expected_loss_ratio",
            }
        )
    total_unpaid = sum(_to_decimal(item["unpaid_loss"]) for item in estimates)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "method": "expected_loss_ratio",
        "expected_loss_ratio": str(ratio),
        "estimates": tuple(estimates),
        "total_unpaid_loss": str(_money(total_unpaid)),
        "side_effects": (),
    }


def reserve_rollforward(prior_reserve: object, movements: Mapping[str, object], selected_reserve: object) -> dict:
    prior = _to_decimal(prior_reserve)
    selected = _to_decimal(selected_reserve)
    movement_total = sum(_to_decimal(value) for value in movements.values())
    indicated = prior + movement_total
    variance = selected - indicated
    return {
        "ok": variance == 0,
        "pbc": PBC_KEY,
        "prior_reserve": str(_money(prior)),
        "movements": tuple({"component": key, "amount": str(_money(_to_decimal(value)))} for key, value in movements.items()),
        "indicated_reserve": str(_money(indicated)),
        "selected_reserve": str(_money(selected)),
        "unexplained_variance": str(_money(variance)),
        "side_effects": (),
    }


def actuarial_engine_release_evidence() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "implemented_backlog_items": (
            "rating_model_version_governance",
            "rating_factor_library",
            "premium_calculation_trace",
            "actuarial_assumption_registry",
            "assumption_change_impact_analysis",
            "experience_study_cohort_definition",
            "data_quality_scoring_for_studies",
            "loss_development_triangle_governance",
            "development_factor_selection",
            "reserve_estimate_methods",
            "reserve_rollforward",
        ),
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }
