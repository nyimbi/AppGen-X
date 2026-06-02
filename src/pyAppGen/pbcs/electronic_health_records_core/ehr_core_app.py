"""Executable one-PBC electronic health records core application surface."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256

PBC_KEY = "electronic_health_records_core"
EVENT_TOPIC = "pbc.electronic_health_records_core.events"
APP_EVENT_CONTRACT = "AppGen-X"
OWNED_TABLES = (
    "electronic_health_records_core_patient_chart",
    "electronic_health_records_core_clinical_encounter",
    "electronic_health_records_core_clinical_order",
    "electronic_health_records_core_observation",
    "electronic_health_records_core_allergy",
    "electronic_health_records_core_medication_list",
    "electronic_health_records_core_care_note",
    "electronic_health_records_core_electronic_health_records_core_policy_rule",
    "electronic_health_records_core_electronic_health_records_core_runtime_parameter",
    "electronic_health_records_core_electronic_health_records_core_schema_extension",
    "electronic_health_records_core_electronic_health_records_core_control_assertion",
    "electronic_health_records_core_electronic_health_records_core_governed_model",
    "electronic_health_records_core_appgen_outbox_event",
)
WORKBENCH_QUEUES = (
    "duplicate_chart_reviews",
    "incomplete_encounters",
    "pending_orders",
    "critical_results",
    "medication_reconciliation_needed",
    "unsigned_notes",
    "summary_redaction_requests",
    "control_failures",
)
ENCOUNTER_REQUIRED_DOCUMENTATION = {
    "emergency": ("chief_complaint", "assessment", "disposition"),
    "ambulatory": ("chief_complaint", "assessment", "plan"),
    "inpatient": ("interval_history", "assessment", "plan"),
    "virtual": ("consent", "assessment", "follow_up"),
    "procedure": ("indication", "consent", "findings"),
}
ORDER_TRANSITIONS = {
    "draft": ("signed", "cancelled"),
    "signed": ("released", "cancelled", "discontinued"),
    "released": ("scheduled", "cancelled", "discontinued"),
    "scheduled": ("performed", "cancelled", "discontinued"),
    "performed": ("resulted", "corrected"),
    "resulted": ("completed", "corrected"),
    "completed": (),
    "cancelled": (),
    "discontinued": (),
    "corrected": ("completed",),
}
SUMMARY_PROFILES = {
    "clinical": {
        "chart": True,
        "active_allergies": True,
        "active_medications": True,
        "recent_encounters": True,
        "pending_orders": True,
        "critical_results": True,
        "care_notes": True,
        "control_failures": True,
        "sensitive_flags": True,
    },
    "handoff": {
        "chart": True,
        "active_allergies": True,
        "active_medications": True,
        "recent_encounters": True,
        "pending_orders": True,
        "critical_results": True,
        "care_notes": True,
        "control_failures": False,
        "sensitive_flags": False,
    },
    "patient_portal": {
        "chart": True,
        "active_allergies": True,
        "active_medications": True,
        "recent_encounters": True,
        "pending_orders": True,
        "critical_results": False,
        "care_notes": False,
        "control_failures": False,
        "sensitive_flags": False,
    },
}


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def empty_ehr_state() -> dict:
    return {
        "patient_charts": {},
        "clinical_encounters": {},
        "clinical_orders": {},
        "observations": {},
        "allergies": {},
        "medication_lists": {},
        "care_notes": {},
        "policy_rules": {},
        "runtime_parameters": {},
        "schema_extensions": {},
        "control_assertions": {},
        "governed_models": {},
        "inbox": [],
        "outbox": [],
        "dead_letter": [],
        "idempotency_keys": set(),
    }


def _copy_state(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _emit(state: dict, event_type: str, payload: dict) -> dict:
    event = {
        "event_type": event_type,
        "event_contract": APP_EVENT_CONTRACT,
        "topic": EVENT_TOPIC,
        "payload": dict(payload),
        "idempotency_key": _digest((event_type, payload)),
    }
    state["outbox"].append(event)
    return event


def _idempotency_guard(state: dict, key: str | None, result_key: str, result_value: dict | None = None) -> tuple[bool, dict | None]:
    if not key:
        return False, None
    if key in state["idempotency_keys"]:
        response = {
            "ok": True,
            "duplicate": True,
            "idempotency_key": key,
            "state": state,
            "side_effects": (),
        }
        if result_value is not None:
            response[result_key] = result_value
        return True, response
    state["idempotency_keys"].add(key)
    return False, None


def _add_control_assertion(
    state: dict,
    assertion_type: str,
    severity: str,
    subject_table: str,
    subject_id: str,
    details: dict,
    queue: str,
) -> dict:
    assertion_id = f"control-{_digest((assertion_type, subject_table, subject_id, details))[:12]}"
    record = {
        "assertion_id": assertion_id,
        "table": "electronic_health_records_core_electronic_health_records_core_control_assertion",
        "assertion_type": assertion_type,
        "severity": severity,
        "subject_table": subject_table,
        "subject_id": subject_id,
        "details": dict(details),
        "queue": queue,
        "status": "open",
    }
    state["control_assertions"][assertion_id] = record
    _emit(
        state,
        "ElectronicHealthRecordsCoreExceptionOpened",
        {
            "assertion_type": assertion_type,
            "subject_table": subject_table,
            "subject_id": subject_id,
            "severity": severity,
        },
    )
    return record


def _resolve_control_assertions(state: dict, subject_id: str, assertion_type: str) -> None:
    for record in state["control_assertions"].values():
        if record["subject_id"] == subject_id and record["assertion_type"] == assertion_type:
            record["status"] = "resolved"


def _numeric_flag(value: object, reference_range: dict) -> tuple[bool, bool]:
    if not isinstance(value, (int, float)):
        return False, bool(reference_range.get("critical_flag"))
    low = reference_range.get("low")
    high = reference_range.get("high")
    critical_low = reference_range.get("critical_low")
    critical_high = reference_range.get("critical_high")
    abnormal = (low is not None and value < low) or (high is not None and value > high)
    critical = (critical_low is not None and value <= critical_low) or (critical_high is not None and value >= critical_high)
    return abnormal, critical


def create_patient_chart(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("tenant", "patient_ref", "legal_name", "date_of_birth", "gender")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    chart_id = payload.get("chart_id") or f"chart-{_digest((payload['tenant'], payload['patient_ref']))[:10]}"
    duplicate, response = _idempotency_guard(next_state, payload.get("idempotency_key"), "chart", next_state["patient_charts"].get(chart_id))
    if duplicate:
        return response
    candidates = []
    for chart in next_state["patient_charts"].values():
        if chart["tenant"] != payload["tenant"]:
            continue
        national_match = payload.get("national_id") and payload.get("national_id") == chart.get("national_id")
        demographic_match = (
            payload["legal_name"].strip().lower() == chart["legal_name"].strip().lower()
            and payload["date_of_birth"] == chart["date_of_birth"]
        )
        if national_match or demographic_match:
            candidates.append(chart["chart_id"])
    record = {
        "chart_id": chart_id,
        "id": chart_id,
        "table": "electronic_health_records_core_patient_chart",
        "tenant": payload["tenant"],
        "patient_ref": payload["patient_ref"],
        "chart_number": payload.get("chart_number", chart_id.upper()),
        "legal_name": payload["legal_name"],
        "date_of_birth": payload["date_of_birth"],
        "gender": payload["gender"],
        "national_id": payload.get("national_id"),
        "state": "provisional" if candidates else payload.get("state", "active"),
        "identity_confidence": 0.58 if candidates else 0.97,
        "duplicate_candidate_chart_ids": tuple(candidates),
        "merge_review_required": bool(candidates),
        "merge_decision": None,
        "source_system": payload.get("source_system", "manual_intake"),
        "source_lineage": tuple(payload.get("source_lineage", (payload.get("source_system", "manual_intake"),))),
        "active_problem_list": tuple(payload.get("active_problem_list", ())),
        "sensitive_flags": tuple(payload.get("sensitive_flags", ())),
        "consent_scope": tuple(payload.get("consent_scope", ("clinical", "patient_portal", "handoff"))),
        "version": 1,
    }
    next_state["patient_charts"][chart_id] = record
    duplicate_review = None
    if candidates:
        duplicate_review = _add_control_assertion(
            next_state,
            "duplicate_chart_review_required",
            "high",
            record["table"],
            chart_id,
            {"candidate_chart_ids": tuple(candidates), "identity_confidence": record["identity_confidence"]},
            "duplicate_chart_reviews",
        )
    _emit(next_state, "ElectronicHealthRecordsCoreCreated", {"entity": "patient_chart", "id": chart_id})
    return {"ok": True, "state": next_state, "chart": record, "duplicate_review": duplicate_review, "side_effects": ()}


def review_chart_merge(state: dict, chart_id: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    chart = deepcopy(next_state["patient_charts"].get(chart_id))
    if not chart:
        return {"ok": False, "state": next_state, "reason": "chart_not_found", "side_effects": ()}
    decision = payload.get("decision")
    if decision not in {"link_candidate", "reject_candidate"}:
        return {"ok": False, "state": next_state, "reason": "invalid_merge_decision", "side_effects": ()}
    chart["merge_review_required"] = False
    chart["merge_decision"] = {
        "decision": decision,
        "reviewer": payload.get("reviewer"),
        "candidate_chart_id": payload.get("candidate_chart_id"),
        "reason": payload.get("reason"),
    }
    chart["version"] += 1
    next_state["patient_charts"][chart_id] = chart
    _resolve_control_assertions(next_state, chart_id, "duplicate_chart_review_required")
    _emit(next_state, "ElectronicHealthRecordsCoreApproved", {"entity": "patient_chart", "id": chart_id, "decision": decision})
    return {"ok": True, "state": next_state, "chart": chart, "side_effects": ()}


def record_clinical_encounter(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("chart_id", "encounter_class", "care_setting", "modality", "attending_role", "started_at")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if payload["chart_id"] not in next_state["patient_charts"]:
        return {"ok": False, "state": next_state, "reason": "chart_not_found", "side_effects": ()}
    encounter_id = payload.get("encounter_id") or f"enc-{_digest((payload['chart_id'], payload['started_at'], payload['encounter_class']))[:10]}"
    checklist = ENCOUNTER_REQUIRED_DOCUMENTATION.get(payload["care_setting"], ("assessment", "plan"))
    documentation = tuple(payload.get("documentation", ()))
    missing_docs = tuple(item for item in checklist if item not in documentation)
    record = {
        "encounter_id": encounter_id,
        "id": encounter_id,
        "table": "electronic_health_records_core_clinical_encounter",
        "chart_id": payload["chart_id"],
        "encounter_class": payload["encounter_class"],
        "care_setting": payload["care_setting"],
        "modality": payload["modality"],
        "attending_role": payload["attending_role"],
        "service_line": payload.get("service_line"),
        "started_at": payload["started_at"],
        "discharged_at": payload.get("discharged_at"),
        "external_source": payload.get("external_source"),
        "documentation_checklist": checklist,
        "documentation_complete": not missing_docs,
        "missing_documentation": missing_docs,
        "status": "ready_for_attestation" if not missing_docs else "incomplete",
        "version": 1,
    }
    next_state["clinical_encounters"][encounter_id] = record
    control = None
    if missing_docs:
        control = _add_control_assertion(
            next_state,
            "encounter_documentation_incomplete",
            "medium",
            record["table"],
            encounter_id,
            {"missing_documentation": missing_docs},
            "incomplete_encounters",
        )
    _emit(next_state, "ElectronicHealthRecordsCoreCreated", {"entity": "clinical_encounter", "id": encounter_id})
    return {"ok": True, "state": next_state, "encounter": record, "control_assertion": control, "side_effects": ()}


def review_clinical_order(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("chart_id", "order_type", "priority", "ordering_clinician", "indication")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if payload["chart_id"] not in next_state["patient_charts"]:
        return {"ok": False, "state": next_state, "reason": "chart_not_found", "side_effects": ()}
    order_id = payload.get("order_id") or f"order-{_digest((payload['chart_id'], payload['order_type'], payload['indication']))[:10]}"
    target_substance = (payload.get("medication_substance") or "").strip().lower()
    allergy_warnings = tuple(
        {
            "allergy_id": allergy["allergy_id"],
            "reaction": allergy["reaction"],
            "severity": allergy["severity"],
            "substance": allergy["specific_substance"],
        }
        for allergy in next_state["allergies"].values()
        if allergy["chart_id"] == payload["chart_id"]
        and allergy["status"] != "inactive"
        and target_substance
        and allergy["specific_substance"].strip().lower() == target_substance
    )
    record = {
        "order_id": order_id,
        "id": order_id,
        "table": "electronic_health_records_core_clinical_order",
        "chart_id": payload["chart_id"],
        "order_type": payload["order_type"],
        "priority": payload["priority"],
        "ordering_clinician": payload["ordering_clinician"],
        "indication": payload["indication"],
        "status": payload.get("status", "draft"),
        "requires_result_evidence": bool(payload.get("requires_result_evidence", payload["order_type"] in {"lab", "imaging"})),
        "medication_substance": payload.get("medication_substance"),
        "scheduling_dependency": payload.get("scheduling_dependency"),
        "result_expectation": payload.get("result_expectation"),
        "result_evidence": payload.get("result_evidence"),
        "cancellation_reason": None,
        "discontinuation_authority": None,
        "allergy_warnings": allergy_warnings,
        "version": 1,
    }
    next_state["clinical_orders"][order_id] = record
    if allergy_warnings:
        _add_control_assertion(
            next_state,
            "clinical_order_allergy_warning",
            "high",
            record["table"],
            order_id,
            {"allergy_warnings": allergy_warnings},
            "pending_orders",
        )
    _emit(next_state, "ElectronicHealthRecordsCoreCreated", {"entity": "clinical_order", "id": order_id})
    return {"ok": True, "state": next_state, "order": record, "side_effects": ()}


def transition_clinical_order(state: dict, order_id: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    order = deepcopy(next_state["clinical_orders"].get(order_id))
    if not order:
        return {"ok": False, "state": next_state, "reason": "order_not_found", "side_effects": ()}
    target_state = payload.get("target_state")
    if target_state not in ORDER_TRANSITIONS.get(order["status"], ()):
        return {"ok": False, "state": next_state, "reason": "invalid_order_transition", "current_state": order["status"], "target_state": target_state, "side_effects": ()}
    actor_role = payload.get("actor_role")
    if target_state in {"signed", "released", "discontinued"} and actor_role not in {"ordering_clinician", "attending_clinician", "pharmacist"}:
        return {"ok": False, "state": next_state, "reason": "insufficient_clinical_authority", "side_effects": ()}
    if target_state == "completed" and order["requires_result_evidence"] and not payload.get("result_evidence") and not order.get("result_evidence"):
        return {"ok": False, "state": next_state, "reason": "result_evidence_required", "side_effects": ()}
    order["status"] = target_state
    if payload.get("result_evidence"):
        order["result_evidence"] = payload["result_evidence"]
    order["cancellation_reason"] = payload.get("cancellation_reason")
    order["discontinuation_authority"] = payload.get("discontinuation_authority")
    order["version"] += 1
    next_state["clinical_orders"][order_id] = order
    _emit(next_state, "ElectronicHealthRecordsCoreUpdated", {"entity": "clinical_order", "id": order_id, "status": target_state})
    return {"ok": True, "state": next_state, "order": order, "side_effects": ()}


def approve_observation(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("chart_id", "observation_code", "value", "unit", "collected_at")
    missing = tuple(field for field in required if payload.get(field) in (None, ""))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if payload["chart_id"] not in next_state["patient_charts"]:
        return {"ok": False, "state": next_state, "reason": "chart_not_found", "side_effects": ()}
    observation_id = payload.get("observation_id") or f"obs-{_digest((payload['chart_id'], payload['observation_code'], payload['collected_at']))[:10]}"
    reference_range = dict(payload.get("reference_range", {}))
    abnormal, critical_from_range = _numeric_flag(payload["value"], reference_range)
    critical_flag = bool(payload.get("critical_flag", critical_from_range))
    record = {
        "observation_id": observation_id,
        "id": observation_id,
        "table": "electronic_health_records_core_observation",
        "chart_id": payload["chart_id"],
        "observation_code": payload["observation_code"],
        "value": payload["value"],
        "unit": payload["unit"],
        "method": payload.get("method"),
        "specimen_type": payload.get("specimen_type"),
        "collected_at": payload["collected_at"],
        "resulted_at": payload.get("resulted_at", payload["collected_at"]),
        "reference_range": reference_range,
        "abnormal_flag": abnormal,
        "critical_flag": critical_flag,
        "performer": payload.get("performer"),
        "corrected_result_of": payload.get("corrected_result_of"),
        "acknowledgement_state": "pending" if critical_flag else "not_required",
        "acknowledgement_owner": payload.get("acknowledgement_owner"),
        "acknowledgement_deadline": payload.get("acknowledgement_deadline"),
        "read_back_evidence": None,
        "version": 1,
    }
    next_state["observations"][observation_id] = record
    control = None
    if critical_flag:
        control = _add_control_assertion(
            next_state,
            "critical_result_acknowledgement_required",
            "high",
            record["table"],
            observation_id,
            {
                "acknowledgement_owner": record["acknowledgement_owner"],
                "acknowledgement_deadline": record["acknowledgement_deadline"],
            },
            "critical_results",
        )
    _emit(next_state, "ElectronicHealthRecordsCoreCreated", {"entity": "observation", "id": observation_id})
    return {"ok": True, "state": next_state, "observation": record, "control_assertion": control, "side_effects": ()}


def acknowledge_critical_result(state: dict, observation_id: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    observation = deepcopy(next_state["observations"].get(observation_id))
    if not observation:
        return {"ok": False, "state": next_state, "reason": "observation_not_found", "side_effects": ()}
    if not observation["critical_flag"]:
        return {"ok": False, "state": next_state, "reason": "critical_acknowledgement_not_required", "side_effects": ()}
    if not payload.get("acknowledged_by") or not payload.get("read_back_evidence"):
        return {"ok": False, "state": next_state, "reason": "acknowledgement_evidence_required", "side_effects": ()}
    observation["acknowledgement_state"] = "acknowledged"
    observation["acknowledged_by"] = payload["acknowledged_by"]
    observation["read_back_evidence"] = payload["read_back_evidence"]
    observation["notification_channel"] = payload.get("notification_channel")
    observation["version"] += 1
    next_state["observations"][observation_id] = observation
    _resolve_control_assertions(next_state, observation_id, "critical_result_acknowledgement_required")
    _emit(next_state, "ElectronicHealthRecordsCoreApproved", {"entity": "observation", "id": observation_id})
    return {"ok": True, "state": next_state, "observation": observation, "side_effects": ()}


def simulate_allergy(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("chart_id", "specific_substance", "reaction", "severity")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if payload["chart_id"] not in next_state["patient_charts"]:
        return {"ok": False, "state": next_state, "reason": "chart_not_found", "side_effects": ()}
    allergy_id = payload.get("allergy_id") or f"alg-{_digest((payload['chart_id'], payload['specific_substance'], payload['reaction']))[:10]}"
    duplicates = tuple(
        allergy["allergy_id"]
        for allergy in next_state["allergies"].values()
        if allergy["chart_id"] == payload["chart_id"]
        and allergy["specific_substance"].strip().lower() == payload["specific_substance"].strip().lower()
        and allergy["status"] != "inactive"
    )
    record = {
        "allergy_id": allergy_id,
        "id": allergy_id,
        "table": "electronic_health_records_core_allergy",
        "chart_id": payload["chart_id"],
        "substance_class": payload.get("substance_class", "medication"),
        "specific_substance": payload["specific_substance"],
        "reaction": payload["reaction"],
        "severity": payload["severity"],
        "onset": payload.get("onset"),
        "verification_status": payload.get("verification_status", "verified"),
        "source": payload.get("source", "clinician_entered"),
        "inactive_reason": payload.get("inactive_reason"),
        "clinical_override_guidance": payload.get("clinical_override_guidance"),
        "duplicate_candidate_ids": duplicates,
        "status": payload.get("status", "active"),
        "version": 1,
    }
    next_state["allergies"][allergy_id] = record
    control = None
    if duplicates:
        control = _add_control_assertion(
            next_state,
            "duplicate_allergy_review_required",
            "medium",
            record["table"],
            allergy_id,
            {"duplicate_candidate_ids": duplicates},
            "control_failures",
        )
    _emit(next_state, "ElectronicHealthRecordsCoreCreated", {"entity": "allergy", "id": allergy_id})
    return {"ok": True, "state": next_state, "allergy": record, "control_assertion": control, "side_effects": ()}


def create_medication_list(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("chart_id", "reviewer", "source_list")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if payload["chart_id"] not in next_state["patient_charts"]:
        return {"ok": False, "state": next_state, "reason": "chart_not_found", "side_effects": ()}
    medication_list_id = payload.get("medication_list_id") or f"med-{_digest((payload['chart_id'], payload['reviewer'], tuple(payload.get('source_list', ()))))[:10]}"
    discrepancies = tuple(payload.get("discrepancies", ()))
    record = {
        "medication_list_id": medication_list_id,
        "id": medication_list_id,
        "table": "electronic_health_records_core_medication_list",
        "chart_id": payload["chart_id"],
        "reviewer": payload["reviewer"],
        "source_list": tuple(payload["source_list"]),
        "patient_reported_list": tuple(payload.get("patient_reported_list", ())),
        "reconciliation_actions": tuple(payload.get("reconciliation_actions", ())),
        "discrepancies": discrepancies,
        "unresolved_discrepancy_count": len(discrepancies),
        "status": "needs_follow_up" if discrepancies else "reconciled",
        "version": 1,
    }
    next_state["medication_lists"][medication_list_id] = record
    control = None
    if discrepancies:
        control = _add_control_assertion(
            next_state,
            "medication_reconciliation_incomplete",
            "medium",
            record["table"],
            medication_list_id,
            {"unresolved_discrepancy_count": len(discrepancies)},
            "medication_reconciliation_needed",
        )
    _emit(next_state, "ElectronicHealthRecordsCoreUpdated", {"entity": "medication_list", "id": medication_list_id})
    return {"ok": True, "state": next_state, "medication_list": record, "control_assertion": control, "side_effects": ()}


def record_care_note(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("chart_id", "note_type", "author_ref", "note_text")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    if payload["chart_id"] not in next_state["patient_charts"]:
        return {"ok": False, "state": next_state, "reason": "chart_not_found", "side_effects": ()}
    amends_note_id = payload.get("amends_note_id")
    if amends_note_id and amends_note_id not in next_state["care_notes"]:
        return {"ok": False, "state": next_state, "reason": "amended_note_not_found", "side_effects": ()}
    note_id = payload.get("note_id") or f"note-{_digest((payload['chart_id'], payload['author_ref'], payload['note_text']))[:10]}"
    record = {
        "note_id": note_id,
        "id": note_id,
        "table": "electronic_health_records_core_care_note",
        "chart_id": payload["chart_id"],
        "note_type": payload["note_type"],
        "author_ref": payload["author_ref"],
        "contributors": tuple(payload.get("contributors", ())),
        "supervising_signer": payload.get("supervising_signer"),
        "co_signature_required": bool(payload.get("co_signature_required", False)),
        "attestation_status": "pending_cosign" if payload.get("co_signature_required") else payload.get("attestation_status", "draft"),
        "note_text": payload["note_text"],
        "amends_note_id": amends_note_id,
        "correction_reason": payload.get("correction_reason"),
        "late_entry_marker": bool(payload.get("late_entry_marker", False)),
        "source_evidence": payload.get("source_evidence"),
        "version": 1,
    }
    next_state["care_notes"][note_id] = record
    if record["attestation_status"] != "signed":
        _add_control_assertion(
            next_state,
            "care_note_attestation_required",
            "medium",
            record["table"],
            note_id,
            {"co_signature_required": record["co_signature_required"]},
            "unsigned_notes",
        )
    _emit(next_state, "ElectronicHealthRecordsCoreCreated", {"entity": "care_note", "id": note_id})
    return {"ok": True, "state": next_state, "care_note": record, "side_effects": ()}


def attest_care_note(state: dict, note_id: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    note = deepcopy(next_state["care_notes"].get(note_id))
    if not note:
        return {"ok": False, "state": next_state, "reason": "care_note_not_found", "side_effects": ()}
    signer_ref = payload.get("signer_ref")
    signer_role = payload.get("signer_role")
    if not signer_ref or not signer_role:
        return {"ok": False, "state": next_state, "reason": "signer_identity_required", "side_effects": ()}
    if note["co_signature_required"] and signer_ref != note.get("supervising_signer"):
        return {"ok": False, "state": next_state, "reason": "supervising_signer_required", "side_effects": ()}
    if not note["co_signature_required"] and signer_ref not in {note["author_ref"], note.get("supervising_signer")}:
        return {"ok": False, "state": next_state, "reason": "unauthorized_note_signer", "side_effects": ()}
    note["attestation_status"] = "signed"
    note["signed_by"] = signer_ref
    note["signed_role"] = signer_role
    note["signed_at"] = payload.get("signed_at")
    note["version"] += 1
    next_state["care_notes"][note_id] = note
    _resolve_control_assertions(next_state, note_id, "care_note_attestation_required")
    _emit(next_state, "ElectronicHealthRecordsCoreApproved", {"entity": "care_note", "id": note_id})
    return {"ok": True, "state": next_state, "care_note": note, "side_effects": ()}


def assemble_patient_summary(state: dict, chart_id: str, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    chart = deepcopy(state.get("patient_charts", {}).get(chart_id))
    if not chart:
        return {"ok": False, "reason": "chart_not_found", "side_effects": ()}
    profile = payload.get("profile", "clinical")
    if profile not in SUMMARY_PROFILES:
        return {"ok": False, "reason": "unsupported_summary_profile", "side_effects": ()}
    allowed = SUMMARY_PROFILES[profile]
    active_allergies = tuple(
        allergy
        for allergy in state.get("allergies", {}).values()
        if allergy["chart_id"] == chart_id and allergy["status"] != "inactive"
    )
    active_medications = []
    for medication_list in state.get("medication_lists", {}).values():
        if medication_list["chart_id"] != chart_id:
            continue
        active_medications.extend(medication_list["source_list"])
    recent_encounters = tuple(
        sorted(
            (encounter for encounter in state.get("clinical_encounters", {}).values() if encounter["chart_id"] == chart_id),
            key=lambda item: item["started_at"],
            reverse=True,
        )[:3]
    )
    pending_orders = tuple(
        order
        for order in state.get("clinical_orders", {}).values()
        if order["chart_id"] == chart_id and order["status"] not in {"completed", "cancelled", "discontinued"}
    )
    critical_results = tuple(
        observation
        for observation in state.get("observations", {}).values()
        if observation["chart_id"] == chart_id and observation["critical_flag"] and observation["acknowledgement_state"] != "acknowledged"
    )
    notes = tuple(
        note
        for note in state.get("care_notes", {}).values()
        if note["chart_id"] == chart_id and note["attestation_status"] == "signed"
    )
    control_failures = tuple(
        assertion
        for assertion in state.get("control_assertions", {}).values()
        if assertion["status"] == "open"
        and assertion["subject_id"] in {chart_id}
        or (
            assertion["subject_table"].startswith("electronic_health_records_core_")
            and any(
                parent.get("chart_id") == chart_id
                for parent in (
                    state.get("clinical_encounters", {}).get(assertion["subject_id"]),
                    state.get("clinical_orders", {}).get(assertion["subject_id"]),
                    state.get("observations", {}).get(assertion["subject_id"]),
                    state.get("medication_lists", {}).get(assertion["subject_id"]),
                    state.get("care_notes", {}).get(assertion["subject_id"]),
                )
                if parent
            )
        )
    )
    raw_summary = {
        "chart": {
            "chart_id": chart["chart_id"],
            "legal_name": chart["legal_name"],
            "active_problem_list": chart["active_problem_list"],
        },
        "active_allergies": active_allergies,
        "active_medications": tuple(active_medications),
        "recent_encounters": recent_encounters,
        "pending_orders": pending_orders,
        "critical_results": critical_results,
        "care_notes": notes,
        "control_failures": control_failures,
        "sensitive_flags": chart["sensitive_flags"],
    }
    redacted_sections = tuple(section for section, enabled in allowed.items() if not enabled)
    summary = {section: value for section, value in raw_summary.items() if allowed.get(section, False)}
    source_freshness = {
        "recent_encounters": recent_encounters[0]["started_at"] if recent_encounters else None,
        "pending_orders": pending_orders[0]["order_id"] if pending_orders else None,
        "critical_results": critical_results[0]["resulted_at"] if critical_results else None,
    }
    return {
        "ok": True,
        "chart_id": chart_id,
        "profile": profile,
        "summary": summary,
        "redacted_sections": redacted_sections,
        "source_freshness": source_freshness,
        "side_effects": (),
    }


def ehr_core_workbench(state: dict, payload: dict | None = None) -> dict:
    payload = dict(payload or {})
    tenant = payload.get("tenant")
    charts = tuple(
        chart for chart in state.get("patient_charts", {}).values() if tenant in (None, chart["tenant"])
    )
    queues = {
        "duplicate_chart_reviews": tuple(chart for chart in charts if chart["merge_review_required"]),
        "incomplete_encounters": tuple(
            encounter
            for encounter in state.get("clinical_encounters", {}).values()
            if encounter["status"] == "incomplete"
            and (tenant is None or state["patient_charts"][encounter["chart_id"]]["tenant"] == tenant)
        ),
        "pending_orders": tuple(
            order
            for order in state.get("clinical_orders", {}).values()
            if order["status"] not in {"completed", "cancelled", "discontinued"}
            and (tenant is None or state["patient_charts"][order["chart_id"]]["tenant"] == tenant)
        ),
        "critical_results": tuple(
            observation
            for observation in state.get("observations", {}).values()
            if observation["critical_flag"] and observation["acknowledgement_state"] != "acknowledged"
            and (tenant is None or state["patient_charts"][observation["chart_id"]]["tenant"] == tenant)
        ),
        "medication_reconciliation_needed": tuple(
            medication_list
            for medication_list in state.get("medication_lists", {}).values()
            if medication_list["unresolved_discrepancy_count"] > 0
            and (tenant is None or state["patient_charts"][medication_list["chart_id"]]["tenant"] == tenant)
        ),
        "unsigned_notes": tuple(
            note
            for note in state.get("care_notes", {}).values()
            if note["attestation_status"] != "signed"
            and (tenant is None or state["patient_charts"][note["chart_id"]]["tenant"] == tenant)
        ),
        "summary_redaction_requests": tuple(chart for chart in charts if chart["sensitive_flags"]),
        "control_failures": tuple(
            control
            for control in state.get("control_assertions", {}).values()
            if control["status"] == "open"
        ),
    }
    metrics = {
        "chart_count": len(charts),
        "encounter_count": len(state.get("clinical_encounters", {})),
        "order_count": len(state.get("clinical_orders", {})),
        "critical_result_count": len(queues["critical_results"]),
        "unsigned_note_count": len(queues["unsigned_notes"]),
        "open_control_count": len(queues["control_failures"]),
    }
    return {
        "ok": True,
        "tenant": tenant,
        "queues": queues,
        "metrics": metrics,
        "queue_names": WORKBENCH_QUEUES,
        "side_effects": (),
    }


def ehr_core_forms_contract() -> dict:
    forms = (
        {"name": "PatientChartIntakeForm", "writes_table": "electronic_health_records_core_patient_chart", "fields": ("tenant", "patient_ref", "legal_name", "date_of_birth", "gender", "national_id", "source_system")},
        {"name": "ClinicalEncounterForm", "writes_table": "electronic_health_records_core_clinical_encounter", "fields": ("chart_id", "encounter_class", "care_setting", "modality", "attending_role", "documentation")},
        {"name": "ClinicalOrderForm", "writes_table": "electronic_health_records_core_clinical_order", "fields": ("chart_id", "order_type", "priority", "ordering_clinician", "indication", "medication_substance")},
        {"name": "ObservationResultForm", "writes_table": "electronic_health_records_core_observation", "fields": ("chart_id", "observation_code", "value", "unit", "reference_range", "acknowledgement_owner")},
        {"name": "AllergyCaptureForm", "writes_table": "electronic_health_records_core_allergy", "fields": ("chart_id", "specific_substance", "reaction", "severity", "verification_status")},
        {"name": "MedicationReconciliationForm", "writes_table": "electronic_health_records_core_medication_list", "fields": ("chart_id", "reviewer", "source_list", "patient_reported_list", "discrepancies")},
        {"name": "CareNoteForm", "writes_table": "electronic_health_records_core_care_note", "fields": ("chart_id", "note_type", "author_ref", "note_text", "co_signature_required")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def ehr_core_wizards_contract() -> dict:
    wizards = (
        {"name": "ChartIdentityReviewWizard", "steps": ("capture_identity", "review_duplicates", "record_link_decision")},
        {"name": "EncounterCloseoutWizard", "steps": ("capture_context", "complete_documentation", "route_for_attestation")},
        {"name": "CriticalResultAcknowledgementWizard", "steps": ("review_result", "notify_clinician", "record_read_back")},
        {"name": "MedicationReconciliationWizard", "steps": ("compare_lists", "resolve_discrepancies", "confirm_reconciliation")},
        {"name": "SummaryRedactionWizard", "steps": ("select_profile", "preview_redactions", "publish_summary")},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def ehr_core_controls_contract() -> dict:
    controls = (
        {"name": "duplicate_chart_review_required", "prevents": "automatic_merge", "queue": "duplicate_chart_reviews"},
        {"name": "encounter_documentation_complete", "prevents": "encounter_attestation", "queue": "incomplete_encounters"},
        {"name": "clinical_order_transition_guard", "prevents": "invalid_order_state_change", "queue": "pending_orders"},
        {"name": "critical_result_acknowledgement_required", "prevents": "silent_critical_result_closure", "queue": "critical_results"},
        {"name": "care_note_attestation_authority", "prevents": "unauthorized_note_signing", "queue": "unsigned_notes"},
        {"name": "summary_redaction_required", "prevents": "oversharing_sensitive_sections", "queue": "summary_redaction_requests"},
        {"name": "owned_table_boundary_guard", "prevents": "foreign_table_mutation", "queue": "control_failures"},
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": controls, "side_effects": ()}


def single_pbc_app_contract() -> dict:
    forms = ehr_core_forms_contract()
    wizards = ehr_core_wizards_contract()
    controls = ehr_core_controls_contract()
    return {
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": PBC_KEY,
        "database_backed": True,
        "workbench": "ElectronicHealthRecordsCoreWorkbench",
        "assistant_panel": "ElectronicHealthRecordsCoreAssistantPanel",
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "routes": (
            "POST /patient-charts",
            "POST /clinical-encounters",
            "POST /clinical-orders",
            "POST /clinical-orders/transition",
            "POST /observations",
            "POST /observations/acknowledgements",
            "POST /allergies",
            "POST /medication-reconciliations",
            "POST /care-notes",
            "POST /care-notes/attestations",
            "GET /patient-summaries",
            "GET /electronic-health-records-core-workbench",
        ),
        "service_class": "ElectronicHealthRecordsCoreService",
        "side_effects": (),
    }


def document_instruction_mutation_plan(document: str, instruction: str) -> dict:
    content = f"{document} {instruction}".lower()
    if "critical" in content or "acknowledge" in content:
        target_table = "electronic_health_records_core_observation"
        proposed_action = "update"
        reason = "critical_result_acknowledgement"
    elif "allerg" in content:
        target_table = "electronic_health_records_core_allergy"
        proposed_action = "create"
        reason = "allergy_capture"
    elif "medication" in content and "reconcil" in content:
        target_table = "electronic_health_records_core_medication_list"
        proposed_action = "update"
        reason = "medication_reconciliation"
    elif "note" in content or "attest" in content:
        target_table = "electronic_health_records_core_care_note"
        proposed_action = "create"
        reason = "note_authorship"
    elif "order" in content:
        target_table = "electronic_health_records_core_clinical_order"
        proposed_action = "create"
        reason = "clinical_order_workflow"
    elif "summary" in content or "handoff" in content:
        target_table = "electronic_health_records_core_patient_chart"
        proposed_action = "query"
        reason = "patient_summary"
    else:
        target_table = "electronic_health_records_core_patient_chart"
        proposed_action = "create"
        reason = "patient_chart_intake"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "instruction_digest": _digest(instruction),
        "target_table": target_table,
        "proposed_action": proposed_action,
        "reason": reason,
        "requires_human_confirmation": proposed_action != "query",
        "side_effects": (),
    }


def ehr_core_smoke_test() -> dict:
    state = empty_ehr_state()
    chart = create_patient_chart(
        state,
        {
            "tenant": "tenant-smoke",
            "patient_ref": "patient-smoke",
            "legal_name": "Smoke Patient",
            "date_of_birth": "1975-01-01",
            "gender": "unknown",
        },
    )
    encounter = record_clinical_encounter(
        chart["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "encounter_class": "ambulatory",
            "care_setting": "ambulatory",
            "modality": "in_person",
            "attending_role": "attending_clinician",
            "started_at": "2026-05-29T09:00:00Z",
            "documentation": ("chief_complaint", "assessment", "plan"),
        },
    )
    allergy = simulate_allergy(
        encounter["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "specific_substance": "penicillin",
            "reaction": "rash",
            "severity": "high",
        },
    )
    order = review_clinical_order(
        allergy["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "order_type": "medication",
            "priority": "routine",
            "ordering_clinician": "clinician-1",
            "indication": "infection",
            "medication_substance": "penicillin",
        },
    )
    observation = approve_observation(
        order["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "observation_code": "potassium",
            "value": 6.5,
            "unit": "mmol/L",
            "collected_at": "2026-05-29T10:00:00Z",
            "reference_range": {"low": 3.5, "high": 5.0, "critical_high": 6.0},
            "acknowledgement_owner": "clinician-1",
            "acknowledgement_deadline": "2026-05-29T10:15:00Z",
        },
    )
    ack = acknowledge_critical_result(
        observation["state"],
        observation["observation"]["observation_id"],
        {"acknowledged_by": "clinician-1", "read_back_evidence": "read back to charge nurse"},
    )
    note = record_care_note(
        ack["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "note_type": "progress_note",
            "author_ref": "clinician-1",
            "note_text": "Critical result reviewed and patient notified.",
        },
    )
    signed = attest_care_note(
        note["state"],
        note["care_note"]["note_id"],
        {"signer_ref": "clinician-1", "signer_role": "attending_clinician", "signed_at": "2026-05-29T10:20:00Z"},
    )
    medications = create_medication_list(
        signed["state"],
        {
            "chart_id": chart["chart"]["chart_id"],
            "reviewer": "pharmacist-1",
            "source_list": ({"name": "Furosemide", "dose": "40 mg"},),
            "discrepancies": (),
        },
    )
    summary = assemble_patient_summary(medications["state"], chart["chart"]["chart_id"], {"profile": "clinical"})
    workbench = ehr_core_workbench(medications["state"], {"tenant": "tenant-smoke"})
    app = single_pbc_app_contract()
    return {
        "ok": all(
            (
                chart["ok"],
                encounter["ok"],
                allergy["ok"],
                order["ok"],
                observation["ok"],
                ack["ok"],
                note["ok"],
                signed["ok"],
                medications["ok"],
                summary["ok"],
                workbench["ok"],
                app["ok"],
            )
        ),
        "chart": chart,
        "workbench": workbench,
        "summary": summary,
        "single_pbc_app": app,
        "side_effects": (),
    }
