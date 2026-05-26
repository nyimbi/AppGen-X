"""UI contract for the Enterprise PIM PBC."""

from __future__ import annotations

from .runtime import ENTERPRISE_PIM_OWNED_TABLES
from .runtime import ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC
from .runtime import enterprise_pim_permissions_contract


ENTERPRISE_PIM_UI_FRAGMENT_KEYS = (
    "EnterprisePimWorkbench",
    "TaxonomyGraphStudio",
    "AttributeDefinitionStudio",
    "AttributeInheritanceInspector",
    "LocalizationWorkbench",
    "ValidationWorkflowBoard",
    "DependencySchemaConsole",
    "PimEventOutbox",
    "PimDeadLetterQueue",
    "PimRuleStudio",
    "PimParameterConsole",
    "PimConfigurationPanel",
    "PimAuditEvidencePanel",
)


def enterprise_pim_ui_contract() -> dict:
    return {
        "format": "appgen.enterprise-pim-ui-contract.v1",
        "ok": True,
        "pbc": "enterprise_pim",
        "implementation_directory": "src/pyAppGen/pbcs/enterprise_pim",
        "fragments": ENTERPRISE_PIM_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/enterprise_pim",
            "/workbench/pbcs/enterprise_pim/taxonomies",
            "/workbench/pbcs/enterprise_pim/attributes",
            "/workbench/pbcs/enterprise_pim/localization",
            "/workbench/pbcs/enterprise_pim/workflows",
            "/workbench/pbcs/enterprise_pim/dependencies",
            "/workbench/pbcs/enterprise_pim/events",
            "/workbench/pbcs/enterprise_pim/rules",
            "/workbench/pbcs/enterprise_pim/parameters",
            "/workbench/pbcs/enterprise_pim/configuration",
            "/workbench/pbcs/enterprise_pim/audit",
        ),
        "panels": (
            {
                "key": "taxonomy_governance",
                "fragment": "TaxonomyGraphStudio",
                "binds_to": ("product_taxonomy",),
                "commands": ("create_taxonomy", "start_validation_workflow", "approve_validation_workflow"),
            },
            {
                "key": "attribute_governance",
                "fragment": "AttributeDefinitionStudio",
                "binds_to": ("product_attribute",),
                "commands": ("define_attribute", "register_rule", "set_parameter"),
            },
            {
                "key": "localization",
                "fragment": "LocalizationWorkbench",
                "binds_to": ("localized_content", "product_attribute"),
                "commands": ("upsert_localized_content", "start_validation_workflow"),
            },
            {
                "key": "integration_evidence",
                "fragment": "DependencySchemaConsole",
                "binds_to": ("inbox", "outbox", "dead_letter"),
                "commands": ("accept_dependency_schema", "receive_event", "run_control_tests"),
            },
        ),
        "action_permissions": enterprise_pim_permissions_contract()["action_permissions"],
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_locale", "allowed_locales"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "required_event_topic": ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "stream_engine_picker_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": (
                "minimum_completeness",
                "minimum_translation_quality",
                "validation_sla_hours",
                "max_inheritance_depth",
                "dead_letter_retry_limit",
                "workbench_limit",
            ),
        },
        "rule_editor": {
            "rule_types": ("taxonomy", "attribute", "localization", "validation", "dependency", "publication"),
            "required_fields": ("rule_id", "tenant", "scope", "status", "required_locales", "required_attributes"),
        },
        "event_surfaces": {
            "emits": ("TaxonomyClassified", "AttributeDefined", "ContentLocalized", "ValidationApproved", "PimMasterDataReady"),
            "consumes": ("MediaAssetApproved", "PricePromotionApproved", "TaxCalculated", "InventoryPositionUpdated"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
        },
        "binding_evidence": {
            "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
            "shared_table_access": False,
        },
    }


def enterprise_pim_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = enterprise_pim_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, permission in action_permissions.items() if permission in permissions)
    taxonomies = tuple(item for item in state["product_taxonomy"].values() if item["tenant"] == tenant)
    attributes = tuple(item for item in state["product_attribute"].values() if item["tenant"] == tenant)
    localized = tuple(item for item in state["localized_content"].values() if item["tenant"] == tenant)
    workflows = tuple(item for item in state["validation_workflow"].values() if item["tenant"] == tenant)
    cards = (
        {"key": "taxonomies", "value": len(taxonomies), "fragment": "TaxonomyGraphStudio"},
        {"key": "attributes", "value": len(attributes), "fragment": "AttributeDefinitionStudio"},
        {"key": "localized_content", "value": len(localized), "fragment": "LocalizationWorkbench"},
        {"key": "approved_workflows", "value": len(tuple(item for item in workflows if item["status"] == "approved")), "fragment": "ValidationWorkflowBoard"},
        {"key": "outbox", "value": len(state["outbox"]), "fragment": "PimEventOutbox"},
        {"key": "dead_letter", "value": len(state["dead_letter"]), "fragment": "PimDeadLetterQueue"},
    )
    return {
        "format": "appgen.enterprise-pim-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/enterprise_pim",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "dependency_schemas_bound": tuple(sorted(state["dependency_schemas"])),
        "event_outbox_count": len(state["outbox"]),
        "binding_evidence": {
            "owned_tables": ENTERPRISE_PIM_OWNED_TABLES,
            "outbox_table": "enterprise_pim_appgen_outbox_event",
            "inbox_table": "enterprise_pim_appgen_inbox_event",
            "dead_letter_table": "enterprise_pim_dead_letter_event",
        },
    }
