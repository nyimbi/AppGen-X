"""Guided workflows for the media_production_management PBC."""
from __future__ import annotations

PBC_KEY = "media_production_management"


def wizard_catalog() -> dict:
    wizards = (
        {
            "id": "development_to_greenlight",
            "title": "Development To Greenlight",
            "steps": (
                "capture script and creative package", "verify attachments and financing", "lock top sheet",
                "route stage approvals", "emit development greenlit event",
            ),
            "outputs": ("production lifecycle state", "greenlight dossier", "approval event"),
        },
        {
            "id": "schedule_lock_and_call_sheet",
            "title": "Schedule Lock And Call Sheet Issue",
            "steps": (
                "version stripboard", "validate location packages", "check cast and crew turnaround",
                "confirm transport and equipment", "issue call sheet with supersede trail",
            ),
            "outputs": ("locked schedule", "call sheet", "readiness scorecard"),
        },
        {
            "id": "daily_wrap_to_cost_report",
            "title": "Daily Wrap To Cost Report",
            "steps": (
                "capture daily production report", "compute labor and meal penalties", "classify delays",
                "update estimate to complete", "open exceptions for missing receipts or incidents",
            ),
            "outputs": ("daily report", "variance ledger", "burn forecast"),
        },
        {
            "id": "dailies_to_editorial_handoff",
            "title": "Dailies To Editorial Handoff",
            "steps": (
                "ingest camera and sound manifests", "verify checksums", "attach script and continuity notes",
                "flag missing media", "open editorial-ready event when complete",
            ),
            "outputs": ("dailies packet", "editorial queue", "missing media exceptions"),
        },
        {
            "id": "post_vfx_delivery_readiness",
            "title": "Post, VFX, And Delivery Readiness",
            "steps": (
                "track edit milestone dependencies", "turn over VFX packages", "approve sound color and mastering",
                "run technical QC", "assemble platform deliverables and archive bundle",
            ),
            "outputs": ("picture lock evidence", "QC result", "delivered package", "archive manifest"),
        },
        {
            "id": "document_instruction_to_safe_mutation",
            "title": "Document Instruction To Safe Mutation",
            "steps": (
                "classify source document", "extract cited fields", "score confidence", "prepare CRUD preview",
                "require human confirmation", "write owned table and outbox event",
            ),
            "outputs": ("mutation preview", "source citations", "AppGen-X event"),
        },
    )
    return {"ok": True, "pbc": PBC_KEY, "wizards": wizards, "side_effects": ()}


def wizard_for(wizard_id: str) -> dict:
    for wizard in wizard_catalog()["wizards"]:
        if wizard["id"] == wizard_id:
            return {"ok": True, "wizard": wizard, "side_effects": ()}
    return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}


def smoke_test() -> dict:
    catalog = wizard_catalog()
    return {"ok": catalog["ok"] and len(catalog["wizards"]) >= 6 and wizard_for("post_vfx_delivery_readiness")["ok"], "side_effects": ()}
