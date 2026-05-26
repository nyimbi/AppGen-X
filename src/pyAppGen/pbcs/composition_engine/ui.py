"""UI contract for the Composition Engine PBC."""

from __future__ import annotations


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
        "action_permissions": {
            "create_workspace": "composition_engine.compose",
            "select_pbc": "composition_engine.compose",
            "register_component": "composition_engine.compose",
            "register_ui_fragment": "composition_engine.compose",
            "bind_layout": "composition_engine.compose",
            "generate_composition_dsl": "composition_engine.publish",
            "publish_composition": "composition_engine.publish",
            "register_rule": "composition_engine.configure",
            "set_parameter": "composition_engine.configure",
            "configure_runtime": "composition_engine.configure",
            "run_control_tests": "composition_engine.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": ("max_fragments_per_page", "release_risk_threshold", "layout_density_target", "route_budget", "preview_batch_limit", "review_sla_hours"),
        },
        "rule_editor": {
            "rule_types": ("workspace", "layout", "route", "permission", "release_gate"),
            "required_fields": ("rule_id", "tenant", "scope", "required_fragments", "allowed_meshes", "route_policy", "severity", "status"),
        },
        "event_surfaces": {
            "emits": ("CompositionWorkspaceCreated", "PbcSelectedForComposition", "ComponentRegistered", "UiFragmentRegistered", "LayoutBound", "CompositionPublished", "PbcDeployed"),
            "consumes": ("SchemaAccepted", "RoutePublished", "AuditEventSealed", "AccessPolicyChanged", "WorkflowCompleted"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
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
    }
