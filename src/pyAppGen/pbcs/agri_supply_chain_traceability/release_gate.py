"""Release readiness checks for agricultural traceability flows."""
from __future__ import annotations

from datetime import date


RELEASE_GATE_CHECKS = (
    "farm_lot_active",
    "provenance_complete",
    "certification_covered",
    "storage_clear",
    "transport_clear",
    "no_active_recall",
    "quality_holds_cleared",
)


def _tupled(value):
    if value is None:
        return ()
    if isinstance(value, (list, tuple, set)):
        return tuple(item for item in value if item not in (None, ""))
    return (value,)


def _parse_iso_date(value):
    if not value:
        return None
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _record_payload(record):
    return dict(record.get("payload") or {})


def _candidate_subject_ids(candidate):
    return tuple(
        dict.fromkeys(
            _tupled(candidate.get("candidate_id"))
            + _tupled(candidate.get("shipment_id"))
            + _tupled(candidate.get("batch_id"))
            + _tupled(candidate.get("batch_ids"))
            + _tupled(candidate.get("subject_id"))
            + _tupled(candidate.get("subject_ids"))
        )
    )


def _record_subject_ids(record):
    payload = _record_payload(record)
    return tuple(
        dict.fromkeys(
            _tupled(payload.get("subject_id"))
            + _tupled(payload.get("subject_ids"))
            + _tupled(payload.get("shipment_id"))
            + _tupled(payload.get("shipment_ids"))
            + _tupled(payload.get("batch_id"))
            + _tupled(payload.get("batch_ids"))
            + _tupled(payload.get("release_candidate_id"))
            + _tupled(payload.get("release_candidate_ids"))
        )
    )


def _record_farm_lot_ids(record):
    payload = _record_payload(record)
    return tuple(
        dict.fromkeys(
            _tupled(payload.get("farm_lot_id"))
            + _tupled(payload.get("farm_lot_ids"))
            + _tupled(payload.get("source_farm_lot_id"))
            + _tupled(payload.get("source_farm_lot_ids"))
            + _tupled(payload.get("covered_farm_lot_id"))
            + _tupled(payload.get("covered_farm_lot_ids"))
        )
    )


def _blocker(code, message, evidence):
    return {"code": code, "message": message, "evidence": evidence}


def _applies_to_candidate(record, candidate):
    candidate_subject_ids = set(_candidate_subject_ids(candidate))
    record_subject_ids = set(_record_subject_ids(record))
    if candidate_subject_ids and record_subject_ids.intersection(candidate_subject_ids):
        return True
    candidate_farm_lot_id = candidate.get("farm_lot_id")
    if candidate_farm_lot_id and record.get("entity_type") == "farm_lot" and record.get("id") == candidate_farm_lot_id:
        return True
    if candidate_farm_lot_id and candidate_farm_lot_id in _record_farm_lot_ids(record):
        return True
    return False


def _certification_covers_candidate(record, candidate):
    payload = _record_payload(record)
    shipment_date = _parse_iso_date(candidate.get("shipment_date"))
    valid_from = _parse_iso_date(payload.get("valid_from") or payload.get("validity_start"))
    valid_to = _parse_iso_date(payload.get("valid_to") or payload.get("validity_end"))
    if payload.get("suspended") or str(record.get("status", "")).lower() in {"suspended", "expired", "revoked"}:
        return False
    if shipment_date and valid_from and shipment_date < valid_from:
        return False
    if shipment_date and valid_to and shipment_date > valid_to:
        return False

    farm_lot_ids = set(_record_farm_lot_ids(record))
    covered_sites = set(_tupled(payload.get("covered_site_ids")) + _tupled(payload.get("covered_site_id")))
    covered_commodities = set(_tupled(payload.get("covered_commodities")) + _tupled(payload.get("covered_commodity")))

    farm_lot_ok = not farm_lot_ids or candidate.get("farm_lot_id") in farm_lot_ids
    site_ok = not covered_sites or candidate.get("site_id") in covered_sites
    commodity_ok = not covered_commodities or candidate.get("commodity") in covered_commodities
    return farm_lot_ok and site_ok and commodity_ok


def _storage_exception(record):
    payload = _record_payload(record)
    status = str(record.get("status") or payload.get("status") or "").lower()
    resolved = bool(payload.get("resolved_at") or payload.get("resolution") or payload.get("released_at"))
    breached = bool(payload.get("temperature_breach") or payload.get("condition_breach"))
    quarantined = str(payload.get("quarantine_state") or "").lower() in {"active", "open", "hold"}
    open_exception = bool(payload.get("exception_open")) or status in {"exception", "quarantined", "blocked"}
    if resolved:
        return False
    return open_exception or breached or quarantined


def _transport_exception(record):
    payload = _record_payload(record)
    status = str(record.get("status") or payload.get("status") or "").lower()
    resolved = bool(payload.get("resolved_at") or payload.get("resolution"))
    seal_state = str(payload.get("seal_state") or "").lower()
    receiving_confirmed = payload.get("receiving_confirmed")
    open_exception = bool(payload.get("exception_open")) or status in {"exception", "blocked"}
    if resolved:
        return False
    if seal_state in {"broken", "mismatch", "missing"}:
        return True
    if receiving_confirmed is False:
        return True
    return open_exception


def _active_recall(record):
    payload = _record_payload(record)
    status = str(payload.get("recall_status") or record.get("status") or "").lower()
    return status in {"active", "open", "hold", "initiated", "quarantine"}


def evaluate_release_readiness(records, candidate, parameters=None):
    candidate = dict(candidate or {})
    tenant = candidate.get("tenant", "default")
    farm_lot_id = candidate.get("farm_lot_id")
    candidate_id = (
        candidate.get("candidate_id")
        or candidate.get("shipment_id")
        or candidate.get("batch_id")
        or candidate.get("subject_id")
        or "release-candidate"
    )
    relevant_records = tuple(
        record for record in records
        if record.get("tenant", "default") == tenant and _applies_to_candidate(record, candidate)
    )

    farm_lot = next(
        (
            record for record in relevant_records
            if record.get("entity_type") == "farm_lot" and record.get("id") == farm_lot_id
        ),
        None,
    )
    provenance_records = tuple(record for record in relevant_records if record.get("entity_type") == "provenance_proof")
    certification_records = tuple(record for record in relevant_records if record.get("entity_type") == "certification")
    storage_records = tuple(record for record in relevant_records if record.get("entity_type") == "storage_event")
    transport_records = tuple(record for record in relevant_records if record.get("entity_type") == "transport_leg")
    recall_records = tuple(record for record in relevant_records if record.get("entity_type") == "recall_link")

    blockers = []
    passed_checks = []

    farm_lot_status = str((farm_lot or {}).get("status") or "").lower()
    if farm_lot and farm_lot_status == "active":
        passed_checks.append("farm_lot_active")
    else:
        blockers.append(
            _blocker(
                "farm_lot_inactive_or_missing",
                "Release requires an active source farm lot.",
                {"farm_lot_id": farm_lot_id, "found": bool(farm_lot), "status": farm_lot_status or None},
            )
        )

    provenance_ok = any(
        farm_lot_id in _record_farm_lot_ids(record)
        and candidate_id in _record_subject_ids(record)
        for record in provenance_records
    )
    if provenance_ok:
        passed_checks.append("provenance_complete")
    else:
        blockers.append(
            _blocker(
                "provenance_missing",
                "Release requires provenance proof that links the release candidate back to the source farm lot.",
                {"candidate_id": candidate_id, "farm_lot_id": farm_lot_id, "provenance_records": len(provenance_records)},
            )
        )

    matching_certifications = tuple(
        record for record in certification_records if _certification_covers_candidate(record, candidate)
    )
    if matching_certifications:
        passed_checks.append("certification_covered")
    else:
        blockers.append(
            _blocker(
                "certification_out_of_scope_or_expired",
                "Release requires at least one active certification that covers the farm lot, site, commodity, and shipment date.",
                {
                    "candidate_id": candidate_id,
                    "farm_lot_id": farm_lot_id,
                    "shipment_date": candidate.get("shipment_date"),
                    "certification_records": len(certification_records),
                },
            )
        )

    storage_exceptions = tuple(record for record in storage_records if _storage_exception(record))
    if not storage_exceptions:
        passed_checks.append("storage_clear")
    else:
        blockers.append(
            _blocker(
                "storage_exception_open",
                "Release is blocked by unresolved storage or cold-chain exceptions.",
                {"record_ids": tuple(record["id"] for record in storage_exceptions)},
            )
        )

    transport_exceptions = tuple(record for record in transport_records if _transport_exception(record))
    if not transport_exceptions:
        passed_checks.append("transport_clear")
    else:
        blockers.append(
            _blocker(
                "transport_exception_open",
                "Release is blocked by unresolved transport, seal-integrity, or receiving-confirmation issues.",
                {"record_ids": tuple(record["id"] for record in transport_exceptions)},
            )
        )

    active_recalls = tuple(record for record in recall_records if _active_recall(record))
    if not active_recalls:
        passed_checks.append("no_active_recall")
    else:
        blockers.append(
            _blocker(
                "active_recall",
                "Release is blocked because the candidate is already linked to an active recall or quarantine hold.",
                {"record_ids": tuple(record["id"] for record in active_recalls)},
            )
        )

    pending_hazards = _tupled(candidate.get("pending_hazards"))
    pending_lab_results = _tupled(candidate.get("pending_lab_results"))
    pending_corrective_actions = _tupled(candidate.get("pending_corrective_actions"))
    if not pending_hazards and not pending_lab_results and not pending_corrective_actions:
        passed_checks.append("quality_holds_cleared")
    else:
        blockers.append(
            _blocker(
                "quality_hold_open",
                "Release is blocked until pending hazards, lab results, and corrective actions are resolved.",
                {
                    "pending_hazards": pending_hazards,
                    "pending_lab_results": pending_lab_results,
                    "pending_corrective_actions": pending_corrective_actions,
                },
            )
        )

    release_status = "approved" if not blockers else "blocked"
    return {
        "ok": True,
        "candidate": {
            "candidate_id": candidate_id,
            "tenant": tenant,
            "farm_lot_id": farm_lot_id,
            "commodity": candidate.get("commodity"),
            "shipment_date": candidate.get("shipment_date"),
            "site_id": candidate.get("site_id"),
        },
        "release_status": release_status,
        "approved": release_status == "approved",
        "passed_checks": tuple(passed_checks),
        "pending_checks": tuple(check for check in RELEASE_GATE_CHECKS if check not in passed_checks),
        "blockers": tuple(blockers),
        "evidence": {
            "relevant_record_count": len(relevant_records),
            "farm_lot_present": bool(farm_lot),
            "provenance_record_ids": tuple(record["id"] for record in provenance_records),
            "matching_certification_ids": tuple(record["id"] for record in matching_certifications),
            "storage_record_ids": tuple(record["id"] for record in storage_records),
            "transport_record_ids": tuple(record["id"] for record in transport_records),
            "recall_record_ids": tuple(record["id"] for record in recall_records),
        },
        "parameter_snapshot": {
            "quality_score_floor": dict(parameters or {}).get("quality_score_floor"),
            "risk_threshold": dict(parameters or {}).get("risk_threshold"),
        },
        "recommended_actions": tuple(
            blocker["code"] for blocker in blockers
        ),
    }


def build_release_gate_panel(verdict):
    verdict = dict(verdict or {})
    return {
        "ok": verdict.get("ok", False),
        "release_status": verdict.get("release_status"),
        "passed_checks": verdict.get("passed_checks", ()),
        "blockers": verdict.get("blockers", ()),
        "recommended_actions": verdict.get("recommended_actions", ()),
    }
