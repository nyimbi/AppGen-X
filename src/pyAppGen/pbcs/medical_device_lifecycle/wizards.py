"""Package-local guided wizards for the Medical Device Lifecycle workbench."""

from __future__ import annotations

from .forms import medical_device_lifecycle_form_catalog


MEDICAL_DEVICE_LIFECYCLE_WIZARDS = (
    {
        "wizard_id": "device_onboarding_and_qualification",
        "title": "Device onboarding and qualification",
        "goal": "Register a device, confirm governing rules, and record its initial calibration or qualification posture.",
        "keywords": ("register", "qualify", "incoming inspection", "new device", "udi"),
        "steps": (
            {"step_id": "register_device", "label": "Register device", "form_id": "medical_device_registry_intake", "operation": "register_device"},
            {"step_id": "confirm_rules", "label": "Confirm lifecycle rules", "form_id": "policy_rule_editor", "operation": "upsert_policy_rule"},
            {"step_id": "set_runtime", "label": "Set runtime thresholds", "form_id": "runtime_parameter_editor", "operation": "update_runtime_parameter"},
            {"step_id": "capture_calibration", "label": "Record calibration", "form_id": "calibration_review", "operation": "record_calibration"},
        ),
    },
    {
        "wizard_id": "point_of_care_assignment",
        "title": "Point-of-care assignment",
        "goal": "Assign a safe, qualified device while preserving privacy and readiness controls.",
        "keywords": ("assign", "point of care", "room", "patient", "implant"),
        "steps": (
            {"step_id": "review_assignment_gate", "label": "Review assignment controls", "form_id": "assistant_document_intake", "operation": "preview_document_change"},
            {"step_id": "assign_device", "label": "Assign device", "form_id": "device_assignment_governance", "operation": "assign_device"},
            {"step_id": "capture_usage", "label": "Capture first use", "form_id": "usage_trace_capture", "operation": "record_usage_trace"},
        ),
    },
    {
        "wizard_id": "calibration_and_return_to_service",
        "title": "Calibration and return-to-service",
        "goal": "Review calibration findings, complete maintenance, and return a device to service only when safe.",
        "keywords": ("calibration", "maintenance", "return to service", "repair"),
        "steps": (
            {"step_id": "review_calibration", "label": "Review calibration", "form_id": "calibration_review", "operation": "record_calibration"},
            {"step_id": "record_maintenance", "label": "Record maintenance", "form_id": "maintenance_return_to_service", "operation": "record_maintenance"},
            {"step_id": "attach_service_evidence", "label": "Attach evidence", "form_id": "regulatory_evidence_packet", "operation": "attach_regulatory_evidence"},
        ),
    },
    {
        "wizard_id": "recall_containment_and_notification",
        "title": "Recall containment and notification",
        "goal": "Contain recalled devices, identify affected assignments, and assemble remediation evidence.",
        "keywords": ("recall", "field safety notice", "quarantine", "patient notification"),
        "steps": (
            {"step_id": "launch_recall", "label": "Launch recall", "form_id": "recall_containment", "operation": "launch_recall"},
            {"step_id": "inspect_controls", "label": "Inspect control center", "form_id": "assistant_document_intake", "operation": "build_control_center"},
            {"step_id": "attach_recall_evidence", "label": "Attach recall evidence", "form_id": "regulatory_evidence_packet", "operation": "attach_regulatory_evidence"},
        ),
    },
    {
        "wizard_id": "assistant_change_preview",
        "title": "Assistant-guided change preview",
        "goal": "Turn a calibration memo, maintenance note, or recall letter into a governed preview-only CRUD plan.",
        "keywords": ("document", "instruction", "preview", "assistant", "change plan"),
        "steps": (
            {"step_id": "capture_document", "label": "Capture document", "form_id": "assistant_document_intake", "operation": "preview_document_change"},
            {"step_id": "review_boundary", "label": "Review datastore boundary", "form_id": "assistant_document_intake", "operation": "preview_document_change"},
            {"step_id": "review_route", "label": "Review route candidates", "form_id": "assistant_document_intake", "operation": "preview_document_change"},
        ),
    },
)


def medical_device_lifecycle_wizard_catalog() -> dict:
    """Return guided wizard definitions for this PBC."""
    forms = medical_device_lifecycle_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in MEDICAL_DEVICE_LIFECYCLE_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(MEDICAL_DEVICE_LIFECYCLE_WIZARDS) and not missing_form_bindings,
        "pbc": "medical_device_lifecycle",
        "wizards": MEDICAL_DEVICE_LIFECYCLE_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in MEDICAL_DEVICE_LIFECYCLE_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def medical_device_lifecycle_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return one guided wizard plan with lightweight blocking hints."""
    wizard = next((item for item in MEDICAL_DEVICE_LIFECYCLE_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}

    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by: tuple[str, ...] = ()
        if wizard_id == "point_of_care_assignment" and step["step_id"] != "review_assignment_gate" and not supplied.get("device_id"):
            blocked_by = ("device_id",)
        elif wizard_id == "calibration_and_return_to_service" and step["step_id"] != "review_calibration" and not supplied.get("maintenance_id"):
            blocked_by = ("maintenance_id",)
        elif wizard_id == "recall_containment_and_notification" and step["step_id"] != "launch_recall" and not supplied.get("recall_id"):
            blocked_by = ("recall_id",)
        planned_steps.append({**step, "position": position, "ready": not blocked_by, "blocked_by": blocked_by})
    return {
        "ok": True,
        "pbc": "medical_device_lifecycle",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    catalog = medical_device_lifecycle_wizard_catalog()
    plan = medical_device_lifecycle_plan_wizard("point_of_care_assignment", {"device_id": "DEV-1"})
    return {
        "ok": catalog["ok"] and plan["ok"] and bool(plan["steps"]),
        "catalog": catalog,
        "plan": plan,
        "side_effects": (),
    }
