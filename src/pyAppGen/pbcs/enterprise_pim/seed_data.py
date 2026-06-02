"""Executable seed-data and bootstrap fixtures for the enterprise_pim PBC."""

from __future__ import annotations

from .runtime import ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC


PBC_KEY = "enterprise_pim"
DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": ENTERPRISE_PIM_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_locale": "en-US",
    "allowed_locales": ("en-US", "fr-FR"),
    "allowed_channels": ("commerce", "b2b"),
    "dependency_sources": ("dam_core", "pricing_core", "tax_core", "inventory_core"),
}
DEFAULT_PARAMETERS = {
    "minimum_completeness": 0.8,
    "minimum_translation_quality": 0.75,
    "validation_sla_hours": 24,
    "max_inheritance_depth": 4,
    "dead_letter_retry_limit": 3,
    "dependency_schema_version_floor": 1,
    "anomaly_zscore_threshold": 2.5,
    "workbench_limit": 50,
}
DEFAULT_RULES = (
    {
        "rule_id": "enterprise_pim.default_readiness",
        "tenant": "tenant_demo",
        "scope": "master_data_readiness",
        "status": "active",
        "required_locales": ("en-US",),
        "required_attributes": ("material",),
        "validation_policy": {"required_approvers": ("data_steward",)},
    },
)
DEFAULT_DEPENDENCY_SCHEMAS = (
    {
        "dependency": "dam_core",
        "contract": {
            "schema_version": 1,
            "events": ("MediaAssetApproved",),
            "fields": ("asset_ref", "asset_type", "approved_at"),
        },
    },
    {
        "dependency": "pricing_core",
        "contract": {
            "schema_version": 1,
            "events": ("PricePromotionApproved",),
            "fields": ("pricebook_id", "currency", "effective_at"),
        },
    },
)
DEMO_BOOTSTRAP_STEPS = (
    {
        "operation": "create_taxonomy",
        "payload": {
            "taxonomy_id": "tax_demo_pumps",
            "tenant": "tenant_demo",
            "code": "industrial/pumps",
            "name": "Industrial Pumps",
            "parent_id": None,
            "localized_names": {"en-US": "Industrial Pumps", "fr-FR": "Pompes industrielles"},
        },
    },
    {
        "operation": "define_attribute",
        "payload": {
            "attribute_id": "attr_demo_material",
            "tenant": "tenant_demo",
            "taxonomy_id": "tax_demo_pumps",
            "name": "material",
            "data_type": "string",
            "required": True,
            "localized_labels": {"en-US": "Material", "fr-FR": "Materiau"},
            "value": "steel",
        },
    },
    {
        "operation": "create_attribute_group",
        "payload": {
            "group_id": "grp_demo_core",
            "tenant": "tenant_demo",
            "taxonomy_id": "tax_demo_pumps",
            "name": "Core Specifications",
            "sequence": 1,
            "attributes": ("attr_demo_material",),
        },
    },
    {
        "operation": "register_attribute_value_option",
        "payload": {
            "option_id": "opt_demo_steel",
            "tenant": "tenant_demo",
            "attribute_id": "attr_demo_material",
            "value": "steel",
            "label": "Steel",
        },
    },
    {
        "operation": "register_attribute_validation_rule",
        "payload": {
            "validation_rule_id": "avr_demo_material",
            "tenant": "tenant_demo",
            "attribute_id": "attr_demo_material",
            "data_type": "string",
            "required": True,
            "pattern": "^(steel|alloy)$",
        },
    },
    {
        "operation": "upsert_localized_content",
        "payload": {
            "content_id": "content_demo_en",
            "tenant": "tenant_demo",
            "entity_id": "tax_demo_pumps",
            "entity_type": "product_taxonomy",
            "locale": "en-US",
            "title": "Industrial Pumps",
            "description": "Governed master data for industrial pump families with localization and readiness proof.",
            "overrides": {},
        },
    },
    {
        "operation": "upsert_translation_memory",
        "payload": {
            "translation_id": "tm_demo_fr",
            "tenant": "tenant_demo",
            "source_locale": "en-US",
            "target_locale": "fr-FR",
            "source_text": "Industrial Pumps",
            "target_text": "Pompes industrielles",
            "quality_score": 0.92,
        },
    },
    {
        "operation": "register_locale_fallback_rule",
        "payload": {
            "fallback_rule_id": "lfr_demo_fr",
            "tenant": "tenant_demo",
            "locale": "fr-FR",
            "fallback_locale": "en-US",
            "priority": 1,
        },
    },
    {
        "operation": "start_validation_workflow",
        "payload": {
            "workflow_id": "wf_demo_taxonomy",
            "tenant": "tenant_demo",
            "entity_id": "tax_demo_pumps",
            "entity_type": "product_taxonomy",
            "requested_by": "steward_demo",
        },
    },
    {
        "operation": "approve_validation_workflow",
        "payload": {
            "workflow_id": "wf_demo_taxonomy",
            "approver": "data_steward",
        },
    },
    {
        "operation": "receive_event",
        "payload": {
            "event": {
                "event_id": "evt_demo_media",
                "event_type": "MediaAssetApproved",
                "payload": {"asset_ref": "dam://pump-family-hero", "asset_type": "image"},
            },
        },
    },
    {
        "operation": "publish_master_data",
        "payload": {
            "taxonomy_id": "tax_demo_pumps",
            "channels": ("commerce",),
        },
    },
)
SEED_DATA = (
    {
        "table": "enterprise_pim_product_taxonomy",
        "rows": ({"code": "INDUSTRIAL-PUMPS", "status": "ready"},),
    },
    {
        "table": "enterprise_pim_product_attribute",
        "rows": ({"code": "MATERIAL", "status": "active"},),
    },
    {
        "table": "enterprise_pim_localized_content",
        "rows": ({"code": "PUMPS-EN-US", "status": "approved"},),
    },
    {
        "table": "enterprise_pim_validation_workflow",
        "rows": ({"code": "WF-TAXONOMY", "status": "approved"},),
    },
    {
        "table": "enterprise_pim_dependency_schema",
        "rows": ({"code": "DAM-CORE", "status": "accepted"},),
    },
)


def bootstrap_seed_bundle():
    """Return the default standalone bootstrap bundle without mutating state."""
    return {
        "configuration": dict(DEFAULT_CONFIGURATION),
        "parameters": dict(DEFAULT_PARAMETERS),
        "rules": tuple(dict(rule) for rule in DEFAULT_RULES),
        "dependency_schemas": tuple(
            {"dependency": item["dependency"], "contract": dict(item["contract"])}
            for item in DEFAULT_DEPENDENCY_SCHEMAS
        ),
        "steps": tuple({"operation": step["operation"], "payload": dict(step["payload"])} for step in DEMO_BOOTSTRAP_STEPS),
    }


def seed_plan():
    """Return deterministic seed rows and runtime bootstrap fixtures without applying them."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    bootstrap = bootstrap_seed_bundle()
    return {
        "ok": bool(SEED_DATA) and bool(bootstrap["steps"]),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": SEED_DATA,
        "bootstrap": bootstrap,
        "side_effects": (),
    }


def validate_seed_data():
    """Validate seed ownership, row shape, and bootstrap completeness."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code") or not row.get("status")
    )
    bootstrap = bootstrap_seed_bundle()
    missing_bootstrap = tuple(
        key
        for key in ("configuration", "parameters", "rules", "dependency_schemas", "steps")
        if not bootstrap.get(key)
    )
    invalid_configuration = tuple(
        key
        for key in ("database_backend", "event_topic", "retry_limit", "default_locale", "allowed_locales")
        if key not in bootstrap["configuration"]
    )
    plan = seed_plan()
    return {
        "ok": plan["ok"]
        and not invalid_tables
        and not invalid_rows
        and not missing_bootstrap
        and not invalid_configuration,
        "pbc": PBC_KEY,
        "plan": plan,
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "missing_bootstrap": missing_bootstrap,
        "invalid_configuration": invalid_configuration,
        "side_effects": (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    validation = validate_seed_data()
    return {
        "ok": validation["ok"],
        **validation,
    }
