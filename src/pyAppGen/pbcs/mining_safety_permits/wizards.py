"""Guided safety workflows for the mining_safety_permits PBC."""
from __future__ import annotations
PBC_KEY = "mining_safety_permits"

def wizard_catalog() -> dict:
    wizards = (
        {"id":"draft_review_activate_permit","steps":("classify work","resolve rule overlay","attach controls","verify competencies","approve and activate"),"outputs":("active permit","AppGen-X permit issued event")},
        {"id":"isolation_to_zero_energy","steps":("identify energy sources","apply locks","verify boundary","record zero energy test","revalidate after boundary change"),"outputs":("verified isolation","revalidation hold if changed")},
        {"id":"confined_space_entry","steps":("select registered space","confirm rescue plan","gas test sequence","ventilation dependency check","authorize entry and retest timer"),"outputs":("entry authorization","gas test timeline")},
        {"id":"blast_clearance_reentry","steps":("validate shotfirer and magazine issue","set exclusion zone","fire and record status","confirm fumes and gas clearance","release reentry"),"outputs":("blast cleared event","reentry evidence")},
        {"id":"incident_to_prevention_loop","steps":("capture precursor","classify high potential","hold affected area","preserve evidence","create corrective controls"),"outputs":("incident record","control action backlog")},
        {"id":"regulatory_pack_export","steps":("select permit scope","collect approvals and tests","hash evidence","build manifest","export side-effect-free plan"),"outputs":("reproducible evidence pack","submission manifest")},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}

def wizard_for(wizard_id: str) -> dict:
    for wizard in wizard_catalog()["wizards"]:
        if wizard["id"] == wizard_id:
            return {"ok": True, "wizard": wizard, "side_effects": ()}
    return {"ok": False, "reason": "unknown_wizard", "side_effects": ()}

def smoke_test() -> dict:
    return {"ok": len(wizard_catalog()["wizards"]) >= 6 and wizard_for("confined_space_entry")["ok"], "side_effects": ()}
