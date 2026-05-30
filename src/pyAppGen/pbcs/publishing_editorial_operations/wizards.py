"""Workflow wizard contracts for the Publishing Editorial Operations PBC."""
from __future__ import annotations

PBC_KEY = "publishing_editorial_operations"


def wizard_catalog() -> dict:
    wizards = (
        {"id": "acquisition_to_manuscript", "steps": ("capture proposal", "build board packet", "record votes", "resolve conditions", "convert to manuscript")},
        {"id": "manuscript_readiness", "steps": ("evaluate package completeness", "record waivers", "freeze version", "assign editor", "open editorial tasks")},
        {"id": "peer_review_decision", "steps": ("select review model", "check reviewer conflicts", "send invitations", "receive reviews", "synthesize decision bundle")},
        {"id": "copyedit_author_query", "steps": ("apply style sheet", "open queries", "track author responses", "classify changes", "sign off copyedit")},
        {"id": "rights_edition_clearance", "steps": ("build rights matrix", "detect territory/format collisions", "clear asset permissions", "approve edition", "store boundary ledger")},
        {"id": "production_proof_release", "steps": ("assemble handoff packet", "open proof round", "classify corrections", "check accessibility", "approve final proof")},
        {"id": "metadata_distribution_export", "steps": ("validate authority metadata", "snapshot edition metadata", "export distributor feed", "track failed exports", "record release timestamp")},
        {"id": "schedule_scenario_planning", "steps": ("model reviewer delay", "model proof expansion", "recalculate critical path", "compare scenarios", "attach chosen plan")},
        {"id": "release_evidence_binder", "steps": ("assemble lineage", "attach rights clearance", "attach metadata readiness", "attach proof signoff", "publish release verdict")},
        {"id": "editorial_agent_preview", "steps": ("parse pitch or proof note", "map fields", "highlight missing evidence", "preview CRUD", "require human confirmation")},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def wizard_for(wizard_id: str) -> dict:
    for wizard in wizard_catalog()["wizards"]:
        if wizard["id"] == wizard_id:
            return {"ok": True, "wizard": wizard, "side_effects": ()}
    return {"ok": False, "reason": "unknown_wizard", "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": len(wizard_catalog()["wizards"]) >= 10 and wizard_for("release_evidence_binder")["ok"], "side_effects": ()}
