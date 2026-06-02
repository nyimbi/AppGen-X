"""Package-local controls for the Library and Archives Management workbench."""

from __future__ import annotations

from .agent import datastore_crud_plan
from .agent import document_instruction_plan
from .forms import library_archives_management_form_examples
from .forms import library_archives_management_form_catalog
from .forms import library_archives_management_validate_form_payload
from .runtime import LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES
from .runtime import library_archives_management_build_release_evidence
from .runtime import library_archives_management_empty_state
from .runtime import library_archives_management_execute_domain_operation
from .runtime import library_archives_management_run_advanced_assessment
from .runtime import library_archives_management_runtime_smoke
from .runtime import library_archives_management_verify_owned_table_boundary
from .wizards import library_archives_management_plan_wizard
from .wizards import library_archives_management_wizard_catalog

PBC_KEY = "library_archives_management"

LIBRARY_ARCHIVES_MANAGEMENT_CONTROLS = (
    {
        "control_id": "accession_lineage_gate",
        "title": "Accession and provenance lineage gate",
        "description": "Checks that accession intake, provenance, and donor restrictions stay linked before material moves downstream.",
        "permission": "library_archives_management.audit",
        "domain_areas": ("accessioning", "acquisitions", "provenance", "rights/access restrictions"),
    },
    {
        "control_id": "authority_and_description_quality",
        "title": "Authority and description quality",
        "description": "Validates authority normalization, descriptive completeness, and finding-aid hierarchy coverage.",
        "permission": "library_archives_management.audit",
        "domain_areas": ("cataloging", "authority control", "finding aids"),
    },
    {
        "control_id": "circulation_and_reading_room_guardrail",
        "title": "Circulation and reading room guardrail",
        "description": "Prevents archival and restricted material from being treated like unrestricted circulating stock.",
        "permission": "library_archives_management.audit",
        "domain_areas": ("circulation/loans", "holds", "reading-room requests", "rights/access restrictions"),
    },
    {
        "control_id": "preservation_digitization_gate",
        "title": "Preservation and digitization gate",
        "description": "Requires preservation, conservation, rights, and QC evidence before capture or publication.",
        "permission": "library_archives_management.audit",
        "domain_areas": ("preservation", "conservation", "digitization", "rights/access restrictions"),
    },
    {
        "control_id": "deaccession_audit_proof",
        "title": "Deaccession audit proof",
        "description": "Checks audit evidence, legal hold status, provenance, and authorization before withdrawal or transfer.",
        "permission": "library_archives_management.admin",
        "domain_areas": ("deaccessioning", "audits", "provenance", "rights/access restrictions"),
    },
    {
        "control_id": "assistant_boundary_guardrail",
        "title": "Assistant boundary guardrail",
        "description": "Ensures CRUD previews remain inside owned tables and stay confirmation-gated for mutations.",
        "permission": "library_archives_management.audit",
        "domain_areas": ("assistant CRUD previews", "audits"),
    },
)



def library_archives_management_control_catalog() -> dict:
    """Return package-local control metadata."""
    return {
        "ok": bool(LIBRARY_ARCHIVES_MANAGEMENT_CONTROLS),
        "pbc": PBC_KEY,
        "controls": LIBRARY_ARCHIVES_MANAGEMENT_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in LIBRARY_ARCHIVES_MANAGEMENT_CONTROLS),
        "domain_areas": tuple(
            dict.fromkeys(area for item in LIBRARY_ARCHIVES_MANAGEMENT_CONTROLS for area in item["domain_areas"])
        ),
        "side_effects": (),
    }



def library_archives_management_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a requested mutation respects the package-owned boundary."""
    preview = datastore_crud_plan(action, table=table, payload=payload)
    boundary = library_archives_management_verify_owned_table_boundary((table,))
    return {
        "ok": preview.get("ok") is True and boundary.get("ok") is True,
        "pbc": PBC_KEY,
        "action": action,
        "table": table,
        "preview": preview,
        "boundary": boundary,
        "side_effects": (),
    }



def library_archives_management_assistant_crud_preview(
    document_text: str,
    instruction: str,
    *,
    action: str,
    target_table: str,
    payload: dict | None = None,
) -> dict:
    """Build a bounded assistant CRUD preview."""
    document_plan = document_instruction_plan(document_text, instruction)
    crud_plan = datastore_crud_plan(action, table=target_table, payload=payload)
    return {
        "ok": document_plan.get("ok") is True and crud_plan.get("ok") is True,
        "pbc": PBC_KEY,
        "document_plan": document_plan,
        "crud_plan": crud_plan,
        "side_effects": (),
    }



def library_archives_management_control_center(context: dict | None = None) -> dict:
    """Return executable control evidence for the standalone workbench."""
    supplied = dict(context or {})
    catalog = library_archives_management_control_catalog()
    forms = library_archives_management_form_catalog()
    examples = library_archives_management_form_examples()
    wizards = library_archives_management_wizard_catalog()
    runtime = library_archives_management_runtime_smoke()
    release = library_archives_management_build_release_evidence()
    assessment = library_archives_management_run_advanced_assessment(
        library_archives_management_empty_state(),
        {"tenant": supplied.get("tenant", "default"), "mode": "control_center"},
    )
    accepted_boundary = library_archives_management_verify_owned_table_boundary(
        (
            "library_archives_management_collection_item",
            "library_archives_management_catalog_record",
            "library_archives_management_archive_request",
        )
    )
    rejected_boundary = library_archives_management_verify_owned_table_boundary(("foreign_table",))
    assistant_preview = library_archives_management_assistant_crud_preview(
        "Preview an onsite-only access change for an oral history collection.",
        "Update the rights statement and keep the action confirmation-gated.",
        action="update",
        target_table="library_archives_management_rights_statement",
        payload={"access_level": "onsite_only"},
    )
    foreign_preview = datastore_crud_plan("delete", table="foreign_table", payload={})
    validations = tuple(
        library_archives_management_validate_form_payload(form_id, examples["examples"][form_id])
        for form_id in forms["form_ids"]
    )
    wizard_plans = (
        library_archives_management_plan_wizard(
            "acquisition_to_accession",
            {"decision_id": "ACQ-2026-014", "accession_number": "2026-045", "provenance_id": "PROV-884"},
        ),
        library_archives_management_plan_wizard(
            "reading_room_service",
            {"request_id": "RR-0091", "researcher_id": "RES-771", "item_ids": ["ITEM-OH-44"]},
        ),
        library_archives_management_plan_wizard(
            "deaccession_and_audit",
            {"audit_id": "AUD-330", "provenance_id": "PROV-884", "rights_id": "RIGHTS-204"},
        ),
    )
    domain_operations = tuple(
        library_archives_management_execute_domain_operation(operation, {"tenant": supplied.get("tenant", "default")})
        for operation in (
            "record_archive_request",
            "record_catalog_record",
            "review_circulation_loan",
            "approve_digitization_job",
            "simulate_rights_statement",
            "create_preservation_action",
            "create_library_archives_management_control_assertion",
            "record_library_archives_management_governed_model",
        )
    )
    checks = (
        {"id": "catalog_present", "ok": catalog["ok"]},
        {"id": "form_examples_validate", "ok": all(item["ok"] for item in validations)},
        {"id": "wizard_bindings_valid", "ok": wizards["ok"] and all(plan["ok"] for plan in wizard_plans)},
        {"id": "runtime_smoke", "ok": runtime["ok"]},
        {"id": "release_evidence", "ok": release["ok"]},
        {"id": "assessment", "ok": assessment["ok"]},
        {"id": "accepted_boundary", "ok": accepted_boundary["ok"]},
        {"id": "rejected_boundary", "ok": rejected_boundary["ok"] is False},
        {"id": "assistant_preview", "ok": assistant_preview["ok"]},
        {"id": "foreign_preview_rejected", "ok": foreign_preview["ok"] is False},
        {"id": "domain_operations", "ok": all(item["ok"] for item in domain_operations)},
    )
    return {
        "ok": all(check["ok"] for check in checks),
        "pbc": PBC_KEY,
        "controls": catalog["controls"],
        "forms": forms,
        "wizards": wizards,
        "release": release,
        "runtime": runtime,
        "assessment": assessment,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_preview": assistant_preview,
        "foreign_preview": foreign_preview,
        "wizard_plans": wizard_plans,
        "validations": validations,
        "domain_operations": domain_operations,
        "checks": checks,
        "supported_domain_areas": tuple(
            dict.fromkeys(forms["domain_areas"] + wizards["domain_areas"] + catalog["domain_areas"])
        ),
        "owned_tables": tuple(LIBRARY_ARCHIVES_MANAGEMENT_OWNED_TABLES),
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise the control center and a direct mutation preview."""
    preview = library_archives_management_mutation_preview(
        "read",
        "library_archives_management_catalog_record",
        {"record_id": "CAT-00045"},
    )
    center = library_archives_management_control_center({"tenant": "archives-east"})
    return {
        "ok": preview["ok"] and center["ok"],
        "preview": preview,
        "control_center": center,
        "side_effects": (),
    }
