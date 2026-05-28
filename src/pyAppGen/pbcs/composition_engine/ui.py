"""UI contract for the Composition Engine PBC."""

from __future__ import annotations

from .controls import composition_engine_control_catalog
from .forms import composition_engine_form_catalog
from .runtime import COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_EMITTED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_OWNED_TABLES
from .runtime import COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import COMPOSITION_ENGINE_RUNTIME_TABLES
from .runtime import composition_engine_permissions_contract
from .wizards import composition_engine_wizard_catalog


COMPOSITION_ENGINE_UI_FRAGMENT_KEYS = (
    "CompositionWorkbench",
    "WorkspaceSelector",
    "PbcSelector",
    "SelectionImpactPreview",
    "ComponentRegistry",
    "FragmentCatalog",
    "LayoutCanvas",
    "BindingInspector",
    "RouteMapView",
    "PublicationConsole",
    "ReleaseEvidenceBoard",
    "ReleaseRehearsalPanel",
    "CompositionRuleStudio",
    "CompositionParameterConsole",
    "CompositionConfigurationPanel",
    "AssistantPreviewWorkbench",
    "CompositionWizardLauncher",
    "CompositionControlCenter",
    "DocumentationMatrix",
    "SecurityReviewPanel",
)


def composition_engine_ui_contract() -> dict:
    """Return workbench metadata for the one-PBC composition/orchestration app."""
    forms = composition_engine_form_catalog()
    wizards = composition_engine_wizard_catalog()
    controls = composition_engine_control_catalog()
    action_permissions = composition_engine_permissions_contract()["action_permissions"]
    return {
        "format": "appgen.composition-engine-ui-contract.v1",
        "ok": forms["ok"] and wizards["ok"] and controls["ok"],
        "pbc": "composition_engine",
        "implementation_directory": "src/pyAppGen/pbcs/composition_engine",
        "fragments": COMPOSITION_ENGINE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/composition_engine",
            "/workbench/pbcs/composition_engine/workspaces",
            "/workbench/pbcs/composition_engine/selections",
            "/workbench/pbcs/composition_engine/components",
            "/workbench/pbcs/composition_engine/layouts",
            "/workbench/pbcs/composition_engine/rehearsal",
            "/workbench/pbcs/composition_engine/release-evidence",
            "/workbench/pbcs/composition_engine/rules",
            "/workbench/pbcs/composition_engine/parameters",
            "/workbench/pbcs/composition_engine/configuration",
            "/workbench/pbcs/composition_engine/assistant",
            "/workbench/pbcs/composition_engine/controls",
            "/workbench/pbcs/composition_engine/security",
        ),
        "panels": (
            {
                "key": "workspace",
                "fragment": "WorkspaceSelector",
                "binds_to": ("composition_workspace", "composition_plan"),
                "commands": ("create_workspace", "select_pbc", "preview_selection_impact"),
            },
            {
                "key": "registry",
                "fragment": "ComponentRegistry",
                "binds_to": ("component_registry", "ui_fragment"),
                "commands": ("register_component", "register_ui_fragment"),
            },
            {
                "key": "layout",
                "fragment": "LayoutCanvas",
                "binds_to": ("layout_binding", "dsl_artifact"),
                "commands": ("bind_layout", "generate_composition_dsl", "build_smoke_plan"),
            },
            {
                "key": "publication",
                "fragment": "ReleaseRehearsalPanel",
                "binds_to": ("release_evidence", "package_registration_plan", "package_index_entry"),
                "commands": ("release_rehearsal", "plan_package_registration", "publish_composition", "build_release_notes"),
            },
            {
                "key": "assistant",
                "fragment": "AssistantPreviewWorkbench",
                "binds_to": ("composition_workspace", "composition_rule", "composition_parameter", "composition_configuration"),
                "commands": ("assistant_document_preview", "route_agent_intent"),
            },
            {
                "key": "controls",
                "fragment": "CompositionControlCenter",
                "binds_to": ("release_evidence", "composition_validation_run", "composition_rule"),
                "commands": ("build_control_center", "build_security_review", "build_documentation_matrix"),
            },
        ),
        "action_permissions": action_permissions,
        "forms": forms["forms"],
        "wizards": wizards["wizards"],
        "controls": controls["controls"],
        "configuration_editor": {
            "required_fields": (
                "database_backend",
                "event_topic",
                "retry_limit",
                "allowed_targets",
                "allowed_layout_modes",
                "publication_mode",
                "default_timezone",
                "workbench_limit",
            ),
            "allowed_database_backends": COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS,
            "required_event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
            "user_selectable_event_contract": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "max_fragments_per_page",
                "release_risk_threshold",
                "layout_density_target",
                "route_budget",
                "preview_batch_limit",
                "review_sla_hours",
            ),
            "bounded_supported_parameters": True,
        },
        "rule_editor": {
            "rule_types": ("workspace", "selection", "layout", "release_gate"),
            "required_fields": (
                "rule_id",
                "tenant",
                "scope",
                "required_fragments",
                "allowed_meshes",
                "route_policy",
                "requires_approval",
                "severity",
                "status",
            ),
            "compiled_evidence_required": True,
        },
        "event_surfaces": {
            "emits": COMPOSITION_ENGINE_EMITTED_EVENT_TYPES,
            "consumes": COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
            "runtime_tables": COMPOSITION_ENGINE_RUNTIME_TABLES,
            "required_event_topic": COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "shared_table_access": False,
            "form_ids": forms["form_ids"],
            "wizard_ids": wizards["wizard_ids"],
            "control_ids": controls["control_ids"],
        },
    }


def composition_engine_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    """Render high-level workbench cards for the composition slice."""
    contract = composition_engine_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(
        action for action, required in contract["action_permissions"].items() if required in permissions
    )
    workspaces = tuple(item for item in state["workspaces"].values() if item["tenant"] == tenant)
    fragments = tuple(item for item in state["fragments"].values() if item["tenant"] == tenant)
    bindings = tuple(item for item in state["bindings"].values() if item["tenant"] == tenant)
    cards = (
        {"key": "workspaces", "value": len(workspaces), "fragment": "WorkspaceSelector"},
        {"key": "published", "value": len(tuple(item for item in workspaces if item["status"] == "published")), "fragment": "PublicationConsole"},
        {"key": "fragments", "value": len(fragments), "fragment": "FragmentCatalog"},
        {"key": "bindings", "value": len(bindings), "fragment": "LayoutCanvas"},
        {"key": "forms", "value": len(contract["forms"]), "fragment": "AssistantPreviewWorkbench"},
        {"key": "wizards", "value": len(contract["wizards"]), "fragment": "CompositionWizardLauncher"},
        {"key": "controls", "value": len(contract["controls"]), "fragment": "CompositionControlCenter"},
    )
    return {
        "format": "appgen.composition-engine-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/composition_engine",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in contract["action_permissions"] if action not in visible_actions),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rules_bound": tuple(sorted(rule_id for rule_id, rule in state.get("rules", {}).items() if rule["tenant"] == tenant)),
        "parameters_bound": tuple(sorted(state.get("parameters", {}))),
        "event_outbox_count": len(state.get("outbox", ())),
        "event_inbox_count": len(tuple(event for event in state.get("inbox", ()) if event.get("tenant") == tenant)),
        "dead_letter_count": len(tuple(event for event in state.get("dead_letter", ()) if event.get("tenant") == tenant)),
        "forms": contract["forms"],
        "wizards": contract["wizards"],
        "controls": contract["controls"],
        "binding_evidence": contract["binding_evidence"],
    }


class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState(
        {
            "configuration": _AppGenSmokeState({"ok": True}),
            "rules": _AppGenSmokeState(),
            "parameters": _AppGenSmokeState(),
            "workspaces": _AppGenSmokeState(),
            "fragments": _AppGenSmokeState(),
            "bindings": _AppGenSmokeState(),
            "outbox": (),
            "inbox": (),
            "dead_letter": (),
        }
    )


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = composition_engine_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = composition_engine_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("forms"))
        and bool(contract.get("wizards"))
        and bool(contract.get("controls"))
        and contract["configuration_editor"]["stream_engine_picker_visible"] is False
        and contract["binding_evidence"]["shared_table_access"] is False,
        "manifest": {"fragments": contract.get("fragments", ())},
        "contract": contract,
        "rendered": rendered,
        "side_effects": (),
    }
