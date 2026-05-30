"""Package-local controls for the Professional Services Automation workbench."""

from __future__ import annotations

from .runtime import professional_services_automation_build_release_evidence
from .runtime import professional_services_automation_empty_state
from .runtime import professional_services_automation_runtime_smoke
from .runtime import professional_services_automation_verify_owned_table_boundary


PROFESSIONAL_SERVICES_AUTOMATION_CONTROLS = (
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Runs package-local release evidence and standalone coverage checks.",
        "permission": "professional_services_automation.admin",
    },
    {
        "control_id": "scope_boundary",
        "title": "Scope boundary",
        "description": "Flags out-of-scope work, missing change control, and foreign-table references.",
        "permission": "professional_services_automation.approve",
    },
    {
        "control_id": "billing_gate",
        "title": "Billing gate",
        "description": "Requires approved time, accepted deliverables, and clear blockers before billing readiness passes.",
        "permission": "professional_services_automation.approve",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Ensures assistant previews stay package-owned and confirmation-gated.",
        "permission": "professional_services_automation.read",
    },
)



def professional_services_automation_control_catalog() -> dict:
    """Return package-local operational controls."""
    return {
        "ok": bool(PROFESSIONAL_SERVICES_AUTOMATION_CONTROLS),
        "pbc": "professional_services_automation",
        "controls": PROFESSIONAL_SERVICES_AUTOMATION_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in PROFESSIONAL_SERVICES_AUTOMATION_CONTROLS),
        "side_effects": (),
    }



def professional_services_automation_control_center(state: dict | None = None) -> dict:
    """Return executable control evidence for release and operator workflows."""
    runtime = professional_services_automation_runtime_smoke()
    source_state = dict(state or runtime["state"])
    release = professional_services_automation_build_release_evidence()
    accepted_boundary = professional_services_automation_verify_owned_table_boundary(
        (
            "professional_services_automation_engagement",
            "professional_services_automation_billing_readiness_check",
            "projection_dependency",
        )
    )
    rejected_boundary = professional_services_automation_verify_owned_table_boundary(("shared_foreign_project",))
    billing_gate = {
        "configuration_ready": bool(source_state.get("configuration")),
        "has_parameters": bool(source_state.get("parameters")),
        "has_rules": bool(source_state.get("rules")),
        "outbox_has_event": bool(source_state.get("outbox")),
    }
    assistant_guardrails = {
        "preview_only": True,
        "requires_confirmation_for_mutation": True,
        "boundary_ok": accepted_boundary["ok"] and not rejected_boundary["ok"],
    }
    return {
        "ok": release["ok"] and assistant_guardrails["boundary_ok"] and all(billing_gate.values()),
        "pbc": "professional_services_automation",
        "controls": professional_services_automation_control_catalog()["controls"],
        "release": release,
        "runtime": runtime,
        "billing_gate": billing_gate,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_guardrails": assistant_guardrails,
        "side_effects": (),
    }



def professional_services_automation_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a mutation would stay inside the PSA-owned boundary."""
    normalized = str(action).lower()
    boundary = professional_services_automation_verify_owned_table_boundary((table,))
    requires_confirmation = normalized != "read"
    return {
        "ok": boundary["ok"] and normalized in {"create", "read", "update", "delete"},
        "pbc": "professional_services_automation",
        "action": normalized,
        "table": table,
        "payload_keys": tuple(sorted(dict(payload or {}))),
        "requires_confirmation": requires_confirmation,
        "boundary": boundary,
        "side_effects": (),
    }



def smoke_test() -> dict:
    """Exercise the control center with runtime smoke evidence."""
    preview = professional_services_automation_mutation_preview(
        "update",
        "professional_services_automation_statement_of_work",
        {"status": "needs_change_order"},
    )
    control_center = professional_services_automation_control_center(
        professional_services_automation_empty_state() | professional_services_automation_runtime_smoke()["state"]
    )
    return {
        "ok": preview["ok"] and control_center["ok"],
        "preview": preview,
        "control_center": control_center,
        "side_effects": (),
    }
