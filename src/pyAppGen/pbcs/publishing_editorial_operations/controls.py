"""Governance controls for the Publishing Editorial Operations PBC."""
from __future__ import annotations

PBC_KEY = "publishing_editorial_operations"


def control_catalog() -> dict:
    controls = (
        ("acquisition_packet_complete", "blocking", "Acquisition cannot go to board without packet, comp titles, season, and sponsor."),
        ("board_decision_has_quorum", "blocking", "Board decisions require quorum and recorded conditions."),
        ("manuscript_package_complete", "blocking", "Manuscripts need required artifacts or approved waivers."),
        ("version_freeze_recorded", "blocking", "Production and proof records must reference a frozen manuscript version."),
        ("reviewer_conflict_cleared", "blocking", "Reviewer assignment requires conflict and anonymity checks."),
        ("decision_bundle_complete", "blocking", "Editorial decisions need rationale, review synthesis, revision points, and rights/schedule impact."),
        ("critical_queries_resolved", "blocking", "Critical author queries block copyedit or proof exit."),
        ("rights_collision_absent", "blocking", "Edition approval requires no territory, language, format, exclusivity, or embargo collision."),
        ("metadata_authority_valid", "blocking", "Metadata export requires authority-controlled identifiers and accessibility flags."),
        ("production_handoff_complete", "blocking", "Production start requires frozen text, assets, rights, specs, metadata, and risk notes."),
        ("proof_corrections_classified", "blocking", "Proof signoff requires classified corrections and downstream checks."),
        ("release_binder_complete", "blocking", "Release readiness needs lineage, rights, metadata, proof, schedule, communications, and exceptions."),
        ("blind_review_privacy_enforced", "blocking", "Blind review exports must redact prohibited identities."),
        ("notification_replay_safe", "warning", "Time-sensitive notification retries must be safe or escalated."),
        ("agent_mutations_require_confirmation", "blocking", "Assistant-authored mutations require human confirmation."),
    )
    return {"ok": True, "pbc": PBC_KEY, "controls": tuple({"id": cid, "severity": severity, "description": desc} for cid, severity, desc in controls), "side_effects": ()}


def evaluate_control(control_id: str, facts: dict | None = None) -> dict:
    facts = dict(facts or {})
    controls = {control["id"]: control for control in control_catalog()["controls"]}
    if control_id not in controls:
        return {"ok": False, "reason": "unknown_control", "side_effects": ()}
    failures: list[str] = []
    if control_id == "acquisition_packet_complete" and not all(facts.get(field) for field in ("packet", "comp_titles", "season", "sponsor")):
        failures.append("acquisition_packet_incomplete")
    elif control_id == "board_decision_has_quorum" and (not facts.get("quorum") or (facts.get("decision") == "conditional" and not facts.get("conditions"))):
        failures.append("board_decision_incomplete")
    elif control_id == "manuscript_package_complete" and facts.get("missing") and not facts.get("waiver"):
        failures.append("manuscript_package_missing_artifacts")
    elif control_id == "version_freeze_recorded" and not facts.get("frozen_version"):
        failures.append("frozen_version_missing")
    elif control_id == "reviewer_conflict_cleared" and (facts.get("conflict") or not facts.get("anonymity_rule")):
        failures.append("reviewer_conflict_or_anonymity_missing")
    elif control_id == "decision_bundle_complete" and not all(facts.get(field) for field in ("rationale", "review_synthesis", "revision_points", "schedule_impact")):
        failures.append("decision_bundle_incomplete")
    elif control_id == "critical_queries_resolved" and facts.get("critical_open", 0) > 0:
        failures.append("critical_queries_open")
    elif control_id == "rights_collision_absent" and facts.get("collisions"):
        failures.append("rights_collision")
    elif control_id == "metadata_authority_valid" and not facts.get("identifiers"):
        failures.append("metadata_identifiers_missing")
    elif control_id == "production_handoff_complete" and not all(facts.get(field) for field in ("frozen_text", "assets", "rights", "specs", "metadata")):
        failures.append("production_handoff_incomplete")
    elif control_id == "proof_corrections_classified" and facts.get("unclassified", 0) > 0:
        failures.append("proof_corrections_unclassified")
    elif control_id == "release_binder_complete" and facts.get("missing_sections"):
        failures.append("release_binder_missing_sections")
    elif control_id == "blind_review_privacy_enforced" and facts.get("blind") and not facts.get("redacted"):
        failures.append("blind_review_identity_leak")
    elif control_id == "notification_replay_safe" and facts.get("expired") and not facts.get("escalated"):
        failures.append("notification_replay_unsafe")
    elif control_id == "agent_mutations_require_confirmation" and not facts.get("confirmed"):
        failures.append("confirmation_required")
    return {"ok": not failures, "control": controls[control_id], "failures": tuple(failures), "requires_exception": bool(failures), "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": not evaluate_control("acquisition_packet_complete", {"packet": "p"})["ok"] and evaluate_control("rights_collision_absent", {"collisions": ()})["ok"] and not evaluate_control("agent_mutations_require_confirmation", {"confirmed": False})["ok"], "side_effects": ()}
