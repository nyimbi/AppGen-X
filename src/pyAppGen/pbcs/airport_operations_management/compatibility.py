"""Gate and stand compatibility rules for airport operations management."""
from __future__ import annotations

from typing import Iterable, Mapping

PBC_KEY = "airport_operations_management"

_DECISION_PRIORITY = {"usable": 3, "conditional": 2, "blocked": 1}
_WINGSPAN_ORDER = {code: index for index, code in enumerate(("A", "B", "C", "D", "E", "F"), start=1)}

DEFAULT_STAND_CATALOG = (
    {
        "stand_code": "A1",
        "gate_code": "A1",
        "stand_type": "contact",
        "supported_aircraft_families": ("regional", "narrowbody"),
        "max_wingspan_code": "C",
        "international_capable": False,
        "bussing_supported": False,
        "hydrant_fuel": True,
        "ground_power": True,
        "preconditioned_air": True,
        "adjacent_shadow_stands": (),
        "active": True,
    },
    {
        "stand_code": "B7",
        "gate_code": "B7",
        "stand_type": "contact",
        "supported_aircraft_families": ("narrowbody", "widebody"),
        "max_wingspan_code": "E",
        "international_capable": True,
        "bussing_supported": False,
        "hydrant_fuel": True,
        "ground_power": True,
        "preconditioned_air": True,
        "adjacent_shadow_stands": ("B6", "B8"),
        "active": True,
    },
    {
        "stand_code": "R2",
        "gate_code": "R2",
        "stand_type": "remote",
        "supported_aircraft_families": ("regional", "narrowbody"),
        "max_wingspan_code": "C",
        "international_capable": False,
        "bussing_supported": True,
        "hydrant_fuel": False,
        "ground_power": True,
        "preconditioned_air": False,
        "adjacent_shadow_stands": (),
        "active": True,
    },
)


def _as_tuple(value: object) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, str):
        return (value,)
    return tuple(value)


def _rank_wingspan(code: object) -> int:
    return _WINGSPAN_ORDER.get(str(code or "").upper(), 0)


def _reason(code: str, severity: str, **details: object) -> dict:
    return {"code": code, "severity": severity, "details": details}


def _normalize_request(request: Mapping[str, object] | None) -> dict:
    payload = dict(request or {})
    return {
        "flight_number": payload.get("flight_number", "UNKNOWN"),
        "aircraft_family": payload.get("aircraft_family", "narrowbody"),
        "wingspan_code": str(payload.get("wingspan_code", "C")).upper(),
        "operation_type": payload.get("operation_type", "domestic"),
        "requires_hydrant_fuel": bool(payload.get("requires_hydrant_fuel", False)),
        "requires_ground_power": bool(payload.get("requires_ground_power", False)),
        "requires_preconditioned_air": bool(payload.get("requires_preconditioned_air", False)),
        "requires_contact_stand": bool(payload.get("requires_contact_stand", False)),
        "prefers_contact_stand": bool(payload.get("prefers_contact_stand", True)),
        "adjacent_occupied_stands": _as_tuple(payload.get("adjacent_occupied_stands")),
    }


def _normalize_stand(stand: Mapping[str, object]) -> dict:
    payload = dict(stand)
    return {
        "stand_code": payload.get("stand_code", "UNKNOWN"),
        "gate_code": payload.get("gate_code", payload.get("stand_code", "UNKNOWN")),
        "stand_type": payload.get("stand_type", "contact"),
        "supported_aircraft_families": _as_tuple(
            payload.get("supported_aircraft_families", ("narrowbody",))
        ),
        "max_wingspan_code": str(payload.get("max_wingspan_code", "C")).upper(),
        "international_capable": bool(payload.get("international_capable", False)),
        "bussing_supported": bool(payload.get("bussing_supported", False)),
        "hydrant_fuel": bool(payload.get("hydrant_fuel", False)),
        "ground_power": bool(payload.get("ground_power", False)),
        "preconditioned_air": bool(payload.get("preconditioned_air", False)),
        "adjacent_shadow_stands": _as_tuple(payload.get("adjacent_shadow_stands")),
        "active": bool(payload.get("active", True)),
    }


def evaluate_stand_compatibility(
    request: Mapping[str, object] | None,
    stand: Mapping[str, object],
    occupied_stands: Iterable[str] = (),
) -> dict:
    normalized_request = _normalize_request(request)
    normalized_stand = _normalize_stand(stand)
    occupied = tuple(str(item) for item in occupied_stands) + normalized_request["adjacent_occupied_stands"]
    reasons = []
    warnings = []

    if not normalized_stand["active"]:
        reasons.append(_reason("stand_inactive", "blocking"))
    if normalized_request["aircraft_family"] not in normalized_stand["supported_aircraft_families"]:
        reasons.append(
            _reason(
                "aircraft_family_not_supported",
                "blocking",
                aircraft_family=normalized_request["aircraft_family"],
            )
        )
    if _rank_wingspan(normalized_request["wingspan_code"]) > _rank_wingspan(
        normalized_stand["max_wingspan_code"]
    ):
        reasons.append(
            _reason(
                "wingspan_code_exceeds_stand_limit",
                "blocking",
                requested=normalized_request["wingspan_code"],
                allowed=normalized_stand["max_wingspan_code"],
            )
        )
    if (
        normalized_request["operation_type"] == "international"
        and not normalized_stand["international_capable"]
    ):
        reasons.append(_reason("international_arrival_requires_border_capable_stand", "blocking"))
    if normalized_request["requires_contact_stand"] and normalized_stand["stand_type"] != "contact":
        reasons.append(_reason("contact_stand_required", "blocking"))
    if normalized_request["requires_hydrant_fuel"] and not normalized_stand["hydrant_fuel"]:
        reasons.append(_reason("hydrant_fuel_required", "blocking"))
    if normalized_request["requires_ground_power"] and not normalized_stand["ground_power"]:
        reasons.append(_reason("ground_power_required", "blocking"))
    if normalized_request["requires_preconditioned_air"] and not normalized_stand["preconditioned_air"]:
        reasons.append(_reason("preconditioned_air_required", "blocking"))

    shadow_conflicts = tuple(
        stand_code
        for stand_code in normalized_stand["adjacent_shadow_stands"]
        if stand_code in occupied
    )
    if shadow_conflicts:
        reasons.append(
            _reason(
                "adjacent_shadow_conflict",
                "blocking",
                conflicting_stands=shadow_conflicts,
            )
        )

    if normalized_stand["stand_type"] == "remote":
        if not normalized_stand["bussing_supported"]:
            reasons.append(_reason("remote_stand_missing_bussing_support", "blocking"))
        else:
            warnings.append(_reason("remote_transfer_required", "conditional"))
    elif normalized_request["prefers_contact_stand"]:
        warnings.append(_reason("contact_stand_preference_satisfied", "info"))

    decision = "blocked"
    if not reasons:
        decision = "conditional" if any(item["severity"] == "conditional" for item in warnings) else "usable"

    score = (
        _DECISION_PRIORITY[decision] * 100
        - len(reasons) * 25
        - len(warnings) * 5
        + (10 if normalized_stand["stand_type"] == "contact" else 0)
        + (5 if normalized_stand["international_capable"] else 0)
    )
    return {
        "stand_code": normalized_stand["stand_code"],
        "gate_code": normalized_stand["gate_code"],
        "stand_type": normalized_stand["stand_type"],
        "decision": decision,
        "compatible": decision != "blocked",
        "score": score,
        "reason_codes": tuple(item["code"] for item in reasons),
        "warning_codes": tuple(item["code"] for item in warnings),
        "reasons": tuple(reasons),
        "warnings": tuple(warnings),
        "event_contract": "AppGen-X",
    }


def build_gate_assignment_compatibility_matrix(
    request: Mapping[str, object] | None,
    stands: Iterable[Mapping[str, object]] | None = None,
    occupied_stands: Iterable[str] = (),
) -> dict:
    normalized_request = _normalize_request(request)
    candidates = tuple(stands or DEFAULT_STAND_CATALOG)
    assessments = tuple(
        sorted(
            (
                evaluate_stand_compatibility(normalized_request, stand, occupied_stands)
                for stand in candidates
            ),
            key=lambda item: (
                -_DECISION_PRIORITY[item["decision"]],
                -item["score"],
                item["stand_code"],
            ),
        )
    )
    recommended = next((item for item in assessments if item["compatible"]), None)
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "request": normalized_request,
        "assessments": assessments,
        "recommended_option": recommended,
        "summary": {
            "usable": sum(1 for item in assessments if item["decision"] == "usable"),
            "conditional": sum(1 for item in assessments if item["decision"] == "conditional"),
            "blocked": sum(1 for item in assessments if item["decision"] == "blocked"),
        },
        "event_contract": "AppGen-X",
    }


def build_gate_assignment_decision(
    request: Mapping[str, object] | None,
    stands: Iterable[Mapping[str, object]] | None = None,
    occupied_stands: Iterable[str] = (),
) -> dict:
    matrix = build_gate_assignment_compatibility_matrix(request, stands, occupied_stands)
    recommended = matrix["recommended_option"]
    if recommended is None:
        return {
            "ok": False,
            "pbc": PBC_KEY,
            "reason": "no_compatible_stand",
            "request": matrix["request"],
            "compatibility_matrix": matrix,
            "event_contract": "AppGen-X",
        }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "request": matrix["request"],
        "recommended_option": recommended,
        "compatibility_matrix": matrix,
        "event_contract": "AppGen-X",
    }


def explain_gate_assignment_decision(
    request: Mapping[str, object] | None,
    stands: Iterable[Mapping[str, object]] | None = None,
    occupied_stands: Iterable[str] = (),
) -> dict:
    decision = build_gate_assignment_decision(request, stands, occupied_stands)
    if not decision["ok"]:
        blocked = decision["compatibility_matrix"]["assessments"]
        return {
            "ok": True,
            "pbc": PBC_KEY,
            "summary": "No stand can safely accept the requested flight profile.",
            "recommendation": None,
            "blocked_options": blocked,
            "event_contract": "AppGen-X",
        }

    recommendation = decision["recommended_option"]
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "summary": (
            f"Recommend stand {recommendation['stand_code']} via gate {recommendation['gate_code']} "
            f"with decision state {recommendation['decision']}."
        ),
        "recommendation": recommendation,
        "blocked_options": tuple(
            item
            for item in decision["compatibility_matrix"]["assessments"]
            if item["decision"] == "blocked"
        ),
        "event_contract": "AppGen-X",
    }
