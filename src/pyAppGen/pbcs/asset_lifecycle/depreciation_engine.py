"""Pure helpers for versioned asset depreciation schedules."""

from __future__ import annotations

from decimal import Decimal
from decimal import ROUND_HALF_UP
from typing import Iterable


_CENT = Decimal("0.01")


def normalize_period(value: str) -> str:
    text = str(value or "").strip()
    if len(text) >= 7 and text[4] == "-":
        return text[:7]
    raise ValueError(f"Unsupported depreciation period format: {value}")


def next_period(period: str, offset: int = 1) -> str:
    normalized = normalize_period(period)
    year, month = (int(part) for part in normalized.split("-"))
    absolute = year * 12 + (month - 1) + offset
    next_year = absolute // 12
    next_month = absolute % 12 + 1
    return f"{next_year:04d}-{next_month:02d}"


def first_period_from_service_date(service_date: str) -> str:
    return normalize_period(service_date)


def build_schedule_version(
    asset: dict,
    *,
    method: str,
    version: int,
    revision_reason: str,
    effective_period: str | None = None,
    prior_schedule: dict | None = None,
) -> dict:
    if method != "straight_line":
        return {"ok": False, "reason": "unsupported_method", "method": method}
    if asset.get("status") != "in_service":
        return {"ok": False, "reason": "asset_not_in_service", "asset_id": asset.get("asset_id")}

    posted_months = int(asset.get("depreciation_months_posted", 0))
    total_life_months = int(asset.get("useful_life_months", 0))
    remaining_months = max(total_life_months - posted_months, 0)
    if remaining_months < 1:
        return {
            "ok": False,
            "reason": "no_remaining_life",
            "asset_id": asset.get("asset_id"),
            "total_life_months": total_life_months,
            "posted_months": posted_months,
        }

    current_book_value = _money(asset.get("book_value", asset.get("cost", 0.0)))
    residual_value = _money(asset.get("residual_value", 0.0))
    remaining_basis = max(Decimal("0.00"), current_book_value - residual_value)
    start_period = normalize_period(
        effective_period
        or asset.get("next_depreciation_period")
        or first_period_from_service_date(asset["service_date"])
    )

    amounts = _allocate_amounts(remaining_basis, remaining_months)
    opening_value = current_book_value
    lines = []
    for index, amount in enumerate(amounts, start=1):
        period = next_period(start_period, index - 1)
        closing_value = max(residual_value, opening_value - amount)
        lines.append(
            {
                "schedule_line_id": f"sch_{asset['asset_id']}_v{version}_ln_{index:03d}",
                "sequence": index,
                "period": period,
                "amount": float(amount),
                "opening_book_value": float(opening_value),
                "closing_book_value": float(closing_value),
                "posted": False,
            }
        )
        opening_value = closing_value

    schedule_id = f"sch_{asset['asset_id']}_v{version}"
    assumptions = {
        "current_book_value": float(current_book_value),
        "residual_value": float(residual_value),
        "posted_months": posted_months,
        "total_life_months": total_life_months,
        "remaining_months": remaining_months,
        "effective_period": start_period,
    }
    return {
        "ok": True,
        "schedule_id": schedule_id,
        "asset_id": asset["asset_id"],
        "book": asset["book"],
        "method": method,
        "version": version,
        "status": "active",
        "revision_reason": revision_reason,
        "revises_schedule_id": prior_schedule.get("schedule_id") if prior_schedule else None,
        "revises_version": prior_schedule.get("version") if prior_schedule else None,
        "line_count": len(lines),
        "posted_line_count": 0,
        "next_open_period": lines[0]["period"] if lines else None,
        "assumptions": assumptions,
        "lines": tuple(lines),
    }


def line_fingerprints_for_period(schedule: dict, period: str) -> tuple[tuple[str, int, str], ...]:
    normalized = normalize_period(period)
    return tuple(
        (
            schedule["schedule_id"],
            int(schedule.get("version", 0)),
            line["schedule_line_id"],
        )
        for line in schedule.get("lines", ())
        if line["period"] == normalized
    )


def first_open_line_for_period(schedule: dict, period: str) -> dict | None:
    normalized = normalize_period(period)
    for line in schedule.get("lines", ()):
        if line["period"] == normalized and not line.get("posted"):
            return line
    return None


def posted_periods(schedule_history: Iterable[dict]) -> tuple[str, ...]:
    periods = []
    for schedule in schedule_history:
        for line in schedule.get("lines", ()):
            if line.get("posted"):
                periods.append(line["period"])
    return tuple(periods)


def _allocate_amounts(total: Decimal, periods: int) -> tuple[Decimal, ...]:
    if periods < 1:
        return ()
    if total <= Decimal("0.00"):
        return tuple(Decimal("0.00") for _ in range(periods))

    base = (total / periods).quantize(_CENT, rounding=ROUND_HALF_UP)
    amounts = [base for _ in range(periods)]
    allocated = sum(amounts[:-1], Decimal("0.00"))
    amounts[-1] = (total - allocated).quantize(_CENT, rounding=ROUND_HALF_UP)
    return tuple(amounts)


def _money(value: float | int | str | Decimal) -> Decimal:
    return Decimal(str(value)).quantize(_CENT, rounding=ROUND_HALF_UP)
