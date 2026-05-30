"""Package-local guided wizards for the Library and Archives Management workbench."""

from __future__ import annotations

from .forms import library_archives_management_form_catalog

PBC_KEY = "library_archives_management"

LIBRARY_ARCHIVES_MANAGEMENT_WIZARDS = (
    {
        "wizard_id": "acquisition_to_accession",
        "title": "Acquisition to accession",
        "goal": "Move potential new holdings from acquisition review into a controlled accession register with provenance and rights context.",
        "domain_areas": ("acquisitions", "accessioning", "provenance", "rights/access restrictions"),
        "steps": (
            {"step_id": "acquisition", "label": "Record acquisition decision", "form_id": "acquisition_decision", "operation": "record_archive_request", "requires": ()},
            {"step_id": "accession", "label": "Create accession register entry", "form_id": "accession_register_intake", "operation": "record_archive_request", "requires": ("decision_id",)},
            {"step_id": "provenance", "label": "Capture provenance chain", "form_id": "provenance_chain_update", "operation": "create_collection_item", "requires": ("accession_number",)},
            {"step_id": "rights", "label": "Apply donor and access restrictions", "form_id": "rights_access_restriction", "operation": "simulate_rights_statement", "requires": ("accession_number", "provenance_id")},
        ),
    },
    {
        "wizard_id": "catalog_authority_and_finding_aid",
        "title": "Catalog, authority, and finding aid",
        "goal": "Move from descriptive intake to authority-reviewed cataloging and multilevel finding aid publication.",
        "domain_areas": ("cataloging", "authority control", "finding aids", "provenance"),
        "steps": (
            {"step_id": "catalog", "label": "Create catalog record", "form_id": "catalog_recording", "operation": "record_catalog_record", "requires": ()},
            {"step_id": "authority", "label": "Normalize headings", "form_id": "authority_control_heading", "operation": "review_library_archives_management_policy_rule", "requires": ("record_id",)},
            {"step_id": "provenance", "label": "Link provenance narrative", "form_id": "provenance_chain_update", "operation": "create_collection_item", "requires": ("record_id",)},
            {"step_id": "finding_aid", "label": "Publish hierarchical finding aid", "form_id": "finding_aid_description", "operation": "record_catalog_record", "requires": ("record_id", "heading_id")},
        ),
    },
    {
        "wizard_id": "circulation_and_holds",
        "title": "Circulation and holds",
        "goal": "Support standard library circulation while diverting archival or restricted materials to supervised workflows.",
        "domain_areas": ("circulation/loans", "holds", "rights/access restrictions"),
        "steps": (
            {"step_id": "loan", "label": "Issue or review loan", "form_id": "circulation_loan_checkout", "operation": "review_circulation_loan", "requires": ()},
            {"step_id": "hold", "label": "Queue hold request", "form_id": "hold_request_management", "operation": "create_collection_item", "requires": ("item_id",)},
            {"step_id": "restriction_check", "label": "Reconfirm access restrictions", "form_id": "rights_access_restriction", "operation": "simulate_rights_statement", "requires": ("item_id",)},
        ),
    },
    {
        "wizard_id": "preservation_digitization_access",
        "title": "Preservation, digitization, and access",
        "goal": "Route fragile, restricted, or born-digital materials through conservation, capture, QC, and access review.",
        "domain_areas": ("preservation", "conservation", "digitization", "rights/access restrictions", "finding aids"),
        "steps": (
            {"step_id": "preservation", "label": "Open preservation plan", "form_id": "preservation_treatment", "operation": "create_preservation_action", "requires": ()},
            {"step_id": "conservation", "label": "Authorize conservation", "form_id": "conservation_treatment", "operation": "create_preservation_action", "requires": ("item_id",)},
            {"step_id": "digitization", "label": "Triage digitization job", "form_id": "digitization_triage", "operation": "approve_digitization_job", "requires": ("item_id",)},
            {"step_id": "rights", "label": "Confirm publication rights", "form_id": "rights_access_restriction", "operation": "simulate_rights_statement", "requires": ("item_id", "job_id")},
            {"step_id": "finding_aid", "label": "Expose digital access note", "form_id": "finding_aid_description", "operation": "record_catalog_record", "requires": ("item_id", "rights_id")},
        ),
    },
    {
        "wizard_id": "reading_room_service",
        "title": "Reading room service",
        "goal": "Verify researcher eligibility, item restrictions, and supervised handling for archival consultation.",
        "domain_areas": ("reading-room requests", "rights/access restrictions", "circulation/loans", "holds"),
        "steps": (
            {"step_id": "request", "label": "Open reading room request", "form_id": "reading_room_request", "operation": "review_circulation_loan", "requires": ()},
            {"step_id": "rights", "label": "Review onsite restrictions", "form_id": "rights_access_restriction", "operation": "simulate_rights_statement", "requires": ("request_id",)},
            {"step_id": "loan", "label": "Create supervised circulation record", "form_id": "circulation_loan_checkout", "operation": "review_circulation_loan", "requires": ("request_id", "researcher_id")},
            {"step_id": "hold_release", "label": "Release queued holds after visit", "form_id": "hold_request_management", "operation": "create_collection_item", "requires": ("request_id", "item_ids")},
        ),
    },
    {
        "wizard_id": "deaccession_and_audit",
        "title": "Deaccession and audit",
        "goal": "Gate withdrawals behind provenance, policy, legal hold, and stewardship evidence.",
        "domain_areas": ("deaccessioning", "audits", "provenance", "rights/access restrictions"),
        "steps": (
            {"step_id": "audit", "label": "Run stewardship audit", "form_id": "inventory_audit", "operation": "create_library_archives_management_control_assertion", "requires": ()},
            {"step_id": "provenance", "label": "Recheck provenance chain", "form_id": "provenance_chain_update", "operation": "create_collection_item", "requires": ("audit_id",)},
            {"step_id": "rights", "label": "Review donor and legal constraints", "form_id": "rights_access_restriction", "operation": "simulate_rights_statement", "requires": ("audit_id", "provenance_id")},
            {"step_id": "deaccession", "label": "Open deaccession case", "form_id": "deaccession_case", "operation": "create_library_archives_management_control_assertion", "requires": ("audit_id", "rights_id")},
        ),
    },
    {
        "wizard_id": "assistant_curator_preview",
        "title": "Assistant curator preview",
        "goal": "Turn operator instructions into bounded CRUD previews without leaving the PBC-owned datastore boundary.",
        "domain_areas": ("assistant CRUD previews", "rights/access restrictions", "audits"),
        "steps": (
            {"step_id": "preview", "label": "Preview CRUD intent", "form_id": "assistant_crud_preview", "operation": "record_library_archives_management_governed_model", "requires": ()},
            {"step_id": "rights", "label": "Cross-check rights impact", "form_id": "rights_access_restriction", "operation": "simulate_rights_statement", "requires": ("target_table",)},
            {"step_id": "audit", "label": "Capture audit evidence", "form_id": "inventory_audit", "operation": "create_library_archives_management_control_assertion", "requires": ("requested_action",)},
        ),
    },
)



def library_archives_management_wizard_catalog() -> dict:
    """Return the package-local wizard registry."""
    forms = library_archives_management_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in LIBRARY_ARCHIVES_MANAGEMENT_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(LIBRARY_ARCHIVES_MANAGEMENT_WIZARDS) and not missing_form_bindings,
        "pbc": PBC_KEY,
        "wizards": LIBRARY_ARCHIVES_MANAGEMENT_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in LIBRARY_ARCHIVES_MANAGEMENT_WIZARDS),
        "domain_areas": tuple(
            dict.fromkeys(
                area
                for wizard in LIBRARY_ARCHIVES_MANAGEMENT_WIZARDS
                for area in wizard["domain_areas"]
            )
        ),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }



def library_archives_management_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided step plan with readiness details."""
    wizard = next((item for item in LIBRARY_ARCHIVES_MANAGEMENT_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {
            "ok": False,
            "reason": "unknown_wizard",
            "wizard_id": wizard_id,
            "side_effects": (),
        }

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = tuple(requirement for requirement in step.get("requires", ()) if not supplied.get(requirement))
        planned_steps.append(
            {
                **step,
                "position": position,
                "ready": not blocked_by,
                "blocked_by": blocked_by,
            }
        )

    return {
        "ok": True,
        "pbc": PBC_KEY,
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "domain_areas": wizard["domain_areas"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise the package-local wizard registry and one guided plan."""
    catalog = library_archives_management_wizard_catalog()
    plan = library_archives_management_plan_wizard(
        "preservation_digitization_access",
        {"item_id": "ITEM-OH-44", "job_id": "DIG-6001", "rights_id": "RIGHTS-204"},
    )
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
