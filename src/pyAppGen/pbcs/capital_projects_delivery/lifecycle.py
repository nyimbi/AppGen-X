"""Lifecycle helpers for capital project gate governance."""
from __future__ import annotations

from copy import deepcopy

INITIAL_STAGE = "idea"
LIFECYCLE_STAGES = (
    "idea",
    "screening",
    "fel",
    "approved_for_execution",
    "active_construction",
    "mechanical_completion",
    "ready_for_startup",
    "handover_complete",
    "closeout",
)

GATE_DEFINITIONS = {
    "idea": {
        "label": "Idea",
        "required_approver_role": "project_sponsor",
        "entry_criteria": (),
    },
    "screening": {
        "label": "Screening",
        "required_approver_role": "project_sponsor",
        "entry_criteria": ("business_case_defined", "sponsorship_assigned"),
    },
    "fel": {
        "label": "FEL",
        "required_approver_role": "project_controls_lead",
        "entry_criteria": ("screening_complete", "initial_risk_review"),
    },
    "approved_for_execution": {
        "label": "Approved For Execution",
        "required_approver_role": "investment_board",
        "entry_criteria": (
            "fel_complete",
            "funding_secured",
            "execution_plan_baselined",
        ),
    },
    "active_construction": {
        "label": "Active Construction",
        "required_approver_role": "construction_manager",
        "entry_criteria": (
            "execution_authorized",
            "packages_ready_for_construction",
        ),
    },
    "mechanical_completion": {
        "label": "Mechanical Completion",
        "required_approver_role": "construction_manager",
        "entry_criteria": (
            "construction_scope_complete",
            "system_turnover_plan_ready",
        ),
    },
    "ready_for_startup": {
        "label": "Ready For Startup",
        "required_approver_role": "commissioning_manager",
        "entry_criteria": (
            "mechanical_completion_certified",
            "commissioning_plan_approved",
        ),
    },
    "handover_complete": {
        "label": "Handover Complete",
        "required_approver_role": "operations_manager",
        "entry_criteria": ("startup_readiness_approved", "operations_docs_complete"),
    },
    "closeout": {
        "label": "Closeout",
        "required_approver_role": "project_controls_lead",
        "entry_criteria": ("handover_signed", "closeout_financials_reconciled"),
    },
}


def stage_catalog() -> tuple[dict, ...]:
    return tuple(
        {
            "stage": stage,
            "label": GATE_DEFINITIONS[stage]["label"],
            "required_approver_role": GATE_DEFINITIONS[stage]["required_approver_role"],
            "entry_criteria": GATE_DEFINITIONS[stage]["entry_criteria"],
        }
        for stage in LIFECYCLE_STAGES
    )


def normalize_criteria_status(criteria_status: dict | None) -> dict[str, bool]:
    return {
        str(name): bool(value)
        for name, value in dict(criteria_status or {}).items()
    }


def stage_index(stage: str) -> int:
    return LIFECYCLE_STAGES.index(stage)


def next_stage(stage: str) -> str | None:
    index = stage_index(stage)
    return LIFECYCLE_STAGES[index + 1] if index + 1 < len(LIFECYCLE_STAGES) else None


def required_criteria(stage: str) -> tuple[str, ...]:
    return GATE_DEFINITIONS[stage]["entry_criteria"]


def blocked_criteria(criteria_status: dict | None, target_stage: str | None) -> tuple[str, ...]:
    if not target_stage:
        return ()
    normalized = normalize_criteria_status(criteria_status)
    return tuple(
        criterion
        for criterion in required_criteria(target_stage)
        if not normalized.get(criterion, False)
    )


def transition_plan(current_stage: str, target_stage: str) -> dict:
    if current_stage not in GATE_DEFINITIONS:
        return {"ok": False, "reason": "unknown_current_stage"}
    if target_stage not in GATE_DEFINITIONS:
        return {"ok": False, "reason": "unknown_target_stage"}
    current_index = stage_index(current_stage)
    target_index = stage_index(target_stage)
    if current_index == target_index:
        return {"ok": False, "reason": "stage_transition_required"}
    direction = "advance" if target_index > current_index else "rollback"
    if direction == "advance" and target_index != current_index + 1:
        return {"ok": False, "reason": "non_adjacent_forward_transition"}
    return {
        "ok": True,
        "direction": direction,
        "from_stage": current_stage,
        "to_stage": target_stage,
        "required_approver_role": GATE_DEFINITIONS[target_stage]["required_approver_role"],
    }


def project_record_from_payload(payload: dict | None) -> dict:
    data = dict(payload or {})
    record_id = data.get("id") or data.get("code") or "capital_project-1"
    created_at = data.get("created_at") or data.get("reported_at") or "unspecified"
    criteria_status = normalize_criteria_status(data.get("criteria_status"))
    record = {
        "id": record_id,
        "tenant": data.get("tenant", "default"),
        "code": data.get("code", record_id),
        "name": data.get("name", data.get("code", record_id)),
        "status": INITIAL_STAGE,
        "lifecycle_stage": INITIAL_STAGE,
        "criteria_status": criteria_status,
        "gate_dates": {INITIAL_STAGE: created_at},
        "gate_history": (),
        "checklist_updates": (),
        "rebaseline_required": False,
        "rebaseline_count": 0,
        "payload": data,
    }
    return _with_lifecycle_fields(record)


def record_gate_checklist(project: dict, criteria_status: dict, context: dict | None = None) -> dict:
    next_project = deepcopy(project)
    merged = normalize_criteria_status(next_project.get("criteria_status"))
    merged.update(normalize_criteria_status(criteria_status))
    update = {
        "updated_at": dict(context or {}).get("updated_at", "unspecified"),
        "updated_by": dict(context or {}).get("updated_by", "unspecified"),
        "criteria_status": deepcopy(merged),
    }
    next_project["criteria_status"] = merged
    next_project["checklist_updates"] = tuple(next_project.get("checklist_updates", ())) + (update,)
    return _with_lifecycle_fields(next_project)


def validate_gate_transition(
    project: dict,
    target_stage: str,
    approver_role: str,
    criteria_status: dict | None = None,
    rebaseline_reason: str | None = None,
) -> dict:
    plan = transition_plan(project["lifecycle_stage"], target_stage)
    if not plan["ok"]:
        return plan
    if approver_role != plan["required_approver_role"]:
        return {
            "ok": False,
            "reason": "invalid_approver_role",
            "required_approver_role": plan["required_approver_role"],
        }
    merged_criteria = normalize_criteria_status(project.get("criteria_status"))
    merged_criteria.update(normalize_criteria_status(criteria_status))
    if plan["direction"] == "advance":
        blocked = blocked_criteria(merged_criteria, target_stage)
        if blocked:
            return {
                "ok": False,
                "reason": "exit_criteria_incomplete",
                "blocked_criteria": blocked,
                "required_approver_role": plan["required_approver_role"],
            }
    elif not rebaseline_reason:
        return {
            "ok": False,
            "reason": "rebaseline_reason_required",
            "required_approver_role": plan["required_approver_role"],
        }
    return {
        "ok": True,
        **plan,
        "criteria_status": merged_criteria,
        "blocked_criteria": (),
    }


def apply_gate_transition(
    project: dict,
    target_stage: str,
    approver_role: str,
    approved_by: str,
    approved_at: str,
    criteria_status: dict | None = None,
    rebaseline_reason: str | None = None,
) -> dict:
    validation = validate_gate_transition(
        project,
        target_stage,
        approver_role,
        criteria_status=criteria_status,
        rebaseline_reason=rebaseline_reason,
    )
    if not validation["ok"]:
        return {"ok": False, "reason": validation["reason"], "validation": validation}

    next_project = deepcopy(project)
    next_project["criteria_status"] = validation["criteria_status"]
    next_project["status"] = target_stage
    next_project["lifecycle_stage"] = target_stage
    next_project["rebaseline_required"] = validation["direction"] == "rollback"
    next_project["rebaseline_count"] = int(next_project.get("rebaseline_count", 0)) + (
        1 if validation["direction"] == "rollback" else 0
    )

    gate_dates = dict(next_project.get("gate_dates", {}))
    gate_dates[target_stage] = approved_at
    next_project["gate_dates"] = gate_dates

    approval_record = {
        "from_stage": validation["from_stage"],
        "to_stage": target_stage,
        "direction": validation["direction"],
        "approved_by": approved_by,
        "approver_role": approver_role,
        "approved_at": approved_at,
        "approved_criteria": tuple(
            criterion
            for criterion in required_criteria(target_stage)
            if validation["criteria_status"].get(criterion, False)
        ),
        "rebaseline_required": validation["direction"] == "rollback",
        "rebaseline_reason": rebaseline_reason,
    }
    next_project["gate_history"] = tuple(next_project.get("gate_history", ())) + (
        approval_record,
    )
    return {"ok": True, "project": _with_lifecycle_fields(next_project), "approval": approval_record}


def project_detail(project: dict) -> dict:
    return _with_lifecycle_fields(project)


def workbench_card(project: dict) -> dict:
    detail = project_detail(project)
    return {
        "id": detail["id"],
        "code": detail["code"],
        "tenant": detail["tenant"],
        "lifecycle_stage": detail["lifecycle_stage"],
        "next_stage": detail["next_stage"],
        "gate_status": detail["gate_status"],
        "blocked_criteria": detail["blocked_criteria"],
        "ready_for_next_stage": detail["ready_for_next_stage"],
        "required_approver_role": detail["required_approver_role"],
        "last_gate_date": detail["last_gate_date"],
        "rebaseline_required": detail["rebaseline_required"],
    }


def _with_lifecycle_fields(project: dict) -> dict:
    detail = deepcopy(project)
    current_stage = detail["lifecycle_stage"]
    upcoming_stage = next_stage(current_stage)
    blocked = blocked_criteria(detail.get("criteria_status"), upcoming_stage)
    detail["current_stage"] = current_stage
    detail["next_stage"] = upcoming_stage
    detail["required_approver_role"] = (
        GATE_DEFINITIONS[upcoming_stage]["required_approver_role"] if upcoming_stage else None
    )
    detail["blocked_criteria"] = blocked
    detail["ready_for_next_stage"] = bool(upcoming_stage) and not blocked
    detail["gate_status"] = (
        "final_stage"
        if not upcoming_stage
        else "ready" if not blocked else "blocked"
    )
    gate_dates = dict(detail.get("gate_dates", {}))
    detail["gate_dates"] = gate_dates
    detail["last_gate_date"] = gate_dates.get(current_stage)
    detail["stage_catalog"] = stage_catalog()
    return detail
