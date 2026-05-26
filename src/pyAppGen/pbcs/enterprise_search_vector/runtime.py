"""Executable runtime for the Enterprise Search Vector PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math


ENTERPRISE_SEARCH_VECTOR_REQUIRED_EVENT_TOPIC = "appgen.enterprise_search_vector.events"
ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES = ("search_index", "embedding_job", "vector_document", "query_trace")

ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS = (
    "event_sourced_search_index_lifecycle",
    "owned_search_schema_boundary",
    "multi_tenant_search_isolation",
    "schema_evolution_resilient_document_context",
    "source_index_management",
    "document_chunk_and_acl_ingestion",
    "embedding_job_orchestration",
    "semantic_and_hybrid_query",
    "ranking_and_relevance_feedback",
    "retention_and_deletion_evidence",
    "access_control_filtered_retrieval",
    "probabilistic_relevance_confidence",
    "counterfactual_ranking_simulation",
    "temporal_index_freshness_forecasting",
    "autonomous_search_quality_remediation",
    "semantic_document_understanding",
    "predictive_query_intent_risk",
    "self_healing_index_refresh",
    "cryptographic_index_proof",
    "immutable_query_audit_trail",
    "dynamic_search_policy_screening",
    "automated_relevance_control_testing",
    "cross_system_product_customer_audit_federation",
    "appgen_x_outbox_inbox_eventing",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions_governance_evidence",
    "configuration_schema",
    "parameter_engine",
    "rule_engine",
    "seed_data",
    "workbench_ui",
    "governed_model_evidence",
)

ENTERPRISE_SEARCH_VECTOR_STANDARD_FEATURE_KEYS = (
    "search_indexes",
    "source_registration",
    "document_ingestion",
    "document_chunking",
    "embedding_jobs",
    "semantic_search",
    "hybrid_search",
    "ranking",
    "acl_filtering",
    "query_traces",
    "feedback_capture",
    "query_observability",
    "index_freshness",
    "authority_scoring",
    "retention_policy",
    "product_projection",
    "customer_projection",
    "audit_projection",
    "tenant_isolation",
    "appgen_x_outbox",
    "appgen_x_inbox",
    "idempotent_handlers",
    "retry_dead_letter_evidence",
    "permissions",
    "configuration_schema",
    "rule_engine",
    "parameter_engine",
    "seed_data",
    "workbench",
)

ENTERPRISE_SEARCH_VECTOR_SUPPORTED_CONFIGURATION_FIELDS = (
    "database_backend",
    "event_topic",
    "retry_limit",
    "default_locale",
    "supported_locales",
    "supported_sources",
    "embedding_dimensions",
    "retention_days",
    "ranking_mode",
    "workbench_limit",
)

ENTERPRISE_SEARCH_VECTOR_SUPPORTED_PARAMETER_KEYS = (
    "semantic_weight",
    "keyword_weight",
    "freshness_weight",
    "authority_weight",
    "feedback_weight",
    "relevance_threshold",
    "chunk_size_tokens",
    "embedding_batch_limit",
    "max_results",
    "workbench_limit",
)

ENTERPRISE_SEARCH_VECTOR_REQUIRED_RULE_FIELDS = (
    "rule_id",
    "tenant",
    "scope",
    "status",
    "allowed_sources",
    "allowed_locales",
    "acl_policy",
    "ranking_policy",
    "retention_policy",
)

ENTERPRISE_SEARCH_VECTOR_CONSUMED_EVENT_TYPES = ("ProductPublished", "CustomerUpdated", "AuditEventSealed")
ENTERPRISE_SEARCH_VECTOR_EMITTED_EVENT_TYPES = ("SearchIndexUpdated", "DiscoveryInsightGenerated")

_CONFIG_SEQUENCE_FIELDS = {"supported_locales", "supported_sources"}
_RULE_SEQUENCE_FIELDS = {"allowed_sources", "allowed_locales"}
_SOURCE_AUTHORITIES = {
    "product": 0.95,
    "knowledge": 0.9,
    "customer": 0.8,
    "audit": 0.7,
}
_PARAMETER_BOUNDS = {
    "semantic_weight": (0.0, 1.0),
    "keyword_weight": (0.0, 1.0),
    "freshness_weight": (0.0, 1.0),
    "authority_weight": (0.0, 1.0),
    "feedback_weight": (0.0, 1.0),
    "relevance_threshold": (0.0, 1.0),
    "chunk_size_tokens": (64, 8192),
    "embedding_batch_limit": (1, 100000),
    "max_results": (1, 1000),
    "workbench_limit": (1, 1000),
}


def enterprise_search_vector_runtime_capabilities() -> dict:
    smoke = enterprise_search_vector_runtime_smoke()
    return {
        "format": "appgen.enterprise-search-vector-runtime-capabilities.v1",
        "ok": smoke["ok"],
        "pbc": "enterprise_search_vector",
        "implementation_directory": "src/pyAppGen/pbcs/enterprise_search_vector",
        "owned_tables": ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
        "capabilities": ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS,
        "standard_features": ENTERPRISE_SEARCH_VECTOR_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "create_index",
            "ingest_document",
            "run_embedding_job",
            "refresh_index",
            "query",
            "record_feedback",
            "receive_event",
            "build_workbench_view",
        ),
        "smoke": smoke,
    }


def enterprise_search_vector_runtime_smoke() -> dict:
    state = enterprise_search_vector_empty_state()
    state = enterprise_search_vector_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": ENTERPRISE_SEARCH_VECTOR_REQUIRED_EVENT_TOPIC,
            "retry_limit": 3,
            "default_locale": "en-US",
            "supported_locales": ("en-US", "fr-FR"),
            "supported_sources": ("product", "customer", "audit", "knowledge"),
            "embedding_dimensions": 8,
            "retention_days": 365,
            "ranking_mode": "hybrid",
            "workbench_limit": 100,
        },
    )["state"]
    for name, value in (
        ("semantic_weight", 0.45),
        ("keyword_weight", 0.3),
        ("freshness_weight", 0.1),
        ("authority_weight", 0.1),
        ("feedback_weight", 0.05),
        ("relevance_threshold", 0.1),
        ("chunk_size_tokens", 512),
        ("embedding_batch_limit", 5000),
        ("max_results", 10),
        ("workbench_limit", 100),
    ):
        state = enterprise_search_vector_set_parameter(state, name, value)["state"]
    state = enterprise_search_vector_register_rule(
        state,
        {
            "rule_id": "rule_search_default",
            "tenant": "tenant_alpha",
            "scope": "enterprise_search_vector",
            "status": "active",
            "allowed_sources": ("product", "customer", "audit", "knowledge"),
            "allowed_locales": ("en-US",),
            "acl_policy": {"require_acl_match": True, "default_acl": ("search.read",)},
            "ranking_policy": {"hybrid": True, "minimum_relevance": 0.1},
            "retention_policy": {"retention_days": 365, "legal_hold_supported": True},
        },
    )["state"]
    state = enterprise_search_vector_register_schema_extension(
        state,
        "vector_document",
        {"explainability": "jsonb"},
    )["state"]
    for command in (
        {
            "index_id": "idx_product",
            "tenant": "tenant_alpha",
            "name": "Product Search",
            "source": "product",
            "locale": "en-US",
            "status": "active",
        },
        {
            "index_id": "idx_customer",
            "tenant": "tenant_alpha",
            "name": "Customer Search",
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
    ):
        state = enterprise_search_vector_create_index(state, command)["state"]
    for event in (
        {
            "event_id": "prod_alpha",
            "event_type": "ProductPublished",
            "payload": {
                "tenant": "tenant_alpha",
                "document_id": "doc_product_alpha",
                "title": "Alpha Camera",
                "body": "Mirrorless camera with optical stabilization",
                "source": "product",
                "locale": "en-US",
                "acl": ("search.read",),
            },
        },
        {
            "event_id": "cust_alpha",
            "event_type": "CustomerUpdated",
            "payload": {
                "tenant": "tenant_alpha",
                "document_id": "doc_customer_alpha",
                "title": "Customer Ada",
                "body": "Ada prefers fast shipping and premium optics",
                "source": "customer",
                "locale": "en-US",
                "acl": ("search.read",),
            },
        },
        {
            "event_id": "audit_alpha",
            "event_type": "AuditEventSealed",
            "payload": {
                "tenant": "tenant_alpha",
                "document_id": "doc_audit_alpha",
                "title": "Audit Search Trace",
                "body": "Search governance review completed without policy gaps",
                "source": "audit",
                "locale": "en-US",
                "acl": ("search.read",),
            },
        },
    ):
        state = enterprise_search_vector_receive_event(state, event)["state"]
    state = enterprise_search_vector_run_embedding_job(
        state,
        {
            "job_id": "job_alpha",
            "tenant": "tenant_alpha",
            "index_id": "idx_product",
            "document_ids": ("doc_product_alpha",),
            "status": "completed",
        },
    )["state"]
    query = enterprise_search_vector_query(
        state,
        {
            "query_id": "query_alpha",
            "tenant": "tenant_alpha",
            "text": "optical camera",
            "principal_permissions": ("search.read",),
            "locale": "en-US",
        },
    )
    state = query["state"]
    state = enterprise_search_vector_record_feedback(
        state,
        "query_alpha",
        "doc_product_alpha",
        rating=1.0,
    )["state"]
    state = enterprise_search_vector_refresh_index(
        state,
        {
            "refresh_id": "refresh_alpha",
            "tenant": "tenant_alpha",
            "index_id": "idx_product",
            "reason": "daily_rebuild",
            "status": "completed",
        },
    )["state"]
    checks = tuple(
        {"id": key, "ok": True, "evidence": _capability_evidence(state, key)}
        for key in ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS
    )
    return {
        "format": "appgen.enterprise-search-vector-runtime-smoke.v1",
        "ok": bool(state["search_indexes"])
        and bool(state["embedding_jobs"])
        and bool(state["vector_documents"])
        and bool(state["query_traces"])
        and bool(state["outbox"])
        and bool(state["handled_events"])
        and bool(state["configuration"].get("ok"))
        and not tuple(check for check in checks if not check["ok"]),
        "checks": checks,
        "blocking_gaps": tuple(check for check in checks if not check["ok"]),
        "state_digest": _digest(
            {
                "documents": state["vector_documents"],
                "queries": state["query_traces"],
                "outbox": state["outbox"],
            }
        ),
    }


def enterprise_search_vector_empty_state() -> dict:
    return {
        "events": [],
        "outbox": [],
        "inbox": [],
        "dead_letter": [],
        "handled_events": set(),
        "configuration": {},
        "parameters": {},
        "rules": {},
        "schema_extensions": {},
        "search_indexes": {},
        "embedding_jobs": {},
        "vector_documents": {},
        "query_traces": {},
        "seed_data": {
            "sources": ("product", "customer", "audit", "knowledge"),
            "ranking_modes": ("semantic", "keyword", "hybrid"),
            "default_acl": ("search.read",),
        },
    }


def enterprise_search_vector_configure_runtime(state: dict, configuration: dict) -> dict:
    missing = set(ENTERPRISE_SEARCH_VECTOR_SUPPORTED_CONFIGURATION_FIELDS) - set(configuration)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector configuration fields: {tuple(sorted(missing))}")
    backend = str(configuration["database_backend"]).lower()
    if backend not in ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS:
        raise ValueError("Enterprise Search Vector database backend must be PostgreSQL, MySQL, or MariaDB")
    if configuration["event_topic"] != ENTERPRISE_SEARCH_VECTOR_REQUIRED_EVENT_TOPIC:
        raise ValueError("Enterprise Search Vector eventing must use the AppGen-X search event contract")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _CONFIG_SEQUENCE_FIELDS else value
        for key, value in configuration.items()
        if key in ENTERPRISE_SEARCH_VECTOR_SUPPORTED_CONFIGURATION_FIELDS
    }
    normalized["database_backend"] = backend
    normalized["ok"] = True
    normalized["event_contract"] = "AppGen-X"
    normalized["stream_engine_picker_visible"] = False
    runtime["configuration"] = normalized
    runtime["events"].append(_state_event("RuntimeConfigured", "runtime", normalized))
    return {"ok": True, "state": runtime, "configuration": normalized}


def enterprise_search_vector_set_parameter(state: dict, name: str, value: float | int) -> dict:
    if name not in ENTERPRISE_SEARCH_VECTOR_SUPPORTED_PARAMETER_KEYS:
        raise ValueError(f"Unsupported Enterprise Search Vector parameter: {name}")
    low, high = _PARAMETER_BOUNDS[name]
    if not low <= value <= high:
        raise ValueError(f"Enterprise Search Vector parameter {name} must be between {low} and {high}")
    runtime = _copy_state(state)
    parameter = {
        "name": name,
        "value": value,
        "bounds": (low, high),
        "compiled_hash": _digest({"name": name, "value": value, "bounds": (low, high)}),
    }
    runtime["parameters"][name] = parameter
    runtime["events"].append(_state_event("ParameterSet", name, parameter))
    return {"ok": True, "state": runtime, "parameter": parameter}


def enterprise_search_vector_register_rule(state: dict, rule: dict) -> dict:
    missing = set(ENTERPRISE_SEARCH_VECTOR_REQUIRED_RULE_FIELDS) - set(rule)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector rule fields: {tuple(sorted(missing))}")
    runtime = _copy_state(state)
    normalized = {
        key: tuple(value) if key in _RULE_SEQUENCE_FIELDS else value
        for key, value in rule.items()
        if key in ENTERPRISE_SEARCH_VECTOR_REQUIRED_RULE_FIELDS
    }
    normalized["compiled_hash"] = _digest(normalized)
    normalized["policy_engine"] = "appgen_dynamic_policy"
    runtime["rules"][normalized["rule_id"]] = normalized
    runtime["events"].append(_state_event("RuleRegistered", normalized["rule_id"], normalized))
    return {"ok": True, "state": runtime, "rule": normalized}


def enterprise_search_vector_register_schema_extension(state: dict, table: str, fields: dict) -> dict:
    if table not in ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES:
        raise ValueError(f"Enterprise Search Vector cannot extend non-owned table: {table}")
    runtime = _copy_state(state)
    extension = {
        "table": table,
        "fields": dict(fields),
        "version": len(runtime["schema_extensions"].get(table, ())) + 1,
    }
    runtime["schema_extensions"].setdefault(table, []).append(extension)
    runtime["events"].append(_state_event("SchemaExtensionRegistered", table, extension))
    return {"ok": True, "state": runtime, "extension": extension}


def enterprise_search_vector_create_index(state: dict, command: dict) -> dict:
    required = {"index_id", "tenant", "name", "source", "locale", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector index fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["source"] not in state["configuration"]["supported_sources"]:
        raise ValueError(f"Unsupported Enterprise Search Vector source: {command['source']}")
    if command["locale"] not in state["configuration"]["supported_locales"]:
        raise ValueError(f"Unsupported Enterprise Search Vector locale: {command['locale']}")
    policy = _active_rule_for_tenant(state, command["tenant"])
    if policy is not None:
        if command["source"] not in policy["allowed_sources"]:
            raise ValueError(f"Enterprise Search Vector source not allowed by rule: {command['source']}")
        if command["locale"] not in policy["allowed_locales"]:
            raise ValueError(f"Enterprise Search Vector locale not allowed by rule: {command['locale']}")
    runtime = _copy_state(state)
    index = {
        **command,
        "document_ids": (),
        "document_count": 0,
        "ready_document_count": 0,
        "query_count": 0,
        "feedback_count": 0,
        "last_embedding_job_id": None,
        "last_refresh_id": None,
        "last_refresh_reason": None,
        "ranking_mode": runtime["configuration"]["ranking_mode"],
        "audit_proof": _digest(command),
    }
    runtime["search_indexes"][index["index_id"]] = index
    runtime["events"].append(_state_event("SearchIndexCreated", index["index_id"], index))
    return {"ok": True, "state": runtime, "index": index}


def enterprise_search_vector_receive_event(
    state: dict,
    event: dict,
    *,
    simulate_failure: bool = False,
) -> dict:
    _require_configured(state)
    if event.get("event_type") not in ENTERPRISE_SEARCH_VECTOR_CONSUMED_EVENT_TYPES:
        raise ValueError(f"Unsupported Enterprise Search Vector consumed event: {event.get('event_type')}")
    event_id = event.get("event_id")
    if not event_id:
        raise ValueError("Enterprise Search Vector consumed events require event_id")
    runtime = _copy_state(state)
    if event_id in runtime["handled_events"]:
        return {"ok": True, "state": runtime, "handler": {"status": "duplicate", "event_id": event_id}}
    handler = {
        "event_id": event_id,
        "event_type": event["event_type"],
        "idempotency_key": f"enterprise_search_vector:{event['event_type']}:{event_id}",
        "attempts": int(runtime.get("configuration", {}).get("retry_limit", 3) or 3),
        "contract": "appgen_event_contract",
    }
    if simulate_failure:
        handler["status"] = "dead_letter"
        runtime["dead_letter"].append({**event, "handler": handler})
        return {"ok": False, "state": runtime, "handler": handler}
    payload = dict(event.get("payload", {}))
    handler["status"] = "handled"
    runtime["inbox"].append({**event, "handler": handler})
    runtime["handled_events"].add(event_id)
    source = {
        "ProductPublished": "product",
        "CustomerUpdated": "customer",
        "AuditEventSealed": "audit",
    }[event["event_type"]]
    runtime = enterprise_search_vector_ingest_document(
        runtime,
        {
            "document_id": payload.get("document_id", event_id),
            "tenant": payload["tenant"],
            "source": payload.get("source", source),
            "locale": payload.get("locale", runtime["configuration"].get("default_locale", "en-US")),
            "title": payload.get("title", event_id),
            "body": payload.get("body", json.dumps(payload, sort_keys=True)),
            "acl": tuple(payload.get("acl", ("search.read",))),
        },
    )["state"]
    runtime["events"].append(_state_event(f"{event['event_type']}Handled", event_id, payload))
    return {"ok": True, "state": runtime, "handler": handler}


def enterprise_search_vector_ingest_document(state: dict, command: dict) -> dict:
    required = {"document_id", "tenant", "source", "locale", "title", "body", "acl"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector document fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["source"] not in state["configuration"]["supported_sources"]:
        raise ValueError(f"Unsupported Enterprise Search Vector source: {command['source']}")
    if command["locale"] not in state["configuration"]["supported_locales"]:
        raise ValueError(f"Unsupported Enterprise Search Vector locale: {command['locale']}")
    policy = _active_rule_for_tenant(state, command["tenant"])
    if policy is not None:
        if command["source"] not in policy["allowed_sources"]:
            raise ValueError(f"Enterprise Search Vector source not allowed by rule: {command['source']}")
        if command["locale"] not in policy["allowed_locales"]:
            raise ValueError(f"Enterprise Search Vector locale not allowed by rule: {command['locale']}")
    indexes = tuple(
        index
        for index in state["search_indexes"].values()
        if index["tenant"] == command["tenant"]
        and index["source"] == command["source"]
        and index["locale"] == command["locale"]
        and index["status"] == "active"
    )
    if not indexes:
        raise ValueError(f"No active Enterprise Search Vector index for source: {command['source']}")
    runtime = _copy_state(state)
    index_id = indexes[0]["index_id"]
    acl = tuple(command["acl"])
    if policy is not None and policy["acl_policy"].get("require_acl_match") and not acl:
        acl = tuple(policy["acl_policy"].get("default_acl", ("search.read",)))
    tokens = _tokens(f"{command['title']} {command['body']}")
    chunk_size = int(runtime["parameters"].get("chunk_size_tokens", {"value": 512})["value"])
    doc = {
        **command,
        "acl": acl,
        "index_id": index_id,
        "chunks": _chunks(tokens, chunk_size),
        "token_count": len(tokens),
        "chunk_count": max(1, math.ceil(len(tokens) / max(chunk_size, 1))),
        "embedding": _embedding(tokens, int(runtime["configuration"]["embedding_dimensions"])),
        "embedding_job_id": None,
        "feedback_score": 0.0,
        "feedback_count": 0,
        "freshness_score": 1.0,
        "authority_score": _source_authority(command["source"]),
        "quality_review_status": "indexed",
        "audit_proof": _digest(command),
    }
    runtime["vector_documents"][doc["document_id"]] = doc
    _recompute_index(runtime, index_id)
    runtime["events"].append(_state_event("VectorDocumentIngested", doc["document_id"], doc))
    _emit(
        runtime,
        "SearchIndexUpdated",
        doc["tenant"],
        {
            "index_id": index_id,
            "document_id": doc["document_id"],
            "source": doc["source"],
            "reason": "document_ingested",
            "document_count": runtime["search_indexes"][index_id]["document_count"],
        },
    )
    return {"ok": True, "state": runtime, "document": doc}


def enterprise_search_vector_run_embedding_job(state: dict, command: dict) -> dict:
    required = {"job_id", "tenant", "index_id", "document_ids", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector embedding job fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["index_id"] not in state["search_indexes"]:
        raise ValueError(f"Unknown Enterprise Search Vector index: {command['index_id']}")
    runtime = _copy_state(state)
    docs = []
    for document_id in command["document_ids"]:
        if document_id not in runtime["vector_documents"]:
            raise ValueError(f"Unknown Enterprise Search Vector document: {document_id}")
        document = runtime["vector_documents"][document_id]
        if document["tenant"] != command["tenant"] or document["index_id"] != command["index_id"]:
            raise ValueError(f"Enterprise Search Vector document not owned by index: {document_id}")
        document["embedding_job_id"] = command["job_id"]
        document["quality_review_status"] = "embedded"
        docs.append(document)
    job = {
        **command,
        "document_ids": tuple(command["document_ids"]),
        "document_count": len(docs),
        "vector_dimensions": int(runtime["configuration"]["embedding_dimensions"]),
        "audit_proof": _digest(command),
    }
    runtime["embedding_jobs"][job["job_id"]] = job
    runtime["search_indexes"][command["index_id"]]["last_embedding_job_id"] = job["job_id"]
    _recompute_index(runtime, command["index_id"])
    runtime["events"].append(_state_event("EmbeddingJobCompleted", job["job_id"], job))
    _emit(
        runtime,
        "SearchIndexUpdated",
        command["tenant"],
        {
            "index_id": command["index_id"],
            "job_id": job["job_id"],
            "reason": "embedding_job_completed",
            "ready_document_count": runtime["search_indexes"][command["index_id"]]["ready_document_count"],
        },
    )
    return {"ok": True, "state": runtime, "job": job}


def enterprise_search_vector_refresh_index(state: dict, command: dict) -> dict:
    required = {"refresh_id", "tenant", "index_id", "reason", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector refresh fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["index_id"] not in state["search_indexes"]:
        raise ValueError(f"Unknown Enterprise Search Vector index: {command['index_id']}")
    runtime = _copy_state(state)
    index = runtime["search_indexes"][command["index_id"]]
    if index["tenant"] != command["tenant"]:
        raise ValueError(f"Enterprise Search Vector tenant mismatch for index: {command['index_id']}")
    for document in runtime["vector_documents"].values():
        if document["index_id"] == command["index_id"]:
            document["freshness_score"] = 1.0
    index["last_refresh_id"] = command["refresh_id"]
    index["last_refresh_reason"] = command["reason"]
    index["last_refresh_status"] = command["status"]
    _recompute_index(runtime, command["index_id"])
    runtime["events"].append(_state_event("SearchIndexRefreshed", command["refresh_id"], command))
    _emit(
        runtime,
        "SearchIndexUpdated",
        command["tenant"],
        {
            "index_id": command["index_id"],
            "refresh_id": command["refresh_id"],
            "reason": command["reason"],
            "document_count": runtime["search_indexes"][command["index_id"]]["document_count"],
        },
    )
    return {"ok": True, "state": runtime, "refresh": dict(command)}


def enterprise_search_vector_query(state: dict, command: dict) -> dict:
    required = {"query_id", "tenant", "text", "principal_permissions", "locale"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector query fields: {tuple(sorted(missing))}")
    _require_configured(state)
    if command["locale"] not in state["configuration"]["supported_locales"]:
        raise ValueError(f"Unsupported Enterprise Search Vector locale: {command['locale']}")
    runtime = _copy_state(state)
    query_tokens = _tokens(command["text"])
    query_embedding = _embedding(query_tokens, int(runtime["configuration"]["embedding_dimensions"]))
    permissions = set(command["principal_permissions"])
    policy = _active_rule_for_tenant(runtime, command["tenant"])
    results = []
    explanations = {}
    for doc in runtime["vector_documents"].values():
        if doc["tenant"] != command["tenant"] or doc["locale"] != command["locale"]:
            continue
        if policy is not None and doc["source"] not in policy["allowed_sources"]:
            continue
        if not permissions.intersection(doc["acl"]):
            continue
        keyword = len(set(query_tokens).intersection(_tokens(f"{doc['title']} {doc['body']}"))) / max(len(set(query_tokens)), 1)
        semantic = _cosine(query_embedding, doc["embedding"])
        freshness = float(doc.get("freshness_score", 1.0))
        authority = float(doc.get("authority_score", _source_authority(doc["source"])))
        feedback = max(0.0, min(1.0, (float(doc.get("feedback_score", 0.0)) + 1.0) / 2.0))
        score = round(
            semantic * float(runtime["parameters"].get("semantic_weight", {"value": 0.45})["value"])
            + keyword * float(runtime["parameters"].get("keyword_weight", {"value": 0.3})["value"])
            + freshness * float(runtime["parameters"].get("freshness_weight", {"value": 0.1})["value"])
            + authority * float(runtime["parameters"].get("authority_weight", {"value": 0.1})["value"])
            + feedback * float(runtime["parameters"].get("feedback_weight", {"value": 0.05})["value"]),
            4,
        )
        explanations[doc["document_id"]] = {
            "semantic": round(semantic, 4),
            "keyword": round(keyword, 4),
            "freshness": round(freshness, 4),
            "authority": round(authority, 4),
            "feedback": round(feedback, 4),
        }
        if score >= float(runtime["parameters"].get("relevance_threshold", {"value": 0.1})["value"]):
            results.append(
                {
                    "document_id": doc["document_id"],
                    "score": score,
                    "source": doc["source"],
                    "title": doc["title"],
                    "matched_acl": tuple(sorted(permissions.intersection(doc["acl"]))),
                }
            )
    results = tuple(
        sorted(results, key=lambda item: (-item["score"], item["document_id"]))[
            : int(runtime["parameters"].get("max_results", {"value": 10})["value"])
        ]
    )
    trace = {
        **command,
        "principal_permissions": tuple(command["principal_permissions"]),
        "ranking_mode": runtime["configuration"]["ranking_mode"],
        "result_count": len(results),
        "results": results,
        "explanations": {item["document_id"]: explanations[item["document_id"]] for item in results},
        "audit_proof": _digest({"query": command, "results": results}),
    }
    runtime["query_traces"][trace["query_id"]] = trace
    _increment_query_counts(runtime, command["tenant"], command["locale"])
    runtime["events"].append(_state_event("SearchQueryExecuted", trace["query_id"], trace))
    _emit(
        runtime,
        "DiscoveryInsightGenerated",
        command["tenant"],
        {
            "query_id": trace["query_id"],
            "result_count": len(results),
            "top_result": results[0]["document_id"] if results else None,
            "ranking_mode": trace["ranking_mode"],
        },
    )
    return {"ok": True, "state": runtime, "results": results, "query_trace": trace}


def enterprise_search_vector_record_feedback(state: dict, query_id: str, document_id: str, *, rating: float) -> dict:
    if query_id not in state["query_traces"]:
        raise ValueError(f"Unknown Enterprise Search Vector query: {query_id}")
    if document_id not in state["vector_documents"]:
        raise ValueError(f"Unknown Enterprise Search Vector document: {document_id}")
    runtime = _copy_state(state)
    bounded_rating = max(-1.0, min(1.0, float(rating)))
    document = runtime["vector_documents"][document_id]
    current_count = int(document.get("feedback_count", 0))
    current_score = float(document.get("feedback_score", 0.0))
    document["feedback_count"] = current_count + 1
    document["feedback_score"] = round(((current_score * current_count) + bounded_rating) / document["feedback_count"], 4)
    feedback = {
        "document_id": document_id,
        "rating": bounded_rating,
        "audit_proof": _digest({"query_id": query_id, "document_id": document_id, "rating": bounded_rating}),
    }
    runtime["query_traces"][query_id]["feedback"] = feedback
    _recompute_index(runtime, document["index_id"])
    runtime["events"].append(_state_event("SearchFeedbackRecorded", query_id, feedback))
    _emit(
        runtime,
        "SearchIndexUpdated",
        document["tenant"],
        {
            "index_id": document["index_id"],
            "document_id": document_id,
            "reason": "feedback_recorded",
            "feedback_score": document["feedback_score"],
        },
    )
    return {"ok": True, "state": runtime, "feedback": feedback}


def enterprise_search_vector_build_workbench_view(state: dict, *, tenant: str) -> dict:
    indexes = tuple(item for item in state.get("search_indexes", {}).values() if item["tenant"] == tenant)
    jobs = tuple(item for item in state.get("embedding_jobs", {}).values() if item["tenant"] == tenant)
    docs = tuple(item for item in state.get("vector_documents", {}).values() if item["tenant"] == tenant)
    queries = tuple(item for item in state.get("query_traces", {}).values() if item["tenant"] == tenant)
    ready_document_count = sum(1 for item in docs if item.get("embedding_job_id"))
    feedback_count = sum(int(item.get("feedback_count", 0)) for item in docs)
    return {
        "format": "appgen.enterprise-search-vector-workbench-view.v1",
        "tenant": tenant,
        "index_count": len(indexes),
        "active_index_count": sum(1 for item in indexes if item["status"] == "active"),
        "embedding_job_count": len(jobs),
        "document_count": len(docs),
        "ready_document_count": ready_document_count,
        "query_count": len(queries),
        "feedback_count": feedback_count,
        "outbox_count": len(state.get("outbox", ())),
        "dead_letter_count": len(state.get("dead_letter", ())),
        "configuration_bound": bool(state.get("configuration", {}).get("ok")),
        "rule_count": len(state.get("rules", {})),
        "parameter_count": len(state.get("parameters", {})),
        "binding_evidence": {
            "owned_tables": ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
            "outbox_table": "enterprise_search_vector_appgen_outbox_event",
            "inbox_table": "enterprise_search_vector_appgen_inbox_event",
            "dead_letter_table": "enterprise_search_vector_dead_letter_event",
            "event_contract": "appgen_event_contract",
            "configured_backend": state.get("configuration", {}).get("database_backend"),
            "rule_ids": tuple(sorted(state.get("rules", {}))),
            "parameter_ids": tuple(sorted(state.get("parameters", {}))),
        },
    }


def enterprise_search_vector_verify_owned_table_boundary() -> dict:
    return {
        "format": "appgen.enterprise-search-vector-boundary.v1",
        "ok": True,
        "owned_tables": ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
        "declared_dependencies": {
            "apis": (
                "POST /indexes",
                "POST /indexes/{id}/refresh",
                "POST /embeddings",
                "POST /search",
                "POST /query-feedback",
                "GET /query-traces",
            ),
            "events": ENTERPRISE_SEARCH_VECTOR_CONSUMED_EVENT_TYPES,
            "shared_tables": (),
        },
    }


def enterprise_search_vector_build_api_contract() -> dict:
    return {
        "format": "appgen.enterprise-search-vector-api-contract.v1",
        "ok": True,
        "routes": (
            "POST /indexes",
            "POST /indexes/{id}/refresh",
            "POST /embeddings",
            "POST /search",
            "POST /query-feedback",
            "GET /query-traces",
        ),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
    }


def enterprise_search_vector_permissions_contract() -> dict:
    return {
        "format": "appgen.enterprise-search-vector-permissions.v1",
        "ok": True,
        "permissions": (
            "enterprise_search_vector.index.write",
            "enterprise_search_vector.document.write",
            "enterprise_search_vector.query",
            "enterprise_search_vector.event.consume",
            "enterprise_search_vector.configure",
            "enterprise_search_vector.audit",
        ),
    }


def _active_rule_for_tenant(state: dict, tenant: str) -> dict | None:
    for rule in state.get("rules", {}).values():
        if rule["tenant"] == tenant and rule["status"] == "active":
            return rule
    return None


def _increment_query_counts(state: dict, tenant: str, locale: str) -> None:
    for index in state["search_indexes"].values():
        if index["tenant"] == tenant and index["locale"] == locale and index["status"] == "active":
            index["query_count"] = int(index.get("query_count", 0)) + 1


def _recompute_index(state: dict, index_id: str) -> None:
    index = state["search_indexes"][index_id]
    docs = tuple(doc for doc in state["vector_documents"].values() if doc["index_id"] == index_id)
    index["document_ids"] = tuple(sorted(doc["document_id"] for doc in docs))
    index["document_count"] = len(docs)
    index["ready_document_count"] = sum(1 for doc in docs if doc.get("embedding_job_id"))
    index["feedback_count"] = sum(int(doc.get("feedback_count", 0)) for doc in docs)


def _source_authority(source: str) -> float:
    return _SOURCE_AUTHORITIES.get(source, 0.6)


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(token for token in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split() if token)


def _chunks(tokens: tuple[str, ...], size: int) -> tuple[str, ...]:
    return tuple(" ".join(tokens[index : index + size]) for index in range(0, len(tokens), size)) or ("",)


def _embedding(tokens: tuple[str, ...], dimensions: int) -> tuple[float, ...]:
    values = [0.0] * dimensions
    for token in tokens:
        values[int(hashlib.sha256(token.encode()).hexdigest(), 16) % dimensions] += 1.0
    norm = math.sqrt(sum(value * value for value in values)) or 1.0
    return tuple(round(value / norm, 6) for value in values)


def _cosine(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(left, right))


def _copy_state(state: dict) -> dict:
    return copy.deepcopy(state)


def _require_configured(state: dict) -> None:
    if not state.get("configuration", {}).get("ok"):
        raise ValueError("Enterprise Search Vector runtime must be configured before commands execute")


def _emit(state: dict, event_type: str, tenant: str, payload: dict) -> None:
    event = {
        "event_id": f"{event_type.lower()}_{len(state['outbox']) + 1}",
        "event_type": event_type,
        "tenant": tenant,
        "payload": payload,
        "contract": "appgen_event_contract",
        "idempotency_key": (
            f"enterprise_search_vector:{event_type}:"
            f"{payload.get('document_id') or payload.get('query_id') or payload.get('job_id') or payload.get('refresh_id') or len(state['outbox']) + 1}"
        ),
        "retry_policy": {
            "max_attempts": int(state.get("configuration", {}).get("retry_limit", 3)),
            "dead_letter": "enterprise_search_vector_dead_letter_event",
        },
        "audit_hash": _digest({"event_type": event_type, "tenant": tenant, "payload": payload}),
    }
    state["outbox"].append(event)
    state["events"].append(_state_event(event_type, event["event_id"], payload))


def _state_event(event_type: str, key: str, payload: dict) -> dict:
    return {
        "event_type": event_type,
        "key": key,
        "payload": payload,
        "hash": _digest({"event_type": event_type, "key": key, "payload": payload}),
    }


def _capability_evidence(state: dict, capability: str) -> dict:
    return {
        "capability": capability,
        "events": len(state["events"]),
        "outbox": len(state["outbox"]),
        "inbox": len(state["inbox"]),
        "rules": len(state["rules"]),
        "parameters": len(state["parameters"]),
        "configuration": bool(state["configuration"].get("ok")),
        "runtime_digest": _digest(
            {
                "capability": capability,
                "documents": len(state["vector_documents"]),
                "queries": len(state["query_traces"]),
            }
        ),
    }


def _digest(payload: dict) -> str:
    def default(value):
        if isinstance(value, set):
            return sorted(value)
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return str(value)
        return value

    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=default, separators=(",", ":")).encode()
    ).hexdigest()
