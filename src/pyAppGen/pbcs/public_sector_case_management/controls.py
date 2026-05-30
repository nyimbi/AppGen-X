"""Governance controls for the Public Sector Case Management PBC."""
from __future__ import annotations

PBC_KEY = "public_sector_case_management"


def control_catalog() -> dict:
    controls = (
        ("intake_envelope_complete", "blocking", "Every inbound request needs channel, language, program, and contactability."),
        ("representative_authority_verified", "blocking", "Authorized representatives need effective dates and verification."),
        ("jurisdiction_determined", "blocking", "A case cannot route without jurisdiction and office."),
        ("evidence_sufficient_for_rule", "blocking", "Eligibility approval requires sufficient evidence for each decisive rule."),
        ("missing_information_due_date_valid", "blocking", "Checklist due dates must be active or explicitly tolled."),
        ("notice_has_rule_citation", "blocking", "Adverse notices need governing citations and fact snapshots."),
        ("referral_packet_privacy_safe", "blocking", "Referral packages may include only allowed evidence."),
        ("appeal_timeliness_and_standing", "blocking", "Appeals require standing and a timely filing or rejection reason."),
        ("hearing_packet_complete", "blocking", "Hearing packets need issue, chronology, evidence index, notice history, and rule basis."),
        ("sla_clock_not_expired", "warning", "Stage clocks must be timely or have an approved pause."),
        ("purpose_based_access_declared", "blocking", "Sensitive fields require a declared processing purpose."),
        ("confidentiality_marker_enforced", "blocking", "Protected address, youth, sealed, or witness markers must suppress unsafe display/export."),
        ("manual_override_governed", "blocking", "Overrides need type, justification, approver, expiry, and recalculation behavior."),
        ("fraud_handoff_boundary", "blocking", "Fraud referrals expose only approved facts and excerpts to the fraud boundary."),
        ("agent_mutations_require_confirmation", "blocking", "Assistant-authored datastore mutations require human confirmation."),
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": tuple({"id": cid, "severity": severity, "description": desc} for cid, severity, desc in controls), "side_effects": ()}


def evaluate_control(control_id: str, facts: dict | None = None) -> dict:
    facts = dict(facts or {})
    controls = {control["id"]: control for control in control_catalog()["controls"]}
    if control_id not in controls:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    failures: list[str] = []
    if control_id == "intake_envelope_complete" and not all(facts.get(field) for field in ("channel", "language", "program", "contactability")):
        failures.append("intake_envelope_incomplete")
    elif control_id == "representative_authority_verified" and facts.get("representative") and not facts.get("verified"):
        failures.append("representative_authority_unverified")
    elif control_id == "jurisdiction_determined" and not facts.get("jurisdiction"):
        failures.append("jurisdiction_missing")
    elif control_id == "evidence_sufficient_for_rule" and facts.get("sufficiency") not in {"satisfied", "waived"}:
        failures.append("evidence_insufficient")
    elif control_id == "missing_information_due_date_valid" and facts.get("expired") and not facts.get("tolled"):
        failures.append("checklist_due_date_expired")
    elif control_id == "notice_has_rule_citation" and (not facts.get("citation") or not facts.get("fact_snapshot")):
        failures.append("notice_citation_or_snapshot_missing")
    elif control_id == "referral_packet_privacy_safe" and facts.get("includes_restricted") and not facts.get("override"):
        failures.append("restricted_evidence_in_referral")
    elif control_id == "appeal_timeliness_and_standing" and (not facts.get("standing") or (not facts.get("timely") and not facts.get("rejection_reason"))):
        failures.append("appeal_timeliness_or_standing_invalid")
    elif control_id == "hearing_packet_complete" and not all(facts.get(field) for field in ("issue", "chronology", "evidence_index", "notice_history", "rule_basis")):
        failures.append("hearing_packet_incomplete")
    elif control_id == "sla_clock_not_expired" and facts.get("expired") and not facts.get("pause_reason"):
        failures.append("sla_clock_expired")
    elif control_id == "purpose_based_access_declared" and facts.get("sensitive") and not facts.get("purpose"):
        failures.append("processing_purpose_missing")
    elif control_id == "confidentiality_marker_enforced" and facts.get("marker") and not facts.get("masked"):
        failures.append("confidentiality_marker_not_enforced")
    elif control_id == "manual_override_governed" and facts.get("override") and not all(facts.get(field) for field in ("justification", "approver", "expiry")):
        failures.append("override_governance_missing")
    elif control_id == "fraud_handoff_boundary" and facts.get("investigative_notes_visible"):
        failures.append("fraud_boundary_leak")
    elif control_id == "agent_mutations_require_confirmation" and not facts.get("confirmed"):
        failures.append("confirmation_required")
    return {"ok": not failures, "control": controls[control_id], "failures": tuple(failures), "requires_exception": bool(failures), "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": not evaluate_control("intake_envelope_complete", {"channel": "portal"})["ok"] and evaluate_control("jurisdiction_determined", {"jurisdiction": "north"})["ok"] and not evaluate_control("agent_mutations_require_confirmation", {"confirmed": False})["ok"], "side_effects": ()}
