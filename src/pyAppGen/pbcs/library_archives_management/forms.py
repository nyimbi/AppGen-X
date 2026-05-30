"""Package-local forms for the Library and Archives Management standalone workbench."""

from __future__ import annotations

from .runtime import LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES

PBC_KEY = "library_archives_management"
OWNED_TABLE_CHOICES = tuple(LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES)

LIBRARY_ARCHIVES_MANAGEMENT_FORM_DEFINITIONS = (
    {
        "form_id": "accession_register_intake",
        "domain_area": "accessioning",
        "title": "Register accession intake",
        "route": "POST /app/library-archives-management/accessions",
        "operation": "record_archive_request",
        "permission": "library_archives_management.create",
        "owned_tables": (
            "library_archives_management_archive_request",
            "library_archives_management_collection_item",
            "library_archives_management_rights_statement",
        ),
        "outcomes": (
            "Creates a custody-first accession register entry.",
            "Captures transfer type, source of custody, temporary restrictions, and appraisal notes.",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "accession_number", "type": "string", "required": True},
            {"name": "transfer_type", "type": "enum", "required": True, "choices": ("donation", "institutional_transfer", "purchase", "emergency_transfer", "born_digital_transfer")},
            {"name": "source_name", "type": "string", "required": True},
            {"name": "custody_date", "type": "string", "required": True},
            {"name": "quantity_received", "type": "string", "required": True},
            {"name": "temporary_restrictions", "type": "list", "required": True},
            {"name": "appraisal_note", "type": "text", "required": True},
            {"name": "provenance_confidence", "type": "enum", "required": True, "choices": ("high", "medium", "low")},
        ),
        "example_payload": {
            "tenant": "archives-east",
            "accession_number": "2026-045",
            "transfer_type": "donation",
            "source_name": "Ngugi Family Papers",
            "custody_date": "2026-05-30",
            "quantity_received": "12 boxes, 4 oversize folders, 2 hard drives",
            "temporary_restrictions": ["personal_correspondence_review", "donor_embargo"],
            "appraisal_note": "Contains literary drafts, family correspondence, and born-digital photographs pending forensic intake.",
            "provenance_confidence": "high",
        },
    },
    {
        "form_id": "catalog_recording",
        "domain_area": "cataloging",
        "title": "Create or update descriptive record",
        "route": "POST /app/library-archives-management/catalog-records",
        "operation": "record_catalog_record",
        "permission": "library_archives_management.update",
        "owned_tables": (
            "library_archives_management_catalog_record",
            "library_archives_management_collection_item",
        ),
        "outcomes": (
            "Captures material-type-aware bibliographic or archival description.",
            "Flags missing descriptive elements before publication or circulation.",
        ),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "record_id", "type": "string", "required": True},
            {"name": "material_type", "type": "enum", "required": True, "choices": ("monograph", "serial", "map", "manuscript", "photograph", "oral_history", "born_digital_package")},
            {"name": "title", "type": "string", "required": True},
            {"name": "creator_heading", "type": "string", "required": True},
            {"name": "description_level", "type": "enum", "required": True, "choices": ("collection", "series", "file", "item")},
            {"name": "call_number", "type": "string", "required": True},
            {"name": "location_code", "type": "string", "required": True},
            {"name": "missing_fields", "type": "list", "required": True},
        ),
        "example_payload": {
            "tenant": "archives-east",
            "record_id": "CAT-00045",
            "material_type": "manuscript",
            "title": "Ngugi Family Papers",
            "creator_heading": "Ngugi family",
            "description_level": "collection",
            "call_number": "MS 1024",
            "location_code": "VAULT-A1",
            "missing_fields": ["biographical_note", "processing_information"],
        },
    },
    {
        "form_id": "authority_control_heading",
        "domain_area": "authority control",
        "title": "Normalize authority heading",
        "route": "POST /app/library-archives-management/authority-headings",
        "operation": "review_library_archives_management_policy_rule",
        "permission": "library_archives_management.update",
        "owned_tables": (
            "library_archives_management_catalog_record",
            "library_archives_management_library_archives_management_policy_rule",
        ),
        "outcomes": (
            "Captures preferred and variant headings with local override rationale.",
            "Supports merge and split review of people, bodies, and subjects.",
        ),
        "fields": (
            {"name": "heading_id", "type": "string", "required": True},
            {"name": "authority_type", "type": "enum", "required": True, "choices": ("person", "family", "corporate_body", "geographic", "topical")},
            {"name": "preferred_label", "type": "string", "required": True},
            {"name": "variant_labels", "type": "list", "required": True},
            {"name": "authority_source", "type": "enum", "required": True, "choices": ("lcnaf", "lcsh", "local", "wikidata", "community_protocol")},
            {"name": "local_override_reason", "type": "text", "required": True},
            {"name": "impacted_record_ids", "type": "list", "required": True},
        ),
        "example_payload": {
            "heading_id": "AUTH-119",
            "authority_type": "corporate_body",
            "preferred_label": "Kenya National Theatre",
            "variant_labels": ["National Theatre (Kenya)", "KNT"],
            "authority_source": "local",
            "local_override_reason": "Repository uses the creator's own published corporate identity in donor files.",
            "impacted_record_ids": ["CAT-00045", "CAT-00061"],
        },
    },
    {
        "form_id": "circulation_loan_checkout",
        "domain_area": "circulation/loans",
        "title": "Issue circulation loan",
        "route": "POST /app/library-archives-management/circulation-loans",
        "operation": "review_circulation_loan",
        "permission": "library_archives_management.create",
        "owned_tables": (
            "library_archives_management_circulation_loan",
            "library_archives_management_collection_item",
        ),
        "outcomes": (
            "Creates a library-style loan with due dates and circulation rules.",
            "Rejects archival or restricted items from general circulation.",
        ),
        "fields": (
            {"name": "loan_id", "type": "string", "required": True},
            {"name": "item_id", "type": "string", "required": True},
            {"name": "borrower_id", "type": "string", "required": True},
            {"name": "loan_type", "type": "enum", "required": True, "choices": ("general", "course_reserve", "staff", "exhibit", "reading_room")},
            {"name": "due_at", "type": "string", "required": True},
            {"name": "restriction_flags", "type": "list", "required": True},
        ),
        "example_payload": {
            "loan_id": "LOAN-2026-009",
            "item_id": "ITEM-BOOK-778",
            "borrower_id": "PATRON-204",
            "loan_type": "general",
            "due_at": "2026-06-20T17:00:00Z",
            "restriction_flags": [],
        },
    },
    {
        "form_id": "hold_request_management",
        "domain_area": "holds",
        "title": "Manage hold request",
        "route": "POST /app/library-archives-management/holds",
        "operation": "create_collection_item",
        "permission": "library_archives_management.update",
        "owned_tables": (
            "library_archives_management_collection_item",
            "library_archives_management_circulation_loan",
        ),
        "outcomes": (
            "Places, prioritizes, and expires holds.",
            "Keeps restricted or archival items in supervised request queues.",
        ),
        "fields": (
            {"name": "hold_id", "type": "string", "required": True},
            {"name": "item_id", "type": "string", "required": True},
            {"name": "requester_id", "type": "string", "required": True},
            {"name": "queue_priority", "type": "enum", "required": True, "choices": ("standard", "faculty", "research_priority", "preservation_review")},
            {"name": "pickup_mode", "type": "enum", "required": True, "choices": ("desk", "locker", "reading_room", "staff_delivery")},
            {"name": "expires_at", "type": "string", "required": True},
        ),
        "example_payload": {
            "hold_id": "HOLD-028",
            "item_id": "ITEM-BOOK-778",
            "requester_id": "PATRON-331",
            "queue_priority": "faculty",
            "pickup_mode": "desk",
            "expires_at": "2026-06-02T17:00:00Z",
        },
    },
    {
        "form_id": "acquisition_decision",
        "domain_area": "acquisitions",
        "title": "Record acquisition decision",
        "route": "POST /app/library-archives-management/acquisitions",
        "operation": "record_archive_request",
        "permission": "library_archives_management.approve",
        "owned_tables": (
            "library_archives_management_archive_request",
            "library_archives_management_rights_statement",
        ),
        "outcomes": (
            "Captures purchase, gift, or transfer decisions.",
            "Links budget, donor terms, and legal intake evidence before accessioning.",
        ),
        "fields": (
            {"name": "decision_id", "type": "string", "required": True},
            {"name": "acquisition_mode", "type": "enum", "required": True, "choices": ("purchase", "gift", "transfer", "deposit")},
            {"name": "seller_or_donor", "type": "string", "required": True},
            {"name": "value_basis", "type": "enum", "required": True, "choices": ("market_purchase", "donor_estimate", "insurance_estimate", "internal_transfer")},
            {"name": "budget_code", "type": "string", "required": True},
            {"name": "rights_clause_refs", "type": "list", "required": True},
            {"name": "decision_status", "type": "enum", "required": True, "choices": ("proposed", "approved", "rejected", "pending_board")},
        ),
        "example_payload": {
            "decision_id": "ACQ-2026-014",
            "acquisition_mode": "gift",
            "seller_or_donor": "Ngugi Family Trust",
            "value_basis": "donor_estimate",
            "budget_code": "SPECIAL-COLL-2026",
            "rights_clause_refs": ["DEED-OF-GIFT-4.2", "EMBARGO-CLAUSE-7"],
            "decision_status": "approved",
        },
    },
    {
        "form_id": "preservation_treatment",
        "domain_area": "preservation",
        "title": "Plan preservation action",
        "route": "POST /app/library-archives-management/preservation-actions",
        "operation": "create_preservation_action",
        "permission": "library_archives_management.update",
        "owned_tables": (
            "library_archives_management_preservation_action",
            "library_archives_management_collection_item",
        ),
        "outcomes": (
            "Registers stabilization or rehousing work with risk thresholds.",
            "Captures environmental exposure and handling requirements.",
        ),
        "fields": (
            {"name": "action_id", "type": "string", "required": True},
            {"name": "item_id", "type": "string", "required": True},
            {"name": "treatment_type", "type": "enum", "required": True, "choices": ("rehousing", "stabilization", "freeze_dry", "encapsulation", "format_migration")},
            {"name": "condition_state", "type": "enum", "required": True, "choices": ("stable", "fragile", "critical")},
            {"name": "environment_risks", "type": "list", "required": True},
            {"name": "target_storage", "type": "string", "required": True},
        ),
        "example_payload": {
            "action_id": "PRES-991",
            "item_id": "ITEM-MAP-551",
            "treatment_type": "rehousing",
            "condition_state": "fragile",
            "environment_risks": ["oversize_shelving", "light_exposure"],
            "target_storage": "OVERSIZE-CAB-03",
        },
    },
    {
        "form_id": "digitization_triage",
        "domain_area": "digitization",
        "title": "Triage digitization request",
        "route": "POST /app/library-archives-management/digitization-jobs",
        "operation": "approve_digitization_job",
        "permission": "library_archives_management.approve",
        "owned_tables": (
            "library_archives_management_digitization_job",
            "library_archives_management_rights_statement",
            "library_archives_management_preservation_action",
        ),
        "outcomes": (
            "Routes work to quick capture, conservation review, metadata cleanup, or rights review.",
            "Captures QC profile, fixity expectations, and publication intent.",
        ),
        "fields": (
            {"name": "job_id", "type": "string", "required": True},
            {"name": "item_id", "type": "string", "required": True},
            {"name": "capture_profile", "type": "enum", "required": True, "choices": ("text_ocr", "photo_master", "oversize_map", "av_reformat", "born_digital_package")},
            {"name": "condition_gate", "type": "enum", "required": True, "choices": ("quick_capture", "metadata_cleanup", "conservation_review", "rights_review")},
            {"name": "use_case", "type": "enum", "required": True, "choices": ("reading_room", "classroom", "web_publication", "preservation_copy")},
            {"name": "qc_checks", "type": "list", "required": True},
        ),
        "example_payload": {
            "job_id": "DIG-6001",
            "item_id": "ITEM-OH-44",
            "capture_profile": "av_reformat",
            "condition_gate": "rights_review",
            "use_case": "web_publication",
            "qc_checks": ["focus", "completeness", "caption_accuracy", "checksum"],
        },
    },
    {
        "form_id": "rights_access_restriction",
        "domain_area": "rights/access restrictions",
        "title": "Assess rights and access restrictions",
        "route": "POST /app/library-archives-management/rights-statements",
        "operation": "simulate_rights_statement",
        "permission": "library_archives_management.approve",
        "owned_tables": (
            "library_archives_management_rights_statement",
            "library_archives_management_archive_request",
            "library_archives_management_catalog_record",
        ),
        "outcomes": (
            "Determines allowed use by channel and jurisdiction.",
            "Propagates donor embargoes, cultural protocols, and privacy restrictions.",
        ),
        "fields": (
            {"name": "rights_id", "type": "string", "required": True},
            {"name": "item_id", "type": "string", "required": True},
            {"name": "access_level", "type": "enum", "required": True, "choices": ("open", "onsite_only", "staff_only", "sealed", "community_protocol")},
            {"name": "use_case_matrix", "type": "list", "required": True},
            {"name": "restriction_basis", "type": "list", "required": True},
            {"name": "review_due_on", "type": "string", "required": True},
        ),
        "example_payload": {
            "rights_id": "RIGHTS-204",
            "item_id": "ITEM-OH-44",
            "access_level": "onsite_only",
            "use_case_matrix": ["reading_room:allow", "web_publication:deny", "classroom:review"],
            "restriction_basis": ["donor_embargo", "privacy_sensitive_audio"],
            "review_due_on": "2027-01-15",
        },
    },
    {
        "form_id": "finding_aid_description",
        "domain_area": "finding aids",
        "title": "Edit hierarchical finding aid",
        "route": "POST /app/library-archives-management/finding-aids",
        "operation": "record_catalog_record",
        "permission": "library_archives_management.update",
        "owned_tables": (
            "library_archives_management_catalog_record",
            "library_archives_management_collection_item",
        ),
        "outcomes": (
            "Maintains collection, series, file, and item hierarchy.",
            "Allows inherited notes, restrictions, and container references.",
        ),
        "fields": (
            {"name": "finding_aid_id", "type": "string", "required": True},
            {"name": "parent_level", "type": "enum", "required": True, "choices": ("collection", "series", "subseries", "file", "item")},
            {"name": "component_title", "type": "string", "required": True},
            {"name": "container_refs", "type": "list", "required": True},
            {"name": "inherited_restrictions", "type": "list", "required": True},
            {"name": "scope_note", "type": "text", "required": True},
        ),
        "example_payload": {
            "finding_aid_id": "FA-1024-S1",
            "parent_level": "series",
            "component_title": "Series I: Literary Drafts",
            "container_refs": ["Box 1", "Box 2"],
            "inherited_restrictions": ["donor_embargo_until_2030"],
            "scope_note": "Includes handwritten and typescript drafts arranged by title.",
        },
    },
    {
        "form_id": "reading_room_request",
        "domain_area": "reading-room requests",
        "title": "Approve reading room request",
        "route": "POST /app/library-archives-management/reading-room-requests",
        "operation": "review_circulation_loan",
        "permission": "library_archives_management.create",
        "owned_tables": (
            "library_archives_management_archive_request",
            "library_archives_management_rights_statement",
            "library_archives_management_circulation_loan",
        ),
        "outcomes": (
            "Schedules researcher visits and item pulls.",
            "Enforces orientation, identity verification, and supervised handling rules.",
        ),
        "fields": (
            {"name": "request_id", "type": "string", "required": True},
            {"name": "researcher_id", "type": "string", "required": True},
            {"name": "item_ids", "type": "list", "required": True},
            {"name": "seat_type", "type": "enum", "required": True, "choices": ("general", "supervised", "av_booth", "special_collections")},
            {"name": "orientation_complete", "type": "boolean", "required": True},
            {"name": "requested_for", "type": "string", "required": True},
        ),
        "example_payload": {
            "request_id": "RR-0091",
            "researcher_id": "RES-771",
            "item_ids": ["ITEM-OH-44", "ITEM-MS-12"],
            "seat_type": "special_collections",
            "orientation_complete": True,
            "requested_for": "2026-06-03T09:00:00Z",
        },
    },
    {
        "form_id": "deaccession_case",
        "domain_area": "deaccessioning",
        "title": "Open deaccession case",
        "route": "POST /app/library-archives-management/deaccession-cases",
        "operation": "create_library_archives_management_control_assertion",
        "permission": "library_archives_management.approve",
        "owned_tables": (
            "library_archives_management_library_archives_management_control_assertion",
            "library_archives_management_collection_item",
            "library_archives_management_rights_statement",
        ),
        "outcomes": (
            "Opens governed withdrawal review with policy and donor checks.",
            "Retains audit trail for transfer, return, or disposal outcomes.",
        ),
        "fields": (
            {"name": "case_id", "type": "string", "required": True},
            {"name": "candidate_scope", "type": "enum", "required": True, "choices": ("item", "file", "series", "accession")},
            {"name": "reason_code", "type": "enum", "required": True, "choices": ("reappraisal", "duplication", "preservation_failure", "legal_return", "transfer")},
            {"name": "authorizing_policy", "type": "string", "required": True},
            {"name": "stakeholders", "type": "list", "required": True},
            {"name": "legal_hold_clear", "type": "boolean", "required": True},
        ),
        "example_payload": {
            "case_id": "DEACC-22",
            "candidate_scope": "accession",
            "reason_code": "transfer",
            "authorizing_policy": "COLL-MGMT-9.1",
            "stakeholders": ["university_archivist", "legal_counsel", "donor_relations"],
            "legal_hold_clear": True,
        },
    },
    {
        "form_id": "provenance_chain_update",
        "domain_area": "provenance",
        "title": "Capture provenance chain",
        "route": "POST /app/library-archives-management/provenance",
        "operation": "create_collection_item",
        "permission": "library_archives_management.update",
        "owned_tables": (
            "library_archives_management_collection_item",
            "library_archives_management_archive_request",
        ),
        "outcomes": (
            "Records creators, custodians, and custody gaps.",
            "Distinguishes asserted provenance from inferred relationships.",
        ),
        "fields": (
            {"name": "provenance_id", "type": "string", "required": True},
            {"name": "creator", "type": "string", "required": True},
            {"name": "custody_chain", "type": "list", "required": True},
            {"name": "gaps_or_uncertainties", "type": "list", "required": True},
            {"name": "assertion_basis", "type": "enum", "required": True, "choices": ("documented", "oral_history", "inferred")},
        ),
        "example_payload": {
            "provenance_id": "PROV-884",
            "creator": "Ministry of Culture, Theatre Division",
            "custody_chain": ["Theatre Division", "Department of Arts", "University Archives"],
            "gaps_or_uncertainties": ["1999-2001 custody unknown"],
            "assertion_basis": "documented",
        },
    },
    {
        "form_id": "conservation_treatment",
        "domain_area": "conservation",
        "title": "Authorize conservation treatment",
        "route": "POST /app/library-archives-management/conservation-treatments",
        "operation": "create_preservation_action",
        "permission": "library_archives_management.approve",
        "owned_tables": (
            "library_archives_management_preservation_action",
            "library_archives_management_collection_item",
        ),
        "outcomes": (
            "Approves interventive conservation with condition narratives.",
            "Tracks treatment reports and before/after evidence.",
        ),
        "fields": (
            {"name": "treatment_id", "type": "string", "required": True},
            {"name": "item_id", "type": "string", "required": True},
            {"name": "intervention_level", "type": "enum", "required": True, "choices": ("minimal", "stabilization", "full_treatment")},
            {"name": "conservator", "type": "string", "required": True},
            {"name": "before_condition", "type": "text", "required": True},
            {"name": "after_goal", "type": "text", "required": True},
        ),
        "example_payload": {
            "treatment_id": "CONS-410",
            "item_id": "ITEM-MAP-551",
            "intervention_level": "stabilization",
            "conservator": "A. Wanjiru",
            "before_condition": "Tears along fold lines with active surface dirt and brittle edges.",
            "after_goal": "Stabilize for supervised handling and oversize digitization.",
        },
    },
    {
        "form_id": "inventory_audit",
        "domain_area": "audits",
        "title": "Run collection audit",
        "route": "POST /app/library-archives-management/audits",
        "operation": "create_library_archives_management_control_assertion",
        "permission": "library_archives_management.admin",
        "owned_tables": (
            "library_archives_management_library_archives_management_control_assertion",
            "library_archives_management_collection_item",
            "library_archives_management_circulation_loan",
        ),
        "outcomes": (
            "Checks location accuracy, restrictions, and circulation exceptions.",
            "Creates auditable evidence for stewardship and compliance reviews.",
        ),
        "fields": (
            {"name": "audit_id", "type": "string", "required": True},
            {"name": "scope", "type": "enum", "required": True, "choices": ("stacks", "vault", "reading_room", "offsite", "digital_preservation")},
            {"name": "sample_size", "type": "string", "required": True},
            {"name": "findings", "type": "list", "required": True},
            {"name": "exception_severity", "type": "enum", "required": True, "choices": ("none", "low", "moderate", "high")},
        ),
        "example_payload": {
            "audit_id": "AUD-330",
            "scope": "vault",
            "sample_size": "125 containers",
            "findings": ["2 location mismatches", "0 missing items", "1 expired embargo flag"],
            "exception_severity": "moderate",
        },
    },
    {
        "form_id": "assistant_crud_preview",
        "domain_area": "assistant CRUD previews",
        "title": "Preview assistant CRUD request",
        "route": "POST /app/library-archives-management/assistant/crud-preview",
        "operation": "record_library_archives_management_governed_model",
        "permission": "library_archives_management.read",
        "owned_tables": OWNED_TABLE_CHOICES,
        "outcomes": (
            "Constrains assistant previews to owned tables only.",
            "Shows whether requested create, read, update, or delete actions require confirmation.",
        ),
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {"name": "requested_action", "type": "enum", "required": True, "choices": ("create", "read", "update", "delete")},
            {"name": "target_table", "type": "enum", "required": True, "choices": OWNED_TABLE_CHOICES},
            {"name": "operator_note", "type": "text", "required": False},
        ),
        "example_payload": {
            "document_text": "Researcher requests a preview of whether oral history transcripts can be opened for onsite consultation only.",
            "instructions": "Show a bounded update plan for the rights statement and preserve donor embargo lineage.",
            "requested_action": "update",
            "target_table": "library_archives_management_rights_statement",
            "operator_note": "Preview only, no mutation.",
        },
    },
)


def library_archives_management_form_catalog() -> dict:
    """Return the package-local forms registry."""
    forms = tuple(LIBRARY_ARCHIVES_MANAGEMENT_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": PBC_KEY,
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "domain_areas": tuple(dict.fromkeys(item["domain_area"] for item in forms)),
        "side_effects": (),
    }



def library_archives_management_get_form(form_id: str) -> dict:
    """Return one form definition by identifier."""
    form = next((item for item in LIBRARY_ARCHIVES_MANAGEMENT_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": PBC_KEY,
        "form": form,
        "side_effects": (),
    }



def library_archives_management_form_examples() -> dict:
    """Return package-local example payloads keyed by form identifier."""
    examples = {
        item["form_id"]: dict(item.get("example_payload", {}))
        for item in LIBRARY_ARCHIVES_MANAGEMENT_FORM_DEFINITIONS
    }
    return {
        "ok": bool(examples),
        "pbc": PBC_KEY,
        "examples": examples,
        "side_effects": (),
    }



def library_archives_management_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate a payload against the package-local form definitions."""
    form = library_archives_management_get_form(form_id).get("form")
    if form is None:
        return {
            "ok": False,
            "accepted": False,
            "reason": "unknown_form",
            "form_id": form_id,
            "side_effects": (),
        }

    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and (supplied.get(field["name"]) is None or supplied.get(field["name"]) == "")
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum"
        and supplied.get(field["name"]) not in {None, *field.get("choices", ())}
    )
    invalid_lists = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "list"
        and supplied.get(field["name"]) is not None
        and not isinstance(supplied.get(field["name"]), (list, tuple))
    )
    invalid_booleans = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "boolean"
        and supplied.get(field["name"]) is not None
        and not isinstance(supplied.get(field["name"]), bool)
    )
    accepted = not missing and not invalid_choices and not invalid_lists and not invalid_booleans
    return {
        "ok": accepted,
        "accepted": accepted,
        "pbc": PBC_KEY,
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "invalid_lists": invalid_lists,
        "invalid_booleans": invalid_booleans,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise the package-local form registry and example validation."""
    catalog = library_archives_management_form_catalog()
    examples = library_archives_management_form_examples()
    validations = tuple(
        library_archives_management_validate_form_payload(form_id, examples["examples"][form_id])
        for form_id in catalog["form_ids"]
    )
    return {
        "ok": catalog["ok"] and examples["ok"] and all(item["ok"] for item in validations),
        "catalog": catalog,
        "examples": examples,
        "validations": validations,
        "side_effects": (),
    }
