"""Wizard contracts for the Renewables Asset Operations PBC."""
PBC_KEY = "renewables_asset_operations"


def wizard_catalog():
    wizards = (
        {"id": "site_asset_onboarding", "steps": ("build hierarchy", "classify technology", "attach meters", "load OEM profile", "activate site")},
        {"id": "telemetry_to_availability", "steps": ("ingest reading", "reconcile meters", "classify outage", "apply exclusions", "lock availability pack")},
        {"id": "curtailment_recovery", "steps": ("capture instruction", "classify cause", "estimate counterfactual energy", "prepare compensation evidence", "publish event")},
        {"id": "maintenance_safety_release", "steps": ("score criticality", "check spares", "verify contractor competency", "approve permit", "release work")},
        {"id": "inspection_to_work_order", "steps": ("capture offline inspection", "classify defects", "attach imagery", "create follow-up work", "sync conflicts")},
        {"id": "warranty_claim_packet", "steps": ("detect recurrence", "collect fault history", "check terms", "notify OEM", "assemble claim evidence")},
        {"id": "performance_rca", "steps": ("normalize resource", "bucket losses", "exclude alternatives", "assign corrective action", "verify recovery")},
        {"id": "storage_dispatch_review", "steps": ("record dispatch", "compare delivery", "calculate efficiency", "update cycle count", "flag degradation")},
        {"id": "shift_handover", "steps": ("summarize alarms", "list holds", "carry open dispatch", "acknowledge risks", "publish handover")},
        {"id": "operator_assistant_preview", "steps": ("parse manual or PPA", "extract obligations", "preview tasks", "block missing evidence", "require confirmation")},
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def wizard_for(wizard_id):
    for wizard in wizard_catalog()["wizards"]:
        if wizard["id"] == wizard_id:
            return {"ok": True, "wizard": wizard, "side_effects": ()}
    return {"ok": False, "reason": "unknown_wizard", "side_effects": ()}


def smoke_test():
    return {"ok": len(wizard_catalog()["wizards"]) >= 10 and wizard_for("performance_rca")["ok"], "side_effects": ()}
