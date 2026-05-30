"""Package-local guided wizards for the Composition Engine workbench."""

from __future__ import annotations

from .forms import composition_engine_form_catalog


COMPOSITION_ENGINE_WIZARDS = (
    {
        "wizard_id": "bootstrap_composition",
        "title": "Bootstrap composition workspace",
        "goal": "Move from workspace intake to a validated one-PBC composition draft.",
        "steps": (
            {"step_id": "workspace", "label": "Create workspace", "form_id": "workspace_intake", "operation": "create_workspace"},
            {"step_id": "select_pbc", "label": "Select capability", "form_id": "pbc_selection", "operation": "select_pbc"},
            {"step_id": "register_component", "label": "Register component and fragment", "form_id": "component_fragment_registration", "operation": "register_component"},
            {"step_id": "bind_layout", "label": "Bind layout", "form_id": "layout_binding", "operation": "bind_layout"},
            {"step_id": "validate", "label": "Run governance review", "form_id": "workspace_governance_review", "operation": "release_rehearsal"},
        ),
    },
    {
        "wizard_id": "document_driven_intake",
        "title": "Document-driven composition intake",
        "goal": "Turn a requirements document into a bounded composition preview and impact assessment.",
        "steps": (
            {"step_id": "capture_document", "label": "Capture document", "form_id": "assistant_document_intake", "operation": "assistant_document_preview"},
            {"step_id": "preview_impact", "label": "Preview selection impact", "form_id": "selection_impact_preview_request", "operation": "preview_selection_impact"},
            {"step_id": "review_routing", "label": "Review assistant routing", "form_id": "agent_intent_request", "operation": "route_agent_intent"},
        ),
    },
    {
        "wizard_id": "release_gate",
        "title": "Release gate",
        "goal": "Rehearse publication and inspect package-local evidence before publishing.",
        "steps": (
            {"step_id": "inspect_controls", "label": "Inspect controls", "form_id": "control_center_request", "operation": "build_control_center"},
            {"step_id": "rehearse_release", "label": "Run rehearsal", "form_id": "workspace_governance_review", "operation": "release_rehearsal"},
            {"step_id": "review_release_notes", "label": "Review notes", "form_id": "release_notes_request", "operation": "build_release_notes"},
        ),
    },
)


def composition_engine_wizard_catalog() -> dict:
    """Return the guided wizard registry for this PBC."""
    forms = composition_engine_form_catalog()
    form_ids = set(forms["form_ids"])
    missing_form_bindings = tuple(
        f"{wizard['wizard_id']}:{step['step_id']}"
        for wizard in COMPOSITION_ENGINE_WIZARDS
        for step in wizard["steps"]
        if step["form_id"] not in form_ids
    )
    return {
        "ok": bool(COMPOSITION_ENGINE_WIZARDS) and not missing_form_bindings,
        "pbc": "composition_engine",
        "wizards": COMPOSITION_ENGINE_WIZARDS,
        "wizard_ids": tuple(item["wizard_id"] for item in COMPOSITION_ENGINE_WIZARDS),
        "missing_form_bindings": missing_form_bindings,
        "side_effects": (),
    }


def composition_engine_plan_wizard(wizard_id: str, context: dict | None = None) -> dict:
    """Return a guided step plan with lightweight readiness hints."""
    wizard = next((item for item in COMPOSITION_ENGINE_WIZARDS if item["wizard_id"] == wizard_id), None)
    if wizard is None:
        return {"ok": False, "reason": "unknown_wizard", "wizard_id": wizard_id, "side_effects": ()}
    supplied = dict(context or {})
    planned_steps = []
    for position, step in enumerate(wizard["steps"], start=1):
        blocked_by = ()
        if wizard_id == "bootstrap_composition" and step["step_id"] != "workspace" and not supplied.get("workspace_id"):
            blocked_by = ("workspace_id",)
        if wizard_id == "document_driven_intake" and step["step_id"] == "preview_impact" and not supplied.get("workspace_id"):
            blocked_by = ("workspace_id",)
        if wizard_id == "document_driven_intake" and step["step_id"] in {"capture_document", "review_routing"} and not supplied.get("document_text"):
            blocked_by = ("document_text",)
        if wizard_id == "release_gate" and not supplied.get("workspace_id"):
            blocked_by = ("workspace_id",)
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
        "pbc": "composition_engine",
        "wizard_id": wizard_id,
        "goal": wizard["goal"],
        "steps": tuple(planned_steps),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise wizard catalog and plans for bootstrap and release gating."""
    catalog = composition_engine_wizard_catalog()
    bootstrap = composition_engine_plan_wizard(
        "bootstrap_composition",
        {"workspace_id": "ws_100"},
    )
    release_gate = composition_engine_plan_wizard(
        "release_gate",
        {"workspace_id": "ws_100"},
    )
    return {
        "ok": catalog["ok"] and bootstrap["ok"] and release_gate["ok"] and bool(bootstrap["steps"]) and bool(release_gate["steps"]),
        "catalog": catalog,
        "bootstrap": bootstrap,
        "release_gate": release_gate,
        "side_effects": (),
    }
