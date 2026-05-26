"""UI contract for the Enterprise Product Catalog and PIM PBC."""

from __future__ import annotations

from .runtime import PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS
from .runtime import PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES
from .runtime import PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES
from .runtime import PRODUCT_CATALOG_PIM_OWNED_TABLES
from .runtime import PRODUCT_CATALOG_PIM_REQUIRED_CONFIGURATION_FIELDS
from .runtime import PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC
from .runtime import PRODUCT_CATALOG_PIM_REQUIRED_RULE_FIELDS
from .runtime import PRODUCT_CATALOG_PIM_RUNTIME_TABLES
from .runtime import PRODUCT_CATALOG_PIM_SUPPORTED_PARAMETER_NAMES
from .runtime import product_catalog_pim_binding_evidence
from .runtime import product_catalog_pim_permissions_contract


PRODUCT_CATALOG_PIM_UI_FRAGMENT_KEYS = (
    "ProductCatalogWorkbench",
    "ProductMasterConsole",
    "ProductFamilyModeler",
    "VariantModeler",
    "TaxonomyAssignmentStudio",
    "CategoryHierarchyBoard",
    "AttributeSchemaStudio",
    "EnrichmentWorkbench",
    "LocalizationConsole",
    "MediaReferencePanel",
    "ComplianceClaimBoard",
    "LifecycleApprovalBoard",
    "AssortmentPlanner",
    "PublicationConsole",
    "ChannelSyndicationConsole",
    "DataQualityBoard",
    "SemanticCatalogConsole",
    "AnalyticsReadinessPanel",
    "GovernedModelPanel",
    "ChannelProjectionDashboard",
    "ProductRuleStudio",
    "ProductParameterConsole",
    "ProductConfigurationPanel",
    "InboxOutboxMonitor",
    "DeadLetterTriage",
)


def product_catalog_pim_ui_contract() -> dict:
    permissions = product_catalog_pim_permissions_contract()["action_permissions"]
    return {
        "format": "appgen.product-catalog-pim-ui-contract.v1",
        "ok": True,
        "pbc": "product_catalog_pim",
        "implementation_directory": "src/pyAppGen/pbcs/product_catalog_pim",
        "fragments": PRODUCT_CATALOG_PIM_UI_FRAGMENT_KEYS,
        "routes": (
            "/workbench/pbcs/product_catalog_pim",
            "/workbench/pbcs/product_catalog_pim/products",
            "/workbench/pbcs/product_catalog_pim/families",
            "/workbench/pbcs/product_catalog_pim/variants",
            "/workbench/pbcs/product_catalog_pim/taxonomy",
            "/workbench/pbcs/product_catalog_pim/categories",
            "/workbench/pbcs/product_catalog_pim/attributes",
            "/workbench/pbcs/product_catalog_pim/enrichment",
            "/workbench/pbcs/product_catalog_pim/localization",
            "/workbench/pbcs/product_catalog_pim/media",
            "/workbench/pbcs/product_catalog_pim/compliance",
            "/workbench/pbcs/product_catalog_pim/lifecycle",
            "/workbench/pbcs/product_catalog_pim/assortments",
            "/workbench/pbcs/product_catalog_pim/publication",
            "/workbench/pbcs/product_catalog_pim/syndication",
            "/workbench/pbcs/product_catalog_pim/data-quality",
            "/workbench/pbcs/product_catalog_pim/analytics",
            "/workbench/pbcs/product_catalog_pim/channels",
            "/workbench/pbcs/product_catalog_pim/rules",
            "/workbench/pbcs/product_catalog_pim/parameters",
            "/workbench/pbcs/product_catalog_pim/configuration",
        ),
        "panels": (
            {
                "key": "product_model",
                "fragment": "ProductMasterConsole",
                "binds_to": ("product", "product_family", "product_variant", "product_attribute_schema"),
                "commands": ("create_product_family", "register_product", "define_attribute_schema", "set_product_attribute"),
            },
            {
                "key": "classification",
                "fragment": "TaxonomyAssignmentStudio",
                "binds_to": ("product_taxonomy", "taxonomy_node", "product_category", "category_assignment"),
                "commands": ("register_product", "define_attribute_schema", "build_workbench_view"),
            },
            {
                "key": "enrichment",
                "fragment": "EnrichmentWorkbench",
                "binds_to": ("product_attribute", "product_locale_content", "product_media", "product_compliance_claim", "product_enrichment_task"),
                "commands": ("add_localized_content", "attach_product_media", "add_compliance_claim"),
            },
            {
                "key": "lifecycle_and_approvals",
                "fragment": "LifecycleApprovalBoard",
                "binds_to": ("product_lifecycle_stage", "product_approval_workflow", "product_approval_decision"),
                "commands": ("publish_product", "run_control_tests", "build_release_evidence"),
            },
            {
                "key": "publication",
                "fragment": "PublicationConsole",
                "binds_to": ("catalog_publication", "catalog_channel_projection", "catalog_syndication_feed", "catalog_syndication_delivery", "outbox", "inbox", "dead_letter"),
                "commands": ("add_price_metadata", "publish_product", "receive_event", "run_control_tests"),
            },
            {
                "key": "governance_studio",
                "fragment": "ProductRuleStudio",
                "binds_to": ("product_rule", "product_parameter", "product_configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "build_schema_contract", "build_service_contract", "build_release_evidence"),
            },
        ),
        "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES,
        "runtime_tables": {
            "outbox": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
            "inbox": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1],
            "dead_letter": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2],
        },
        "action_permissions": permissions,
        "configuration_editor": {
            "required_fields": PRODUCT_CATALOG_PIM_REQUIRED_CONFIGURATION_FIELDS,
            "allowed_database_backends": PRODUCT_CATALOG_PIM_ALLOWED_DATABASE_BACKENDS,
            "event_contract": "AppGen-X",
            "event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
            "stream_engine_picker_visible": False,
            "user_eventing_choice_visible": False,
        },
        "parameter_editor": {
            "numeric_parameters": PRODUCT_CATALOG_PIM_SUPPORTED_PARAMETER_NAMES,
        },
        "rule_editor": {
            "rule_types": ("sellability", "enrichment", "publication", "compliance", "channel", "taxonomy"),
            "required_fields": PRODUCT_CATALOG_PIM_REQUIRED_RULE_FIELDS,
        },
        "event_surfaces": {
            "emits": PRODUCT_CATALOG_PIM_EMITTED_EVENT_TYPES,
            "consumes": PRODUCT_CATALOG_PIM_CONSUMED_EVENT_TYPES,
            "outbox_status": "visible",
            "inbox_status": "visible",
            "dead_letter_status": "visible",
            "stream_engine_picker_visible": False,
        },
        "binding_evidence": {
            "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES,
            "runtime_tables": PRODUCT_CATALOG_PIM_RUNTIME_TABLES,
            "outbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
            "inbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1],
            "dead_letter_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2],
            "required_event_topic": PRODUCT_CATALOG_PIM_REQUIRED_EVENT_TOPIC,
            "event_contract": "AppGen-X",
            "shared_table_access": False,
            "workbench_route": "/workbench/pbcs/product_catalog_pim",
            "rule_fragment": "ProductRuleStudio",
            "parameter_fragment": "ProductParameterConsole",
            "configuration_fragment": "ProductConfigurationPanel",
        },
    }


def product_catalog_pim_render_workbench(
    state: dict,
    *,
    tenant: str,
    principal_permissions: tuple[str, ...],
) -> dict:
    contract = product_catalog_pim_ui_contract()
    permissions = set(principal_permissions)
    action_permissions = contract["action_permissions"]
    visible_actions = tuple(action for action, required_permission in action_permissions.items() if required_permission in permissions)
    products = tuple(product for product in state["products"].values() if product["tenant"] == tenant)
    families = tuple(family for family in state["families"].values() if family["tenant"] == tenant)
    publications = tuple(publication for publication in state["publications"].values() if publication["tenant"] == tenant)
    media = tuple(item for item in state["media"].values() if item["tenant"] == tenant)
    cards = (
        {"key": "products", "value": len(products), "fragment": "ProductMasterConsole"},
        {"key": "families", "value": len(families), "fragment": "ProductFamilyModeler"},
        {"key": "published_products", "value": len(tuple(product for product in products if product["lifecycle_state"] == "published")), "fragment": "PublicationConsole"},
        {"key": "publications", "value": len(publications), "fragment": "ChannelProjectionDashboard"},
        {"key": "media", "value": len(media), "fragment": "MediaReferencePanel"},
        {"key": "outbox", "value": len(state["outbox"]), "fragment": "PublicationConsole"},
        {"key": "inbox", "value": len(state.get("inbox", ())), "fragment": "PublicationConsole"},
        {"key": "dead_letter", "value": len(state.get("dead_letter", ())), "fragment": "PublicationConsole"},
    )
    binding_evidence = product_catalog_pim_binding_evidence(state)
    return {
        "format": "appgen.product-catalog-pim-workbench-render.v1",
        "ok": True,
        "tenant": tenant,
        "route": "/workbench/pbcs/product_catalog_pim",
        "fragments": contract["fragments"],
        "cards": cards,
        "visible_actions": visible_actions,
        "locked_actions": tuple(action for action in action_permissions if action not in visible_actions),
        "configuration_bound": bool(state["configuration"].get("ok")),
        "rules_bound": tuple(sorted(state["rules"])),
        "parameters_bound": tuple(sorted(state["parameters"])),
        "event_outbox_count": len(state["outbox"]),
        "event_inbox_count": len(state.get("inbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "owned_tables": PRODUCT_CATALOG_PIM_OWNED_TABLES,
        "binding_evidence": {
            **binding_evidence,
            "ui_bindings": {
                "configuration_fragment": "ProductConfigurationPanel",
                "rule_fragment": "ProductRuleStudio",
                "parameter_fragment": "ProductParameterConsole",
                "publication_fragment": "PublicationConsole",
                "assortment_fragment": "AssortmentPlanner",
                "quality_fragment": "DataQualityBoard",
                "outbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[0],
                "inbox_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[1],
                "dead_letter_table": PRODUCT_CATALOG_PIM_RUNTIME_TABLES[2],
                "rbac": contract["action_permissions"],
            },
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
    contract = product_catalog_pim_ui_contract()
    permissions = tuple(dict.fromkeys(contract.get("action_permissions", {}).values()))
    rendered = product_catalog_pim_render_workbench(
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
