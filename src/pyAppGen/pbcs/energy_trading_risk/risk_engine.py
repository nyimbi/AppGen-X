"""Executable risk and workflow logic for the energy_trading_risk slice."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone
import hashlib

from .config import default_policy_rules
from .config import default_runtime_parameters

PBC_KEY = "energy_trading_risk"
EVENT_CONTRACT = "AppGen-X"
_VALID_SIDES = {"BUY", "SELL"}
_VALID_POSITION_TYPES = {"physical", "financial", "linked"}
_ACTIVE_TRADE_STATUSES = {"risk_passed", "scheduled", "settled", "approved"}



def _digest(value) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()



def _missing(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (tuple, list, set, dict)):
        return len(value) == 0
    return False



def _number(value):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None



def _parse_timestamp(value: str | None):
    if not value or not isinstance(value, str):
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)



def _trade_signature(payload: dict) -> str:
    fields = (
        payload.get("tenant", "default"),
        payload.get("commodity"),
        payload.get("market_hub"),
        payload.get("book"),
        payload.get("counterparty"),
        payload.get("side"),
        payload.get("position_type"),
        payload.get("delivery_start"),
        payload.get("delivery_end"),
        payload.get("delivery_profile"),
        payload.get("volume_mwh"),
        payload.get("fixed_price"),
    )
    return _digest(fields)



def signed_volume(volume_mwh, side: str) -> float:
    size = _number(volume_mwh) or 0.0
    return size if str(side).upper() == "BUY" else -size



def derive_delivery_period(payload: dict) -> str:
    start = str(payload.get("delivery_start", "")).strip()
    end = str(payload.get("delivery_end", "")).strip()
    if len(start) >= 7 and start[:7] == end[:7]:
        return start[:7]
    if len(start) >= 7:
        return start[:7]
    return payload.get("delivery_period", "unknown")



def exposure_bucket_key(payload: dict) -> tuple[str, str, str, str]:
    return (
        str(payload.get("commodity", "")).strip().lower(),
        str(payload.get("market_hub", "")).strip().upper(),
        derive_delivery_period(payload),
        str(payload.get("book", "")).strip().upper(),
    )



def select_applicable_limit(limit_records, payload: dict):
    bucket = exposure_bucket_key(payload)
    best = None
    best_score = None
    for record in limit_records:
        if record.get("status") in {"retired", "cancelled"}:
            continue
        candidate = dict(record.get("payload", {}))
        score = 0
        for value, field in zip(bucket[:3], ("commodity", "market_hub", "delivery_period")):
            expected = str(candidate.get(field, "")).strip().lower() if field == "commodity" else str(candidate.get(field, "")).strip().upper()
            if expected and expected != value:
                score = None
                break
            if expected:
                score += 1
        if score is None:
            continue
        expected_book = str(candidate.get("book", "")).strip().upper()
        if expected_book and expected_book != bucket[3]:
            continue
        if expected_book:
            score += 1
        if best is None or score > best_score:
            best = record
            best_score = score
    return best



def select_market_curve(curve_records, payload: dict):
    bucket = exposure_bucket_key(payload)
    selected = None
    selected_ts = None
    for record in curve_records:
        candidate = dict(record.get("payload", {}))
        if str(candidate.get("commodity", "")).strip().lower() != bucket[0]:
            continue
        if str(candidate.get("market_hub", "")).strip().upper() != bucket[1]:
            continue
        if str(candidate.get("delivery_period", "")).strip() != bucket[2]:
            continue
        timestamp = _parse_timestamp(candidate.get("as_of"))
        if timestamp is None:
            continue
        if selected is None or timestamp > selected_ts:
            selected = record
            selected_ts = timestamp
    return selected



def build_exposure_buckets(trade_records) -> tuple[dict, ...]:
    buckets: dict[tuple[str, str, str, str], dict] = {}
    for record in trade_records:
        if record.get("status") not in _ACTIVE_TRADE_STATUSES:
            continue
        payload = dict(record.get("payload", {}))
        bucket_key = exposure_bucket_key(payload)
        entry = buckets.setdefault(
            bucket_key,
            {
                "commodity": bucket_key[0],
                "market_hub": bucket_key[1],
                "delivery_period": bucket_key[2],
                "book": bucket_key[3],
                "net_volume_mwh": 0.0,
                "projected_mtm": 0.0,
                "trade_ids": [],
            },
        )
        entry["net_volume_mwh"] += float(record.get("signed_volume_mwh", 0.0))
        entry["projected_mtm"] += float(record.get("projected_mark_to_market", 0.0))
        entry["trade_ids"].append(record.get("id"))
    return tuple(
        {
            **value,
            "net_volume_mwh": round(value["net_volume_mwh"], 4),
            "projected_mtm": round(value["projected_mtm"], 2),
            "trade_ids": tuple(value["trade_ids"]),
        }
        for value in sorted(
            buckets.values(),
            key=lambda item: (item["commodity"], item["market_hub"], item["delivery_period"], item["book"]),
        )
    )



def evaluate_trade_capture(payload: dict | None, existing_records=(), parameters=None, rules=None, limit_records=(), curve_records=()):
    payload = dict(payload or {})
    parameter_values = {
        name: item["value"] for name, item in (parameters or default_runtime_parameters()).items()
    }
    defaults = default_policy_rules()
    rule_values = dict(defaults)
    rule_values.update(rules or {})
    trade_policy = dict(defaults["trade_capture_policy"])
    trade_policy.update(rule_values.get("trade_capture_policy", {}))

    required_fields = tuple(trade_policy["required_fields"])
    missing_fields = tuple(field for field in required_fields if _missing(payload.get(field)))
    invalid_fields = []

    side = str(payload.get("side", "")).strip().upper()
    if side not in _VALID_SIDES:
        invalid_fields.append("side")

    position_type = str(payload.get("position_type", "")).strip().lower()
    if position_type not in set(trade_policy["allowed_position_types"]):
        invalid_fields.append("position_type")

    volume_mwh = _number(payload.get("volume_mwh"))
    if volume_mwh is None or volume_mwh <= 0:
        invalid_fields.append("volume_mwh")

    fixed_price = _number(payload.get("fixed_price"))
    if fixed_price is None or fixed_price <= 0:
        invalid_fields.append("fixed_price")

    submitted_at = _parse_timestamp(payload.get("submitted_at"))
    if payload.get("submitted_at") and submitted_at is None:
        invalid_fields.append("submitted_at")
    evaluation_time = submitted_at or datetime.now(timezone.utc)

    bucket_key = exposure_bucket_key(payload)
    current_bucket_volume = 0.0
    duplicate_matches = []
    signature = _trade_signature(payload)
    window_minutes = int(trade_policy["duplicate_window_minutes"])
    for record in existing_records:
        existing_payload = dict(record.get("payload", {}))
        if record.get("trade_signature") == signature:
            match_time = _parse_timestamp(existing_payload.get("submitted_at"))
            if submitted_at is None or match_time is None:
                duplicate_matches.append({"id": record.get("id"), "status": record.get("status")})
            else:
                gap = abs((submitted_at - match_time).total_seconds())
                if gap <= window_minutes * 60:
                    duplicate_matches.append({"id": record.get("id"), "status": record.get("status")})
        if exposure_bucket_key(existing_payload) == bucket_key and record.get("status") in _ACTIVE_TRADE_STATUSES:
            current_bucket_volume += float(record.get("signed_volume_mwh", 0.0))

    signed_volume_mwh = signed_volume(volume_mwh, side)
    candidate_bucket_volume = current_bucket_volume + signed_volume_mwh

    curve_record = select_market_curve(curve_records, payload)
    curve_payload = dict(curve_record.get("payload", {})) if curve_record else {}
    curve_as_of = _parse_timestamp(curve_payload.get("as_of")) if curve_record else None
    curve_age_hours = None
    market_curve_failures = []
    if curve_record is None:
        market_curve_failures.append({"gate": "market_curve_available", "reason": "missing_curve_for_bucket"})
    else:
        curve_age_hours = round((evaluation_time - curve_as_of).total_seconds() / 3600, 2) if curve_as_of else None
        if curve_age_hours is not None and curve_age_hours > float(parameter_values["curve_max_age_hours"]):
            market_curve_failures.append(
                {
                    "gate": "curve_freshness",
                    "reason": "curve_is_stale",
                    "age_hours": curve_age_hours,
                }
            )

    mark_price = _number(curve_payload.get("curve_price"))
    projected_mtm = round(signed_volume_mwh * ((mark_price or 0.0) - (fixed_price or 0.0)), 2)

    limit_record = select_applicable_limit(limit_records, payload)
    limit_payload = dict(limit_record.get("payload", {})) if limit_record else {}
    limit_breaches = []
    max_net_exposure = _number(limit_payload.get("max_net_exposure_mwh"))
    if max_net_exposure is not None and abs(candidate_bucket_volume) > max_net_exposure:
        limit_breaches.append(
            {
                "gate": "net_exposure_limit",
                "reason": "candidate_bucket_volume_exceeds_limit",
                "candidate_bucket_volume_mwh": round(candidate_bucket_volume, 4),
                "limit_mwh": max_net_exposure,
            }
        )
    max_projected_mtm = _number(limit_payload.get("max_projected_mtm")) or float(parameter_values["risk_threshold"])
    if abs(projected_mtm) > max_projected_mtm:
        limit_breaches.append(
            {
                "gate": "projected_mtm_limit",
                "reason": "projected_mark_to_market_exceeds_limit",
                "projected_mtm": projected_mtm,
                "limit": max_projected_mtm,
            }
        )

    requires_four_eyes = abs(projected_mtm) >= float(parameter_values["materiality_threshold"])
    approval_state = str(payload.get("approval_state", "pending")).strip().lower() or "pending"
    approval_failures = []
    if requires_four_eyes and approval_state != "approved":
        approval_failures.append(
            {
                "gate": "four_eyes_approval",
                "reason": "approval_required_before_release",
                "approval_state": approval_state,
            }
        )

    duplicate_failures = []
    if duplicate_matches:
        duplicate_failures.append(
            {
                "gate": "duplicate_window",
                "reason": "duplicate_trade_capture_detected",
                "matches": tuple(duplicate_matches),
                "window_minutes": window_minutes,
            }
        )

    safety_case_checks = (
        {"gate": "book", "passed": not _missing(payload.get("book"))},
        {"gate": "strategy", "passed": not _missing(payload.get("strategy"))},
        {"gate": "side", "passed": side in _VALID_SIDES},
        {"gate": "volume_mwh", "passed": volume_mwh is not None and volume_mwh > 0},
        {"gate": "pricing_formula", "passed": not _missing(payload.get("pricing_formula"))},
        {"gate": "delivery_profile", "passed": not _missing(payload.get("delivery_profile"))},
        {"gate": "position_type", "passed": position_type in _VALID_POSITION_TYPES},
        {"gate": "counterparty", "passed": not _missing(payload.get("counterparty"))},
    )

    failures = tuple(market_curve_failures + limit_breaches + approval_failures + duplicate_failures)
    reference_data_ok = not missing_fields and not invalid_fields
    release_ready = reference_data_ok and not failures
    if not reference_data_ok:
        lifecycle_state = "draft"
        status = "release_blocked"
        status_badge = "Draft"
    elif release_ready:
        lifecycle_state = "risk_passed"
        status = "risk_passed"
        status_badge = "Risk Passed"
    else:
        lifecycle_state = "exception_open"
        status = "release_blocked"
        status_badge = "Exception"

    remediation = tuple(
        [f"Populate missing field: {field}" for field in missing_fields]
        + [f"Correct invalid field: {field}" for field in invalid_fields]
        + [f"Clear gate: {item['gate']}" for item in failures]
    )

    return {
        "ok": True,
        "required_fields": required_fields,
        "missing_fields": missing_fields,
        "invalid_fields": tuple(invalid_fields),
        "safety_case_checks": safety_case_checks,
        "market_curve_failures": tuple(market_curve_failures),
        "limit_breaches": tuple(limit_breaches),
        "approval_failures": tuple(approval_failures),
        "duplicate_failures": tuple(duplicate_failures),
        "release_ready": release_ready,
        "lifecycle_state": lifecycle_state,
        "status": status,
        "status_badge": status_badge,
        "bucket_key": bucket_key,
        "signed_volume_mwh": round(signed_volume_mwh, 4),
        "current_bucket_volume_mwh": round(current_bucket_volume, 4),
        "candidate_bucket_volume_mwh": round(candidate_bucket_volume, 4),
        "projected_mark_to_market": projected_mtm,
        "market_curve_id": curve_record.get("id") if curve_record else None,
        "market_curve_price": mark_price,
        "curve_age_hours": curve_age_hours,
        "trade_signature": signature,
        "duplicate_matches": tuple(duplicate_matches),
        "requires_four_eyes_approval": requires_four_eyes,
        "actionable_remediation": remediation,
        "workbench_queue": "ready_for_release" if release_ready else "trade_exceptions",
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }



def build_trade_record(payload: dict | None, validation: dict, record_id: str, version: int = 1) -> dict:
    payload = dict(payload or {})
    return {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "status": validation["status"],
        "status_badge": validation["status_badge"],
        "version": version,
        "lifecycle_state": validation["lifecycle_state"],
        "bucket_key": validation["bucket_key"],
        "signed_volume_mwh": validation["signed_volume_mwh"],
        "projected_mark_to_market": validation["projected_mark_to_market"],
        "release_ready": validation["release_ready"],
        "trade_signature": validation["trade_signature"],
        "validation": validation,
        "actionable_remediation": validation["actionable_remediation"],
        "workbench_queue": validation["workbench_queue"],
        "payload": payload,
    }



def evaluate_nomination_submission(payload: dict | None, existing_records=(), trade_records=(), parameters=None, rules=None):
    payload = dict(payload or {})
    parameter_values = {
        name: item["value"] for name, item in (parameters or default_runtime_parameters()).items()
    }
    defaults = default_policy_rules()
    rule_values = dict(defaults)
    rule_values.update(rules or {})

    required_fields = ("trade_id", "delivery_period", "interval_start", "interval_end", "volume_mwh", "submitted_at", "operator")
    missing_fields = tuple(field for field in required_fields if _missing(payload.get(field)))
    invalid_fields = []
    volume_mwh = _number(payload.get("volume_mwh"))
    if volume_mwh is None or volume_mwh <= 0:
        invalid_fields.append("volume_mwh")
    submitted_at = _parse_timestamp(payload.get("submitted_at"))
    if payload.get("submitted_at") and submitted_at is None:
        invalid_fields.append("submitted_at")

    cutoff_hour = int(parameter_values["nomination_cutoff_hour_utc"])
    cutoff_failures = []
    if submitted_at is not None and submitted_at.hour >= cutoff_hour:
        cutoff_failures.append(
            {
                "gate": "nomination_cutoff",
                "reason": "submitted_after_cutoff",
                "cutoff_hour_utc": cutoff_hour,
            }
        )

    trade = next((record for record in trade_records if record.get("id") == payload.get("trade_id")), None)
    trade_payload = dict(trade.get("payload", {})) if trade else {}
    trade_volume = abs(float(trade.get("signed_volume_mwh", 0.0))) if trade else None
    tolerance = float(parameter_values["nomination_tolerance_mwh"])
    trade_failures = []
    if trade is None:
        trade_failures.append({"gate": "trade_reference", "reason": "unknown_trade"})
    elif volume_mwh is not None and trade_volume is not None and volume_mwh > trade_volume + tolerance:
        trade_failures.append(
            {
                "gate": "nomination_vs_trade_volume",
                "reason": "nomination_exceeds_trade_volume",
                "trade_volume_mwh": trade_volume,
                "nomination_volume_mwh": volume_mwh,
            }
        )

    existing_versions = [record for record in existing_records if record.get("payload", {}).get("trade_id") == payload.get("trade_id")]
    version = len(existing_versions) + 1
    supersedes_id = existing_versions[-1]["id"] if existing_versions else None
    failures = tuple(cutoff_failures + trade_failures)
    accepted = not missing_fields and not invalid_fields and not failures
    status = "accepted" if accepted else "exception"
    lifecycle_state = "submitted" if accepted else "post_cutoff_exception"
    return {
        "ok": True,
        "missing_fields": missing_fields,
        "invalid_fields": tuple(invalid_fields),
        "cutoff_failures": tuple(cutoff_failures),
        "trade_failures": tuple(trade_failures),
        "accepted": accepted,
        "status": status,
        "lifecycle_state": lifecycle_state,
        "version": version,
        "supersedes_id": supersedes_id,
        "trade_delivery_period": derive_delivery_period(trade_payload) if trade_payload else None,
        "actionable_remediation": tuple(
            [f"Populate missing field: {field}" for field in missing_fields]
            + [f"Correct invalid field: {field}" for field in invalid_fields]
            + [f"Clear gate: {item['gate']}" for item in failures]
        ),
        "workbench_queue": "nominations_ready" if accepted else "nomination_exceptions",
        "side_effects": (),
    }



def build_nomination_record(payload: dict | None, validation: dict, record_id: str) -> dict:
    payload = dict(payload or {})
    return {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "status": validation["status"],
        "lifecycle_state": validation["lifecycle_state"],
        "version": validation["version"],
        "supersedes_id": validation["supersedes_id"],
        "workbench_queue": validation["workbench_queue"],
        "actionable_remediation": validation["actionable_remediation"],
        "validation": validation,
        "payload": payload,
    }



def evaluate_schedule_submission(payload: dict | None, nomination_records=(), parameters=None):
    payload = dict(payload or {})
    parameter_values = {
        name: item["value"] for name, item in (parameters or default_runtime_parameters()).items()
    }
    required_fields = ("nomination_id", "trade_id", "delivery_period", "scheduled_volume_mwh", "path_status", "submitted_at")
    missing_fields = tuple(field for field in required_fields if _missing(payload.get(field)))
    invalid_fields = []
    scheduled_volume_mwh = _number(payload.get("scheduled_volume_mwh"))
    if scheduled_volume_mwh is None or scheduled_volume_mwh <= 0:
        invalid_fields.append("scheduled_volume_mwh")
    nomination = next((record for record in nomination_records if record.get("id") == payload.get("nomination_id")), None)
    nomination_payload = dict(nomination.get("payload", {})) if nomination else {}
    nomination_volume = _number(nomination_payload.get("volume_mwh"))
    tolerance = float(parameter_values["nomination_tolerance_mwh"])
    failures = []
    if nomination is None:
        failures.append({"gate": "nomination_reference", "reason": "unknown_nomination"})
    elif nomination_volume is not None and scheduled_volume_mwh is not None and scheduled_volume_mwh > nomination_volume + tolerance:
        failures.append(
            {
                "gate": "schedule_vs_nomination",
                "reason": "scheduled_volume_exceeds_nomination",
                "scheduled_volume_mwh": scheduled_volume_mwh,
                "nomination_volume_mwh": nomination_volume,
            }
        )
    accepted = not missing_fields and not invalid_fields and not failures
    return {
        "ok": True,
        "missing_fields": missing_fields,
        "invalid_fields": tuple(invalid_fields),
        "failures": tuple(failures),
        "accepted": accepted,
        "status": "scheduled" if accepted else "exception",
        "lifecycle_state": "scheduled" if accepted else "schedule_exception",
        "actionable_remediation": tuple(
            [f"Populate missing field: {field}" for field in missing_fields]
            + [f"Correct invalid field: {field}" for field in invalid_fields]
            + [f"Clear gate: {item['gate']}" for item in failures]
        ),
        "workbench_queue": "schedule_ready" if accepted else "schedule_exceptions",
        "side_effects": (),
    }



def build_schedule_record(payload: dict | None, validation: dict, record_id: str) -> dict:
    payload = dict(payload or {})
    return {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "status": validation["status"],
        "lifecycle_state": validation["lifecycle_state"],
        "workbench_queue": validation["workbench_queue"],
        "actionable_remediation": validation["actionable_remediation"],
        "validation": validation,
        "payload": payload,
    }



def evaluate_price_curve_submission(payload: dict | None, parameters=None, rules=None):
    payload = dict(payload or {})
    parameter_values = {
        name: item["value"] for name, item in (parameters or default_runtime_parameters()).items()
    }
    defaults = default_policy_rules()
    rule_values = dict(defaults)
    rule_values.update(rules or {})
    curve_policy = dict(defaults["price_curve_policy"])
    curve_policy.update(rule_values.get("price_curve_policy", {}))
    required_fields = ("commodity", "market_hub", "delivery_period", "strip_start", "strip_end", "curve_price", "as_of", "source_name")
    missing_fields = tuple(field for field in required_fields if _missing(payload.get(field)))
    invalid_fields = []
    curve_price = _number(payload.get("curve_price"))
    if curve_price is None:
        invalid_fields.append("curve_price")
    as_of = _parse_timestamp(payload.get("as_of"))
    if payload.get("as_of") and as_of is None:
        invalid_fields.append("as_of")

    failures = []
    if curve_price is not None:
        if curve_price < float(curve_policy["min_curve_price"]):
            failures.append({"gate": "curve_floor", "reason": "curve_price_below_floor", "curve_price": curve_price})
        if curve_price > float(curve_policy["max_curve_price"]):
            failures.append({"gate": "curve_ceiling", "reason": "curve_price_above_ceiling", "curve_price": curve_price})
    if as_of is not None:
        reference_time = _parse_timestamp(payload.get("received_at") or payload.get("evaluation_time")) or as_of
        age_hours = round((reference_time - as_of).total_seconds() / 3600, 2)
    else:
        age_hours = None
    if age_hours is not None and age_hours > float(parameter_values["curve_max_age_hours"]):
        failures.append({"gate": "curve_freshness", "reason": "curve_is_stale", "age_hours": age_hours})

    accepted = not missing_fields and not invalid_fields and not failures
    return {
        "ok": True,
        "missing_fields": missing_fields,
        "invalid_fields": tuple(invalid_fields),
        "failures": tuple(failures),
        "accepted": accepted,
        "status": "published" if accepted else "curve_exception",
        "quality_state": "fresh" if accepted else "stale_or_invalid",
        "actionable_remediation": tuple(
            [f"Populate missing field: {field}" for field in missing_fields]
            + [f"Correct invalid field: {field}" for field in invalid_fields]
            + [f"Clear gate: {item['gate']}" for item in failures]
        ),
        "workbench_queue": "curve_ready" if accepted else "curve_exceptions",
        "side_effects": (),
    }



def build_price_curve_record(payload: dict | None, validation: dict, record_id: str) -> dict:
    payload = dict(payload or {})
    return {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "status": validation["status"],
        "quality_state": validation["quality_state"],
        "workbench_queue": validation["workbench_queue"],
        "actionable_remediation": validation["actionable_remediation"],
        "validation": validation,
        "payload": payload,
    }



def build_exposure_limit_record(payload: dict | None, record_id: str) -> dict:
    payload = dict(payload or {})
    return {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "status": "active",
        "lifecycle_state": "effective",
        "workbench_queue": "limits_ready",
        "payload": payload,
        "validation": {"ok": True, "severity": payload.get("severity", "hard_stop")},
        "actionable_remediation": (),
    }



def build_settlement_record(payload: dict | None, record_id: str, trade_records=()) -> dict:
    payload = dict(payload or {})
    trade = next((record for record in trade_records if record.get("id") == payload.get("trade_id")), None)
    trade_payload = dict(trade.get("payload", {})) if trade else {}
    realized_volume = _number(payload.get("realized_volume_mwh")) or 0.0
    realized_price = _number(payload.get("realized_price")) or 0.0
    fixed_price = _number(trade_payload.get("fixed_price")) or 0.0
    side = str(trade_payload.get("side", "BUY")).strip().upper() or "BUY"
    pnl = round(signed_volume(realized_volume, side) * (realized_price - fixed_price), 2)
    return {
        "id": record_id,
        "tenant": payload.get("tenant", "default"),
        "status": "settled" if trade else "exception",
        "lifecycle_state": "settled" if trade else "settlement_exception",
        "workbench_queue": "settlements_ready" if trade else "settlement_exceptions",
        "realized_pnl": pnl,
        "validation": {"trade_found": trade is not None, "realized_pnl": pnl},
        "actionable_remediation": () if trade else ("Reference a known trade before settlement.",),
        "payload": payload,
    }



def build_workbench_summary(trade_records=(), nomination_records=(), schedule_records=(), settlement_records=(), curve_records=(), limit_records=()):
    trade_records = tuple(trade_records)
    nomination_records = tuple(nomination_records)
    schedule_records = tuple(schedule_records)
    settlement_records = tuple(settlement_records)
    curve_records = tuple(curve_records)
    limit_records = tuple(limit_records)
    exposure_buckets = build_exposure_buckets(trade_records)
    return {
        "total_trades": len(trade_records),
        "ready_trades": sum(1 for record in trade_records if record.get("status") == "risk_passed"),
        "blocked_trades": sum(1 for record in trade_records if record.get("status") == "release_blocked"),
        "nomination_exceptions": sum(1 for record in nomination_records if record.get("status") == "exception"),
        "schedule_exceptions": sum(1 for record in schedule_records if record.get("status") == "exception"),
        "stale_curves": sum(1 for record in curve_records if record.get("quality_state") != "fresh"),
        "active_limits": sum(1 for record in limit_records if record.get("status") == "active"),
        "realized_pnl_total": round(sum(float(record.get("realized_pnl", 0.0)) for record in settlement_records), 2),
        "net_exposure_buckets": exposure_buckets,
        "top_exception_ids": tuple(
            record.get("id")
            for record in list(trade_records) + list(nomination_records) + list(schedule_records)
            if record.get("status") in {"release_blocked", "exception"}
        )[:5],
    }
