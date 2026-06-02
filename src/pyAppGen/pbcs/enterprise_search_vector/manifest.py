"""Package manifest for the Enterprise Search Vector PBC."""

from __future__ import annotations

from .runtime import ENTERPRISE_SEARCH_VECTOR_CONSUMED_EVENT_TYPES
from .runtime import ENTERPRISE_SEARCH_VECTOR_EMITTED_EVENT_TYPES
from .runtime import ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES
from .runtime import ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS
from .runtime import ENTERPRISE_SEARCH_VECTOR_STANDARD_FEATURE_KEYS
from .runtime import enterprise_search_vector_permissions_contract
from .runtime import enterprise_search_vector_runtime_capabilities
from .ui import ENTERPRISE_SEARCH_VECTOR_UI_FRAGMENT_KEYS


PBC_KEY = 'enterprise_search_vector'

API_ROUTES = (
    "POST /indexes",
    "POST /indexes/{id}/refresh",
    "POST /documents",
    "POST /embeddings",
    "POST /search",
    "POST /query-feedback",
    "POST /ranking-simulations",
    "POST /freshness-forecasts",
    "POST /quality-remediations",
    "POST /policy-screenings",
    "POST /relevance-controls",
    "POST /index-proofs",
    "POST /federated-source-views",
    "POST /query-intent-risks",
    "POST /retention-deletions",
    "POST /governed-models",
    "POST /enterprise-search-vector/events/inbox",
    "GET /query-traces",
    "GET /enterprise-search-vector-workbench",
    "GET /enterprise-search-vector/schema-contract",
    "GET /enterprise-search-vector/service-contract",
    "GET /enterprise-search-vector/release-evidence",
)

PBC_MANIFEST = {
    "pbc": "enterprise_search_vector",
    "label": "Enterprise Search and Vector Discovery",
    "mesh": "intelligence",
    "description": (
        "Semantic and hybrid enterprise search across governed product, customer, "
        "audit, and knowledge projections with source indexing, document chunking, "
        "embeddings, ACL-filtered retrieval, feedback, query traces, freshness, "
        "rules, parameters, configuration, and AppGen-X event orchestration."
    ),
    "datastore_backend": "postgresql",
    "tables": ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
    "apis": API_ROUTES,
    "emits": ENTERPRISE_SEARCH_VECTOR_EMITTED_EVENT_TYPES,
    "consumes": ENTERPRISE_SEARCH_VECTOR_CONSUMED_EVENT_TYPES,
    "template": None,
    "ui_fragments": ENTERPRISE_SEARCH_VECTOR_UI_FRAGMENT_KEYS,
    "permissions": tuple(sorted(enterprise_search_vector_permissions_contract()["permissions"])),
    "configuration": (
        "ENTERPRISE_SEARCH_VECTOR_DATABASE_URL",
        "ENTERPRISE_SEARCH_VECTOR_EVENT_TOPIC",
        "ENTERPRISE_SEARCH_VECTOR_RETRY_LIMIT",
        "ENTERPRISE_SEARCH_VECTOR_DEFAULT_LOCALE",
        "ENTERPRISE_SEARCH_VECTOR_EMBEDDING_DIMENSIONS",
        "ENTERPRISE_SEARCH_VECTOR_RETENTION_DAYS",
        "ENTERPRISE_SEARCH_VECTOR_RANKING_MODE",
    ),
    "capabilities": tuple(f"enterprise_search_vector.{table}" for table in ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES),
    "standard_features": ENTERPRISE_SEARCH_VECTOR_STANDARD_FEATURE_KEYS,
    "workflows": enterprise_search_vector_runtime_capabilities()["operations"],
    "analytics": (
        "query_result_count",
        "relevance_confidence",
        "index_freshness",
        "acl_filter_rate",
        "embedding_job_latency",
        "feedback_score",
        "search_index_updated_throughput",
        "discovery_insight_generated_throughput",
    ),
    "advanced_capabilities": ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS,
    "migrations": ("migrations/001_initial.sql",),
    "seed_data": ("seed_data.py",),
    "tests": ("tests/test_contract.py",),
    "docs": (
        "README.md",
        "RELEASE_EVIDENCE.md",
        "SPECIFICATION.md",
        "implementation-plan.md",
        "implementation-status.md",
    ),
}
