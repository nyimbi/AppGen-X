"""Package-local controls for the Composition Engine workbench."""

from __future__ import annotations

from .runtime import composition_engine_assistant_document_preview
from .runtime import composition_engine_build_control_center
from .runtime import composition_engine_build_release_evidence
from .runtime import composition_engine_empty_state
from .runtime import composition_engine_release_rehearsal
from .runtime import composition_engine_runtime_smoke
from .runtime import composition_engine_verify_owned_table_boundary


COMPOSITION_ENGINE_CONTROLS = (
    {
        "control_id": "release_readiness",
        "title": "Release readiness",
        "description": "Runs package-local release evidence, rehearsal, and smoke-plan coverage checks.",
        "permission": "composition_engine.audit",
    },
    {
        "control_id": "tenant_boundary",
        "title": "Tenant and boundary proof",
        "description": "Rejects foreign table references and proves package-owned event handling only.",
        "permission": "composition_engine.audit",
    },
    {
        "control_id": "assistant_guardrails",
        "title": "Assistant guardrails",
        "description": "Ensures assistant previews stay package-owned and mutation plans remain confirmation-gated.",
        "permission": "composition_engine.audit",
    },
    {
        "control_id": "publication_freeze",
        "title": "Publication freeze",
        "description": "Shows whether release rehearsal or security blockers should freeze publication.",
        "permission": "composition_engine.publish",
    },
)


def composition_engine_control_catalog() -> dict:
    """Return package-local operational controls."""
    return {
        "ok": bool(COMPOSITION_ENGINE_CONTROLS),
        "pbc": "composition_engine",
        "controls": COMPOSITION_ENGINE_CONTROLS,
        "control_ids": tuple(item["control_id"] for item in COMPOSITION_ENGINE_CONTROLS),
        "side_effects": (),
    }


def composition_engine_control_center(state: dict | None = None, *, workspace_id: str | None = None) -> dict:
    """Return executable control evidence for release and operator workflows."""
    source_state = state or composition_engine_runtime_smoke()["state"]
    target_workspace = workspace_id or next(iter(source_state.get("workspaces", {}) or ()), None)
    control_center = composition_engine_build_control_center(source_state, workspace_id=target_workspace)
    release = composition_engine_build_release_evidence()
    rehearsal = (
        composition_engine_release_rehearsal(source_state, target_workspace)
        if target_workspace
        else {"ok": False, "reason": "missing_workspace"}
    )
    accepted_boundary = composition_engine_verify_owned_table_boundary(("composition_workspace", "package_registration_projection"))
    rejected_boundary = composition_engine_verify_owned_table_boundary(("foreign_registration_table",))
    assistant_preview = composition_engine_assistant_document_preview(
        "Create a governed preview for composition rules only.",
        "Update the route budget rule but do not publish.",
        action="update",
        target_table="composition_engine_composition_rule",
    )
    return {
        "ok": control_center["ok"]
        and release["ok"]
        and accepted_boundary["ok"]
        and not rejected_boundary["ok"]
        and assistant_preview["ok"],
        "pbc": "composition_engine",
        "controls": composition_engine_control_catalog()["controls"],
        "control_center": control_center,
        "release": release,
        "rehearsal": rehearsal,
        "accepted_boundary": accepted_boundary,
        "rejected_boundary": rejected_boundary,
        "assistant_preview": assistant_preview,
        "side_effects": (),
    }


def composition_engine_mutation_preview(action: str, table: str, payload: dict | None = None) -> dict:
    """Preview whether a mutation would stay inside the composition-owned boundary."""
    preview = composition_engine_assistant_document_preview(
        "Operator requested a bounded datastore preview.",
        f"{action} {table}",
        action=action,
        target_table=table,
        payload=payload,
    )
    return {
        "ok": preview["ok"],
        "pbc": "composition_engine",
        "action": preview["crud_plan"]["action"],
        "table": preview["crud_plan"]["table"],
        "requires_confirmation": preview["crud_plan"]["requires_confirmation"],
        "boundary": preview["crud_plan"]["boundary"],
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise the control center with runtime smoke evidence."""
    state = composition_engine_empty_state() | composition_engine_runtime_smoke()["state"]
    preview = composition_engine_mutation_preview("read", "composition_engine_composition_workspace", {})
    center = composition_engine_control_center(state)
    return {
        "ok": preview["ok"] and center["ok"],
        "preview": preview,
        "control_center": center,
        "side_effects": (),
    }
