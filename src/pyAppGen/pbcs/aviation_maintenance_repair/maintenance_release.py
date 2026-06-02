"""Executable maintenance release governance for aviation MRO.

The functions here are deterministic and side-effect-free. Runtime command
functions can persist their returned evidence inside the PBC-owned state, but
this module does not mutate external maintenance, inventory, dispatch, or audit
systems.
"""
from __future__ import annotations

from datetime import date
from typing import Mapping, Sequence

PBC_KEY = "aviation_maintenance_repair"
EVENT_CONTRACT = "AppGen-X"

RELEASE_CHECKS = (
    "work_cards_closed",
    "duplicate_inspections_complete",
    "technicians_authorized",
    "controlled_tools_valid",
    "consumables_within_life",
    "components_airworthy",
    "deferred_defects_within_limits",
    "airworthiness_directives_complied",
    "human_certifier_present",
)


def _today(value: object | None) -> date:
    if value is None:
        return date.today()
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _tupled(value: object) -> tuple:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    if isinstance(value, (list, set)):
        return tuple(value)
    return (value,)


def _blocker(code: str, message: str, evidence: Mapping[str, object]) -> dict:
    return {"code": code, "message": message, "evidence": dict(evidence)}


def evaluate_component_installation(component: Mapping[str, object], aircraft: Mapping[str, object] | None = None, *, as_of: object | None = None) -> dict:
    """Evaluate whether a component can be installed or remain released."""

    component = dict(component or {})
    aircraft = dict(aircraft or {})
    as_of_date = _today(as_of)
    blockers = []

    remaining_cycles = component.get("remaining_cycles")
    remaining_hours = component.get("remaining_hours")
    if remaining_cycles is not None and int(remaining_cycles) <= 0:
        blockers.append(_blocker("life_limit_cycles_exhausted", "Component has no remaining cycle life.", {"remaining_cycles": remaining_cycles}))
    if remaining_hours is not None and float(remaining_hours) <= 0:
        blockers.append(_blocker("life_limit_hours_exhausted", "Component has no remaining hour life.", {"remaining_hours": remaining_hours}))

    if component.get("quarantine_state") in {"active", "hold", "suspect", "quarantined"}:
        blockers.append(_blocker("component_quarantined", "Quarantined or suspect material cannot be released.", {"quarantine_state": component.get("quarantine_state")}))
    if not component.get("release_certificate"):
        blockers.append(_blocker("missing_release_certificate", "Installation requires authorized release certificate evidence.", {"component_id": component.get("component_id")}))

    expiry = component.get("shelf_life_expiry") or component.get("certification_expiry")
    if expiry and _today(expiry) < as_of_date:
        blockers.append(_blocker("component_evidence_expired", "Component evidence or shelf life has expired.", {"expiry": str(expiry), "as_of": as_of_date.isoformat()}))

    effectivity = set(_tupled(component.get("effectivity_aircraft_types")) + _tupled(component.get("effectivity_tail_numbers")))
    aircraft_markers = {aircraft.get("aircraft_type"), aircraft.get("tail_number"), aircraft.get("fleet_subtype")}
    aircraft_markers.discard(None)
    if effectivity and not effectivity.intersection(aircraft_markers):
        blockers.append(_blocker("component_not_effective_for_aircraft", "Component effectivity does not cover the aircraft.", {"effectivity": tuple(sorted(effectivity)), "aircraft": tuple(sorted(aircraft_markers))}))

    return {
        "ok": not blockers,
        "pbc": PBC_KEY,
        "component_id": component.get("component_id") or component.get("serial_number"),
        "status": "eligible" if not blockers else "blocked",
        "blockers": tuple(blockers),
        "remaining_life": {
            "hours": remaining_hours,
            "cycles": remaining_cycles,
            "calendar_expiry": expiry,
        },
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def evaluate_work_card_closeout(work_card: Mapping[str, object], technician_authorizations: Sequence[Mapping[str, object]], *, as_of: object | None = None) -> dict:
    """Evaluate work-card closeout, signatures, tooling, and consumables."""

    card = dict(work_card or {})
    as_of_date = _today(as_of)
    signoffs = tuple(dict(item) for item in _tupled(card.get("signoffs")))
    authorization_index = {
        (auth.get("technician_id"), auth.get("task_family"), auth.get("aircraft_type")): dict(auth)
        for auth in technician_authorizations
    }
    blockers = []

    required_roles = tuple(card.get("required_signoff_roles") or ("performer",))
    signed_roles = {item.get("role") for item in signoffs}
    missing_roles = tuple(role for role in required_roles if role not in signed_roles)
    if card.get("status", "open") not in {"closed", "signed", "complete"}:
        blockers.append(_blocker("work_card_not_closed", "Work card must be closed before release.", {"status": card.get("status")}))
    if missing_roles:
        blockers.append(_blocker("missing_required_signoff", "Work card is missing required signoff roles.", {"missing_roles": missing_roles}))

    performer = next((item for item in signoffs if item.get("role") == "performer"), None)
    inspector = next((item for item in signoffs if item.get("role") in {"inspector", "duplicate_inspector"}), None)
    if card.get("duplicate_inspection_required"):
        if not inspector:
            blockers.append(_blocker("duplicate_inspection_missing", "Duplicate inspection is required before release.", {"work_card_id": card.get("work_card_id")}))
        elif performer and performer.get("technician_id") == inspector.get("technician_id"):
            blockers.append(_blocker("self_inspection_blocked", "Duplicate inspection cannot be self-certified.", {"technician_id": performer.get("technician_id")}))

    for signoff in signoffs:
        key = (signoff.get("technician_id"), card.get("task_family"), card.get("aircraft_type"))
        auth = authorization_index.get(key)
        valid_to = auth.get("valid_to") if auth else None
        if not auth:
            blockers.append(_blocker("technician_not_authorized", "Signoff technician lacks matching task and type authorization.", {"technician_id": signoff.get("technician_id"), "task_family": card.get("task_family"), "aircraft_type": card.get("aircraft_type")}))
        elif valid_to and _today(valid_to) < as_of_date:
            blockers.append(_blocker("technician_authorization_expired", "Technician authorization expired before signoff.", {"technician_id": signoff.get("technician_id"), "valid_to": valid_to}))

    for tool in _tupled(card.get("controlled_tools")):
        tool = dict(tool)
        if not tool.get("returned"):
            blockers.append(_blocker("controlled_tool_not_returned", "Controlled tooling must be returned before release.", {"tool_id": tool.get("tool_id")}))
        if tool.get("calibration_due") and _today(tool["calibration_due"]) < as_of_date:
            blockers.append(_blocker("tool_calibration_expired", "Controlled tool calibration expired before use.", {"tool_id": tool.get("tool_id"), "calibration_due": tool.get("calibration_due")}))

    for consumable in _tupled(card.get("consumables")):
        consumable = dict(consumable)
        if consumable.get("expiry") and _today(consumable["expiry"]) < as_of_date:
            blockers.append(_blocker("consumable_expired", "Consumable batch was outside allowed life.", {"batch_id": consumable.get("batch_id"), "expiry": consumable.get("expiry")}))
        if consumable.get("mix_life_expired"):
            blockers.append(_blocker("consumable_mix_life_expired", "Mixed consumable exceeded mix-life before use.", {"batch_id": consumable.get("batch_id")}))

    if card.get("open_non_routine_count", 0):
        blockers.append(_blocker("open_non_routine_work", "Originating non-routine work remains open.", {"open_non_routine_count": card.get("open_non_routine_count")}))

    return {
        "ok": not blockers,
        "pbc": PBC_KEY,
        "work_card_id": card.get("work_card_id") or card.get("id"),
        "status": "closed" if not blockers else "blocked",
        "blockers": tuple(blockers),
        "required_roles": required_roles,
        "signed_roles": tuple(sorted(role for role in signed_roles if role)),
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def build_release_to_service_pack(payload: Mapping[str, object], *, as_of: object | None = None) -> dict:
    """Assemble release evidence and decide whether release is allowed."""

    source = dict(payload or {})
    as_of_date = _today(as_of or source.get("as_of"))
    aircraft = dict(source.get("aircraft") or {})
    authorizations = tuple(dict(item) for item in _tupled(source.get("technician_authorizations")))
    blockers = []
    passed = []

    if not aircraft:
        blockers.append(_blocker("missing_aircraft", "Release pack requires an aircraft selection.", {"release_id": source.get("release_id")}))

    work_card_results = tuple(
        evaluate_work_card_closeout(card, authorizations, as_of=as_of_date)
        for card in _tupled(source.get("work_cards"))
    )
    if work_card_results and all(result["ok"] for result in work_card_results):
        passed.extend(("work_cards_closed", "duplicate_inspections_complete", "technicians_authorized", "controlled_tools_valid", "consumables_within_life"))
    else:
        for result in work_card_results:
            blockers.extend(result["blockers"])
        if not work_card_results:
            blockers.append(_blocker("no_work_cards_in_release_pack", "Release pack requires at least one closed work card.", {"tail_number": aircraft.get("tail_number")}))

    component_results = tuple(
        evaluate_component_installation(component, aircraft, as_of=as_of_date)
        for component in _tupled(source.get("components"))
    )
    if all(result["ok"] for result in component_results):
        passed.append("components_airworthy")
    else:
        for result in component_results:
            blockers.extend(result["blockers"])

    deferred_defects = tuple(dict(item) for item in _tupled(source.get("deferred_defects")))
    expired_defects = tuple(
        defect for defect in deferred_defects
        if defect.get("status", "open") in {"open", "deferred"} and defect.get("expiry_date") and _today(defect["expiry_date"]) < as_of_date
    )
    if not expired_defects:
        passed.append("deferred_defects_within_limits")
    else:
        blockers.append(_blocker("deferred_defect_expired", "Deferred defect has exceeded its approved interval.", {"defect_ids": tuple(defect.get("defect_id") for defect in expired_defects)}))

    ad_items = tuple(dict(item) for item in _tupled(source.get("airworthiness_directives")))
    open_ads = tuple(item for item in ad_items if item.get("applicable", True) and item.get("status") not in {"complied", "terminated", "not_applicable"})
    if not open_ads:
        passed.append("airworthiness_directives_complied")
    else:
        blockers.append(_blocker("airworthiness_directive_open", "Applicable airworthiness directive still lacks compliance evidence.", {"ad_ids": tuple(item.get("ad_id") for item in open_ads)}))

    certifier = dict(source.get("certifier") or {})
    if certifier.get("technician_id") and certifier.get("release_authorization"):
        passed.append("human_certifier_present")
    else:
        blockers.append(_blocker("human_certifier_required", "Release-to-service requires a human certifier with release authorization.", {"certifier": certifier.get("technician_id")}))

    passed = tuple(check for check in RELEASE_CHECKS if check in set(passed))
    readiness_score = round(len(passed) / len(RELEASE_CHECKS), 2)
    return {
        "ok": not blockers,
        "pbc": PBC_KEY,
        "release_id": source.get("release_id") or f"release-{aircraft.get('tail_number', 'unknown')}",
        "tail_number": aircraft.get("tail_number"),
        "status": "release_ready" if not blockers else "blocked",
        "readiness_score": readiness_score,
        "passed_checks": passed,
        "pending_checks": tuple(check for check in RELEASE_CHECKS if check not in set(passed)),
        "blockers": tuple(blockers),
        "work_card_results": work_card_results,
        "component_results": component_results,
        "certifier": certifier,
        "summary": {
            "blocker_count": len(blockers),
            "passed_count": len(passed),
            "pending_count": len(RELEASE_CHECKS) - len(passed),
        },
        "event_contract": EVENT_CONTRACT,
        "side_effects": (),
    }


def maintenance_release_evidence() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "implemented_backlog_items": (
            "component_life_limit_tracking",
            "parts_traceability_pack",
            "quarantine_lockout",
            "work_card_duplicate_inspection",
            "technician_authorization_matrix",
            "tooling_calibration_lockout",
            "consumable_shelf_life_checks",
            "deferred_defect_countdown",
            "airworthiness_directive_compliance",
            "release_to_service_pack",
            "agent_release_guardrails",
        ),
        "event_contract": EVENT_CONTRACT,
        "shared_table_access": False,
        "side_effects": (),
    }
