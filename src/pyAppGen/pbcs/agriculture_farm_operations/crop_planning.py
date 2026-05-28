"""Crop-plan evaluation for the agriculture_farm_operations PBC."""
from __future__ import annotations

from collections import Counter
from datetime import date

PBC_KEY = "agriculture_farm_operations"
CROP_PLAN_TABLE = f"{PBC_KEY}_crop_plan"
EVENT_CONTRACT = "AppGen-X"
PLANTING_WINDOW_STATUSES = ("early", "optimal", "late", "missed", "unknown")
ACTIVE_PLAN_STATUSES = ("planned", "planned_with_alert", "approved", "released", "active")
REQUIRED_READINESS_CHECKS = ("soil_fit", "fertility_ready", "equipment_ready", "crew_assigned")
WINDOW_BLOCKING_CODES = (
    "soil_temperature_below_threshold",
    "frost_risk_above_threshold",
    "dry_outlook_without_irrigation",
)
YIELD_RISK_BY_WINDOW = {
    "optimal": 0.0,
    "early": 0.05,
    "late": 0.08,
    "missed": 0.18,
    "unknown": 0.03,
}


def _as_date(value) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str) and value:
        return date.fromisoformat(value)
    return None


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1", "y"}:
            return True
        if lowered in {"false", "no", "0", "n", ""}:
            return False
    return bool(value)


def _normalize_plan_id(field_id: str, crop: str, market_year: int, season: str, plan_id: str | None) -> str:
    if plan_id:
        return str(plan_id)
    parts = (field_id, crop, str(market_year), season)
    return "-".join(str(part).strip().lower().replace(" ", "-") for part in parts)


def _normalize_schedule(payload: dict) -> tuple[date | None, date | None]:
    window = dict(payload.get("planting_window") or {})
    planting_date = _as_date(payload.get("planting_date"))
    start = _as_date(payload.get("planned_start") or payload.get("season_start") or window.get("start") or planting_date)
    end = _as_date(payload.get("planned_end") or payload.get("season_end") or window.get("latest") or planting_date)
    return start, end


def _ranges_overlap(left: tuple[date | None, date | None], right: tuple[date | None, date | None]) -> bool:
    left_start, left_end = left
    right_start, right_end = right
    if left_start is None or left_end is None or right_start is None or right_end is None:
        return True
    return left_start <= right_end and right_start <= left_end


def _scope_overlaps(existing: dict, candidate: dict) -> bool:
    if existing.get("field_id") != candidate.get("field_id"):
        return False
    existing_zone = existing.get("management_zone")
    candidate_zone = candidate.get("management_zone")
    if not existing_zone or not candidate_zone:
        return True
    return existing_zone == candidate_zone


def _is_active(existing: dict) -> bool:
    status = str(existing.get("status", "planned")).lower()
    return status in ACTIVE_PLAN_STATUSES


def classify_planting_window(payload: dict) -> dict:
    window = dict(payload.get("planting_window") or {})
    planting_date = _as_date(payload.get("planting_date"))
    start = _as_date(window.get("start"))
    optimal_start = _as_date(window.get("optimal_start"))
    optimal_end = _as_date(window.get("optimal_end"))
    latest = _as_date(window.get("latest"))
    conditions = dict(payload.get("conditions") or {})
    alerts: list[str] = []
    blockers: list[str] = []

    status = "unknown"
    if planting_date and optimal_start and optimal_end and latest:
        if planting_date < optimal_start:
            status = "early"
        elif optimal_start <= planting_date <= optimal_end:
            status = "optimal"
        elif optimal_end < planting_date <= latest:
            status = "late"
        else:
            status = "missed"

    minimum_soil_temperature = window.get("minimum_soil_temperature_c")
    if minimum_soil_temperature is not None:
        actual_soil_temperature = conditions.get("soil_temperature_c")
        if actual_soil_temperature is not None and actual_soil_temperature < minimum_soil_temperature:
            blockers.append("soil_temperature_below_threshold")

    maximum_frost_risk = window.get("maximum_frost_risk")
    if maximum_frost_risk is not None:
        actual_frost_risk = conditions.get("frost_risk")
        if actual_frost_risk is not None and actual_frost_risk > maximum_frost_risk:
            blockers.append("frost_risk_above_threshold")

    minimum_rainfall_outlook = window.get("minimum_rainfall_outlook_mm")
    if minimum_rainfall_outlook is not None:
        rainfall_outlook = conditions.get("rainfall_outlook_mm")
        irrigation_ready = _as_bool((payload.get("readiness") or {}).get("irrigation_ready"))
        if rainfall_outlook is not None and rainfall_outlook < minimum_rainfall_outlook and not irrigation_ready:
            blockers.append("dry_outlook_without_irrigation")

    if status == "missed":
        alerts.append("missed_planting_window")
    elif status == "late":
        alerts.append("late_planting_window")
    elif status == "early":
        alerts.append("early_planting_window")

    alerts.extend(code for code in blockers if code not in alerts)
    day_offset = 0
    if planting_date and optimal_start and planting_date < optimal_start:
        day_offset = (planting_date - optimal_start).days
    elif planting_date and optimal_end and planting_date > optimal_end:
        day_offset = (planting_date - optimal_end).days

    return {
        "status": status,
        "start": start.isoformat() if start else None,
        "optimal_start": optimal_start.isoformat() if optimal_start else None,
        "optimal_end": optimal_end.isoformat() if optimal_end else None,
        "latest": latest.isoformat() if latest else None,
        "alerts": tuple(dict.fromkeys(alerts)),
        "blocking_codes": tuple(dict.fromkeys(blockers)),
        "days_from_optimal_range": day_offset,
        "yield_risk_percent": YIELD_RISK_BY_WINDOW[status],
    }


def evaluate_preplant_readiness(payload: dict, planting_window: dict) -> dict:
    checklist = dict(payload.get("readiness") or {})
    required_checks = list(REQUIRED_READINESS_CHECKS)
    if (payload.get("planting_window") or {}).get("requires_irrigation_ready"):
        required_checks.append("irrigation_ready")
    blockers = [f"missing_{check}" for check in required_checks if not _as_bool(checklist.get(check))]
    blockers.extend(code for code in planting_window.get("blocking_codes", ()) if code in WINDOW_BLOCKING_CODES)
    return {
        "status": "ready" if not blockers else "blocked",
        "required_checks": tuple(required_checks),
        "checklist": {check: _as_bool(checklist.get(check)) for check in tuple(dict.fromkeys(required_checks + ["irrigation_ready"]))},
        "blockers": tuple(dict.fromkeys(blockers)),
    }


def detect_crop_plan_conflicts(existing_plans: tuple[dict, ...], candidate: dict) -> tuple[dict, ...]:
    conflicts = []
    candidate_schedule = _normalize_schedule(candidate)
    for existing in existing_plans:
        if not _is_active(existing):
            continue
        if existing.get("plan_id") == candidate.get("replant_of"):
            continue
        if existing.get("market_year") != candidate.get("market_year"):
            continue
        if not _scope_overlaps(existing, candidate):
            continue
        if not _ranges_overlap(_normalize_schedule(existing), candidate_schedule):
            continue
        conflicts.append(
            {
                "plan_id": existing.get("plan_id"),
                "field_id": existing.get("field_id"),
                "management_zone": existing.get("management_zone"),
                "season": existing.get("season"),
                "status": existing.get("status"),
                "reason_code": "overlapping_active_crop_plan",
            }
        )
    return tuple(conflicts)


def evaluate_crop_plan_submission(existing_plans: tuple[dict, ...], payload: dict) -> dict:
    payload = dict(payload or {})
    required_fields = ("field_id", "crop", "season", "market_year", "planting_date")
    missing_fields = tuple(field for field in required_fields if payload.get(field) in (None, ""))
    field_id = str(payload.get("field_id", "")).strip()
    crop = str(payload.get("crop", "")).strip()
    season = str(payload.get("season", "")).strip().lower()
    market_year = int(payload.get("market_year")) if payload.get("market_year") not in (None, "") else 0
    plan_id = _normalize_plan_id(field_id or "field", crop or "crop", market_year or 0, season or "season", payload.get("plan_id") or payload.get("id"))
    planting_date = _as_date(payload.get("planting_date"))
    planned_start, planned_end = _normalize_schedule(payload)
    window = classify_planting_window(payload)
    readiness = evaluate_preplant_readiness(payload, window)
    normalized_plan = {
        "plan_id": plan_id,
        "tenant": payload.get("tenant", "default"),
        "field_id": field_id or None,
        "management_zone": payload.get("management_zone"),
        "season": season or None,
        "market_year": market_year or None,
        "crop": crop or None,
        "fallback_crop": payload.get("fallback_crop"),
        "previous_crop": payload.get("previous_crop"),
        "replant_of": payload.get("replant_of"),
        "variety": payload.get("variety"),
        "acreage": payload.get("acreage"),
        "planting_date": planting_date.isoformat() if planting_date else None,
        "planned_start": planned_start.isoformat() if planned_start else None,
        "planned_end": planned_end.isoformat() if planned_end else None,
        "planting_window": window,
        "readiness": readiness,
        "event_contract": EVENT_CONTRACT,
        "owned_table": CROP_PLAN_TABLE,
    }

    if missing_fields:
        reason_codes = tuple(f"missing_{field}" for field in missing_fields)
        exception = {
            "plan_id": plan_id,
            "field_id": normalized_plan["field_id"],
            "management_zone": normalized_plan["management_zone"],
            "exception_code": "crop_plan_invalid",
            "reason_codes": reason_codes,
            "severity": "high",
        }
        return {
            "ok": False,
            "accepted": False,
            "plan": {**normalized_plan, "status": "blocked"},
            "conflicts": (),
            "alerts": reason_codes,
            "exception": exception,
            "emitted_event": "AgricultureFarmOperationsExceptionOpened",
            "owned_tables": (CROP_PLAN_TABLE,),
            "side_effects": (),
        }

    conflicts = detect_crop_plan_conflicts(existing_plans, normalized_plan)
    blockers = tuple(dict.fromkeys(readiness["blockers"]))
    accepted = not conflicts and not blockers
    alerts = tuple(dict.fromkeys(window["alerts"] + blockers))
    status = "planned" if accepted and not alerts else "planned_with_alert" if accepted else "blocked"
    plan = {**normalized_plan, "status": status, "alerts": alerts}
    if accepted:
        return {
            "ok": True,
            "accepted": True,
            "plan": plan,
            "conflicts": conflicts,
            "alerts": alerts,
            "exception": None,
            "emitted_event": "AgricultureFarmOperationsCreated",
            "owned_tables": (CROP_PLAN_TABLE,),
            "side_effects": (),
        }

    reason_codes = tuple(dict.fromkeys(tuple(conflict["reason_code"] for conflict in conflicts) + blockers))
    exception = {
        "plan_id": plan_id,
        "field_id": normalized_plan["field_id"],
        "management_zone": normalized_plan["management_zone"],
        "exception_code": "crop_plan_blocked",
        "reason_codes": reason_codes,
        "severity": "high" if conflicts else "medium",
    }
    return {
        "ok": False,
        "accepted": False,
        "plan": plan,
        "conflicts": conflicts,
        "alerts": alerts,
        "exception": exception,
        "emitted_event": "AgricultureFarmOperationsExceptionOpened",
        "owned_tables": (CROP_PLAN_TABLE,),
        "side_effects": (),
    }


def build_crop_plan_workbench_summary(crop_plans: tuple[dict, ...], planning_exceptions: tuple[dict, ...]) -> dict:
    status_counter = Counter(plan.get("status", "unknown") for plan in crop_plans)
    window_counter = Counter(plan.get("planting_window", {}).get("status", "unknown") for plan in crop_plans)
    season_counter = Counter(plan.get("season", "unknown") for plan in crop_plans)
    active_plan_count = sum(1 for plan in crop_plans if plan.get("status") in ACTIVE_PLAN_STATUSES)
    alerts = []
    for plan in crop_plans:
        if plan.get("alerts"):
            alerts.append(
                {
                    "plan_id": plan.get("plan_id"),
                    "field_id": plan.get("field_id"),
                    "status": plan.get("status"),
                    "window_status": plan.get("planting_window", {}).get("status"),
                    "alerts": tuple(plan.get("alerts", ())),
                    "yield_risk_percent": plan.get("planting_window", {}).get("yield_risk_percent", 0.0),
                }
            )
    alerts.sort(key=lambda item: (-item["yield_risk_percent"], item["plan_id"] or ""))
    return {
        "accepted_count": active_plan_count,
        "blocked_count": len(planning_exceptions),
        "status_counts": dict(sorted(status_counter.items())),
        "window_status_counts": dict(sorted(window_counter.items())),
        "season_counts": dict(sorted(season_counter.items())),
        "alerts": tuple(alerts),
        "exception_queue": tuple(planning_exceptions),
    }
