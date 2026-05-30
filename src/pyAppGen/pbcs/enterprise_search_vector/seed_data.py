"""Executable seed-data contract for the enterprise_search_vector PBC."""

from __future__ import annotations

import copy

from .runtime import ENTERPRISE_SEARCH_VECTOR_REQUIRED_EVENT_TOPIC


PBC_KEY = "enterprise_search_vector"

DEFAULT_CONFIGURATION = {
    "database_backend": "postgresql",
    "event_topic": ENTERPRISE_SEARCH_VECTOR_REQUIRED_EVENT_TOPIC,
    "retry_limit": 3,
    "default_locale": "en-US",
    "supported_locales": ("en-US", "fr-FR"),
    "supported_sources": ("product", "customer", "audit", "knowledge"),
    "embedding_dimensions": 8,
    "retention_days": 365,
    "ranking_mode": "hybrid",
    "workbench_limit": 50,
}

DEFAULT_PARAMETERS = {
    "semantic_weight": 0.45,
    "keyword_weight": 0.25,
    "freshness_weight": 0.1,
    "authority_weight": 0.1,
    "feedback_weight": 0.1,
    "relevance_threshold": 0.1,
    "chunk_size_tokens": 256,
    "embedding_batch_limit": 5000,
    "max_results": 10,
    "workbench_limit": 50,
}

DEFAULT_RULES = (
    {
        "rule_id": "enterprise_search_vector.default_tenant_policy",
        "tenant": "tenant_alpha",
        "scope": "enterprise_search_vector",
        "status": "active",
        "allowed_sources": ("product", "customer", "audit", "knowledge"),
        "allowed_locales": ("en-US", "fr-FR"),
        "acl_policy": {"require_acl_match": True, "default_acl": ("search.read",)},
        "ranking_policy": {"mode": "hybrid", "minimum_relevance": 0.1},
        "retention_policy": {"retention_days": 365, "legal_hold_supported": True},
    },
)

DEFAULT_INDEXES = (
    {
        "index_id": "idx_product",
        "tenant": "tenant_alpha",
        "name": "Product Discovery",
        "source": "product",
        "locale": "en-US",
        "status": "active",
    },
    {
        "index_id": "idx_customer",
        "tenant": "tenant_alpha",
        "name": "Customer Signals",
        "source": "customer",
        "locale": "en-US",
        "status": "active",
    },
    {
        "index_id": "idx_audit",
        "tenant": "tenant_alpha",
        "name": "Audit Search",
        "source": "audit",
        "locale": "en-US",
        "status": "active",
    },
    {
        "index_id": "idx_knowledge",
        "tenant": "tenant_alpha",
        "name": "Knowledge Search",
        "source": "knowledge",
        "locale": "en-US",
        "status": "active",
    },
)

DEFAULT_DOCUMENT_COMMANDS = (
    {
        "document_id": "doc_product_alpha",
        "tenant": "tenant_alpha",
        "source": "product",
        "locale": "en-US",
        "title": "Alpha Camera",
        "body": "Mirrorless camera with optical stabilization and low-light autofocus.",
        "acl": ("search.read",),
    },
    {
        "document_id": "doc_customer_alpha",
        "tenant": "tenant_alpha",
        "source": "customer",
        "locale": "en-US",
        "title": "Customer Ada",
        "body": "Ada prefers premium optics and fast delivery for camera purchases.",
        "acl": ("search.read",),
    },
)

DEFAULT_GOVERNED_MODELS = (
    {
        "model_id": "embed_2026_05",
        "tenant": "tenant_alpha",
        "model_type": "embedding",
        "version": "2026.05",
        "status": "approved",
        "validation_dataset": "enterprise-search-golden-set",
        "risk_rating": "medium",
    },
)

SEED_DATA = (
    {
        "table": "enterprise_search_vector_search_index",
        "rows": (
            {"code": "ENTERPRISE_SEARCH_VECTOR-IDX-PRODUCT", "status": "active"},
            {"code": "ENTERPRISE_SEARCH_VECTOR-IDX-KNOWLEDGE", "status": "active"},
        ),
    },
    {
        "table": "enterprise_search_vector_search_governed_model",
        "rows": (
            {"code": "ENTERPRISE_SEARCH_VECTOR-MODEL-EMBED", "status": "approved"},
        ),
    },
)


def _copy(value):
    return copy.deepcopy(value)


def default_configuration() -> dict:
    """Return the standalone bootstrap configuration."""
    return _copy(DEFAULT_CONFIGURATION)


def default_parameter_values() -> dict:
    """Return bounded default parameters for standalone bootstrap."""
    return _copy(DEFAULT_PARAMETERS)


def default_rules() -> tuple[dict, ...]:
    """Return package-local governance rules for bootstrap."""
    return _copy(DEFAULT_RULES)


def default_indexes() -> tuple[dict, ...]:
    """Return initial indexes for standalone bootstrap."""
    return _copy(DEFAULT_INDEXES)


def default_document_commands() -> tuple[dict, ...]:
    """Return sample documents used by focused bootstrap and smoke tests."""
    return _copy(DEFAULT_DOCUMENT_COMMANDS)


def default_governed_models() -> tuple[dict, ...]:
    """Return governed model seed payloads for bootstrap."""
    return _copy(DEFAULT_GOVERNED_MODELS)


def seed_plan():
    """Return deterministic seed rows and standalone bootstrap bundles."""
    tables = tuple(dict.fromkeys(item["table"] for item in SEED_DATA))
    return {
        "ok": bool(SEED_DATA)
        and bool(DEFAULT_CONFIGURATION)
        and bool(DEFAULT_PARAMETERS)
        and bool(DEFAULT_RULES)
        and bool(DEFAULT_INDEXES),
        "pbc": PBC_KEY,
        "tables": tables,
        "rows": _copy(SEED_DATA),
        "standalone_bundle": {
            "configuration": default_configuration(),
            "parameters": default_parameter_values(),
            "rules": default_rules(),
            "indexes": default_indexes(),
            "documents": default_document_commands(),
            "governed_models": default_governed_models(),
        },
        "side_effects": (),
    }


def validate_seed_data():
    """Validate seed ownership, bootstrap completeness, and minimum row shape."""
    invalid_tables = tuple(
        item["table"] for item in SEED_DATA if not item.get("table", "").startswith(f"{PBC_KEY}_")
    )
    invalid_rows = tuple(
        row
        for item in SEED_DATA
        for row in item.get("rows", ())
        if not row.get("code") or not row.get("status")
    )
    bundle = seed_plan()["standalone_bundle"]
    bundle_gaps = tuple(
        name
        for name in ("configuration", "parameters", "rules", "indexes", "documents", "governed_models")
        if not bundle.get(name)
    )
    invalid_event_topic = bundle["configuration"]["event_topic"] != ENTERPRISE_SEARCH_VECTOR_REQUIRED_EVENT_TOPIC
    return {
        "ok": not invalid_tables and not invalid_rows and not bundle_gaps and not invalid_event_topic,
        "pbc": PBC_KEY,
        "plan": seed_plan(),
        "invalid_tables": invalid_tables,
        "invalid_rows": invalid_rows,
        "bundle_gaps": bundle_gaps,
        "invalid_event_topic": invalid_event_topic,
        "side_effects": (),
    }


def smoke_test():
    """Exercise seed validation without writing rows."""
    validation = validate_seed_data()
    bundle = validation["plan"]["standalone_bundle"]
    return {
        "ok": validation["ok"]
        and bundle["configuration"]["database_backend"] == "postgresql"
        and len(bundle["indexes"]) >= 4
        and len(bundle["documents"]) >= 1,
        "validation": validation,
        "side_effects": (),
    }
