"""Package-local controls for the Laboratory Information Management workbench."""

from __future__ import annotations

from .runtime import LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES


LABORATORY_INFORMATION_MANAGEMENT_CONTROLS = (
    {
        "control_id": "sample_identity_gate",
        "title": "Sample identity gate",
        "description": "Blocks duplicate accession numbers, low identity confidence, and unresolved custody exceptions.",
        "permission": "laboratory_information_management.approve",
    },
    {
        "control_id": "instrument_and_calibration_gate",
        "title": "Instrument and calibration gate",
        "description": "Prevents batch execution on unqualified instruments, expired calibration, or missing analyst competency.",
        "permission": "laboratory_information_management.admin",
    },
    {
        "control_id": "qc_release_gate",
        "title": "QC release gate",
        "description": "Stops release when required QC is missing, failed, or unresolved.",
        "permission": "laboratory_information_management.approve",
    },
    {
        "control_id": "regulatory_audit_trail",
        "title": "Regulatory audit trail",
        "description": "Maintains a tamper-evident hash chain and e-signature evidence for reportable actions.",
        "permission": "laboratory_information_management.admin",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Keeps document-driven CRUD previews inside owned tables with citations and confirmation requirements.",
        "permission": "laboratory_information_management.read",
    },
    {
        "control_id": "stability_and_inventory_watch",
        "title": "Stability and inventory watch",
        "description": "Highlights due stability pulls, expiring reagent lots, and analyst competency renewals.",
        "permission": "laboratory_information_management.update",
    },
)


def laboratory_information_management_control_catalog() -> dict:
    """Return package-local operational controls."""
    return {
        "ok": bool(LABORATORY_INFORMATION_MANAGEMENT_CONTROLS),
        "pbc": "laboratory_information_management",
        "controls": LABORATORY_INFORMATION_MANAGEMENT_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in LABORATORY_INFORMATION_MANAGEMENT_CONTROLS),
        "side_effects": (),
    }


def laboratory_information_management_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether an assistant mutation stays inside the LIMS owned boundary."""
    normalized = str(action).lower()
    boundary_ok = table in LABORATORY_INFORMATION_MANAGEMENT_OWNED_TABLES and table.startswith("laboratory_information_management_")
    return {
        "ok": boundary_ok and normalized in {"create", "read", "update", "delete"},
        "pbc": "laboratory_information_management",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": normalized != "read",
        "citation_required": normalized != "read",
        "boundary_ok": boundary_ok,
        "side_effects": (),
    }


def laboratory_information_management_control_center(summary: dict | None = None) -> dict:
    """Render a lightweight control center from a workbench summary."""
    source = dict(summary or {})
    queue_counts = source.get("queue_counts", {})
    audit = source.get("audit", {})
    assistant = source.get("assistant_guardrails", {})
    return {
        "ok": bool(LABORATORY_INFORMATION_MANAGEMENT_CONTROLS),
        "pbc": "laboratory_information_management",
        "controls": laboratory_information_management_control_catalog()["controls"],
        "queue_counts": queue_counts,
        "audit_integrity_ok": audit.get("ok", True),
        "assistant_guardrails": {
            "preview_only": assistant.get("preview_only", True),
            "requires_confirmation_for_mutation": assistant.get("requires_confirmation_for_mutation", True),
            "citations_required": assistant.get("citations_required", True),
        },
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise control catalog and a package-owned mutation preview."""
    preview = laboratory_information_management_mutation_preview("update", "laboratory_information_management_result", {"result_id": "RES-001"})
    center = laboratory_information_management_control_center(
        {
            "queue_counts": {"qc_failures": 1, "results_review": 2},
            "audit": {"ok": True},
            "assistant_guardrails": {
                "preview_only": True,
                "requires_confirmation_for_mutation": True,
                "citations_required": True,
            },
        }
    )
    return {"ok": preview["ok"] and center["ok"], "preview": preview, "control_center": center, "side_effects": ()}
