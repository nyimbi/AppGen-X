"""Governance controls for the Renewables Asset Operations PBC."""
PBC_KEY = "renewables_asset_operations"


def control_catalog():
    ids = (
        ("asset_hierarchy_complete", "blocking"),
        ("meter_reconciliation_within_tolerance", "blocking"),
        ("curtailment_has_instruction_evidence", "blocking"),
        ("availability_exclusion_approved", "blocking"),
        ("ppa_settlement_deadline_safe", "warning"),
        ("maintenance_has_safety_permit", "blocking"),
        ("contractor_competency_valid", "blocking"),
        ("remote_reset_not_allowed_during_lockout", "blocking"),
        ("warranty_claim_threshold_met", "warning"),
        ("performance_rca_has_recovery_evidence", "blocking"),
        ("storage_dispatch_compliant", "blocking"),
        ("environmental_permit_attached", "blocking"),
        ("agent_mutations_require_confirmation", "blocking"),
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": tuple({"id": i, "severity": s} for i, s in ids), "side_effects": ()}


def evaluate_control(control_id, facts=None):
    facts = dict(facts or {})
    known = {c["id"]: c for c in control_catalog()["controls"]}
    if control_id not in known:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    failures = []
    if control_id == "asset_hierarchy_complete" and not all(facts.get(k) for k in ("site", "technology", "grid_node")):
        failures.append("asset_hierarchy_incomplete")
    elif control_id == "meter_reconciliation_within_tolerance" and abs(facts.get("variance", 0)) > facts.get("tolerance", 0):
        failures.append("meter_variance_breach")
    elif control_id == "curtailment_has_instruction_evidence" and not facts.get("evidence"):
        failures.append("instruction_evidence_missing")
    elif control_id == "availability_exclusion_approved" and facts.get("exclusion") and not facts.get("approved"):
        failures.append("exclusion_unapproved")
    elif control_id == "ppa_settlement_deadline_safe" and facts.get("late") and not facts.get("waiver"):
        failures.append("settlement_deadline_late")
    elif control_id == "maintenance_has_safety_permit" and not facts.get("permit"):
        failures.append("safety_permit_missing")
    elif control_id == "contractor_competency_valid" and facts.get("expired"):
        failures.append("contractor_competency_expired")
    elif control_id == "remote_reset_not_allowed_during_lockout" and facts.get("lockout") and facts.get("remote_reset"):
        failures.append("remote_reset_blocked_by_lockout")
    elif control_id == "warranty_claim_threshold_met" and facts.get("recurrence", 0) < facts.get("threshold", 1):
        failures.append("warranty_threshold_not_met")
    elif control_id == "performance_rca_has_recovery_evidence" and not facts.get("recovery_evidence"):
        failures.append("recovery_evidence_missing")
    elif control_id == "storage_dispatch_compliant" and facts.get("delivered", 0) < facts.get("committed", 0):
        failures.append("dispatch_shortfall")
    elif control_id == "environmental_permit_attached" and facts.get("regulated") and not facts.get("permit"):
        failures.append("environmental_permit_missing")
    elif control_id == "agent_mutations_require_confirmation" and not facts.get("confirmed"):
        failures.append("confirmation_required")
    return {"ok": not failures, "control": known[control_id], "failures": tuple(failures), "requires_exception": bool(failures), "side_effects": ()}


def smoke_test():
    return {"ok": not evaluate_control("asset_hierarchy_complete", {"site": "S"})["ok"] and evaluate_control("storage_dispatch_compliant", {"delivered": 10, "committed": 9})["ok"] and not evaluate_control("agent_mutations_require_confirmation", {"confirmed": False})["ok"], "side_effects": ()}
