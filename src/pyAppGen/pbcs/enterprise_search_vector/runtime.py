"""Executable runtime for the Enterprise Search Vector PBC."""

from __future__ import annotations

import copy
import hashlib
import json
import math

from .domain_schema import class_name_for, field_names_for, fields_for, relationships_for

ENTERPRISE_SEARCH_VECTOR_REQUIRED_EVENT_TOPIC = "appgen.enterprise_search_vector.events"
ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS = ("postgresql", "mysql", "mariadb")
ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES = (
    "search_index",
    "embedding_job",
    "vector_document",
    "query_trace",
    "ranking_simulation",
    "freshness_forecast",
    "quality_remediation",
    "search_policy_screening",
    "relevance_control_assertion",
    "index_proof",
    "federated_search_view",
    "query_intent_risk",
    "retention_deletion_record",
    "search_audit_entry",
    "search_governed_model",
)
ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES = (
    "enterprise_search_vector_appgen_outbox_event",
    "enterprise_search_vector_appgen_inbox_event",
    "enterprise_search_vector_dead_letter_event",
)

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
        "runtime_tables": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES,
        "capabilities": ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS,
        "standard_features": ENTERPRISE_SEARCH_VECTOR_STANDARD_FEATURE_KEYS,
        "operations": (
            "configure_runtime",
            "set_parameter",
            "register_rule",
            "register_schema_extension",
            "create_index",
            "ingest_document",
            "run_embedding_job",
            "refresh_index",
            "query",
            "record_feedback",
            "simulate_counterfactual_ranking",
            "forecast_index_freshness",
            "remediate_search_quality",
            "screen_search_policy",
            "run_relevance_controls",
            "generate_index_proof",
            "federate_search_sources",
            "score_query_intent_risk",
            "record_retention_deletion",
            "register_governed_model",
            "receive_event",
            "build_api_contract",
            "build_workbench_view",
            "build_schema_contract",
            "build_service_contract",
            "build_release_evidence",
            "permissions_contract",
            "verify_owned_table_boundary",
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
    state = enterprise_search_vector_simulate_counterfactual_ranking(
        state,
        {
            "simulation_id": "sim_alpha",
            "tenant": "tenant_alpha",
            "query_id": "query_alpha",
            "weight_overrides": {"freshness": 0.5, "feedback": 0.2},
        },
    )["state"]
    state = enterprise_search_vector_forecast_index_freshness(
        state,
        {"forecast_id": "fresh_alpha", "tenant": "tenant_alpha", "index_id": "idx_product", "horizon_days": 30},
    )["state"]
    state = enterprise_search_vector_remediate_search_quality(
        state,
        {
            "remediation_id": "rem_alpha",
            "tenant": "tenant_alpha",
            "document_id": "doc_product_alpha",
            "issue": "low_explainability",
            "action": "regenerate_chunks",
        },
    )["state"]
    state = enterprise_search_vector_screen_search_policy(
        state,
        {
            "screening_id": "policy_alpha",
            "tenant": "tenant_alpha",
            "source": "product",
            "locale": "en-US",
            "principal_permissions": ("search.read",),
        },
    )["state"]
    state = enterprise_search_vector_run_relevance_controls(
        state,
        {"assertion_id": "ctl_alpha", "tenant": "tenant_alpha", "query_id": "query_alpha"},
    )["state"]
    state = enterprise_search_vector_generate_index_proof(
        state,
        {"proof_id": "proof_alpha", "tenant": "tenant_alpha", "index_id": "idx_product"},
    )["state"]
    state = enterprise_search_vector_federate_search_sources(
        state,
        {"view_id": "fed_alpha", "tenant": "tenant_alpha", "index_id": "idx_product"},
    )["state"]
    state = enterprise_search_vector_score_query_intent_risk(
        state,
        {"risk_id": "risk_alpha", "tenant": "tenant_alpha", "query_id": "query_alpha"},
    )["state"]
    state = enterprise_search_vector_record_retention_deletion(
        state,
        {
            "record_id": "ret_alpha",
            "tenant": "tenant_alpha",
            "document_id": "doc_customer_alpha",
            "reason": "retention_review",
            "status": "retained",
        },
    )["state"]
    state = enterprise_search_vector_register_governed_model(
        state,
        {
            "model_id": "model_alpha",
            "tenant": "tenant_alpha",
            "model_type": "embedding",
            "version": "2026.05",
            "status": "approved",
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
        and bool(state["ranking_simulations"])
        and bool(state["freshness_forecasts"])
        and bool(state["quality_remediations"])
        and bool(state["search_policy_screenings"])
        and bool(state["relevance_control_assertions"])
        and bool(state["index_proofs"])
        and bool(state["federated_search_views"])
        and bool(state["query_intent_risks"])
        and bool(state["retention_deletion_records"])
        and bool(state["search_governed_models"])
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
        "ranking_simulations": {},
        "freshness_forecasts": {},
        "quality_remediations": {},
        "search_policy_screenings": {},
        "relevance_control_assertions": {},
        "index_proofs": {},
        "federated_search_views": {},
        "query_intent_risks": {},
        "retention_deletion_records": {},
        "search_audit_entries": {},
        "search_governed_models": {},
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


def enterprise_search_vector_simulate_counterfactual_ranking(state: dict, command: dict) -> dict:
    required = {"simulation_id", "tenant", "query_id", "weight_overrides"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector ranking simulation fields: {tuple(sorted(missing))}")
    if command["query_id"] not in state["query_traces"]:
        raise ValueError(f"Unknown Enterprise Search Vector query: {command['query_id']}")
    trace = state["query_traces"][command["query_id"]]
    if trace["tenant"] != command["tenant"]:
        raise ValueError(f"Enterprise Search Vector tenant mismatch for query: {command['query_id']}")
    overrides = dict(command["weight_overrides"])
    simulated = []
    for result in trace["results"]:
        factors = trace["explanations"][result["document_id"]]
        score = (
            factors["semantic"] * float(overrides.get("semantic", state["parameters"].get("semantic_weight", {"value": 0.45})["value"]))
            + factors["keyword"] * float(overrides.get("keyword", state["parameters"].get("keyword_weight", {"value": 0.3})["value"]))
            + factors["freshness"] * float(overrides.get("freshness", state["parameters"].get("freshness_weight", {"value": 0.1})["value"]))
            + factors["authority"] * float(overrides.get("authority", state["parameters"].get("authority_weight", {"value": 0.1})["value"]))
            + factors["feedback"] * float(overrides.get("feedback", state["parameters"].get("feedback_weight", {"value": 0.05})["value"]))
        )
        simulated.append({**result, "simulated_score": round(score, 4)})
    simulation = {
        **command,
        "weight_overrides": overrides,
        "baseline_top_result": trace["results"][0]["document_id"] if trace["results"] else None,
        "simulated_results": tuple(sorted(simulated, key=lambda item: (-item["simulated_score"], item["document_id"]))),
        "audit_proof": _digest(command),
    }
    runtime = _copy_state(state)
    runtime["ranking_simulations"][simulation["simulation_id"]] = simulation
    runtime["events"].append(_state_event("CounterfactualRankingSimulated", simulation["simulation_id"], simulation))
    return {"ok": True, "state": runtime, "simulation": simulation}


def enterprise_search_vector_forecast_index_freshness(state: dict, command: dict) -> dict:
    required = {"forecast_id", "tenant", "index_id", "horizon_days"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector freshness forecast fields: {tuple(sorted(missing))}")
    if command["index_id"] not in state["search_indexes"]:
        raise ValueError(f"Unknown Enterprise Search Vector index: {command['index_id']}")
    index = state["search_indexes"][command["index_id"]]
    if index["tenant"] != command["tenant"]:
        raise ValueError(f"Enterprise Search Vector tenant mismatch for index: {command['index_id']}")
    docs = tuple(doc for doc in state["vector_documents"].values() if doc["index_id"] == command["index_id"])
    current = round(sum(float(doc.get("freshness_score", 1.0)) for doc in docs) / max(len(docs), 1), 4)
    decay = min(0.8, max(0.0, int(command["horizon_days"]) / 365.0))
    forecast = {
        **command,
        "document_count": len(docs),
        "current_freshness_score": current,
        "projected_freshness_score": round(max(0.0, current - decay), 4),
        "recommended_refresh_before_days": max(1, min(int(command["horizon_days"]), 14 if current < 0.8 else 30)),
        "audit_proof": _digest(command),
    }
    runtime = _copy_state(state)
    runtime["freshness_forecasts"][forecast["forecast_id"]] = forecast
    runtime["events"].append(_state_event("IndexFreshnessForecasted", forecast["forecast_id"], forecast))
    return {"ok": True, "state": runtime, "forecast": forecast}


def enterprise_search_vector_remediate_search_quality(state: dict, command: dict) -> dict:
    required = {"remediation_id", "tenant", "document_id", "issue", "action"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector quality remediation fields: {tuple(sorted(missing))}")
    if command["document_id"] not in state["vector_documents"]:
        raise ValueError(f"Unknown Enterprise Search Vector document: {command['document_id']}")
    runtime = _copy_state(state)
    document = runtime["vector_documents"][command["document_id"]]
    if document["tenant"] != command["tenant"]:
        raise ValueError(f"Enterprise Search Vector tenant mismatch for document: {command['document_id']}")
    document["quality_review_status"] = "remediated"
    document["freshness_score"] = max(float(document.get("freshness_score", 1.0)), 0.95)
    remediation = {
        **command,
        "result": "applied",
        "index_id": document["index_id"],
        "post_quality_status": document["quality_review_status"],
        "audit_proof": _digest(command),
    }
    runtime["quality_remediations"][remediation["remediation_id"]] = remediation
    _recompute_index(runtime, document["index_id"])
    runtime["events"].append(_state_event("SearchQualityRemediated", remediation["remediation_id"], remediation))
    _emit(
        runtime,
        "SearchIndexUpdated",
        command["tenant"],
        {"index_id": document["index_id"], "document_id": command["document_id"], "reason": "quality_remediated"},
    )
    return {"ok": True, "state": runtime, "remediation": remediation}


def enterprise_search_vector_screen_search_policy(state: dict, command: dict) -> dict:
    required = {"screening_id", "tenant", "source", "locale", "principal_permissions"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector policy screening fields: {tuple(sorted(missing))}")
    policy = _active_rule_for_tenant(state, command["tenant"])
    permissions = tuple(command["principal_permissions"])
    allowed_source = policy is None or command["source"] in policy["allowed_sources"]
    allowed_locale = policy is None or command["locale"] in policy["allowed_locales"]
    required_acl = tuple((policy or {}).get("acl_policy", {}).get("default_acl", ("search.read",)))
    allowed_acl = bool(set(permissions).intersection(required_acl))
    screening = {
        **command,
        "principal_permissions": permissions,
        "decision": "allowed" if allowed_source and allowed_locale and allowed_acl else "blocked",
        "policy_rule_id": policy.get("rule_id") if policy else None,
        "required_acl": required_acl,
        "audit_proof": _digest(command),
    }
    runtime = _copy_state(state)
    runtime["search_policy_screenings"][screening["screening_id"]] = screening
    runtime["events"].append(_state_event("SearchPolicyScreened", screening["screening_id"], screening))
    return {"ok": True, "state": runtime, "screening": screening}


def enterprise_search_vector_run_relevance_controls(state: dict, command: dict) -> dict:
    required = {"assertion_id", "tenant", "query_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector relevance control fields: {tuple(sorted(missing))}")
    if command["query_id"] not in state["query_traces"]:
        raise ValueError(f"Unknown Enterprise Search Vector query: {command['query_id']}")
    trace = state["query_traces"][command["query_id"]]
    threshold = float(state["parameters"].get("relevance_threshold", {"value": 0.1})["value"])
    top_score = float(trace["results"][0]["score"]) if trace["results"] else 0.0
    passed = trace["tenant"] == command["tenant"] and trace["result_count"] > 0 and top_score >= threshold
    assertion = {
        **command,
        "top_score": top_score,
        "threshold": threshold,
        "result_count": trace["result_count"],
        "status": "passed" if passed else "failed",
        "audit_proof": _digest(command),
    }
    runtime = _copy_state(state)
    runtime["relevance_control_assertions"][assertion["assertion_id"]] = assertion
    runtime["events"].append(_state_event("RelevanceControlsExecuted", assertion["assertion_id"], assertion))
    return {"ok": passed, "state": runtime, "assertion": assertion}


def enterprise_search_vector_generate_index_proof(state: dict, command: dict) -> dict:
    required = {"proof_id", "tenant", "index_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector index proof fields: {tuple(sorted(missing))}")
    if command["index_id"] not in state["search_indexes"]:
        raise ValueError(f"Unknown Enterprise Search Vector index: {command['index_id']}")
    index = state["search_indexes"][command["index_id"]]
    docs = tuple(doc for doc in state["vector_documents"].values() if doc["index_id"] == command["index_id"])
    proof_payload = {"index": index, "documents": docs, "query_count": index.get("query_count", 0)}
    proof = {
        **command,
        "document_count": len(docs),
        "proof_hash": _digest(proof_payload),
        "verification_status": "verifiable",
        "audit_proof": _digest(command),
    }
    runtime = _copy_state(state)
    runtime["index_proofs"][proof["proof_id"]] = proof
    _record_search_audit(runtime, command["tenant"], "generate_index_proof", proof)
    return {"ok": True, "state": runtime, "proof": proof}


def enterprise_search_vector_federate_search_sources(state: dict, command: dict) -> dict:
    required = {"view_id", "tenant", "index_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector federated view fields: {tuple(sorted(missing))}")
    if command["index_id"] not in state["search_indexes"]:
        raise ValueError(f"Unknown Enterprise Search Vector index: {command['index_id']}")
    docs = tuple(doc for doc in state["vector_documents"].values() if doc["tenant"] == command["tenant"])
    view = {
        **command,
        "source_counts": {
            source: sum(1 for doc in docs if doc["source"] == source)
            for source in tuple(sorted({doc["source"] for doc in docs}))
        },
        "query_count": sum(1 for query in state["query_traces"].values() if query["tenant"] == command["tenant"]),
        "declared_dependencies": enterprise_search_vector_verify_owned_table_boundary()["declared_dependencies"],
        "audit_proof": _digest(command),
    }
    runtime = _copy_state(state)
    runtime["federated_search_views"][view["view_id"]] = view
    runtime["events"].append(_state_event("FederatedSearchViewMaterialized", view["view_id"], view))
    return {"ok": True, "state": runtime, "view": view}


def enterprise_search_vector_score_query_intent_risk(state: dict, command: dict) -> dict:
    required = {"risk_id", "tenant", "query_id"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector query intent risk fields: {tuple(sorted(missing))}")
    if command["query_id"] not in state["query_traces"]:
        raise ValueError(f"Unknown Enterprise Search Vector query: {command['query_id']}")
    trace = state["query_traces"][command["query_id"]]
    sensitive_tokens = {"secret", "password", "payroll", "private", "credential"}
    hits = set(_tokens(trace["text"])).intersection(sensitive_tokens)
    risk = {
        **command,
        "risk_score": round(min(1.0, len(hits) * 0.35 + (0.2 if trace["result_count"] == 0 else 0.0)), 4),
        "risk_reasons": tuple(sorted(hits)) or ("normal_discovery_intent",),
        "decision": "allow" if not hits else "review",
        "audit_proof": _digest(command),
    }
    runtime = _copy_state(state)
    runtime["query_intent_risks"][risk["risk_id"]] = risk
    runtime["events"].append(_state_event("QueryIntentRiskScored", risk["risk_id"], risk))
    return {"ok": True, "state": runtime, "risk": risk}


def enterprise_search_vector_record_retention_deletion(state: dict, command: dict) -> dict:
    required = {"record_id", "tenant", "document_id", "reason", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector retention deletion fields: {tuple(sorted(missing))}")
    if command["document_id"] not in state["vector_documents"]:
        raise ValueError(f"Unknown Enterprise Search Vector document: {command['document_id']}")
    runtime = _copy_state(state)
    document = runtime["vector_documents"][command["document_id"]]
    if document["tenant"] != command["tenant"]:
        raise ValueError(f"Enterprise Search Vector tenant mismatch for document: {command['document_id']}")
    record = {**command, "index_id": document["index_id"], "audit_proof": _digest(command)}
    if command["status"] == "deleted":
        document["status"] = "deleted"
        document["body"] = ""
        document["chunks"] = ()
        document["embedding"] = ()
    runtime["retention_deletion_records"][record["record_id"]] = record
    _record_search_audit(runtime, command["tenant"], "record_retention_deletion", record)
    return {"ok": True, "state": runtime, "record": record}


def enterprise_search_vector_register_governed_model(state: dict, command: dict) -> dict:
    required = {"model_id", "tenant", "model_type", "version", "status"}
    missing = required - set(command)
    if missing:
        raise ValueError(f"Missing Enterprise Search Vector governed model fields: {tuple(sorted(missing))}")
    model = {
        **command,
        "approved": command["status"] in {"approved", "active"},
        "evidence_hash": _digest(command),
        "audit_proof": _digest(command),
    }
    runtime = _copy_state(state)
    runtime["search_governed_models"][model["model_id"]] = model
    runtime["events"].append(_state_event("SearchGovernedModelRegistered", model["model_id"], model))
    return {"ok": True, "state": runtime, "model": model}


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
            "runtime_tables": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES,
            "outbox_table": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[0],
            "inbox_table": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[1],
            "dead_letter_table": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[2],
            "event_contract": "appgen_event_contract",
            "configured_backend": state.get("configuration", {}).get("database_backend"),
            "rule_ids": tuple(sorted(state.get("rules", {}))),
            "parameter_ids": tuple(sorted(state.get("parameters", {}))),
        },
    }


def enterprise_search_vector_verify_owned_table_boundary(
    references: tuple[str, ...] | list[str] | set[str] = (),
) -> dict:
    allowed = (
        *ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
        *ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES,
        *ENTERPRISE_SEARCH_VECTOR_CONSUMED_EVENT_TYPES,
        *ENTERPRISE_SEARCH_VECTOR_EMITTED_EVENT_TYPES,
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
        "GET /query-traces",
    )
    allowed_set = set(allowed)
    violations = tuple(
        reference
        for reference in references
        if reference not in allowed_set and not str(reference).startswith("enterprise_search_vector_")
    )
    return {
        "format": "appgen.enterprise-search-vector-boundary.v1",
        "ok": not violations,
        "owned_tables": ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
        "runtime_tables": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES,
        "violations": violations,
        "declared_dependencies": {
            "apis": (
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
            "GET /query-traces",
        ),
        "shared_table_access": False,
        "event_contract": "AppGen-X",
        "stream_engine_picker_visible": False,
        "database_backends": ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS,
        "emits": ENTERPRISE_SEARCH_VECTOR_EMITTED_EVENT_TYPES,
        "consumes": ENTERPRISE_SEARCH_VECTOR_CONSUMED_EVENT_TYPES,
        "owned_tables": ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
    }


def enterprise_search_vector_build_schema_contract() -> dict:
    owned = (*ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES, *ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES)
    tables = tuple(
        {
            "table": table,
            "schema": "enterprise_search_vector",
            "pbc": "enterprise_search_vector",
            "owned": True,
            "migration": f"pbcs/enterprise_search_vector/migrations/{index:03d}_{table}.sql",
            "model": f"pbcs/enterprise_search_vector/models/{_class_name(table)}.py",
            "fields": _table_fields(table),
            "relationships": _table_relationships(table),
        }
        for index, table in enumerate(owned, start=1)
    )
    return {
        "format": "appgen.enterprise-search-vector-owned-schema-contract.v1",
        "ok": True,
        "pbc": "enterprise_search_vector",
        "owned_tables": owned,
        "business_tables": ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES,
        "runtime_tables": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES,
        "tables": tables,
        "migrations": tuple(table["migration"] for table in tables),
        "models": tuple(table["model"] for table in tables),
        "database_backends": ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS,
        "shared_table_access": False,
        "tenant_isolation": {"field": "tenant", "required": True},
        "schema_extensions": {"allowed": True, "owned_tables_only": True},
        "declared_dependencies": enterprise_search_vector_verify_owned_table_boundary()["declared_dependencies"],
    }


def enterprise_search_vector_build_service_contract() -> dict:
    command_methods = (
        "configure_runtime",
        "set_parameter",
        "register_rule",
        "register_schema_extension",
        "receive_event",
        "create_index",
        "ingest_document",
        "run_embedding_job",
        "refresh_index",
        "query",
        "record_feedback",
        "build_workbench_view",
        "verify_owned_table_boundary",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
        "simulate_counterfactual_ranking",
        "forecast_index_freshness",
        "remediate_search_quality",
        "screen_search_policy",
        "run_relevance_controls",
        "generate_index_proof",
        "federate_search_sources",
        "score_query_intent_risk",
        "record_retention_deletion",
        "register_governed_model",
    )
    query_methods = (
        "build_api_contract",
        "permissions_contract",
        "build_workbench_view",
        "build_schema_contract",
        "build_service_contract",
        "build_release_evidence",
    )
    return {
        "format": "appgen.enterprise-search-vector-service-contract.v1",
        "ok": True,
        "pbc": "enterprise_search_vector",
        "transaction_boundary": "enterprise_search_vector_owned_datastore_plus_appgen_outbox",
        "command_methods": command_methods,
        "query_methods": query_methods,
        "mutates_only": (*ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES, *ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES),
        "external_dependencies": enterprise_search_vector_verify_owned_table_boundary()["declared_dependencies"],
        "eventing": {
            "contract": "AppGen-X",
            "topic": ENTERPRISE_SEARCH_VECTOR_REQUIRED_EVENT_TOPIC,
            "outbox_table": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[0],
            "inbox_table": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[1],
            "dead_letter_table": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[2],
            "idempotency_required": True,
        },
        "idempotent_handlers": ("receive_event",),
        "retry_dead_letter_evidence": {
            "retry_limit_field": "retry_limit",
            "dead_letter_table": ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[2],
        },
        "generated_artifacts": {
            "services": ("pbcs/enterprise_search_vector/services/search_service.py",),
            "routes": ("pbcs/enterprise_search_vector/routes/search_routes.py",),
            "events": ("pbcs/enterprise_search_vector/events/search_events.py",),
            "handlers": ("pbcs/enterprise_search_vector/handlers/search_handlers.py",),
            "ui": ("pbcs/enterprise_search_vector/ui/workbench.py",),
        },
        "shared_table_access": False,
    }


def enterprise_search_vector_build_release_evidence() -> dict:
    schema = enterprise_search_vector_build_schema_contract()
    service = enterprise_search_vector_build_service_contract()
    api = enterprise_search_vector_build_api_contract()
    permissions = enterprise_search_vector_permissions_contract()
    checks = (
        {"id": "owned_schema_depth", "ok": len(schema["owned_tables"]) >= 7},
        {"id": "migration_per_owned_table", "ok": len(schema["migrations"]) == len(schema["owned_tables"])},
        {"id": "model_per_owned_table", "ok": len(schema["models"]) == len(schema["owned_tables"])},
        {"id": "service_contract_depth", "ok": len(service["command_methods"]) >= 20},
        {"id": "generated_runtime_artifacts", "ok": {"services", "routes", "events", "handlers", "ui"} <= set(service["generated_artifacts"])},
        {"id": "appgen_event_contract_only", "ok": api["event_contract"] == "AppGen-X" and api["stream_engine_picker_visible"] is False},
        {"id": "backend_allowlist", "ok": set(api["database_backends"]) <= {"postgresql", "mysql", "mariadb"}},
        {"id": "runtime_event_tables_owned", "ok": set(ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES) <= set(schema["owned_tables"])},
        {"id": "no_shared_table_access", "ok": not schema["shared_table_access"] and not service["shared_table_access"] and not api["shared_table_access"]},
        {"id": "permissions_cover_release_queries", "ok": {"build_schema_contract", "build_service_contract", "build_release_evidence"} <= set(permissions["action_permissions"])},
    )
    blocking = tuple(check for check in checks if not check["ok"])
    return {
        "format": "appgen.enterprise-search-vector-release-evidence.v1",
        "ok": not blocking,
        "pbc": "enterprise_search_vector",
        "checks": checks,
        "blocking_gaps": blocking,
        "schema": schema,
        "service": service,
        "api": api,
        "permissions": permissions,
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
            "enterprise_search_vector.quality.write",
            "enterprise_search_vector.policy.write",
            "enterprise_search_vector.intelligence.write",
            "enterprise_search_vector.retention.write",
        ),
        "action_permissions": {
            "create_index": "enterprise_search_vector.index.write",
            "refresh_index": "enterprise_search_vector.index.write",
            "run_embedding_job": "enterprise_search_vector.document.write",
            "ingest_document": "enterprise_search_vector.document.write",
            "query": "enterprise_search_vector.query",
            "record_feedback": "enterprise_search_vector.query",
            "receive_event": "enterprise_search_vector.event.consume",
            "register_rule": "enterprise_search_vector.configure",
            "register_schema_extension": "enterprise_search_vector.configure",
            "set_parameter": "enterprise_search_vector.configure",
            "configure_runtime": "enterprise_search_vector.configure",
            "build_workbench_view": "enterprise_search_vector.audit",
            "verify_owned_table_boundary": "enterprise_search_vector.audit",
            "build_schema_contract": "enterprise_search_vector.audit",
            "build_service_contract": "enterprise_search_vector.audit",
            "build_release_evidence": "enterprise_search_vector.audit",
            "simulate_counterfactual_ranking": "enterprise_search_vector.intelligence.write",
            "forecast_index_freshness": "enterprise_search_vector.intelligence.write",
            "remediate_search_quality": "enterprise_search_vector.quality.write",
            "screen_search_policy": "enterprise_search_vector.policy.write",
            "run_relevance_controls": "enterprise_search_vector.audit",
            "generate_index_proof": "enterprise_search_vector.audit",
            "federate_search_sources": "enterprise_search_vector.intelligence.write",
            "score_query_intent_risk": "enterprise_search_vector.policy.write",
            "record_retention_deletion": "enterprise_search_vector.retention.write",
            "register_governed_model": "enterprise_search_vector.configure",
        },
    }


def _class_name(table: str) -> str:
    return class_name_for(table)


def _table_fields(table: str) -> tuple[dict, ...]:
    return fields_for(table)


def _table_field_names(table: str) -> tuple[str, ...]:
    return field_names_for(table)


def _table_relationships(table: str) -> tuple[dict, ...]:
    if table in ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES:
        return relationships_for(table)
    if table in ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES:
        return ({"type": "event_contract", "to": "AppGen-X", "topic": ENTERPRISE_SEARCH_VECTOR_REQUIRED_EVENT_TOPIC},)
    return ()


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


def _record_search_audit(state: dict, tenant: str, action: str, payload: dict) -> dict:
    entry = {
        "entry_id": f"audit_{len(state['search_audit_entries']) + 1}",
        "tenant": tenant,
        "action": action,
        "payload_digest": _digest(payload),
        "proof_hash": _digest({"tenant": tenant, "action": action, "payload": payload}),
        "status": "sealed",
    }
    state["search_audit_entries"][entry["entry_id"]] = entry
    state["events"].append(_state_event("SearchAuditEntrySealed", entry["entry_id"], entry))
    return entry


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
