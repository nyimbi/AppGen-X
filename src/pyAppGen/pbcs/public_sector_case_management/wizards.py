"""Workflow wizard contracts for the Public Sector Case Management PBC."""
from __future__ import annotations

PBC_KEY = "public_sector_case_management"


def wizard_catalog() -> dict:
    wizards = (
        {"id": "multi_channel_intake_to_case", "steps": ("capture intake envelope", "match applicant and household", "derive jurisdiction", "screen programs", "open case or rejection queue")},
        {"id": "evidence_to_eligibility", "steps": ("classify evidence", "link asserted facts", "evaluate sufficiency", "compile date rules", "record eligibility determination")},
        {"id": "missing_information_loop", "steps": ("generate checklist", "issue request notice", "match inbound response", "waive or substitute proof", "resume decision clock")},
        {"id": "benefit_service_package_review", "steps": ("assemble benefit recommendation", "attach service obligations", "test package conflicts", "approve partial or full package", "publish decision snapshot")},
        {"id": "notice_and_correspondence", "steps": ("select notice type", "render language template", "attach rule explanations", "route delivery", "track response deadline")},
        {"id": "referral_loop_closure", "steps": ("create referral package", "share privacy-safe evidence", "track provider response", "capture service outcome", "escalate overdue referrals")},
        {"id": "appeal_hearing_management", "steps": ("validate appeal intake", "frame contested issue", "schedule hearing", "assemble packet", "record outcome and implementation")},
        {"id": "sla_and_supervisor_queue", "steps": ("start stage clocks", "apply tolling", "resume clocks", "surface aging queue", "open control exception")},
        {"id": "privacy_override_and_fraud_handoff", "steps": ("declare processing purpose", "apply confidentiality marker", "approve manual override", "prepare fraud handoff", "hide investigative notes from ordinary queue")},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def wizard_for(wizard_id: str) -> dict:
    for wizard in wizard_catalog()["wizards"]:
        if wizard["id"] == wizard_id:
            return {"ok": True, "wizard": wizard, "side_effects": ()}
    return {"ok": False, "reason": "unknown_wizard", "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": len(wizard_catalog()["wizards"]) >= 9 and wizard_for("appeal_hearing_management")["ok"], "side_effects": ()}
