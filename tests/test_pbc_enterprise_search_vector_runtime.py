import pytest

from pyAppGen.pbcs.enterprise_search_vector import ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS
from pyAppGen.pbcs.enterprise_search_vector import ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES
from pyAppGen.pbcs.enterprise_search_vector import ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS
from pyAppGen.pbcs.enterprise_search_vector import ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_build_api_contract
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_build_release_evidence
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_build_schema_contract
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_build_service_contract
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_build_workbench_view
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_configure_runtime
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_create_index
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_empty_state
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_ingest_document
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_permissions_contract
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_query
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_receive_event
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_record_feedback
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_refresh_index
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_register_rule
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_render_workbench
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_run_embedding_job
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_runtime_capabilities
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_runtime_smoke
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_set_parameter
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_ui_contract
from pyAppGen.pbcs.enterprise_search_vector import enterprise_search_vector_verify_owned_table_boundary
from pyAppGen.pbcs.enterprise_search_vector import implementation_contract


def test_enterprise_search_vector_runtime_executes_standard_and_advanced_capabilities() -> None:
    runtime = enterprise_search_vector_runtime_capabilities()
    smoke = enterprise_search_vector_runtime_smoke()
    contract = implementation_contract()

    assert runtime["format"] == "appgen.enterprise-search-vector-runtime-capabilities.v1"
    assert runtime["ok"] is True
    assert runtime["implementation_directory"] == "src/pyAppGen/pbcs/enterprise_search_vector"
    assert runtime["owned_tables"] == ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES
    assert len(runtime["standard_features"]) >= 20
    assert "configuration_schema" in runtime["standard_features"]
    assert "rule_engine" in runtime["standard_features"]
    assert "workbench" in runtime["standard_features"]
    assert smoke["ok"] is True
    assert {check["id"] for check in smoke["checks"]} == set(ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS)
    assert not smoke["blocking_gaps"]

    assert contract["format"] == "appgen.pbc-source-package.v1"
    assert contract["side_effect_free"] is True
    assert contract["advanced_runtime"]["ok"] is True
    assert contract["ui_contract"]["ok"] is True
    assert contract["schema_contract"]["ok"] is True
    assert contract["service_contract"]["ok"] is True
    assert contract["release_evidence"]["ok"] is True
    assert "SearchConfigurationPanel" in contract["ui_contract"]["fragments"]
    assert contract["runtime_tables"] == ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES
    assert set(contract["advanced_runtime"]["capabilities"]) == set(
        ENTERPRISE_SEARCH_VECTOR_RUNTIME_CAPABILITY_KEYS
    )


def test_enterprise_search_vector_runtime_applies_rules_parameters_queries_and_ui() -> None:
    state = _configured_state()
    for command in (
        {
            "index_id": "idx_product_ops",
            "tenant": "tenant_ops",
            "name": "Product Search",
            "source": "product",
            "locale": "en-US",
            "status": "active",
        },
        {
            "index_id": "idx_customer_ops",
            "tenant": "tenant_ops",
            "name": "Customer Search",
            "source": "customer",
            "locale": "en-US",
            "status": "active",
        },
        {
            "index_id": "idx_audit_ops",
            "tenant": "tenant_ops",
            "name": "Audit Search",
            "source": "audit",
            "locale": "en-US",
            "status": "active",
        },
        {
            "index_id": "idx_knowledge_ops",
            "tenant": "tenant_ops",
            "name": "Knowledge Search",
            "source": "knowledge",
            "locale": "en-US",
            "status": "active",
        },
    ):
        state = enterprise_search_vector_create_index(state, command)["state"]

    state = enterprise_search_vector_receive_event(
        state,
        {
            "event_id": "evt_product_ops",
            "event_type": "ProductPublished",
            "payload": {
                "tenant": "tenant_ops",
                "document_id": "doc_product_ops",
                "title": "Warehouse Camera",
                "body": "Mirrorless camera stocked in the east warehouse",
                "source": "product",
                "locale": "en-US",
                "acl": ("search.read",),
            },
        },
    )["state"]
    duplicate = enterprise_search_vector_receive_event(
        state,
        {
            "event_id": "evt_product_ops",
            "event_type": "ProductPublished",
            "payload": {
                "tenant": "tenant_ops",
                "document_id": "doc_product_ops",
                "title": "Warehouse Camera",
                "body": "Mirrorless camera stocked in the east warehouse",
                "source": "product",
                "locale": "en-US",
                "acl": ("search.read",),
            },
        },
    )
    state = duplicate["state"]
    assert duplicate["handler"]["status"] == "duplicate"

    for event in (
        {
            "event_id": "evt_customer_ops",
            "event_type": "CustomerUpdated",
            "payload": {
                "tenant": "tenant_ops",
                "document_id": "doc_customer_ops",
                "title": "Customer Ada",
                "body": "Ada searches for fulfillment exception steps weekly",
                "source": "customer",
                "locale": "en-US",
                "acl": ("search.read",),
            },
        },
        {
            "event_id": "evt_audit_ops",
            "event_type": "AuditEventSealed",
            "payload": {
                "tenant": "tenant_ops",
                "document_id": "doc_audit_ops",
                "title": "Search Audit",
                "body": "Audit confirms index refresh and relevance control evidence",
                "source": "audit",
                "locale": "en-US",
                "acl": ("search.read",),
            },
        },
    ):
        state = enterprise_search_vector_receive_event(state, event)["state"]

    state = enterprise_search_vector_ingest_document(
        state,
        {
            "document_id": "doc_knowledge_ops",
            "tenant": "tenant_ops",
            "source": "knowledge",
            "locale": "en-US",
            "title": "Warehouse exception playbook",
            "body": "Delayed fulfillment exception and guided recovery workflow",
            "acl": ("search.read",),
        },
    )["state"]
    state = enterprise_search_vector_run_embedding_job(
        state,
        {
            "job_id": "job_ops",
            "tenant": "tenant_ops",
            "index_id": "idx_knowledge_ops",
            "document_ids": ("doc_knowledge_ops",),
            "status": "completed",
        },
    )["state"]

    result = enterprise_search_vector_query(
        state,
        {
            "query_id": "query_ops",
            "tenant": "tenant_ops",
            "text": "fulfillment exception recovery",
            "principal_permissions": ("search.read",),
            "locale": "en-US",
        },
    )
    state = result["state"]
    assert result["results"]
    assert result["results"][0]["document_id"] == "doc_knowledge_ops"

    state = enterprise_search_vector_record_feedback(
        state,
        "query_ops",
        "doc_knowledge_ops",
        rating=1.0,
    )["state"]
    state = enterprise_search_vector_refresh_index(
        state,
        {
            "refresh_id": "refresh_ops",
            "tenant": "tenant_ops",
            "index_id": "idx_knowledge_ops",
            "reason": "quality_rebuild",
            "status": "completed",
        },
    )["state"]

    workbench = enterprise_search_vector_build_workbench_view(state, tenant="tenant_ops")
    assert workbench["index_count"] == 4
    assert workbench["active_index_count"] == 4
    assert workbench["embedding_job_count"] == 1
    assert workbench["document_count"] == 4
    assert workbench["ready_document_count"] == 1
    assert workbench["query_count"] == 1
    assert workbench["feedback_count"] == 1
    assert workbench["configuration_bound"] is True
    assert workbench["rule_count"] == 1
    assert workbench["parameter_count"] == 10
    assert workbench["binding_evidence"]["event_contract"] == "appgen_event_contract"

    ui_contract = enterprise_search_vector_ui_contract()
    assert ui_contract["configuration_editor"]["allowed_database_backends"] == (
        ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS
    )
    assert ui_contract["configuration_editor"]["stream_engine_picker_visible"] is False
    assert ui_contract["event_surfaces"]["contract"] == "appgen_event_contract"
    rendered = enterprise_search_vector_render_workbench(
        state,
        tenant="tenant_ops",
        principal_permissions=(
            "enterprise_search_vector.index.write",
            "enterprise_search_vector.document.write",
            "enterprise_search_vector.query",
            "enterprise_search_vector.event.consume",
            "enterprise_search_vector.configure",
            "enterprise_search_vector.audit",
        ),
    )
    assert rendered["ok"] is True
    assert not rendered["locked_actions"]
    assert rendered["binding_evidence"]["owned_tables"] == ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES

    outbox_event_types = {event["event_type"] for event in state["outbox"]}
    assert {"SearchIndexUpdated", "DiscoveryInsightGenerated"} <= outbox_event_types

    api_contract = enterprise_search_vector_build_api_contract()
    assert "POST /query-feedback" in api_contract["routes"]
    assert api_contract["shared_table_access"] is False
    assert api_contract["database_backends"] == ENTERPRISE_SEARCH_VECTOR_ALLOWED_DATABASE_BACKENDS
    permissions = enterprise_search_vector_permissions_contract()
    assert "enterprise_search_vector.query" in permissions["permissions"]
    assert permissions["action_permissions"]["build_release_evidence"] == "enterprise_search_vector.audit"

    schema = enterprise_search_vector_build_schema_contract()
    service = enterprise_search_vector_build_service_contract()
    release = enterprise_search_vector_build_release_evidence()
    assert set(ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES) <= set(schema["owned_tables"])
    assert len(schema["migrations"]) == len(schema["owned_tables"])
    assert all(path.startswith("pbcs/enterprise_search_vector/migrations/") for path in schema["migrations"])
    assert service["eventing"]["contract"] == "AppGen-X"
    assert service["eventing"]["dead_letter_table"] == ENTERPRISE_SEARCH_VECTOR_RUNTIME_TABLES[2]
    assert "receive_event" in service["idempotent_handlers"]
    assert {"services", "routes", "events", "handlers", "ui"} <= set(service["generated_artifacts"])
    assert release["ok"] is True
    assert not release["blocking_gaps"]


def test_enterprise_search_vector_rejects_invalid_inputs_and_proves_boundary_and_dead_letters() -> None:
    state = enterprise_search_vector_empty_state()
    with pytest.raises(ValueError, match="PostgreSQL, MySQL, or MariaDB"):
        enterprise_search_vector_configure_runtime(
            state,
            {
                "database_backend": "stream_store",
                "event_topic": "appgen.enterprise_search_vector.events",
                "retry_limit": 3,
                "default_locale": "en-US",
                "supported_locales": ("en-US",),
                "supported_sources": ("knowledge",),
                "embedding_dimensions": 8,
                "retention_days": 365,
                "ranking_mode": "hybrid",
                "workbench_limit": 50,
            },
        )

    state = _configured_state(
        supported_sources=("product", "customer", "audit", "knowledge"),
        allowed_sources=("knowledge",),
    )
    with pytest.raises(ValueError, match="Unsupported Enterprise Search Vector parameter"):
        enterprise_search_vector_set_parameter(state, "stream_engine", 1)

    state = enterprise_search_vector_create_index(
        state,
        {
            "index_id": "idx_guard_ops",
            "tenant": "tenant_ops",
            "name": "Guarded Search",
            "source": "knowledge",
            "locale": "en-US",
            "status": "active",
        },
    )["state"]
    with pytest.raises(ValueError, match="source not allowed by rule"):
        enterprise_search_vector_ingest_document(
            state,
            {
                "document_id": "doc_forbidden_ops",
                "tenant": "tenant_ops",
                "source": "product",
                "locale": "en-US",
                "title": "Forbidden",
                "body": "Should not pass rule policy",
                "acl": ("search.read",),
            },
        )

    failed = enterprise_search_vector_receive_event(
        state,
        {"event_id": "evt_fail", "event_type": "AuditEventSealed", "payload": {"tenant": "tenant_ops"}},
        simulate_failure=True,
    )
    assert failed["ok"] is False
    assert failed["handler"]["status"] == "dead_letter"
    assert len(failed["state"]["dead_letter"]) == 1

    boundary = enterprise_search_vector_verify_owned_table_boundary()
    assert boundary["ok"] is True
    assert boundary["owned_tables"] == ENTERPRISE_SEARCH_VECTOR_OWNED_TABLES
    assert boundary["declared_dependencies"]["shared_tables"] == ()


def _configured_state(
    *,
    supported_sources: tuple[str, ...] = ("product", "customer", "audit", "knowledge"),
    allowed_sources: tuple[str, ...] = ("product", "customer", "audit", "knowledge"),
) -> dict:
    state = enterprise_search_vector_empty_state()
    state = enterprise_search_vector_configure_runtime(
        state,
        {
            "database_backend": "postgresql",
            "event_topic": "appgen.enterprise_search_vector.events",
            "retry_limit": 3,
            "default_locale": "en-US",
            "supported_locales": ("en-US",),
            "supported_sources": supported_sources,
            "embedding_dimensions": 8,
            "retention_days": 365,
            "ranking_mode": "hybrid",
            "workbench_limit": 50,
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
        ("workbench_limit", 50),
    ):
        state = enterprise_search_vector_set_parameter(state, name, value)["state"]
    state = enterprise_search_vector_register_rule(
        state,
        {
            "rule_id": "rule_ops",
            "tenant": "tenant_ops",
            "scope": "enterprise_search_vector",
            "status": "active",
            "allowed_sources": allowed_sources,
            "allowed_locales": ("en-US",),
            "acl_policy": {"require_acl_match": True, "default_acl": ("search.read",)},
            "ranking_policy": {"hybrid": True, "minimum_relevance": 0.1},
            "retention_policy": {"retention_days": 365, "legal_hold_supported": True},
        },
    )["state"]
    return state
