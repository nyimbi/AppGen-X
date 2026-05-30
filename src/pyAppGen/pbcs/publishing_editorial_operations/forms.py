"""Professional form contracts for the Publishing Editorial Operations PBC."""
from __future__ import annotations

PBC_KEY = "publishing_editorial_operations"


def form_catalog() -> dict:
    forms = (
        {"id": "acquisition_pipeline_intake", "owned_table": "publishing_editorial_operations_manuscript", "fields": ("proposal", "sponsor_editor", "comp_titles", "target_imprint", "season", "format_mix", "decision_stage", "rationale"), "validations": ("proposal complete", "sponsor assigned", "stage transition evidence")},
        {"id": "acquisition_board_decision", "owned_table": "publishing_editorial_operations_editorial_task", "fields": ("board_packet", "votes", "conditions", "requested_revisions", "followups", "decision", "decision_owner"), "validations": ("vote quorum", "conditions tracked", "contract linkage")},
        {"id": "manuscript_package", "owned_table": "publishing_editorial_operations_manuscript", "fields": ("synopsis", "author_bio", "permissions_notes", "sample_chapters", "art_log", "target_metadata", "waiver_reason"), "validations": ("completeness profile", "waiver approval", "intake readiness")},
        {"id": "manuscript_version_lineage", "owned_table": "publishing_editorial_operations_manuscript", "fields": ("submission_version", "developmental_version", "copyedited_version", "proof_version", "corrected_proof_version", "final_version", "freeze_reason"), "validations": ("freeze timestamp", "lineage graph", "production reference")},
        {"id": "peer_review", "owned_table": "publishing_editorial_operations_editorial_task", "fields": ("review_model", "reviewer", "conflict_status", "anonymity_rule", "invitation_status", "deadline", "review_received", "recommendation"), "validations": ("conflict checked", "blind review redaction", "deadline control")},
        {"id": "copyedit_and_queries", "owned_table": "publishing_editorial_operations_editorial_task", "fields": ("style_sheet", "query", "severity", "author_response", "response_deadline", "unresolved_impact", "signoff"), "validations": ("style sheet version", "critical query closure", "reentry path")},
        {"id": "rights_and_permissions", "owned_table": "publishing_editorial_operations_rights_grant", "fields": ("territory", "language", "format", "duration", "sublicensing", "asset", "permission_status", "collision_check"), "validations": ("rights boundary", "collision detection", "permission packet")},
        {"id": "edition_metadata", "owned_table": "publishing_editorial_operations_edition", "fields": ("parent_edition", "isbn", "doi", "contributors", "subject_codes", "keywords", "accessibility_flags", "metadata_snapshot"), "validations": ("authority control", "edition diff", "export readiness")},
        {"id": "production_schedule", "owned_table": "publishing_editorial_operations_production_schedule", "fields": ("season", "critical_path", "handoff_packet", "proof_round", "asset_freeze", "schedule_risk", "scenario"), "validations": ("handoff complete", "proof signoff", "date risk evidence")},
        {"id": "distribution_release_binder", "owned_table": "publishing_editorial_operations_distribution_plan", "fields": ("metadata_export", "distribution_feed", "release_date", "territory_sequence", "binder_sections", "missing_sections", "release_verdict"), "validations": ("binder complete", "feed traceability", "release readiness")},
        {"id": "author_reviewer_correspondence", "owned_table": "publishing_editorial_operations_editorial_task", "fields": ("recipient_role", "message_intent", "due_date_context", "privacy_safe_summary", "blind_review_safe", "triggering_event"), "validations": ("timeline evidence", "anonymity preserved", "template trace")},
        {"id": "editorial_exception", "owned_table": "publishing_editorial_operations_publishing_editorial_operations_control_assertion", "fields": ("exception_class", "owner", "sla", "impact", "resolution", "evidence"), "validations": ("taxonomy", "owner assigned", "resolution evidence")},
    )
    return {"ok": True, "pbc": PBC_KEY, "forms": forms, "side_effects": ()}


def form_for(form_id: str) -> dict:
    for form in form_catalog()["forms"]:
        if form["id"] == form_id:
            return {"ok": True, "form": form, "side_effects": ()}
    return {"ok": False, "reason": "unknown_form", "side_effects": ()}


def smoke_test() -> dict:
    return {"ok": len(form_catalog()["forms"]) >= 12 and form_for("rights_and_permissions")["ok"], "side_effects": ()}
