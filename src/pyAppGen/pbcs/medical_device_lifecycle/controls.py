"""Package-local operational controls for the Medical Device Lifecycle workbench."""

from __future__ import annotations

from .runtime import medical_device_lifecycle_build_release_evidence
from .runtime import medical_device_lifecycle_verify_owned_table_boundary


MEDICAL_DEVICE_LIFECYCLE_CONTROLS = (
    {
        "control_id": "assignment_safety_gate",
        "title": "Assignment safety gate",
        "description": "Blocks assignment when the device is recalled, calibration overdue, maintenance-bound, retired, or quarantined.",
        "permission": "medical_device_lifecycle.approve",
    },
    {
        "control_id": "calibration_due_gate",
        "title": "Calibration due gate",
        "description": "Flags overdue or failed calibration and keeps out-of-tolerance devices unavailable pending review.",
        "permission": "medical_device_lifecycle.approve",
    },
    {
        "control_id": "maintenance_release_gate",
        "title": "Maintenance release gate",
        "description": "Requires maintenance qualification evidence before returning the device to service.",
        "permission": "medical_device_lifecycle.approve",
    },
    {
        "control_id": "recall_containment_gate",
        "title": "Recall containment gate",
        "description": "Tracks recall hold inventory, affected assignments, remediation backlog, and unresolved deadlines.",
        "permission": "medical_device_lifecycle.admin",
    },
    {
        "control_id": "regulatory_packet_completeness",
        "title": "Regulatory packet completeness",
        "description": "Shows devices missing manuals, service records, calibration certificates, or recall letters required for evidence packets.",
        "permission": "medical_device_lifecycle.read",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Keeps document-driven previews inside the owned datastore boundary and confirmation-gated for mutations.",
        "permission": "medical_device_lifecycle.read",
    },
)


def medical_device_lifecycle_control_catalog() -> dict:
    """Return the package-local operational controls."""
    return {
        "ok": bool(MEDICAL_DEVICE_LIFECYCLE_CONTROLS),
        "pbc": "medical_device_lifecycle",
        "controls": MEDICAL_DEVICE_LIFECYCLE_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in MEDICAL_DEVICE_LIFECYCLE_CONTROLS),
        "side_effects": (),
    }


def medical_device_lifecycle_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a requested mutation remains package-owned and safety-sensitive."""
    normalized = str(action).lower()
    boundary = medical_device_lifecycle_verify_owned_table_boundary((table,))
    regulatory_facing = table in {
        "medical_device_lifecycle_recall_notice",
        "medical_device_lifecycle_regulatory_evidence",
        "medical_device_lifecycle_medical_device",
    }
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": "medical_device_lifecycle",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": normalized != "read",
        "patient_safety_sensitive": regulatory_facing,
        "boundary": boundary,
        "side_effects": (),
    }


def medical_device_lifecycle_control_center(summary: dict | None = None) -> dict:
    """Return executable operational control evidence for the standalone slice."""
    if summary is None:
        from .standalone import medical_device_lifecycle_standalone_app_smoke

        summary = medical_device_lifecycle_standalone_app_smoke()["workbench"]

    release = medical_device_lifecycle_build_release_evidence()
    accepted_boundary = medical_device_lifecycle_verify_owned_table_boundary(
        (
            "medical_device_lifecycle_medical_device",
            "medical_device_lifecycle_device_assignment",
            "medical_device_lifecycle_recall_notice",
        )
    )
    rejected_boundary = medical_device_lifecycle_verify_owned_table_boundary(("foreign_table",))
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
    }
    blocking_items = tuple(
        item
        for item, active in (
            ("calibration_due", summary.get("calibration_due_count", 0) > 0),
            ("maintenance_due", summary.get("maintenance_due_count", 0) > 0),
            ("recall_hold", summary.get("recall_hold_count", 0) > 0),
            ("missing_evidence", summary.get("missing_evidence_count", 0) > 0),
        )
        if active
    )
    return {
        "ok": release["ok"] and assistant_guardrails["boundary_ok"],
        "pbc": "medical_device_lifecycle",
        "controls": medical_device_lifecycle_control_catalog()["controls"],
        "release": release,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_guardrails": assistant_guardrails,
        "blocking_items": blocking_items,
        "summary": summary,
        "side_effects": (),
    }


def smoke_test() -> dict:
    preview = medical_device_lifecycle_mutation_preview(
        "update",
        "medical_device_lifecycle_recall_notice",
        {"status": "open"},
    )
    center = medical_device_lifecycle_control_center(
        {
            "calibration_due_count": 1,
            "maintenance_due_count": 0,
            "recall_hold_count": 0,
            "missing_evidence_count": 0,
        }
    )
    return {
        "ok": preview["ok"] and center["ok"],
        "preview": preview,
        "control_center": center,
        "side_effects": (),
    }
