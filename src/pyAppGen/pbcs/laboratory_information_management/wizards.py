"""Package-local guided wizards for the Laboratory Information Management workbench."""

from __future__ import annotations

from .forms import laboratory_information_management_form_catalog


LABORATORY_INFORMATION_MANAGEMENT_WIZARDS = (
    {
        "wizard_id": "accession_to_release",
        "title": "Accession to release",
        "goal": "Move a controlled sample from accessioning to reviewed and approved result release.",
        "steps": (
            {"step_id": "accession", "label": "Accession sample", "form_id": "sample_accessioning", "operation": "accession_sample"},
            {"step_id": "custody", "label": "Record custody", "form_id": "chain_of_custody_handoff", "operation": "record_chain_of_custody"},
            {"step_id": "order", "label": "Place test order", "form_id": "test_order_intake", "operation": "place_test_order"},
            {"step_id": "batch", "label": "Create batch run", "form_id": "batch_run_execution", "operation": "create_batch_run"},
            {"step_id": "release", "label": "Review and release", "form_id": "result_review_and_release", "operation": "release_result"},
        ),
    },
    {
        "wizard_id": "qc_and_oos_recovery",
        "title": "QC and OOS recovery",
        "goal": "Assess QC, open an investigation, and document CAPA before release continues.",
        "steps": (
            {"step_id": "lot", "label": "Inspect QC lot", "form_id": "qc_and_reagent_lot", "operation": "register_qc_lot"},
            {"step_id": "investigation", "label": "Open investigation", "form_id": "oos_investigation", "operation": "open_oos_investigation"},
            {"step_id": "release_hold", "label": "Re-evaluate release", "form_id": "result_review_and_release", "operation": "release_result"},
        ),
    },
    {
        "wizard_id": "method_readiness",
        "title": "Method readiness",
        "goal": "Prepare a method, qualified instrument, calibration, reagent lot, and analyst competency for execution.",
        "steps": (
            {"step_id": "method", "label": "Register method", "form_id": "method_and_sop_register", "operation": "register_method"},
            {"step_id": "instrument", "label": "Prepare instrument", "form_id": "instrument_calibration_console", "operation": "manage_instrument"},
            {"step_id": "lots", "label": "Qualify QC and reagents", "form_id": "qc_and_reagent_lot", "operation": "register_qc_lot"},
        ),
    },
    {
        "wizard_id": "stability_and_coa",
        "title": "Stability and CoA",
        "goal": "Schedule stability pulls, complete evidence, and issue a compliant certificate of analysis.",
        "steps": (
            {"step_id": "study", "label": "Create stability study", "form_id": "stability_study_scheduler", "operation": "create_stability_study"},
            {"step_id": "coa", "label": "Generate CoA", "form_id": "certificate_of_analysis", "operation": "generate_certificate_of_analysis"},
            {"step_id": "audit", "label": "Preview audit packet", "form_id": "assistant_document_preview", "operation": "document_instruction_preview"},
        ),
    },
    {
        "wizard_id": "assistant_guided_change",
        "title": "Assistant-guided change preview",
        "goal": "Turn a lab memo or worksheet into a governed CRUD preview with citations and confirmation gates.",
        "steps": (
            {"step_id": "capture", "label": "Capture document", "form_id": "assistant_document_preview", "operation": "document_instruction_preview"},
            {"step_id": "review_scope", "label": "Review boundary", "form_id": "assistant_document_preview", "operation": "document_instruction_preview"},
            {"step_id": "review_action", "label": "Review preview", "form_id": "assistant_document_preview", "operation": "document_instruction_preview"},
        ),
    },
)


def laboratory_information_management_wizard_catalog() -> dict:
    """Return the guided wizard registry for this PBC."""
    forms = laboratory_information_management_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in LABORATORY_INFORMATION_MANAGEMENT_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(LABORATORY_INFORMATION_MANAGEMENT_WIZARDS) and not missing_form_bindings,
        "pbc": "laboratory_information_management",
        "wizards": LABORATORY_INFORMATION_MANAGEMENT_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in LABORATORY_INFORMATION_MANAGEMENT_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def laboratory_information_management_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided wizard plan with lightweight readiness hints."""
    wizard = next((item for item in LABORATORY_INFORMATION_MANAGEMENT_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "accession_to_release" and step["step_id"] in {"order", "batch", "release"} and not supplied.get("sample_id"):
            blocked_by = ("sample_id",)
        if wizard_id == "accession_to_release" and step["step_id"] in {"batch", "release"} and not supplied.get("order_id"):
            blocked_by = tuple(dict.fromkeys(blocked_by + ("order_id",)))
        if wizard_id == "qc_and_oos_recovery" and step["step_id"] != "lot" and not supplied.get("result_id"):
            blocked_by = ("result_id",)
        if wizard_id == "stability_and_coa" and step["step_id"] != "study" and not supplied.get("order_id"):
            blocked_by = ("order_id",)
        planned_steps.append({**step, "position": position, "ready": not blocked_by, "blocked_by": blocked_by})
    return {
        "ok": True,
        "pbc": "laboratory_information_management",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise wizard catalog and a guided plan."""
    catalog = laboratory_information_management_wizard_catalog()
    plan = laboratory_information_management_plan_wizard("accession_to_release", {"sample_id": "SMP-001", "order_id": "ORD-001"})
    return {"ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]), "catalog": catalog, "plan": plan, "side_effects": ()}
