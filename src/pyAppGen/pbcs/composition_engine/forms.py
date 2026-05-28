"""Package-local forms for the Composition Engine workbench."""

from __future__ import annotations


COMPOSITION_ENGINE_FORM_DEFINITIONS = (
    {
        "form_id": "workspace_intake",
        "title": "Create composition workspace",
        "route": "POST /api/pbc/composition_engine/composition-workspaces",
        "operation": "create_workspace",
        "permission": "composition_engine.compose",
        "owned_tables": ("composition_engine_composition_workspace",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "workspace_id", "type": "string", "required": True},
            {"name": "name", "type": "string", "required": True},
            {"name": "owner", "type": "string", "required": True},
            {"name": "target", "type": "enum", "required": True, "choices": ("web", "admin", "mobile")},
        ),
    },
    {
        "form_id": "pbc_selection",
        "title": "Select packaged capability",
        "route": "POST /api/pbc/composition_engine/composition-workspaces/{id}/pbcs",
        "operation": "select_pbc",
        "permission": "composition_engine.compose",
        "owned_tables": ("composition_engine_composition_workspace", "composition_engine_composition_plan"),
        "fields": (
            {"name": "workspace_id", "type": "string", "required": True},
            {"name": "pbc", "type": "string", "required": True},
            {"name": "mesh", "type": "enum", "required": True, "choices": ("platform", "commerce", "operations", "relationship", "finance")},
            {"name": "reason", "type": "text", "required": True},
        ),
    },
    {
        "form_id": "component_fragment_registration",
        "title": "Register component and fragment",
        "route": "POST /api/pbc/composition_engine/component-registry",
        "operation": "register_component",
        "permission": "composition_engine.compose",
        "owned_tables": ("composition_engine_component_registry", "composition_engine_ui_fragment"),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "component_id", "type": "string", "required": True},
            {"name": "pbc", "type": "string", "required": True},
            {"name": "fragment", "type": "string", "required": True},
            {"name": "permissions", "type": "list", "required": True},
            {"name": "schemas", "type": "list", "required": True},
        ),
    },
    {
        "form_id": "layout_binding",
        "title": "Bind layout fragment",
        "route": "POST /api/pbc/composition_engine/layout-bindings",
        "operation": "bind_layout",
        "permission": "composition_engine.compose",
        "owned_tables": ("composition_engine_layout_binding",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "binding_id", "type": "string", "required": True},
            {"name": "workspace_id", "type": "string", "required": True},
            {"name": "page", "type": "string", "required": True},
            {"name": "slot", "type": "enum", "required": True, "choices": ("hero", "main", "side", "footer")},
            {"name": "fragment_id", "type": "string", "required": True},
            {"name": "projection", "type": "string", "required": True},
        ),
    },
    {
        "form_id": "governance_rule",
        "title": "Register composition rule",
        "route": "POST /api/pbc/composition_engine/composition/rules",
        "operation": "register_rule",
        "permission": "composition_engine.configure",
        "owned_tables": ("composition_engine_composition_rule",),
        "fields": (
            {"name": "tenant", "type": "string", "required": True},
            {"name": "rule_id", "type": "string", "required": True},
            {"name": "scope", "type": "enum", "required": True, "choices": ("workspace", "selection", "layout", "release_gate")},
            {"name": "required_fragments", "type": "list", "required": True},
            {"name": "allowed_meshes", "type": "list", "required": True},
            {"name": "route_policy", "type": "string", "required": True},
            {"name": "requires_approval", "type": "boolean", "required": True},
            {"name": "severity", "type": "enum", "required": True, "choices": ("info", "warning", "blocking")},
            {"name": "status", "type": "enum", "required": True, "choices": ("draft", "active", "retired")},
        ),
    },
    {
        "form_id": "assistant_document_intake",
        "title": "Assistant document preview",
        "route": "POST /api/pbc/composition_engine/composition/assistant/document-preview",
        "operation": "assistant_document_preview",
        "permission": "composition_engine.read",
        "owned_tables": (
            "composition_engine_composition_workspace",
            "composition_engine_component_registry",
            "composition_engine_ui_fragment",
            "composition_engine_layout_binding",
            "composition_engine_composition_rule",
            "composition_engine_composition_parameter",
            "composition_engine_composition_configuration",
        ),
        "fields": (
            {"name": "document_text", "type": "text", "required": True},
            {"name": "instructions", "type": "text", "required": True},
            {
                "name": "target_table",
                "type": "enum",
                "required": False,
                "choices": (
                    "composition_engine_composition_workspace",
                    "composition_engine_component_registry",
                    "composition_engine_ui_fragment",
                    "composition_engine_layout_binding",
                    "composition_engine_composition_rule",
                    "composition_engine_composition_parameter",
                    "composition_engine_composition_configuration",
                ),
            },
            {"name": "requested_action", "type": "enum", "required": True, "choices": ("create", "read", "update", "delete")},
        ),
    },
)


def composition_engine_form_catalog() -> dict:
    """Return the package-local workbench form registry."""
    forms = tuple(COMPOSITION_ENGINE_FORM_DEFINITIONS)
    return {
        "ok": bool(forms),
        "pbc": "composition_engine",
        "forms": forms,
        "form_ids": tuple(item["form_id"] for item in forms),
        "side_effects": (),
    }


def composition_engine_get_form(form_id: str) -> dict:
    """Return one form definition by identifier."""
    form = next((item for item in COMPOSITION_ENGINE_FORM_DEFINITIONS if item["form_id"] == form_id), None)
    return {
        "ok": form is not None,
        "pbc": "composition_engine",
        "form": form,
        "side_effects": (),
    }


def composition_engine_validate_form_payload(form_id: str, payload: dict | None = None) -> dict:
    """Validate a form payload against required fields and enum choices."""
    form = composition_engine_get_form(form_id).get("form")
    if form is None:
        return {"ok": False, "accepted": False, "reason": "unknown_form", "form_id": form_id, "side_effects": ()}
    supplied = dict(payload or {})
    missing = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("required") and supplied.get(field["name"]) in {None, ""}
    )
    invalid_choices = tuple(
        field["name"]
        for field in form["fields"]
        if field.get("type") == "enum" and supplied.get(field["name"]) not in {None, *field.get("choices", ())}
    )
    return {
        "ok": not missing and not invalid_choices,
        "accepted": not missing and not invalid_choices,
        "pbc": "composition_engine",
        "form_id": form_id,
        "missing": missing,
        "invalid_choices": invalid_choices,
        "payload_keys": tuple(sorted(supplied)),
        "side_effects": (),
    }


def smoke_test() -> dict:
    """Exercise one happy-path form validation."""
    catalog = composition_engine_form_catalog()
    validation = composition_engine_validate_form_payload(
        "assistant_document_intake",
        {
            "document_text": "Compose a customer service workbench with customer_360 and workflow orchestration.",
            "instructions": "Create a preview-only plan and keep publication gated.",
            "requested_action": "create",
            "target_table": "composition_engine_composition_workspace",
        },
    )
    return {
        "ok": catalog["ok"] and validation["ok"],
        "catalog": catalog,
        "validation": validation,
        "side_effects": (),
    }
