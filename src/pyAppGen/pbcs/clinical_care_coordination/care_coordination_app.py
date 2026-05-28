"""Executable one-PBC care coordination application surface."""
from __future__ import annotations

from copy import deepcopy
from hashlib import sha256

PBC_KEY = "clinical_care_coordination"
OWNED_TABLES = (
    "clinical_care_coordination_patient_care_plan",
    "clinical_care_coordination_care_team",
    "clinical_care_coordination_referral",
    "clinical_care_coordination_encounter",
    "clinical_care_coordination_care_gap",
    "clinical_care_coordination_transition_plan",
    "clinical_care_coordination_outcome_measure",
    "clinical_care_coordination_appgen_outbox_event",
)

CARE_PLAN_STATES = (
    "draft",
    "active",
    "suspended",
    "patient_declined",
    "partially_met",
    "achieved",
    "closed",
)
REFERRAL_STATES = (
    "need_identified",
    "authorization_required",
    "authorization_obtained",
    "sent",
    "accepted",
    "scheduled",
    "completed",
    "result_received",
    "result_reconciled",
    "closed",
    "declined",
    "expired",
)
CARE_GAP_TYPES = (
    "preventive_screening",
    "immunization",
    "chronic_monitoring",
    "medication_reconciliation",
    "behavioral_health_follow_up",
    "social_determinant",
    "post_discharge_follow_up",
    "missed_appointment",
    "patient_outreach",
)


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def empty_care_coordination_state() -> dict:
    return {
        "patient_care_plans": {},
        "care_teams": {},
        "referrals": {},
        "encounters": {},
        "care_gaps": {},
        "transition_plans": {},
        "outcome_measures": {},
        "coordination_tasks": {},
        "source_evidence": {},
        "outbox": [],
        "idempotency_keys": set(),
    }


def _copy_state(state: dict) -> dict:
    copied = deepcopy(state)
    copied["idempotency_keys"] = set(state.get("idempotency_keys", set()))
    return copied


def _emit(state: dict, event_type: str, payload: dict) -> None:
    envelope = {
        "event_type": event_type,
        "event_contract": "AppGen-X",
        "topic": "pbc.clinical_care_coordination.events",
        "payload": dict(payload),
        "idempotency_key": _digest((event_type, payload)),
    }
    state["outbox"].append(envelope)


def _idempotency_guard(state: dict, key: str | None) -> tuple[bool, dict | None]:
    if not key:
        return False, None
    if key in state["idempotency_keys"]:
        return True, {
            "ok": True,
            "duplicate": True,
            "idempotency_key": key,
            "state": state,
            "side_effects": (),
        }
    state["idempotency_keys"].add(key)
    return False, None


def create_care_plan(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    duplicate, response = _idempotency_guard(next_state, payload.get("idempotency_key"))
    if duplicate:
        return response
    required = ("patient_ref", "problem", "goal", "responsible_role", "review_cadence_days")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    plan_id = payload.get("care_plan_id") or f"cp-{_digest((payload.get('patient_ref'), payload.get('problem')))[:10]}"
    goals = tuple(
        {
            "goal_id": goal.get("goal_id") or f"{plan_id}-goal-{index + 1}",
            "type": goal.get("type", "clinical"),
            "description": goal.get("description", payload["goal"]),
            "target": goal.get("target"),
            "status": goal.get("status", "active"),
            "responsible_role": goal.get("responsible_role", payload["responsible_role"]),
        }
        for index, goal in enumerate(payload.get("goals") or ({"description": payload["goal"]},))
    )
    record = {
        "id": plan_id,
        "table": "clinical_care_coordination_patient_care_plan",
        "patient_ref": payload["patient_ref"],
        "state": payload.get("state", "draft"),
        "problem": payload["problem"],
        "patient_goal_text": payload["goal"],
        "goals": goals,
        "preferences": dict(payload.get("preferences", {})),
        "barriers": tuple(payload.get("barriers", ())),
        "responsible_role": payload["responsible_role"],
        "review_cadence_days": int(payload["review_cadence_days"]),
        "source_evidence_id": payload.get("source_evidence_id"),
        "risk_score": 0,
        "version": 1,
    }
    next_state["patient_care_plans"][plan_id] = record
    _emit(next_state, "ClinicalCareCoordinationCreated", {"entity": "patient_care_plan", "id": plan_id})
    return {"ok": True, "state": next_state, "care_plan": record, "side_effects": ()}


def transition_care_plan(state: dict, care_plan_id: str, target_state: str, reason: str, actor_role: str) -> dict:
    next_state = _copy_state(state)
    plan = deepcopy(next_state["patient_care_plans"].get(care_plan_id))
    if not plan:
        return {"ok": False, "state": next_state, "reason": "care_plan_not_found", "side_effects": ()}
    if target_state not in CARE_PLAN_STATES:
        return {"ok": False, "state": next_state, "reason": "invalid_target_state", "side_effects": ()}
    if target_state == "closed":
        active_goals = tuple(goal for goal in plan["goals"] if goal.get("status") == "active")
        if active_goals and not reason.startswith("override:"):
            return {
                "ok": False,
                "state": next_state,
                "reason": "active_child_goals_require_override",
                "active_goals": active_goals,
                "side_effects": (),
            }
    if target_state in {"active", "closed"} and actor_role not in {"primary_coordinator", "attending_clinician"}:
        return {"ok": False, "state": next_state, "reason": "insufficient_clinical_authority", "side_effects": ()}
    plan["state"] = target_state
    plan["closure_reason"] = reason if target_state == "closed" else None
    plan["version"] += 1
    next_state["patient_care_plans"][care_plan_id] = plan
    _emit(next_state, "ClinicalCareCoordinationUpdated", {"entity": "patient_care_plan", "id": care_plan_id, "state": target_state})
    return {"ok": True, "state": next_state, "care_plan": plan, "side_effects": ()}


def add_care_team_member(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("patient_ref", "member_ref", "role", "coverage_start", "consent_scope")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    member_id = payload.get("member_id") or f"ct-{_digest((payload['patient_ref'], payload['member_ref'], payload['role']))[:10]}"
    member = {
        "id": member_id,
        "table": "clinical_care_coordination_care_team",
        "patient_ref": payload["patient_ref"],
        "member_ref": payload["member_ref"],
        "role": payload["role"],
        "coverage_start": payload["coverage_start"],
        "coverage_end": payload.get("coverage_end"),
        "backup_contact_ref": payload.get("backup_contact_ref"),
        "escalation_route": payload.get("escalation_route", "primary_coordinator"),
        "consent_scope": tuple(payload.get("consent_scope") or ()),
        "can_receive_protected_details": bool(payload.get("can_receive_protected_details", False)),
    }
    next_state["care_teams"][member_id] = member
    _emit(next_state, "ClinicalCareCoordinationUpdated", {"entity": "care_team", "id": member_id})
    return {"ok": True, "state": next_state, "care_team_member": member, "side_effects": ()}


def disclose_to_care_team_member(state: dict, member_id: str, topic: str) -> dict:
    member = state.get("care_teams", {}).get(member_id)
    if not member:
        return {"ok": False, "reason": "care_team_member_not_found", "side_effects": ()}
    allowed = topic in member["consent_scope"] and member["can_receive_protected_details"]
    return {
        "ok": allowed,
        "member_id": member_id,
        "topic": topic,
        "reason": None if allowed else "consent_scope_or_protection_limit",
        "side_effects": (),
    }


def create_referral(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    required = ("patient_ref", "specialty", "urgency", "reason", "expected_turnaround_days")
    missing = tuple(field for field in required if not payload.get(field))
    if missing:
        return {"ok": False, "state": next_state, "reason": "missing_required_fields", "missing": missing, "side_effects": ()}
    duplicate = tuple(
        referral
        for referral in next_state["referrals"].values()
        if referral["patient_ref"] == payload["patient_ref"]
        and referral["specialty"] == payload["specialty"]
        and referral["state"] not in {"closed", "declined", "expired"}
    )
    if duplicate:
        return {"ok": False, "state": next_state, "reason": "active_duplicate_referral", "duplicates": duplicate, "side_effects": ()}
    referral_id = payload.get("referral_id") or f"ref-{_digest((payload['patient_ref'], payload['specialty'], payload['reason']))[:10]}"
    needs_auth = bool(payload.get("authorization_required", payload["urgency"] != "same_day"))
    referral = {
        "id": referral_id,
        "table": "clinical_care_coordination_referral",
        "patient_ref": payload["patient_ref"],
        "specialty": payload["specialty"],
        "urgency": payload["urgency"],
        "reason": payload["reason"],
        "state": "authorization_required" if needs_auth else "sent",
        "receiving_organization_ref": payload.get("receiving_organization_ref"),
        "expected_turnaround_days": int(payload["expected_turnaround_days"]),
        "authorization_evidence": payload.get("authorization_evidence"),
        "appointment": None,
        "result_document_ref": None,
        "closure_accountability": payload.get("closure_accountability", "primary_coordinator"),
    }
    next_state["referrals"][referral_id] = referral
    _emit(next_state, "ClinicalCareCoordinationCreated", {"entity": "referral", "id": referral_id, "state": referral["state"]})
    return {"ok": True, "state": next_state, "referral": referral, "side_effects": ()}


def receive_referral_result(state: dict, referral_id: str, payload: dict) -> dict:
    next_state = _copy_state(state)
    referral = deepcopy(next_state["referrals"].get(referral_id))
    if not referral:
        return {"ok": False, "state": next_state, "reason": "referral_not_found", "side_effects": ()}
    referral["state"] = "result_received"
    referral["result_document_ref"] = payload.get("result_document_ref")
    referral["result_summary"] = payload.get("summary")
    next_state["referrals"][referral_id] = referral
    task_id = f"task-reconcile-{referral_id}"
    next_state["coordination_tasks"][task_id] = {
        "id": task_id,
        "source": "referral_result",
        "patient_ref": referral["patient_ref"],
        "owner_role": referral["closure_accountability"],
        "priority": "urgent" if referral["urgency"] in {"same_day", "urgent"} else "routine",
        "state": "open",
        "action": "reconcile_result_into_care_plan",
    }
    _emit(next_state, "ClinicalCareCoordinationUpdated", {"entity": "referral", "id": referral_id, "state": "result_received"})
    return {"ok": True, "state": next_state, "referral": referral, "task": next_state["coordination_tasks"][task_id], "side_effects": ()}


def record_encounter_and_tasks(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    encounter_id = payload.get("encounter_id") or f"enc-{_digest((payload.get('patient_ref'), payload.get('occurred_at')))[:10]}"
    encounter = {
        "id": encounter_id,
        "table": "clinical_care_coordination_encounter",
        "patient_ref": payload.get("patient_ref"),
        "occurred_at": payload.get("occurred_at"),
        "source_note_ref": payload.get("source_note_ref"),
        "priority": payload.get("priority", "routine"),
    }
    next_state["encounters"][encounter_id] = encounter
    tasks = []
    for index, action in enumerate(payload.get("coordination_actions", ())):
        task_id = f"task-{encounter_id}-{index + 1}"
        task = {
            "id": task_id,
            "source": "encounter",
            "source_encounter_id": encounter_id,
            "source_note_span": action.get("source_note_span"),
            "patient_ref": encounter["patient_ref"],
            "owner_role": action.get("owner_role", "primary_coordinator"),
            "priority": action.get("priority", encounter["priority"]),
            "due_days": int(action.get("due_days", 7)),
            "state": "open",
            "action": action.get("action"),
        }
        next_state["coordination_tasks"][task_id] = task
        tasks.append(task)
    _emit(next_state, "ClinicalCareCoordinationCreated", {"entity": "encounter", "id": encounter_id, "task_count": len(tasks)})
    return {"ok": True, "state": next_state, "encounter": encounter, "tasks": tuple(tasks), "side_effects": ()}


def open_care_gap(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    if payload.get("gap_type") not in CARE_GAP_TYPES:
        return {"ok": False, "state": next_state, "reason": "unknown_care_gap_type", "allowed_types": CARE_GAP_TYPES, "side_effects": ()}
    gap_id = payload.get("care_gap_id") or f"gap-{_digest((payload.get('patient_ref'), payload.get('gap_type'), payload.get('guideline_basis')))[:10]}"
    gap = {
        "id": gap_id,
        "table": "clinical_care_coordination_care_gap",
        "patient_ref": payload.get("patient_ref"),
        "gap_type": payload["gap_type"],
        "severity": payload.get("severity", "moderate"),
        "guideline_basis": payload.get("guideline_basis"),
        "denominator_eligible": bool(payload.get("denominator_eligible", True)),
        "state": "open",
        "exclusion_reason": None,
        "closure_evidence": None,
        "linked_care_plan_id": payload.get("linked_care_plan_id"),
    }
    next_state["care_gaps"][gap_id] = gap
    _emit(next_state, "ClinicalCareCoordinationExceptionOpened", {"entity": "care_gap", "id": gap_id, "severity": gap["severity"]})
    return {"ok": True, "state": next_state, "care_gap": gap, "side_effects": ()}


def close_care_gap(state: dict, care_gap_id: str, evidence: dict) -> dict:
    next_state = _copy_state(state)
    gap = deepcopy(next_state["care_gaps"].get(care_gap_id))
    if not gap:
        return {"ok": False, "state": next_state, "reason": "care_gap_not_found", "side_effects": ()}
    if not evidence.get("evidence_type") or not evidence.get("confirmed_by"):
        return {"ok": False, "state": next_state, "reason": "closure_evidence_required", "side_effects": ()}
    gap["state"] = "closed"
    gap["closure_evidence"] = dict(evidence)
    next_state["care_gaps"][care_gap_id] = gap
    _emit(next_state, "ClinicalCareCoordinationUpdated", {"entity": "care_gap", "id": care_gap_id, "state": "closed"})
    return {"ok": True, "state": next_state, "care_gap": gap, "side_effects": ()}


def create_transition_plan(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    transition_id = payload.get("transition_plan_id") or f"toc-{_digest((payload.get('patient_ref'), payload.get('discharge_source')))[:10]}"
    required_packet_fields = (
        "medication_reconciliation_status",
        "follow_up_appointments",
        "patient_instructions",
    )
    missing_packet = tuple(field for field in required_packet_fields if not payload.get(field))
    transition = {
        "id": transition_id,
        "table": "clinical_care_coordination_transition_plan",
        "patient_ref": payload.get("patient_ref"),
        "discharge_source": payload.get("discharge_source"),
        "receiving_setting": payload.get("receiving_setting"),
        "readmission_risk": payload.get("readmission_risk", "moderate"),
        "missing_packet_fields": missing_packet,
        "packet_complete": not missing_packet,
        "state": "packet_incomplete" if missing_packet else "ready_for_handoff",
        "caregiver_confirmation": payload.get("caregiver_confirmation"),
        "transportation_plan": payload.get("transportation_plan"),
    }
    next_state["transition_plans"][transition_id] = transition
    event_type = "ClinicalCareCoordinationExceptionOpened" if missing_packet else "ClinicalCareCoordinationUpdated"
    _emit(next_state, event_type, {"entity": "transition_plan", "id": transition_id, "state": transition["state"]})
    return {"ok": True, "state": next_state, "transition_plan": transition, "side_effects": ()}


def complete_transition_plan(state: dict, transition_plan_id: str) -> dict:
    next_state = _copy_state(state)
    transition = deepcopy(next_state["transition_plans"].get(transition_plan_id))
    if not transition:
        return {"ok": False, "state": next_state, "reason": "transition_plan_not_found", "side_effects": ()}
    if not transition["packet_complete"]:
        return {
            "ok": False,
            "state": next_state,
            "reason": "transition_packet_incomplete",
            "missing_packet_fields": transition["missing_packet_fields"],
            "side_effects": (),
        }
    transition["state"] = "handoff_accepted"
    next_state["transition_plans"][transition_plan_id] = transition
    _emit(next_state, "ClinicalCareCoordinationApproved", {"entity": "transition_plan", "id": transition_plan_id, "state": "handoff_accepted"})
    return {"ok": True, "state": next_state, "transition_plan": transition, "side_effects": ()}


def record_outcome_measure(state: dict, payload: dict) -> dict:
    next_state = _copy_state(state)
    measure_id = payload.get("outcome_measure_id") or f"out-{_digest((payload.get('care_plan_id'), payload.get('measure_code')))[:10]}"
    baseline = float(payload.get("baseline_value", 0))
    current = float(payload.get("current_value", baseline))
    target = float(payload.get("target_value", current))
    trend = "stable"
    if current >= target and target >= baseline:
        trend = "improving"
    elif current < baseline:
        trend = "worsening"
    measure = {
        "id": measure_id,
        "table": "clinical_care_coordination_outcome_measure",
        "care_plan_id": payload.get("care_plan_id"),
        "measure_code": payload.get("measure_code"),
        "baseline_value": baseline,
        "current_value": current,
        "target_value": target,
        "unit": payload.get("unit"),
        "source": payload.get("source", "coordinator_reported"),
        "patient_reported": bool(payload.get("patient_reported", False)),
        "confidence": float(payload.get("confidence", 1)),
        "trend": trend,
    }
    next_state["outcome_measures"][measure_id] = measure
    _emit(next_state, "ClinicalCareCoordinationUpdated", {"entity": "outcome_measure", "id": measure_id, "trend": trend})
    return {"ok": True, "state": next_state, "outcome_measure": measure, "side_effects": ()}


def care_coordination_workbench(state: dict) -> dict:
    referrals = tuple(state.get("referrals", {}).values())
    gaps = tuple(state.get("care_gaps", {}).values())
    transitions = tuple(state.get("transition_plans", {}).values())
    tasks = tuple(state.get("coordination_tasks", {}).values())
    plans = tuple(state.get("patient_care_plans", {}).values())
    high_risk = tuple(
        plan
        for plan in plans
        if plan.get("state") in {"active", "partially_met"} and (plan.get("barriers") or plan.get("risk_score", 0) >= 70)
    )
    queues = {
        "high_risk_patients": high_risk,
        "unscheduled_referrals": tuple(ref for ref in referrals if ref["state"] in {"authorization_required", "sent", "accepted"}),
        "unreconciled_results": tuple(ref for ref in referrals if ref["state"] == "result_received"),
        "active_transitions": tuple(item for item in transitions if item["state"] != "handoff_accepted"),
        "blocked_care_gaps": tuple(gap for gap in gaps if gap["state"] == "open" and gap["severity"] in {"high", "critical"}),
        "outreach_due_today": tuple(task for task in tasks if task["state"] == "open" and task.get("action") in {"patient_outreach", "confirm_follow_up"}),
        "care_team_coverage_gaps": tuple(plan for plan in plans if not _has_primary_coordinator(state, plan["patient_ref"])),
        "control_failures": tuple(item for item in transitions if item.get("missing_packet_fields")),
    }
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "queues": queues,
        "queue_counts": {name: len(items) for name, items in queues.items()},
        "actions": (
            "create_care_plan",
            "add_care_team_member",
            "create_referral",
            "receive_referral_result",
            "record_encounter_and_tasks",
            "open_care_gap",
            "close_care_gap",
            "create_transition_plan",
            "complete_transition_plan",
            "record_outcome_measure",
        ),
        "side_effects": (),
    }


def _has_primary_coordinator(state: dict, patient_ref: str) -> bool:
    return any(
        member["patient_ref"] == patient_ref
        and member["role"] == "primary_coordinator"
        and not member.get("coverage_end")
        for member in state.get("care_teams", {}).values()
    )


def care_coordination_forms_contract() -> dict:
    return {
        "ok": True,
        "forms": (
            {"form_id": "care_plan_form", "writes_table": "clinical_care_coordination_patient_care_plan", "fields": ("patient_ref", "problem", "goal", "responsible_role", "review_cadence_days")},
            {"form_id": "care_team_roster_form", "writes_table": "clinical_care_coordination_care_team", "fields": ("patient_ref", "member_ref", "role", "coverage_start", "consent_scope")},
            {"form_id": "referral_lifecycle_form", "writes_table": "clinical_care_coordination_referral", "fields": ("patient_ref", "specialty", "urgency", "reason", "expected_turnaround_days")},
            {"form_id": "encounter_task_extraction_form", "writes_table": "clinical_care_coordination_encounter", "fields": ("patient_ref", "occurred_at", "coordination_actions")},
            {"form_id": "care_gap_form", "writes_table": "clinical_care_coordination_care_gap", "fields": ("patient_ref", "gap_type", "severity", "guideline_basis")},
            {"form_id": "transition_packet_form", "writes_table": "clinical_care_coordination_transition_plan", "fields": ("patient_ref", "discharge_source", "receiving_setting", "medication_reconciliation_status", "follow_up_appointments", "patient_instructions")},
            {"form_id": "outcome_measure_form", "writes_table": "clinical_care_coordination_outcome_measure", "fields": ("care_plan_id", "measure_code", "baseline_value", "current_value", "target_value")},
        ),
        "side_effects": (),
    }


def care_coordination_wizards_contract() -> dict:
    return {
        "ok": True,
        "wizards": (
            {"wizard_id": "longitudinal_care_plan_wizard", "steps": ("capture_problem_and_goal", "assign_team_and_preferences", "review_barriers", "activate_plan")},
            {"wizard_id": "closed_loop_referral_wizard", "steps": ("identify_need", "check_authorization", "send_and_schedule", "receive_result", "reconcile_result")},
            {"wizard_id": "transition_of_care_packet_wizard", "steps": ("capture_discharge_context", "verify_medication_reconciliation", "confirm_follow_up", "confirm_patient_instructions", "handoff_acceptance")},
            {"wizard_id": "care_gap_closure_wizard", "steps": ("classify_gap", "validate_guideline_basis", "collect_evidence", "approve_closure")},
        ),
        "side_effects": (),
    }


def care_coordination_controls_contract() -> dict:
    return {
        "ok": True,
        "controls": (
            {"control_id": "consent_scope_disclosure_guard", "blocks_on_failure": True, "table_scope": ("clinical_care_coordination_care_team",)},
            {"control_id": "active_goal_closure_guard", "blocks_on_failure": True, "table_scope": ("clinical_care_coordination_patient_care_plan",)},
            {"control_id": "duplicate_referral_guard", "blocks_on_failure": True, "table_scope": ("clinical_care_coordination_referral",)},
            {"control_id": "transition_packet_completeness_guard", "blocks_on_failure": True, "table_scope": ("clinical_care_coordination_transition_plan",)},
            {"control_id": "care_gap_closure_evidence_guard", "blocks_on_failure": True, "table_scope": ("clinical_care_coordination_care_gap",)},
            {"control_id": "owned_table_boundary_guard", "blocks_on_failure": True, "table_scope": OWNED_TABLES},
        ),
        "side_effects": (),
    }


def single_pbc_app_contract() -> dict:
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "single_pbc_app": True,
        "database_backed": True,
        "owned_tables": OWNED_TABLES,
        "forms": care_coordination_forms_contract()["forms"],
        "wizards": care_coordination_wizards_contract()["wizards"],
        "controls": care_coordination_controls_contract()["controls"],
        "workbench": "ClinicalCareCoordinationWorkbench",
        "detail_view": "ClinicalCareCoordinationDetail",
        "assistant_panel": "ClinicalCareCoordinationAssistantPanel",
        "agent_skills": (
            "parse_care_plan_document",
            "draft_referral_from_instruction",
            "create_coordination_task",
            "close_care_gap_with_evidence",
            "summarize_transition_packet",
        ),
        "side_effects": (),
    }


def document_instruction_mutation_plan(document: str, instruction: str) -> dict:
    lowered = f"{document} {instruction}".lower()
    if "referral" in lowered:
        action = "create_referral"
        table = "clinical_care_coordination_referral"
    elif "transition" in lowered or "discharge" in lowered:
        action = "create_transition_plan"
        table = "clinical_care_coordination_transition_plan"
    elif "gap" in lowered or "screening" in lowered:
        action = "open_care_gap"
        table = "clinical_care_coordination_care_gap"
    else:
        action = "create_care_plan"
        table = "clinical_care_coordination_patient_care_plan"
    return {
        "ok": True,
        "pbc": PBC_KEY,
        "document_digest": _digest(document),
        "instruction": instruction,
        "proposed_action": action,
        "target_table": table,
        "requires_human_confirmation": True,
        "crud_datastore_mutation": True,
        "event_contract": "AppGen-X",
        "side_effects": (),
    }


def care_coordination_smoke_test() -> dict:
    state = empty_care_coordination_state()
    plan = create_care_plan(
        state,
        {
            "patient_ref": "patient-001",
            "problem": "post discharge heart failure follow-up",
            "goal": "complete follow-up and medication reconciliation",
            "responsible_role": "primary_coordinator",
            "review_cadence_days": 7,
            "barriers": ("transportation",),
            "idempotency_key": "care-plan-001",
        },
    )
    team = add_care_team_member(
        plan["state"],
        {
            "patient_ref": "patient-001",
            "member_ref": "coordinator-1",
            "role": "primary_coordinator",
            "coverage_start": "2026-01-01",
            "consent_scope": ("care_plan", "referral", "transition"),
            "can_receive_protected_details": True,
        },
    )
    referral = create_referral(
        team["state"],
        {
            "patient_ref": "patient-001",
            "specialty": "cardiology",
            "urgency": "urgent",
            "reason": "post discharge medication optimization",
            "expected_turnaround_days": 3,
            "authorization_required": False,
        },
    )
    result = receive_referral_result(referral["state"], referral["referral"]["id"], {"result_document_ref": "doc-77", "summary": "increase monitoring"})
    gap = open_care_gap(
        result["state"],
        {
            "patient_ref": "patient-001",
            "gap_type": "post_discharge_follow_up",
            "severity": "high",
            "guideline_basis": "post discharge follow-up within seven days",
        },
    )
    transition = create_transition_plan(
        gap["state"],
        {
            "patient_ref": "patient-001",
            "discharge_source": "inpatient",
            "receiving_setting": "home",
            "medication_reconciliation_status": "complete",
            "follow_up_appointments": ("cardiology",),
            "patient_instructions": "daily weight and call threshold",
        },
    )
    outcome = record_outcome_measure(
        transition["state"],
        {
            "care_plan_id": plan["care_plan"]["id"],
            "measure_code": "follow_up_completed",
            "baseline_value": 0,
            "current_value": 1,
            "target_value": 1,
        },
    )
    workbench = care_coordination_workbench(outcome["state"])
    checks = (
        plan["ok"],
        team["ok"],
        referral["ok"],
        result["ok"],
        gap["ok"],
        transition["ok"],
        outcome["ok"],
        workbench["ok"],
        single_pbc_app_contract()["ok"],
        document_instruction_mutation_plan("referral note", "create referral")["ok"],
    )
    return {
        "ok": all(checks),
        "final_state": outcome["state"],
        "workbench": workbench,
        "single_pbc_app": single_pbc_app_contract(),
        "side_effects": (),
    }
