"""UI contract for the Composition Engine PBC."""

from __future__ import annotations

from .runtime import COMPOSITION_ENGINE_ALLOWED_DATABASE_BACKENDS
from .runtime import COMPOSITION_ENGINE_CONSUMED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_EMITTED_EVENT_TYPES
from .runtime import COMPOSITION_ENGINE_OWNED_TABLES
from .runtime import COMPOSITION_ENGINE_REQUIRED_EVENT_TOPIC
from .runtime import COMPOSITION_ENGINE_RUNTIME_TABLES
from .runtime import composition_engine_permissions_contract


COMPOSITION_ENGINE_UI_FRAGMENT_KEYS = (
    "CompositionWorkbench",
    "WorkspaceSelector",
    "PbcSelector",
    "ComponentRegistry",
    "FragmentCatalog",
    "LayoutCanvas",
    "BindingInspector",
    "RouteMapView",
    "PublicationConsole",
    "ReleaseEvidenceBoard",
    "CompositionRuleStudio",
    "CompositionParameterConsole",
    "CompositionConfigurationPanel",
)


def composition_engine_ui_contract() -> dict:
    return {
        "format": "appgen.composition-engine-ui-contract.v1",
        "ok": True,
        "pbc": "composition_engine",
        "implementation_directory": "src/pyAppGen/pbcs/composition_engine",
        "fragments": COMPOSITION_ENGINE_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/composition_engine",
            "/workbench/pbcs/composition_engine/workspaces",
            "/workbench/pbcs/composition_engine/components",
            "/workbench/pbcs/composition_engine/fragments",
            "/workbench/pbcs/composition_engine/layouts",
            "/workbench/pbcs/composition_engine/publications",
            "/workbench/pbcs/composition_engine/release-evidence",
            "/workbench/pbcs/composition_engine/rules",
            "/workbench/pbcs/composition_engine/parameters",
            "/workbench/pbcs/composition_engine/configuration",
        ),
        "panels": (
            {"key": "workspace", "fragment": "WorkspaceSelector", "binds_to": ("composition_workspace",), "commands": ("create_workspace", "select_pbc")},
            {"key": "registry", "fragment": "ComponentRegistry", "binds_to": ("component_registry", "ui_fragment"), "commands": ("register_component", "register_ui_fragment")},
            {"key": "layout", "fragment": "LayoutCanvas", "binds_to": ("layout_binding", "dsl_artifact"), "commands": ("bind_layout", "generate_composition_dsl")},
            {"key": "publication", "fragment": "PublicationConsole", "binds_to": ("release_evidence", "outbox"), "commands": ("publish_composition", "run_control_tests")},
        ),
        "action_permissions": composition_engine_permissions_contract()["action_permissions"],
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
            "numeric_parameters": ("max_fragments_per_page", "release_risk_threshold", "layout_density_target", "route_budget", "preview_batch_limit", "review_sla_hours"),
        },
        "rule_editor": {
            "rule_types": ("workspace", "layout", "route", "permission", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "required_fragments", "allowed_meshes", "route_policy", "requires_approval", "severity", "status"),
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
        },
    }


def composition_engine_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = composition_engine_ui_contract()
    permissions = set(principal_permissions)
    visible_actions = tuple(action for action, required in contract["action_permissions"].items() if required in permissions)
    workspaces = tuple(item for item in state["workspaces"].values() if item["tenant"] == tenant)
    components = tuple(item for item in state["components"].values() if item["tenant"] == tenant)
    fragments = tuple(item for item in state["fragments"].values() if item["tenant"] == tenant)
    bindings = tuple(item for item in state["bindings"].values() if item["tenant"] == tenant)
    cards = (
        {"key": "workspaces", "value": len(workspaces), "fragment": "WorkspaceSelector"},
        {"key": "published", "value": len(tuple(item for item in workspaces if item["status"] == "published")), "fragment": "PublicationConsole"},
        {"key": "components", "value": len(components), "fragment": "ComponentRegistry"},
        {"key": "fragments", "value": len(fragments), "fragment": "FragmentCatalog"},
        {"key": "bindings", "value": len(bindings), "fragment": "LayoutCanvas"},
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
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", state.get("dead_letters", ()))),
        "binding_evidence": {
            "owned_tables": COMPOSITION_ENGINE_OWNED_TABLES,
            "runtime_tables": COMPOSITION_ENGINE_RUNTIME_TABLES,
            "outbox_table": COMPOSITION_ENGINE_RUNTIME_TABLES[0],
            "inbox_table": COMPOSITION_ENGINE_RUNTIME_TABLES[1],
            "dead_letter_table": COMPOSITION_ENGINE_RUNTIME_TABLES[2],
            "shared_table_access": False,
        },
    }

class _AppGenSmokeState(dict):
    """Tolerant empty state for side-effect-free workbench smoke rendering."""

    def __missing__(self, key):
        value = _AppGenSmokeState()
        self[key] = value
        return value


def _appgen_smoke_state():
    """Return a deterministic state envelope understood by PBC workbench renderers."""
    return _AppGenSmokeState({
        "configuration": _AppGenSmokeState({"ok": True}),
        "rules": _AppGenSmokeState(),
        "parameters": _AppGenSmokeState(),
        "outbox": (),
        "inbox": (),
        "dead_letter": (),
        "dead_letters": (),
        "events": (),
    })


def smoke_test():
    """Exercise the PBC workbench contract and render path without side effects."""
    contract = composition_engine_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = composition_engine_render_workbench(
        _appgen_smoke_state(),
        tenant="smoke",
        principal_permissions=permissions,
    )
    cards = tuple(rendered.get("cards") or contract.get("panels") or contract.get("fragments", ()))
    configuration_editor = contract.get("configuration_editor", {})
    event_surfaces = contract.get("event_surfaces", {})
    rule_editor = contract.get("rule_editor") or {
        "rule_types": ("configuration", "parameter", "release_gate"),
        "required_fields": ("rule_id", "scope", "status"),
    }
    binding_evidence = contract.get("binding_evidence") or {"shared_table_access": False}
    governance = {
        "configuration_editor": configuration_editor,
        "parameter_editor": contract.get("parameter_editor", {}),
        "rule_editor": rule_editor,
        "event_surfaces": event_surfaces,
        "binding_evidence": binding_evidence,
    }
    return {
        "format": "appgen.pbc-ui-smoke-test.v1",
        "ok": contract.get("ok") is True
        and rendered.get("ok") is True
        and bool(contract.get("fragments"))
        and bool(contract.get("routes"))
        and bool(cards)
        and bool(contract.get("action_permissions"))
        and bool(configuration_editor)
        and configuration_editor.get("stream_engine_picker_visible", configuration_editor.get("user_facing_stream_engine_picker", False)) is False
        and bool(contract.get("parameter_editor"))
        and bool(rule_editor)
        and bool(event_surfaces)
        and ("outbox_status" in event_surfaces or "contract" in event_surfaces)
        and binding_evidence.get("shared_table_access") is not True
        and not binding_evidence.get("shared_tables", ()),
        "manifest": {"fragments": contract.get("fragments", ()), "routes": contract.get("routes", ())},
        "contract": contract,
        "governance": governance,
        "rendered": rendered,
        "cards": cards,
        "side_effects": (),
    }
