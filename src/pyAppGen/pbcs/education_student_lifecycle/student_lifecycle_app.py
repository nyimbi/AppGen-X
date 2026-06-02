"""Standalone education student lifecycle app surface."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256

PBC_KEY = "education_student_lifecycle"
OWNED_TABLES = (
    "education_student_lifecycle_student_applicant",
    "education_student_lifecycle_applicant_document_evidence",
    "education_student_lifecycle_enrollment",
    "education_student_lifecycle_curriculum_plan",
    "education_student_lifecycle_course_attempt",
    "education_student_lifecycle_assessment_result",
    "education_student_lifecycle_advising_case",
    "education_student_lifecycle_intervention_plan",
    "education_student_lifecycle_academic_petition",
    "education_student_lifecycle_transfer_credit_evaluation",
    "education_student_lifecycle_degree_audit",
    "education_student_lifecycle_student_risk_signal",
    "education_student_lifecycle_hold_projection",
    "education_student_lifecycle_engagement_projection",
    "education_student_lifecycle_accommodation_projection",
    "education_student_lifecycle_graduation_clearance",
    "education_student_lifecycle_credential",
)
APPLICANT_STAGES = (
    "inquiry",
    "application_submitted",
    "document_review",
    "decision_ready",
    "offered",
    "accepted",
    "matriculated",
    "withdrawn",
    "declined",
)
ENROLLMENT_STATES = (
    "admitted",
    "matriculated",
    "active",
    "probation",
    "leave",
    "withdrawn",
    "suspended",
    "completed",
    "graduated",
)
PASSING_GRADES = {"A", "A-", "B+", "B", "B-", "C+", "C", "P", "CR"}


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def empty_student_lifecycle_state() -> dict:
    return {
        "applicants": {},
        "documents": {},
        "enrollments": {},
        "curriculum_plans": {},
        "course_attempts": {},
        "assessments": {},
        "advising_cases": {},
        "interventions": {},
        "petitions": {},
        "transfer_credits": {},
        "degree_audits": {},
        "risk_signals": {},
        "hold_projections": {},
        "engagement_projections": {},
        "accommodation_projections": {},
        "graduation_clearances": {},
        "credentials": {},
        "exceptions": {},
        "outbox": [],
    }


def _copy_state(state: dict) -> dict:
    return deepcopy(state)


def _emit(state: dict, event_type: str, payload: dict) -> None:
    state["outbox"].append(
        {
            "event_type": event_type,
            "event_contract": "AppGen-X",
            "topic": "pbc.education_student_lifecycle.events",
            "payload": dict(payload),
            "idempotency_key": _digest((event_type, payload)),
        }
    )


def _record_exception(state: dict, entity: str, entity_id: str, blockers: tuple[str, ...]) -> None:
    key = f"{entity}:{entity_id}"
    if blockers:
        state["exceptions"][key] = {"entity": entity, "entity_id": entity_id, "blockers": blockers}
    else:
        state["exceptions"].pop(key, None)


def _active_holds(state: dict, student_id: str | None, action: str) -> tuple[dict, ...]:
    return tuple(
        hold
        for hold in state["hold_projections"].values()
        if hold.get("student_id") == student_id
        and hold.get("status", "active") == "active"
        and action in hold.get("blocking_actions", ())
    )


def _latest_for_student(records: dict, student_id: str, field: str = "student_id") -> dict | None:
    matches = [record for record in records.values() if record.get(field) == student_id]
    return matches[-1] if matches else None


def register_student_applicant(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    applicant_id = payload.get("applicant_id") or f"app-{_digest((payload.get('student_name'), payload.get('program_code')))[:8]}"
    stage = payload.get("application_stage", "application_submitted")
    decision_status = payload.get("decision_status", "pending")
    required_documents = tuple(payload.get("required_documents", ("transcript", "essay")))
    documents_received = tuple(payload.get("documents_received", ()))
    missing_documents = tuple(doc for doc in required_documents if doc not in documents_received)
    blockers = []
    if not payload.get("program_code"):
        blockers.append("program_code_missing")
    if stage not in APPLICANT_STAGES:
        blockers.append("invalid_application_stage")
    if stage in {"decision_ready", "offered", "accepted"} and missing_documents:
        blockers.append("required_documents_missing")
    applicant = {
        "id": applicant_id,
        "table": "education_student_lifecycle_student_applicant",
        "student_name": payload.get("student_name", applicant_id),
        "program_code": payload.get("program_code"),
        "intake_term": payload.get("intake_term"),
        "catalog_year": payload.get("catalog_year"),
        "application_stage": stage if not blockers else "application_submitted",
        "decision_status": decision_status if "required_documents_missing" not in blockers else "pending",
        "required_documents": required_documents,
        "documents_received": documents_received,
        "missing_documents": missing_documents,
        "applicant_type": payload.get("applicant_type", "first_year"),
        "residency": payload.get("residency", "domestic"),
        "offer_conditions": tuple(payload.get("offer_conditions", ())),
        "acceptance_deadline": payload.get("acceptance_deadline"),
        "blockers": tuple(blockers),
    }
    next_state["applicants"][applicant_id] = applicant
    _record_exception(next_state, "student_applicant", applicant_id, applicant["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleCreated",
        {"entity": "student_applicant", "id": applicant_id, "blockers": applicant["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "student_applicant": applicant, "side_effects": ()}


def review_applicant_documents(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    applicant_id = payload.get("applicant_id")
    applicant = next_state["applicants"].get(applicant_id)
    if applicant is None:
        return {"ok": False, "state": next_state, "reason": "applicant_missing", "side_effects": ()}
    document_id = payload.get("document_id") or f"doc-{_digest((applicant_id, payload.get('document_type')))[:8]}"
    blockers = []
    if not payload.get("document_type"):
        blockers.append("document_type_missing")
    if payload.get("authenticity_status") == "verified" and not payload.get("reviewer"):
        blockers.append("reviewer_required_for_verified_document")
    if float(payload.get("confidence", 1.0)) < 0.8:
        blockers.append("document_confidence_below_threshold")
    document = {
        "id": document_id,
        "table": "education_student_lifecycle_applicant_document_evidence",
        "applicant_id": applicant_id,
        "document_type": payload.get("document_type"),
        "issuing_institution": payload.get("issuing_institution"),
        "received_date": payload.get("received_date"),
        "authenticity_status": payload.get("authenticity_status", "pending"),
        "reviewer": payload.get("reviewer"),
        "confidence": float(payload.get("confidence", 1.0)),
        "blockers": tuple(blockers),
    }
    next_state["documents"][document_id] = document
    received = set(applicant.get("documents_received", ()))
    if document["document_type"]:
        received.add(document["document_type"])
    applicant["documents_received"] = tuple(sorted(received))
    applicant["missing_documents"] = tuple(doc for doc in applicant["required_documents"] if doc not in applicant["documents_received"])
    if not applicant["missing_documents"] and applicant["application_stage"] == "application_submitted":
        applicant["application_stage"] = "document_review"
    applicant_blockers = tuple(blockers) + applicant["missing_documents"]
    _record_exception(next_state, "applicant_document_evidence", document_id, document["blockers"])
    _record_exception(next_state, "student_applicant", applicant_id, applicant_blockers)
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if document["blockers"] else "EducationStudentLifecycleUpdated",
        {"entity": "applicant_document_evidence", "id": document_id, "blockers": document["blockers"]},
    )
    return {"ok": not document["blockers"], "state": next_state, "document": document, "student_applicant": applicant, "side_effects": ()}


def activate_enrollment(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    applicant_id = payload.get("applicant_id")
    applicant = next_state["applicants"].get(applicant_id)
    student_id = payload.get("student_id") or f"student-{(applicant_id or 'unknown').split('-')[-1]}"
    blockers = []
    if applicant is None:
        blockers.append("applicant_missing")
    elif applicant.get("decision_status") not in {"accepted", "deferred"} and applicant.get("application_stage") not in {"accepted", "matriculated"}:
        blockers.append("applicant_not_accepted")
    if applicant and applicant.get("missing_documents"):
        blockers.append("admissions_evidence_incomplete")
    if _active_holds(next_state, student_id, "activate_enrollment"):
        blockers.append("blocking_hold_present")
    status = payload.get("status", "active")
    if status not in ENROLLMENT_STATES:
        blockers.append("invalid_enrollment_status")
    enrollment_id = payload.get("enrollment_id") or f"enr-{_digest((student_id, payload.get('program_code'), payload.get('term')))[:8]}"
    enrollment = {
        "id": enrollment_id,
        "table": "education_student_lifecycle_enrollment",
        "student_id": student_id,
        "applicant_id": applicant_id,
        "program_code": payload.get("program_code") or (applicant or {}).get("program_code"),
        "catalog_year": payload.get("catalog_year") or (applicant or {}).get("catalog_year"),
        "term": payload.get("term"),
        "campus": payload.get("campus", "main"),
        "modality": payload.get("modality", "in_person"),
        "status": status if not blockers else "admitted",
        "standing": payload.get("standing", "good"),
        "load": payload.get("load", "full_time"),
        "blockers": tuple(blockers),
    }
    next_state["enrollments"][enrollment_id] = enrollment
    _record_exception(next_state, "enrollment", enrollment_id, enrollment["blockers"])
    if applicant and not blockers:
        applicant["application_stage"] = "matriculated"
        applicant["decision_status"] = "accepted"
        _record_exception(next_state, "student_applicant", applicant_id, ())
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleApproved",
        {"entity": "enrollment", "id": enrollment_id, "blockers": enrollment["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "enrollment": enrollment, "side_effects": ()}


def maintain_curriculum_plan(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    plan_id = payload.get("plan_id") or f"plan-{_digest((payload.get('student_id'), payload.get('catalog_year')))[:8]}"
    blockers = []
    if not payload.get("student_id"):
        blockers.append("student_id_missing")
    if not payload.get("catalog_year"):
        blockers.append("catalog_year_missing")
    if not payload.get("requirements"):
        blockers.append("requirements_missing")
    curriculum_plan = {
        "id": plan_id,
        "table": "education_student_lifecycle_curriculum_plan",
        "student_id": payload.get("student_id"),
        "program_code": payload.get("program_code"),
        "catalog_year": payload.get("catalog_year"),
        "plan_version": payload.get("plan_version", "v1"),
        "required_credits": int(payload.get("required_credits", 120)),
        "requirements": tuple(payload.get("requirements", ())),
        "required_competencies": tuple(payload.get("required_competencies", ())),
        "approved_substitutions": tuple(payload.get("approved_substitutions", ())),
        "approved_waivers": tuple(payload.get("approved_waivers", ())),
        "blockers": tuple(blockers),
    }
    next_state["curriculum_plans"][plan_id] = curriculum_plan
    _record_exception(next_state, "curriculum_plan", plan_id, curriculum_plan["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleUpdated",
        {"entity": "curriculum_plan", "id": plan_id, "blockers": curriculum_plan["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "curriculum_plan": curriculum_plan, "side_effects": ()}


def record_hold_projection(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    hold_id = payload.get("hold_id") or f"hold-{_digest((payload.get('student_id'), payload.get('hold_type')))[:8]}"
    hold = {
        "id": hold_id,
        "table": "education_student_lifecycle_hold_projection",
        "student_id": payload.get("student_id"),
        "hold_type": payload.get("hold_type", "administrative"),
        "source": payload.get("source", "external_projection"),
        "blocking_actions": tuple(payload.get("blocking_actions", ("register_course",))),
        "freshness": payload.get("freshness", "current"),
        "status": payload.get("status", "active"),
    }
    next_state["hold_projections"][hold_id] = hold
    _record_exception(next_state, "hold_projection", hold_id, ("blocking_hold_present",) if hold["status"] == "active" else ())
    _emit(next_state, "EducationStudentLifecycleUpdated", {"entity": "hold_projection", "id": hold_id})
    return {"ok": True, "state": next_state, "hold_projection": hold, "side_effects": ()}


def record_engagement_projection(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    projection_id = payload.get("projection_id") or f"eng-{_digest((payload.get('student_id'), payload.get('attendance_rate')))[:8]}"
    engagement = {
        "id": projection_id,
        "table": "education_student_lifecycle_engagement_projection",
        "student_id": payload.get("student_id"),
        "attendance_rate": float(payload.get("attendance_rate", 1.0)),
        "last_activity_at": payload.get("last_activity_at"),
        "missing_work_flag": bool(payload.get("missing_work_flag", False)),
        "risk_contribution": float(payload.get("risk_contribution", 0.0)),
        "privacy_scope": payload.get("privacy_scope", "advisor"),
    }
    next_state["engagement_projections"][projection_id] = engagement
    _emit(next_state, "EducationStudentLifecycleUpdated", {"entity": "engagement_projection", "id": projection_id})
    return {"ok": True, "state": next_state, "engagement_projection": engagement, "side_effects": ()}


def finalize_assessment_result(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    assessment_id = payload.get("assessment_id") or f"asmt-{_digest((payload.get('student_id'), payload.get('assessment_type')))[:8]}"
    blockers = []
    if payload.get("moderation_status", "draft") != "final":
        blockers.append("moderation_not_final")
    if payload.get("finalization_requested", True) and not payload.get("scorer"):
        blockers.append("scorer_missing")
    assessment = {
        "id": assessment_id,
        "table": "education_student_lifecycle_assessment_result",
        "student_id": payload.get("student_id"),
        "assessment_type": payload.get("assessment_type"),
        "score": float(payload.get("score", 0.0)),
        "competencies": tuple(payload.get("competencies", ())),
        "achieved": bool(payload.get("achieved", False)),
        "moderation_status": payload.get("moderation_status", "draft"),
        "scorer": payload.get("scorer"),
        "blockers": tuple(blockers),
    }
    next_state["assessments"][assessment_id] = assessment
    _record_exception(next_state, "assessment_result", assessment_id, assessment["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleApproved",
        {"entity": "assessment_result", "id": assessment_id, "blockers": assessment["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "assessment_result": assessment, "side_effects": ()}


def register_course_attempt(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    student_id = payload.get("student_id")
    enrollment = next(
        (
            item
            for item in next_state["enrollments"].values()
            if item.get("student_id") == student_id and item.get("status") in {"matriculated", "active", "probation"}
        ),
        None,
    )
    blockers = []
    if enrollment is None:
        blockers.append("active_enrollment_required")
    if _active_holds(next_state, student_id, "register_course"):
        blockers.append("registration_hold_present")
    if not payload.get("prerequisites_satisfied", False) and not payload.get("override_approved", False):
        blockers.append("missing_prerequisite_or_override")
    status = payload.get("status", "registered")
    grade = payload.get("grade")
    attempt_id = payload.get("attempt_id") or f"attempt-{_digest((student_id, payload.get('course_code'), payload.get('term')))[:8]}"
    attempt = {
        "id": attempt_id,
        "table": "education_student_lifecycle_course_attempt",
        "student_id": student_id,
        "course_code": payload.get("course_code"),
        "term": payload.get("term"),
        "status": "blocked" if blockers else status,
        "credits": float(payload.get("credits", 0.0)),
        "earned_credits": float(payload.get("credits", 0.0)) if status == "completed" and grade in PASSING_GRADES else 0.0,
        "grade": grade,
        "grade_mode": payload.get("grade_mode", "graded"),
        "attempt_number": int(payload.get("attempt_number", 1)),
        "override_approved": bool(payload.get("override_approved", False)),
        "blockers": tuple(blockers),
    }
    next_state["course_attempts"][attempt_id] = attempt
    _record_exception(next_state, "course_attempt", attempt_id, attempt["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleUpdated",
        {"entity": "course_attempt", "id": attempt_id, "blockers": attempt["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "course_attempt": attempt, "side_effects": ()}


def open_advising_case(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    case_id = payload.get("case_id") or f"case-{_digest((payload.get('student_id'), payload.get('case_type')))[:8]}"
    blockers = []
    if not payload.get("student_id"):
        blockers.append("student_id_missing")
    case = {
        "id": case_id,
        "table": "education_student_lifecycle_advising_case",
        "student_id": payload.get("student_id"),
        "case_type": payload.get("case_type", "academic_planning"),
        "urgency": payload.get("urgency", "normal"),
        "owner": payload.get("owner"),
        "student_goal": payload.get("student_goal"),
        "barrier": payload.get("barrier"),
        "status": payload.get("status", "open"),
        "blockers": tuple(blockers),
    }
    next_state["advising_cases"][case_id] = case
    _record_exception(next_state, "advising_case", case_id, case["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleCreated",
        {"entity": "advising_case", "id": case_id, "blockers": case["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "advising_case": case, "side_effects": ()}


def record_intervention_plan(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    case = next_state["advising_cases"].get(payload.get("case_id"))
    intervention_id = payload.get("intervention_id") or f"int-{_digest((payload.get('case_id'), payload.get('objective')))[:8]}"
    blockers = []
    if case is None:
        blockers.append("advising_case_missing")
    if payload.get("high_impact", False) and not payload.get("reviewer_confirmed", False):
        blockers.append("human_review_required")
    intervention = {
        "id": intervention_id,
        "table": "education_student_lifecycle_intervention_plan",
        "case_id": payload.get("case_id"),
        "student_id": payload.get("student_id") or (case or {}).get("student_id"),
        "objective": payload.get("objective"),
        "owner": payload.get("owner"),
        "due_date": payload.get("due_date"),
        "resource_referral": payload.get("resource_referral"),
        "high_impact": bool(payload.get("high_impact", False)),
        "reviewer_confirmed": bool(payload.get("reviewer_confirmed", False)),
        "blockers": tuple(blockers),
    }
    next_state["interventions"][intervention_id] = intervention
    _record_exception(next_state, "intervention_plan", intervention_id, intervention["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleUpdated",
        {"entity": "intervention_plan", "id": intervention_id, "blockers": intervention["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "intervention_plan": intervention, "side_effects": ()}


def submit_academic_petition(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    petition_id = payload.get("petition_id") or f"pet-{_digest((payload.get('student_id'), payload.get('petition_type')))[:8]}"
    blockers = []
    if not payload.get("evidence"):
        blockers.append("petition_evidence_required")
    petition = {
        "id": petition_id,
        "table": "education_student_lifecycle_academic_petition",
        "student_id": payload.get("student_id"),
        "petition_type": payload.get("petition_type", "exception"),
        "requested_exception": payload.get("requested_exception"),
        "decision": payload.get("decision", "submitted"),
        "evidence": tuple(payload.get("evidence", ())),
        "granted_competency_waiver": payload.get("granted_competency_waiver"),
        "blockers": tuple(blockers),
    }
    next_state["petitions"][petition_id] = petition
    _record_exception(next_state, "academic_petition", petition_id, petition["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleUpdated",
        {"entity": "academic_petition", "id": petition_id, "blockers": petition["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "academic_petition": petition, "side_effects": ()}


def record_transfer_credit(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    evaluation_id = payload.get("evaluation_id") or f"trn-{_digest((payload.get('student_id'), payload.get('source_institution')))[:8]}"
    blockers = []
    if float(payload.get("credits_awarded", 0.0)) <= 0:
        blockers.append("credits_awarded_required")
    if not payload.get("equivalency"):
        blockers.append("equivalency_required")
    transfer_credit = {
        "id": evaluation_id,
        "table": "education_student_lifecycle_transfer_credit_evaluation",
        "student_id": payload.get("student_id"),
        "source_institution": payload.get("source_institution"),
        "source_course": payload.get("source_course"),
        "equivalency": payload.get("equivalency"),
        "credits_awarded": float(payload.get("credits_awarded", 0.0)),
        "applicability": payload.get("applicability", "program"),
        "status": payload.get("status", "approved"),
        "blockers": tuple(blockers),
    }
    next_state["transfer_credits"][evaluation_id] = transfer_credit
    _record_exception(next_state, "transfer_credit_evaluation", evaluation_id, transfer_credit["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleApproved",
        {"entity": "transfer_credit_evaluation", "id": evaluation_id, "blockers": transfer_credit["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "transfer_credit_evaluation": transfer_credit, "side_effects": ()}


def evaluate_degree_audit(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    student_id = payload.get("student_id")
    plan = payload.get("curriculum_plan") or _latest_for_student(next_state["curriculum_plans"], student_id)
    if plan is None:
        return {"ok": False, "state": next_state, "reason": "curriculum_plan_missing", "side_effects": ()}
    earned_from_attempts = sum(
        attempt.get("earned_credits", 0.0)
        for attempt in next_state["course_attempts"].values()
        if attempt.get("student_id") == student_id
    )
    earned_from_transfer = sum(
        transfer.get("credits_awarded", 0.0)
        for transfer in next_state["transfer_credits"].values()
        if transfer.get("student_id") == student_id and transfer.get("status") == "approved"
    )
    earned_credits = round(earned_from_attempts + earned_from_transfer, 2)
    achieved_competencies = set()
    for assessment in next_state["assessments"].values():
        if assessment.get("student_id") == student_id and assessment.get("achieved") and assessment.get("moderation_status") == "final":
            achieved_competencies.update(assessment.get("competencies", ()))
    for petition in next_state["petitions"].values():
        if petition.get("student_id") == student_id and petition.get("decision") == "approved" and petition.get("granted_competency_waiver"):
            achieved_competencies.add(petition["granted_competency_waiver"])
    required_competencies = set(plan.get("required_competencies", ()))
    unmet_competencies = tuple(sorted(required_competencies - achieved_competencies))
    remaining_credits = max(0.0, round(float(plan.get("required_credits", 0)) - earned_credits, 2))
    blockers = []
    if remaining_credits > 0:
        blockers.append("remaining_credit_requirement")
    if unmet_competencies:
        blockers.append("unmet_competency_requirement")
    if _active_holds(next_state, student_id, "graduate"):
        blockers.append("graduation_blocking_hold_present")
    audit_id = payload.get("audit_id") or f"audit-{_digest((student_id, plan.get('id'), earned_credits))[:8]}"
    audit = {
        "id": audit_id,
        "table": "education_student_lifecycle_degree_audit",
        "student_id": student_id,
        "curriculum_plan_id": plan.get("id"),
        "earned_credits": earned_credits,
        "required_credits": float(plan.get("required_credits", 0)),
        "remaining_credits": remaining_credits,
        "unmet_competencies": unmet_competencies,
        "status": "complete" if not blockers else "incomplete",
        "blockers": tuple(blockers),
    }
    next_state["degree_audits"][audit_id] = audit
    _record_exception(next_state, "degree_audit", audit_id, audit["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if blockers else "EducationStudentLifecycleApproved",
        {"entity": "degree_audit", "id": audit_id, "blockers": audit["blockers"]},
    )
    return {"ok": not blockers, "state": next_state, "degree_audit": audit, "side_effects": ()}


def project_student_risk(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    student_id = payload.get("student_id")
    engagement = _latest_for_student(next_state["engagement_projections"], student_id)
    hold_count = len(_active_holds(next_state, student_id, "register_course"))
    open_petitions = sum(1 for petition in next_state["petitions"].values() if petition.get("student_id") == student_id and petition.get("decision") != "approved")
    gpa = float(payload.get("gpa", 3.0))
    attendance_rate = float(payload.get("attendance_rate", (engagement or {}).get("attendance_rate", 1.0)))
    score = 0.2
    score += 0.25 if attendance_rate < 0.8 else 0.0
    score += 0.2 if gpa < 2.0 else 0.0
    score += 0.15 * hold_count
    score += 0.1 * open_petitions
    score += float((engagement or {}).get("risk_contribution", 0.0))
    score = round(min(0.99, score), 2)
    band = "high" if score >= 0.75 else "medium" if score >= 0.45 else "low"
    risk_id = payload.get("risk_id") or f"risk-{_digest((student_id, score, band))[:8]}"
    signal = {
        "id": risk_id,
        "table": "education_student_lifecycle_student_risk_signal",
        "student_id": student_id,
        "risk_score": score,
        "risk_band": band,
        "attendance_rate": attendance_rate,
        "gpa": gpa,
        "hold_count": hold_count,
        "human_review_required": band == "high",
        "recommended_intervention": "advisor_review" if band == "high" else "monitor",
    }
    next_state["risk_signals"][risk_id] = signal
    _record_exception(next_state, "student_risk_signal", risk_id, ("human_review_required",) if signal["human_review_required"] else ())
    _emit(next_state, "EducationStudentLifecycleUpdated", {"entity": "student_risk_signal", "id": risk_id, "risk_band": band})
    return {"ok": True, "state": next_state, "student_risk_signal": signal, "side_effects": ()}


def prepare_graduation_clearance(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    student_id = payload.get("student_id")
    audit = payload.get("degree_audit") or _latest_for_student(next_state["degree_audits"], student_id)
    blockers = []
    if audit is None:
        blockers.append("degree_audit_missing")
    elif audit.get("status") != "complete":
        blockers.extend(audit.get("blockers", ()))
    if _active_holds(next_state, student_id, "graduate"):
        blockers.append("graduation_blocking_hold_present")
    clearance_id = payload.get("clearance_id") or f"clear-{_digest((student_id, audit and audit.get('id')))[:8]}"
    clearance = {
        "id": clearance_id,
        "table": "education_student_lifecycle_graduation_clearance",
        "student_id": student_id,
        "degree_audit_id": audit and audit.get("id"),
        "status": "ready" if not blockers else "blocked",
        "advisor_approved": bool(payload.get("advisor_approved", not blockers)),
        "registrar_approved": bool(payload.get("registrar_approved", not blockers)),
        "blockers": tuple(dict.fromkeys(blockers)),
    }
    next_state["graduation_clearances"][clearance_id] = clearance
    _record_exception(next_state, "graduation_clearance", clearance_id, clearance["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if clearance["blockers"] else "EducationStudentLifecycleApproved",
        {"entity": "graduation_clearance", "id": clearance_id, "blockers": clearance["blockers"]},
    )
    return {"ok": not clearance["blockers"], "state": next_state, "graduation_clearance": clearance, "side_effects": ()}


def award_credential(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    student_id = payload.get("student_id")
    clearance = payload.get("graduation_clearance") or _latest_for_student(next_state["graduation_clearances"], student_id)
    blockers = []
    if clearance is None:
        blockers.append("graduation_clearance_missing")
    elif clearance.get("status") != "ready":
        blockers.extend(clearance.get("blockers", ()))
    credential_id = payload.get("credential_id") or f"cred-{_digest((student_id, payload.get('credential_type')))[:8]}"
    credential = {
        "id": credential_id,
        "table": "education_student_lifecycle_credential",
        "student_id": student_id,
        "credential_type": payload.get("credential_type", "degree"),
        "program_code": payload.get("program_code"),
        "conferral_date": payload.get("conferral_date"),
        "honors": payload.get("honors"),
        "certificate_number": payload.get("certificate_number") or f"CERT-{credential_id[-6:].upper()}",
        "status": "conferred" if not blockers else "blocked",
        "blockers": tuple(dict.fromkeys(blockers)),
    }
    next_state["credentials"][credential_id] = credential
    _record_exception(next_state, "credential", credential_id, credential["blockers"])
    _emit(
        next_state,
        "EducationStudentLifecycleExceptionOpened" if credential["blockers"] else "EducationStudentLifecycleApproved",
        {"entity": "credential", "id": credential_id, "blockers": credential["blockers"]},
    )
    return {"ok": not credential["blockers"], "state": next_state, "credential": credential, "side_effects": ()}


def build_student_lifecycle_workbench(state: dict) -> dict:
    applicants = tuple(state["applicants"].values())
    course_attempts = tuple(state["course_attempts"].values())
    risk_signals = tuple(state["risk_signals"].values())
    interventions = tuple(state["interventions"].values())
    petitions = tuple(state["petitions"].values())
    audits = tuple(state["degree_audits"].values())
    clearances = tuple(state["graduation_clearances"].values())
    queues = {
        "admissions_readiness": tuple(
            applicant
            for applicant in applicants
            if not applicant.get("missing_documents") and applicant.get("application_stage") in {"document_review", "decision_ready", "accepted"}
        ),
        "registration_blockers": tuple(attempt for attempt in course_attempts if attempt.get("blockers")),
        "high_risk_students": tuple(signal for signal in risk_signals if signal.get("risk_band") == "high"),
        "intervention_follow_up": tuple(intervention for intervention in interventions if intervention.get("reviewer_confirmed") is False or intervention.get("due_date")),
        "petition_review": tuple(petition for petition in petitions if petition.get("decision") in {"submitted", "committee_review"}),
        "graduation_candidates": tuple(audit for audit in audits if audit.get("status") == "complete"),
        "credential_clearance": tuple(clearance for clearance in clearances if clearance.get("status") != "ready"),
        "exception_backlog": tuple(state["exceptions"].values()),
    }
    return {"ok": True, "pbc": PBC_KEY, "queues": queues, "queue_counts": {name: len(items) for name, items in queues.items()}, "side_effects": ()}


def document_instruction_mutation_plan(document: str, instruction: str) -> dict:
    text = f"{document} {instruction}".lower()
    routes = (
        ("transcript", "review_applicant_documents", "education_student_lifecycle_applicant_document_evidence"),
        ("essay", "review_applicant_documents", "education_student_lifecycle_applicant_document_evidence"),
        ("petition", "submit_academic_petition", "education_student_lifecycle_academic_petition"),
        ("waiver", "submit_academic_petition", "education_student_lifecycle_academic_petition"),
        ("risk", "project_student_risk", "education_student_lifecycle_student_risk_signal"),
        ("attendance", "project_student_risk", "education_student_lifecycle_student_risk_signal"),
        ("degree audit", "evaluate_degree_audit", "education_student_lifecycle_degree_audit"),
        ("graduation", "prepare_graduation_clearance", "education_student_lifecycle_graduation_clearance"),
        ("credential", "award_credential", "education_student_lifecycle_credential"),
        ("register course", "register_course_attempt", "education_student_lifecycle_course_attempt"),
        ("advising", "open_advising_case", "education_student_lifecycle_advising_case"),
    )
    selected = next((item for item in routes if item[0] in text), None)
    keyword, operation, target_table = selected or ("applicant", "register_student_applicant", "education_student_lifecycle_student_applicant")
    return {
        "ok": True,
        "document_digest": _digest(document),
        "instruction_digest": _digest(instruction),
        "matched_keyword": keyword,
        "proposed_operation": operation,
        "target_table": target_table,
        "requires_confirmation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def forms_contract() -> dict:
    forms = (
        {"form_id": "student_applicant_intake", "command": "register_student_applicant", "table": "education_student_lifecycle_student_applicant"},
        {"form_id": "applicant_document_review", "command": "review_applicant_documents", "table": "education_student_lifecycle_applicant_document_evidence"},
        {"form_id": "student_enrollment_activation", "command": "activate_enrollment", "table": "education_student_lifecycle_enrollment"},
        {"form_id": "curriculum_plan_editor", "command": "maintain_curriculum_plan", "table": "education_student_lifecycle_curriculum_plan"},
        {"form_id": "course_registration", "command": "register_course_attempt", "table": "education_student_lifecycle_course_attempt"},
        {"form_id": "assessment_finalization", "command": "finalize_assessment_result", "table": "education_student_lifecycle_assessment_result"},
        {"form_id": "advising_case", "command": "open_advising_case", "table": "education_student_lifecycle_advising_case"},
        {"form_id": "academic_petition", "command": "submit_academic_petition", "table": "education_student_lifecycle_academic_petition"},
        {"form_id": "credential_conferral", "command": "award_credential", "table": "education_student_lifecycle_credential"},
    )
    return {"ok": True, "forms": forms, "side_effects": ()}


def wizards_contract() -> dict:
    wizards = (
        {"wizard_id": "applicant_to_matriculation_wizard", "steps": ("register_student_applicant", "review_applicant_documents", "activate_enrollment")},
        {"wizard_id": "student_success_intervention_wizard", "steps": ("open_advising_case", "project_student_risk", "record_intervention_plan")},
        {"wizard_id": "graduation_clearance_wizard", "steps": ("evaluate_degree_audit", "prepare_graduation_clearance", "award_credential")},
        {"wizard_id": "first_run_setup_wizard", "steps": ("maintain_curriculum_plan", "record_hold_projection", "record_engagement_projection")},
    )
    return {"ok": True, "wizards": wizards, "side_effects": ()}


def controls_contract() -> dict:
    controls = (
        {"control_id": "applicant_decision_readiness", "command": "register_student_applicant", "blocks_on_failure": True},
        {"control_id": "course_registration_gate", "command": "register_course_attempt", "blocks_on_failure": True},
        {"control_id": "risk_intervention_human_review", "command": "record_intervention_plan", "blocks_on_failure": True},
        {"control_id": "graduation_clearance_gate", "command": "prepare_graduation_clearance", "blocks_on_failure": True},
        {"control_id": "credential_conferral_gate", "command": "award_credential", "blocks_on_failure": True},
    )
    return {"ok": True, "controls": controls, "side_effects": ()}


def single_pbc_app_contract() -> dict:
    queues = tuple(build_student_lifecycle_workbench(empty_student_lifecycle_state())["queue_counts"].keys())
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
        "owned_tables": OWNED_TABLES,
        "commands": (
            "register_student_applicant",
            "review_applicant_documents",
            "activate_enrollment",
            "maintain_curriculum_plan",
            "record_hold_projection",
            "record_engagement_projection",
            "register_course_attempt",
            "finalize_assessment_result",
            "open_advising_case",
            "record_intervention_plan",
            "submit_academic_petition",
            "record_transfer_credit",
            "evaluate_degree_audit",
            "project_student_risk",
            "prepare_graduation_clearance",
            "award_credential",
        ),
        "queries": ("build_student_lifecycle_workbench",),
        "forms": forms_contract()["forms"],
        "wizards": wizards_contract()["wizards"],
        "controls": controls_contract()["controls"],
        "queues": queues,
        "side_effects": (),
    }


def student_lifecycle_app_smoke_test() -> dict:
    state = empty_student_lifecycle_state()
    applicant = register_student_applicant(
        state,
        {
            "applicant_id": "app-smoke",
            "student_name": "Smoke Student",
            "program_code": "BSCS",
            "intake_term": "2026-FALL",
            "catalog_year": 2026,
            "application_stage": "accepted",
            "decision_status": "accepted",
            "required_documents": (),
        },
    )
    enrollment = activate_enrollment(applicant["state"], {"applicant_id": "app-smoke", "student_id": "student-smoke", "term": "2026-FALL"})
    plan = maintain_curriculum_plan(
        enrollment["state"],
        {
            "student_id": "student-smoke",
            "program_code": "BSCS",
            "catalog_year": 2026,
            "required_credits": 6,
            "requirements": ("CS101", "CS102"),
            "required_competencies": ("communication",),
        },
    )
    course = register_course_attempt(
        plan["state"],
        {
            "student_id": "student-smoke",
            "course_code": "CS101",
            "term": "2026-FALL",
            "status": "completed",
            "grade": "A",
            "credits": 3,
            "prerequisites_satisfied": True,
        },
    )
    transfer = record_transfer_credit(
        course["state"],
        {
            "student_id": "student-smoke",
            "source_institution": "Regional College",
            "source_course": "ENG101",
            "equivalency": "GEN-communication",
            "credits_awarded": 3,
        },
    )
    assessment = finalize_assessment_result(
        transfer["state"],
        {
            "student_id": "student-smoke",
            "assessment_type": "capstone",
            "score": 88,
            "competencies": ("communication",),
            "achieved": True,
            "moderation_status": "final",
            "scorer": "faculty-1",
        },
    )
    audit = evaluate_degree_audit(assessment["state"], {"student_id": "student-smoke"})
    clearance = prepare_graduation_clearance(audit["state"], {"student_id": "student-smoke"})
    credential = award_credential(clearance["state"], {"student_id": "student-smoke", "program_code": "BSCS"})
    workbench = build_student_lifecycle_workbench(credential["state"])
    app = single_pbc_app_contract()
    checks = (
        applicant["ok"],
        enrollment["ok"],
        plan["ok"],
        course["ok"],
        transfer["ok"],
        assessment["ok"],
        audit["ok"],
        clearance["ok"],
        credential["ok"],
        workbench["ok"],
        app["ok"],
    )
    return {"ok": all(checks), "state": credential["state"], "workbench": workbench, "single_pbc_app": app, "side_effects": ()}
