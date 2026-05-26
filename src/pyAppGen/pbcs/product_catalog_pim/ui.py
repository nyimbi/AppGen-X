"""UI contract for the Enterprise Product Catalog and PIM PBC."""

from __future__ import annotations


PRODUCT_CATALOG_PIM_UI_FRAGMENT_KEYS = (
    "ProductCatalogWorkbench",
    "ProductMasterConsole",
    "ProductFamilyModeler",
    "VariantModeler",
    "AttributeSchemaStudio",
    "EnrichmentWorkbench",
    "LocalizationConsole",
    "MediaReferencePanel",
    "ComplianceClaimBoard",
    "PublicationConsole",
    "ChannelProjectionDashboard",
    "ProductRuleStudio",
    "ProductParameterConsole",
    "ProductConfigurationPanel",
)


def product_catalog_pim_ui_contract() -> dict:
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
            "/workbench/pbcs/product_catalog_pim/attributes",
            "/workbench/pbcs/product_catalog_pim/enrichment",
            "/workbench/pbcs/product_catalog_pim/localization",
            "/workbench/pbcs/product_catalog_pim/media",
            "/workbench/pbcs/product_catalog_pim/compliance",
            "/workbench/pbcs/product_catalog_pim/publication",
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
                "key": "enrichment",
                "fragment": "EnrichmentWorkbench",
                "binds_to": ("product_attribute", "product_locale_content", "product_media", "product_compliance_claim"),
                "commands": ("add_localized_content", "attach_product_media", "add_compliance_claim"),
            },
            {
                "key": "publication",
                "fragment": "PublicationConsole",
                "binds_to": ("catalog_publication", "catalog_channel_projection", "outbox"),
                "commands": ("add_price_metadata", "publish_product", "run_control_tests"),
            },
            {
                "key": "governance_studio",
                "fragment": "ProductRuleStudio",
                "binds_to": ("rule", "parameter", "configuration"),
                "commands": ("register_rule", "set_parameter", "configure_runtime", "run_control_tests"),
            },
        ),
        "action_permissions": {
            "create_product_family": "product_catalog_pim.product",
            "register_product": "product_catalog_pim.product",
            "define_attribute_schema": "product_catalog_pim.product",
            "set_product_attribute": "product_catalog_pim.enrich",
            "add_localized_content": "product_catalog_pim.enrich",
            "attach_product_media": "product_catalog_pim.enrich",
            "add_price_metadata": "product_catalog_pim.publish",
            "add_compliance_claim": "product_catalog_pim.enrich",
            "publish_product": "product_catalog_pim.publish",
            "register_rule": "product_catalog_pim.configure",
            "set_parameter": "product_catalog_pim.configure",
            "configure_runtime": "product_catalog_pim.configure",
            "run_control_tests": "product_catalog_pim.audit",
        },
        "configuration_editor": {
            "required_fields": ("database_backend", "event_topic", "retry_limit", "default_timezone"),
            "allowed_database_backends": ("postgresql", "mysql", "mariadb"),
            "event_contract": "AppGen-X",
        },
        "parameter_editor": {
            "numeric_parameters": (
                "minimum_completeness",
                "minimum_margin",
                "max_missing_required_attributes",
                "content_quality_threshold",
                "publication_batch_size",
                "retention_days",
            ),
        },
        "rule_editor": {
            "rule_types": ("sellability", "enrichment", "publication", "compliance", "channel", "taxonomy"),
            "required_fields": ("rule_id", "tenant", "rule_type", "allowed_channels", "allowed_locales", "status"),
        },
        "event_surfaces": {
            "emits": ("ProductClassified", "ProductEnriched", "ProductPublished", "ProductPriceReady", "ForecastUpdated"),
            "consumes": ("TaxCalculated", "MediaAssetApproved", "InventoryPositionUpdated", "PricePromotionApproved"),
            "outbox_status": "visible",
            "dead_letter_status": "visible",
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
    )
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
    }
